"""Load source documents and split them into overlapping chunks.

Chunking is one of the most important — and most under-appreciated — parts of RAG.
Chunks that are too big dilute retrieval; too small and you lose context. We split on
paragraph boundaries and then pack paragraphs into windows of roughly `chunk_size`
characters, carrying a small overlap so a sentence split across a boundary is still
retrievable. This is exactly the kind of design decision the AIP-C01 exam probes."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from .config import settings


@dataclass
class Chunk:
    id: str        # e.g. "error-codes.md#3"
    text: str
    source: str    # the file the chunk came from (used for citations)


def load_documents(docs_dir: str = None) -> List[Tuple[str, str]]:
    """Return a list of (filename, full_text) for every .md/.txt file in docs_dir."""
    docs_dir = docs_dir or settings.docs_dir
    docs: List[Tuple[str, str]] = []
    for path in sorted(Path(docs_dir).glob("**/*")):
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
            docs.append((path.name, path.read_text(encoding="utf-8")))
    if not docs:
        raise FileNotFoundError(f"No .md or .txt documents found in {docs_dir!r}")
    return docs


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Pack paragraphs into ~chunk_size windows with a trailing character overlap."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    current = ""
    for para in paragraphs:
        if current and len(current) + len(para) + 2 > chunk_size:
            chunks.append(current.strip())
            # start the next chunk with the tail of the previous one for continuity
            current = current[-overlap:] + "\n\n" + para if overlap else para
        else:
            current = f"{current}\n\n{para}" if current else para
    if current.strip():
        chunks.append(current.strip())
    return chunks


def build_chunks(docs_dir: str = None) -> List[Chunk]:
    """Load every document and return a flat list of Chunk objects with metadata."""
    chunks: List[Chunk] = []
    for filename, text in load_documents(docs_dir):
        for i, piece in enumerate(chunk_text(text, settings.chunk_size, settings.chunk_overlap)):
            chunks.append(Chunk(id=f"{filename}#{i}", text=piece, source=filename))
    return chunks
