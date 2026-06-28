import json
import time
from pathlib import Path
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
    tokens: dict = {} # 添加 tokens 字段
    duration: float = 0.0 # 添加 duration 字段

# 日志记录
LOG_FILE = Path("./data/chat_log.jsonl")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # 确保目录存在

def log_chat(thread_id:str,question:str,answer:str,tool_calls:list,duration:float):
    record = {
        "ts":time.time(),
        "thread_id":thread_id,
        "question":question,
        "answer":answer,
        "tool_count":len(tool_calls),
        "tool_used": [t["name"] for t in tool_calls],
        "duration_sec":round(duration,2),
    }
    with open(LOG_FILE,"a",encoding = "utf-8") as f:
        f.write(json.dumps(record,ensure_ascii=False)+"\n")

@router.post("/chat",response_model = ChatResponse) # 定义路由
def chat(req:ChatRequest):#FastAPI 自动把 JSON 转成对象
    start = time.time()
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

        duration = time.time() - start  # 计算处理时间
        log_chat(req.thread_id,req.message,final.content,tool_calls,duration) # 记录日志
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
        start = time.time()
        full = ""
        tool_calls = []  # 存储工具调用信息的列表
        config = {"configurable":{"thread_id":req.thread_id}} # 从请求中获取thread_id，用于配置流式处理
        for chunk in app_graph.stream(
            {"messages": [HumanMessage(content=req.message)]},
            config = config,
            stream_mode = "values", # 指定流式模型为 values
        ):
            last = chunk["messages"][-1]  # 获取最后一条消息
            # 收集 tool_calls
            if hasattr(last, "tool_calls") and last.tool_calls:
                tool_calls.extend(last.tool_calls)
            # 收集 content
            if hasattr(last,"content") and isinstance(last.content,str):
                full += last.content
                yield f"data: {json.dumps({'content': last.content}, ensure_ascii=False)}\n\n" # 返回JSON格式的数据

        duration = time.time() - start  # 计算处理时间
        log_chat(req.thread_id,req.message,full,tool_calls,duration) # 记录日志
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
