#!/bin/bash
# Start script with ChromaDB warm up for AI Legal Assistant

set -e  # Exit on any error

echo "Starting AI Legal Assistant with warm up..."

# Run initial warm up script
echo "Running initial warm up sequence..."
if python /app/scripts/warmup_chromadb.py; then
    echo "Initial warm up completed successfully!"
else
    echo "Initial warm up failed! Continuing anyway..."
fi

echo "Starting FastAPI server..."

# Start the main application in background
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

# Wait for server to be ready
echo "Waiting for server to start..."
sleep 10

# Check if server is running
if kill -0 $UVICORN_PID 2>/dev/null; then
    echo "Server started successfully! Running post-startup warm up..."
    
    # Run second warm up after server is running
    if python /app/scripts/warmup_chromadb.py --post-startup; then
        echo "Post-startup warm up completed successfully!"
    else
        echo "Post-startup warm up failed! Server will continue running..."
    fi
    
    # Wait for the uvicorn process
    wait $UVICORN_PID
else
    echo "Server failed to start!"
    exit 1
fi
