# Super minimal Dockerfile
# pragma: allowlist nextline critical_high_vulnerabilities
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

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

# Fix line endings and make startup script executable
RUN sed -i 's/\r$//' /app/scripts/start_with_warmup.sh && \
    chmod +x /app/scripts/start_with_warmup.sh

EXPOSE 8000

CMD ["/app/scripts/start_with_warmup.sh"]