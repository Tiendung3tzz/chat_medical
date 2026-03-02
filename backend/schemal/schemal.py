from pydantic import BaseModel
from typing import List, Any

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    tokens_used: int
    cost: float