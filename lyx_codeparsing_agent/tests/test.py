from src.agents.code_parsing_agent import CodeParsingAgent
from pathlib import Path

def main():
    # 初始化 Agent
    agent = CodeParsingAgent()
    
    # 指定要分析的二进制文件
    binary_path = "path/to/your/binary"  # 替换为实际的二进制文件路径
    
    # 运行分析
    result = agent.parse_binary(binary_path)
    
    # 打印结果
    if result['status'] == 'success':
        print("\n=== 分析报告 ===")
        print(result['analysis'])
    else:
        print(f"分析失败: {result['error']}")

if __name__ == "__main__":
    main()