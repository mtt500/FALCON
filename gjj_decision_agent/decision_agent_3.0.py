'''
这个版本增加 rag 功能。

增加源码的json字段。

tools:
horusec, flawfinder, cppcheck, splint

cppcheck
编程错误，malloc内存未释放，除 0 等

flawfinder
模式匹配和语法检查


动态检查C语言程序安全弱点和编写错误（实际上还是静态分析工具）

horusec
侧重 Web 应用程序安全的漏洞，如 SQL 注入、命令注入、XSS 攻击 和身份验证问题等
'''


import os
import random
import json
import re

os.environ["OPENAI_API_KEY"] = "sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11"
os.environ["OPENAI_API_BASE"] = "https://api.gptapi.us/v1/chat/completions"

# 初始化 OpenAI 模型
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.core.settings import Settings
from llama_index.core import Settings, StorageContext
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, load_index_from_storage
from llama_index.core.tools import QueryEngineTool

llm = OpenAI(model="gpt-3.5-turbo", max_retries=3, temperature=1)
Settings.llm = llm
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

from llama_index.core.callbacks import CallbackManager

callback_manager = CallbackManager()
Settings.callback_manager = callback_manager

from llama_index.core.tools import FunctionTool
import nest_asyncio

nest_asyncio.apply()


# ========================== 构建/加载漏洞知识库索引 ==========================
# ========================== 构建/加载漏洞知识库索引 ==========================
try:
    print("正在加载固件漏洞知识库索引..")
    kb_storage_context = StorageContext.from_defaults(persist_dir="/home/seed/Desktop/gjj_decision_agent/vector_data")
    # 使用 StorageContext 加载索引
    vuln_kb_index = load_index_from_storage(kb_storage_context)
    print("固件漏洞知识库索引加载成功！")
except Exception as e:
    print("固件漏洞知识库索引加载失败，正在构建索引..")
    # 加载 "./data/vuln_kb" 目录下所有漏洞相关文件
    print("loading documents...")
    documents = SimpleDirectoryReader(input_dir="/home/seed/Desktop/gjj_decision_agent/storage/testcases").load_data()
    print("indexing...")
    # 使用所有文档构建向量存储索引
    vuln_kb_index = VectorStoreIndex.from_documents(documents, show_progress=True)
    print("persisting...")
    # 持久化索引到存储目录
    vuln_kb_index.storage_context.persist(persist_dir="/home/seed/Desktop/gjj_decision_agent/vector_data")
    print("固件漏洞知识库索引构建并持久化完成。")

# ===================== 创建基于知识库索引的查询引擎 =====================
kb_query_engine = vuln_kb_index.as_query_engine(similarity_top_k=3)

# 将查询引擎包装为工具供 Agent 调用
kb_tool = QueryEngineTool.from_defaults(
    query_engine=kb_query_engine,
    name="vuln_knowledge_base",
    description=("Provides vulnerable code snippets similar to the target code.")
)


# ========================== 定义分析工具 ==========================
import subprocess
import tempfile
import uuid


