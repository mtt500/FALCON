import requests
import os
import sys
import json
from datetime import datetime

def test_analyze_binary(binary_file: str, prompt: str = None):
    """
    测试二进制文件分析 API
    :param binary_file: 二进制文件路径
    :param prompt: 可选的提示词
    :return: None
    """
    # 检查文件是否存在
    if not os.path.exists(binary_file):
        print(f"错误：找不到文件 {binary_file}")
        return

    # API 地址
    url = "http://localhost:8000/analyze"
    
    # 准备请求数据
    files = {
        'file': (os.path.basename(binary_file), open(binary_file, 'rb'))
    }
    
    # 如果提供了提示词，添加到请求中
    if prompt:
        files['prompt'] = (None, prompt)
    
    try:
        print(f"开始分析文件: {binary_file}")
        print("正在发送请求到服务器...")
        
        # 发送请求
        response = requests.post(url, files=files)
        
        # 检查响应状态
        if response.status_code == 200:
            # 解析 JSON 响应
            result = response.json()
            
            # 生成输出文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(os.path.basename(binary_file))[0]
            
            # 保存分析过程
            process_file = f"analysis_process_{base_name}_{timestamp}.txt"
            with open(process_file, 'w', encoding='utf-8') as f:
                f.write("=== 分析过程 ===\n")
                f.write(result.get('process_output', ''))
                if result.get('error_output'):
                    f.write("\n=== 错误输出 ===\n")
                    f.write(result.get('error_output', ''))
            
            # 保存反编译结果
            if result.get('status') == 'success':
                decompiled_file = f"decompiled_{base_name}_{timestamp}.txt"
                with open(decompiled_file, 'w', encoding='utf-8') as f:
                    f.write(result.get('decompiled_content', ''))
                
                print(f"分析完成！")
                print(f"分析过程已保存到: {process_file}")
                print(f"反编译结果已保存到: {decompiled_file}")
            else:
                print(f"分析失败: {result.get('message')}")
                print(f"分析过程已保存到: {process_file}")
                
        else:
            print(f"错误：服务器返回状态码 {response.status_code}")
            try:
                error_info = response.json()
                print(f"错误信息: {error_info}")
            except:
                print(f"响应内容: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到服务器，请确保服务器正在运行")
    except requests.exceptions.Timeout:
        print("错误：请求超时")
    except Exception as e:
        print(f"发生未知错误: {str(e)}")
    finally:
        # 确保文件被关闭
        files['file'][1].close()

def main():
    # 检查命令行参数
    if len(sys.argv) < 2:
        return
        
    binary_file = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else None
    
    test_analyze_binary(binary_file, prompt)

if __name__ == "__main__":
    main()