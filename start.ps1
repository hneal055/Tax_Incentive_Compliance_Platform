# Tax-Incentive Compliance Platform - Daily Startup Script
# Run this script every day to start your development environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Tax-Incentive Compliance Platform" -ForegroundColor Cyan
Write-Host "Daily Startup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if in correct directory
$projectPath = "C:\Projects\Tax_Incentive_Compliance_Platform"
if ((Get-Location).Path -ne $projectPath) {
    Write-Host "Navigating to project directory..." -ForegroundColor Yellow
    Set-Location $projectPath
}

Write-Host "✓ In project directory" -ForegroundColor Green
Write-Host ""

# Step 2: Check Docker Desktop
Write-Host "Checking Docker Desktop..." -ForegroundColor Yellow
try {
    $dockerRunning = docker ps 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Docker Desktop is running" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Docker Desktop is not running" -ForegroundColor Red
    Write-Host "  Please start Docker Desktop and run this script again" -ForegroundColor Yellow
    pause
    exit
}
Write-Host ""

# Step 3: Start PostgreSQL
Write-Host "Starting PostgreSQL..." -ForegroundColor Yellow
$containerExists = docker ps -a --filter "name=tax-incentive-db" --format "{{.Names}}"
if ($containerExists -eq "tax-incentive-db") {
    docker start tax-incentive-db | Out-Null
    Write-Host "✓ PostgreSQL container started" -ForegroundColor Green
} else {
    docker-compose up -d | Out-Null
    Write-Host "✓ PostgreSQL created and started" -ForegroundColor Green
}

# Wait for PostgreSQL to be ready
Write-Host "  Waiting for PostgreSQL to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

$ready = docker exec tax-incentive-db pg_isready -U postgres 2>&1
if ($ready -like "*accepting connections*") {
    Write-Host "✓ PostgreSQL is ready" -ForegroundColor Green
} else {
    Write-Host "✗ PostgreSQL connection failed" -ForegroundColor Red
    Write-Host "  Check Docker logs: docker logs tax-incentive-db" -ForegroundColor Yellow
}
Write-Host ""

# Step 4: Activate Virtual Environment
Write-Host "Activating Python virtual environment..." -ForegroundColor Yellow
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment not found" -ForegroundColor Red
    Write-Host "  Run: python -m venv venv" -ForegroundColor Yellow
    pause
    exit
}
Write-Host ""

# Step 5: Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version
Write-Host "  $pythonVersion" -ForegroundColor Cyan
if ($pythonVersion -like "*3.12*") {
    Write-Host "✓ Python 3.12 confirmed" -ForegroundColor Green
} else {
    Write-Host "⚠ Warning: Python 3.12 recommended" -ForegroundColor Yellow
}
Write-Host ""

# Step 6: Quick dependency check
Write-Host "Checking key dependencies..." -ForegroundColor Yellow
$hasUvicorn = pip list 2>&1 | Select-String "uvicorn"
$hasPrisma = pip list 2>&1 | Select-String "prisma"
if ($hasUvicorn -and $hasPrisma) {
    Write-Host "✓ Key dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠ Some dependencies missing - installing..." -ForegroundColor Yellow
    pip install -r requirements.txt -q
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
}
Write-Host ""

# Step 7: Start API Server
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting API Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server will start at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Health Check: http://localhost:8000/health" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start server
python -m uvicorn src.main:app --reload
