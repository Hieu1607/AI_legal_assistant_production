# Check if Docker is running
Write-Host "Checking Docker status..."
try {
    docker info | Out-Null
    Write-Host "Docker is running: OK"
} catch {
    Write-Host "Error: Docker is not running. Please start Docker Desktop first."
    exit 1
}

# Clone repository
Write-Host "Cloning repository..."
git clone https://github.com/Hieu1607/AI_legal_assistant_production.git

# Change to project directory
Set-Location AI_legal_assistant_production

# Install gdown for data download
Write-Host "Installing gdown..."
pip install gdown

# Run download script
Write-Host "Running download script..."
python scripts/download_gdown.py

# Build Docker image
Write-Host "Building Docker image..."
docker-compose build

# Start containers
Write-Host "Starting containers..."
docker-compose up -d

Write-Host "Setup complete!"
Write-Host ""
Write-Host "🚀 Application is starting up with smoke tests..."
Write-Host "⏳ This process takes about 2-3 minutes:"
Write-Host "   1. Warm up ChromaDB (~30s)"
Write-Host "   2. Start server (~30s)" 
Write-Host "   3. Wait for server stability (60s)"
Write-Host "   4. Run smoke tests (~30s)"
Write-Host ""
Write-Host "You can access the application at:"
Write-Host "- API Documentation: http://localhost:8000/docs"
Write-Host "- Health Check: http://localhost:8000/health"
Write-Host ""
Write-Host "To monitor progress: docker-compose logs -f"
Write-Host "Look for 'AI Legal Assistant is fully operational!' message"
