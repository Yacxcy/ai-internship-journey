import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.embeddings import  DashScopeEmbeddings

# 导入环境变量
load_dotenv()

# 初始化向量数据库
embedder = DashScopeEmbeddings(
    model = "text-embedding-v3",
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY"),
)

vectorstore = Chroma(
    collection_name = "my_docs",
    embedding_function = embedder,
    persist_directory = "./chroma_db"
)

retriever = vectorstore.as_retriever(search_kwargs={"k":5})

for q in ["你的领域问题1", "你的领域问题2"]:
    print(f"\n=== Q: {q} ===")
    docs = retriever.invoke(q)
    for i,d in enumerate(docs):
        print(f"[{i+1}] {d.page_content[:120]}...")

