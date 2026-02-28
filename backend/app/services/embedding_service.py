"""
NyayaSahaya — Embedding + FAISS vector store service (local sentence-transformers).
Embeddings run 100% locally on CPU — no API quota used.
Gemini is only used for LLM answer generation.
"""

import logging
import pickle
from pathlib import Path
from typing import Optional

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import get_settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Manages text embeddings via Gemini and the FAISS vector index."""

    _instance: Optional["EmbeddingService"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        settings = get_settings()
        model_name = settings.local_embedding_model
        logger.info(f"Loading local embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Embedding dimension: {self.dimension}")
        self.index: Optional[faiss.IndexFlatL2] = None
        self.metadata: list[dict] = []  # parallel list of chunk metadata
        self.index_path = Path(settings.vector_store_dir) / "index.faiss"
        self.meta_path = Path(settings.vector_store_dir) / "metadata.pkl"
        self._initialized = True

    # ── Embedding ────────────────────────────────────────────
    def embed_texts(self, texts: list[str]) -> np.ndarray:
        """Generate embeddings locally using SentenceTransformer (no API, no quota)."""
        vectors = self.model.encode(texts, batch_size=64, show_progress_bar=False, convert_to_numpy=True)
        return vectors.astype("float32")

    def embed_query(self, text: str) -> np.ndarray:
        """Generate embedding for a single query locally."""
        vector = self.model.encode([text], convert_to_numpy=True)
        return vector[0].astype("float32")

    # ── Index management ─────────────────────────────────────
    def create_index(self):
        """Create a fresh FAISS index."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []

    def add_chunks(self, chunks: list[dict]):
        """
        Add document chunks to the index.
        Each chunk: {"text": str, "source": str, "index": int}
        """
        if self.index is None:
            self.create_index()

        texts = [c["text"] for c in chunks]
        vectors = self.embed_texts(texts)
        self.index.add(vectors)
        self.metadata.extend(chunks)
        logger.info(f"Added {len(chunks)} chunks to FAISS index (total: {self.index.ntotal})")

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Search the FAISS index and return top-k matching chunks."""
        if self.index is None or self.index.ntotal == 0:
            return []

        query_vec = self.embed_query(query).reshape(1, -1)
        distances, indices = self.index.search(query_vec, min(top_k, self.index.ntotal))

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata) and idx >= 0:
                chunk = self.metadata[idx].copy()
                chunk["score"] = float(dist)
                results.append(chunk)
        return results

    # ── Persistence ──────────────────────────────────────────
    def save_index(self):
        """Save the FAISS index and metadata to disk."""
        if self.index is None:
            return
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
        logger.info(f"Saved FAISS index ({self.index.ntotal} vectors) to {self.index_path}")

    def load_index_if_exists(self):
        """Load a previously saved index from disk."""
        if self.index_path.exists() and self.meta_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)
            logger.info(f"Loaded FAISS index ({self.index.ntotal} vectors) from {self.index_path}")
        else:
            logger.info("No existing FAISS index found; starting fresh.")

    @property
    def total_vectors(self) -> int:
        return self.index.ntotal if self.index else 0
