# Goal completion entry: harness evidence + precompletion sync + 600s patch guard
param(
    [string]$ScratchDir = "",
    [string]$RepoRoot = "C:\Users\spear\grok-hermes-symbiosis",
    [string]$SessionDir = "",
    [switch]$SkipHarness
)

$ErrorActionPreference = "Stop"
$moduleDir = $PSScriptRoot
$harnessScript = Join-Path $moduleDir "Invoke-KumquatVerificationHarness.ps1"
$preSyncScript = Join-Path $moduleDir "Invoke-KumquatPreCompletionSync.ps1"

if (-not $ScratchDir) { $ScratchDir = $env:KUMQUAT_SCRATCH }
if (-not $ScratchDir) { throw "KUMQUAT_SCRATCH or -ScratchDir required" }
if (-not (Test-Path $ScratchDir)) { New-Item -ItemType Directory -Path $ScratchDir -Force | Out-Null }

if (-not $SkipHarness) {
    & powershell -ExecutionPolicy Bypass -File $harnessScript -ScratchDir $ScratchDir -RepoRoot $RepoRoot
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

$preArgs = @("-ExecutionPolicy", "Bypass", "-File", $preSyncScript, "-ScratchDir", $ScratchDir, "-RepoRoot", $RepoRoot)
if ($SessionDir) { $preArgs += @("-SessionDir", $SessionDir) }
& powershell @preArgs
exit $LASTEXITCODE