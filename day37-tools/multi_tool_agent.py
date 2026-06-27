import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools import get_weather, add_calendar_event, list_calendar_events

# 导入环境变量
load_dotenv()

@tool
def calculator(expression:str):
    """计算数学表达式。仅支持加减乘除、括号、幂运算。  
    例：calculator("2*3+5") → "11"
    """
    import numexpr
    try:
        return(str(numexpr.evaluate(expression).item()))
    except Exception as e:
        return(f"计算错误: {e}")

@tool
def web_search(query:str)->str:
    """搜索互联网最新信息。当问题涉及实时/新近内容时使用。"""
    client = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))
    try:
        result = client.search(query =query,max_result = 3)
        return "\n".join(f"- {r['title']}: {r['content'][:200]}" for r in result.get("results", []))
    except Exception as e:
        return(f"搜索错误: {e}")

# 5 个工具
tools = [get_weather, add_calendar_event, list_calendar_events, calculator, web_search]

llm = ChatOpenAI(
    model = "deepseek-v4-pro",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
    temperature = 0,
)

agent = create_agent(
    model = llm,
    tools = tools,
    system_prompt= """
    你是个人 AI 助手。你有以下能力：
    - 查天气
    - 算数学
    - 搜互联网
    - 管理日历

    需要时主动调用工具。日期/时间请用标准格式。
    """
)

# 测试综合任务
test_queries = [
    "北京今天天气怎么样？",
    "(2 + 3) * 4 - 5 / 1.25",
    "明天 10 点提醒我开会",
    "明天有啥安排？",
    "北京今天天气、提醒我下午 3 点开会、再算一下 100*1.13 等于多少",  # 多工具串行
]

for q in test_queries:
    print(f"\n========== Q: {q} ==========")
    result = agent.invoke(
        {
            "messages":[
                {
                    "role":"user",
                    "content": q
                }
            ]
        }
    )
    print(f"\n[Final]")
    print(result["messages"][-1].content)