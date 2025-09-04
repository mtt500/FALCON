import sys
import os
import tempfile
from datetime import datetime
import io
import contextlib

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI(title="Binary Analysis API")

# 将项目根目录加入模块搜索路径
proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_root not in sys.path:
    sys.path.append(proj_root)

# 导入分析工具
from code_analysis_agent_tools import analyze_binary

from fastapi.concurrency import run_in_threadpool

# 创建一个上下文管理器来捕获标准输出
@contextlib.contextmanager
def capture_output():
    stdout = io.StringIO()
    stderr = io.StringIO()
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    try:
        sys.stdout = stdout
        sys.stderr = stderr
        yield stdout, stderr
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

@app.post("/analyze")
async def analyze_binary_endpoint(file: UploadFile, prompt: str = "请帮我反编译这个二进制文件："):
    """
    使用 Agent 选择合适的工具进行反编译，返回分析过程和结果
    """
    try:
        # 创建临时文件保存上传的二进制文件
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # 捕获分析过程的输出
        with capture_output() as (stdout, stderr):
            # 调用分析函数
            result_file = await run_in_threadpool(analyze_binary, prompt, tmp_path)
            
            # 获取捕获的输出
            process_output = stdout.getvalue()
            error_output = stderr.getvalue()

        # 删除临时文件
        os.unlink(tmp_path)

        # 检查结果是否是文件路径
        if os.path.exists(result_file):
            # 读取反编译结果文件内容
            with open(result_file, 'r', encoding='utf-8') as f:
                decompiled_content = f.read()
            
            # 返回完整的分析信息
            return JSONResponse({
                "status": "success",
                "process_output": process_output,
                "error_output": error_output,
                "decompiled_content": decompiled_content,
                "result_file": result_file,
                "agent_response": result_file  # 添加 Agent 的响应
            })
        else:
            # 如果返回的是文件路径但文件不存在，或者返回的是 Agent 的文本响应
            return JSONResponse({
                "status": "success",  # 改为 success，因为 Agent 确实返回了响应
                "process_output": process_output,
                "error_output": error_output,
                "agent_response": result_file,  # Agent 的响应
                "message": "分析完成，但未生成反编译文件"  # 可选的消息
            })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败：{str(e)}")

@app.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)