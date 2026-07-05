"""Build the vector index: load docs -> chunk -> embed -> save.

Run this once (and again whenever your documents change):

    python build_index.py
"""

from dotenv import load_dotenv

load_dotenv()  # read .env before importing config-dependent modules

from src.config import settings
from src.embeddings import embed_batch
from src.ingest import build_chunks
from src.vector_store import VectorStore


def main():
    print(f"Loading documents from {settings.docs_dir} ...")
    chunks = build_chunks()
    print(f"  -> {len(chunks)} chunks")

    print(f"Embedding with {settings.embedding_model_id} (this calls Bedrock) ...")
    embeddings = embed_batch([c.text for c in chunks])

    store = VectorStore()
    store.add(embeddings, chunks)
    store.save(settings.index_path)
    print(f"Saved index to {settings.index_path}. You can now run: python ask.py")


if __name__ == "__main__":
    main()
