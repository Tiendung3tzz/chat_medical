import time
from fastapi import APIRouter, Depends

from backend.dependencies import get_retriever, get_generator, get_reranker
from backend.schemal.schemal import ChatRequest, ChatResponse
from core.HybridRetriever import HybridRetriever
from core.LLMGenerator import LLMGenerator
from utils.config import settings
from utils.logger import setup_logger

router = APIRouter(prefix="/chat", tags=["Chat"])
logger = setup_logger(__name__)


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    retriever: HybridRetriever = Depends(get_retriever),
    reranker = Depends(get_reranker),
    generator: LLMGenerator = Depends(get_generator),
):

    t0 = time.time()
    retrieved_chunks = retriever.retrieve(
        request.query,
        top_k=20,
    )
    retrieval_latency = time.time() - t0
    
    t0 = time.time()
    chunk_reranked = reranker.rerank(request.query, retrieved_chunks.matches, top_k=5)
    reranked_latency = time.time() - t0

    t0 = time.time()
    result = generator.generate(
        query=request.query,
        retrieved_chunks=chunk_reranked,
        conversation_history=[], 
    )
    llm_latency = time.time() - t0

    logger.info(
        "Retrieval: %.2fs | Reranking: %.2fs | LLM: %.2fs | Tokens: %s | Cost: $%.4f",
        retrieval_latency,
        reranked_latency,
        llm_latency,
        result["output_tokens"]+result["input_tokens"],
        result["cost"],
    )

    return ChatResponse(
        answer=result["answer"],
        tokens_used=result["output_tokens"]+result["input_tokens"],
        cost=result["cost"],
    )