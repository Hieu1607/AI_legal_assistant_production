#!/bin/bash
# Start script with ChromaDB warm up for AI Legal Assistant

set -e  # Exit on any error

echo "Starting AI Legal Assistant with warm up..."

# Run warm up script
echo "Running warm up sequence..."
if python /app/scripts/warmup_chromadb.py; then
    echo "Warm up completed successfully!"
    echo "Starting FastAPI server..."
    
    # Start the main application
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
else
    echo "Warm up failed! Starting server anyway..."
    # Start server even if warm up fails (graceful degradation)
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi
