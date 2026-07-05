"""The RAG loop: embed the question, retrieve the most relevant chunks, then ask the
model to answer *using only those chunks*, with citations.

The system prompt is doing real work here. Forcing the model to answer only from
retrieved context — and to say "I don't know" otherwise — is the core technique for
reducing hallucination in a production assistant. That grounding + citation discipline
is precisely what makes this defensible in an interview and relevant to AIP-C01."""

from typing import List, Tuple

import boto3

from .config import settings
from .embeddings import embed_text
from .ingest import Chunk
from .vector_store import VectorStore

SYSTEM_PROMPT = (
    "You are a marketplace catalog integration assistant. Answer the user's question "
    "using ONLY the provided context passages. Cite the source of each fact in square "
    "brackets, e.g. [error-codes.md]. If the answer is not contained in the context, "
    "say you don't have that information rather than guessing."
)


def _bedrock():
    return boto3.client("bedrock-runtime", region_name=settings.aws_region)


def _format_context(hits: List[Tuple[Chunk, float]]) -> str:
    return "\n\n".join(f"[{chunk.source}]\n{chunk.text}" for chunk, _ in hits)


def answer(question: str, store: VectorStore) -> dict:
    """Return the model's grounded answer plus the sources it was given."""
    query_vec = embed_text(question)
    hits = store.search(query_vec, settings.top_k)

    if not hits:
        return {"answer": "The knowledge base is empty. Build the index first.", "sources": []}

    context = _format_context(hits)
    user_message = (
        f"Context passages:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the context above and cite your sources."
    )

    response = _bedrock().converse(
        modelId=settings.generation_model_id,
        system=[{"text": SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": [{"text": user_message}]}],
        inferenceConfig={"maxTokens": 800, "temperature": 0.2},
    )

    text = response["output"]["message"]["content"][0]["text"]
    sources = sorted({chunk.source for chunk, _ in hits})
    return {"answer": text, "sources": sources, "retrieved": hits}
