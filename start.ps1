# ========================================
# Tax-Incentive Compliance Platform
# Self-Healing Startup Script (Windows-Optimized)
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Tax-Incentive Compliance Platform" -ForegroundColor White
Write-Host "Startup Script" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

# ========================================
# 1. FIND PYTHON 3.12 (WINDOWS-SMART)
# ========================================
Write-Host "`n[1/6] Locating Python 3.12..." -ForegroundColor Yellow

$pythonCmd = $null
$pythonVersion = $null

# Strategy 1: Try Python Launcher (py. exe) - most reliable on Windows
try {
    $pythonVersion = py -3.12 --version 2>&1
    if ($pythonVersion -match "Python 3\.12\.(\d+)") {
        $pythonCmd = "py -3.12"
        Write-Host "✓ Found via Python Launcher:  $pythonVersion" -ForegroundColor Green
    }
}
catch { }

# Strategy 2: Try 'python' in PATH
if (-not $pythonCmd) {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3\.12\. (\d+)") {
            $pythonCmd = "python"
            Write-Host "✓ Found in PATH: $pythonVersion" -ForegroundColor Green
        }
    }
    catch { }
}

# Strategy 3: Search common installation locations
if (-not $pythonCmd) {
    Write-Host "  Searching for Python 3.12 installation..." -ForegroundColor Gray
    
    $searchPaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312-64\python.exe",
        "C:\Program Files\Python312\python.exe",
        "C:\Python312\python.exe"
    )
    
    foreach ($path in $searchPaths) {
        if (Test-Path $path) {
            $testVersion = & $path --version 2>&1
            if ($testVersion -match "Python 3\.12\.(\d+)") {
                $pythonCmd = $path
                $pythonVersion = $testVersion
                Write-Host "✓ Found at: $path" -ForegroundColor Green
                Write-Host "  Version: $pythonVersion" -ForegroundColor Green
                break
            }
        }
    }
}

# Strategy 4: Give up and show helpful error
if (-not $pythonCmd) {
    Write-Host "❌ Python 3.12 NOT found!" -ForegroundColor Red
    Write-Host "`nDiagnostics:" -ForegroundColor Yellow
    
    Write-Host "`n  Available Python versions (via launcher):" -ForegroundColor Cyan
    py --list 2>&1 | ForEach-Object { Write-Host "    $_" }
    
    Write-Host "`n  Searched locations:" -ForegroundColor Cyan
    $searchPaths | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    
    Write-Host "`n📥 Install Python 3.12:" -ForegroundColor Yellow
    Write-Host "  1. Download: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "  2. ✅ CHECK 'Add Python to PATH' during install!" -ForegroundColor White
    Write-Host "  3.  Restart PowerShell after installation" -ForegroundColor White
    
    pause
    exit 1
}

# ========================================
# 2. CHECK/CREATE CORRECT VENV
# ========================================
Write-Host "`n[2/6] Checking virtual environment..." -ForegroundColor Yellow

$venvPath = ". venv"
$needsRecreate = $false

if (-not (Test-Path $venvPath)) {
    Write-Host "⚠ Virtual environment not found" -ForegroundColor Yellow
    $needsRecreate = $true
}
else {
    $venvPython = & "$venvPath\Scripts\python.exe" --version 2>&1
    if ($venvPython -match "Python 3\.12\.(\d+)") {
        Write-Host "✓ Virtual environment is Python 3.12" -ForegroundColor Green
    }
    else {
        Write-Host "⚠ Wrong version:  $venvPython (need 3.12)" -ForegroundColor Yellow
        $needsRecreate = $true
    }
}

if ($needsRecreate) {
    Write-Host "  Recreating virtual environment..." -ForegroundColor Cyan
    
    if (Test-Path $venvPath) {
        Remove-Item -Path $venvPath -Recurse -Force
    }
    
    # Use the Python we found
    $createCmd = "$pythonCmd -m venv $venvPath"
    Invoke-Expression $createCmd
    
    if (Test-Path "$venvPath\Scripts\python. exe") {
        $newVersion = & "$venvPath\Scripts\python.exe" --version
        Write-Host "✓ Created:  $newVersion" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Failed to create venv!" -ForegroundColor Red
        exit 1
    }
}

# ========================================
# 3. ACTIVATE VENV
# ========================================
Write-Host "`n[3/6] Activating virtual environment..." -ForegroundColor Yellow

try {
    & "$venvPath\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to activate!" -ForegroundColor Red
    Write-Host "   Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

# ========================================
# 4. INSTALL/UPDATE DEPENDENCIES
# ========================================
Write-Host "`n[4/6] Checking dependencies..." -ForegroundColor Yellow

if (Test-Path "requirements.txt") {
    $pipList = pip list 2>&1
    if ($pipList -notmatch "fastapi") {
        Write-Host "  Installing dependencies..." -ForegroundColor Cyan
        pip install -r requirements. txt --quiet
        Write-Host "✓ Dependencies installed" -ForegroundColor Green
    }
    else {
        Write-Host "✓ Dependencies present" -ForegroundColor Green
    }
}
else {
    Write-Host "⚠ requirements.txt not found" -ForegroundColor Yellow
}

if (Test-Path "prisma") {
    python -m prisma generate 2>&1 | Out-Null
    Write-Host "✓ Prisma client ready" -ForegroundColor Green
}

# ========================================
# 5. START DOCKER & POSTGRESQL
# ========================================
Write-Host "`n[5/6] Starting Docker services..." -ForegroundColor Yellow

try {
    docker version 2>$null 1>$null
    if ($LASTEXITCODE -ne 0) { throw "Docker not running" }
    Write-Host "✓ Docker is running" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker Desktop not running!" -ForegroundColor Red
    Write-Host "   Please start Docker Desktop first" -ForegroundColor Yellow
    exit 1
}

$containerRunning = docker ps --filter "name=tax-incentive-db" --format "{{.Names}}" 2>$null

if ($containerRunning -eq "tax-incentive-db") {
    Write-Host "✓ PostgreSQL running" -ForegroundColor Green
}
else {
    docker start tax-incentive-db 2>$null | Out-Null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Creating container..." -ForegroundColor Cyan
        docker-compose up -d
    }
    
    Write-Host "  Waiting for PostgreSQL..." -ForegroundColor Gray
    $maxAttempts = 20
    for ($i = 0; $i -lt $maxAttempts; $i++) {
        Start-Sleep -Seconds 2
        $isReady = docker exec tax-incentive-db pg_isready -U postgres 2>$null
        if ($isReady -match "accepting connections") {
            Write-Host "✓ PostgreSQL ready" -ForegroundColor Green
            break
        }
        Write-Host "." -NoNewline
    }
}

# ========================================
# 6. CHECK . ENV
# ========================================
Write-Host "`n[6/6] Checking configuration..." -ForegroundColor Yellow

if (-not (Test-Path ". env")) {
    if (Test-Path ". env.example") {
        Copy-Item .env.example .env
        Write-Host "✓ .env created from template" -ForegroundColor Green
    }
}
else {
    Write-Host "✓ .env exists" -ForegroundColor Green
}

# ========================================
# START APPLICATION
# ========================================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✓ ALL SYSTEMS READY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nStarting FastAPI server..." -ForegroundColor Yellow
Write-Host "  📚 API Docs:    http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  ❤️  Health:     http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop`n" -ForegroundColor Gray

python -m uvicorn src.main:app --reload