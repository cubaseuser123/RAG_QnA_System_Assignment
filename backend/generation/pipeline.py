import logging 
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import get_response_synthesizer

from generation.prompt import QA_PROMPT_TEMPLATE
logger = logging.getLogger(__name__)

def build_query_engine(retriever) -> RetrieverQueryEngine:
    response_synthesizer = get_response_synthesizer(
        response_mode = 'simple_summarize',
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
        content = node.node.get_content()

        # Filter out garbled/binary chunks (less than 60% printable chars)
        if len(content) > 0:
            printable_ratio = sum(1 for c in content if c.isprintable()) / len(content)
            if printable_ratio < 0.60:
                logger.debug(f"Skipping garbled chunk (printable ratio: {printable_ratio:.2f})")
                continue

        # Try multiple page metadata key variants
        page = (
            meta.get("page_label")
            or meta.get("page_number")
            or meta.get("page")
            or "N/A"
        )

        sources.append({
            "file" : meta.get("file_name", meta.get("source_file", "unknown")),
            "page" : str(page),
            "excerpt" : content[:200],
        })
    return{
        "answer" : str(response),
        "sources" : sources,
    }