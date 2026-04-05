import logging 
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from llama_index.core import Settings
from ingestion.embedder import get_embed_model
from generation.llm import get_llm
from api.routes import router

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app : FastAPI):
    logger.info("Starting up...")
    
    Settings.embed_model = get_embed_model()
    logger.info(f"Embed model loaded: {Settings.embed_model.model_name}")

    Settings.llm = get_llm()
    logger.info(f"LLM loaded: {Settings.llm.model}")

    logger.info("Startup complete. ✅")
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title = "RAG Assignment API",
    description = "RAG-based QnA over documents",
    version = "1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(router)