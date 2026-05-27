from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api import analytics, auth, documents, rag, roles
from app.config import get_settings
from app.database.session import Base, SessionLocal, engine
from app.services.seed import seed_defaults

settings = get_settings()

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_defaults(db)
    finally:
        db.close()


# ── API routes ──────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(documents.router)
app.include_router(rag.router)
app.include_router(analytics.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}


# ── Serve React frontend (only in production/deployment) ───
# The Dockerfile copies the built frontend into /app/static
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

if STATIC_DIR.is_dir():
    # Serve JS/CSS/image assets from the built React app
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(request: Request, full_path: str):
        """Catch-all: serve index.html for any route not matched by API endpoints.
        This enables React Router client-side navigation."""
        file_path = STATIC_DIR / full_path
        if full_path and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(STATIC_DIR / "index.html")
else:
    # Local development — no static files, just show API info
    @app.get("/")
    def root():
        return {
            "status": "ok",
            "service": settings.app_name,
            "docs": "/docs",
            "health": "/health",
        }
