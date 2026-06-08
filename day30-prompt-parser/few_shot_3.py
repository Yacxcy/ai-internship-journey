import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,FewShotChatMessagePromptTemplate

# 导入环境变量
load_dotenv()

llm = ChatOpenAI(
    model = "deepseek-v4-pro",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)

example_prompt = ChatPromptTemplate.from_messages([
    ("human","{input}"),
    ("ai","{output}"),
])

examples = [
    {"input": "iPhone 15", "output": "手机/Apple"},
    {"input": "MacBook Air", "output": "电脑/Apple"},
    {"input": "AirPods", "output": "耳机/Apple"},
]

few_shot = FewShotChatMessagePromptTemplate(
    example_prompt = example_prompt,
    examples = examples,
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system","按例子格式输出商品分类。"),
    few_shot,
    ("human","{input}")
])

# 测试
chain = final_prompt | llm
print(chain.invoke({"input": "iPad Pro"}).content)
print(chain.invoke({"input": "罗技 MX Master 3"}).content)