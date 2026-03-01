# ========================================
# Build Docker Image for PilotForge
# ========================================

param(
    [string]$Tag = "latest",
    [switch]$NoBuildCache,
    [switch]$Push
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "PilotForge - Docker Image Builder" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Docker is running
Write-Host "[1/5] Checking Docker..." -NoNewline
try {
    docker version 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Docker not running" }
    Write-Host " ✅" -ForegroundColor Green
} catch {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host "`nError: Docker Desktop is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again.`n" -ForegroundColor Yellow
    exit 1
}

# Verify required files exist
Write-Host "[2/5] Checking required files..." -NoNewline
$requiredFiles = @("Dockerfile", "requirements.txt", "prisma/schema.prisma")
$missing = @()

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missing += $file
    }
}

if ($missing.Count -gt 0) {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host "`nMissing required files:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "  • $_" -ForegroundColor Gray }
    exit 1
}
Write-Host " ✅" -ForegroundColor Green

# Display build info
Write-Host "[3/5] Build configuration:" -ForegroundColor Cyan
Write-Host "  Image name: pilotforge:$Tag" -ForegroundColor White
Write-Host "  Build cache: $(-not $NoBuildCache)" -ForegroundColor White
Write-Host "  Push to registry: $Push" -ForegroundColor White

# Build the image
Write-Host "`n[4/5] Building Docker image..." -ForegroundColor Yellow
Write-Host "  This may take 3-5 minutes...`n" -ForegroundColor Gray

$buildArgs = @(
    "build",
    "-t", "pilotforge:$Tag",
    "-f", "Dockerfile"
)

if ($NoBuildCache) {
    $buildArgs += "--no-cache"
}

$buildArgs += "."

Write-Host "Command: docker $($buildArgs -join ' ')`n" -ForegroundColor DarkGray

$buildStart = Get-Date
& docker $buildArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Build failed!" -ForegroundColor Red
    exit 1
}

$buildTime = ((Get-Date) - $buildStart).TotalSeconds
Write-Host "`n✅ Build completed in $([math]::Round($buildTime, 1))s" -ForegroundColor Green

# Get image info
Write-Host "`n[5/5] Image details:" -ForegroundColor Yellow
$imageInfo = docker images pilotforge:$Tag --format "{{.Repository}}:{{.Tag}} - {{.Size}}" 2>&1
Write-Host "  $imageInfo" -ForegroundColor White

# Tag as latest if building a version tag
if ($Tag -ne "latest") {
    Write-Host "`n  Tagging as latest..." -NoNewline
    docker tag pilotforge:$Tag pilotforge:latest 2>&1 | Out-Null
    Write-Host " ✅" -ForegroundColor Green
}

# Push if requested
if ($Push) {
    Write-Host "`n  Pushing to registry..." -ForegroundColor Cyan
    docker push pilotforge:$Tag
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ⚠️ Push failed (check registry authentication)" -ForegroundColor Yellow
    } else {
        Write-Host "  ✅ Pushed successfully" -ForegroundColor Green
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ SUCCESS!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Image ready: pilotforge:$Tag`n" -ForegroundColor White

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Test locally:   docker-compose up" -ForegroundColor White
Write-Host "  2. Run standalone: docker run -p 8000:8000 pilotforge:$Tag" -ForegroundColor White
Write-Host "  3. View logs:      docker logs pilotforge-api`n" -ForegroundColor White
