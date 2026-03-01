from pydantic_settings import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "medical_rag"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Vector Store
    VECTOR_STORE_TYPE: str = "pinecone"
    QDRANT_URL: str = "http://localhost:6333"
    PINECONE_API_KEY: str = ""
    PINECONE_ENV: str = ""
    PINECONE_INDEX_NAME: str = "youmedmedical"

    # Models
    EMBEDDING_MODEL_PATH: str = ""
    RERANKER_MODEL_PATH: str = ""
    BM25_INDEX_PATH: str = ""
    EMBEDDING_DIM: int = 1024

    # Retrieval
    RETRIEVAL_TOP_K: int = 5
    RETRIEVAL_CANDIDATES: int = 20
    VECTOR_WEIGHT: float = 0.7
    BM25_WEIGHT: float = 0.3

    # Session
    SESSION_TTL: int = 3600
    MAX_CONVERSATION_TURNS: int = 4

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()