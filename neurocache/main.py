from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List
import os, uuid
from pathlib import Path
from langchain_community.embeddings import OpenAIEmbeddings
from neurocache.core.ingestion import load_document, chunk_and_augment
from neurocache.core.vector_store import create_index, add_embeddings

load_dotenv()

app = FastAPI(
    title="NeuroCache API",
    version="0.1.0",
    description="Augmented RAG Ingest & Retrieval System",
)


class QueryRequest(BaseModel):
    user_id: str
    question: str
    top_k: int = 5
    metadata_filters: Optional[dict] = None


@app.post("/ingest")
async def ingest(
    user_id: str = Form(...),
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
):
    """Ingest a document file or URL for a given user."""
    # Ingest pipeline
    from neurocache.config import TEMP_UPLOADS_DIR
    temp_dir = TEMP_UPLOADS_DIR
    file_path = None
    if file:
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = str(temp_dir / filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
    # Load text
    text = load_document(file_path=file_path, url=url)
    # Chunk and augment
    metadata = {"source": file.filename if file else url}
    chunks = chunk_and_augment(text, metadata)
    # Create and populate vector store
    create_index(user_id)
    embedder = OpenAIEmbeddings()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedder.embed_documents(texts)
    metadatas = [chunk["metadata"] for chunk in chunks]
    add_embeddings(user_id, embeddings, metadatas)
    return {"status": "success", "ingested_chunks": len(chunks)}


@app.post("/query")
async def query_endpoint(request: QueryRequest):
    """Query a user's vector store."""
    # Generate embedding for the question
    embedder = OpenAIEmbeddings()
    query_embedding = embedder.embed_query(request.question)
    # Query vector store
    from neurocache.core.vector_store import query_index
    results = query_index(request.user_id, query_embedding, request.top_k)
    # Optionally filter by metadata
    if request.metadata_filters:
        def match(meta):
            return all(meta.get(k) == v for k, v in request.metadata_filters.items())
        results = [r for r in results if match(r)]
    return {"results": results}

    return {"answers": [], "detail": "Query pipeline not implemented yet"}


@app.get("/users")
async def list_users():
    """List all user IDs with existing vector stores."""
    from neurocache.config import USER_STORES_DIR
    if not USER_STORES_DIR.exists():
        return {"user_ids": []}
    files = os.listdir(USER_STORES_DIR)
    user_ids = set()
    for f in files:
        if f.endswith(".index"):
            user_ids.add(f[:-6])
    return {"user_ids": sorted(user_ids)}
