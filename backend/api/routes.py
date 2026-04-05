from fastapi import APIRouter, HTTPException
import logging
from api.schemas import(
    QuestionRequest,
    AnswerResponse,
    InjestRequest,
    InjestResponse,
    HealthResponse,
    SourceNode
)
from config import VECTOR_STORE, LLM_MODEL
from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from retrieval.vectorstore import build_index_from_nodes, load_existing_index
from retrieval.retriever import build_hybrid_retriever
from generation.pipeline import build_query_engine, query

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status = "healthy",
        vector_store = VECTOR_STORE,
        llm = LLM_MODEL,
    )

@router.post("/ingest", response_model=InjestResponse)
async def ingest_documents(request : InjestRequest):
    try:
        documents = load_documents(request.path)
        nodes = chunk_documents(documents)
        build_index_from_nodes(nodes)
        return InjestResponse(
            message=f"Successfully injested {len(documents)} document(s)",
            chunks_injested=len(nodes),
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code = 404, detail=str(e))
    except Exception as e:
        logger.error(f"Injestion failed")
        raise HTTPException(status_code = 500, detail=f"Injestion error:{str(e)}")
    except ValueError as e:
        raise HTTPException(status_code = 400, detail=str(e))
    
@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    try:
        index = load_existing_index()
        retriever = build_hybrid_retriever(index)
        query_engine = build_query_engine(retriever)
        result = query(query_engine, request.question)
        return AnswerResponse(
            answer = result["answer"],
            sources = [SourceNode(**s) for s in result["sources"]],
        )
    except Exception as e:
        logger.exception("Query failed")
        if "empty" in str(e).lower() or "no nodes" in str(e).lower():
            return AnswerResponse(
                answer = "We don't have enough information in the knowlesge base to answer this question with facts.",
                sources = [],
            )
        raise HTTPException(status_code = 500, detail=f"Query error: {str(e)}")