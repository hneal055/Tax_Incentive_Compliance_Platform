# PilotForge Setup and Run Script
# This script sets up the environment, installs dependencies,
# initializes the database, and starts the FastAPI server.

Write-Host "🚀 PilotForge Setup and Run Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# 1. Navigate to project root
Set-Location $PSScriptRoot
Write-Host "📍 Working directory: $(Get-Location)" -ForegroundColor Yellow

# 2. Check Python installation
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green

# 3. Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists." -ForegroundColor Green
}

# 4. Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Virtual environment activated." -ForegroundColor Green

# 5. Install dependencies
Write-Host "📚 Installing dependencies from requirements.txt..." -ForegroundColor Yellow
if (Test-Path "backend\requirements.txt") {
    pip install -r backend\requirements.txt
} else {
    Write-Host "⚠️  backend\requirements.txt not found, installing default packages..." -ForegroundColor Yellow
    pip install fastapi uvicorn sqlalchemy python-multipart
}
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies installed." -ForegroundColor Green

# 6. Initialize the database (create tables)
Write-Host "🗄️  Initializing database..." -ForegroundColor Yellow
Set-Location backend
python init_db.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to initialize database." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Database initialized." -ForegroundColor Green

# 7. Seed Georgia jurisdiction and rules (if not already present)
Write-Host "🌱 Seeding Georgia jurisdiction and rules..." -ForegroundColor Yellow
python scripts\add_georgia.py
python scripts\seed_georgia.py
Write-Host "✅ Georgia data seeded." -ForegroundColor Green

# 8. Start the FastAPI server
Write-Host "🚀 Starting FastAPI server..." -ForegroundColor Cyan
Write-Host "Server will be available at http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Yellow
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000