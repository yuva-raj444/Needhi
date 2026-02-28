"""
NyayaSahaya — Pydantic schemas for request / response models.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


# ── RAG Q&A ──────────────────────────────────────────────────
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000, description="Legal question in Tamil or English")
    language: Optional[str] = Field(None, description="Force language: 'ta' or 'en'. Auto-detected if omitted.")


class SourceChunk(BaseModel):
    text: str
    source: Optional[str] = None
    score: Optional[float] = None


class QueryResponse(BaseModel):
    answer: str
    detected_language: str
    category: Optional[str] = None
    sources: list[SourceChunk] = []
    disclaimer: str = "This AI provides general legal information and is not a substitute for professional legal advice."


# ── Classifier ───────────────────────────────────────────────
class ClassifyRequest(BaseModel):
    description: str = Field(..., min_length=5, max_length=3000, description="Describe your legal issue")


class ClassifyResponse(BaseModel):
    category: str
    confidence: Optional[str] = None
    explanation: str
    detected_language: str
    disclaimer: str = "This AI provides general legal information and is not a substitute for professional legal advice."


# ── Complaint ────────────────────────────────────────────────
class ComplaintRequest(BaseModel):
    complainant_name: str = Field(..., min_length=2, max_length=200)
    complainant_address: str = Field(..., min_length=5, max_length=500)
    opponent_name: str = Field(..., min_length=2, max_length=200)
    issue_description: str = Field(..., min_length=10, max_length=5000)
    location: str = Field(..., min_length=2, max_length=300)
    date: str = Field(..., description="Date of incident (YYYY-MM-DD)")
    language: Optional[str] = Field("en", description="'ta' or 'en'")


class ComplaintResponse(BaseModel):
    draft_text: str
    language: str
    disclaimer: str = "This AI provides general legal information and is not a substitute for professional legal advice."


# ── Document Upload ──────────────────────────────────────────
class DocumentIndexResponse(BaseModel):
    message: str
    documents_processed: int
    total_chunks: int


class DocumentUploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int
