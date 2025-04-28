import sys
import os
import tempfile

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Ghidra Agent API")

# 将项目根目录加入模块搜索路径（确保能 import 到 code_analysis_agent.py）
proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_root not in sys.path:
    sys.path.append(proj_root)

# 正确导入code_analysis_agent
from code_analysis_agent import ghidra_tool, analyze_binary

from fastapi.concurrency import run_in_threadpool

@app.post("/decompile")
async def decompile_binary(file: UploadFile):
    """
    只调用 ghidra_tool 做反编译，返回原始 C 样式代码
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # 用线程池调用阻塞函数
        result = await run_in_threadpool(ghidra_tool, tmp_path)

        os.unlink(tmp_path)
        return JSONResponse({"status": "success", "code": result})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"反编译失败：{e}")


@app.post("/analyze")
async def analyze_binary_endpoint(file: UploadFile, prompt: str = "请帮我详细分析这段反编译代码："):
    """
    先用 ghidra_tool 反编译，再用 LLM 进行深度分析，返回分析报告
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # 调用带 LLM 分析的函数
        report = analyze_binary(prompt, tmp_path)

        os.unlink(tmp_path)
        return JSONResponse({"status": "success", "report": report})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败：{e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)