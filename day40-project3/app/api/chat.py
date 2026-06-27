import json
from fastapi import APIRouter,HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, ToolMessage
from app.agent.graph import app_graph

router = APIRouter() # 创建路由对象

class ChatRequest(BaseModel): # 定义前端请求结构
    message: str
    thread_id:str = "default"

class ChatResponse(BaseModel): # 定义后端响应结构
    answer:str
    tool_calls:list=[]
    references:list = []

@router.post("/chat",response_model = ChatResponse) # 定义路由
def chat(req:ChatRequest):#FastAPI 自动把 JSON 转成对象
    try:
        config = {"configurable":{"thread_id":req.thread_id}} # 从请求中获取thread_id
        request = app_graph.invoke(
            {"messages":[HumanMessage(content=req.message)]},
            config = config,
        )
        final = request["messages"][-1]  # 获取最后一条消息
        tool_calls = []  # 存储工具调用信息的列表
        references = []  # 存储引用信息的列表
        for m in request["messages"]:  # 遍历所有消息
            if hasattr(m, "tool_calls") and m.tool_calls:  # 检查消息是否有工具调用
                tool_calls.extend([{"name": t["name"], "args": t["args"]} for t in m.tool_calls])# 获取工具调用信息
            if isinstance(m, ToolMessage):  # 检查是否是工具消息
                references.append({"content": m.content[:1000]})  # 添加引用内容，限制长度为1000字符

        return ChatResponse(
            answer = final.content,  # 返回最终回答内容
            tool_calls = tool_calls,  # 返回工具调用信息
            references = references  # 返回引用信息
        )
    except Exception as e:  # 异常处理
        raise HTTPException(500, str(e))  # 抛出HTTP异常，状态码500，错误信息为异常信息

@router.post("/chat/stream") # 定义流式路由
def chat_stream(req:ChatRequest):
    def event_stream():
        config = {"configurable":{"thread_id":req.thread_id}} # 从请求中获取thread_id，用于配置流式处理
        for chunk in app_graph.stream(
            {"messages": [HumanMessage(content=req.message)]},
            config = config,
            stream_mode = "values", # 指定流式模型为 values
        ):
            last = chunk["messages"][-1]  # 获取最后一条消息
            if hasattr(last,"content") and isinstance(last.content,str):
                yield f"data: {json.dumps({'content': last.content}, ensure_ascii=False)}\n\n" # 返回JSON格式的数据
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")