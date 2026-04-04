import logging 
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import TextNode, Document
from ingestion.embedder import get_embed_model

logger = logging.getLogger(__name__)

def chunk_documents(documents: list[Document]) -> list[TextNode]:
    embed_model = get_embed_model()
    splitter = SemanticSplitterNodeParser(
        buffer_size = 1,
        breakpoint_percentile_threshold = 95,
        embed_model = embed_model,
    )

    nodes = splitter.get_nodes_from_documents(documents, show_progress = True)

    for idx , node in enumerate(nodes):
        node.metadata["chunk_index"] = idx
        if "file_name" in node.metadata:
            node.metadata["source_file"] = node.metadata["file_name"]
    
    logger.info(f"Split {len(documents)} documents into {len(nodes)} chunks")
    return nodes