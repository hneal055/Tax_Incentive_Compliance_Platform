# SceneIQ — One-command startup
# Usage:  .\start.ps1
# Works on any machine — pulls images from Docker Hub if not present locally.
# Opens http://localhost:3000 automatically once all services are healthy.

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SceneIQ  —  Tax Incentive Platform" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ── [1] Guard: Docker must be running ────────────────────────────────────────
try {
    docker info 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "  [1/4] Docker is running." -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Docker Desktop is not running. Please start it first." -ForegroundColor Red
    exit 1
}

# ── [2] Pull images if not present locally ───────────────────────────────────
$backendExists  = docker image inspect hneal1038/pilotforge-backend:latest  2>$null
$frontendExists = docker image inspect hneal1038/pilotforge-frontend:latest 2>$null

if (-not $backendExists -or -not $frontendExists) {
    Write-Host "  [2/4] Images not found locally — pulling from Docker Hub..." -ForegroundColor Yellow
    Set-Location $PSScriptRoot
    docker compose pull
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Pull failed. Check your internet connection or run: docker login" -ForegroundColor Red
        exit 1
    }
    Write-Host "  [2/4] Images ready." -ForegroundColor Green
} else {
    Write-Host "  [2/4] Images already present — skipping pull." -ForegroundColor Green
}

# ── [3] Remove orphaned containers (not part of this project) ────────────────
$running = docker ps -q 2>$null
if ($running) {
    foreach ($id in $running) {
        $cname = docker inspect --format "{{.Name}}" $id 2>$null
        if ($cname -notmatch "pilotforge") {
            Write-Host "  Removing orphaned container: $cname" -ForegroundColor Yellow
            docker rm -f $id | Out-Null
        }
    }
}

# ── [4] Start all services ────────────────────────────────────────────────────
Write-Host "  [3/4] Starting containers..." -ForegroundColor White
Set-Location $PSScriptRoot
docker compose up -d 2>&1 | ForEach-Object { Write-Host "         $_" -ForegroundColor DarkGray }

# ── Wait for backend to be healthy ───────────────────────────────────────────
Write-Host "  [4/4] Waiting for backend to be ready..." -ForegroundColor White
$waited = 0
do {
    Start-Sleep -Seconds 2
    $waited += 2
    $health = docker inspect --format "{{.State.Health.Status}}" pilotforge-api 2>$null
} while ($health -ne "healthy" -and $waited -lt 60)

Write-Host ""
if ($health -eq "healthy") {
    Write-Host "  All services healthy." -ForegroundColor Green
} else {
    Write-Host "  Still starting up — dashboard may take a few more seconds." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "  Dashboard : http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Login     : admin@pilotforge.com  /  pilotforge2024" -ForegroundColor Cyan
Write-Host "  API docs  : http://localhost:8001/docs" -ForegroundColor DarkGray
Write-Host ""

Start-Process "http://localhost:3000"
