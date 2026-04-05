import logging
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.schema import TextNode

from config import(
    VECTOR_STORE,
    NEON_DATABASE_URL,
    PG_TABLE_NAME,
    EMBED_DIM
)

logger = logging.getLogger(__name__)

def _create_neon_vector_store():
    from llama_index.vector_stores.postgres import PGVectorStore
    from sqlalchemy import make_url

    if not NEON_DATABASE_URL:
        raise ValueError("NEON_DATABASE_URL is not set")
    
    url = make_url(NEON_DATABASE_URL)
    vector_store = PGVectorStore.from_params(
        database = url.database,
        host = url.host,
        password = url.password,
        port = str(url.port or 5432),
        user = url.username,
        table_name = PG_TABLE_NAME,
        embed_dim = EMBED_DIM,
    )

    logger.info(f"Initialized PGVectorStore -> {url.host}/{url.database} (table:{PG_TABLE_NAME})")
    return vector_store

def get_vector_store():
    if VECTOR_STORE == "neon":
        return _create_neon_vector_store()
    else:
        raise ValueError(f"Unknown VECTOR_STORE value: '{VECTOR_STORE}'. Only 'neon' is supported.")

def _sanitize_nodes(nodes: list[TextNode]) -> list[TextNode]:
    """Strip NUL (0x00) bytes that some PDFs produce — PostgreSQL rejects them."""
    for node in nodes:
        if node.text:
            node.text = node.text.replace("\x00", "")
        if node.metadata:
            node.metadata = {
                k: v.replace("\x00", "") if isinstance(v, str) else v
                for k, v in node.metadata.items()
            }
    return nodes

def build_index_from_nodes(nodes : list[TextNode]) -> VectorStoreIndex:
    vector_store = get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store = vector_store)

    nodes = _sanitize_nodes(nodes)

    index = VectorStoreIndex(
        nodes = nodes,
        storage_context = storage_context,
        show_progress = True, 
    )

    logger.info(f"Built VectorStoreIndex from {len(nodes)} nodes")
    return index

def load_existing_index() -> VectorStoreIndex:
    vector_store = get_vector_store()
    index = VectorStoreIndex.from_vector_store(vector_store = vector_store)
    logger.info("Loaded existing VectorStoreIndex")
    return index