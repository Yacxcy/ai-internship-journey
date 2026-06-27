import sys
from pathlib import Path
from langchain_community.document_loaders import (PyPDFLoader, UnstructuredMarkdownLoader, TextLoader,)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

sys.path.insert(0,Path(__file__).resolve().parents[2])
from app.config import settings


LOADERS = {
    ".pdf": PyPDFLoader,
    ".md": UnstructuredMarkdownLoader,
    ".txt": lambda p: TextLoader(p,encoding="utf-8"),
}

# 加载文档
def load_documents(docs_dir:Path):
    all_docs = []
    for p in docs_dir.rglob("*"):
        loader_cls = LOADERS.get(p.suffix.lower())
        if not loader_cls:
            continue
        try:
            print(f"加载{p.name}")
            docs = loader_cls(str(p)).load()
            for d in docs:
                d.metadata["source"] = p.name
            all_docs.extend(docs)
        except Exception as e:
            print(f"加载{p.name}失败: {e}")
    return all_docs


def main():
    docs_dir = Path("./data/docs")
    if not docs_dir.exists():
        print("请把文档放到 data/docs/")
        return
    
    all_docs = load_documents(docs_dir)
    if not all_docs:
        print("没有可加载的文档")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(all_docs)
    print(f"\n切分得到 {len(chunks)} 个 chunks")

    embedder = DashScopeEmbeddings(model = settings.EMBEDDING_MODEL)
    vs = Chroma(
        collection_name = settings.COLLECTION,
        embedding_function = embedder,
        persist_directory = settings.CHROMA_DIR
    )
    vs.add_documents(chunks)
    print(f"✅ 入库完成，库内现有 {vs._collection.count()} chunks")


if __name__ == "__main__":
    main()