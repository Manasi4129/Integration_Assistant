"""A minimal local vector store backed by NumPy.

This stands in for a managed vector database (Amazon OpenSearch Serverless, Aurora
pgvector, etc.) so you can understand retrieval end-to-end before paying for infra.
Phase 2 of the roadmap swaps this class out for a real AWS vector store — the rest of
the code barely changes, which is the whole point of keeping retrieval behind an
interface."""

from typing import List, Tuple

import numpy as np

from .ingest import Chunk


class VectorStore:
    def __init__(self):
        self.vectors: np.ndarray | None = None   # shape (n_chunks, dim)
        self.chunks: List[Chunk] = []

    def add(self, embeddings: List[List[float]], chunks: List[Chunk]) -> None:
        mat = np.array(embeddings, dtype=np.float32)
        # normalise so a dot product == cosine similarity
        mat /= np.linalg.norm(mat, axis=1, keepdims=True) + 1e-10
        self.vectors = mat if self.vectors is None else np.vstack([self.vectors, mat])
        self.chunks.extend(chunks)

    def search(self, query_vec: List[float], top_k: int) -> List[Tuple[Chunk, float]]:
        if self.vectors is None:
            return []
        q = np.array(query_vec, dtype=np.float32)
        q /= np.linalg.norm(q) + 1e-10
        scores = self.vectors @ q                      # cosine similarity to every chunk
        top = np.argsort(scores)[::-1][:top_k]         # indices of the best matches
        return [(self.chunks[i], float(scores[i])) for i in top]

    def save(self, path: str) -> None:
        import os
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        np.savez(
            path,
            vectors=self.vectors,
            ids=np.array([c.id for c in self.chunks]),
            texts=np.array([c.text for c in self.chunks], dtype=object),
            sources=np.array([c.source for c in self.chunks]),
        )

    @classmethod
    def load(cls, path: str) -> "VectorStore":
        data = np.load(path, allow_pickle=True)
        store = cls()
        store.vectors = data["vectors"]
        store.chunks = [
            Chunk(id=i, text=t, source=s)
            for i, t, s in zip(data["ids"], data["texts"], data["sources"])
        ]
        return store
