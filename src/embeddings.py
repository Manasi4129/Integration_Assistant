"""Turn text into vectors using Amazon Bedrock (Titan Text Embeddings v2).

An embedding is a list of floats that captures the *meaning* of a piece of text.
Similar meanings produce vectors that point in similar directions, which is what lets
us retrieve relevant chunks by comparing a question's vector to each chunk's vector."""

import json
from functools import lru_cache
from typing import List

import boto3

from .config import settings


@lru_cache(maxsize=1)
def _client():
    """One reusable Bedrock runtime client (created lazily so imports stay cheap)."""
    return boto3.client("bedrock-runtime", region_name=settings.aws_region)


def embed_text(text: str) -> List[float]:
    """Embed a single string and return its vector."""
    body = json.dumps({"inputText": text})
    response = _client().invoke_model(modelId=settings.embedding_model_id, body=body)
    payload = json.loads(response["body"].read())
    return payload["embedding"]


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Embed many strings. Titan embeds one input at a time, so we loop.
    (When you migrate to Bedrock Knowledge Bases in Phase 2, AWS handles batching
    and storage for you — this manual version is here to make the mechanics visible.)"""
    return [embed_text(t) for t in texts]
