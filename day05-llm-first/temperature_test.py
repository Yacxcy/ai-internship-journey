import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 从环境变量中获取DeepSeek API的key和base_url
client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)

# 定义prompt聊天消息
prompt = "给我一个 Python AI 项目名称的创意，要求好记又有点意思"

# 测试DeepSeek API
for temp in [0.0,0.7,1.]:
    print(f"\n=== temperature={temp} ===")
    for i in range(3):
        resp = client.chat.completions.create(
            model = "deepseek-v4-pro",
            messages=[{"role":"user","content":prompt}],
            temperature = temp,
            max_tokens = 200,
        )
        print(f"[{i+1}]{resp.choices[0].message.content.strip()}")
