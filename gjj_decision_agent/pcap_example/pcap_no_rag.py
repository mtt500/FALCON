import nltk
import os
import subprocess

os.environ["OPENAI_API_KEY"] = "sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11"
os.environ["OPENAI_API_BASE"] = "https://api.gptapi.us/v1/chat/completions"

# 初始化 OpenAI 模型
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings
llm = OpenAI(model="gpt-4o", max_retries=3, temperature=1)
Settings.llm = llm

from llama_index.core.callbacks import CallbackManager
callback_manager = CallbackManager()
Settings.callback_manager = callback_manager

# 加载 pcap 文件分析工具
from llama_index.core.tools import FunctionTool
import nest_asyncio
nest_asyncio.apply()

# 使用 tshark 工具分析 pcap 文件
# def tshark_tool(tshark_command: str):
#     """
#     运行指定的 tshark 命令，并返回其输出结果。
#     :param tshark_command: tshark 命令字符串
#     :return: 命令执行结果或错误信息
#     """
#     try:
#         if not tshark_command.startswith("tshark"):
#             tshark_command = "tshark " + tshark_command
#         print(tshark_command)
#         tshark_command = tshark_command.replace("\"", "")
#
#         if len(tshark_command.split()) <= 3:
#             return "错误：命令过短，请使用选项或过滤器来过滤结果。"
#
#         result = subprocess.run(
#             tshark_command.split(),
#             capture_output=True,
#             text=True,
#             check=True
#         )
#         return result.stdout.strip()
#     except subprocess.CalledProcessError as e:
#         print(e)
#         return f"错误：tshark 执行失败：{e}"
#     except FileNotFoundError:
#         return "错误：未找到 tshark。请安装 Wireshark/tshark。"


def tshark_tool(pcap_command: str):
    """
    模拟分析 pcap 文件的工具，基于给定的命令，模拟分析内容。
    :param pcap_command: 传入的模拟分析命令（实际上不执行命令，仅模拟分析）
    :return: 模拟的分析结果，包括文件大小、数据包统计等
    """

    # 模拟分析的文件信息
    simulated_pcap_info = {
        "file_name": pcap_command.split()[-1],  # 假设命令最后一个部分是文件名
        "file_size": f"{random.randint(5, 50)} MB",  # 模拟文件大小
        "packet_count": random.randint(100, 1000),  # 随机数据包数量
        "protocols": {
            "TCP": random.randint(20, 50),  # 随机模拟 TCP 协议占比
            "UDP": random.randint(5, 30),  # 随机模拟 UDP 协议占比
            "HTTP": random.randint(10, 40),  # 随机模拟 HTTP 协议占比
            "ICMP": random.randint(0, 10)  # 随机模拟 ICMP 协议占比
        }
    }

    # 模拟生成的分析报告
    analysis_report = (
        f"分析报告: {simulated_pcap_info['file_name']}\n"
        f"文件大小: {simulated_pcap_info['file_size']}\n"
        f"数据包数量: {simulated_pcap_info['packet_count']}\n"
        f"协议分布:\n"
        f"  TCP: {simulated_pcap_info['protocols']['TCP']} 数据包\n"
        f"  UDP: {simulated_pcap_info['protocols']['UDP']} 数据包\n"
        f"  HTTP: {simulated_pcap_info['protocols']['HTTP']} 数据包\n"
        f"  ICMP: {simulated_pcap_info['protocols']['ICMP']} 数据包\n"
    )

    return analysis_report


fn_tool_tshark_tool = FunctionTool.from_defaults(fn=tshark_tool)

# 创建 OpenAIAgent 实例，用于分析 pcap 文件
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.llms import ChatMessage

system_prompt = """
You are a helpful pcap analysis assistant(agent). you can use tshark to analyze pcap files.

Agent's step:
1. analyze the pcap file and extract the information you need.
2. generate the tshark command to analyze the pcap file.
3. execute the tshark command and get the result.
4. analyze the result and extract the information you need.
5. generate the report.
"""

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
    :param prompt: 要进行的 pcap 分析类型
    :param pcap_file: pcap 文件路径
    :return: 分析结果
    """
    prompt = f"analyze the pcap file {pcap_file}, {prompt}"
    resp = agent.query(prompt)
    return resp.response

# 加载数据集中的所有 pcap 文件
import random

pcap_files = []
for root, dirs, files in os.walk("./dataset"):
    for file in files:
        if file.endswith(".pcap"):
            pcap_files.append(os.path.join(root, file))
print(pcap_files)

# 随机打乱 pcap 文件列表
rules = []
random.shuffle(pcap_files)
for pcap_file in pcap_files:
    if os.path.exists("result.txt"):
        if pcap_file in open("result.txt", encoding='utf-8').read():
            continue
    try:
        resp = tshark_agent("analyze the pcap file and generate a report.", pcap_file)
        if resp is None:
            continue
        print(pcap_file, resp)

        with open("result.txt", "a", encoding='utf-8') as f:
            f.write(f"{pcap_file}\n{resp}\n\n")
    except Exception as e:
        print(e)
