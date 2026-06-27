import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
import numexpr
from tavily import TavilyClient
from tools import search_knowledge_base
from dotenv import load_dotenv

load_dotenv()


@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    return str(numexpr.evaluate(expression).item())


@tool
def web_search(query: str) -> str:
    """搜索互联网获取**实时/最新/外部**信息（如新闻、股价、天气、人物等）。
    不适用：内部资料、公司专有信息（用 search_knowledge_base）。
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    result = client.search(query=query, max_results=3)
    return "\n".join(f"- {r['title']}: {r['content'][:300]}" for r in result.get("results", []))


tools = [search_knowledge_base, web_search, calculator]

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    temperature=0,
)

system_prompt = """你是企业知识助手 + 通用 AI 助手。

# 工具选择规则（重要）
- 用户问内部资料/产品/项目/政策 → 优先 search_knowledge_base
- 用户问实时/最新/外部信息（新闻、天气、股价、人物） → web_search
- 数学计算 → calculator
- 闲聊/通用问题 → 直接回答，不调用工具
- 复杂问题可以**串行调用多个工具**

# 回答要求
- 必须基于工具结果
- 引用来源：知识库引用文档名，搜索引用 URL
- 找不到就说"信息不足"，不要编造"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10, handle_parsing_errors=True)


def run(query: str, history: list = None):
    history = history or []
    return executor.invoke({"input": query, "chat_history": history})


if __name__ == "__main__":
    test_queries = [
        "我们公司的报销流程是怎样的？",        # → search_knowledge_base
        "2026 年 OpenAI 最新模型是什么？",      # → web_search
        "(125 + 75) * 0.13 = ?",              # → calculator
        "我们公司 Q2 销售目标 + 现在人民币兑美元汇率，算一下美元目标是多少？",  # 串行
        "你好，介绍一下你自己",                 # 不调工具
    ]
    for q in test_queries:
        print(f"\n{'=' * 50}\nQ: {q}\n{'=' * 50}")
        result = run(q)
        print(f"\n[Final] {result['output']}")