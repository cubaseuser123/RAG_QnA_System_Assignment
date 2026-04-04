from llama_index.embeddings.huggingface import HuggingFaceEmbedding 
from config import EMBEDDING_MODEL

_embed_model = None

def get_embed_model() -> HuggingFaceEmbedding:
    global _embed_model
    if _embed_model is None:
        _embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    return _embed_model