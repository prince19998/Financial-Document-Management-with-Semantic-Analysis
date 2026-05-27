from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_permission
from app.database.session import get_db
from app.models.entities import User
from app.rag.pipeline import rag_pipeline
from app.schemas.domain import SearchRequest, SearchResponse

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/search", response_model=SearchResponse)
def semantic_search(payload: SearchRequest, db: Session = Depends(get_db), user: User = Depends(require_permission("rag:search"))):
    insights, results = rag_pipeline.search(db, payload.query, user_id=user.id, top_k=payload.top_k)
    return SearchResponse(query=payload.query, insights=insights, results=results)
