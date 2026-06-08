import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage,AIMessage

# 导入环境变量
load_dotenv()

llm = ChatOpenAI(
    model = "deepseek-v4-pro",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system","你是友好助手"),
    MessagesPlaceholder("history"),
    ("human","{input}"),
])

history = [
    HumanMessage(content="我叫 Yaai"),
    AIMessage(content="你好 Yaai！很高兴见到你。"),
]

# 渲染并查看
chain = prompt | llm 
resp = chain.invoke({"history":history,"input":"我叫什么？"})
print(resp.content)