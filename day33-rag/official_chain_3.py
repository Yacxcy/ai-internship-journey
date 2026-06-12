import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import  DashScopeEmbeddings
from langchain_community.chains import create_retrieval_chain
from langchain_community.chains import create_stuff_documents_chain

# 导入环境变量
load_dotenv()

embedder = DashScopeEmbeddings(
    model = "text-embedding-3-small",
    api_key = os.getenv("DASHSCOPE_API_KEY"),
)
vectorstore = Chroma(
    collection_name = "my_markdown_docs",
    embedding_function = embedder,
    persist_directory = "./chroma_db"
)
retriever = vectorstore.as_retriever(search_kwargs={"k":5})

llm = OpenAI(
    model = "deepseek-v4-pro",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)
# 文档组合 prompt
combine_prompt = ChatPromptTemplate.from_template([
        ("system",
     "你是基于知识库的问答助手。\n"
     "必须基于上下文回答。如果没有答案，说不知道。\n\n"
     "上下文：\n{context}"),
    ("human", "{input}"),
])

combine_chain = create_stuff_documents_chain(llm, combine_prompt)

# 完整 retrieval chain（自动调 retriever + combine）
rag_chain = create_retrieval_chain(retriever,combine_chain)

# 调用，输出有 input/context/answer
result = rag_chain.invoke({"input":"你的问题"})
print("回答:", result["answer"])
print("\n引用文档:")
for d in result["context"]:
    print(" -", d.metadata.get("source"), d.page_content[:80])
