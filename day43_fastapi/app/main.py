from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import chat,documents

app = FastAPI(
    title = "Project 3 API",
    description = "基于 LangGraph + RAG + 多工具的 AI 应用",
    version = "1.0.0",
)

app.add_middleware(
    CORSMiddleware,  # 允许跨域 
    allow_origins = ["*"], # 允许所有请求源
    allow_methods = ["*"], # 允许所有请求方法
    allow_headers = ["*"], # 允许所有请求头
)

app.include_router(chat.router,prefix = "/api",tags = ["chat"])  # 添加路由,前缀为 /api,标签为 chat,用于在文档中分类
app.include_router(documents.router,prefix = "/api",tags = ["documents"])  # 添加路由,前缀为 /api,标签为 documents,用于在文档中分类

@app.get("/api/health")
def health():
    """
    健康检查函数，用于返回系统健康状态
    
    返回:
        dict: 包含系统健康状态的字典，其中status键表示健康状态
    """
    return {"status": "ok"}  # 返回健康状态字典，状态值为"healthy"