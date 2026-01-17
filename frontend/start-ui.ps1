# ============================================
# PilotForge Frontend Startup Script (Windows)
# ============================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🎬 PilotForge Frontend Startup" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Cyan

# Check if we're in the frontend directory
if (-not (Test-Path "package.json")) {
    Write-Host "❌ Error: This script must be run from the frontend directory" -ForegroundColor Red
    Write-Host "   Run: cd frontend; .\start-ui.ps1" -ForegroundColor Yellow
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Node.js $nodeVersion detected" -ForegroundColor Green
        
        # Extract major version number
        $majorVersion = [int]($nodeVersion -replace 'v(\d+)\..*', '$1')
        if ($majorVersion -lt 20) {
            Write-Host "⚠️  Warning: Node.js 20+ recommended, found $nodeVersion" -ForegroundColor Yellow
        }
    } else {
        throw "Node.js not found"
    }
} catch {
    Write-Host "❌ Error: Node.js is not installed" -ForegroundColor Red
    Write-Host "   Please install Node.js 20+ from https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check if npm is installed
try {
    $npmVersion = npm --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ npm $npmVersion detected" -ForegroundColor Green
    } else {
        throw "npm not found"
    }
} catch {
    Write-Host "❌ Error: npm is not installed" -ForegroundColor Red
    exit 1
}

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "`n📦 Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✓ Dependencies already installed" -ForegroundColor Green
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "`nℹ️  Note: No .env file found (optional)" -ForegroundColor Cyan
    Write-Host "   Using default configuration: API at http://localhost:8000" -ForegroundColor Gray
    Write-Host "   To customize, run: Copy-Item .env.example .env" -ForegroundColor Gray
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "🚀 Starting Development Server..." -ForegroundColor White
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "`nFrontend will be available at:" -ForegroundColor White
Write-Host "  → http://localhost:3000" -ForegroundColor Cyan
Write-Host "`nMake sure the backend is running at:" -ForegroundColor White
Write-Host "  → http://localhost:8000" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow

# Start the development server
try {
    npm run dev
} catch {
    Write-Host "`n❌ Failed to start development server: $_" -ForegroundColor Red
    exit 1
}
