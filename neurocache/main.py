from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List

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
    # TODO: call ingestion pipeline
    return {
        "status": "not_implemented",
        "detail": "Ingestion pipeline not implemented yet",
    }


@app.post("/query")
async def query_endpoint(request: QueryRequest):
    """Query a user's vector store."""
    # TODO: call vector store manager
    return {"answers": [], "detail": "Query pipeline not implemented yet"}


@app.get("/users")
async def list_users():
    """List all user IDs with existing vector stores."""
    # TODO: implement user store tracking
    return {"users": []}
