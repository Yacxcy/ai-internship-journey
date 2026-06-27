"""一次性入库脚本"""
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader,UnstructuredMarkdownLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

# 导入环境变量
load_dotenv()
# 加载器
def get_loader(path:str):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return PyPDFLoader(path)
    if ext == ".md":
        return UnstructuredMarkdownLoader(path, encoding="utf-8")
    return TextLoader(path, encoding="utf-8")

DOCS_DIR = Path("C:\\Users\\Ya\\Desktop\\练习\\ai-internship-journey\\day38-rag-agent\\data") #文档目录
all_chunks = [] #所有分块
splitter = RecursiveCharacterTextSplitter(chunk_size = 800,chunk_overlap = 100) #分块器

for p in DOCS_DIR.rglob("*"):  #遍历所有文件
    if p.suffix.lower() in (".pdf",".md",".txt"):
        print(f"加载 {p.name}")
        docs = get_loader(p).load() #加载文档
        for d in docs:
            d.metadata["source"] = p.name #添加来源
        chunks = splitter.split_documents(docs) #分块
        all_chunks.extend(chunks) #加入总列表

print(f"\n总共 {len(all_chunks)} chunks 入库...")
embedder = DashScopeEmbeddings(
    model = "text-embedding-v1",
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
)

vs = Chroma(
    collection_name = "project_name1", #知识库名称
    embedding_function = embedder,
    persist_directory = "./chroma_db" #持久化目录
)

vs.add_documents(all_chunks) #入库
print(f"✅ 完成，库内现有 {vs._collection.count()} chunks")
 