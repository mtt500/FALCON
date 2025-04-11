import nltk

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

import os
import subprocess

os.environ["OPENAI_API_KEY"] = "sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11"
os.environ["OPENAI_API_BASE"] = "https://api.gptapi.us/v1/chat/completions"

# from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings

# 初始化 OpenAI 模型
llm = OpenAI(model="gpt-4o", max_retries=3, temperature=1)
Settings.llm = llm


from llama_index.core.settings import Settings
from llama_index.core.callbacks import CallbackManager

# 初始化回调管理器
callback_manager = CallbackManager()
Settings.callback_manager = callback_manager

# 设置 Arize Phoenix 进行日志记录和可观测性
# import phoenix as px
# import llama_index.core
#
#
# px.launch_app()  # 启动 Arize Phoenix 应用
# llama_index.core.set_global_handler("arize_phoenix")  # 设置全局处理器



# 加载 Suricata 规则文档
from llama_index.readers.file import UnstructuredReader
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from pathlib import Path
from tqdm import tqdm

# 定义规则文件路径
path = "D:/Desktop/xas/pcap-agent/suricata/doc/userguide/rules"
loader = UnstructuredReader()
docs = []

# 遍历规则文件夹，加载规则
for file in os.listdir(path):
    if file.endswith(".rst") and 'keywords' in file:
        rpath = os.path.join(path, file)
        first_line = open(rpath, "r").readline()
        title = file.replace(".rst", "-")
        doc = loader.load_data(Path(rpath), split_documents=False)
        for d in doc:
            d.metadata = {"title": title}
        docs.append((title, doc))

docs_with_index = []

# 为每个规则创建索引
for title, doc in tqdm(docs):
    loaded = False
    try:
        storage_context = StorageContext.from_defaults(persist_dir=f"./rag-storage/{title}")
        index = load_index_from_storage(storage_context)
        loaded = True
    except Exception as e:
        print(e)

    if not loaded:
        index = VectorStoreIndex.from_documents(doc, show_progress=True)
        index.storage_context.persist(persist_dir=f"./rag-storage/{title}")

    docs_with_index.append((title, doc, index))


# 导入查询引擎工具
from llama_index.core.tools import QueryEngineTool, ToolMetadata

# QueryEngineTool 是用于将查询引擎转换为 function call 的工具
individual_query_engine_tools = [
    QueryEngineTool(
        query_engine=index.as_query_engine(),
        metadata=ToolMetadata(
            name=f"vector_index_{title}",
            description=(
                "suricate rules for protocol "f" {title}"
            ),
        ),
    )
    for title, _, index in docs_with_index
]

# 导入子问题查询引擎
from llama_index.core.query_engine import SubQuestionQueryEngine

# 初始化子问题查询引擎
query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=individual_query_engine_tools,

)

# 创建查询引擎工具
query_engine_tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="sub_question_query_engine",
        description=(
            "用于查询 Suricata 规则文档的引擎，适用于查询协议（如 TCP、UDP、HTTP 等）的规则。"
        ),
    ),
)


import nest_asyncio  # 导入异步IO库

nest_asyncio.apply()  # 应用异步IO补丁


