import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY : str = os.getenv("GROQ_API_KEY")
LLM_MODEL : str = "llama-3.3-70b-versatile"
LLM_TEMPERATURE : float = 0.1

VECTOR_STORE : str = os.getenv("VECTOR_STORE", "neon").lower()
NEON_DATABASE_URL : str = os.getenv("NEON_DATABASE_URL", "")
CHROMA_PERSIST_PATH : str = os.getenv("CHROMA_PERSIST_PATH", "./chroma_db")

EMBEDDING_MODEL : str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
EMBED_DIM : int = 384

TOP_K : int = int(os.getenv("TOK_K", "5"))

PG_TABLE_NAME : str = "rag_embeddings"
CHROMA_COLLECTION_NAME : str = "rag_embeddings"