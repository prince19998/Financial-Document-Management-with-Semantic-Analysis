from datetime import datetime

from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    description: str | None = None
    permissions: list[str] = []


class AssignRoleRequest(BaseModel):
    user_id: int
    role_name: str


class DocumentOut(BaseModel):
    id: int
    title: str
    company_name: str
    document_type: str
    filename: str
    uploaded_by: int
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentDetail(DocumentOut):
    content_preview: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    document_id: int
    title: str
    company_name: str
    document_type: str
    chunk: str
    score: float


class SearchResponse(BaseModel):
    query: str
    insights: str
    results: list[SearchResult]
