import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

# 导入环境变量
load_dotenv()

# 1. 加载PDF文档
docs = PyPDFLoader("C:\\Users\\Ya\\Desktop\\练习\\ai-internship-journey\\day32-rag-ingest\\data\\机器学习.pdf").load()

# 2. 切分
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 800, # 每个chunk的目标长度
    chunk_overlap = 100, # chunk之间的重叠长度，越大越能保留上下文，但会增加冗余
)
chunks = splitter.split_documents(docs)
print(f"切成 {len(chunks)} 块")

# 3. Embedding
embedder = DashScopeEmbeddings(
    model = "text-embedding-v3",
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY"),
)

# 4. 入 Chroma
vectorstore = Chroma.from_documents(
    documents = chunks,
    embedding = embedder,
    collection_name = "my_docs",
    persist_directory = "./chroma_db", # 持久化目录
)
print(f"已入库{vectorstore._collection.count()}条")