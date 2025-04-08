from openai import OpenAI
import httpx

# 设置代理
transport = httpx.HTTPTransport(
    proxy="http://127.0.0.1:7890",  # 根据您的代理设置修改
    verify=False  # 如果有SSL证书问题，可以禁用验证
)

# 创建自定义的 httpx 客户端
http_client = httpx.Client(
    transport=transport,
    timeout=30.0
)

# 设置 API 密钥和自定义 API 基础 URL
api_key = 'sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11'
base_url = 'https://api.gptapi.us/v1'

# 创建 OpenAI 客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
    http_client=http_client
)

# 定义消息列表
messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': 'Hello!'}
]

# 创建聊天补全请求
response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=messages
)

# 输出助手的回复
print(response.choices[0].message.content)
