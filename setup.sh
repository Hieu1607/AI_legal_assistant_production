#!/bin/bash

# Check if Docker is running
echo "Checking Docker status..."
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    echo "On Linux: sudo systemctl start docker"
    echo "On macOS: Start Docker Desktop application"
    exit 1
fi
echo "Docker is running: OK"

# Clone repository
echo "Cloning repository..."
git clone https://github.com/Hieu1607/AI_legal_assistant_production.git

# Change to project directory
cd AI_legal_assistant_production

# Install gdown for data download
echo "Installing gdown..."
pip install gdown

# Run download script
echo "Running download script..."
python scripts/download_gdown.py

# Build Docker image
echo "Building Docker image..."
docker-compose build

# Start containers
echo "Starting containers..."
docker-compose up -d

echo "Setup complete!"
echo ""
echo "   Application is starting up with smoke tests..."
echo "   This process takes about 2-3 minutes:"
echo "   1. Warm up ChromaDB (~30s)"
echo "   2. Start server (~30s)" 
echo "   3. Wait for server stability (60s)"
echo "   4. Run smoke tests (~30s)"
echo ""
echo "You can access the application at:"
echo "- API Documentation: http://localhost:8000/docs"
echo "- Health Check: http://localhost:8000/health"
echo ""
echo "To monitor progress: docker-compose logs -f"
echo "Look for 'AI Legal Assistant is fully operational!' message"
