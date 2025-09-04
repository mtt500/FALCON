import nltk
import os
import subprocess



os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["OPENAI_API_KEY"] = "sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11"
os.environ["OPENAI_API_BASE"] = "https://api.gptapi.us/v1"

# $env:PYTHONIOENCODING = "utf-8"
# 初始化 OpenAI 模型
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings
llm = OpenAI(model="gpt-4o", max_retries=3, temperature=1)
Settings.llm = llm

from llama_index.core.callbacks import CallbackManager
callback_manager = CallbackManager()
Settings.callback_manager = callback_manager

# 加载反编译工具
from llama_index.core.tools import FunctionTool
import nest_asyncio
nest_asyncio.apply()

def IDA_tool(binary_file: str):
    """
    使用 IDA 反汇编和反编译二进制文件
    :param binary_file: 二进制文件路径
    :return: 反汇编和反编译结果
    """
    pass
def capstone_tool(binary_file: str):
    """
    使用 Capstone 反汇编和反编译二进制文件
    :param binary_file: 二进制文件路径
    :return: 反汇编和反编译结果
    """
    pass

def radare2_tool(binary_file: str):
    """
    使用 radare2 反汇编和反编译二进制文件
    :param binary_file: 二进制文件路径
    :return: 反汇编和反编译结果
    """
    pass

def llm4decompile_tool(binary_file: str):
    """
    使用 LLM 反汇编和反编译二进制文件
    :param binary_file: 二进制文件路径
    :return: 反汇编和反编译结果
    """

import re
def filter_functions(code: str) -> str:
    """
    过滤出包含 'system' 函数名或字符串操作的函数
    :param code: Ghidra 的完整反编译输出
    :return: 过滤后的函数代码
    """
    filtered_funcs = []
    # 正则匹配函数块（假设函数以 'void ' 或 'int ' 等返回类型开头）
    function_blocks = re.findall(r'(?:[\w\*\s]+)\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}', code, re.DOTALL)
    
    for match in re.finditer(r'(?:[\w\*\s]+)\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}', code, re.DOTALL):
        func_name = match.group(1)
        func_body = match.group(0)
        if (
            'system' in func_name.lower() or
            any(api in func_body for api in ['strcpy', 'strcat', 'sprintf', 'strncpy', 'memcpy', 'strlen', 'strcmp', 'strstr'])
        ):
            filtered_funcs.append(func_body)
    
    return "\n\n".join(filtered_funcs) if filtered_funcs else "未发现匹配的函数"


# 使用 Ghidra 工具反汇编和反编译二进制文件
def ghidra_tool(binary_file: str):
    """
    使用 Ghidra 反汇编和反编译二进制文件
    :param binary_file: 二进制文件路径
    :return: 反汇编和反编译结果
    """
    try:
        print(f"开始处理二进制文件: {binary_file}")
        
        # 检查文件是否存在
        if not os.path.exists(binary_file):
            return f"错误：找不到二进制文件 {binary_file}"
            
        # Ghidra 安装路径
        ghidra_path = "D:\ghidra\ghidra_10.4_PUBLIC_20230928\ghidra_10.4_PUBLIC"
        if not os.path.exists(ghidra_path):
            return f"错误：找不到 Ghidra 安装目录 {ghidra_path}"
            
        # 创建临时项目目录
        project_dir = os.path.join(os.getcwd(), "ghidra_project")
        os.makedirs(project_dir, exist_ok=True)
        print(f"项目目录: {project_dir}")
        
        # 构建 Ghidra 命令行
        cmd = [
            os.path.join(ghidra_path, "support", "analyzeHeadless.bat"),
            project_dir,
            "temp_project",
            "-import", binary_file,
            "-scriptPath", os.path.join(os.getcwd(), "ghidra_scripts"),
            "-postScript", "DecompileScript.java",
            "-deleteProject"
        ]
        
        print("执行 Ghidra 命令...")
        # print("命令: " + " ".join(cmd))
        
        # 执行 Ghidra
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=True,
            timeout=300
        )
        
        print("Ghidra 执行完成")

        # 读取反编译结果文件
        output_file = "decompiled_output.txt"
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                decompiled_code = f.read()
            print("成功读取反编译结果")
            return decompiled_code
        else:
            print(f"未找到输出文件: {output_file}")
            return "错误：未生成反编译结果文件"
            
    except subprocess.TimeoutExpired:
        return "错误：Ghidra 执行超时"
    except subprocess.CalledProcessError as e:
        print(f"Ghidra 执行失败: {e}")
        stdout = e.stdout.encode('utf-8', errors='replace').decode('utf-8')
        stderr = e.stderr.encode('utf-8', errors='replace').decode('utf-8')
        print("标准输出:", stdout)
        print("标准错误:", stderr)
        return f"错误：Ghidra 执行失败：{e}"
    except FileNotFoundError:
        print("未找到 Ghidra")
        return "错误：未找到 Ghidra。请确保 Ghidra 已正确安装。"
    except Exception as e:
        print(f"发生未知错误: {e}")
        return f"错误：{str(e)}"


