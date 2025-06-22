# NeuroCache

**Augmented RAG Ingest & Retrieval System**

NeuroCache is a real-time RAG API that lets you ingest documents or web pages, automatically chunk and enrich them with metadata and AI-generated tags, store vector embeddings, and query them via FastAPI endpoints.

## Features

- **Ingest any file or URL**: PDF, TXT, DOCX, or webpage.
- **Augmented Chunking**: semantic chunks with source info, position, and auto-tags.
- **Vector storage**: FAISS-backed, per-user isolation.
- **Precision Query**: similarity search with metadata filters.

## Getting Started

1. Clone the repo and create a venv:
    ```bash
    git clone https://github.com/CodeBlackwell/NeuroCache.git
    cd NeuroCache
    python -m venv .venv
    source .venv/bin/activate
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Copy `.env.example` to `.env` and set your `OPENAI_API_KEY`:
    ```bash
    cp .env.example .env
    ```
4. Run the server:
    ```bash
    uvicorn neurocache.main:app --reload
    ```

## API Endpoints

- `POST /ingest` – Ingest a file or URL.
- `POST /query` – Query your knowledge store.
- `GET  /users` – List active user IDs.

## Project Structure
Refer to [plan.md](.windsurf/plan.md) for development roadmap.

## License
MIT
