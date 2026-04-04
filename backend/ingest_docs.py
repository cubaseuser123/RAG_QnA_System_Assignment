"""
ingest_docs.py — CLI script for document ingestion.

Usage:
    python ingest_docs.py --path ./docs
"""

import argparse
import logging
import sys
import os

# Ensure the backend directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llama_index.core import Settings
from ingestion.embedder import get_embed_model
from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from retrieval.vectorstore import build_index_from_nodes
from generation.llm import get_llm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Ingest PDF/TXT documents into the RAG vector store."
    )
    parser.add_argument(
        "--path",
        type=str,
        default="./docs",
        help="Directory path containing PDF/TXT documents (default: ./docs)",
    )
    args = parser.parse_args()

    # ── Initialize LlamaIndex Settings ────────────────────────────────────
    logger.info("Initializing embedding model...")
    Settings.embed_model = get_embed_model()

    logger.info("Initializing LLM...")
    Settings.llm = get_llm()

    # ── Step 1: Load ──────────────────────────────────────────────────────
    logger.info(f"📂 Loading documents from: {args.path}")
    documents = load_documents(args.path)
    logger.info(f"   → Loaded {len(documents)} document(s)")

    # ── Step 2: Chunk ─────────────────────────────────────────────────────
    logger.info("✂️  Chunking documents semantically...")
    nodes = chunk_documents(documents)
    logger.info(f"   → Created {len(nodes)} chunk(s)")

    # ── Step 3: Embed + Store ─────────────────────────────────────────────
    logger.info("📦 Embedding and storing chunks...")
    build_index_from_nodes(nodes)
    logger.info(f"   → Stored {len(nodes)} chunk(s) in vector store")

    # ── Done ──────────────────────────────────────────────────────────────
    logger.info("✅ Ingestion complete!")
    logger.info(f"   Files:  {len(documents)}")
    logger.info(f"   Chunks: {len(nodes)}")


if __name__ == "__main__":
    main()
