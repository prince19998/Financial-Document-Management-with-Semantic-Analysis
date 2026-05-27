FROM python:3.11-slim

# Create a non-root user (required by Hugging Face Spaces)
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create storage directories
RUN mkdir -p storage/uploads storage/vectors && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 7860

# Hugging Face Spaces uses port 7860 by default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
