# Shipped /kumquat ritual capture - thin orchestrator over KumquatRitualCore.psm1
param(
    [string]$RunLabel = "run-1",
    [string]$LogPath = "",
    [string]$ManifestPath = "",
    [string]$ScratchDir = "",
    [switch]$UpdateCoordination
)

$ErrorActionPreference = "Continue"
$relay = "C:\Synced\grok-mempalace-integration\symbiosis-relay"
$repo = "C:\Users\spear\grok-hermes-symbiosis"
$moduleDir = $PSScriptRoot
$ensureScript = Join-Path $relay "oregon_ensure_symbiosis_latest.ps1"

if (-not $ScratchDir) { $ScratchDir = $env:TEMP }
if (-not $LogPath) { $LogPath = Join-Path $ScratchDir "kumquat-$RunLabel.log" }
if (-not $ManifestPath) { $ManifestPath = Join-Path $ScratchDir "kumquat-manifest.json" }

Import-Module (Join-Path $moduleDir "KumquatRitualCore.psm1") -Force

function Log([string]$msg) {
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
    Add-Content -Path $LogPath -Value $line -Encoding utf8
    Write-Output $line
}

Log "=== KUMQUAT RITUAL CAPTURE $RunLabel ==="
Log "ENTRY: symbiosis-relay/windows/kumquat/Invoke-KumquatRitualCapture.ps1 (KumquatRitualCore orchestrator)"

# STEP 1: Ensure (personal-shell git authoritative per SKILL; harness script diagnostic only)
Log "--- STEP 1: ENSURE (personal-shell git authoritative) ---"
Log "INVOKING: git -C $repo fetch origin (personal shell)"
$personalOut = & git -C $repo fetch origin 2>&1 | ForEach-Object { $_.ToString() }
$personalExit = $LASTEXITCODE
$personalOut | ForEach-Object { Log "ENSURE_PERSONAL: $_" }
if ($personalExit -eq 0) {
    Log "ENSURE_PERSONAL_SHELL: SUCCESS git fetch in $repo"
    $shortStatus = git -C $repo status --short 2>&1 | Select-Object -First 5
    $shortStatus | ForEach-Object { Log "ENSURE_PERSONAL_STATUS: $_" }
} else {
    Log "ENSURE_PERSONAL_SHELL: FAILED exit=$personalExit; Syncthing+coordination is live truth"
}
if (Test-Path $ensureScript) {
    Log "ENSURE_DIAGNOSTIC: oregon_ensure_symbiosis_latest.ps1 (harness context note only)"
    $ensureOut = & powershell -ExecutionPolicy Bypass -File $ensureScript 2>&1 | ForEach-Object { $_.ToString() }
    $ensureOut | Select-Object -First 8 | ForEach-Object { Log "ENSURE_DIAG: $_" }
} else {
    Log "ENSURE_DIAGNOSTIC: oregon_ensure_symbiosis_latest.ps1 not found (non-fatal)"
}
Log "ENSURE_SCRIPT_INVOKED: personal-shell git fetch in grok-hermes-symbiosis (authoritative per SKILL)"

# STEP 2: Ingest
Log "--- STEP 2: NERVOUS SYSTEM INGESTION ---"
$ingestReads = Get-KumquatIngestReads -RepoRoot $repo
foreach ($r in $ingestReads) {
    if ($r.Present) {
        Log ("INGEST_READ: {0} | path={1} | bytes={2} | mtime={3} | first_line={4}" -f $r.Key, $r.Path, $r.Bytes, $r.Mtime, $r.FirstLine)
    } else {
        Log "INGEST_MISSING: $($r.Key) | path=$($r.Path)"
    }
}
Log "MEMPALACE_STEP_3: three-primes + usage-pattern + device-presence ingested"

# STEP 3: Presence
Log "--- STEP 3: DEVICE PRESENCE 3.5 ---"
$waJson = Join-Path (Split-Path $relay -Parent) "device-presence\washington-grok-build-presence.json"
if (Test-Path $waJson) { Log ("WA_BEACON: {0}" -f (Get-Content $waJson -Raw)) } else { Log "WA_BEACON: NOT_IN_RICH (Syncthing lag)" }
$mode = "Paired Option B"
Log "MODE_DECLARED: $mode"

