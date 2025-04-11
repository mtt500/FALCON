import json
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.query_pipeline import QueryPipeline as QP
from llama_index.core.agent.react.types import ActionReasoningStep, ObservationReasoningStep, ResponseReasoningStep
from llama_index.core.query_pipeline import StatefulFnComponent
from llama_index.core.llms import MessageRole
from typing import Dict, Any, Tuple, List
import openai
from llama_index.core.agent.react.output_parser import ReActOutputParser
from llama_index.core.agent import ReActChatFormatter
from llama_index.core.llms import ChatMessage
from llama_index.core.llms import ChatResponse
from llama_index.core.agent import FnAgentWorker

# 设置 OpenAI API 密钥
openai.api_key = "sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11"
openai.base_url = 'https://api.gptapi.us/v1/chat/completions'

# 设置 LlamaIndex 使用的模型
Settings.llm = OpenAI(
    model="gpt-3.5-turbo",
    api_key=openai.api_key,
    base_url=openai.base_url,
)


# 定义一个简单的工具，模拟检查 C 语言函数片段中的漏洞
def simple_vulnerability_checker(c_code: str) -> str:
    """模拟检查 C 语言代码中的漏洞"""
    # 这里只是一个简单的模拟，实际上你可以检查更复杂的漏洞，如缓冲区溢出、SQL 注入等。
    if "strcpy" in c_code:
        return "Vulnerability found: Possible buffer overflow due to strcpy."
    elif "scanf" in c_code:
        return "Vulnerability found: Possible buffer overflow due to scanf."
    else:
        return "No vulnerabilities found."


# 读取 C 语言代码的函数
def read_c_code_from_file(file_path: str) -> str:
    """
    从指定的文件读取 C 语言代码。

    参数:
    file_path (str): C 语言源代码文件的路径。

    返回:
    str: 文件中的 C 语言代码。
    """
    try:
        with open(file_path, "r") as file:
            return file.read()  # 返回文件内容
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""


# 输出漏洞检测结果为 JSON 文件的函数
def output_vulnerability_report_as_json(report_data: dict, output_file: str):
    """
    将漏洞检测结果保存为 JSON 文件。

    参数:
    report_data (dict): 包含漏洞信息的字典。
    output_file (str): 输出 JSON 文件的路径。
    """
    try:
        with open(output_file, "w") as json_file:
            json.dump(report_data, json_file, indent=4)  # 将结果写入 JSON 文件
        print(f"Vulnerability report saved to {output_file}")
    except Exception as e:
        print(f"Error writing JSON to {output_file}: {e}")


# 定义代理输入组件
def agent_input_fn(state: Dict[str, Any]) -> str:
    """代理输入函数，返回任务输入"""
    task = state["task"]
    if len(state["current_reasoning"]) == 0:
        reasoning_step = ObservationReasoningStep(observation=task.input)
        state["current_reasoning"].append(reasoning_step)
    return task.input


# agent_input_component 是一个 StatefulFnComponent，它执行该函数并将其作为代理的输入
agent_input_component = StatefulFnComponent(fn=agent_input_fn)


# 定义代理提示符生成函数
def react_prompt_fn(state: Dict[str, Any], input: str, tools: List) -> List:
    task = state["task"]  # 从状态中提取当前的任务
    chat_formatter = ReActChatFormatter()  # 创建一个 ReActChatFormatter 实例，用于格式化聊天内容
    cur_prompt = chat_formatter.format(
        tools,  # 传入工具
        chat_history=task.memory.get(),  # 获取任务的聊天历史
        current_reasoning=state["current_reasoning"],  # 获取当前的推理步骤
    )
    return cur_prompt  # 返回生成的提示符


# react_prompt_component 使用 StatefulFnComponent 将该函数包装成一个代理组件
react_prompt_component = StatefulFnComponent(
    fn=react_prompt_fn, partial_dict={"tools": []}  # 无需SQL工具，移除SQL部分
)


# 定义代理输出解析器，从 GPT 响应中提取推理步骤，并判断推理是否完成
def parse_react_output_fn(state: Dict[str, Any], chat_response: ChatResponse):
    """解析ReAct输出"""
    output_parser = ReActOutputParser()
    reasoning_step = output_parser.parse(chat_response.message.content)
    return {"done": reasoning_step.is_done, "reasoning_step": reasoning_step}  # 返回是否完成推理的标志和推理步骤


parse_react_output = StatefulFnComponent(fn=parse_react_output_fn)


# 定义工具运行函数
def run_tool_fn(state: Dict[str, Any], reasoning_step: ActionReasoningStep):
    """运行工具并处理输出"""
    task = state["task"]
    c_code = task.input  # 获取 C 语言代码片段
    result = simple_vulnerability_checker(c_code)  # 使用工具检查漏洞
    observation_step = ObservationReasoningStep(observation=result)
    state["current_reasoning"].append(observation_step)
    return observation_step.get_content(), False


# run_tool 是一个 StatefulFnComponent，它模拟执行工具并返回结果
run_tool = StatefulFnComponent(fn=run_tool_fn)


# 定义处理响应的函数
def process_response_fn(state: Dict[str, Any], response_step: ResponseReasoningStep):
    """处理响应步骤"""
    state["current_reasoning"].append(response_step)
    return response_step.response, True


process_response = StatefulFnComponent(fn=process_response_fn)

