import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import analyze_code_agent, extract_json_from_content  # 根据您的文件路径导入
from process_code import extract_functions_from_code, filter_and_extract_functions


app = FastAPI()


# 定义输入数据模型
class CodeRequest(BaseModel):
    c_str: str  # 用户传入的 C 语言代码


# 处理代码分析的路由
@app.post("/analyze_code")
async def analyze_code(request: CodeRequest):
    c_str = request.c_str

    functions = extract_functions_from_code(c_str)
    filtered_functions = filter_and_extract_functions(functions)

    try:
        for function in filtered_functions:
            try:
                func_name = function['func_name']
                code_snippet = function['code_snippet']
                resp, code_snippet = analyze_code_agent(code_snippet)  # str
                print('func_name:', func_name)
                print('code_snippet:', code_snippet)
                extract_json_from_content(resp, code_snippet)
            except Exception as e:
                print(e)
        return {"status": "success", "message": "Analysis complete."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 运行 FastAPI 应用 (在命令行中运行 `uvicorn app.py:app --host 0.0.0.0 --port 8000 --reload`)
# curl -X POST "http://10.132.230.117/analyze_code" -H "Content-Type: application/json" -d '{"c_str": "{"status":"success","code":"Function: mainCRTStartup\n\nvoid mainCRTStartup(undefined8 param_1,undefined8 param_2,undefined8 param_3)\n\n{\n  *(undefined4 *)_refptr_mingw_app_type = 0;
# \n  __security_init_cookie();\n  __tmainCRTStartup(param_1,param_2,param_3);\n  return;\n}\n\n\n----------------------------------------\nFunction: atexit\n\nint __cdecl atexit(_func_5
# 014 *param_1)\n\n{\n  _onexit_t p_Var1;\n  \n  p_Var1 = _onexit((_onexit_t)param_1);\n  return -(uint)(p_Var1 == (_onexit_t)0x0);\n}\n\n\n----------------------------------------\nFunc
# tion: vulnerable_function\n\nvoid vulnerable_function(char *param_1)\n\n{\n  char local_12 [10];\n  \n  strcpy(local_12,param_1);\n  return;\n}\n\n\n-----------------------------------
# -----\n""}}'


