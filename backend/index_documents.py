"""
NyayaSahaya — Standalone document indexing script.
Uses LOCAL sentence-transformers model — no API quota needed.
Run once, takes ~1.5 min on CPU.

Usage: python index_documents.py
"""

import sys
import time
import pickle
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))
import os
os.chdir(SCRIPT_DIR)

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

from app.utils.text_processor import chunk_text, read_document
from app.config import get_settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def main():
    load_dotenv()
    settings = get_settings()

    # ── Load local model ─────────────────────────────────────
    model_name = settings.local_embedding_model
    logger.info(f"Loading local embedding model: {model_name}")
    logger.info(f"(First run downloads ~90MB, subsequent runs are instant)")
    model = SentenceTransformer(model_name)
    dimension = model.get_sentence_embedding_dimension()
    logger.info(f"Model loaded. Embedding dimension: {dimension}\n")

    # ── Read and chunk all documents ─────────────────────────
    docs_dir = Path(settings.sample_docs_dir)
    files = sorted(list(docs_dir.glob("*.txt")) + list(docs_dir.glob("*.pdf")))
    logger.info(f"Found {len(files)} documents in {docs_dir}")

    all_chunks = []
    for f in files:
        text = read_document(f)
        chunks = chunk_text(text, source=f.name)
        all_chunks.extend(chunks)
        logger.info(f"  📄 {f.name}: {len(chunks)} chunks")

    if not all_chunks:
        logger.error("No chunks found! Check sample_docs directory.")
        sys.exit(1)

    logger.info(f"\nTotal chunks: {len(all_chunks)}")

    # ── Embed all chunks locally ──────────────────────────────
    logger.info(f"Embedding {len(all_chunks)} chunks on CPU (no API quota)...")
    start = time.time()
    texts = [c["text"] for c in all_chunks]
    vectors = model.encode(texts, batch_size=64, show_progress_bar=True, convert_to_numpy=True)
    vectors = vectors.astype("float32")
    elapsed = time.time() - start
    logger.info(f"Embedding done in {elapsed:.1f}s")

    # ── Build FAISS index ─────────────────────────────────────
    logger.info(f"Building FAISS index...")
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    # ── Save to disk ─────────────────────────────────────────
    store_dir = Path(settings.vector_store_dir)
    store_dir.mkdir(parents=True, exist_ok=True)
    index_path = store_dir / "index.faiss"
    meta_path = store_dir / "metadata.pkl"

    faiss.write_index(index, str(index_path))
    with open(meta_path, "wb") as f:
        pickle.dump(all_chunks, f)

    logger.info(f"\n{'='*50}")
    logger.info(f"✅ DONE!")
    logger.info(f"   Documents : {len(files)}")
    logger.info(f"   Chunks    : {len(all_chunks)}")
    logger.info(f"   Vectors   : {index.ntotal}")
    logger.info(f"   Dimension : {dimension}")
    logger.info(f"   Time      : {elapsed:.1f}s")
    logger.info(f"   Saved to  : {index_path}")
    logger.info(f"{'='*50}")
    logger.info(f"\nStart the server and ask questions!")


if __name__ == "__main__":
    main()

