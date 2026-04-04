from networkx.algorithms import similarity
import logging 
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.retrievers.bm25 import BM25Retriever
from llama_index.core.schema import TextNode

from config import TOP_K
logger = logging.getLogger(__name__)

def build_hybrid_retriever(index : VectorStoreIndex,nodes : list[TextNode] | None = None) -> QueryFusionRetriever:
    vector_retriever = index.as_retriever(similarity_top_k = TOP_K)

    if nodes is not None:
        bm25_retriever = BM25Retriever.from_defaults(
            nodes = nodes,
            similarity_top_k = TOP_K,
        )
    else:
        bm25_retriever = BM25Retriever.from_defaults(
            docstore = index.docstore,
            similarity_top_k = TOP_K,
        )
    
    hybrid_retriever = QueryFusionRetriever(
        retrievers = [vector_retriever, bm25_retriever],
        similarity_top_k = TOP_K,
        num_queries = 1,
        mode = "reciprocal_rerank",
    )

    logger.info(f"Built hybrid retriever (dense + BM25, top_k ={TOP_K}, mode=RRF")
    return hybrid_retriever

