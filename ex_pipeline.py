# 使用 SQLAlchemy 创建一个连接到名为 chinook.db 的 SQLite 数据库的引擎
import os
os.environ["OPENAI_API_KEY"] = "sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11"
from llama_index.core import SQLDatabase
from sqlalchemy import create_engine

engine = create_engine("sqlite:///chinook.db")  # 创建一个连接到 'chinook.db' 的 SQLite 数据库引擎
sql_database = SQLDatabase(engine)  # 使用 LlamaIndex 的 SQLDatabase 类对引擎进行包装


# from llama_index.core.query_pipeline import QueryPipeline
#
# # 设置可观测性
# import phoenix as px
# import llama_index.core
#
# px.launch_app()
# llama_index.core.set_global_handler("arize_phoenix")


# 设置 Text-to-SQL 查询引擎/工具
# 给定一个查询，将文本转换为 SQL，针对数据库执行，并返回结果。
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
import openai

openai.api_key = "sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11"
openai.base_url = 'https://api.gptapi.us/v1/chat/completions'


Settings.llm = OpenAI(
    model="gpt-4o-mini",
    api_key=openai.api_key,
    base_url=openai.base_url
)

sql_query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["albums", "tracks", "artists"],
    verbose=True,
    llm=Settings.llm  # 确保这里使用了正确的 llm
)

# sql_query_engine = NLSQLTableQueryEngine(
#     sql_database=sql_database,
#     tables=["albums", "tracks", "artists"],
#     verbose=True,
# )

sql_tool = QueryEngineTool.from_defaults(
    query_engine=sql_query_engine,
    name="sql_tool",
    description=(
        "Useful for translating a natural language query into a SQL query"
    ),
)


# 设置 ReAct 代理管道
from llama_index.core.query_pipeline import QueryPipeline as QP

qp = QP(verbose=True)


# 定义代理输入组件
from llama_index.core.agent.react.types import (
    ActionReasoningStep,
    ObservationReasoningStep,
    ResponseReasoningStep,
)
from llama_index.core.agent import Task, AgentChatResponse
from llama_index.core.query_pipeline import (
    StatefulFnComponent,
    QueryComponent,
    ToolRunnerComponent,
)
from llama_index.core.llms import MessageRole
from typing import Dict, Any, Optional, Tuple, List, cast


# Input Component
## This is the component that produces agent inputs to the rest of the components
## Can also put initialization logic here.
def agent_input_fn(state: Dict[str, Any]) -> str:
    """Agent input function.

    Returns:
        A Dictionary of output keys and values. If you are specifying
        src_key when defining links between this component and other
        components, make sure the src_key matches the specified output_key.

    """
    task = state["task"]
    if len(state["current_reasoning"]) == 0:
        reasoning_step = ObservationReasoningStep(observation=task.input)
        state["current_reasoning"].append(reasoning_step)
    return task.input


agent_input_component = StatefulFnComponent(fn=agent_input_fn)


# 定义代理提示符
from llama_index.core.agent import ReActChatFormatter
from llama_index.core.query_pipeline import InputComponent, Link
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool


## define prompt function
def react_prompt_fn(
    state: Dict[str, Any], input: str, tools: List[BaseTool]
) -> List[ChatMessage]:
    task = state["task"]
    # Add input to reasoning
    chat_formatter = ReActChatFormatter()
    cur_prompt = chat_formatter.format(
        tools,
        chat_history=task.memory.get(),
        current_reasoning=state["current_reasoning"],
    )
    return cur_prompt


react_prompt_component = StatefulFnComponent(
    fn=react_prompt_fn, partial_dict={"tools": [sql_tool]}
)


# 定义代理输出解析器 + 工具管道
from typing import Set, Optional
from llama_index.core.agent.react.output_parser import ReActOutputParser
from llama_index.core.llms import ChatResponse
from llama_index.core.agent.types import Task


def parse_react_output_fn(state: Dict[str, Any], chat_response: ChatResponse):
    """Parse ReAct output into a reasoning step."""
    output_parser = ReActOutputParser()
    reasoning_step = output_parser.parse(chat_response.message.content)
    return {"done": reasoning_step.is_done, "reasoning_step": reasoning_step}


parse_react_output = StatefulFnComponent(fn=parse_react_output_fn)


def run_tool_fn(state: Dict[str, Any], reasoning_step: ActionReasoningStep):
    """Run tool and process tool output."""
    task = state["task"]
    tool_runner_component = ToolRunnerComponent(
        [sql_tool], callback_manager=task.callback_manager
    )
    tool_output = tool_runner_component.run_component(
        tool_name=reasoning_step.action,
        tool_input=reasoning_step.action_input,
    )
    observation_step = ObservationReasoningStep(observation=str(tool_output))
    state["current_reasoning"].append(observation_step)
    # TODO: get output

    # return tuple of current output and False for is_done
    return observation_step.get_content(), False


run_tool = StatefulFnComponent(fn=run_tool_fn)


def process_response_fn(
    state: Dict[str, Any], response_step: ResponseReasoningStep
):
    """Process response."""
    state["current_reasoning"].append(response_step)
    return response_step.response, True


process_response = StatefulFnComponent(fn=process_response_fn)

# 将 Agent Query Pipeline 拼接在一起
from llama_index.core.query_pipeline import QueryPipeline as QP

qp.add_modules({
    "agent_input": agent_input_component,       # 1. 解析输入
    "react_prompt": react_prompt_component,     # 2. 生成 GPT-3.5 提示词
    "llm": OpenAI(model="gpt-3.5-turbo", api_key=openai.api_key, base_url=openai.base_url),  # 3. 运行 LLM
    "react_output_parser": parse_react_output,  # 4. 解析 LLM 输出
    "run_tool": run_tool,                       # 5. 运行 SQL 查询
    "process_response": process_response,       # 6. 处理查询结果
})


