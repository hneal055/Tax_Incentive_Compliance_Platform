# SceneIQ Demo — Stop all services
# Usage: .\stop.ps1

Set-Location $PSScriptRoot
Write-Host ""
Write-Host "  Stopping SceneIQ demo..." -ForegroundColor Yellow
docker compose down
Write-Host "  Done. Data is preserved — run start.ps1 to resume." -ForegroundColor Green
Write-Host ""
