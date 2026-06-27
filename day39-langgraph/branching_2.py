from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image

# 1. 定义状态
class State(TypedDict):
    value:int
    result:str

# 2. 定义节点（函数）
def classify(state:State)->dict:
    return {"result":""}

def positive(state:State)->dict:
    return {"result":"正数"}

def negative(state:State)->dict:
    return {"result":"负数"}

def zero(state:State)->dict:
    return {"result":"零"}

def route(state:State)->str:
    """根据 state 决定下一节点"""
    if state["value"] >0:
        return "positive"
    elif state["value"] <0:
        return "negative"
    return "zero"

# 3. 构建图
graph = StateGraph(State)
graph.add_node("classify",classify)
graph.add_node("positive",positive)
graph.add_node("negative",negative)
graph.add_node("zero",zero)

graph.add_edge(START,"classify")
graph.add_conditional_edges("classify",route,{
    "positive":"positive",
    "negative":"negative",
    "zero":"zero"
})
graph.add_edge("positive",END)
graph.add_edge("negative",END)
graph.add_edge("zero",END)

# 4. 编译运行
app = graph.compile() # compile() 会把图转换成一个可执行程序。
print(app.invoke({"value": 5, "result": ""}))
print(app.invoke({"value": -3, "result": ""}))
print(app.invoke({"value": 0, "result": ""}))

print(app.get_graph().draw_mermaid())