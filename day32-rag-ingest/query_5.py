import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

# 导入环境变量
load_dotenv()

embedder = DashScopeEmbeddings(
    model = "text-embedding-v3",
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY"),
)
vectorstore = Chroma(
    collection_name = "my_docs", # 集合名，类似数据库表名，不能重复
    embedding_function = embedder, # embedding实例
    persist_directory = "./chroma_db", # 持久化目录，必须和入库时一致
)

# 相似度检索
question = "你的领域问题"
results = vectorstore.similarity_search(question, k=5) # k是返回的相似结果数量
for i,doc in enumerate(results):
    print(f"--- Result {i+1} ---")
    print(doc.page_content[:200]) # 打印前200字符
    print(doc.metadata) # 打印元数据，如页码等

print("-"*100)
# 带分数
results_with_scores = vectorstore.similarity_search_with_score(question,k=3)
for document,score in results_with_scores:
    print(f"Score: {score:.4f}")
    print(document.page_content[:200])