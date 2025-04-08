from typing import Dict, Any, List
from pathlib import Path
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from src.tools.binary_analyzer import BinaryAnalyzer  # 二进制分析工具
from src.tools.decompiler import Decompiler  # 反编译器工具
from src.utils.logger import setup_logger
from config.settings import Settings

class CodeParsingAgent:
    def __init__(self):
        self.logger = setup_logger()
        self.settings = Settings()
        
        # 初始化组件
        self.binary_analyzer = BinaryAnalyzer()  # 用于分析二进制文件基本信息
        self.decompiler = Decompiler()  # 用于反编译
        
        # 初始化 OpenAI
        self.llm = OpenAI(
            api_key=self.settings.OPENAI_API_KEY,
            model=self.settings.OPENAI_MODEL
        )
        
        # 初始化工具
        self.tools = self._init_tools()
        
        # 初始化 Agent
        system_prompt = """
        你是一个专业的二进制代码分析助手。你的任务是：
        1. 分析二进制文件的基本信息（架构、格式等）
        2. 将二进制代码反编译为可读的源代码
        
        分析步骤：
        1. 使用 binary_analyzer 工具获取二进制文件信息
        2. 使用 decompiler 工具进行反编译
        3. 生成人类可读的分析报告
        """
        
        self.agent = ReActAgent.from_tools(
            tools=self.tools,
            llm=self.llm,
            system_prompt=system_prompt,
            verbose=True
        )

    def _init_tools(self) -> List[FunctionTool]:
        """初始化所有工具"""
        tools = []
        
        # 二进制分析工具
        def analyze_binary(binary_path: str) -> Dict[str, Any]:
            """分析二进制文件的基本信息"""
            try:
                info = self.binary_analyzer.analyze(binary_path)
                return {
                    "status": "success",
                    "info": info
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e)
                }
        
        tools.append(FunctionTool.from_defaults(
            fn=analyze_binary,
            name="analyze_binary",
            description="分析二进制文件的基本信息，包括架构、格式等"
        ))
        
        # 反编译工具
        def decompile_binary(binary_path: str) -> Dict[str, Any]:
            """反编译二进制文件"""
            try:
                decompiled_code = self.decompiler.decompile(binary_path)
                return {
                    "status": "success",
                    "code": decompiled_code
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e)
                }
        
        tools.append(FunctionTool.from_defaults(
            fn=decompile_binary,
            name="decompile_binary",
            description="将二进制文件反编译为可读的源代码"
        ))
        
        return tools

    def parse_binary(self, binary_path: str) -> Dict[str, Any]:
        """解析二进制文件"""
        try:
            # 使用 Agent 进行解析
            response = self.agent.query(f"""
            请分析二进制文件 {binary_path}：
            1. 使用 analyze_binary 工具获取文件基本信息
            2. 使用 decompile_binary 工具进行反编译
            3. 生成完整的分析报告，包括：
               - 文件基本信息
               - 反编译后的代码
            """)
            
            return {
                "status": "success",
                "analysis": response.response
            }
            
        except Exception as e:
            self.logger.error(f"解析失败: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }