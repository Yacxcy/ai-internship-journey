import os
import langchain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

langchain.debug = True  # 看每步输入输出

# 导入环境变量
load_dotenv()

llm = ChatOpenAI(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)

# Step 1: 英→中
translate = ChatPromptTemplate.from_template("Translate to Chinese:\n{text}") | llm | StrOutputParser()
# Step 2: 总结
summarize = ChatPromptTemplate.from_template("用 30 字总结：\n{chinese}") | llm | StrOutputParser()
# Step 3: 改写成营销文案
rewrite = ChatPromptTemplate.from_template("把这句话改写成有冲击力的营销标题：\n{summary}") | llm | StrOutputParser()

# 完整链
chain = (
    {"text":RunnablePassthrough()}
    |RunnablePassthrough.assign(chinese = translate) # 翻译结果放到 chinese
    |RunnablePassthrough.assign(summary = lambda X:summarize.invoke({"chinese":X["chinese"]})) # 总结结果放到 summary
    |RunnablePassthrough.assign(headline = lambda X:rewrite.invoke({"summary":X["summary"]})) # 改写结果放到 headline
)

result = chain.invoke(
    "LangChain provides a unified interface for building applications powered by large language models, "
    "including chat, RAG, and agents. Trusted by 100,000+ developers worldwide."
)

print(result)
print("英文原文:", result["text"][:80], "...")
print("中文翻译:", result["chinese"])
print("总结:", result["summary"])
print("营销标题:", result["headline"])