import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import  StrOutputParser
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (PyPDFLoader, TextLoader, UnstructuredMarkdownLoader,)


# 导入环境变量
load_dotenv()
# 数据库配置
PERSIST_DIR = "./chroma_db"
COLLECTION = "my_docs"


def get_loader(filepath: str):
    """根据后缀选 loader"""
    ext = Path(filepath).suffix.lower()
    if ext == ".pdf":
        return PyPDFLoader(filepath)
    if ext == ".md":
        return UnstructuredMarkdownLoader(filepath)
    return TextLoader(filepath, encoding="utf-8")


def ingest(files: list):
    """入库"""
    embedder = DashScopeEmbeddings(model="text-embedding-v3")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

    all_chunks = []
    for f in files:
        print(f"加载 {f}...")
        docs = get_loader(f).load()
        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)
        print(f"  → {len(chunks)} chunks")

    vectorstore = Chroma(
        collection_name=COLLECTION,
        embedding_function=embedder,
        persist_directory=PERSIST_DIR,
    )
    vectorstore.add_documents(all_chunks)
    print(f"\n总计入库 {len(all_chunks)} chunks")


def chat():
    """问答模式"""
    embedder = DashScopeEmbeddings(model="text-embedding-v3")
    vectorstore = Chroma(
        collection_name=COLLECTION,
        embedding_function=embedder,
        persist_directory=PERSIST_DIR,
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL"),
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "你是基于知识库的助手。必须基于上下文回答。\n"
         "末尾用 [文档名] 引用。\n\n"
         "上下文：\n{context}"),
        ("human", "{input}"),
    ])
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    rag_chain = (
        {"context":retriever | format_docs,"input": RunnablePassthrough()}
        |prompt
        |llm
        |StrOutputParser()
    )

    print("RAG 已就绪。输入 /quit 退出。\n")
    while True:
        q = input("Q: ").strip()
        if not q:
            continue
        if q == "/quit":
            break
        answer = rag_chain.invoke(q)
        print("\nA:", answer)
        docs = retriever.invoke(q)
        print("\n引用：")
        for d in docs[:3]:
            src = d.metadata.get("source", "?")
            print(f"  - {Path(src).name}")
        print()


def main():
    parser = argparse.ArgumentParser()   # 支持命令行参数 
    sub = parser.add_subparsers(dest="cmd", required=True) #支持ingest、chat

    ing = sub.add_parser("ingest")  #允许python xxx.py ingest a.pdf b.md
    ing.add_argument("files", nargs="+", help="文件路径列表")

    sub.add_parser("chat")  #支持python xxx.py chat

    args = parser.parse_args() #解析参数，得到"ingest"/"chat"
    if args.cmd == "ingest":
        ingest(args.files)
    elif args.cmd == "chat":
        chat()


if __name__ == "__main__":
    main()