import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import asyncio

# 导入环境变量
load_dotenv()

llm = ChatOpenAI(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)

questions = [f"写一个 30 字的笑话 #{i}" for i in range(5)] # 5 个问题

# 同步串行
start = time.time()
for q in questions:
    llm.invoke(q)
print(f"同步串行耗时: {time.time() - start:.2f} 秒")

# 异步并行
async def run_async(): # 定义异步函数
    start = time.time()
    await asyncio.gather(*[llm.ainvoke(q) for q in questions]) # 并行调用
    print(f"异步并行耗时: {time.time() - start:.2f} 秒")
asyncio.run(run_async())