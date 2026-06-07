import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 导入环境变量
load_dotenv()

# DeepSeek
deepseek = ChatOpenAI(
    model = "deepseek-v4-pro",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)

# 通义千问（百炼）
qwen = ChatOpenAI(
    model = "qwen-plus",
    api_key = os.getenv("QWEN_API_KEY"),
    base_url = os.getenv("QWEN_BASE_URL"),
)

# 测一个问题，对比两个模型
question = "Python 中 list 和 tuple 的区别是什么？"

print("=== DeepSeek ===")
print(deepseek.invoke(question).content[:200]) # 只显示前200字符

print("\n=== 通义千问 ===")
print(qwen.invoke(question).content[:200]) # 只显示前200字符
