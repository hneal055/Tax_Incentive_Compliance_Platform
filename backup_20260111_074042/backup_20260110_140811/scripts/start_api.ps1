[CmdletBinding()]
param(
  [int]$Port = 8000,
  [string]$Host = "0.0.0.0",
  [switch]$NoReload,
  [switch]$OverrideEnv
)

$ErrorActionPreference = "Stop"

# Ensure we run from project root (parent of /scripts)
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $ProjectRoot

function Load-DotEnv([string]$Path, [switch]$Override) {
  if (!(Test-Path $Path)) { return }
  Get-Content $Path | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith("#")) { return }

    # Support: KEY=VALUE and optional quotes
    $m = [regex]::Match($line, '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$')
    if (-not $m.Success) { return }

    $key = $m.Groups[1].Value
    $val = $m.Groups[2].Value.Trim()

    if (($val.StartsWith('"') -and $val.EndsWith('"')) -or ($val.StartsWith("'") -and $val.EndsWith("'"))) {
      $val = $val.Substring(1, $val.Length - 2)
    }

    $existing = [Environment]::GetEnvironmentVariable($key, "Process")
    if ($Override -or [string]::IsNullOrEmpty($existing)) {
      [Environment]::SetEnvironmentVariable($key, $val, "Process")
    }
  }
}

# Load .env into current process (so uvicorn sees DATABASE_URL, etc.)
Load-DotEnv -Path (Join-Path $ProjectRoot ".env") -Override:$OverrideEnv

# Quick visibility
if ([string]::IsNullOrEmpty($env:DATABASE_URL)) {
  Write-Warning "DATABASE_URL is not set. If you expect it from .env, confirm .env exists and contains DATABASE_URL=..."
}

# Build uvicorn args
$argsList = @("src.main:app", "--host", $Host, "--port", "$Port")
if (-not $NoReload) { $argsList += "--reload" }

Write-Host ("Starting API: python -m uvicorn " + ($argsList -join " ")) -ForegroundColor Cyan
python -m uvicorn @argsList
