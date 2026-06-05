<#
.SYNOPSIS
Fire-and-forget launcher for symbiosis-handoff-live-dashboard (AUTON 3694a72b).
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Device,
    [string]$RepoRoot,
    [string]$MempalaceRoot,
    [int]$Port = 8766,
    [string]$BindAddress = "127.0.0.1",
    [switch]$Open,
    [switch]$NoPresence,
    [int]$CompletedLimit = 5,
    [switch]$AllowLan
)

$ErrorActionPreference = "Stop"

$LockFile = if ($env:SYMBIOSIS_HANDOFF_DASHBOARD_LOCK) {
    $env:SYMBIOSIS_HANDOFF_DASHBOARD_LOCK
} else {
    Join-Path $env:TEMP "symbiosis-handoff-dashboard.lock"
}
$LogFile = Join-Path $env:TEMP "symbiosis-handoff-dashboard.log"
$Url = "http://127.0.0.1:$Port/"

if (Test-Path -LiteralPath $LockFile) {
    $pidText = (Get-Content -LiteralPath $LockFile -Raw -ErrorAction SilentlyContinue).Trim()
    $existingPid = 0
    if ([int]::TryParse($pidText, [ref]$existingPid)) {
        $proc = Get-Process -Id $existingPid -ErrorAction SilentlyContinue
        if ($proc -and -not $proc.HasExited) {
            Write-Host "[symbiosis-handoff-dashboard] Already running (PID $existingPid) — $Url"
            Start-Process $Url | Out-Null
            exit 0
        }
    }
    Remove-Item -LiteralPath $LockFile -Force -ErrorAction SilentlyContinue
}

$getParams = @{
    Device          = $Device
    Port            = $Port
    BindAddress     = $BindAddress
    CompletedLimit  = $CompletedLimit
}
if ($RepoRoot) { $getParams.RepoRoot = $RepoRoot }
if ($MempalaceRoot) { $getParams.MempalaceRoot = $MempalaceRoot }
if ($NoPresence) { $getParams.NoPresence = $true }
if ($Open) { $getParams.Open = $true }
if ($AllowLan) { $getParams.AllowLan = $true }

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "python not found"; exit 1 }

$root = $RepoRoot
if (-not $root) {
    $guess = Resolve-Path (Join-Path $PSScriptRoot "..\..") -ErrorAction SilentlyContinue
    if ($guess) { $root = $guess.Path }
    elseif ($env:SYMBIOSIS_REPO_ROOT) { $root = $env:SYMBIOSIS_REPO_ROOT }
}
if (-not $root) { Write-Error "Cannot resolve repo root; pass -RepoRoot"; exit 1 }

$shim = Join-Path $root "cross-device\scripts\symbiosis-handoff-dashboard"
if (-not (Test-Path -LiteralPath $shim)) {
    Write-Error "symbiosis-handoff-dashboard shim not found: $shim"
    exit 1
}

$argList = @(
    $shim,
    "--device", $Device,
    "--repo-root", $root,
    "--port", "$Port",
    "--host", $BindAddress,
    "--completed-limit", "$CompletedLimit"
)
if ($MempalaceRoot) { $argList += @("--mempalace-root", $MempalaceRoot) }
if ($NoPresence) { $argList += "--no-presence" }
if ($Open) { $argList += "--open" }
if ($AllowLan) { $argList += "--allow-lan" }

$wd = Split-Path -Parent $shim
$p = Start-Process -FilePath $py.Source -ArgumentList $argList -WindowStyle Hidden `
    -RedirectStandardOutput $LogFile -RedirectStandardError $LogFile -PassThru -WorkingDirectory $wd
if (-not $p) { Write-Error "Failed to start dashboard"; exit 1 }

Set-Content -LiteralPath $LockFile -Value $p.Id -Encoding ascii
Start-Sleep -Seconds 2
Start-Process $Url | Out-Null
Write-Host "[symbiosis-handoff-dashboard] Launched at $Url (PID $($p.Id))"
Write-Host "[symbiosis-handoff-dashboard] Logs: $LogFile"
exit 0

# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 3694a72b implementer batch3) -->