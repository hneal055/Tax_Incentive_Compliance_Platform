Write-Host "🔍 Docker Status Check" -ForegroundColor Cyan
Write-Host "=" * 50

# Method 1: Check with docker version
Write-Host "1. Checking with 'docker version'..." -ForegroundColor Yellow
docker version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker is accessible" -ForegroundColor Green
} else {
    Write-Host "❌ Docker is not accessible" -ForegroundColor Red
    Write-Host "   Try: docker version" -ForegroundColor Yellow
}

# Method 2: Check running containers
Write-Host "`n2. Checking running containers..." -ForegroundColor Yellow
docker ps 2>$null
if ($LASTEXITCODE -eq 0) {
    $containerCount = (docker ps --format "{{.Names}}" | Measure-Object).Count
    Write-Host "✅ Found $containerCount running container(s)" -ForegroundColor Green
} else {
    Write-Host "❌ Cannot list containers" -ForegroundColor Red
}

# Method 3: Check for PostgreSQL specifically
Write-Host "`n3. Checking for PostgreSQL container..." -ForegroundColor Yellow
$postgresContainer = docker ps --filter "name=tax-incentive-db" --format "{{.Names}}" 2>$null
if ($postgresContainer) {
    Write-Host "✅ PostgreSQL container is running: $postgresContainer" -ForegroundColor Green
} else {
    Write-Host "⚠ PostgreSQL container is not running" -ForegroundColor Yellow
    # Check if it exists but stopped
    $stoppedContainer = docker ps -a --filter "name=tax-incentive-db" --format "{{.Names}}" 2>$null
    if ($stoppedContainer) {
        Write-Host "   Container exists but is stopped. Start with: docker start tax-incentive-db" -ForegroundColor Gray
    } else {
        Write-Host "   Container doesn't exist. Create with:" -ForegroundColor Gray
        Write-Host "   docker run -d --name tax-incentive-db -p 5432:5432 \" -ForegroundColor Gray
        Write-Host "     -e POSTGRES_PASSWORD=postgres \" -ForegroundColor Gray
        Write-Host "     -e POSTGRES_DB=tax_incentive_db \" -ForegroundColor Gray
        Write-Host "     -v postgres-tax-data:/var/lib/postgresql/data \" -ForegroundColor Gray
        Write-Host "     postgres:16-alpine" -ForegroundColor Gray
    }
}

# Method 4: Check Docker Desktop status (alternative)
Write-Host "`n4. Alternative check..." -ForegroundColor Yellow
try {
    $dockerProcess = Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue
    if ($dockerProcess) {
        Write-Host "✅ Docker Desktop process is running" -ForegroundColor Green
    } else {
        Write-Host "⚠ Docker Desktop process not found (may be running as service)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ Could not check Docker Desktop process" -ForegroundColor Yellow
}

Write-Host "`n" + "=" * 50
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "• If 'docker version' works, Docker is running" -ForegroundColor White
Write-Host "• If PostgreSQL container isn't running, start it" -ForegroundColor White
Write-Host "• If issues persist, restart Docker Desktop" -ForegroundColor White
