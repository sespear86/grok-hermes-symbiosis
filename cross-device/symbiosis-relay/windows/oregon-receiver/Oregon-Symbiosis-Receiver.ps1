<#
.SYNOPSIS
  Oregon-Symbiosis-Receiver.ps1 — Thin launcher/wrapper for the hardened 19557e65 activator_core on Oregon.
  Sets SYMBIOSIS_SHARED + SYMBIOSIS_DEVICE=oregon, forwards --Health/--Status/--Once/--Dry-Run to the shared washington_activator.py (name kept for mirror source parity).
  Starts the poll loop when no flag (for scheduled task).
  Mirrors the thin CLI behavior + receipts from LIVE_TEST_19557e65_RECEIPTS.md exactly.

  Part of clean oregon-receiver kit (post WA live test + PASS). All 7 primes + Mirrorability.

.EXAMPLE
  # One-shot (test)
  .\Oregon-Symbiosis-Receiver.ps1 -Once

  # Health
  .\Oregon-Symbiosis-Receiver.ps1 -Health

  # Status
  .\Oregon-Symbiosis-Receiver.ps1 -Status

  # Loop (for scheduled task)
  .\Oregon-Symbiosis-Receiver.ps1
#>

[CmdletBinding()]
param(
    [switch]$Once,
    [switch]$Health,
    [switch]$Status,
    [switch]$DryRun,
    [string]$SharedBase = $env:SYMBIOSIS_SHARED
)

$ErrorActionPreference = "Stop"

if (-not $SharedBase) {
    $SharedBase = "$env:USERPROFILE\Synced\grok-mempalace-integration"
}

$RelayDir = Join-Path $SharedBase "symbiosis-relay"
$ActivatorPy = Join-Path $RelayDir "washington_activator.py"

# 19557e65 + oregon-support: force device for paths (inbox\oregon , status\oregon , *-oregon-grok-*.json beacon)
$env:SYMBIOSIS_SHARED = $SharedBase
$env:SYMBIOSIS_DEVICE = "oregon"

# Optional: point beacon to Oregon Set- script if present (the py calls it; falls back gracefully)
$BeaconCandidate = Join-Path $SharedBase "symbiosis-relay\windows\Set-OregonGrokBuildBeacon.ps1"
if (Test-Path $BeaconCandidate) {
    $env:GROK_BUILD_PRESENCE_BEACON = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$BeaconCandidate`""
}

Write-Host "=== Oregon Symbiosis Receiver (19557e65 hardened core) ===" -ForegroundColor Cyan
Write-Host "Shared: $SharedBase"
Write-Host "Device: oregon (inbox/status/beacon paths)"
Write-Host "Py: $ActivatorPy"
Write-Host ""

if (-not (Test-Path $ActivatorPy)) {
    Write-Error "Hardened activator not found at $ActivatorPy. Pull Kumquat / rich sync first."
    exit 1
}

$pyArgs = @()
if ($Once) { $pyArgs += "--once" }
if ($Health) { $pyArgs += "--health" }
if ($Status) { $pyArgs += "--status" }
if ($DryRun) { $pyArgs += "--dry-run" }

if ($pyArgs.Count -gt 0) {
    # Forward exactly; py will pick SYMBIOSIS_DEVICE from env we set
    & python -u $ActivatorPy @pyArgs
    $rc = $LASTEXITCODE
    if ($Health -or $Status) {
        # Health/status already printed by py; just propagate rc
    }
    exit $rc
}

# No flag: run the loop (for Task Scheduler "Oregon-Symbiosis-Task-Receiver")
Write-Host "Starting hardened loop (SYMBIOSIS_DEVICE=oregon). Use -Once for test. Ctrl-C to stop."
& python -u $ActivatorPy
exit $LASTEXITCODE

# <!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (19557e65 Oregon packaging autonomous) --> Exact primes + Mirrorability + self-provision + raunchy + bing bang boom followed. The receiver wrapper just got rammed into shape for OR Kumquat. Keep er goinnnn.