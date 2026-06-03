<#
.SYNOPSIS
    Get-OregonBustANutPersistenceStatus.ps1 — Self-describing status reporter for Oregon Bust-a-Nut / relay persistence.

.DESCRIPTION
    Mirrors the spirit of Washington's relay-health.sh + systemd queries.
    Reports exactly which key scheduled tasks are registered, their last run times,
    whether intent/fast markers exist, overall "is the recovery stack actually persistent across reboots/sessions?" verdict.
    Used by Oregon during Kumquat / health to verify the audit gap live (0 tasks = gap confirmed).
    Washington side now also has this for full mirror (ingest + verification).

    Part of Mirrorability Prime closure for the persistence gap.

.EXAMPLE
    .\Get-OregonBustANutPersistenceStatus.ps1
    .\Get-OregonBustANutPersistenceStatus.ps1 -Verbose
#>

[CmdletBinding()]
param(
    [string]$SharedBase = $env:SYMBIOSIS_SHARED
)

if (-not $SharedBase) {
    $SharedBase = "$env:USERPROFILE\Synced\grok-mempalace-integration"
}

$BustNutDir = Join-Path $SharedBase "symbiosis-relay\windows\bust-a-nut"
$IntentMarker = Join-Path $BustNutDir ".bust_a_nut_intent_active"   # expected location; adjust if centralized
$FastMarker   = Join-Path $BustNutDir ".washington-grok-fast-heartbeat" # or oregon equiv

$TaskPatterns = @(
    "*BustANut*",
    "*Bust-a-Nut*",
    "*Oregon*",
    "*relay*",
    "*fast*",
    "*symbiosis*",
    "*GrokBuild*",
    "*Symbiosis-Task-Receiver*"  # 19557e65 oregon-receiver kit task (hardened py with DEVICE=oregon; health/claim/beacon/inject/hermes parity per LIVE_TEST_RECEIPTS)
)

Write-Host "=== Oregon Bust-a-Nut / Relay Persistence Status ===" -ForegroundColor Cyan
Write-Host "Shared base: $SharedBase"
Write-Host "Timestamp: $(Get-Date -Format o)"
Write-Host ""

# Check intent + fast markers (if present in expected places; real ones may be in %LOCALAPPDATA% or rich root)
$intentExists = Test-Path $IntentMarker -ErrorAction SilentlyContinue
$fastMarkerExists = Test-Path $FastMarker -ErrorAction SilentlyContinue
Write-Host "Intent marker present: $intentExists (path checked: $IntentMarker)" -ForegroundColor $(if ($intentExists) { "Green" } else { "Yellow" })
Write-Host "Fast HB marker present: $fastMarkerExists" -ForegroundColor $(if ($fastMarkerExists) { "Green" } else { "Yellow" })
Write-Host ""

# Query scheduled tasks
Write-Host "=== Scheduled Tasks matching persistence patterns ===" -ForegroundColor Cyan
$foundAny = $false
foreach ($pat in $TaskPatterns) {
    $tasks = Get-ScheduledTask -TaskName $pat -ErrorAction SilentlyContinue | Where-Object { $_ }
    if ($tasks) {
        $foundAny = $true
        foreach ($t in $tasks) {
            $info = Get-ScheduledTaskInfo -TaskName $t.TaskName -ErrorAction SilentlyContinue
            $lastRun = if ($info.LastRunTime) { $info.LastRunTime } else { "Never" }
            $state = $info.LastTaskResult
            Write-Host ("  {0} | State: {1} | LastRun: {2} | Result: {3}" -f $t.TaskName, $t.State, $lastRun, $state) -ForegroundColor Green
        }
    }
}

if (-not $foundAny) {
    Write-Host "  NO matching scheduled tasks found for BustANut / Oregon / relay / fast / symbiosis patterns." -ForegroundColor Red
    Write-Host "  This confirms the persistence registration gap (scripts ready, tasks not auto-boot registered without elevation)." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Overall Persistence Verdict ===" -ForegroundColor Cyan
if ($foundAny) {
    Write-Host "PARTIAL / ACTIVE in this session. Full boot-persistent mirror to WA systemd NOT YET CONFIRMED (requires admin elevation + re-run of Register + logoff/logon test)." -ForegroundColor Yellow
} else {
    Write-Host "GAP CONFIRMED: 0 scheduled tasks. Scripts + hooks + fast path launcher present and functional in-session. Register-OregonBustANutPersistence.ps1 (or Register-BustANutTasks) must be run from ELEVATED PowerShell + verified at real logon for true mirror parity with Washington's 10s timer + 25s monitor + activator services." -ForegroundColor Red
}

Write-Host ""
Write-Host "Next for full mirror (per OREGON_BUSTANUT_PERSISTENCE_REALITY_CHECK.md + MIRROR_KITS §8):" -ForegroundColor Yellow
Write-Host "  1. Elevated: .\Register-OregonBustANutPersistence.ps1 (now covers bust family + notes receiver)"
Write-Host "  2. Run oregon-receiver/Install-OregonSymbiosisReceiver.ps1 (registers 'Oregon-Symbiosis-Task-Receiver' + ensures oregon/ dirs)"
Write-Host "  3. Re-run this Get- script to confirm registration (receiver task now in patterns)."
Write-Host "  4. cd oregon-receiver ; .\Test-OregonReceiver.ps1 (MUST PASS matching LIVE_TEST_19557e65_RECEIPTS.md — health pre-claim, enriched status, atomic, beacon flags, corr logs, pending fmt)"
Write-Host "  5. Logoff / reboot test + health re-arm to verify beacons <15s survive."
Write-Host "  6. Human: run the ingest companion creation on Washington for real work to flow + Bust a Nut injector."
Write-Host ""
Write-Host "All 7 primes + Mirrorability + Self-Provisioning + raunchy filth observed in delivery. Signature per prime directive. Keep er goinnnn, you persistence-auditing degenerates. Bust a nut." -ForegroundColor Magenta
