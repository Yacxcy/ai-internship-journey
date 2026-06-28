import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain_community.document_loaders import (PyPDFLoader, UnstructuredMarkdownLoader, TextLoader,)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.retriever import get_vectorstore
from app.config import settings

router = APIRouter()  # 创建路由对象
DOCS_DIR = Path("./data/docs")  # 定义文档存储目录
DOCS_DIR.mkdir(parents=True, exist_ok=True) # 如果不存在则创建目录

@router.post("/documents/upload") # 定义上传文档的路由
async def upload(file:UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower() # 获取文件后缀并转换为小写
    if suffix not in [".pdf", ".md", ".txt"]: # 检查文件类型是否支持
        raise HTTPException(400, "仅支持 PDF/MD/TXT") # 抛出HTTP异常，状态码400，错误信息为不支持的文件类型

    save_path = DOCS_DIR / file.filename # 定义保存文件的路径
    with open(save_path,"wb") as f: # 打开文件，以二进制写入模式
        shutil.copyfileobj(file.file,f) # 将上传的文件内容写入保存路径

    if suffix == ".pdf": # 如果是PDF文件
        loader = PyPDFLoader(str(save_path)) # 使用PyPDFLoader加载文件
    elif suffix == ".md": # 如果是MD文件
        loader = UnstructuredMarkdownLoader(str(save_path)) # 使用UnstructuredMarkdownLoader加载文件
    else: # 如果是TXT文件
        loader = TextLoader(str(save_path),encoding = "utf-8") # 使用TextLoader加载文件

    docs = loader.load() # 加载文档内容
    for d in docs: # 遍历文档内容
        d.metadata["source"] = file.filename # 添加文件名到文档元数据中
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = settings.CHUNK_SIZE, # 设置分块大小
        chunk_overlap = settings.CHUNK_OVERLAP, # 设置分块重叠大小
    )
    chunks = splitter.split_documents(docs) # 将文档内容分块
    get_vectorstore().add_documents(chunks) # 将分块后的文档添加到向量存储中

    return {"file": file.filename, "chunks": len(chunks)}

@router.get("/documents")
def list_documents():
    return [
        {"name":p.name,"size":p.stat().st_size}
        for p in DOCS_DIR.iterdir() if p.is_file()
    ]