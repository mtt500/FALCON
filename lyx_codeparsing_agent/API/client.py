import sys
import os

# 添加父目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code_analysis_agent import DecompilerAgent  # 修改这里，从主文件导入
import requests

def decompile_file(file_path: str) -> str:
    """
    调用反编译 API 处理文件。
    :param file_path: 本地文件路径
    :return: 反编译结果
    """
    url = "http://localhost:8000/decompile"
    
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
        
    if response.status_code == 200:
        return response.json()["code"]
    else:
        raise Exception(f"API 调用失败: {response.text}")

if __name__ == "__main__":
    # 测试调用
    result = decompile_file("test.exe")
    print(result)