# horusec 工具
# horusec_win_amd64.exe start -p "D:\Desktop\xas\FALCON\gjj_decision_agent\tools\code" -i "vul_sql.c" -D --log-level "error"
def Horusec_analyze(code_snippet: str):
    """
    使用 Horusec 工具分析 C 语言代码片段并提取漏洞信息。
    :param code_snippet: C 语言代码片段
    :return: Horusec 的 JSON 分析结果
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = f"{uuid.uuid4().hex}.c"
        file_path = os.path.join(tmpdirname, file_name)

        # 写入临时 .c 文件
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(code_snippet)

        try:
            # 调用 Horusec 进行分析
            result = subprocess.run(
                [
                    'horusec', 'start',
                    '-p', tmpdirname,
                    '-i', file_name,
                    '--log-level', 'error',
                    '-D'
                ],
                capture_output=True,
                text=True,
                encoding='utf-8'  # 明确指定使用 UTF-8 编码
            )

            return result.stdout  # 只返回标准输出的内容

        except FileNotFoundError:
            return {"error": "Horusec CLI 未安装或不可用"}



# cppcheck 工具
def cppcheck_analyze(code_snippet: str):
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = f"{uuid.uuid4().hex}.c"
        file_path = os.path.join(tmpdirname, file_name)

        # 写入临时 .c 文件
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(code_snippet)
        try:
            # 调用 Cppcheck 进行分析
            result = subprocess.run(
                ['cppcheck', file_path],
                # ['cppcheck' '--enable=all', file_path],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8',  # 明确指定使用 UTF-8 编码
                errors='ignore'    # 忽略无法解码的字符
            )
            # 返回分析结果
            return result.stdout
        except subprocess.CalledProcessError as e:
            # 如果 Cppcheck 返回非零退出码，捕获异常并返回错误信息
            return f"Cppcheck 错误: {e.stderr}"
        except FileNotFoundError:
            return "Cppcheck 未安装或未添加到系统路径中。"


# flawfinder 工具
# flawfinder ./c_code/vul_sql.c
def flawfinder_analyze(code_snippet: str):
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = f"{uuid.uuid4().hex}.c"
        file_path = os.path.join(tmpdirname, file_name)

        # 写入临时 .c 文件
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(code_snippet)
        try:
            # 调用 Cppcheck 进行分析
            result = subprocess.run(
                ['flawfinder', file_path],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8',  # 明确指定使用 UTF-8 编码
                errors='ignore'    # 忽略无法解码的字符
            )
            # 返回分析结果
            return result.stdout
        except subprocess.CalledProcessError as e:
            # 如果 Cppcheck 返回非零退出码，捕获异常并返回错误信息
            return f"flawfinder 错误: {e.stderr}"
        except FileNotFoundError:
            return "flawfinder 未安装或未添加到系统路径中。"



# 定义分析工具
horusec_analyze_tool = FunctionTool.from_defaults(
    fn=Horusec_analyze,
    name='horusec_analyze_tool',
    description='the horusec tool for static code snippet analysis.'
)


cppcheck_analyze_tool = FunctionTool.from_defaults(
    fn=cppcheck_analyze,
    name='cppcheck_analyze_tool',
    description='the cppcheck tool for static code snippet analysis.'
)

flawfinder_analyze_tool = FunctionTool.from_defaults(
    fn=flawfinder_analyze,
    name='flawfinder_analyze_tool',
    description='the flawfinder tool for static code snippet analysis.'
)



# ========================== 定义 Agent ==========================
# 创建 OpenAIAgent 实例，用于分析 C 语言代码
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.llms import ChatMessage

# 修改后的系统提示
system_prompt = """
You are a helpful code analysis assistant(agent). You can analyze C code and identify potential vulnerabilities such as buffer overflows, null pointer dereferencing, etc.
"""

prefix_msgs = [ChatMessage(role="system", content=system_prompt)]

# 初始化代理
agent = OpenAIAgent.from_tools(
    [horusec_analyze_tool, cppcheck_analyze_tool, flawfinder_analyze_tool, kb_tool],  # 工具列表
    # [horusec_analyze_tool, cppcheck_analyze_tool, flawfinder_analyze_tool],  # 工具列表
    prefix_msgs=prefix_msgs,
    verbose=True,
)


# 定义分析 C 语言函数片段的代理函数
def analyze_code_agent(code_file: str):
    """
    使用代理分析 C 语言函数片段，并判断是否包含漏洞。
    :param code_file: C 语言代码文件路径
    :return: 分析结果
    """
    with open(code_file, "r", encoding='utf-8') as file:
        code_snippet = file.read()

    analyze_prompt = f'''
    Analyze the following C code snippet, identify vulnerabilities and output the analysis results in the specified json format. 
    The C code snippet is as follows.
    
    {code_snippet}

    Agent's step:
    1. analyze the C code snippet and extract potential vulnerabilities.
    2. detect common issues like buffer overflow, improper memory management, and others.
    3. return the vulnerabilities found or if the code is safe.

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

    example output format:
    {{
      "function_name": "authenticate_user",
      "is_vulnerable": true,
      "vulnerability_type": "Buffer Overflow",
      "severity": "high",
      "description": "The function uses strcpy without boundary checks, allowing attackers to overwrite memory and potentially execute arbitrary code."
    }}

    NOTICE: Return the content in JSON format directly. Please do not include any content other than JSON format in your answer.
    '''

    resp = agent.query(analyze_prompt)
    return resp.response, code_snippet


# ========================== 业务逻辑 ==========================
# 加载数据集中的所有 C 语言代码文件
code_files = []
for root, dirs, files in os.walk("/home/seed/Desktop/gjj_decision_agent/c_code"):
    for file in files:
        if file.endswith(".c"):
            code_files.append(os.path.join(root, file))

# 随机打乱 C 语言文件列表
vulnerabilities_report = []
random.shuffle(code_files)


def extract_json_from_content(content, code_snippet, output_file='/home/seed/Desktop/gjj_decision_agent/result.json'):
    """
    从包含 JSON 数据的复杂文本中提取并解析 JSON 数据，然后将解析结果追加到文件。

    :param content: 包含 JSON 数据的字符串
    :param output_file: 目标输出文件的名称（默认是 'output.json'）
    :return: 解析后的 JSON 数据字典，如果没有找到 JSON，则返回 None
    """
    # 正则表达式匹配包含在 ```json 和 ``` 中的 JSON 部分
    # json_pattern = r'```json\n(.*?)\n```'  # 匹配 JSON 格式的部分
    match = re.search(r'\{.*\}', content, re.DOTALL)

    # 如果找到了匹配的 JSON 字符串，解析它
    if match:
        json_str = match.group(0)  # 提取 JSON 字符串
        print("Extracted JSON string:")
        print(json_str)  # 打印提取的 JSON 字符串，帮助调试

        # 去除可能的空白字符（换行符、空格等）
        # json_str = json_str.strip()

        try:
            json_data = json.loads(json_str)  # 将字符串解析为 JSON 对象

            json_data['code_snippet'] = code_snippet  # 增加 code snippet 字段

            # 如果输出文件已存在，则读取文件内容
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    # 确保已经读取的是一个列表，然后追加新数据
                    if isinstance(existing_data, list):
                        existing_data.append(json_data)
                    else:
                        existing_data = [json_data]
            else:
                # 如果文件不存在，初始化一个新的列表
                existing_data = [json_data]

            # 将数据写入文件（无论是初始化文件还是追加数据）
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)

            print(f"JSON data has been appended to {output_file}")
            return json_data
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return None
    else:
        print("No JSON found in the content.")
        return None


for code_file in code_files:
    if os.path.exists("/home/seed/Desktop/gjj_decision_agent/result.json"):
        if code_file in open("/home/seed/Desktop/gjj_decision_agent/result.json", encoding='utf-8').read():
            continue
    try:
        resp, code_snippet = analyze_code_agent(code_file)  # str
        if resp is None:
            continue
        print(code_file)
        # print(resp)

        # try:
        extract_json_from_content(resp, code_snippet)

    except Exception as e:
        print(e)
