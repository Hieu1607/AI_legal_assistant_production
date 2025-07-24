# AI Legal Assistant Quick Installer
# Run this script on any Windows machine to setup the project

Write-Host "AI Legal Assistant - Quick Setup"
Write-Host "================================="

# Check prerequisites
Write-Host "Checking prerequisites..."

# Check Git
try {
    git --version | Out-Null
    Write-Host "Git: OK"
} catch {
    Write-Host "Error: Git is not installed. Please install Git first."
    exit 1
}

# Check Python
try {
    python --version | Out-Null
    Write-Host "Python: OK"
} catch {
    Write-Host "Error: Python is not installed. Please install Python first."
    exit 1
}

# Check Docker
try {
    docker --version | Out-Null
    Write-Host "Docker: OK"
} catch {
    Write-Host "Error: Docker is not installed. Please install Docker Desktop first."
    exit 1
}

Write-Host "All prerequisites met!"
Write-Host ""

# Download and run setup script
Write-Host "Downloading setup script..."
try {
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Hieu1607/AI_legal_assistant_production/main/setup.ps1" -OutFile "ai_legal_setup.ps1"
    Write-Host "Running setup..."
    .\ai_legal_setup.ps1
    Remove-Item "ai_legal_setup.ps1"
} catch {
    Write-Host "Error downloading or running setup script: $_"
    exit 1
}
