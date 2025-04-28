import re


def extract_functions_from_code(input_string: str):
    # 使用正则表达式提取 "code" 部分的内容
    match = re.search(r'"code"\s*:\s*"([^"]*)"', input_string, re.DOTALL)
    if match:
        code = match.group(1)  # 提取 "code" 部分的内容

        # 使用正则表达式分割函数内容，按照 "-----" 分割
        # function_pattern = r"([^\-]+)(?=\n----------------------------------------|\Z)"  # 匹配每个函数，直到遇到 "-----" 或字符串结尾
        # functions = re.findall(function_pattern, code, re.DOTALL)
        functions = code.split('----------------------------------------')

        # 去掉每个函数内容两端的空格和换行符，确保返回的每个函数内容无前后空白
        return [func.strip() for func in functions if func.strip()]
    else:
        print("No 'code' field found.")
        return []


def filter_and_extract_functions(functions):
    filtered_functions = []

    # 遍历 functions 列表
    for func in functions:
        # 如果函数以 "Function:" 开头
        if func.startswith("Function:"):
            # 提取函数名，假设函数名在 "Function: " 后面，并且函数名由单词字符组成
            match = re.match(r"Function:\s*(\w+)", func)
            if match:
                func_name = match.group(1)  # 函数名

                # 提取函数代码，"Function: <func_name>" 后面的内容
                code_snippet = func[len(match.group(0)):].strip()  # 去除 "Function: <func_name>" 部分

                # 删除所有 "----------" 分隔符部分
                code_snippet = code_snippet.replace("-----------------------------------", "").strip()

                # 添加字典到结果列表
                filtered_functions.append({
                    "func_name": func_name,
                    "code_snippet": code_snippet
                })

    return filtered_functions


if __name__ == "__main__":
    # 示例用法
    input_string = '''
    local_c_code = """
{"status":"success","code":"Function: mainCRTStartup\n\nvoid mainCRTStartup(undefined8 param_1,undefined8 param_2,undefined8 param_3)\n\n{\n  *(undefined4 *)_refptr_mingw_app_type = 0;
\n  __security_init_cookie();\n  __tmainCRTStartup(param_1,param_2,param_3);\n  return;\n}\n\n\n----------------------------------------\nFunction: atexit\n\nint __cdecl atexit(_func_5
014 *param_1)\n\n{\n  _onexit_t p_Var1;\n  \n  p_Var1 = _onexit((_onexit_t)param_1);\n  return -(uint)(p_Var1 == (_onexit_t)0x0);\n}\n\n\n----------------------------------------\nFunction: vulnerable_function\n\nvoid vulnerable_function(char *param_1)\n\n{\n  char local_12 [10];\n  \n  strcpy(local_12,param_1);\n  return;\n}\n\n\n-----------------------------------
-----\n"}
"""

    '''

    functions = extract_functions_from_code(input_string)  # list

    filtered_functions = filter_and_extract_functions(functions)

    # 打印输出过滤后的结果
    for item in filtered_functions:
        print(f"Function Name: {item['func_name']}")
        print(f"Code Snippet: {item['code_snippet']}\n")

# filtered_functions = [
#     {'func_name': 'mainCRTStartup', 'code_snippet': 'void mainCRTStartup(...) {...}'},
#     {'func_name': 'atexit', 'code_snippet': 'int __cdecl atexit(...) {...}'},
#     ...
# ]