# 设置查询管道，将上述各个组件组合成一个查询管道
qp = QP(verbose=True)
qp.add_modules({
    "agent_input": agent_input_component,       # 1. 解析输入
    "react_prompt": react_prompt_component,     # 2. 生成 GPT 提示词
    "llm": OpenAI(model="gpt-3.5-turbo", api_key=openai.api_key, base_url=openai.base_url),  # 3. 运行 LLM
    "react_output_parser": parse_react_output,  # 4. 解析 LLM 输出
    "run_tool": run_tool,                       # 5. 运行漏洞检测工具
    "process_response": process_response,       # 6. 处理查询结果
})

# 添加模块链（将各个组件按顺序连接起来）
qp.add_chain(["agent_input", "react_prompt", "llm", "react_output_parser"])

# 添加条件链（如果没有完成推理步骤，则执行工具运行；如果完成，则处理响应）
qp.add_link(
    "react_output_parser",
    "run_tool",
    condition_fn=lambda x: not x["done"],
    input_fn=lambda x: x["reasoning_step"],
)

qp.add_link(
    "react_output_parser",
    "process_response",
    condition_fn=lambda x: x["done"],
    input_fn=lambda x: x["reasoning_step"],
)


# 定义代理任务执行函数
def run_agent_fn(state: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    """执行代理任务"""
    task, qp = state["__task__"], state["query_pipeline"]
    if state["is_first"]:
        qp.set_state(
            {
                "task": task,
                "current_reasoning": [],
            }
        )
        state["is_first"] = False
    response_str, is_done = qp.run()
    state["__output__"] = response_str
    if is_done:
        task.memory.put_messages(
            [
                ChatMessage(content=task.input, role=MessageRole.USER),
                ChatMessage(content=response_str, role=MessageRole.ASSISTANT),
            ]
        )
    return state, is_done


# 创建代理
agent = FnAgentWorker(
    fn=run_agent_fn,
    initial_state={"query_pipeline": qp, "is_first": True},
).as_agent()

c_code = read_c_code_from_file("ex_val.c")  # 读取文件中的 C 语言代码

if not c_code:
    print("Error: Failed to read C code from file.")
    exit(1)  # 如果读取失败，退出程序或做其他处理

custom_prompt = f"""
Your task is to analyze the following C code and return a JSON object with the following fields:
- function_name: The name of the function being analyzed.
- is_vulnerable: A boolean indicating whether the code contains a vulnerability.
- vulnerability_type: The type of vulnerability found (e.g., buffer overflow, command injection).
- severity: The severity of the vulnerability (e.g., low, medium, high).
- description: A detailed description of the vulnerability, explaining why it is a vulnerability and how it can be exploited.

Please return the analysis in the following JSON format:
{{
    "function_name": "function_name_here",
    "is_vulnerable": true_or_false,
    "vulnerability_type": "vulnerability_type_here",
    "severity": "severity_level_here",
    "description": "detailed_description_here"
}}
"""

# 启动代理任务
task = agent.create_task(f"You are a security expert analyzing C code for vulnerabilities. Check if the following c code snippet contains vulnerability.\n c code: {c_code}")

# 运行任务，直到任务完成
while True:
    step_output = agent.run_step(task.task_id)
    if step_output.is_last:
        break

# 完成响应
response = agent.finalize_response(task.task_id)
print(str(response))



'''
1.0 版输出
D:\deep_learning\Anaconda\envs\lamaindex\python.exe D:/Desktop/xas/FALCON/gjj_decision_agent/decision_agent.py
> Running module agent_input with input: 

> Running module react_prompt with input: 
input: Check if the following C code contains vulnerabilities: 
char buf[10]; 
strcpy(buf, "A very long string!");

> Running module llm with input: 
messages: [ChatMessage(role=<MessageRole.SYSTEM: 'system'>, content='You are designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.\n\n## Tools\n\n...

> Running module react_output_parser with input: 
chat_response: assistant: Thought: I need to analyze the provided C code to check for vulnerabilities.
Action: `CodeQL`
Action Input: {"code": "char buf[10];\nstrcpy(buf, \"A very long string!\");"}

> Running module run_tool with input: 
reasoning_step: thought='I need to analyze the provided C code to check for vulnerabilities.' action='`CodeQL`' action_input={'code': 'char buf[10];\nstrcpy(buf, "A very long string!");'}

> Running module agent_input with input: 

> Running module react_prompt with input: 
input: Check if the following C code contains vulnerabilities: 
char buf[10]; 
strcpy(buf, "A very long string!");

> Running module llm with input: 
messages: [ChatMessage(role=<MessageRole.SYSTEM: 'system'>, content='You are designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.\n\n## Tools\n\n...

> Running module react_output_parser with input: 
chat_response: assistant: Thought: I can answer without using any more tools. I'll use the user's language to answer
Answer: Yes, the provided C code contains a vulnerability. The use of strcpy to copy a long string...

> Running module process_response with input: 
response_step: thought="I can answer without using any more tools. I'll use the user's language to answer" response='Yes, the provided C code contains a vulnerability. The use of strcpy to copy a long string into a ...

Yes, the provided C code contains a vulnerability. The use of strcpy to copy a long string into a buffer of size 10 can lead to a buffer overflow, which is a security risk.

Process finished with exit code 0



2.0版输出（从文件中读代码并输出成json文件）
'''