import nltk
import os
import subprocess

os.environ["OPENAI_API_KEY"] = "sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11"
os.environ["OPENAI_API_BASE"] = "https://api.gptapi.us/v1"

# $env:PYTHONIOENCODING = "utf-8"
# 初始化 OpenAI 模型
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings
llm = OpenAI(model="gpt-3.5-turbo", max_retries=3, temperature=1)
Settings.llm = llm

from llama_index.core.callbacks import CallbackManager
callback_manager = CallbackManager()
Settings.callback_manager = callback_manager

# 加载反编译工具
from llama_index.core.tools import FunctionTool
import nest_asyncio
nest_asyncio.apply()

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
        print("命令: " + " ".join(cmd))
        
        # 执行 Ghidra
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=300
        )
        
        print("Ghidra 执行完成")
        print("标准输出:", result.stdout)
        print("标准错误:", result.stderr)
        
        # 读取反编译结果文件
        output_file = "decompiled_output.txt"
        if os.path.exists(output_file):
            print(f"找到输出文件: {output_file}")
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
        print("标准输出:", e.stdout)
        print("标准错误:", e.stderr)
        return f"错误：Ghidra 执行失败：{e}"
    except FileNotFoundError:
        print("未找到 Ghidra")
        return "错误：未找到 Ghidra。请确保 Ghidra 已正确安装。"
    except Exception as e:
        print(f"发生未知错误: {e}")
        return f"错误：{str(e)}"

# 创建工具实例
fn_tool_ghidra = FunctionTool.from_defaults(fn=ghidra_tool)

# 创建 OpenAIAgent 实例
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.llms import ChatMessage

system_prompt = """
You are a code analysis assistant that can analyze binary code using Ghidra.
Your tasks include:
1. Analyzing binary files using Ghidra
2. Providing detailed analysis of the decompiled code
3. Explaining the functionality and potential vulnerabilities

Agent's step:
1. Use Ghidra to analyze the binary file
2. Extract and analyze the decompiled code
3. Provide a comprehensive analysis report
"""

prefix_msgs = [ChatMessage(role="system", content=system_prompt)]

# 初始化代理
agent = OpenAIAgent.from_tools(
    [fn_tool_ghidra],  # 只使用 Ghidra 工具
    prefix_msgs=prefix_msgs,
    verbose=True,
)

# 定义使用代理分析二进制文件的函数
def analyze_binary(prompt: str, binary_file: str):
    """
    使用代理分析二进制文件
    :param prompt: 分析提示
    :param binary_file: 二进制文件路径
    :return: 分析结果
    """
    # 1. 首先使用 Ghidra 工具反编译二进制文件
    decompiled_code = ghidra_tool(binary_file)
    
    # 2. 如果反编译成功，使用 Agent 分析反编译后的代码
    if "错误" not in decompiled_code:
        prompt = f"分析以下反编译代码：\n{decompiled_code}\n{prompt}"
        resp = agent.query(prompt)
        return resp.response
    else:
        return decompiled_code  # 返回反编译过程中的错误信息