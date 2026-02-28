"""
NyayaSahaya — Configuration module.
Loads settings from environment variables / .env file.
"""

from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── Gemini (LLM only — embeddings are local) ────────────
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    # ── Local Embeddings ─────────────────────────────────────
    local_embedding_model: str = "all-MiniLM-L6-v2"

    # ── FAISS ────────────────────────────────────────────────
    faiss_index_path: str = "app/data/vector_store/index.faiss"

    # ── Chunking ─────────────────────────────────────────────
    chunk_size: int = 500
    chunk_overlap: int = 50

    # ── Retrieval ────────────────────────────────────────────
    top_k_results: int = 5

    # ── CORS ─────────────────────────────────────────────────
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # ── Paths ────────────────────────────────────────────────
    data_dir: str = "app/data"
    sample_docs_dir: str = "app/data/sample_docs"
    vector_store_dir: str = "app/data/vector_store"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
