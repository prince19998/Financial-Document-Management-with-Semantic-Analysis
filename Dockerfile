# ============================================
# Stage 1: Build the React frontend
# ============================================
FROM node:20-alpine AS frontend-build

WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --production=false
COPY frontend/ .

# No VITE_API_URL needed — frontend uses relative URLs (same origin)
RUN npm run build

# ============================================
# Stage 2: Python backend + serve frontend
# ============================================
FROM python:3.11-slim

# Required by Hugging Face Spaces
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/app ./app
COPY backend/.env.production .env

# Copy built frontend into /app/static (FastAPI serves this)
COPY --from=frontend-build /frontend/dist ./static

# Create storage directories
RUN mkdir -p storage/uploads storage/vectors && \
    chown -R appuser:appuser /app

USER appuser

# Hugging Face Spaces uses port 7860
EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
