import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

# 导入环境变量
load_dotenv()

llm = ChatOpenAI(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)

# 1. 简单 ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system","你是{role},回答简洁。"),
    ("human","{question}"),
])

# 渲染并查看
messages = prompt.format_messages(role="Python老师",question="什么是装饰器？")
for m in messages:
    print(m.type,":",m.content)

# 调模型
chain = prompt | llm
result = chain.stream({"role":"Python老师","question":"什么是装饰器？"})
for r in result:
    print(r.content,end="",flush=True)