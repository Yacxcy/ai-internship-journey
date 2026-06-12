import os
import re
import tempfile
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import (PyPDFLoader, TextLoader, UnstructuredMarkdownLoader,)
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 导入环境变量
load_dotenv()

# 设置标题
st.set_page_config(page_title = "RAG 知识库助手",page_icon = "📚",layout = "wide")
st.title("📚 RAG 知识库助手")

# 数据库配置
PERSIST_DIR = "./chroma_db_ui"
if "collection_name" not in st.session_state:
    st.session_state.collection_name = "ui_docs" 

# 获取文件加载器
def get_loader(filepath:str):
    ext = Path(filepath).suffix.lower()
    if ext == ".pdf":
        return PyPDFLoader(filepath)
    if ext == ".md":
        return UnstructuredMarkdownLoader(filepath, encoding="utf-8")
    return TextLoader(filepath, encoding="utf-8")
# 获取embedding模型
@st.cache_resource
def get_embedder():
    return DashScopeEmbeddings(
        model = "text-embedding-v3",
        dashscope_api_key = os.getenv("DASHSCOPE_API_KEY"),
    )
# 获取向量数据库
@st.cache_resource
def get_vectorstore(collection_name:str):
    return Chroma(
        collection_name = collection_name,
        embedding_function = get_embedder(),
        persist_directory = PERSIST_DIR,
    )
# 获取聊天模型
@st.cache_resource
def get_llm():
    return ChatOpenAI(
        model = "deepseek-v4-pro",
        api_key = os.getenv("DEEPSEEK_API_KEY"), 
        base_url = os.getenv("DEEPSEEK_BASE_URL"),
    )
# 获取问答模型
@st.cache_resource
def build_chain(collection_name:str,top_key: int = 5):
    vs = get_vectorstore(collection_name) # 获取向量数据库
    retriever = vs.as_retriever(search_kwargs = {"k":top_key}) # 转成检索器

    prompt = ChatPromptTemplate.from_messages([
         ("system",
         "你是基于知识库的问答助手。\n"
         "必须基于「上下文」回答，不要编造。\n"
         "如果资料中没有，说「知识库中暂无相关信息」。\n"
         "末尾用 [文档名] 标注引用来源。\n\n"
         "上下文：\n{context}"),
        ("human", "{input}"),
    ])
    rag_chain =(
        {"context":retriever ,"input":RunnablePassthrough()}
        |prompt
        |get_llm()
        | StrOutputParser()
    )
    return rag_chain 

# 高亮检索关键词
def highlight(text:str,query:str)->str:
    """简单高亮：把 query 的词在原文里加粗"""
    words = [w for w in re.split(r"\s+", query) if len(w) > 1]
    for w in words:
        text = re.sub(f"({re.escape(w)})", r"**\1**", text, flags=re.IGNORECASE)
    return text

# 主区域
col_chat,col_refs = st.columns([2,1])

with col_chat:
    retriever = get_vectorstore(st.session_state.collection_name).as_retriever(search_kwargs={"k": 5})# 用于获取数据来源
    st.subheader("💬 提问")
    # 初始化对话历史
    if "history" not in st.session_state:
        st.session_state.history = []
    
    # 显示对话
    for m in st.session_state.history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # 用户输入
    if user_input :=st.chat_input("问点啥..."):
        st.session_state.history.append({"role": "user", "content": user_input}) # 把用户输入添加到对话历史
        # 显示用户输入
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("检索中..."):
                chain = build_chain(st.session_state.collection_name) # 构建RAG链
                answer = chain.invoke(user_input) # 调用RAG链得到答案
                docs = retriever.invoke(user_input)
            st.markdown(answer) # 显示答案

        st.session_state.history.append({"role": "assistant", "content": answer}) # 把助手回答添加到对话历史
        st.session_state.last_refs = docs # 把最后的引用保存到 session_state，供右侧引用区使用

with col_refs:
    st.subheader("📎 引用来源")
    if "last_refs" in st.session_state:
        for i,d in enumerate(st.session_state.last_refs):
            with st.expander(f"📄{d.metadata.get('source', '？')}（来源 {i+1}）"):
                st.markdown(highlight(d.page_content[:1000], user_input)) # 显示引用内容
                st.caption(f"页码:{d.metadata.get('page','N/A')}") # 显示页码
    else:
        st.info("提问后会显示引用文档")

# ---- 上传区 ----
with st.sidebar:  #创建左侧栏。
    st.header("📤 上传文档")
    uploaded = st.file_uploader(
        "选择 PDF / MD / TXT 文件",
        type = ["pdf","md","txt"],
        accept_multiple_files = True,  # 允许不同类型文件同时上传
    )

    chunk_size = st.slider("Chunk_size",200, 2000, 800, 100)
    overlap = st.slider("Overlap",0, 300, 100, 20)
    st.session_state.collection_name = st.text_input("知识库名", value="ui_docs")
    if st.button("🚀 入库",type = "primary") and uploaded :
        with st.spinner("处理中..."):
            splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = overlap) #创建分块器
            vs = get_vectorstore(st.session_state.collection_name) #获取向量数据库
            st.metric("当前知识库 chunks", vs._collection.count())
            for f in uploaded:
                with tempfile.NamedTemporaryFile(delete = False,suffix = Path(f.name).suffix) as tmp:
                    tmp.write(f.read())
                    tmp_path = tmp.name
                docs = get_loader(tmp_path).load() #加载文档
                # 把临时路径改成原文件名，UI 显示更友好
                for d in docs:
                    d.metadata["source"] = f.name
                chunks = splitter.split_documents(docs) #分块
                vs.add_documents(chunks) #入库
                st.success(f"✅ {f.name} 入库 {len(chunks)} 块")
            st.balloons()
    st.divider()
    st.markdown("**示例问题**")
    examples = ["你领域问题1", "你领域问题2", "你领域问题3"]
    for ex in examples:
        if st.button(ex):
            st.session_state.history.append({"role": "user", "content": ex}) # 把示例问题添加到对话历史
            st.rerun() # 重新运行，刷新界面显示示例问题 

    st.divider()
    if st.button("🗑️ 清空知识库"):
        vs = get_vectorstore(st.session_state.collection_name)
        vs.delete_collection() # 删除整个集合
        st.cache_resource.clear() # 清除缓存，重置向量数据库实例
        st.rerun() # 重新运行，刷新界面

