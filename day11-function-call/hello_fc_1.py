import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL")) # 创建OpenAI客户端实例

# 1. 定义工具（JSON Schema 格式）
tools = [
    {
        "type":"function",
        "function":{
            "name":"get_weather",
            "description": "查询某个城市的实时天气",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type": "string",
                        "description": "城市名，例如 北京",
                    },
                },
                "required": ["city"],
            },
        },
    }
]

# 2. 发起请求
messages = [{"role":"user","content":"北京今天多少度？"}]

resp = client.chat.completions.create(
    model  = "deepseek-v4-pro",
    messages = messages,
    tools = tools, # 提供工具定义
    tool_choice = "auto", # 让模型自动选择是否调用工具
)

msg = resp.choices[0].message
print("模型决策:", msg)

# 3. 检查模型是否要调工具
if msg.tool_calls:
    for tc in msg.tool_calls:
        print(f"\n工具名: {tc.function.name}")
        print(f"参数: {tc.function.arguments}")