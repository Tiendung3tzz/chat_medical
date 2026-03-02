from fastapi import Request

def get_retriever(request: Request):
    return request.app.state.hybrid_retriever


def get_generator(request: Request):
    return request.app.state.generator

def get_reranker(request: Request):
    return request.app.state.reranker

