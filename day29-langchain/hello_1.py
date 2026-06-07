import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

# 导入环境变量
load_dotenv()

# 用 OpenAI 兼容协议接入 DeepSeek
llm = ChatOpenAI(
    model = "deepseek-v4-pro",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
    temperature = 0.7,
)

# 1. 直接调用
response = llm.invoke("用一句话解释 LangChain 是什么")
print(response.content)

# 2. 流式输出
print("\n--- 流式 ---")
for chunk in llm.stream("写一段 50 字的 Python 装饰器介绍"):
    print(chunk.content,end="",flush = True)
print()

# 3. 批量调用
print("\n--- 批量 ---")
results = llm.batch([
    "翻译：Hello world",
    "翻译：你好世界",
])
for r in results:
    print(r.content)