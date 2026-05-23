import os # 导入os模块，用于访问环境变量
from openai import OpenAI # 导入OpenAI模块，用于访问OpenAI API
from dotenv import load_dotenv

load_dotenv() # 加载环境变量

client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"), # 从环境变量中获取API key
    base_url = os.getenv("DEEPSEEK_BASE_URL"), # 从环境变量中获取base_url
)

stream = client.chat.completions.create(
    model = "deepseek-v4-pro",
    messages = [{"role":"user","content":"用 100 字介绍一下 Python"}],
    stream = True, # 设置stream参数为True，启用流式输出
)
print("Bot:",end = "",flush = True) # 打印Bot:，并设置end=""和flush=True，使输出不换行并立即刷新

full_response = "" # 定义一个变量，用于保存完整的回复内容
for chunk in stream: # 遍历流式输出的每一块数据
    delta = chunk.choices[0].delta.content # 从每块数据中提取增量内容
    if delta: # 如果增量内容不为空
        print(delta,end = "",flush = True) # 打印增量内容，并设置end=""和flush=True，使输出不换行并立即刷新
        full_response += delta # 将增量内容添加到完整回复内容中
print()  # 换行
print(f"\n[完整长度 {len(full_response)} 字符]")
