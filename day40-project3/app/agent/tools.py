from langchain_core.tools import tool
from app.rag.retriever import retrieve

@tool
def search_kb(query:str)->str:
    """从公司知识库中检索信息（员工手册、流程、政策、产品文档等）。
    用户问"我们""公司""内部"相关时优先使用。
    """
    docs = retrieve(query,k=5,user_rerank = True)
    if not docs:
        return "知识库中未找到相关信息"
    return "\n\n".join(f"[来源: {d.metadata.get('source')} 页 {d.metadata.get('page', '?')}]\n{d.page_content}" for d in docs)