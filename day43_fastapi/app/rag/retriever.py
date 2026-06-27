from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from app.config import settings

import dashscope # 用于调用rerank 模型（重排序模型）

#全局缓存变量
_embedder = None
_vs = None

def get_vectorstore():
    # 声明使用全局变量 _vs 和 _embedder
    global _vs, _embedder
    # 检查向量存储对象 _vs 是否为 None
    if _vs is None:
        # 创建 DashScopeEmbeddings 对象，用于文本嵌入
        _embedder = DashScopeEmbeddings(dashscope_api_key = settings.EMBEDDING_API_KEY)
        # 创建 Chroma 向量存储对象
        # collection_name: 指定集合名称
        # embedding_function: 使用上面创建的嵌入器
        # persist_directory: 指定持久化目录路径
        _vs = Chroma(
            collection_name = settings.COLLECTION,
            embedding_function = _embedder,
            persist_directory = settings.CHROMA_DIR,
        )
    # 返回向量存储对象
    return _vs

def retrieve(query:str,k:int = 5,user_rerank:bool = True):
    vs = get_vectorstore()
    initial_k = 20 if user_rerank else k
    docs = vs.similarity_search(query,k=initial_k)

    if user_rerank and docs:
        try:
            resp = dashscope.TextReRank.call(
                model = "gte-rerank",
                query = query,
                documents = [d.page_content for d in docs],
                top_n = k,
                dashscope_api_key = settings.EMBEDDING_API_KEY,
            )
            if resp.status_code == 200:
                ranked = []
                for r in resp.output["results"]:
                    d = docs[r["index"]]
                    d.metadata["rerank_score"] = r.get("relevance_score",0)
                    ranked.append(d)
                return ranked
        except Exception as e:
            print(f"Rerank 失败: {e}")

    return docs[:k]