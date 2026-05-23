import os # 导入os模块，用于访问环境变量
from openai import OpenAI # 导入OpenAI模块，用于访问OpenAI API
from dotenv import load_dotenv # 导入dotenv模块，用于加载环境变量

load_dotenv() # 加载环境变量

client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"), # 从环境变量中获取API key
    base_url = os.getenv("DEEPSEEK_BASE_URL"), # 从环境变量中获取base_url
)

# 定义一个消息列表，包含系统消息和用户输入的文本,记录的对话的上下文信息
messages = [
    {"role":"system","content":"你是简洁友好的 Python 老师"},
]

#第一轮对话
messages.append({"role":"user","content":"Python 的装饰器是什么？"})
resp = client.chat.completions.create(
    model = "deepseek-v4-pro",
    messages = messages, # 将消息列表作为参数传递给模型
)
reply = resp.choices[0].message.content # 输出模型的回复
messages.append({"role":"assistant","content":reply}) # 将模型的回复添加到消息列表中，作为下一轮对话的上下文
print("Bot:", reply)

#第二轮对话
messages.append({"role":"user","content":"给我一个 3 行的例子"})
resp = client.chat.completions.create(
    model = "deepseek-v4-pro",
    messages = messages,
)
reply = resp.choices[0].message.content
messages.append({"role":"assistant","content":reply})
print("Bot:", reply)