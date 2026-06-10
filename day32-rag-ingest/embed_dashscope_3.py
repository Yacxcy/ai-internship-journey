import os
from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings

# 导入环境变量
load_dotenv()

embedder = DashScopeEmbeddings(
    model = "text-embedding-v3",
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY"),
)

# 单个 embed
vec = embedder.embed_query("Python 装饰器是啥？")
print(f"维度：{len(vec)}")

# 单个 embed
vecs = embedder.embed_documents([
    "Python 装饰器是修改函数行为的语法糖",
    "RAG 是检索增强生成",
    "今天天气不错",
])
print(f"批量结果: {len(vecs)} 个向量")