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

prompt = ChatPromptTemplate.from_template("用一句话解释 {term}")

# 经典三件套
chain = prompt | llm | StrOutputParser()

# 三种调用方式
print(chain.invoke({"term": "RAG"})) # 同步
print(list(chain.stream({"term": "RAG"}))) # 流式
print(chain.batch([{"term": "RAG"}, {"term": "Agent"}])) # 批量