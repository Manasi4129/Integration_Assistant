"""Central configuration. All values can be overridden via environment variables
(see .env.example). Keeping config in one place is a habit that pays off later when
you move from a local prototype to real AWS infrastructure."""

import os
from dataclasses import dataclass


@dataclass
class Settings:
    # AWS
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")

    # Bedrock model IDs. These change over time and vary by region, so make them
    # configurable rather than hard-coded. Run `aws bedrock list-foundation-models`
    # to see what is enabled in your account/region, then set these in .env.
    embedding_model_id: str = os.getenv("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")
    generation_model_id: str = os.getenv(
        "GENERATION_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0"
    )

    # Chunking
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "700"))       # target characters per chunk
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100")) # overlap keeps context across splits

    # Retrieval
    top_k: int = int(os.getenv("TOP_K", "4"))                   # how many chunks to feed the model

    # Paths
    docs_dir: str = os.getenv("DOCS_DIR", "data/sample_docs")
    index_path: str = os.getenv("INDEX_PATH", "index/store.npz")


settings = Settings()
