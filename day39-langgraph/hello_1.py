from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. 定义状态
class State(TypedDict):
    counter:int
    message:str

# 2. 定义节点（函数）
def increment(state:State)->dict:
    return {"counter":state['counter']+1}

def to_message(state:State)->dict:
    return {"message":f"Counter is now {state['counter']}"}

# 3. 构建图
graph = StateGraph(State)
graph.add_node("inc",increment)
graph.add_node("msg",to_message)

graph.add_edge(START,"inc")
graph.add_edge("inc","msg")
graph.add_edge("msg",END)

# 4. 编译运行
app = graph.compile() # compile() 会把图转换成一个可执行程序。
result = app.invoke({"counter":0,"message":""}) # invoke() 会执行图，从 START 开始，直到 END。
print(result) # 输出最终状态
