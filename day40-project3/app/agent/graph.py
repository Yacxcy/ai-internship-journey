from typing import TypedDict,Annotated,Sequence
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,  START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from app.config import settings
from app.agent.tools import search_kb
import os
from langchain_core.tools import tool
from tavily import TavilyClient
import numexpr
import sqlite3

@tool
def web_search(query:str)->str:
    """搜索互联网获取实时信息。"""
    client = TavilyClient(api_key = settings.SEARCH_API_KEY)
    try:
        result = client.search(query = query,max_result = 3)
        return "\n".join(f"- {r['title']}: {r['content'][:300]}" for r in result.get("results", []))
    except Exception as e:
        return f"搜索失败: {str(e)}"


@tool
def calculator(expression:str)->str:
    """计算数学表达式"""
    return str(numexpr.evaluate(expression).item())

tools = [search_kb,web_search,calculator]
tools_by_name = {t.name: t for t in tools}

SYSTEM = """你是企业 AI 助手。

# 工具规则
- 公司/内部/产品 → search_kb
- 实时/最新/外部 → web_search
- 数学 → calculator
- 普通对话 → 直接回答

# 回答要求
- 必须基于工具结果
- 标注来源
- 找不到说"信息不足"
"""

class State(TypedDict):
    messages:Annotated[Sequence[BaseMessage],add_messages]

def call_model(state:State):
    llm = ChatOpenAI(
        model = settings.LLM_MODEL,
        api_key = settings.LLM_API_KEY,
        base_url = settings.LLM_BASE_URL,
        temperature = 0,
    ).bind_tools(tools)
    response = llm.invoke([SystemMessage(content=SYSTEM)] + list(state["messages"]))
    return {"messages":[response]}

def call_tools(state:State):
    last = state["messages"][-1]
    msgs = []
    for tc in last.tool_calls:
        try:
            result = tools_by_name[tc["name"]].invoke(tc["args"])
        except Exception as e:
            result = f"工具执行错误: {e}"
        msgs.append(ToolMessage(content = str(result),tool_call_id = tc["id"])) # 把工具结果返回给 LLM
    return {"messages":msgs}

def should_continue(state:State):
    return "tool" if state["messages"][-1].tool_calls else END

graph = StateGraph(State)
graph.add_node("agent",call_model)
graph.add_node("tools",call_tools)
graph.add_edge(START,"agent")
graph.add_conditional_edges("agent",should_continue,{"tool":"tools",END:END})
graph.add_edge("tools","agent")

def get_app():
    db_path = settings.CHECKPOINT_DB
    # 确保数据库文件所在的目录存在（sqlite3.connect 不会自动创建目录）
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    memory = SqliteSaver(conn)
    return graph.compile(checkpointer=memory)  # 把图变成”可运行 AI 系统”，并支持多轮对话、session记忆

app_graph = get_app()

def chat(user_input:str,thread_id :str = "default"):
    config = {"configurable":{"thread_id":thread_id}}
    result = app_graph.invoke(
        {"messages":[HumanMessage(content = user_input)]},
        config = config,
    )
    return result["messages"][-1].content