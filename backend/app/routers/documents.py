"""
NyayaSahaya — Document upload and indexing endpoints.
"""

import os
import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.schemas import DocumentIndexResponse, DocumentUploadResponse
from app.services.embedding_service import EmbeddingService
from app.utils.text_processor import chunk_text, read_document
from app.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a legal document (.txt or .pdf), chunk it, embed it, and add to FAISS index.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    allowed_ext = {".txt", ".pdf"}
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}. Allowed: {allowed_ext}")

    try:
        settings = get_settings()
        # Save uploaded file
        save_path = Path(settings.sample_docs_dir) / file.filename
        content = await file.read()
        with open(save_path, "wb") as f:
            f.write(content)

        # Read and chunk
        text = read_document(save_path)
        chunks = chunk_text(text, source=file.filename)

        # Embed and index
        emb_service = EmbeddingService()
        emb_service.add_chunks(chunks)
        emb_service.save_index()

        return DocumentUploadResponse(
            message=f"Successfully indexed {file.filename}",
            filename=file.filename,
            chunks_created=len(chunks),
        )
    except Exception as e:
        logger.error(f"Document upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.post("/index-all", response_model=DocumentIndexResponse)
async def index_all_documents():
    """
    Read all documents in the sample_docs directory, chunk, embed, and build the FAISS index.
    """
    try:
        settings = get_settings()
        docs_dir = Path(settings.sample_docs_dir)

        if not docs_dir.exists():
            raise HTTPException(status_code=404, detail="Sample docs directory not found.")

        files = list(docs_dir.glob("*.txt")) + list(docs_dir.glob("*.pdf"))
        if not files:
            raise HTTPException(status_code=404, detail="No .txt or .pdf files found in sample_docs directory.")

        emb_service = EmbeddingService()
        emb_service.create_index()  # Reset index

        total_chunks = 0
        for i, file_path in enumerate(files):
            text = read_document(file_path)
            chunks = chunk_text(text, source=file_path.name)
            emb_service.add_chunks(chunks)
            total_chunks += len(chunks)
            logger.info(f"[{i+1}/{len(files)}] Indexed {file_path.name}: {len(chunks)} chunks")

        emb_service.save_index()

        return DocumentIndexResponse(
            message="Successfully indexed all documents",
            documents_processed=len(files),
            total_chunks=total_chunks,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Indexing error: {e}")
        raise HTTPException(status_code=500, detail=f"Error indexing documents: {str(e)}")


@router.get("/status")
async def index_status():
    """Check the current status of the FAISS index."""
    emb_service = EmbeddingService()
    settings = get_settings()
    docs_dir = Path(settings.sample_docs_dir)

    doc_files = []
    if docs_dir.exists():
        doc_files = [f.name for f in docs_dir.iterdir() if f.suffix.lower() in {".txt", ".pdf"}]

    return {
        "total_vectors": emb_service.total_vectors,
        "total_metadata": len(emb_service.metadata),
        "index_loaded": emb_service.index is not None,
        "documents_on_disk": doc_files,
    }
