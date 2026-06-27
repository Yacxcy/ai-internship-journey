import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    LLM_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    LLM_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
    LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-v4-pro")

    EMBEDDING_API_KEY = os.getenv("DASHSCOPE_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v1")

    SEARCH_API_KEY = os.getenv("TAVILY_API_KEY")

    CHROMA_DIR = os.getenv("CHROMA_DIR", "./data/chroma_db")
    COLLECTION = os.getenv("COLLECTION", "project3")

    CHECKPOINT_DB = os.getenv("CHECKPOINT_DB", "./data/checkpoints.db")

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))
    TOP_K = int(os.getenv("TOP_K", 5))


settings = Settings()