# 创建工具实例
fn_tool_ghidra = FunctionTool.from_defaults(fn=ghidra_tool)
fn_tool_IDA = FunctionTool.from_defaults(fn=IDA_tool)
fn_tool_radare2 = FunctionTool.from_defaults(fn=radare2_tool)
fn_tool_capstone = FunctionTool.from_defaults(fn=capstone_tool)

# 创建 OpenAIAgent 实例
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.llms import ChatMessage

system_prompt = """
You are a binary code decompilation assistant that focuses on extracting and saving decompiled code.
Your tasks include:
1. Analyzing binary files using appropriate tools
2. Extracting and saving decompiled code
3. Ensuring the decompilation process is complete and accurate

Available tools:
1. ghidra_tool: For decompilation and code extraction
2. capstone_tool: For instruction-level disassembly
3. radare2_tool: For code extraction and analysis
4. IDA_tool: For decompilation and code extraction
5. llm4decompile_tool: For code extraction

Agent's steps:
1. Choose the most appropriate tool(s) for decompilation
2. Use the selected tool(s) to extract code
3. If a tool fails, try alternative tools
4. Save the decompiled code for further analysis

Output format:
- Save decompiled code to appropriate files
- Return the paths of saved files
- Report any errors or issues during decompilation
"""

prefix_msgs = [ChatMessage(role="system", content=system_prompt)]

# 初始化代理
agent = OpenAIAgent.from_tools(
    [fn_tool_ghidra, fn_tool_IDA, fn_tool_radare2, 
     fn_tool_capstone],  
    prefix_msgs=prefix_msgs,
    verbose=True,
)

# 定义使用代理分析二进制文件的函数
def analyze_binary(prompt: str, binary_file: str):
    full_prompt = f"""
    目标：反编译二进制文件并保存结果。
    - 二进制文件路径：{binary_file}
    - 分析需求：{prompt}
    
    请按照以下步骤操作：
    1. 分析固件特征（文件类型、架构等）
    2. 根据分析结果，从以下工具中选择一个最合适的工具：
       - ghidra_tool: 适合反编译和代码提取，支持多种架构
       - capstone_tool: 适合指令级反汇编，特别适合 ARM 架构
       - radare2_tool: 适合代码提取和分析，适合 Linux 二进制
       - IDA_tool: 适合反编译和代码提取，适合 Windows 可执行文件
    3. 使用选定的工具进行反编译
    4. 如果当前工具调用失败或未返回有效结果，请尝试选择其他合适的工具
    5. 将反编译结果保存到文件
    
    请使用以下格式调用工具：
    tool: [工具名称]
    tool_input: {{"binary_file": "{binary_file}"}}
    
    请返回：
    - 固件类型
    - 最终选择使用的工具及选择原因
    - 反编译结果保存的文件路径
    """
    resp = agent.query(full_prompt)
    return resp.response

