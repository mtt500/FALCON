import os
import random
import json
import re

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

# 加载 C 语言代码分析工具
from llama_index.core.tools import FunctionTool
import nest_asyncio

nest_asyncio.apply()


def analyze_code_for_vulnerabilities(code_snippet: str):
    """
    模拟分析 C 语言函数片段的漏洞，检查常见的漏洞模式（如缓冲区溢出、空指针解引用等）。
    :param code_snippet: 传入的 C 语言函数片段
    :return: 分析结果，表示是否检测到漏洞
    """
    # 这里可以根据常见的漏洞模式做简单的判断，或者直接调用 GPT 模型生成分析
    vulnerabilities = []

    # 示例漏洞检测逻辑（这里只是模拟）
    if "gets(" in code_snippet or "strcpy(" in code_snippet:
        vulnerabilities.append("潜在缓冲区溢出风险：使用了不安全的字符串操作函数（gets 或 strcpy）。")
    if "free(" in code_snippet and "NULL" in code_snippet:
        vulnerabilities.append("潜在空指针解引用：尝试释放空指针。")

    return vulnerabilities

    # # 使用 GPT 模型进一步分析漏洞
    # analysis_prompt = f"请分析以下 C 语言代码片段，并指出是否包含任何漏洞：\n{code_snippet}\n"
    # response = llm.query(analysis_prompt)  # Got output: Error: 'OpenAI' object has no attribute 'query'
    #
    # return response + "\n检测到的漏洞：" + "\n".join(vulnerabilities)


# 定义这个模拟的分析工具
fn_tool_code_analysis = FunctionTool.from_defaults(fn=analyze_code_for_vulnerabilities)

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
    [fn_tool_code_analysis],
    prefix_msgs=prefix_msgs,
    verbose=True,
)


# 定义分析 C 语言函数片段的代理函数
def analyze_code_agent(prompt: str, code_file: str):
    """
    使用代理分析 C 语言函数片段，并判断是否包含漏洞。
    :param prompt: 要进行的代码分析类型
    :param code_file: C 语言代码文件路径
    :return: 分析结果
    """
    with open(code_file, "r", encoding='utf-8') as file:
        code_snippet = file.read()

    analyze_prompt = f'''
    analyze the following C code snippet, identify vulnerabilities and output in the certain json format: {code_snippet}

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
    return resp.response


# 加载数据集中的所有 C 语言代码文件
code_files = []
for root, dirs, files in os.walk("./c_code"):
    for file in files:
        if file.endswith(".c"):
            code_files.append(os.path.join(root, file))

# 随机打乱 C 语言文件列表
vulnerabilities_report = []
random.shuffle(code_files)


def extract_json_from_content(content, output_file='result.json'):
    """
    从包含 JSON 数据的复杂文本中提取并解析 JSON 数据，然后将解析结果追加到文件。

    :param content: 包含 JSON 数据的字符串
    :param output_file: 目标输出文件的名称（默认是 'output.json'）
    :return: 解析后的 JSON 数据字典，如果没有找到 JSON，则返回 None
    """
    # 正则表达式匹配包含在 ```json 和 ``` 中的 JSON 部分
    json_pattern = r'```json\n(.*?)\n```'  # 匹配 JSON 格式的部分
    match = re.search(json_pattern, content, re.DOTALL)

    # 如果找到了匹配的 JSON 字符串，解析它
    if match:
        json_str = match.group(1)  # 提取 JSON 字符串
        print("Extracted JSON string:")
        print(json_str)  # 打印提取的 JSON 字符串，帮助调试

        # 去除可能的空白字符（换行符、空格等）
        json_str = json_str.strip()

        try:
            json_data = json.loads(json_str)  # 将字符串解析为 JSON 对象

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
    if os.path.exists("result.json"):
        if code_file in open("result.json", encoding='utf-8').read():
            continue
    try:
        resp = analyze_code_agent("analyze the C code and detect vulnerabilities.", code_file)
        if resp is None:
            continue
        print(code_file)
        print(resp)

        # try:
        extract_json_from_content(resp)

    except Exception as e:
        print(e)
