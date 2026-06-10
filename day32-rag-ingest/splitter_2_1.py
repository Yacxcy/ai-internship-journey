from langchain_text_splitters import RecursiveCharacterTextSplitter

spliter = RecursiveCharacterTextSplitter(
    chunk_size = 800,
    chunk_overlap = 100,
    # 优先级递减的分隔符
    separators = ["\n\n", "\n", "。", "！", "？", "，", " ", ""],
    length_function = len, # 计算文本长度的函数，默认为len，也可以自定义
)

text = "..."*1000
chunks = spliter.split_text(text)
print(f"切成{len(chunks)}个chunk")
print(chunks[0][:100])

# 切 Document（保留 metadata）
from langchain_core.documents import Document
docs = [Document(page_content = text,metadata = {"source":"test.pdf"})]
split_docs = spliter.split_documents(docs)
for doc in split_docs:
    print(doc.metadata)
print(split_docs[0].metadata) # 元数据保留 + 加上分块信息