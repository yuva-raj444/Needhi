"""
NyayaSahaya — FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import query, classifier, complaint, documents


# ── Ensure data directories exist ──────────────────────────
def _ensure_dirs():
    settings = get_settings()
    for d in (settings.data_dir, settings.sample_docs_dir, settings.vector_store_dir):
        Path(d).mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    _ensure_dirs()
    # Try to load existing FAISS index on startup
    from app.services.embedding_service import EmbeddingService
    emb = EmbeddingService()
    emb.load_index_if_exists()
    yield


# ── App ─────────────────────────────────────────────────────
app = FastAPI(
    title="Needhi — AI Legal Assistant",
    description="Multilingual AI-powered legal assistant for Indian citizens (Tamil + English)",
    version="1.0.0",
    lifespan=lifespan,
)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ─────────────────────────────────────────────────
app.include_router(query.router, prefix="/api/query", tags=["RAG Q&A"])
app.include_router(classifier.router, prefix="/api/classify", tags=["Classifier"])
app.include_router(complaint.router, prefix="/api/complaint", tags=["Complaint"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "Needhi — AI Legal Assistant",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
