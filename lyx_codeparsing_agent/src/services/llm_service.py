from openai import OpenAI
import logging
from typing import Dict, Any
import httpx

class LLMService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 设置代理
        transport = httpx.HTTPTransport(
            proxy="http://127.0.0.1:7890",
            verify=False
        )
        
        # 创建自定义的 httpx 客户端
        http_client = httpx.Client(
            transport=transport,
            timeout=30.0
        )
        
        # 设置 API 密钥和自定义 API 基础 URL
        api_key = 'sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11'
        base_url = 'https://api.gptapi.us/v1'
        
        # 初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            http_client=http_client
        )
        
    def query(self, prompt: str) -> str:
        """
        向 LLM 发送查询并获取响应
        """
        try:
            # 打印请求信息
            self.logger.info(f"正在发送请求到 OpenAI API...")
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的代码分析助手，擅长分析二进制代码和反编译。"},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # 打印详细的错误信息
            self.logger.error(f"LLM查询失败:")
            self.logger.error(f"错误类型: {type(e).__name__}")
            self.logger.error(f"错误信息: {str(e)}")
            if hasattr(e, 'response'):
                self.logger.error(f"响应状态码: {e.response.status_code}")
                self.logger.error(f"响应内容: {e.response.text}")
            raise