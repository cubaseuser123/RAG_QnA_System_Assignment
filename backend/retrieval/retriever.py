import logging
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.schema import TextNode

from config import TOP_K
logger = logging.getLogger(__name__)

def build_hybrid_retriever(index: VectorStoreIndex, nodes: list[TextNode] | None = None) -> QueryFusionRetriever:
    vector_retriever = index.as_retriever(similarity_top_k=TOP_K)

    # Try to build BM25 retriever
    bm25_nodes = nodes
    if bm25_nodes is None and index.docstore and len(index.docstore.docs) > 0:
        bm25_nodes = list(index.docstore.docs.values())

    if bm25_nodes and len(bm25_nodes) > 0:
        bm25_retriever = BM25Retriever.from_defaults(
            nodes=bm25_nodes,
            similarity_top_k=TOP_K,
        )
        retrievers = [vector_retriever, bm25_retriever]
        logger.info(f"Built hybrid retriever (dense + BM25, top_k={TOP_K}, mode=RRF)")
    else:
        # Fallback: dense-only when docstore is empty (e.g. PGVectorStore)
        retrievers = [vector_retriever]
        logger.warning("BM25 skipped — no nodes in docstore. Using dense retrieval only.")

    hybrid_retriever = QueryFusionRetriever(
        retrievers=retrievers,
        similarity_top_k=TOP_K,
        num_queries=1,
        mode="reciprocal_rerank",
    )

    return hybrid_retriever


