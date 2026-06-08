import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

chain = prompt | llm | StrOutputParser() # 加上 StrOutputParser
print(chain.invoke({"role": "翻译", "question": "Hello"}))
