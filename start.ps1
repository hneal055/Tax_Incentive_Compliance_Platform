# PilotForge — One-command startup
# Usage:  .\start.ps1
# Opens http://localhost:3000 automatically after services are healthy.

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PilotForge  —  Tax Incentive Platform" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ── Guard: Docker must be running ────────────────────────────────────────────
try {
    docker info 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "  [1/3] Docker is running." -ForegroundColor Green
} catch {
    Write-Host "  Docker Desktop is not running. Please start it first." -ForegroundColor Red
    exit 1
}

# ── Remove orphaned containers (not part of this project) ────────────────────
$all = docker ps -q 2>$null
if ($all) {
    foreach ($id in $all) {
        $cname = docker inspect --format "{{.Name}}" $id 2>$null
        if ($cname -notmatch "pilotforge") {
            Write-Host "  Removing orphaned container: $cname" -ForegroundColor Yellow
            docker rm -f $id | Out-Null
        }
    }
}

# ── Start all services ────────────────────────────────────────────────────────
Write-Host "  [2/3] Starting containers..." -ForegroundColor White
Set-Location $PSScriptRoot
docker compose up -d 2>&1 | ForEach-Object { Write-Host "         $_" -ForegroundColor DarkGray }

# ── Wait for backend healthy ──────────────────────────────────────────────────
Write-Host "  [3/3] Waiting for backend..." -ForegroundColor White
$waited = 0
do {
    Start-Sleep -Seconds 2
    $waited += 2
    $health = docker inspect --format "{{.State.Health.Status}}" pilotforge-api 2>$null
} while ($health -ne "healthy" -and $waited -lt 40)

Write-Host ""
if ($health -eq "healthy") {
    Write-Host "  All services healthy." -ForegroundColor Green
} else {
    Write-Host "  Services starting (may need a moment to finish seeding)." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "  Dashboard : http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Login     : admin@pilotforge.com  /  pilotforge2024" -ForegroundColor Cyan
Write-Host "  API docs  : http://localhost:8001/docs" -ForegroundColor DarkGray
Write-Host ""

Start-Process "http://localhost:3000"
