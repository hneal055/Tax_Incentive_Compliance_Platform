Write-Host "📊 TAX INCENTIVE COMPLIANCE PLATFORM - LIVE DASHBOARD" -ForegroundColor Cyan
Write-Host "=" * 60

# Get health status
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/health" -TimeoutSec 3
    Write-Host "✅ API Status: $($health.status)" -ForegroundColor Green
    Write-Host "✅ Database: $($health.database)" -ForegroundColor Green
} catch {
    Write-Host "❌ API not responding" -ForegroundColor Red
    exit 1
}

# Get data
$clients = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/clients" -TimeoutSec 3
$incentives = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/incentives" -TimeoutSec 3
$reports = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/reports" -TimeoutSec 3
$stats = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/stats" -TimeoutSec 3

Write-Host "`n📈 PLATFORM STATISTICS:" -ForegroundColor White
Write-Host "   • Clients: $($clients.Count)" -ForegroundColor Green
Write-Host "   • Tax Incentives: $($incentives.Count)" -ForegroundColor Green
Write-Host "   • Compliance Reports: $($reports.Count)" -ForegroundColor Green

# Financial overview from stats
Write-Host "`n💰 FINANCIAL OVERVIEW:" -ForegroundColor White
Write-Host "   • Total Incentives: $($stats.statistics.financials.total_incentive_amount.ToString('C'))" -ForegroundColor Yellow
Write-Host "   • Total Claimed: $($stats.statistics.financials.total_claimed_amount.ToString('C'))" -ForegroundColor Yellow
Write-Host "   • Remaining: $($stats.statistics.financials.remaining_amount.ToString('C'))" -ForegroundColor Yellow

# Show top clients
Write-Host "`n🏆 TOP CLIENTS:" -ForegroundColor White
$clients | ForEach-Object { 
    $clientId = $_.id
    $clientIncentives = $incentives | Where-Object { $_.client_id -eq $clientId }
    $totalAmount = ($clientIncentives | Measure-Object -Property amount -Sum).Sum
    if ($totalAmount -gt 0) {
        [PSCustomObject]@{
            Name = $_.name
            Incentives = $clientIncentives.Count
            Amount = $totalAmount
        }
    }
} | Sort-Object Amount -Descending | Select-Object -First 3 | ForEach-Object {
    Write-Host "   • $($_.Name): $($_.Incentives) incentives, $($_.Amount.ToString('C'))" -ForegroundColor Gray
}

# Incentive status breakdown
Write-Host "`n📋 INCENTIVE STATUS:" -ForegroundColor White
$incentives | Group-Object status | ForEach-Object {
    $percent = [math]::Round(($_.Count / $incentives.Count) * 100, 1)
    Write-Host "   • $($_.Name): $($_.Count) ($percent%)" -ForegroundColor Gray
}

Write-Host "`n" + "=" * 60
Write-Host "🔗 API ENDPOINTS:" -ForegroundColor Cyan
Write-Host "   • Health:     http://localhost:8000/api/v1/health" -ForegroundColor Yellow
Write-Host "   • Clients:    http://localhost:8000/api/v1/clients" -ForegroundColor Yellow
Write-Host "   • Incentives: http://localhost:8000/api/v1/incentives" -ForegroundColor Yellow
Write-Host "   • Reports:    http://localhost:8000/api/v1/reports" -ForegroundColor Yellow
Write-Host "   • Stats:      http://localhost:8000/api/v1/stats" -ForegroundColor Yellow
Write-Host "   • Docs:       http://localhost:8000/docs" -ForegroundColor Yellow

Write-Host "`n✅ Platform Status: FULLY OPERATIONAL" -ForegroundColor Green
Write-Host "⏰ Last Updated: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
