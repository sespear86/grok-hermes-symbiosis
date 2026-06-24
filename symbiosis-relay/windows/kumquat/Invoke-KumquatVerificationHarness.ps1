# Shipped /kumquat verification harness - ONLY entry for dual-run + evidence bundle
param(
    [string]$ScratchDir = "",
    [string]$RepoRoot = "C:\Users\spear\grok-hermes-symbiosis"
)

$ErrorActionPreference = "Stop"
$moduleDir = $PSScriptRoot
$captureScript = Join-Path $moduleDir "Invoke-KumquatRitualCapture.ps1"

if (-not $ScratchDir) {
    $ScratchDir = $env:KUMQUAT_SCRATCH
}
if (-not $ScratchDir) {
    $ScratchDir = Join-Path $env:TEMP "grok-kumquat-verify"
}
if (-not (Test-Path $ScratchDir)) {
    New-Item -ItemType Directory -Path $ScratchDir -Force | Out-Null
}

Import-Module (Join-Path $moduleDir "KumquatRitualCore.psm1") -Force

$logPath = Join-Path $ScratchDir "kumquat-harness.log"
function HLog([string]$msg) {
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
    Add-Content -Path $logPath -Value $line -Encoding utf8
    Write-Output $line
}

HLog "=== KUMQUAT VERIFICATION HARNESS ==="
HLog "ENTRY: Invoke-KumquatVerificationHarness.ps1"
HLog "SCRATCH: $ScratchDir"

# Snapshot + baseline for clean run-1 (no run-2 receipt leakage)
$statusPath = Join-Path $RepoRoot "cross-device\coordination\status.md"
$oregonPath = Join-Path $RepoRoot "Mempalace\symbiosis\device-presence\oregon.md"
if (Test-Path $statusPath) { Copy-Item $statusPath (Join-Path $ScratchDir "kumquat-snapshot-status.md") -Force }
if (Test-Path $oregonPath) { Copy-Item $oregonPath (Join-Path $ScratchDir "kumquat-snapshot-oregon.md") -Force }
Restore-KumquatCoordinationBaseline -RepoRoot $RepoRoot -ScratchDir $ScratchDir | Out-Null
HLog "BASELINE_RESTORED: status.md cleared of manifest receipt for run-1 isolation"

# Run-1: no coordination update
$run1Log = Join-Path $ScratchDir "kumquat-run-1.log"
$run1Manifest = Join-Path $ScratchDir "kumquat-manifest-run1.json"
if (Test-Path $run1Log) { Remove-Item $run1Log -Force }
& powershell -ExecutionPolicy Bypass -File $captureScript `
    -RunLabel "run-1" -ScratchDir $ScratchDir `
    -LogPath $run1Log -ManifestPath $run1Manifest
if ($LASTEXITCODE -ne 0) { HLog "FATAL: run-1 capture failed"; exit 1 }
HLog "RUN-1_COMPLETE"

# Assert run-1 status ingest lacks run-2 receipt
$run1Content = Get-Content $run1Log -Raw
if ($run1Content -match "INGEST_READ: status.*run-2") {
    HLog "FATAL: run-1 log ingested status with run-2 receipt (state leakage)"
    exit 1
}
HLog "RUN-1_ISOLATION: PASS (status ingest lacks run-2 receipt)"

# Run-2: coordination update
$run2Log = Join-Path $ScratchDir "kumquat-run-2.log"
$run2Manifest = Join-Path $ScratchDir "kumquat-manifest.json"
if (Test-Path $run2Log) { Remove-Item $run2Log -Force }
& powershell -ExecutionPolicy Bypass -File $captureScript `
    -RunLabel "run-2" -ScratchDir $ScratchDir `
    -LogPath $run2Log -ManifestPath $run2Manifest -UpdateCoordination
if ($LASTEXITCODE -ne 0) { HLog "FATAL: run-2 capture failed"; exit 1 }
HLog "RUN-2_COMPLETE COORDINATION_UPDATED"

# Verification bundle (Pester 4/4, grep, closure, relative changes)
$bundle = Write-KumquatVerificationBundle -RepoRoot $RepoRoot -ScratchDir $ScratchDir `
    -ModuleDir $moduleDir -ManifestPath $run2Manifest
HLog ("BUNDLE: pest Passed=$($bundle.pest_passed) Failed=$($bundle.pest_failed)")

if ($bundle.pest_failed -gt 0) {
    HLog "FATAL: Pester failures in bundle"
    exit 1
}

HLog "=== HARNESS COMPLETE ==="
exit 0