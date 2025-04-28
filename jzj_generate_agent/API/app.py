# app.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import uvicorn
from pydantic import BaseModel
from report_generator import generate_report

app = FastAPI()


class JSONInput(BaseModel):
    data: dict  # 接收一个 JSON 对象


@app.post("/generate_report")
async def create_report(input_data: JSONInput):
    markdown = generate_report(input_data.data)
    return {"markdown": markdown}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
