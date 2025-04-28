'''
访问宇茜姐姐：curl -X POST "http://192.168.64.241:8000/decompile" -F "file=@D:\Desktop\test.exe"
访问小鸡：curl -X POST "http://172.20.10.2:8000/generate_report" -H "Content-Type: application/json" -d @result.json
'''


import requests
import json
import subprocess

# # 定义本地 C 语言代码字符串（c_str）
# local_c_code = """
# {"status":"success","code":"Function: mainCRTStartup\n\nvoid mainCRTStartup(undefined8 param_1,undefined8 param_2,undefined8 param_3)\n\n{\n  *(undefined4 *)_refptr_mingw_app_type = 0;
# \n  __security_init_cookie();\n  __tmainCRTStartup(param_1,param_2,param_3);\n  return;\n}\n\n\n----------------------------------------\nFunction: atexit\n\nint __cdecl atexit(_func_5
# 014 *param_1)\n\n{\n  _onexit_t p_Var1;\n  \n  p_Var1 = _onexit((_onexit_t)param_1);\n  return -(uint)(p_Var1 == (_onexit_t)0x0);\n}\n\n\n----------------------------------------\nFunction: vulnerable_function\n\nvoid vulnerable_function(char *param_1)\n\n{\n  char local_12 [10];\n  \n  strcpy(local_12,param_1);\n  return;\n}\n\n\n-----------------------------------
# -----\n"}
# """


yxjj_ip = '192.168.64.241'
gjj_ip = '10.132.230.117'
jzj_ip = '172.20.10.2'

# ========================== 访问宇茜姐姐 ==========================
# 定义要执行的 curl 命令
curl_command_yxjj = [
    "curl",
    "-X", "POST",
    f"http://{yxjj_ip}:8000/decompile",
    "-F", "file=@D:\\Desktop\\test.exe"
]

# 执行 curl 命令并捕获输出
try:
    result = subprocess.run(curl_command_yxjj, capture_output=True, text=True, check=True)
    local_c_code = result.stdout  # 获取命令的标准输出
    # print("YXJJ Curl Command Output:\n", local_c_code)
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running the command: {e}")
    exit(0)


# ========================== 访问小锅 ==========================
# FastAPI API 的 URL
api_url_gjj = f"http://{gjj_ip}:8000/analyze_code"

# 创建要发送的请求体，包含 C 语言代码字符串
payload = {
    "c_str": local_c_code
}

# 发送 POST 请求到 FastAPI
try:
    response = requests.post(api_url_gjj, json=payload)  # 发送请求

    # 检查响应状态
    if response.status_code == 200:
        # 解析并打印返回的 JSON 数据
        result = response.json()
        print("GJJ Analysis Result:", json.dumps(result, indent=4))
    else:
        print(f"Error: {response.status_code}, {response.text}")

except requests.exceptions.RequestException as e:
    print(f"GJJ An error occurred: {e}")
    exit(0)


# ========================== 访问小鸡 ==========================
curl_command = [
    "curl",
    "-X", "POST",
    f"http://{jzj_ip}:8000/generate_report",
    "-H", "Content-Type: application/json",
    "-d", "@result.json"  # 将 result.json 文件内容作为数据发送
]

# 执行 curl 命令并捕获输出
try:
    result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
    output = result.stdout  # 获取命令的标准输出
    # print("JZJ Curl Command Output:\n", output)
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running the command: {e}")