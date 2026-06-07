import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 导入环境变量
load_dotenv()

llm = ChatOpenAI(
    model = "deepseek-v4-pro",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
    temperature = 0.7,
)

messages = [
    SystemMessage(content="你是简洁的 Python 老师"),
    HumanMessage(content="装饰器是啥"),
]

resp = llm.invoke(messages)
print(resp.content)

# 多轮
messages.append(AIMessage(content=resp.content)) # 添加AI的回复
messages.append(HumanMessage(content="请给我一个 3 行的例子")) # 添加新的用户输入
for msg in llm.stream(messages): # 获取模型回复
    print(msg.content, end="", flush=True)
