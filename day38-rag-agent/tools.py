import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

# 导入环境变量
load_dotenv()

@tool
def search_knowledge_base(query:str)->str:
    """私有知识库中检索信息。
    适用场景：用户问公司/产品/项目内部信息，或者问"我们的"任何东西时使用。
    不适用：实时新闻、股价、天气等外部信息。

    参数 query: 检索关键词或问题。
    返回：相关文档片段及来源。
    """
    embedder = DashScopeEmbeddings(
        model = "text-embedding-v1", 
        dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    )
    vs = Chroma(
        collection_name = "project_name1",  # 知识库名称
        embedding_function = embedder,
        persist_directory = "./chroma_db"  # 持久化目录
    )
    docs = vs.similarity_search(query,k = 5) # 检索前5条
    if not docs:
        return "知识库中未找到相关信息"
    return "\n\n".join(
        f"[来源: {d.metadata.get('source', '?')} 页 {d.metadata.get('page', '?')}]\n{d.page_content}"
        for d in docs
    )