from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_permission
from app.database.session import get_db
from app.models.entities import Document, SearchLog, User

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), _: User = Depends(require_permission("documents:view"))):
    document_types = db.query(Document.document_type, func.count(Document.id)).group_by(Document.document_type).all()
    recent_searches = db.query(SearchLog.query, SearchLog.results_count, SearchLog.created_at).order_by(SearchLog.created_at.desc()).limit(8).all()
    return {
        "total_documents": db.query(Document).count(),
        "uploaded_files": db.query(Document).count(),
        "active_users": db.query(User).filter_by(is_active=True).count(),
        "searches": db.query(SearchLog).count(),
        "document_types": [{"name": name, "count": count} for name, count in document_types],
        "recent_searches": [{"query": q, "results_count": count, "created_at": created_at} for q, count, created_at in recent_searches],
    }
