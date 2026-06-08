import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# 导入环境变量
load_dotenv()

llm = ChatOpenAI(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)

parser = JsonOutputParser() # 创建 JsonOutputParser 实例

# 1. 简单 ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system","输出 JSON，包含 name(string), tags(string[]) 字段。"),
    ("human","{input}"),
])

# 测试
chain = prompt | llm |parser # 加上 JsonOutputParser
print(chain.invoke({"input": "我叫小明，标签：程序员、咖啡爱好者"}))