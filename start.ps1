# ========================================
# Tax Incentive Compliance Platform
# Bulletproof Windows Startup Script
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Tax Incentive Compliance Platform" -ForegroundColor White
Write-Host "Automated Startup Script" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ========================================
# STEP 1: Find Python 3.12
# ========================================
Write-Host "[ STEP 1/7 ] Finding Python 3.12..." -ForegroundColor Cyan
$pythonCmd = $null
$pythonVersion = $null

# Strategy 1: Try Windows Python Launcher
Write-Host "  Trying: py -3.12" -ForegroundColor Gray
try {
    $version = & py -3.12 --version 2>&1
    if ($LASTEXITCODE -eq 0 -and $version -match "3\.12") {
        $pythonCmd = "py -3.12"
        $pythonVersion = $version
        Write-Host "  ✓ Found via Python Launcher: $version" -ForegroundColor Green
    }
} catch {}

# Strategy 2: Try 'python' in PATH
if (-not $pythonCmd) {
    Write-Host "  Trying: python" -ForegroundColor Gray
    try {
        $version = & python --version 2>&1
        if ($LASTEXITCODE -eq 0 -and $version -match "3\.12") {
            $pythonCmd = "python"
            $pythonVersion = $version
            Write-Host "  ✓ Found in PATH: $version" -ForegroundColor Green
        }
    } catch {}
}

# Strategy 3: Search common Windows installation paths
if (-not $pythonCmd) {
    Write-Host "  Searching common installation paths..." -ForegroundColor Gray
    $searchPaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312-64\python.exe",
        "C:\Program Files\Python312\python.exe",
        "C:\Python312\python.exe"
    )
    
    foreach ($path in $searchPaths) {
        if (Test-Path $path) {
            try {
                $version = & $path --version 2>&1
                if ($LASTEXITCODE -eq 0 -and $version -match "3\.12") {
                    $pythonCmd = $path
                    $pythonVersion = $version
                    Write-Host "  ✓ Found at: $path" -ForegroundColor Green
                    Write-Host "    Version: $version" -ForegroundColor Green
                    break
                }
            } catch {}
        }
    }
}

