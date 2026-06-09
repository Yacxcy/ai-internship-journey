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
translate_prompt = ChatPromptTemplate.from_template("把下面英文翻译成中文：{english}")
translate_chain = translate_prompt | llm | StrOutputParser()

# 第 2 步：基于翻译结果做总结
summarize_prompt = ChatPromptTemplate.from_template("用一句话总结：{chinese}")
summarize_chain = summarize_prompt | llm | StrOutputParser()

# 串联
combined = (
    {"english":RunnablePassthrough()}  # 接收输入
    | translate_chain                  # 翻译 → 字符串
    |(lambda x :{"chinese":x})         # 包装成字典给下一步
    |summarize_chain
)

print(combined.invoke("LangChain is a framework for building applications with LLMs."))