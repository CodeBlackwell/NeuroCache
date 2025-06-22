from pydantic import BaseModel
from typing import Optional, List, Dict


class IngestResponse(BaseModel):
    status: str
    detail: Optional[str] = None


class QueryRequest(BaseModel):
    user_id: str
    question: str
    top_k: int = 5
    metadata_filters: Optional[Dict[str, List[str]]] = None


class QueryResult(BaseModel):
    matched_text: str
    metadata: Dict[str, str]


class QueryResponse(BaseModel):
    answers: List[QueryResult]
    detail: Optional[str] = None


class UsersResponse(BaseModel):
    users: List[str]