def tshark_tool(tshark_command: str):
    """
    运行指定的 tshark 命令，并返回其输出结果。
    1. 不要使用 '-V' 选项，因为它会打印过多信息，影响可读性。
    2. '-r' 选项后需要跟 pcap 文件路径，路径需要用双引号括起来。
    3. 必须使用其他选项或过滤器来过滤结果，否则结果过多，影响可读性。
    :param tshark_command: tshark 命令字符串
    :return: 命令执行结果或错误信息
    """
    try:
        if not tshark_command.startswith("tshark"):
            tshark_command = "tshark " + tshark_command
        print(tshark_command)
        tshark_command = tshark_command.replace("\"", "")

        if len(tshark_command.split()) <= 3:
            return "错误：命令过短，请使用选项或过滤器来过滤结果。"

        result = subprocess.run(
            tshark_command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(e)
        return f"错误：tshark 执行失败：{e}"
    except FileNotFoundError:
        return "错误：未找到 tshark。请安装 Wireshark/tshark。"



# 示例：使用 tshark 工具分析 pcap 文件
tshark_tool("""tshark -r "./dataset/06脆弱性漏洞攻击类事件/01MS-Office 文件脆弱性/24197-内存破坏漏洞(CVE-2018-0758).pcap" -Y "data\"""")



from llama_index.core.tools import FunctionTool  # 导入函数工具

# 创建 tshark 工具的函数工具
fn_tool_tshark_tool = FunctionTool.from_defaults(fn=tshark_tool)



from llama_index.agent.openai import OpenAIAgent
from llama_index.core.llms import ChatMessage

# 定义系统提示词
system_prompt = """
You are a helpful pcap analysis assistant(agent). you can use tshark to analyze pcap files.

Agent's step:
1. analyze the pcap file and extract the information you need.
2. generate the tshark command to analyze the pcap file.
3. execute the tshark command and get the result.
4. analyze the result and extract the information you need.
5. generate the report.
"""

# 创建提示消息
prefix_msgs = [ChatMessage(role="system", content=system_prompt)]
# 初始化代理
agent = OpenAIAgent.from_tools(
    [fn_tool_tshark_tool],
    prefix_msgs=prefix_msgs,
    verbose=True,
)


# 定义使用 tshark 代理分析 pcap 文件的函数
def tshark_agent(prompt: str, pcap_file: str):
    """
    使用 tshark 代理分析 pcap 文件，仅用于分析 pcap 文件，不应用于其他目的。
    禁止使用 tshark 代理来生成 Suricata 规则。
    :param prompt: 要进行的 pcap 分析类型
    :param pcap_file: pcap 文件路径
    :return: 分析结果
    """
    prompt = f"analyze the pcap file {pcap_file}, {prompt}"
    resp = agent.query(prompt)
    return resp.response


def verify_suricate_rules(suricate_rules: str, pcap_file: str):
    """
    验证 Suricata 规则的正确性。
    :param suricate_rules: Suricata 规则内容
    :param pcap_file: pcap 文件路径
    :return: 如果规则正确，返回 (True, 匹配行数)；否则返回 (False, 错误原因)
    """
    global generate_suricate_rules
    global generate_suricate_rules_all
    generate_suricate_rules_all.append(suricate_rules)

    if os.path.exists("example.rule"):
        os.remove("example.rule")

    if os.path.exists("eve.json"):
        os.remove("eve.json")

    if os.path.exists("fast.log"):
        os.remove("fast.log")

    if os.path.exists("suricata.log"):
        os.remove("suricata.log")

    with open("example.rule", "w") as f:
        f.write(suricate_rules)

    # 使用 Suricata 执行规则检测
    subprocess.run(["suricata", "-r", pcap_file, '-k', 'none', '-S', 'example.rule', '-c', 'suricat-config.yaml'])

    # 检查 Suricata 日志中的错误
    error_lines = []
    with open("suricata.log", "r") as f:
        for line in f:
            if "Error: detect:" in line:
                error_lines.append(line)
            elif "detect: error" in line:
                error_lines.append(line)

    if len(error_lines) > 0:
        return False, "\n".join(error_lines)

    matched_lines_count = 0
    with open("fast.log", "r") as f:
        matched_lines_count = len(f.readlines())

    if matched_lines_count > 0:
        generate_suricate_rules.append(suricate_rules)

    return matched_lines_count > 0, f"matched {matched_lines_count}"


fn_tool_tshark_agent = FunctionTool.from_defaults(fn=tshark_agent)
fn_tool_suricate_verify = FunctionTool.from_defaults(fn=verify_suricate_rules)


from llama_index.agent.openai import OpenAIAgent
from llama_index.core.llms import ChatMessage
# from llama_index.core import ChatPromptTemplate

system_prompt = """
You are a helpful pcap analysis assistant(agent). you can use tshark to analyze pcap files, and generate suricate rules.

pcap analysis step:
1. analyze the pcap file and extract the information you need.
2. generate the tshark command to analyze the pcap file.
3. execute the tshark command and get the result.
4. analyze the result and extract the information you need.
5. generate the report.

Agent's step:
1. use tshark tool to analyze the pcap file and extract the information you need, summarize the pcap file.
2. think step by step
    - what is main vulnerability or attack type in the pcap file?
    - what is the main attack target?
    - what is the main attack method?
    - what is the main attack vector?
3. generate the suricate rules you self, do not use tshark agent to generate the suricate rules.
4. if you need more information, you can use tshark tool to analyze the pcap file again.
5. YOU MUST USE suricate verify tool to verify the suricate rules, if the suricate rules is not correct, you need to generate the correct suricate rules.
DO NOT FORGET TO USE suricate verify tool.

6. IF YOU FAILED MULTIPLE TIMES, YOU NEED TO THINK CAREFULLY AND GENERATE THE SURICATE RULES TOTALY DIFFERENT.
FOR DDOS, DO NOT PRINT ALL PACKETS, JUST USE SOME COUNTER MEASURE.
"""

prefix_msgs = [ChatMessage(role="system", content=system_prompt)]

# 创建 OpenAIAgent 实例，用于生成 Suricata 规则
agent_rule = OpenAIAgent.from_tools(
    [fn_tool_tshark_tool, fn_tool_suricate_verify],
    prefix_msgs=prefix_msgs,
    llm=llm,
    verbose=True,
)


def gen_suricate_rules(pcap_file: str):
    """
    生成 Suricata 规则。
    :param pcap_file: pcap 文件路径
    :return: 生成的 Suricata 规则列表
    """
    global generate_suricate_rules
    global generate_suricate_rules_all
    generate_suricate_rules_all = []
    generate_suricate_rules = []
    agent_rule.reset()
    resp = agent_rule.query(f"""analyze the pcap file \"{pcap_file}\", use quote in -r, and generate suricate rules, 
finally use suricate verify tool to verify the suricate rules, if the suricate rules is not correct, 
you need to generate the correct suricate rules. retry until the suricate rules is correct.
use suricate rules document to generate the suricate rules, feel free to use it.
""")
    # print(resp.response)
    return generate_suricate_rules


def gen_suricate_rules_retry(pcap_file: str, retry_times: int = 2):
    """
    重试生成 Suricata 规则，直到成功或达到最大重试次数。
    :param pcap_file: pcap 文件路径
    :param retry_times: 最大重试次数
    :return: 生成的 Suricata 规则列表，或 None 如果失败
    """
    while retry_times >= 0:
        retry_times -= 1
        r = gen_suricate_rules(pcap_file)
        if len(r) > 0:
            return r
        else:
            print("suricate rules is not correct, retry...")
    return None



# load all dataset
import os

# 加载数据集中的所有 pcap 文件
pcap_files = []
for root, dirs, files in os.walk("./dataset"):
    for file in files:
        if file.endswith(".pcap"):
            pcap_files.append(os.path.join(root, file))
print(pcap_files)


import random

rules = []
# 随机打乱 pcap 文件列表
random.shuffle(pcap_files)
for pcap_file in pcap_files:
    if os.path.exists("result.txt"):
        if pcap_file in open("result.txt").read():
            continue
    try:
        r = gen_suricate_rules_retry(pcap_file)
        if r is None:
            continue
        print(pcap_file, r)

        with open("result.txt", "a") as f:
            f.write(f"{pcap_file}\n{r}\n\n")
    except Exception as e:
        print(e)



