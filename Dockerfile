# Root Dockerfile for ScamShield AI Backend
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including Tesseract OCR and OpenGL libraries for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt && \
    python -m spacy download en_core_web_sm && \
    mkdir -p /app/data /app/mlruns /app/ml/artifacts

# Copy application source code and relevant data
COPY backend/ /app/backend/
COPY ml/ /app/ml/
COPY knowledge_base/ /app/knowledge_base/
COPY docs/ /app/docs/

ENV PYTHONPATH=/app
ENV PORT=8000

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
