RAG Question Answering System

> A production-grade Retrieval-Augmented Generation pipeline that answers questions grounded strictly in your documents with source citations.

---

## ⚡ Key Technical Highlights

- **Hybrid Retrieval Strategy:** Combines Dense Vector Similarity (semantic meaning) with BM25 Keyword Search (exact terms) using Reciprocal Rank Fusion (RRF) for highly accurate context retrieval.
- **Production-ready Vector Storage:** Uses **Neon (Serverless PostgreSQL + pgvector)** for robust, persistent cloud storage.
- **Open-Source LLM Integration:** Powered by the fully open-source **Llama 3.3-70B**. Inference is delegated to the **Groq API** to provide accessible, instant performance without requiring heavy local GPU resources.
- **Smart Semantic Chunking:** Splits documents based on shifts in topic and semantics, not arbitrary character counts, preserving contextual meaning.

---

## What This Does

This system lets you ingest a set of PDF or text documents and ask natural language questions about them. Every answer is generated strictly from the retrieved document context, with citations showing exactly which file and page the answer came from.

Under the hood: documents are semantically chunked, embedded using a local model, and stored in a PostgreSQL vector database. At query time, a hybrid retriever combining dense vector search and BM25 keyword search finds the most relevant passages, which are injected into a grounded prompt and sent to Llama 3.3-70B via Groq for generation.

---

## System Demo & Capabilities

Here is a visual walk-through of the end-to-end functionality using the Next.js frontend and FastAPI backend.

### 1. Document Preparation
Documents intended for the knowledge base are placed into the `backend/docs/` directory. For this demo, we use the original "Attention Is All You Need" paper and a sample text file.

![Documents placed in directory](./demo_ss/two_document_existance.png)
<br>
![Terminal loading of documents](./demo_ss/two_document_loading.png)

### 2. Ingestion Pipeline
The documents are processed via the `/ingest` endpoint. They are semantically chunked, embedded using `BAAI/bge-small-en-v1.5`, and safely stored in the Neon PostgreSQL database.

![Ingestion Endpoint Success](./demo_ss/document_ingestion_success.png)

### 3. Grounded Q&A with Citations
Questions asked through the UI are answered strictly based on the retrieved vector context. The exact source chunks, including file names and page numbers (from PDFs), are provided below the answer.

![QnA Success Response](./demo_ss/qna_success.png)
<br>
![QnA Extracted Sources View](./demo_ss/qna_success_sources.png)

### 4. Graceful Out-of-Scope Fallback
The prompt rigidly enforces grounding. If a question is asked that cannot be answered using the retrieved chunks, the system safely refuses rather than hallucinating an answer.

![Graceful Failure on Out of Scope Question](./demo_ss/qna_failure.png)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        INGESTION PIPELINE                       │
│                                                                 │
│   PDF / TXT Files                                               │
│        │                                                        │
│        ▼                                                        │
│   SimpleDirectoryReader          (ingestion/loader.py)          │
│        │  Loads files, populates file_name + page_label         │
│        ▼                                                        │
│   SemanticSplitterNodeParser     (ingestion/chunker.py)         │
│        │  Splits on topic shifts, not character count           │
│        ▼                                                        │
│   HuggingFaceEmbedding           (ingestion/embedder.py)        │
│        │  BAAI/bge-small-en-v1.5  →  384-dim vectors            │
│        ▼                                                        │
│   PGVectorStore                  (retrieval/vectorstore.py)     │
│        │  Neon (pgvector)                                       │
│        ▼                                                        │
│   Stored ✓                                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         QUERY PIPELINE                          │
│                                                                 │
│   User Question                                                 │
│        │                                                        │
│        ▼                                                        │
│   VectorIndexRetriever           ──┐                            │
│   (dense similarity search)        │  (retrieval/retriever.py)  │
│                                    ├─► QueryFusionRetriever     │
│   BM25Retriever                  ──┘    (RRF merge)             │
│   (keyword search, in-memory)          │                        │
│                                        ▼                        │
│                               Top-K fused chunks                │
│                                        │                        │
│                                        ▼                        │
│   Custom QA PromptTemplate       (generation/prompt.py)         │
│        │  Injects context + enforces grounding                  │
│        ▼                                                        │
│   RetrieverQueryEngine           (generation/pipeline.py)       │
│        │  compact response mode                                 │
│        ▼                                                        │
│   Groq API — Llama 3.3-70B       (generation/llm.py)            │
│        │                                                        │
│        ▼                                                        │
│   Answer + Source Citations      (api/routes.py → FastAPI)      │
│        │                                                        │
│        ▼                                                        │
│   Next.js Frontend               (frontend/)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Choice | Reason |
|---|---|---|
| Language | Python 3.11+ | Assignment requirement |
| RAG Orchestration | LlamaIndex | First-class pgvector support, modular retriever/engine design |
| Embeddings | `BAAI/bge-small-en-v1.5` | Outperforms MiniLM on retrieval benchmarks, 384-dim, lightweight |
| Chunking | `SemanticSplitterNodeParser` | Preserves topical coherence over naive character splitting |
| Vector DB | Neon (PostgreSQL + pgvector) | Production-grade, persistent, cloud-native |
| Retrieval | Hybrid: Dense + BM25 via RRF | Dense handles semantics, BM25 handles exact terms, RRF fuses both |
| LLM | Llama 3.3-70B via Groq | Open-source model, near-zero latency, free tier |
| API | FastAPI | Async, typed, assignment suggestion |
| Frontend | Next.js 16 + shadcn/ui | Clean chat UI, collapsible source citations |

