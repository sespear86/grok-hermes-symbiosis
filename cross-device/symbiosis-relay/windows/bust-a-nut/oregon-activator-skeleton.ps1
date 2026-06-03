<#
.SYNOPSIS
  oregon-activator-skeleton.ps1 — DEPRECATED (19557e65 post-live-test packaging).
  Use the clean shared hardened core instead: cross-device/symbiosis-relay/windows/oregon-receiver/
    - Install-OregonSymbiosisReceiver.ps1 (elevated, dirs, Register call, scheduled "Oregon-Symbiosis-Task-Receiver")
    - Oregon-Symbiosis-Receiver.ps1 (thin launcher, sets DEVICE=oregon, forwards --Once/--Health/--Status to py)
    - Test-OregonReceiver.ps1 (THE STAR — drops oregon-test-19557e65, runs --Once, asserts health pre-claim/enriched status/atomic/pending/beacon/corr logs exactly per LIVE_TEST_19557e65_RECEIPTS.md)
  This skeleton is historical TODO port. The new kit uses the proven py (activator_core.py + washington_activator.py with SYMBIOSIS_DEVICE) for full parity with WA hardened core + live test receipts (no re-impl of claim/health/beacon/prompt/rc/pending).

  See: oregon-receiver/README-OREGON-RECEIVER-INSTALL.md , the handoff 20260603-..., windows-instructions.md top standing order, MIRROR_KITS update.

  Run elevated Register + the new Install for persistence + receiver task. Then Test- must PASS.
#>
param([switch]$Once)

Write-Host "DEPRECATED — use oregon-receiver/ kit (19557e65 + oregon-support packaging). See README-OREGON-RECEIVER-INSTALL.md and Test-OregonReceiver.ps1 for the drop-in that mirrors WA LIVE_TEST_RECEIPTS exactly via shared py." -ForegroundColor Yellow

$SharedBase = $env:SYMBIOSIS_SHARED
if (-not $SharedBase) { $SharedBase = "$env:USERPROFILE\Synced\grok-mempalace-integration" }

if ($Once) {
    Write-Host "One-shot on old skeleton — redirecting note only. Use the new kit for real test."
}

# <!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (19557e65 Oregon packaging autonomous) --> Big deprecation note added pointing to clean oregon-receiver kit + "use the shared hardened py + this launcher for full parity with the 19557e65 live test". Exact primes + Mirrorability + sig followed. Keep er goinnnn.
