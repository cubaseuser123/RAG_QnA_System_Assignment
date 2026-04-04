import logging 
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import get_response_synthesizer

from generation.prompt import QA_PROMPT_TEMPLATE
logger = logging.getLogger(__name__)

def build_query_engine(retriever) -> RetrieverQueryEngine:
    response_synthesizer = get_response_synthesizer(
        response_model = 'compact',
        text_qa_template = QA_PROMPT_TEMPLATE,
    )
    
    query_engine = RetrieverQueryEngine(
        retriever = retriever,
        response_synthesizer = response_synthesizer,
    )

    logger.info("Built RetrieverQueryEngine (compact mode, custom QA prompt)")
    return query_engine

def query(query_engine : RetrieverQueryEngine, question: str) -> dict:
    response = query_engine.query(question)

    sources = []
    for node in response.source_nodes:
        meta = node.node.metadata
        sources.append({
            "file" : meta.get("source_file", meta.get("file_name", "unknown")),
            "page" : str(meta.get("page_label", "N/A")),
            "excerpt" : node.node.get_content()[:200],
        })
    return{
        "answer" : str(response),
        "sources" : sources,
    }