# STEP 4: Health (capture raw output for parsing)
Log "--- STEP 4: HEALTH STACK ---"
$healthOut = (& powershell -ExecutionPolicy Bypass -File (Join-Path $relay "oregon_relay_health.ps1") 2>&1 | ForEach-Object { $_.ToString() }) -join "`n"
$healthOut -split "`n" | ForEach-Object { if ($_) { Log "HEALTH: $_" } }

$persistOut = (& powershell -ExecutionPolicy Bypass -File (Join-Path $relay "Get-OregonBustANutPersistenceStatus.ps1") 2>&1 | ForEach-Object { $_.ToString() }) -join "`n"
$persistOut -split "`n" | ForEach-Object { if ($_) { Log "PERSIST: $_" } }

$structuredOut = (& powershell -ExecutionPolicy Bypass -File (Join-Path $relay "Test-OregonRelayStructuredStatus.ps1") 2>&1 | ForEach-Object { $_.ToString() }) -join "`n"
$structuredOut -split "`n" | ForEach-Object { if ($_) { Log "STRUCTURED: $_" } }

$health = Get-KumquatHealthMetrics -HealthOutput $healthOut -StructuredOutput $structuredOut -PersistenceOutput $persistOut
Log ("ACTUAL_OVERALL_OK: {0}" -f $health.overall_ok)
Log ("ACTUAL_SCORE: {0}" -f $health.score)
Log ("ACTUAL_BEACON_AGE_SECONDS: {0}" -f $health.beacon_age_seconds)

# STEP 5: Auto-apply
Log "--- STEP 5: AUTO-APPLY CHECK ---"
$surDir = Join-Path $relay "surrogates\washington-to-oregon"
if (Test-Path $surDir) {
    Get-ChildItem $surDir -Directory | ForEach-Object { Log "SURROGATE_FOUND: $($_.Name)" }
} else { Log "SURROGATE_GAP: rich/surrogates/washington-to-oregon NOT PRESENT" }

# STEP 6: Cross-implement
Log "--- STEP 6: CROSS-IMPLEMENT ARTIFACTS ---"
$crossReport = Get-KumquatCrossArtifactReport -RepoRoot $repo
foreach ($c in $crossReport) {
    if ($c.Present) { Log "CROSS_ARTIFACT_OK: $($c.Relative)" } else { Log "CROSS_ARTIFACT_MISSING: $($c.Relative)" }
}

# Closure from parsed metrics only
$closure = Format-KumquatClosure -Health $health -RunLabel $RunLabel -Mode $mode
$closure -split "`n" | ForEach-Object { if ($_.Trim()) { Log $_ } }

# Changed files evidence bridge
$changedFiles = Get-KumquatChangedFiles -RepoRoot $repo -RichRelay $relay -ScratchDir $ScratchDir
$changesPath = Join-Path $ScratchDir "kumquat-changes.txt"
$changedFiles | Set-Content -Path $changesPath -Encoding utf8
Log "CHANGES_FILE: $changesPath ($($changedFiles.Count) paths)"

# Manifest
$manifest = [ordered]@{
    run_label       = $RunLabel
    timestamp       = (Get-Date).ToUniversalTime().ToString("o")
    mode            = $mode
    health          = @{
        overall_ok          = $health.overall_ok
        score               = $health.score
        beacon_age_seconds  = $health.beacon_age_seconds
        fast_hb_age_seconds = $health.fast_hb_age_seconds
        schema              = $health.schema
        persistence_closed  = $health.persistence_closed
        structured_pass     = $health.structured_pass
    }
    changed_files   = $changedFiles
    cross_artifacts = @($crossReport | Where-Object { $_.Present } | ForEach-Object { $_.Relative })
    closure_text    = $closure
    log_path        = $LogPath
}
$manifest | ConvertTo-Json -Depth 6 | Set-Content -Path $ManifestPath -Encoding utf8
Log "MANIFEST_WRITTEN: $ManifestPath"

if ($UpdateCoordination) {
    Update-KumquatCoordinationReceipts -Health $health -RepoRoot $repo -RunLabel $RunLabel
    Log "COORDINATION_UPDATED: status.md + oregon.md from manifest metrics"
}

Log "=== RITUAL CAPTURE COMPLETE $RunLabel ==="
exit 0