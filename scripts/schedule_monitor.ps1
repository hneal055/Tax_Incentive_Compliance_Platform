# PilotForge — Register Sub-Jurisdiction Monitor in Windows Task Scheduler
# Run once as Administrator to set up daily monitoring.
# Usage: Right-click → Run with PowerShell (as Administrator)

$TaskName    = "PilotForge-SubJurisdiction-Monitor"
$ProjectPath = "c:\Projects\Tax_Incentive_Compliance_Platform"
$PythonExe   = "$ProjectPath\.venv\Scripts\python.exe"
$ScriptPath  = "$ProjectPath\monitor.py"
$LogFile     = "$ProjectPath\logs\monitor.log"

# Create logs directory if needed
if (-not (Test-Path "$ProjectPath\logs")) {
    New-Item -ItemType Directory -Path "$ProjectPath\logs" | Out-Null
}

# Remove existing task if present
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "  Removed existing task." -ForegroundColor Yellow
}

# Action: run via cmd.exe so >> redirection works
$Action = New-ScheduledTaskAction `
    -Execute "cmd.exe" `
    -Argument "/c `"$PythonExe $ScriptPath >> `"$LogFile`" 2>&1`"" `
    -WorkingDirectory $ProjectPath

# Trigger: daily at 6:00 AM
$Trigger = New-ScheduledTaskTrigger -Daily -At "06:00AM"

# Run whether user is logged on or not
$Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

$Principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType S4U `
    -RunLevel Highest

Register-ScheduledTask `
    -TaskName  $TaskName `
    -Action    $Action `
    -Trigger   $Trigger `
    -Settings  $Settings `
    -Principal $Principal `
    -Description "PilotForge daily sub-jurisdiction feed monitor. Checks county/city feeds for tax incentive changes and queues Claude extractions for review." | Out-Null

Write-Host ""
Write-Host "  Task registered: $TaskName" -ForegroundColor Green
Write-Host "  Schedule:        Daily at 6:00 AM" -ForegroundColor Cyan
Write-Host "  Log output:      $LogFile" -ForegroundColor Cyan
Write-Host ""
Write-Host "  To run immediately:" -ForegroundColor White
Write-Host "    Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  To view logs:" -ForegroundColor White
Write-Host "    Get-Content '$LogFile' -Tail 50" -ForegroundColor DarkGray
Write-Host ""
