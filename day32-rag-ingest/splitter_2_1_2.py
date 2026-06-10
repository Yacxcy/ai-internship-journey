from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on = headers_to_split_on)

md_text = """# 主题
内容...
## 子标题1
具体内容...
## 子标题2
更多内容...
"""
splits = md_splitter.split_text(md_text)

for s in splits:
    print(s.metadata, s.page_content[:50])