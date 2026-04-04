from llama_index.llms.groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE

def get_llm() -> Groq:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in .env")
    
    return Groq(
        model = LLM_MODEL,
        api_key = GROQ_API_KEY,
        temperature = LLM_TEMPERATURE,
    )