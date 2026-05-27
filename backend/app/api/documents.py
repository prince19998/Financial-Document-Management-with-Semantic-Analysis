from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth.dependencies import current_user, require_permission
from app.config import get_settings
from app.database.session import get_db
from app.models.entities import Document, User
from app.rag.pipeline import rag_pipeline
from app.schemas.domain import DocumentDetail, DocumentOut
from app.services.document_parser import extract_text, validate_extension

router = APIRouter(prefix="/documents", tags=["Documents"])
settings = get_settings()


@router.post("/upload", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def upload_document(
    title: str = Form(...),
    company_name: str = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("documents:upload")),
):
    try:
        validate_extension(file.filename or "")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    safe_name = f"{uuid4().hex}_{Path(file.filename or 'document').name}"
    file_path = upload_dir / safe_name
    file_path.write_bytes(await file.read())

    try:
        content_text = extract_text(str(file_path))
    except Exception as exc:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=f"Could not extract document text: {exc}") from exc

    document = Document(
        title=title,
        company_name=company_name,
        document_type=document_type,
        filename=file.filename or safe_name,
        file_path=str(file_path),
        content_text=content_text,
        uploaded_by=user.id,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    rag_pipeline.index_document(db, document)
    return document


@router.get("", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db), _: User = Depends(require_permission("documents:view"))):
    return db.query(Document).order_by(Document.created_at.desc()).all()


@router.get("/search", response_model=list[DocumentOut])
def keyword_search(q: str = "", db: Session = Depends(get_db), _: User = Depends(require_permission("documents:view"))):
    query = db.query(Document)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Document.title.ilike(like), Document.company_name.ilike(like), Document.document_type.ilike(like)))
    return query.order_by(Document.created_at.desc()).all()


@router.get("/{document_id}", response_model=DocumentDetail)
def get_document(document_id: int, db: Session = Depends(get_db), _: User = Depends(require_permission("documents:view"))):
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentDetail(
        id=document.id,
        title=document.title,
        company_name=document.company_name,
        document_type=document.document_type,
        filename=document.filename,
        uploaded_by=document.uploaded_by,
        created_at=document.created_at,
        content_preview=document.content_text[:3000],
    )


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db), _: User = Depends(require_permission("documents:delete"))):
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    Path(document.file_path).unlink(missing_ok=True)
    db.delete(document)
    db.commit()
    return {"message": "Document deleted"}
