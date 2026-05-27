Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# 📊 Financial Document Intelligence Platform

A full-stack **Financial Document Management** system with **Semantic Analysis (RAG)** capabilities. Upload financial documents (PDF, DOCX, CSV, TXT), automatically extract and index their content using vector embeddings, and perform intelligent semantic search across your entire document corpus.

Built with **FastAPI** + **React (Vite)** — featuring JWT authentication, Role-Based Access Control (RBAC), FAISS vector search, cross-encoder re-ranking, and a modern responsive dashboard.

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture Overview](#-architecture-overview)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Getting Started](#-getting-started)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Backend Setup](#2-backend-setup)
  - [3. Frontend Setup](#3-frontend-setup)
  - [4. Run Both Together](#4-run-both-together)
- [Environment Variables](#-environment-variables)
  - [Backend (.env)](#backend-env)
  - [Frontend (.env)](#frontend-env)
- [Security Key — How to Generate](#-security-key--how-to-generate)
- [Authentication & Authorization](#-authentication--authorization)
  - [JWT Tokens](#jwt-tokens)
  - [Default Roles & Permissions](#default-roles--permissions)
  - [Default Admin Credentials](#default-admin-credentials)
- [API Reference](#-api-reference)
  - [Authentication](#authentication)
  - [Documents](#documents)
  - [RAG / Semantic Search](#rag--semantic-search)
  - [Analytics](#analytics)
  - [RBAC (Roles & Users)](#rbac-roles--users)
  - [Health Check](#health-check)
- [RAG Pipeline — How It Works](#-rag-pipeline--how-it-works)
- [Supported File Formats](#-supported-file-formats)
- [Database](#-database)
- [Docker Deployment](#-docker-deployment)
  - [Using Docker Compose (Full Stack)](#using-docker-compose-full-stack)
  - [Single Dockerfile (Hugging Face Spaces)](#single-dockerfile-hugging-face-spaces)
- [Deploying the Frontend](#-deploying-the-frontend)
  - [Vercel](#vercel)
  - [Netlify](#netlify)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| Category | Feature |
|---|---|
| 📄 **Document Management** | Upload, view, search, and delete financial documents (PDF, DOCX, CSV, TXT) |
| 🔍 **Semantic Search (RAG)** | AI-powered search using sentence embeddings + FAISS vector store + cross-encoder re-ranking |
| 🔐 **Authentication** | JWT-based auth with access tokens (30 min) and refresh tokens (7 days) |
| 🛡️ **RBAC** | Role-Based Access Control with 4 default roles: Admin, Financial Analyst, Auditor, Client |
| 📊 **Analytics Dashboard** | Real-time stats: total documents, active users, search logs, document type breakdown |
| 🧠 **Auto Insights** | AI-generated insight summaries for each semantic search query |
| 👥 **User Management** | Admin panel to manage users, create roles, and assign permissions |
| 🐳 **Docker Ready** | Multi-stage Dockerfile + docker-compose for one-command deployment |
| ☁️ **Cloud Deployable** | Pre-configured for Vercel, Netlify (frontend) and Hugging Face Spaces (backend) |

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | REST API framework |
| [SQLAlchemy 2.0](https://www.sqlalchemy.org/) | ORM & database management |
| [Pydantic v2](https://docs.pydantic.dev/) | Data validation & schemas |
| [python-jose](https://github.com/mpdavis/python-jose) | JWT token creation & verification |
| [passlib + bcrypt](https://passlib.readthedocs.io/) | Password hashing |
| [FAISS](https://github.com/facebookresearch/faiss) | Vector similarity search |
| [Sentence Transformers](https://www.sbert.net/) | Text embeddings (`all-MiniLM-L6-v2`) |
| [Cross-Encoder](https://www.sbert.net/docs/cross_encoder/usage/usage.html) | Re-ranking search results (`ms-marco-MiniLM-L-6-v2`) |
| [LangChain](https://www.langchain.com/) | Text chunking (RecursiveCharacterTextSplitter) |
| [PyPDF / python-docx / Pandas](https://pypdf.readthedocs.io/) | Document text extraction |
| SQLite (dev) / PostgreSQL (prod) | Database |
| Uvicorn | ASGI server |

### Frontend
| Technology | Purpose |
|---|---|
| [React 18](https://react.dev/) | UI library |
| [Vite 6](https://vitejs.dev/) | Build tool & dev server |
| [React Router v6](https://reactrouter.com/) | Client-side routing |
| [Axios](https://axios-http.com/) | HTTP client |
| [Bootstrap 5](https://getbootstrap.com/) | CSS framework |
| [Chart.js + react-chartjs-2](https://www.chartjs.org/) | Analytics charts |
| [Lucide React](https://lucide.dev/) | Icon library |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                  │
│  Login/Register │ Dashboard │ Documents │ Search │ Admin Panel  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP (Axios)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
│                                                                 │
│  ┌──────────┐  ┌────────────┐  ┌─────────┐  ┌──────────────┐  │
│  │ Auth API │  │ Docs API   │  │ RAG API │  │ Analytics API│  │
│  │ /auth/*  │  │ /documents │  │ /rag/*  │  │ /analytics/* │  │
│  └────┬─────┘  └─────┬──────┘  └────┬────┘  └──────┬───────┘  │
│       │              │              │               │          │
│  ┌────▼──────────────▼──────────────▼───────────────▼───────┐  │
│  │                   Service Layer                          │  │
│  │  Security │ Document Parser │ RAG Pipeline │ Seed Data   │  │
│  └────┬──────────────┬──────────────┬───────────────────────┘  │
│       │              │              │                          │
│  ┌────▼──────┐  ┌────▼──────┐  ┌───▼────────────┐            │
│  │ SQLAlchemy│  │ File      │  │ FAISS Vector   │            │
│  │ (SQLite/  │  │ Storage   │  │ Store          │            │
│  │ PostgreSQL│  │           │  │ + Embeddings   │            │
│  └───────────┘  └───────────┘  └────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
Financial-Document-Management-with-Semantic-Analysis/
│
├── backend/                        # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # App entry point, CORS, routers, startup
│   │   ├── config.py               # Pydantic Settings (reads .env)
│   │   │
│   │   ├── api/                    # API route handlers
│   │   │   ├── auth.py             # POST /auth/register, /auth/login, GET /auth/me
│   │   │   ├── documents.py        # CRUD for documents + upload
│   │   │   ├── rag.py              # POST /rag/search (semantic search)
│   │   │   ├── analytics.py        # GET /analytics/summary
│   │   │   └── roles.py            # RBAC: roles, permissions, user management
│   │   │
│   │   ├── auth/                   # Authentication & authorization
│   │   │   ├── security.py         # JWT creation, password hashing (bcrypt)
│   │   │   └── dependencies.py     # current_user, require_permission guards
│   │   │
│   │   ├── database/
│   │   │   └── session.py          # SQLAlchemy engine, session, Base
│   │   │
│   │   ├── models/
│   │   │   └── entities.py         # ORM models: User, Role, Permission, Document, etc.
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py             # Pydantic: RegisterRequest, LoginRequest, TokenPair
│   │   │   └── domain.py           # Pydantic: DocumentOut, SearchRequest/Response, etc.
│   │   │
│   │   ├── services/
│   │   │   ├── document_parser.py  # Extract text from PDF, DOCX, CSV, TXT
│   │   │   └── seed.py             # Auto-seed roles, permissions, admin user
│   │   │
│   │   ├── rag/
│   │   │   ├── pipeline.py         # RAG: chunking, embedding, indexing, search, rerank
│   │   │   └── vector_store.py     # FAISS index management (add, search, persist)
│   │   │
│   │   └── utils/                  # (Reserved for future utilities)
│   │
│   ├── storage/
│   │   ├── uploads/                # Uploaded document files
│   │   └── vectors/                # FAISS index + metadata JSON
│   │
│   ├── .env                        # Development environment variables
│   ├── .env.production             # Production environment variables
│   ├── requirements.txt            # Python dependencies
│   └── Dockerfile                  # Backend Docker image
│
├── frontend/                       # React Frontend (Vite)
│   ├── src/
│   │   ├── main.jsx                # React DOM entry point
│   │   ├── App.jsx                 # Router & route definitions
│   │   ├── styles.css              # Global styles
│   │   │
│   │   ├── pages/
│   │   │   ├── Login.jsx           # Login page
│   │   │   ├── Register.jsx        # Registration page
│   │   │   ├── Dashboard.jsx       # Main dashboard with stats
│   │   │   ├── Documents.jsx       # Document listing & search
│   │   │   ├── DocumentDetails.jsx # Single document view
│   │   │   ├── UploadDocument.jsx  # Upload new documents
│   │   │   ├── SemanticSearch.jsx  # RAG-powered search page
│   │   │   ├── Analytics.jsx       # Analytics & charts
│   │   │   ├── Users.jsx           # User management (Admin)
│   │   │   └── Roles.jsx           # Role management (Admin)
│   │   │
│   │   ├── components/
│   │   │   ├── Layout.jsx          # App shell: sidebar + header
│   │   │   ├── StatCard.jsx        # Reusable stat card component
│   │   │   └── Toast.jsx           # Toast notification component
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.jsx     # React Context for auth state
│   │   │
│   │   ├── routes/
│   │   │   └── ProtectedRoute.jsx  # Route guard (auth + role check)
│   │   │
│   │   └── services/
│   │       └── api.js              # Axios instance with auth interceptor
│   │
│   ├── index.html                  # HTML entry point
│   ├── vite.config.js              # Vite configuration
│   ├── .env                        # Frontend env (VITE_API_URL)
│   ├── vercel.json                 # Vercel deployment config
│   ├── netlify.toml                # Netlify deployment config
│   ├── package.json                # Node dependencies
│   └── Dockerfile                  # Frontend Docker image (Nginx)
│
├── docker-compose.yml              # Full-stack orchestration
├── Dockerfile                      # Combined multi-stage Dockerfile (HF Spaces)
├── package.json                    # Root: concurrently for dev
├── .gitignore
└── README.md                       # ← You are here
```

---

## 📋 Prerequisites

Make sure you have the following installed on your system:

| Tool | Minimum Version | Download Link |
|---|---|---|
| **Python** | 3.11+ | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org/) |
| **npm** | 9+ | Comes with Node.js |
| **Git** | Any | [git-scm.com](https://git-scm.com/) |
| **Docker** *(optional)* | 24+ | [docker.com](https://www.docker.com/) |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/prince19998/Financial-Document-Management-with-Semantic-Analysis.git
cd Financial-Document-Management-with-Semantic-Analysis
```

---

### 2. Backend Setup

#### a) Create a Python Virtual Environment

```bash
cd backend

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### b) Install Python Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** The first run will download the Sentence Transformer models (~80 MB for `all-MiniLM-L6-v2` and ~23 MB for `ms-marco-MiniLM-L-6-v2`). This is a one-time download.

#### c) Configure Environment Variables

Copy the example `.env` file and update it:

```bash
# The .env file is already provided for development
# Review and update these values as needed:
```

```env
APP_NAME="Financial Document Intelligence Platform"
ENVIRONMENT=development
DATABASE_URL=sqlite:///./financial_docs.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
UPLOAD_DIR=storage/uploads
VECTOR_DIR=storage/vectors
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
```

#### d) Run the Backend Server

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at:
- **API Base:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

### 3. Frontend Setup

Open a **new terminal** window:

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The frontend will be available at: **http://localhost:5173**

---

### 4. Run Both Together

From the **project root directory**, you can run both the backend and frontend simultaneously:

```bash
# Install root dependencies (one time)
npm install

# Run both servers concurrently
npm run dev
```

> This uses `concurrently` to start the backend (Uvicorn on port 8000) and frontend (Vite on port 5173) in parallel.

---

## ⚙️ Environment Variables

### Backend (.env)

Create/edit `backend/.env`:

| Variable | Description | Default Value |
|---|---|---|
| `APP_NAME` | Application display name | `Financial Document Intelligence Platform` |
| `ENVIRONMENT` | Running environment (`development` / `production`) | `development` |
| `DATABASE_URL` | Database connection string | `sqlite:///./financial_docs.db` |
| `SECRET_KEY` | **JWT signing secret** (see below how to generate) | `change-me-in-production` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | `7` |
| `UPLOAD_DIR` | Directory for uploaded files | `storage/uploads` |
| `VECTOR_DIR` | Directory for FAISS index files | `storage/vectors` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:5173,http://localhost:3000` |
| `EMBEDDING_MODEL` | Sentence Transformer model name | `sentence-transformers/all-MiniLM-L6-v2` |
| `RERANKER_MODEL` | Cross-Encoder model for re-ranking | `cross-encoder/ms-marco-MiniLM-L-6-v2` |

### Frontend (.env)

Create/edit `frontend/.env`:

| Variable | Description | Default Value |
|---|---|---|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000` |

---

## 🔑 Security Key — How to Generate

The `SECRET_KEY` is used to sign and verify JWT tokens. **It is critical that you use a strong, unique key in production.**

### Method 1: Using Python (Recommended)

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

This generates a cryptographically secure 64-character hex string, e.g.:

```
a3f8b2c9d1e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0
```

### Method 2: Using OpenSSL

```bash
openssl rand -hex 32
```

### Method 3: Using Node.js

```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### Method 4: Using PowerShell (Windows)

```powershell
-join ((1..32) | ForEach-Object { '{0:x2}' -f (Get-Random -Maximum 256) })
```

### How to Apply

1. Generate a key using any method above.
2. Open `backend/.env`.
3. Replace the `SECRET_KEY` value:

```env
SECRET_KEY=your-newly-generated-64-char-hex-key
```

> ⚠️ **IMPORTANT:**
> - Never commit your production `SECRET_KEY` to version control.
> - Changing the `SECRET_KEY` will **invalidate all existing JWT tokens** — all users will need to log in again.
> - The key should be **at least 32 characters** long for HS256.

---

## 🔐 Authentication & Authorization

### JWT Tokens

The platform uses **Bearer token** authentication (JWT):

1. **Register** a new account via `POST /auth/register`.
2. **Login** via `POST /auth/login` → returns `access_token` + `refresh_token`.
3. Include the token in all subsequent requests:

```
Authorization: Bearer <access_token>
```

| Token Type | Lifetime | Purpose |
|---|---|---|
| Access Token | 30 minutes | API authentication |
| Refresh Token | 7 days | Obtain new access tokens |

### Default Roles & Permissions

On first startup, the system auto-seeds the following roles:

| Role | Permissions | Description |
|---|---|---|
| **Admin** | `admin:*` | Full platform access (all operations) |
| **Financial Analyst** | `documents:upload`, `documents:edit`, `documents:view`, `rag:search` | Upload/edit docs, semantic search |
| **Auditor** | `documents:view`, `documents:review`, `rag:search` | View & review docs, semantic search |
| **Client** | `documents:view`, `rag:search` | View docs, semantic search (default for new users) |

#### All Available Permissions

| Permission Code | Description |
|---|---|
| `admin:*` | Full platform access |
| `documents:upload` | Upload financial documents |
| `documents:edit` | Edit document metadata |
| `documents:view` | View company documents |
| `documents:delete` | Delete documents |
| `documents:review` | Review documents |
| `rag:search` | Use semantic search and RAG |
| `users:manage` | Manage users and roles |

### Default Admin Credentials

> ⚠️ **Change these immediately in production!**

| Field | Value |
|---|---|
| Email | `admin@example.com` |
| Password | `Admin@123` |
| Role | `Admin` (full access) |

The admin account is auto-created on first startup via the seed service.

---

## 📡 API Reference

The full interactive API documentation is available at **http://localhost:8000/docs** (Swagger UI) after starting the backend.

### Authentication

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | ❌ Public | Register a new user |
| `POST` | `/auth/login` | ❌ Public | Login & receive JWT tokens |
| `GET` | `/auth/me` | ✅ Bearer | Get current user profile |

**Register Example:**
```json
POST /auth/register
{
  "email": "analyst@company.com",
  "full_name": "John Doe",
  "password": "SecureP@ss123"
}
```

**Login Example:**
```json
POST /auth/login
{
  "email": "analyst@company.com",
  "password": "SecureP@ss123"
}

// Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

### Documents

| Method | Endpoint | Auth | Permission | Description |
|---|---|---|---|---|
| `POST` | `/documents/upload` | ✅ | `documents:upload` | Upload a document (multipart form) |
| `GET` | `/documents` | ✅ | `documents:view` | List all documents |
| `GET` | `/documents/search?q=term` | ✅ | `documents:view` | Keyword search (title, company, type) |
| `GET` | `/documents/{id}` | ✅ | `documents:view` | Get document details + content preview |
| `DELETE` | `/documents/{id}` | ✅ | `documents:delete` | Delete a document |

**Upload Example (multipart/form-data):**
```bash
curl -X POST http://localhost:8000/documents/upload \
  -H "Authorization: Bearer <token>" \
  -F "title=Q4 Earnings Report" \
  -F "company_name=Acme Corp" \
  -F "document_type=Earnings Report" \
  -F "file=@/path/to/report.pdf"
```

---

### RAG / Semantic Search

| Method | Endpoint | Auth | Permission | Description |
|---|---|---|---|---|
| `POST` | `/rag/search` | ✅ | `rag:search` | Semantic search across all documents |

**Request:**
```json
POST /rag/search
{
  "query": "What was the revenue growth in Q4?",
  "top_k": 5
}
```

**Response:**
```json
{
  "query": "What was the revenue growth in Q4?",
  "insights": "Found 3 high-relevance passages for 'What was the revenue growth in Q4?'. The evidence spans Earnings Report for Acme Corp. Review the matched excerpts before making audit or credit decisions. Evidence ref: a1b2c3d4.",
  "results": [
    {
      "document_id": 1,
      "title": "Q4 Earnings Report",
      "company_name": "Acme Corp",
      "document_type": "Earnings Report",
      "chunk": "Revenue grew by 15% year-over-year in Q4 2024...",
      "score": 0.89
    }
  ]
}
```

---

### Analytics

| Method | Endpoint | Auth | Permission | Description |
|---|---|---|---|---|
| `GET` | `/analytics/summary` | ✅ | `documents:view` | Platform statistics summary |

**Response:**
```json
{
  "total_documents": 42,
  "uploaded_files": 42,
  "active_users": 8,
  "searches": 156,
  "document_types": [
    { "name": "Earnings Report", "count": 15 },
    { "name": "Balance Sheet", "count": 12 }
  ],
  "recent_searches": [
    { "query": "revenue Q4", "results_count": 3, "created_at": "2024-12-01T..." }
  ]
}
```

---

### RBAC (Roles & Users)

> All RBAC endpoints require `users:manage` permission (Admin only).

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/users` | ✅ | List all users |
| `GET` | `/users/{id}/roles` | ✅ | Get user's assigned roles |
| `GET` | `/users/{id}/permissions` | ✅ | Get user's effective permissions |
| `POST` | `/users/assign-role` | ✅ | Assign a role to a user |
| `GET` | `/roles` | ✅ | List all roles |
| `POST` | `/roles/create` | ✅ | Create a new role with permissions |

---

### Health Check

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/health` | ❌ Public | Service health status |

---

## 🧠 RAG Pipeline — How It Works

The Retrieval-Augmented Generation pipeline processes and searches documents in 5 steps:

```
┌──────────────────────────────────────────────────────────────┐
│                    DOCUMENT INGESTION                        │
│                                                              │
│  1. UPLOAD → Extract text (PDF/DOCX/CSV/TXT)                │
│  2. CHUNK  → Split into ~900 char chunks (150 overlap)      │
│  3. EMBED  → Generate 384-dim vectors (MiniLM-L6-v2)        │
│  4. INDEX  → Store vectors in FAISS (Inner Product search)   │
│  5. SAVE   → Persist chunk metadata in SQLite/PostgreSQL     │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    SEMANTIC SEARCH                           │
│                                                              │
│  1. EMBED QUERY  → Convert user query to 384-dim vector     │
│  2. VECTOR SEARCH → Retrieve top-20 similar chunks (FAISS)  │
│  3. RE-RANK      → Cross-Encoder re-scores for precision    │
│  4. TOP-K        → Return top-K most relevant chunks        │
│  5. INSIGHTS     → Generate summary of findings             │
└──────────────────────────────────────────────────────────────┘
```

### Models Used

| Model | Size | Purpose |
|---|---|---|
| `sentence-transformers/all-MiniLM-L6-v2` | ~80 MB | Bi-encoder for generating 384-dim embeddings |
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | ~23 MB | Cross-encoder for re-ranking search results |

> Models are downloaded automatically from [Hugging Face](https://huggingface.co/) on first use and cached locally.

---

## 📎 Supported File Formats

| Format | Extension | Parser |
|---|---|---|
| PDF | `.pdf` | PyPDF (`pypdf`) |
| Word Document | `.docx` | python-docx |
| CSV | `.csv` | Pandas |
| Plain Text | `.txt` | Built-in Python I/O |

---

## 🗄️ Database

### Development (Default)
- **SQLite** — zero configuration, file-based (`financial_docs.db`)
- Tables are auto-created on startup

### Production
- **PostgreSQL 16** — configured via `docker-compose.yml`
- Connection string: `postgresql+psycopg2://findoc:findoc@db:5432/financial_docs`

### Database Schema (Entity Relationship)

```
┌──────────────┐     ┌──────────────┐     ┌─────────────────┐
│    Users     │────▶│  user_roles  │◀────│     Roles       │
│              │     │ (junction)   │     │                 │
│ id           │     └──────────────┘     │ id              │
│ email        │                          │ name            │
│ full_name    │     ┌──────────────┐     │ description     │
│ hashed_pass  │     │role_permis.  │     └────────┬────────┘
│ is_active    │     │ (junction)   │              │
│ created_at   │     └──────┬───────┘     ┌────────▼────────┐
└──────┬───────┘            │             │  Permissions    │
       │                    │             │ id              │
       │                    └─────────────│ code            │
       │                                  │ description     │
       │                                  └─────────────────┘
       │
       ▼
┌──────────────────┐     ┌──────────────────────┐
│   Documents      │────▶│  EmbeddingMetadata   │
│                  │     │                      │
│ id               │     │ id                   │
│ title            │     │ document_id          │
│ company_name     │     │ chunk_index          │
│ document_type    │     │ vector_id            │
│ filename         │     │ chunk_text           │
│ file_path        │     │ created_at           │
│ content_text     │     └──────────────────────┘
│ uploaded_by (FK) │
│ created_at       │     ┌──────────────────────┐
└──────────────────┘     │   SearchLog          │
                         │                      │
                         │ id                   │
                         │ user_id (FK)         │
                         │ query                │
                         │ results_count        │
                         │ created_at           │
                         └──────────────────────┘
```

---

## 🐳 Docker Deployment

### Using Docker Compose (Full Stack)

This spins up **PostgreSQL + Backend + Frontend** in one command:

```bash
docker-compose up --build
```

| Service | Port | URL |
|---|---|---|
| PostgreSQL | 5432 | Internal |
| Backend (FastAPI) | 8000 | http://localhost:8000 |
| Frontend (Nginx) | 3000 | http://localhost:3000 |

To run in the background:
```bash
docker-compose up --build -d
```

To stop:
```bash
docker-compose down
```

To stop and remove data volumes:
```bash
docker-compose down -v
```

---

### Single Dockerfile (Hugging Face Spaces)

The root `Dockerfile` is a multi-stage build that:
1. Builds the React frontend
2. Copies the built assets into the Python backend
3. Serves everything from FastAPI on **port 7860**

```bash
# Build
docker build -t findoc-ai .

# Run
docker run -p 7860:7860 findoc-ai
```

Access at: **http://localhost:7860**

---

## ☁️ Deploying the Frontend

### Vercel

The `frontend/vercel.json` is pre-configured with SPA rewrites.

1. Push your code to GitHub.
2. Go to [vercel.com](https://vercel.com) → Import your repository.
3. Set the **Root Directory** to `frontend`.
4. Set the environment variable:
   ```
   VITE_API_URL=https://your-backend-url.com
   ```
5. Deploy!

### Netlify

The `frontend/netlify.toml` is pre-configured.

1. Push your code to GitHub.
2. Go to [netlify.com](https://netlify.com) → Import your repository.
3. Set the **Base Directory** to `frontend`.
4. Set the **Build Command** to `npm run build`.
5. Set the **Publish Directory** to `dist`.
6. Add the environment variable:
   ```
   VITE_API_URL=https://your-backend-url.com
   ```
7. Deploy!

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'faiss'` | Run `pip install faiss-cpu` |
| `CORS errors` in browser console | Ensure `CORS_ORIGINS` in `.env` includes your frontend URL |
| Models not downloading | Check internet connection; models download from Hugging Face on first use |
| `sqlite3.OperationalError: database is locked` | This can happen with concurrent writes to SQLite; switch to PostgreSQL for production |
| Port already in use | Kill the process using the port or change the port in config |
| `401 Unauthorized` on API calls | Your JWT token may have expired (30 min); log in again |
| Frontend can't reach backend | Ensure `VITE_API_URL` in `frontend/.env` points to the correct backend URL |
| Upload fails with "Unsupported file format" | Only `.pdf`, `.docx`, `.csv`, and `.txt` files are supported |

### Resetting the Database (Development)

```bash
# Delete the SQLite database file
cd backend
rm financial_docs.db

# Delete vector index
rm -rf storage/vectors/*

# Restart the backend — tables and seed data will be recreated
uvicorn app.main:app --reload
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is open-source. Feel free to use, modify, and distribute as needed.

---

<div align="center">

**Built with ❤️ using FastAPI + React + FAISS**

[⬆ Back to Top](#-financial-document-intelligence-platform)

</div>
