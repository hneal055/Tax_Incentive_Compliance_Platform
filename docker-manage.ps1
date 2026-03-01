# ========================================
# Docker Management Script for PilotForge
# Simplified container management
# ========================================

param(
    [Parameter(Position=0)]
    [ValidateSet("start", "stop", "restart", "status", "logs", "clean", "rebuild", "shell")]
    [string]$Action = "status"
)

$ErrorActionPreference = "Continue"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "PilotForge - Docker Manager" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Docker is running
function Test-Docker {
    try {
        docker version 2>&1 | Out-Null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

if (-not (Test-Docker)) {
    Write-Host "❌ Docker Desktop is not running!" -ForegroundColor Red
    Write-Host "   Please start Docker Desktop first.`n" -ForegroundColor Yellow
    exit 1
}

switch ($Action) {
    "start" {
        Write-Host "🚀 Starting containers...`n" -ForegroundColor Green
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✅ Containers started successfully!" -ForegroundColor Green
            Write-Host "`n📊 Access points:" -ForegroundColor Cyan
            Write-Host "   API:        http://localhost:8000" -ForegroundColor White
            Write-Host "   API Docs:   http://localhost:8000/docs" -ForegroundColor White
            Write-Host "   PostgreSQL: localhost:5432" -ForegroundColor White
            Write-Host "`n   View logs: .\docker-manage.ps1 logs`n" -ForegroundColor Gray
        }
    }
    
    "stop" {
        Write-Host "🛑 Stopping containers...`n" -ForegroundColor Yellow
        docker-compose down
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✅ Containers stopped`n" -ForegroundColor Green
        }
    }
    
    "restart" {
        Write-Host "🔄 Restarting containers...`n" -ForegroundColor Cyan
        docker-compose restart
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✅ Containers restarted`n" -ForegroundColor Green
        }
    }
    
    "status" {
        Write-Host "📊 Container Status:`n" -ForegroundColor Cyan
        docker-compose ps
        
        Write-Host "`n💾 Image Details:`n" -ForegroundColor Cyan
        docker images pilotforge --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
        
        Write-Host "`n📈 Resource Usage:`n" -ForegroundColor Cyan
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" tax-incentive-db pilotforge-api 2>$null
    }
    
    "logs" {
        Write-Host "📋 Recent Logs (press Ctrl+C to stop)`n" -ForegroundColor Cyan
        Write-Host "Backend API logs:" -ForegroundColor Yellow
        docker-compose logs -f --tail=50 backend
    }
    
    "clean" {
        Write-Host "🧹 Cleaning up...`n" -ForegroundColor Yellow
        
        $response = Read-Host "This will remove containers and volumes. Continue? (y/N)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            docker-compose down -v
            docker system prune -f
            
            Write-Host "`n✅ Cleanup complete`n" -ForegroundColor Green
        } else {
            Write-Host "`nCleanup cancelled`n" -ForegroundColor Gray
        }
    }
    
    "rebuild" {
        Write-Host "🔨 Rebuilding and restarting...`n" -ForegroundColor Cyan
        docker-compose down
        docker-compose build --no-cache backend
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✅ Rebuild complete`n" -ForegroundColor Green
        }
    }
    
    "shell" {
        Write-Host "🐚 Opening shell in backend container...`n" -ForegroundColor Cyan
        docker exec -it pilotforge-api /bin/bash
    }
    
    default {
        Write-Host "Unknown action: $Action`n" -ForegroundColor Red
    }
}

Write-Host "========================================`n" -ForegroundColor Cyan
