# AI-Powered Financial Document Management System

Enterprise-style financial document intelligence platform with FastAPI, JWT auth, RBAC, document upload, text extraction, FAISS semantic indexing, reranking, and a React dashboard.

## Features

- JWT registration/login with protected APIs and frontend routes
- RBAC roles: Admin, Financial Analyst, Auditor, Client
- PDF, DOCX, TXT, CSV document upload and metadata management
- RAG pipeline: extraction, chunking, sentence-transformer embeddings, FAISS storage, semantic retrieval, reranking
- Semantic search endpoint with contextual financial insights
- Responsive React + Bootstrap dashboard with dark/light mode
- User, role, document, upload, analytics, and search screens
- PostgreSQL/MySQL-ready via `DATABASE_URL`; SQLite is the local default

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

API docs open at `http://localhost:8000/docs`.

Default admin:

- Email: `admin@example.com`
- Password: `Admin@123`

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Environment

Set `DATABASE_URL` for production databases:

```env
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/financial_docs
```

or:

```env
DATABASE_URL=mysql+pymysql://user:password@host:3306/financial_docs
```

## Main APIs

- `POST /auth/register`
- `POST /auth/login`
- `POST /roles/create`
- `POST /users/assign-role`
- `GET /users/{id}/roles`
- `GET /users/{id}/permissions`
- `POST /documents/upload`
- `GET /documents`
- `GET /documents/{document_id}`
- `DELETE /documents/{document_id}`
- `GET /documents/search`
- `POST /rag/search`
- `GET /analytics/summary`

## Deployment Notes

- Frontend: Vercel or Netlify
- Backend: Render, Railway, AWS, or Docker
- Database: PostgreSQL on NeonDB, Railway, Render, or AWS RDS
- Vector store: FAISS files under `backend/storage/vectors`; swap `app/rag/vector_store.py` for Qdrant or Chroma when using managed vector infrastructure