# link input to react prompt to parsed out response (either tool action/input or observation)
qp.add_chain(["agent_input", "react_prompt", "llm", "react_output_parser"])

# add conditional link from react output to tool call (if not done)
qp.add_link(
    "react_output_parser",
    "run_tool",
    condition_fn=lambda x: not x["done"],
    input_fn=lambda x: x["reasoning_step"],
)
# add conditional link from react output to final response processing (if done)
qp.add_link(
    "react_output_parser",
    "process_response",
    condition_fn=lambda x: x["done"],
    input_fn=lambda x: x["reasoning_step"],
)

# 可视化查询管道
from pyvis.network import Network

net = Network(notebook=True, cdn_resources="in_line", directed=True)
net.from_nx(qp.clean_dag)
html_content = net.generate_html()
with open("agent_dag.html", "w", encoding="utf-8") as f:
    f.write(html_content)


# 围绕 Text-to-SQL Query Pipeline 设置 Agent Worker
from llama_index.core.agent import FnAgentWorker
from typing import Dict, Tuple, Any


def run_agent_fn(state: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    """Run agent function."""
    task, qp = state["__task__"], state["query_pipeline"]
    # if first run, then set query pipeline state to initial variables
    if state["is_first"]:
        qp.set_state(
            {
                "task": task,
                "current_reasoning": [],
            }
        )
        state["is_first"] = False

    # no explicit input here, just run root node
    response_str, is_done = qp.run()
    # if done, store output and log to memory
    # a core memory module is available in the `task` variable. Of course you can log
    # and store your own memory as well
    state["__output__"] = response_str
    if is_done:
        task.memory.put_messages(
            [
                ChatMessage(content=task.input, role=MessageRole.USER),
                ChatMessage(content=response_str, role=MessageRole.ASSISTANT),
            ]
        )
    return state, is_done


agent = FnAgentWorker(
    fn=run_agent_fn,
    initial_state={"query_pipeline": qp, "is_first": True},
).as_agent()


# 运行代理
# start task
task = agent.create_task(
    "What are some tracks from the artist AC/DC? Limit it to 3"
)

# 运行任务，直到任务完成
while True:
    step_output = agent.run_step(task.task_id)

    # 确保任务到达最后一步
    if step_output.is_last:
        break

# 确保任务已经执行完毕后，再调用 finalize_response()
response = agent.finalize_response(task.task_id)

# 打印最终查询结果
print(str(response))



"""
D:\deep_learning\Anaconda\envs\lamaindex\python.exe D:/Desktop/xas/lamaIndex/pipeline.py
> Running module agent_input with input: 

> Running module react_prompt with input: 
input: What are some tracks from the artist AC/DC? Limit it to 3

> Running module llm with input: 
messages: [ChatMessage(role=<MessageRole.SYSTEM: 'system'>, content='You are designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.\n\n## Tools\n\n...

> Running module react_output_parser with input: 
chat_response: assistant: ```
Thought: The current language of the user is: English. I need to use a tool to help me answer the question.
Action: sql_tool
Action Input: {"input": "What are some tracks from the artis...

> Running module run_tool with input: 
reasoning_step: thought='The current language of the user is: English. I need to use a tool to help me answer the question.' action='sql_tool' action_input={'input': 'What are some tracks from the artist AC/DC? Limit...

> Table desc str: Table 'albums' has columns: AlbumId (INTEGER), Title (NVARCHAR(160)), ArtistId (INTEGER),  and foreign keys: ['ArtistId'] -> artists.['ArtistId'].

Table 'tracks' has columns: TrackId (INTEGER), Name (NVARCHAR(200)), AlbumId (INTEGER), MediaTypeId (INTEGER), GenreId (INTEGER), Composer (NVARCHAR(220)), Milliseconds (INTEGER), Bytes (INTEGER), UnitPrice (NUMERIC(10, 2)),  and foreign keys: ['MediaTypeId'] -> media_types.['MediaTypeId'], ['GenreId'] -> genres.['GenreId'], ['AlbumId'] -> albums.['AlbumId'].

Table 'artists' has columns: ArtistId (INTEGER), Name (NVARCHAR(120)), .
> Predicted SQL query: SELECT tracks.Name
FROM tracks
JOIN albums ON tracks.AlbumId = albums.AlbumId
JOIN artists ON albums.ArtistId = artists.ArtistId
WHERE artists.Name = 'AC/DC'
LIMIT 3;
> Running module agent_input with input: 

> Running module react_prompt with input: 
input: What are some tracks from the artist AC/DC? Limit it to 3

> Running module llm with input: 
messages: [ChatMessage(role=<MessageRole.SYSTEM: 'system'>, content='You are designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.\n\n## Tools\n\n...

> Running module react_output_parser with input: 
chat_response: assistant: Thought: I can answer without using any more tools. I'll use the user's language to answer

Answer: Here are three tracks from the artist AC/DC:

- For Those About To Rock (We Salute You)
-...

> Running module process_response with input: 
response_step: thought="I can answer without using any more tools. I'll use the user's language to answer" response="Here are three tracks from the artist AC/DC:\n\n- For Those About To Rock (We Salute You)\n- Put T...

Here are three tracks from the artist AC/DC:

- For Those About To Rock (We Salute You)
- Put The Finger On You
- Let's Get It Up

Process finished with exit code 0
"""