# Python not found - show diagnostics and exit
if (-not $pythonCmd) {
    Write-Host ""
    Write-Host "❌ Python 3.12 not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Diagnostics:" -ForegroundColor Yellow
    Write-Host "  Searched paths:" -ForegroundColor Yellow
    foreach ($path in $searchPaths) {
        $exists = Test-Path $path
        if ($exists) {
            Write-Host "    ✓ $path (found but wrong version)" -ForegroundColor Yellow
        } else {
            Write-Host "    ✗ $path" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    Write-Host "  Available Python versions:" -ForegroundColor Yellow
    try {
        & py --list 2>&1 | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    } catch {
        Write-Host "    (Python Launcher not available)" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "Solution:" -ForegroundColor Cyan
    Write-Host "  1. Download Python 3.12 from: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "  2. During installation, CHECK ✓ 'Add Python to PATH'" -ForegroundColor White
    Write-Host "  3. Run this script again: .\start.ps1" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✓ Python 3.12 ready: $pythonCmd" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 2: Virtual Environment
# ========================================
Write-Host "[ STEP 2/7 ] Checking virtual environment..." -ForegroundColor Cyan
$venvPython = ".\.venv\Scripts\python.exe"
$needsRecreate = $false

if (Test-Path ".venv") {
    Write-Host "  Virtual environment exists, checking version..." -ForegroundColor Gray
    try {
        $venvVersion = & $venvPython --version 2>&1
        if ($LASTEXITCODE -eq 0 -and $venvVersion -match "3\.12") {
            Write-Host "  ✓ Using existing .venv with $venvVersion" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ Virtual environment has wrong version: $venvVersion" -ForegroundColor Yellow
            Write-Host "    Recreating with Python 3.12..." -ForegroundColor Yellow
            $needsRecreate = $true
        }
    } catch {
        Write-Host "  ⚠ Virtual environment is corrupted" -ForegroundColor Yellow
        Write-Host "    Recreating..." -ForegroundColor Yellow
        $needsRecreate = $true
    }
} else {
    Write-Host "  Virtual environment not found, creating..." -ForegroundColor Yellow
    $needsRecreate = $true
}

if ($needsRecreate) {
    # Remove old venv if it exists
    if (Test-Path ".venv") {
        Write-Host "  Removing old .venv..." -ForegroundColor Gray
        Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
    }
    
    # Create new venv
    Write-Host "  Creating new virtual environment..." -ForegroundColor Gray
    try {
        if ($pythonCmd -eq "py -3.12") {
            & py -3.12 -m venv .venv
        } else {
            & $pythonCmd -m venv .venv
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
        } else {
            Write-Host "  ❌ Failed to create virtual environment" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "  ❌ Error creating virtual environment: $_" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ Virtual environment ready" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 3: Dependencies
# ========================================
Write-Host "[ STEP 3/7 ] Checking dependencies..." -ForegroundColor Cyan
$needsInstall = $false

# Quick check: is fastapi installed?
try {
    $fastapiCheck = & $venvPython -m pip show fastapi 2>&1
    if ($LASTEXITCODE -ne 0 -or -not $fastapiCheck) {
        Write-Host "  Dependencies not installed" -ForegroundColor Yellow
        $needsInstall = $true
    } else {
        Write-Host "  ✓ Core dependencies installed" -ForegroundColor Green
    }
} catch {
    Write-Host "  Dependencies not installed" -ForegroundColor Yellow
    $needsInstall = $true
}

if ($needsInstall) {
    Write-Host "  Installing from requirements.txt..." -ForegroundColor Yellow
    try {
        & $venvPython -m pip install -q -r requirements.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ Some dependencies may have failed to install" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ⚠ Error installing dependencies: $_" -ForegroundColor Yellow
    }
}

# Run prisma generate if prisma directory exists
if (Test-Path "prisma") {
    Write-Host "  Running prisma generate..." -ForegroundColor Gray
    try {
        & $venvPython -m prisma generate 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Prisma client generated" -ForegroundColor Green
        }
    } catch {
        Write-Host "  ⚠ Prisma generate skipped" -ForegroundColor Gray
    }
}

Write-Host "✓ Dependencies ready" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 4: Configuration
# ========================================
Write-Host "[ STEP 4/7 ] Checking configuration..." -ForegroundColor Cyan

if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "  Creating .env from .env.example..." -ForegroundColor Yellow
        Copy-Item .env.example .env
        Write-Host "  ✓ .env file created" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ No .env or .env.example found" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✓ .env file exists" -ForegroundColor Green
}

Write-Host "✓ Configuration ready" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 5: Docker Desktop
# ========================================
Write-Host "[ STEP 5/7 ] Checking Docker Desktop..." -ForegroundColor Cyan

try {
    & docker version 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Docker Desktop is running" -ForegroundColor Green
    } else {
        throw "Docker not accessible"
    }
} catch {
    Write-Host "  ❌ Docker Desktop is not running" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Please start Docker Desktop and run this script again." -ForegroundColor Yellow
    Write-Host "  You can verify Docker with: docker version" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

Write-Host "✓ Docker Desktop ready" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 6: PostgreSQL Container
# ========================================
Write-Host "[ STEP 6/7 ] Checking PostgreSQL..." -ForegroundColor Cyan

# Check if container is running
$containerRunning = & docker ps --filter "name=tax-incentive-db" --format "{{.Names}}" 2>&1

if ($containerRunning -eq "tax-incentive-db") {
    Write-Host "  ✓ Container 'tax-incentive-db' is running" -ForegroundColor Green
} else {
    # Try to start existing container
    Write-Host "  Starting PostgreSQL container..." -ForegroundColor Yellow
    $containerExists = & docker ps -a --filter "name=tax-incentive-db" --format "{{.Names}}" 2>&1
    
    if ($containerExists -eq "tax-incentive-db") {
        & docker start tax-incentive-db 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Started existing container" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ Could not start existing container, creating new one..." -ForegroundColor Yellow
            & docker rm tax-incentive-db 2>&1 | Out-Null
            & docker-compose up -d 2>&1 | Out-Null
        }
    } else {
        # Create via docker-compose
        Write-Host "  Creating new PostgreSQL container..." -ForegroundColor Yellow
        & docker-compose up -d 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Container created" -ForegroundColor Green
        } else {
            Write-Host "  ❌ Failed to create container" -ForegroundColor Red
            exit 1
        }
    }
}

# Wait for PostgreSQL to be ready
Write-Host "  Waiting for PostgreSQL to accept connections..." -ForegroundColor Gray
$maxAttempts = 20
$attempt = 0
$ready = $false

while ($attempt -lt $maxAttempts) {
    $attempt++
    try {
        $checkResult = & docker exec tax-incentive-db pg_isready -U postgres 2>&1
        if ($checkResult -match "accepting connections") {
            $ready = $true
            break
        }
    } catch {}
    
    Write-Host "." -NoNewline -ForegroundColor Gray
    Start-Sleep -Seconds 2
}

Write-Host ""
if ($ready) {
    Write-Host "  ✓ PostgreSQL is ready" -ForegroundColor Green
} else {
    Write-Host "  ⚠ PostgreSQL may not be ready (timeout)" -ForegroundColor Yellow
    Write-Host "    Continuing anyway..." -ForegroundColor Gray
}

Write-Host "✓ PostgreSQL ready" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 7: Launch Server
# ========================================
Write-Host "[ STEP 7/7 ] Starting API server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "         ALL SYSTEMS READY ✓" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  📡 Server:       http://localhost:8000" -ForegroundColor White
Write-Host "  📚 API Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host "  ❤️  Health Check: http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start the server
try {
    & $venvPython -m uvicorn src.main:app --reload
} catch {
    Write-Host ""
    Write-Host "❌ Server stopped or failed to start" -ForegroundColor Red
    exit 1
}
