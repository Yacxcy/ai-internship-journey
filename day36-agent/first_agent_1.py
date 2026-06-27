import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.agents import create_agent

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

tools = [calculator, web_search]

# Agent 配置
llm  = ChatOpenAI(
    model = "deepseek-v4-pro",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
    temperature = 0,
)

agent = create_agent(
    model = llm,
    tools = tools,
    system_prompt="""
    你是一个有用的助手。

    你有以下工具：

    - calculator：计算数学表达式
    - web_search：搜索互联网

    需要时主动调用工具。
    无需工具时直接回答。
    """
)

# 测试
test_questions = [
    "(15 + 27) * 3 - 8 等于多少？",                  # 单工具
    "搜一下 2026 年最新 LLM 排行榜",                 # 单工具
    "北京到上海高铁多少分钟？再换算成秒",            # 多工具
    "你好，介绍一下你自己",                          # 不需工具
]

for q in test_questions:
    print(f"\n========== Q: {q} ==========")
    result = agent.invoke(
        {
            "messages":[
                {
                    "role":"user",
                    "content":q
                }
            ]
        }
    )
    print(f"\n[Final]")
    print(result["messages"][-1].content)