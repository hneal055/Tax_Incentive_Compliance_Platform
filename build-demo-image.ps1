# Build and push the PilotForge demo frontend image.
# Run this ONCE from the project root before distributing the demo folder.
# Requires: docker login hneal1038 (or your Docker Hub credentials)

Write-Host ""
Write-Host "  Building pilotforge-frontend:demo ..." -ForegroundColor Cyan
Write-Host "  (VITE_API_URL='' — frontend calls local backend via nginx proxy)" -ForegroundColor DarkGray
Write-Host ""

Set-Location $PSScriptRoot

docker build `
  --build-arg VITE_API_URL="" `
  -t hneal1038/pilotforge-frontend:demo `
  ./frontend

if ($LASTEXITCODE -ne 0) {
    Write-Host "  Build failed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "  Pushing hneal1038/pilotforge-frontend:demo ..." -ForegroundColor Cyan
docker push hneal1038/pilotforge-frontend:demo

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "  Done. Demo image is live on Docker Hub." -ForegroundColor Green
    Write-Host "  Distribute the /demo folder — clients only need Docker Desktop." -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "  Push failed. Run: docker login" -ForegroundColor Red
}
