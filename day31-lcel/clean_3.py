import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 导入环境变量
load_dotenv()

llm = ChatOpenAI(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)

# 第 1 步：翻译
translate = ChatPromptTemplate.from_template("把英文翻译成中文：{text}") | llm | StrOutputParser()
# 第 2 步：基于翻译结果做总结
summarize = ChatPromptTemplate.from_template("用一句话总结：{text}") | llm | StrOutputParser()

chain = translate | RunnablePassthrough(lambda X :{"text":X}) | summarize 
print(chain.invoke({"text": "RAG combines retrieval and generation."}))