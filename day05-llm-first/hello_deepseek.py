import os # 导入os模块，用于访问环境变量
from openai import OpenAI # 导入OpenAI模块，用于访问OpenAI API
from dotenv import load_dotenv # 导入dotenv模块，用于加载环境变量

load_dotenv() # 加载环境变量

# 从环境变量中获取DeepSeek API的key和base_url
client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"), # 从环境变量中获取API key
    base_url = os.getenv("DEEPSEEK_BASE_URL"), # 从环境变量中获取base_url
)

# 测试DeepSeek API
resp = client.chat.completions.create( # 创建一个聊天完成请求
    model = "deepseek-v4-pro", # 使用deepseek-v4-pro模型
    messages = [
        {"role":"system","content":"你是一个简洁的 Python 老师"},# 系统消息，设置模型的角色和行为
        {"role":"user","content":"你是谁"},
    ],
)

# 输出模型的回复
print(resp.choices[0].message.content)
print("-"*10)
print(f"模型使用的token数量: {resp.usage.total_tokens}")