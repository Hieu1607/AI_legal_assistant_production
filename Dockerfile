# Super minimal Dockerfile
# pragma: allowlist nextline critical_high_vulnerabilities
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install system dependencies including curl for smoke tests
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt ./

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app/ ./app/
COPY src/ ./src/
COPY configs/ ./configs/
COPY services/ ./services/
COPY scripts/ ./scripts/
COPY .env.example .env

# Create basic directories
RUN mkdir -p logs

# Pre-download sentence-transformer model để tăng tốc khởi động
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
import os; \
print('Downloading BAAI/bge-m3 model...'); \
model = SentenceTransformer('BAAI/bge-m3'); \
"

# Fix line endings and make startup scripts executable
RUN sed -i 's/\r$//' /app/scripts/start_with_warmup.sh && \
    sed -i 's/\r$//' /app/scripts/start_with_smoke_test.sh && \
    sed -i 's/\r$//' /app/scripts/smoke_test.sh && \
    chmod +x /app/scripts/start_with_warmup.sh && \
    chmod +x /app/scripts/start_with_smoke_test.sh && \
    chmod +x /app/scripts/smoke_test.sh 


EXPOSE 8000

# Mặc định sử dụng startup với smoke test
# Để chạy không có smoke test: docker run ... /app/scripts/start_with_warmup.sh
CMD ["/app/scripts/start_with_smoke_test.sh"]


