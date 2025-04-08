from src.services.llm_service import LLMService
from src.agents.code_parsing_agent import CodeAnalysisAgent
import logging
import os
import sys

def analyze_binary_file(binary_path: str):
    # 初始化服务
    llm_service = LLMService()
    agent = CodeAnalysisAgent(llm_service)
    
    # 分析二进制文件
    result = agent.analyze_binary(binary_path)
    
    if result["status"] == "success":
        print("=== 反编译结果 ===")
        print(result["decompiled_code"])
        
        print("\n=== 程序分析 ===")
        print(result["analysis"])
        
        print("\n=== 函数列表 ===")
        for func in result["functions"]:
            print(f"函数名: {func.get('name', 'unknown')}")
            print(f"地址: {func.get('offset', 'unknown')}")
            print(f"大小: {func.get('size', 'unknown')} bytes")
            print("---")
    else:
        print(f"分析失败: {result.get('error', '未知错误')}")

# 使用示例
if __name__ == "__main__":
    # 设置详细的日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s | %(levelname)s | %(name)s:%(lineno)d - %(message)s'
    )
    
    binary_path = r"D:\大三课程\信安赛\Agent\test_files\sample.bin"
    
    if not os.path.exists(binary_path):
        print(f"错误：找不到文件 {binary_path}")
        sys.exit(1)
        
    try:
        analyze_binary_file(binary_path)
    except Exception as e:
        print(f"分析失败: {str(e)}")
        import traceback
        traceback.print_exc()