import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

# 导入环境变量
load_dotenv()

llm = ChatOpenAI(
    model = "deepseek-v4-pro",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
    temperature = 0
)

@tool
def get_weather(city: str) -> str:
    """查城市天气"""
    return f"{city}: 22℃ 晴"

@tool
def calculator(expr: str) -> str:
    """算数"""
    import numexpr
    return str(numexpr.evaluate(expr).item())

# 一行代码 = 一个 Agent
agent = create_react_agent(llm,[get_weather, calculator])

# 调用
result = agent.invoke({
    "messages": [
        HumanMessage(content="北京今天天气，再算 2+3*4")
    ]
})

# 打印每条消息
for m in result["messages"]:
    m.pretty_print()