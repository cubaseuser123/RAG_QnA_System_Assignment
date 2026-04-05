import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY : str = os.getenv("GROQ_API_KEY")
LLM_MODEL : str = "llama-3.3-70b-versatile"
LLM_TEMPERATURE : float = 0.1

VECTOR_STORE : str = "neon"
NEON_DATABASE_URL : str = os.getenv("NEON_DATABASE_URL", "")

EMBEDDING_MODEL : str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
EMBED_DIM : int = 384

TOP_K : int = int(os.getenv("TOP_K", "5"))

PG_TABLE_NAME : str = "rag_embeddings"