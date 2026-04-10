# PilotForge Demo — One-command launcher (Windows)
# Usage: Right-click → Run with PowerShell  OR  .\start.ps1 in a terminal

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  PilotForge  —  Tax Incentive Intelligence" -ForegroundColor White
Write-Host "  Demo Environment" -ForegroundColor DarkGray
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# ── Guard: Docker must be running ────────────────────────────────────────────
try {
    docker info 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "  [1/4] Docker is running." -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "  ERROR: Docker Desktop is not running." -ForegroundColor Red
    Write-Host "  Please open Docker Desktop and wait for it to finish starting." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "  Press Enter to exit"
    exit 1
}

# ── Pull latest images ────────────────────────────────────────────────────────
Write-Host "  [2/4] Pulling latest images from Docker Hub..." -ForegroundColor White
Set-Location $PSScriptRoot
docker compose pull 2>&1 | ForEach-Object { Write-Host "         $_" -ForegroundColor DarkGray }
Write-Host "  [2/4] Images ready." -ForegroundColor Green

# ── Start all services ────────────────────────────────────────────────────────
Write-Host "  [3/4] Starting services..." -ForegroundColor White
docker compose up -d 2>&1 | ForEach-Object { Write-Host "         $_" -ForegroundColor DarkGray }

# ── Wait for backend to be healthy ───────────────────────────────────────────
Write-Host "  [4/4] Waiting for platform to be ready (up to 90s)..." -ForegroundColor White
$waited = 0
do {
    Start-Sleep -Seconds 3
    $waited += 3
    $health = docker inspect --format "{{.State.Health.Status}}" pilotforge-demo-api 2>$null
} while ($health -ne "healthy" -and $waited -lt 90)

Write-Host ""
if ($health -eq "healthy") {
    Write-Host "  All services are healthy." -ForegroundColor Green
} else {
    Write-Host "  Services are still starting — the dashboard may take a few more seconds." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "  ┌─────────────────────────────────────────┐" -ForegroundColor Cyan
Write-Host "  │  Dashboard : http://localhost:3000       │" -ForegroundColor Cyan
Write-Host "  │  Login     : admin@pilotforge.com        │" -ForegroundColor Cyan
Write-Host "  │  Password  : pilotforge2024              │" -ForegroundColor Cyan
Write-Host "  └─────────────────────────────────────────┘" -ForegroundColor Cyan
Write-Host ""

Start-Process "http://localhost:3000"
