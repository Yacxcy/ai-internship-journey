import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import  DashScopeEmbeddings

# 导入环境变量
load_dotenv()

#准备
embedder = DashScopeEmbeddings(
    model = "text-embedding-v3",
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY"),
)
vectorstore = Chroma(
    collection_name = "my_markdown_docs",
    embedding_function = embedder,
    persist_directory = "./chroma_db"
)
retriever = vectorstore.as_retriever(search_kwargs={"k":5})

llm = ChatOpenAI(
    model = "deepseek-v4-pro",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是基于知识库的问答助手。\n"
     "必须基于「上下文」回答，不要编造。\n"
     "如果上下文中没有答案，说「知识库中暂无相关信息」。\n"
     "末尾用 [来源] 标注引用的文档。\n\n"
     "上下文：\n{context}"),
    ("human", "{question}"),
])

def format_docs(docs):
    return "\n\n".join(f"[文档{i+1} from {d.metadata.get("source","?")}]\n{d.page_content}" for i,d in enumerate(docs))

# 完整 RAG 链
chain = (
    {"context":retriever | format_docs,"question":RunnablePassthrough()}
    |prompt
    |llm
    |StrOutputParser()
)

# 测试
print(chain.invoke("invoke() 和 ainvoke() 的区别"))