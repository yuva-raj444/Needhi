"""
NyayaSahaya — Text processing utilities for chunking legal documents.
"""

from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import get_settings


def chunk_text(text: str, source: str = "unknown") -> list[dict]:
    """Split a large text into overlapping chunks with metadata."""
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", "SECTION", "Section", ". ", " ", ""],
        length_function=len,
    )
    chunks = splitter.split_text(text)
    return [
        {"text": chunk.strip(), "source": source, "index": i}
        for i, chunk in enumerate(chunks)
        if chunk.strip()
    ]


def read_text_file(file_path: str | Path) -> str:
    """Read a plain text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf_file(file_path: str | Path) -> str:
    """Extract text from a PDF file."""
    from PyPDF2 import PdfReader
    reader = PdfReader(str(file_path))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n\n".join(pages)


def read_document(file_path: str | Path) -> str:
    """Read a document (txt or pdf) and return its text."""
    path = Path(file_path)
    if path.suffix.lower() == ".pdf":
        return read_pdf_file(path)
    else:
        return read_text_file(path)
