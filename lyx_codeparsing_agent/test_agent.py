from code_analysis_agent import analyze_binary

# 测试代码
if __name__ == "__main__":
    # 指定要分析的二进制文件路径
    binary_file = "test.exe"  # 替换为你的测试文件路径
    
    # 设置分析提示
    prompt = "分析这段代码的主要功能和结构，指出可能的安全问题"
    
    # 运行分析
    print("开始分析二进制文件...")
    result = analyze_binary(prompt, binary_file)
    
    # 打印分析结果
    print("\n分析结果：")
    print(result) 