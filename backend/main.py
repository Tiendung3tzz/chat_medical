import sys
from pathlib import Path
import logging
import pickle

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.routes import chat
from .utils.config import settings
from backend.core.EmbeddingModel import ONNXEmbeddingModel, BM25Encoder
from .core.ONNXReranker import ONNXReranker
from .core.HybridRetriever import HybridRetriever
from .core.LLMGenerator import LLMGenerator
from .core.IndexManager import PineconeIndexManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading models...")
    app.state.embedding_model = ONNXEmbeddingModel(settings.EMBEDDING_MODEL_PATH)
    app.state.reranker = ONNXReranker(
        settings.RERANKER_MODEL_PATH
    )
    app.state.bm25_encoder = BM25Encoder(settings.BM25_INDEX_PATH)

    vector_kwargs = {}
    vector_kwargs["api_key"] = settings.PINECONE_API_KEY
    vector_kwargs["index_name"] = settings.PINECONE_INDEX_NAME
    vector_kwargs["environment"] = settings.PINECONE_ENV or None

    
    
    app.state.index_manager = PineconeIndexManager(**vector_kwargs)

    app.state.hybrid_retriever = HybridRetriever(
        index_manager=app.state.index_manager,
        embedding_model=app.state.embedding_model,
        bm25=app.state.bm25_encoder,
        candidate=settings.RETRIEVAL_CANDIDATES,
    )

    app.state.generator = LLMGenerator(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
    )
     
    logger.info("Models loaded successfully!")

    yield
    logger.info("Shutting down...")
app = FastAPI(
    title="Medical RAG Chatbot API",
    lifespan=lifespan,
    version="1.0.0",
    description="AI-powered medical chatbot using RAG",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://chat-medical.vercel.app",
        "https://chathealth.site",
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat.router)
@app.get("/")
async def root():
    return {"message": "Welcome to the Medical RAG Chatbot API!"}