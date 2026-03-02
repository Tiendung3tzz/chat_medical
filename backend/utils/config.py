from pydantic_settings import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Vector Store
    VECTOR_STORE_TYPE: str = "pinecone"
    PINECONE_API_KEY: str = ""
    PINECONE_ENV: str = ""
    PINECONE_INDEX_NAME: str = "youmedmedical"

    # Models
    EMBEDDING_MODEL_PATH: str = "backend/models/bge_m3.onnx"
    RERANKER_MODEL_PATH: str = "backend/models/bge_m3_rerank.onnx"
    BM25_INDEX_PATH: str = "backend/models/bm25_encoder.pkl"
    EMBEDDING_DIM: int = 1024

    # Retrieval
    RETRIEVAL_TOP_K: int = 5
    RETRIEVAL_CANDIDATES: int = 20
    ALPHA: float = 0.7

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()