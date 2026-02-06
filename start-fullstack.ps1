# ============================================
# PilotForge Full Stack Startup Script (Windows)
# Starts both Backend and Frontend
# ============================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🎬 PilotForge Full Stack Startup" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Cyan

# Check if we're in the project root
if (-not (Test-Path "frontend") -or -not (Test-Path "main.py")) {
    Write-Host "❌ Error: This script must be run from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "`n📋 Pre-flight Checks" -ForegroundColor Yellow
Write-Host "======================================" -ForegroundColor Cyan


# Kill existing processes on ports 5173 and 8000
Write-Host "Checking for existing processes on ports 5173 and 8000..." -ForegroundColor Gray
foreach ($port in @(5173, 8000)) {
    $conns = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($conns) {
        foreach ($conn in $conns) {
            Write-Host "Killing process on port $port (PID: $($conn.OwningProcess))..." -ForegroundColor Yellow
            Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
        }
    }
}

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion detected" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js $nodeVersion detected" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found - install from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check virtual environment
if (-not (Test-Path ".venv") -and -not (Test-Path "venv")) {
    Write-Host "⚠️  Warning: No Python virtual environment found" -ForegroundColor Yellow
    Write-Host "   Create one with: python -m venv .venv" -ForegroundColor Gray
    Write-Host "   Then activate it and install dependencies" -ForegroundColor Gray
}

# Check frontend dependencies
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "`n📦 Installing frontend dependencies..." -ForegroundColor Yellow
    Push-Location frontend
    npm install
    Pop-Location
    Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
}

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "🚀 Starting Servers" -ForegroundColor White
Write-Host "======================================" -ForegroundColor Cyan

# Activate virtual environment if it exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
} elseif (Test-Path "venv\Scripts\Activate.ps1") {
    . .\venv\Scripts\Activate.ps1
}

# Start backend in a new PowerShell window
Write-Host "`nStarting backend on http://localhost:8000..." -ForegroundColor Yellow
$backendScript = @"
if (Test-Path ".venv\Scripts\Activate.ps1") { . .\.venv\Scripts\Activate.ps1 }
python -m uvicorn src.main:app --reload --port 8000
"@
$backendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript -PassThru
Write-Host "✓ Backend started (PID: $($backendProcess.Id))" -ForegroundColor Green

# Wait for backend to be ready
Write-Host "  Waiting for backend to be ready..." -ForegroundColor Gray
for ($i = 1; $i -le 30; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 1 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "✓ Backend is ready!" -ForegroundColor Green
            break
        }
    } catch {
        # Backend not ready yet
    }
    
    if ($i -eq 30) {
        Write-Host "⚠️  Backend is taking longer than expected to start" -ForegroundColor Yellow
        Write-Host "   Check the backend window for errors" -ForegroundColor Gray
    }
    Start-Sleep -Seconds 1
}

# Start frontend in a new PowerShell window
Write-Host "`nStarting frontend on http://localhost:5173..." -ForegroundColor Yellow
$frontendScript = @"
Set-Location frontend
npm run dev
"@
$frontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript -PassThru
Write-Host "✓ Frontend started (PID: $($frontendProcess.Id))" -ForegroundColor Green

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "✅ Both Servers Running!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "`n📍 URLs:" -ForegroundColor White
Write-Host "  Frontend:  http://localhost:5173" -ForegroundColor Cyan
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`n💡 Tips:" -ForegroundColor White
Write-Host "  - Each server is running in its own window" -ForegroundColor Gray
Write-Host "  - Close the windows or press Ctrl+C in them to stop" -ForegroundColor Gray
Write-Host "  - Backend PID: $($backendProcess.Id)" -ForegroundColor Gray
Write-Host "  - Frontend PID: $($frontendProcess.Id)" -ForegroundColor Gray
Write-Host "`nPress any key to exit this window..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")




