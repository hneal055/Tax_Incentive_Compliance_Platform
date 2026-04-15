param(
  [switch]$Status,
  [switch]$Logs,
  [string]$Service = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

# ── Status-only mode ──────────────────────────────────────────────────────────
if ($Status) {
  Write-Host "`n=== SceneIQ Service Status ===" -ForegroundColor Cyan
  docker ps --filter "name=pilotforge" --format "table {{.Names}}`t{{.Status}}`t{{.Ports}}"
  exit 0
}

# ── Log tail mode ─────────────────────────────────────────────────────────────
if ($Logs) {
  $target = if ($Service) { $Service } else { "backend" }
  Write-Host "=== Tailing logs: $target ===" -ForegroundColor Cyan
  docker compose logs -f $target
  exit 0
}

# ── Normal startup ────────────────────────────────────────────────────────────
Write-Host "`n=== SceneIQ Daily Startup ===" -ForegroundColor Cyan
Write-Host "Working directory: $Root" -ForegroundColor Gray

# 1. Verify .env has ANTHROPIC_API_KEY
if (!(Test-Path "$Root\.env") -or !(Select-String -Path "$Root\.env" -Pattern "ANTHROPIC_API_KEY=sk-" -Quiet)) {
  Write-Host "[WARN] .env missing or ANTHROPIC_API_KEY not set — AI Advisor will use scripted responses only" -ForegroundColor Yellow
}

# 2. Start all services
Write-Host "`n[1/3] Starting Docker services..." -ForegroundColor Green
docker compose up -d

# 3. Wait for backend health
Write-Host "[2/3] Waiting for backend to be healthy..." -ForegroundColor Green
$attempts = 0
do {
  Start-Sleep -Seconds 3
  $attempts++
  $health = docker inspect --format "{{.State.Health.Status}}" pilotforge-api 2>$null
  Write-Host "      pilotforge-api: $health ($attempts/10)" -ForegroundColor Gray
} while ($health -ne "healthy" -and $attempts -lt 10)

if ($health -ne "healthy") {
  Write-Host "[WARN] Backend not healthy after 30s — check logs: docker compose logs backend" -ForegroundColor Yellow
}

# 4. Summary
Write-Host "`n[3/3] Status:" -ForegroundColor Green
docker ps --filter "name=pilotforge" --format "table {{.Names}}`t{{.Status}}"

Write-Host "`n=== Ready ===" -ForegroundColor Cyan
Write-Host "  App:      http://localhost" -ForegroundColor White
Write-Host "  API docs: http://localhost:8001/api/0.1.0/docs" -ForegroundColor White
Write-Host "  Login:    admin@pilotforge.com / pilotforge2024" -ForegroundColor White
Write-Host ""
