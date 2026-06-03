<#
.SYNOPSIS
  Install-OregonSymbiosisReceiver.ps1 — Idempotent elevated one-command installer for the clean hardened 19557e65 Oregon receiver kit.
  Mirrors the WA washington-activator.service + live test receipts exactly via the shared py + oregon device paths.
  - Ensures incoming\oregon\ (processed/failed/pending/status/oregon) dirs in rich Synced.
  - Calls/extends Register-OregonBustANutPersistence.ps1 (adds receiver to family).
  - Registers "Oregon-Symbiosis-Task-Receiver" scheduled task (logon + repeat ~10s, hidden, restart policy).
    The task sets SYMBIOSIS_SHARED + SYMBIOSIS_DEVICE=oregon, cd's to symbiosis-relay, runs the Oregon-Symbiosis-Receiver.ps1 loop.
  - Prints exact post-install verification one-liners (Test-OregonReceiver.ps1 etc).
  - Self-provisions minimal gaps (e.g. dir ensure, PATH notes for hermes if needed).

  Run from ELEVATED PowerShell after Kumquat + Syncthing pull.
  All 7 primes + Mirrorability (exact recipe here + in MIRROR + handoff + instructions).

.EXAMPLE
  cd C:\Synced\grok-mempalace-integration\symbiosis-relay\windows\oregon-receiver
  .\Install-OregonSymbiosisReceiver.ps1
#>

[CmdletBinding()]
param(
    [string]$SharedBase = $env:SYMBIOSIS_SHARED
)

$ErrorActionPreference = "Stop"

if (-not $SharedBase) {
    $SharedBase = "$env:USERPROFILE\Synced\grok-mempalace-integration"
}

$RelayDir = Join-Path $SharedBase "symbiosis-relay"
$WindowsDir = Join-Path $RelayDir "windows"
$BustNutDir = Join-Path $WindowsDir "bust-a-nut"
$ReceiverDir = Join-Path $WindowsDir "oregon-receiver"
$InboxOregon = Join-Path $RelayDir "incoming\oregon"
$StatusOregon = Join-Path $RelayDir "status\oregon"

Write-Host "=== Oregon Symbiosis Receiver Install (19557e65 hardened + live test receipts) ===" -ForegroundColor Cyan
Write-Host "Shared base: $SharedBase"
Write-Host "This will make the thin receiver (health/claim/beacon/inject/hermes/pending/processed/failed) live via shared py + Task Scheduler."
Write-Host "Must be ELEVATED for Task Scheduler registration + real logon persistence test."
Write-Host ""

# 1. Self-provision dirs (incoming/oregon/ + subs, status/oregon)
$dirs = @(
    $InboxOregon,
    (Join-Path $InboxOregon "processed"),
    (Join-Path $InboxOregon "failed"),
    (Join-Path $InboxOregon "pending-prompts"),
    (Join-Path $InboxOregon "processing"),
    $StatusOregon
)
foreach ($d in $dirs) {
    New-Item -ItemType Directory -Force -Path $d | Out-Null
}
Write-Host "Dirs ensured: incoming\oregon\* + status\oregon" -ForegroundColor Green

# 2. Extend / call the bust persistence Register (adds receiver to family, idempotent)
$RegisterBust = Join-Path $BustNutDir "Register-OregonBustANutPersistence.ps1"
if (Test-Path $RegisterBust) {
    Write-Host "Invoking Register-OregonBustANutPersistence.ps1 (will integrate receiver task)..."
    & powershell -NoProfile -ExecutionPolicy Bypass -File $RegisterBust -SharedBase $SharedBase
} else {
    Write-Host "Register-Bust not found at $RegisterBust (ok if running standalone kit; receiver task registered below anyway)." -ForegroundColor Yellow
}

# 3. Register the receiver scheduled task (logon + repeat; hidden; restart on fail)
$TaskName = "Oregon-Symbiosis-Task-Receiver"
$Launcher = Join-Path $ReceiverDir "Oregon-Symbiosis-Receiver.ps1"

