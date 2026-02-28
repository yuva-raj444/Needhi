"""
NyayaSahaya — RAG-based legal Q&A endpoint.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_service import RAGService

router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def ask_legal_question(request: QueryRequest):
    """
    Ask a legal question in Tamil or English.
    Uses RAG to retrieve relevant Indian law sections and generate a simplified answer.
    """
    try:
        rag = RAGService()
        result = await rag.answer_question(
            question=request.question,
            force_language=request.language,
        )
        return QueryResponse(
            answer=result["answer"],
            detected_language=result["detected_language"],
            sources=result["sources"],
            disclaimer=result["disclaimer"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