---

## Project Structure

```
helpora-rag/
├── backend/
│   ├── config.py                  # All env vars — single source of truth
│   ├── ingestion/
│   │   ├── embedder.py            # BGE embedding model (singleton)
│   │   ├── loader.py              # PDF/TXT loader via SimpleDirectoryReader
│   │   └── chunker.py             # Semantic chunking with metadata enrichment
│   ├── retrieval/
│   │   ├── vectorstore.py         # Neon pgvector integration
│   │   └── retriever.py           # Hybrid retriever (dense + BM25 + RRF)
│   ├── generation/
│   │   ├── llm.py                 # Groq LLM wrapper
│   │   ├── prompt.py              # Grounded QA prompt template
│   │   └── pipeline.py            # RetrieverQueryEngine + source extraction
│   ├── api/
│   │   ├── main.py                # FastAPI app, lifespan, CORS
│   │   ├── routes.py              # /health, /ingest, /ask endpoints
│   │   └── schemas.py             # Pydantic request/response models
│   ├── ingest_docs.py             # CLI ingestion script
│   ├── docs/                      # Place your PDFs here
│   └── requirements.txt
└── frontend/
    └── src/
        ├── app/                   # Next.js App Router
        ├── components/            # ChatWindow, MessageBubble, InputBar
        ├── lib/api.ts             # Typed fetch wrapper for FastAPI
        └── types/index.ts         # Shared TypeScript interfaces
```

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+ and pnpm
- A [Neon](https://neon.tech) account (free tier is sufficient)
- A [Groq](https://console.groq.com) API key (free tier)

---

### Step 1 — Clone and scaffold

```bash
git clone <your-repo-url>
cd helpora-rag
```

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate        # macOS/Linux
# .\venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

```bash
# Frontend (from project root)
cd frontend
pnpm install
```

---

### Step 2 — Enable pgvector on Neon

In your Neon dashboard, open the SQL Editor and run once:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

LlamaIndex handles table creation automatically after this. You never write `CREATE TABLE` yourself.

---

### Step 3 — Configure environment variables

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:

```env
GROQ_API_KEY=gsk_your_key_here
NEON_DATABASE_URL=postgresql://user:password@ep-xxxx.us-east-2.aws.neon.tech/dbname?sslmode=require
VECTOR_STORE=neon
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
TOP_K=5
```

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

### Step 4 — Add documents

Place your PDF or TXT files in `backend/docs/`. The knowledge base used in this project:

- `attention_is_all_you_need.pdf` — The original "Attention Is All You Need" paper by Vaswani et al., 2017
- `sample_paper.txt` — A sample test document discussing RAG and LLM patterns

These files are used to demonstrate the system's ability to extract, strictly index, and accurately retrieve from both complex PDFs and plain text files.

---

### Step 5 — Ingest documents

```bash
cd backend
python ingest_docs.py --path ./docs
```

Expected output:

```
2025-01-01 12:00:00 | INFO    | 📂 Loading documents from: ./docs
2025-01-01 12:00:01 | INFO    |    → Loaded 3 document(s)
2025-01-01 12:00:01 | INFO    | ✂️  Chunking documents semantically...
2025-01-01 12:00:45 | INFO    |    → Created 142 chunk(s)
2025-01-01 12:00:45 | INFO    | 📦 Embedding and storing chunks...
2025-01-01 12:01:10 | INFO    |    → Stored 142 chunk(s) in vector store
2025-01-01 12:01:10 | INFO    | ✅ Ingestion complete!
```

---

### Step 6 — Start the backend

```bash
cd backend
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Verify it's running:

```bash
curl http://localhost:8000/health
# {"status":"healthy","vector_store":"neon","llm":"llama-3.3-70b-versatile"}
```

---

### Step 7 — Start the frontend

```bash
cd frontend
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000).

---



## API Reference

### `GET /health`

Returns API status and backend configuration.

```json
{
  "status": "healthy",
  "vector_store": "neon",
  "llm": "llama-3.3-70b-versatile"
}
```

### `POST /ingest`

Ingest documents from a directory.

```json
// Request
{ "path": "./docs" }

// Response
{
  "message": "Successfully ingested 3 document(s)",
  "chunks_ingested": 142
}
```

### `POST /ask`

Ask a question. Returns answer + source citations.

```json
// Request
{ "question": "What is retrieval-augmented generation?" }

// Response
{
  "answer": "Retrieval-Augmented Generation (RAG) is... [Source: rag_paper.pdf, Page 1]",
  "sources": [
    {
      "file": "rag_paper.pdf",
      "page": "1",
      "excerpt": "Retrieval-Augmented Generation combines..."
    }
  ]
}
```

---

## Design Decisions

### Database: Neon + pgvector
I opted for **Neon with pgvector** for vector storage rather than a local file-based database. It's cloud-native, always available, and removes local setup friction, ensuring the database state persists predictably across demo runs for anyone reviewing the application.

### Embeddings: BAAI/bge-small-en-v1.5
Instead of the typical MiniLM model, I chose the **BGE-small** model. It consistently outperforms MiniLM on the BEIR retrieval benchmark suite while remaining equally lightweight (384 dimensions). This results in tangibly higher-quality context retrieval without any added latency or memory cost.

### Chunking Strategy: Semantic Boundary Parsing
Instead of using naive recursive character splitting—which can arbitrarily slice sentences in half or separate definitions from their examples—I implemented a **Semantic Splitter**. It calculates embedding similarity between adjacent sentences and makes cuts only when the topic actually shifts. This preserves the coherence of the text chunks and drastically improves the retriever's accuracy.

### Retrieval Strategy: Hybrid (Dense + BM25)
Standard dense vector search struggles with exact-term matching (like specific acronyms, proper nouns, or version numbers). To solve this, I built a **Hybrid Retriever** that couples semantic dense search with an exact-keyword BM25 index. The results from both lists are combined using Reciprocal Rank Fusion (RRF), ensuring robust retrieval for both broad conceptual questions and highly specific keyword queries.

### Inference: Open-Source via Groq API
The assignment encouraged using an open-source model. I utilized the strictly open-source **Llama 3.3-70B**, but actively opted to delegate the heavy inference workload to the **Groq API**. Running a 70-billion parameter model locally demands immense GPU VRAM, which often causes hard crashes on consumer hardware. Proxying open-source models through Groq honors the assignment's constraints while ensuring the app performs instantly and safely on your machine.

### Orchestration: LlamaIndex
I preferred using **LlamaIndex** over LangChain for the pipeline construction. LlamaIndex is purpose-built explicitly for RAG, and its native abstractions like `QueryFusionRetriever` and `SemanticSplitterNodeParser` are far cleaner and more powerful for this architecture out of the box.

---

## Trade-offs & Future Enhancements

- **No streaming** — The `/ask` endpoint returns a complete response. A streaming implementation via `StreamingResponse` and Groq's streaming API would improve perceived latency for long answers.
- **Index rebuilt per request** — `load_existing_index()` is called on every `/ask` request. In production this would be cached at startup and refreshed only after `/ingest`.
- **BM25 runs in-memory** — BM25 retrieval loads all nodes into memory. For very large corpora this would need to move to a dedicated sparse index (e.g. Elasticsearch BM25).
- **No re-ranking** — A cross-encoder re-ranker (e.g. `BAAI/bge-reranker-base`) applied after hybrid retrieval would further improve precision on the final top-k.
- **Single-turn only** — The system has no conversation memory. Follow-up questions referencing previous answers are treated as independent queries.
