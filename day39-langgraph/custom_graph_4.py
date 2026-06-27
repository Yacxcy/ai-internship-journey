import os,json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import TypedDict,Annotated,Sequence
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages   #更新 messages 时自动追加，而不是覆盖。
from langchain_core.messages import BaseMessage,SystemMessage,HumanMessage,AIMessage,ToolMessage

# 导入环境变量
load_dotenv()

class State(TypedDict):
    messages:Annotated[Sequence[BaseMessage],add_messages]  # messages 是一个列表，且更新时自动追加，而不是覆盖。

@tool
def search(query: str) -> str:
    """搜索"""
    return f"模拟搜索 {query}: 找到 3 条结果"

tools = [search]
llm = ChatOpenAI(
    model = "deepseek-v4-pro",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
    temperature = 0
).bind_tools(tools) # 绑定工具

tools_by_name = {t.name:t for t in tools}

# Node 1: 让模型决策
def call_model(state:State)->dict:
    response = llm.invoke(state["messages"])
    return {"messages":[response]}  # 返回一个字典，包含 messages 键

# Node 2: 执行工具
def call_tools(state:State)->dict:
    last_msg = state["messages"][-1]  # 获取最后一条消息
    tool_msgs = []
    for tc in last_msg.tool_calls: # 遍历工具调用列表
         result = tools_by_name[tc["name"]].invoke(tc["args"])  # 调用工具
         tool_msgs.append(ToolMessage(content = str(result),tool_call_id = tc["id"])) # 创建工具消息,并关联工具调用 ID
    return {"messages":tool_msgs}  # 返回工具消息列表

# 路由：模型有 tool_calls → tools 节点；否则 → END
def should_continue(state:State)->str:
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END

# 构建
graph = StateGraph(State)
graph.add_node("agent",call_model)
graph.add_node("tools",call_tools)
graph.add_edge(START,"agent")
graph.add_conditional_edges("agent",should_continue,{"tools":"tools",END:END})
graph.add_edge("tools","agent") # 添加一个自环边

app = graph.compile()

# 调用
result = app.invoke({"messages":[HumanMessage(content = "搜一下 LangGraph 是什么")]})
for m in result["messages"]:
    m.pretty_print()