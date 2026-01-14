# ========================================
# Tax-Incentive Compliance Platform
# Daily Startup Script - Updated for Python 3.12
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Tax-Incentive Compliance Platform" -ForegroundColor White
Write-Host "Daily Startup Script" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

# Check if we're in the project directory
$projectDir = "C:\Projects\Tax_Incentive_Compliance_Platform"
if ((Get-Location).Path -ne $projectDir) {
    Write-Host "⚠ Not in project directory, changing..." -ForegroundColor Yellow
    Set-Location $projectDir
}

Write-Host "✓ In project directory: $(Get-Location)" -ForegroundColor Green

# Check Docker Desktop - FIXED VERSION
Write-Host "`nChecking Docker Desktop..." -ForegroundColor Yellow
try {
    # Try to run a simple docker command
    docker version 2>$null 1>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Docker Desktop is running" -ForegroundColor Green
    } else {
        throw "Docker command failed"
    }
} catch {
    Write-Host "❌ Docker Desktop is not running or not accessible" -ForegroundColor Red
    Write-Host "   Please start Docker Desktop and try again." -ForegroundColor Yellow
    Write-Host "   If Docker is running, check: docker version" -ForegroundColor Yellow
    exit 1
}

# Start PostgreSQL if not running
Write-Host "`nStarting PostgreSQL..." -ForegroundColor Yellow
try {
    $postgresContainer = docker ps --filter "name=tax-incentive-db" --format "{{.Names}}" 2>$null
    if (-not $postgresContainer) {
        Write-Host "Starting PostgreSQL container..." -ForegroundColor Yellow
        docker start tax-incentive-db 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Creating new PostgreSQL container..." -ForegroundColor Yellow
            docker run -d --name tax-incentive-db -p 5432:5432 `
              -e POSTGRES_PASSWORD=postgres `
              -e POSTGRES_DB=tax_incentive_db `
              -v postgres-tax-data:/var/lib/postgresql/data `
              postgres:16-alpine 2>$null
        }
        
        # Wait for PostgreSQL to be ready
        Write-Host "  Waiting for PostgreSQL to be ready..." -ForegroundColor Gray
        $maxAttempts = 30
        $attempt = 0
        do {
            $attempt++
            $isReady = docker exec tax-incentive-db pg_isready -U postgres 2>$null
            if ($isReady -match "accepting connections") {
                Write-Host "✓ PostgreSQL is ready" -ForegroundColor Green
                break
            }
            Write-Host "." -NoNewline
            Start-Sleep -Seconds 2
        } while ($attempt -lt $maxAttempts)
        
        if ($attempt -ge $maxAttempts) {
            Write-Host "`n❌ PostgreSQL failed to start in time" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "✓ PostgreSQL container already running" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error managing PostgreSQL: $_" -ForegroundColor Red
    exit 1
}

# Activate Python virtual environment with Python 3.12
Write-Host "`nActivating Python virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    Write-Host "Creating new virtual environment with Python 3.12..." -ForegroundColor Yellow
    py -3.12 -m venv .venv
}

# Activate the virtual environment
try {
    .\.venv\Scripts\activate
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to activate virtual environment: $_" -ForegroundColor Red
    exit 1
}

# Check Python version
Write-Host "`nChecking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  $pythonVersion" -ForegroundColor White
    if ($pythonVersion -notmatch "3\.12") {
        Write-Host "⚠ Warning: Python 3.12 recommended, but found $pythonVersion" -ForegroundColor Yellow
        Write-Host "  Attempting to use Python 3.12 anyway..." -ForegroundColor Yellow
    } else {
        Write-Host "✓ Python 3.12 confirmed" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Could not determine Python version: $_" -ForegroundColor Red
}

# Check key dependencies
Write-Host "`nChecking key dependencies..." -ForegroundColor Yellow
$requiredPackages = @(
    "fastapi",
    "uvicorn",
    "psycopg2-binary",
    "python-multipart"
)

foreach ($package in $requiredPackages) {
    try {
        $installed = pip show $package 2>$null
        if ($installed) {
            Write-Host "✓ $package is installed" -ForegroundColor Green
        } else {
            Write-Host "Installing $package..." -ForegroundColor Yellow
            pip install $package --quiet 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ $package installed" -ForegroundColor Green
            } else {
                Write-Host "⚠ Could not install $package" -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "⚠ Error checking $package: $_" -ForegroundColor Yellow
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Starting API Server..." -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nServer will start at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Health Check: http://localhost:8000/health" -ForegroundColor Cyan

Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow

# Start the server
try {
    python main.py
} catch {
    Write-Host "❌ Failed to start server: $_" -ForegroundColor Red
    exit 1
}
