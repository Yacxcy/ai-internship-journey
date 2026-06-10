from langchain_community.document_loaders import (PyPDFLoader,
    TextLoader,
    DirectoryLoader,
    UnstructuredMarkdownLoader,
    WebBaseLoader,)

# 1. PDF
docs = PyPDFLoader("C:\\Users\\Ya\\Desktop\\练习\\ai-internship-journey\\day32-rag-ingest\\data\\机器学习.pdf").load()
print(f"PDF共{len(docs)}页")
print(docs[0].page_content[:200])
print(docs[0].metadata)     # {'source': ..., 'page': 0}
print("-"*50)

# 2. TXT
docs = TextLoader("C:\\Users\\Ya\\Desktop\\练习\\ai-internship-journey\\day32-rag-ingest\\data\\1.txt",encoding="utf-8").load()
print(docs[0].page_content[:200])
print("-"*50)

# 3. Markdown
docs = UnstructuredMarkdownLoader("C:\\Users\\Ya\\Desktop\\练习\\ai-internship-journey\\day32-rag-ingest\\data\\Python 异步编程与 LangChain 高并发详解.md", encoding="utf-8").load()
print(docs[0].page_content[:200])
print("-"*50)

# 4. 整个目录
docs = DirectoryLoader(
    "C:\\Users\\Ya\\Desktop\\练习\\ai-internship-journey\\day32-rag-ingest\\data\\",
    glob = "**\\*.pdf", # 只加载pdf文件
    loader_cls = PyPDFLoader, # 用PyPDFLoader加载
    ).load()
print(f"目录下共{len(docs)}页PDF")
print(docs[1].page_content[:200])
print("-"*50)

# 5. 网页
docs = WebBaseLoader("https://python.langchain.com/docs/introduction/").load()
print(docs[0].page_content[:200])
print(docs[0].metadata) # {'source': 'https://python.langchain.com/docs/introduction/'}