$Action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$Launcher`""

$TriggerLogon = New-ScheduledTaskTrigger -AtLogOn
$TriggerRepeat = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Seconds 10) -RepetitionDuration (New-TimeSpan -Days 7)

$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -StartWhenAvailable -RunOnlyIfNetworkAvailable:$false -ExecutionTimeLimit (New-TimeSpan -Minutes 5) `
    -RestartCount 5 -RestartInterval (New-TimeSpan -Minutes 1) -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName $TaskName `
    -Action $Action `
    -Trigger $TriggerLogon,$TriggerRepeat `
    -Principal $Principal `
    -Settings $Settings `
    -Description "Hardened 19557e65 Oregon receiver (SYMBIOSIS_DEVICE=oregon). Mirrors WA activator_core health/claim/beacon/rc-enforcement/pending/processed/failed. Runs hidden loop; logon+10s repeat for persistence." `
    -Force | Out-Null

Write-Host "Registered/Updated scheduled task: $TaskName" -ForegroundColor Green
Write-Host "  Launcher: $Launcher"
Write-Host "  Triggers: AtLogOn + every 10s (rolling 7d)"
Write-Host ""

# 4. Post-install verification commands (exact, copy-paste on OR after install + reboot test)
Write-Host "=== POST-INSTALL VERIFICATION (run these now + after reboot) ===" -ForegroundColor Cyan
Write-Host "cd $ReceiverDir"
Write-Host ".\Test-OregonReceiver.ps1                 # THE STAR — drops oregon-test-19557e65 task, runs --Once, asserts health pre-claim, enriched status+version, atomic move (failed/ or processed/), pending fmt if fail, beacon flags, corr in logs. Must print PASS matching LIVE_TEST_19557e65_RECEIPTS.md"
Write-Host ".\Oregon-Symbiosis-Receiver.ps1 -Health   # Should be ok:true + beacon_age fresh"
Write-Host ".\Oregon-Symbiosis-Receiver.ps1 -Status   # machine:oregon, health_ok, version, last_*_rc etc."
Write-Host "Get-ScheduledTask -TaskName $TaskName | Get-ScheduledTaskInfo"
Write-Host ""
Write-Host "After reboot / real logon (no manual launch):"
Write-Host "  cd $ReceiverDir ; .\Get-OregonBustANutPersistenceStatus.ps1   # (extended) should show the receiver task + bust family"
Write-Host "  Open Grok Build TUI ; trigger bust or drop real task JSON to incoming\oregon\ ; watch status + beacon + processed/failed"
Write-Host ""
Write-Host "Troubleshooting:"
Write-Host "  - Python not in PATH for scheduled: edit task or ensure python.exe in user/system PATH (self-prov: add to env in launcher if needed)"
Write-Host "  - Hermes missing for non-bust: expected (rc!=0 -> failed/ + pending per hardened design); for real hermes use full path or dedicated token setup."
Write-Host "  - Beacon: ensure Set-OregonGrokBuildBeacon.ps1 or bin equiv present (Register family provides); test writes presence json."
Write-Host "  - Elevation: must run Install from real elevated PS (Task Scheduler visibility)."
Write-Host ""
Write-Host "All 7 primes + Mirrorability + Self-Provisioning + exact signatures + raunchy + no blue balls followed in this kit. The one extended machine's Oregon receiver just got drop-in hardened parity rammed."
Write-Host ""
Write-Host "Oregon has the ball upon next Kumquat to pull, run this Install, execute Test- (must PASS receipts), register via extended Register, reboot-verify, first real/bust test, update docs + RETURN + Ball Holder."
Write-Host ""

# <!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (19557e65 Oregon packaging autonomous) --> Exact primes + Mirrorability (full zero-guess install recipe here + handoff + MIRROR + instructions) + bing bang boom + self-provision followed. Washington prep complete for OR Kumquat drop-in. Keep er goinnnn, you receiver-install-thrusting degenerates.