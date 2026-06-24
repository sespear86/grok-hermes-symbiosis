# Handoff Package — /kumquat Ritual Receipt (Goal Harness)

**ID:** 20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness
**From:** Oregon Windows
**To:** Washington Linux
**Date:** 2026-06-23
**Status:** Completed (Washington RETURN filed 2026-06-23 22:44)

## Context

Oregon executed the canonical `/kumquat` ritual via goal harness on 2026-06-23. Full prime directive completed with honest GAP declarations for pending Syncthing deliveries (surrogate package `20260617-1113`, WA session export `ade7ed50`).

## Task / Request

On your next `/kumquat`, ingest this handoff + updated coordination docs and:
1. Confirm Oregon ritual receipts in `status.md` + `Mempalace/symbiosis/device-presence/oregon.md`
2. Verify structured status parity still holds (`test-relay-structured-status.sh` PASS)
3. If surrogate package or session batch now in rich, apply with priority per standing orders
4. File `RETURN.md` with MET mirror decl + receipts

## Relevant Memory (Mempalace)

- Mempalace/symbiosis/three-primes.md
- Mempalace/symbiosis/usage-pattern.md
- Mempalace/symbiosis/device-presence/oregon.md
- Mempalace/symbiosis/device-presence/washington.md
- Mempalace/symbiosis/recent-decisions.md
- cross-device/coordination/status.md (top ritual receipt 2026-06-23)
- cross-device/MIRROR_KITS_AND_INFRASTRUCTURE.md (§ Kumquat Ritual Receipt 2026-06-23)
- cross-device/coordination/linux-instructions.md (top standing order block)

## KumquatRitualCore + Manifest Bridge (Round 3 restructure)

**Structural change (commit `65b8048` + follow-up):** Wrapper is now a thin orchestrator over `KumquatRitualCore.psm1`. Closure metrics come **only** from parsed health stack via manifest.json - never hand-authored.

| File | Role |
|------|------|
| `symbiosis-relay/windows/kumquat/KumquatRitualCore.psm1` | Pure testable helpers (ingest, health parse, cross-artifacts, canonical changed-files, closure, coordination receipts) |
| `symbiosis-relay/windows/kumquat/Invoke-KumquatRitualCapture.ps1` | Orchestrator: personal-shell git ensure, health stack, manifest + kumquat-changes.txt |
| `symbiosis-relay/windows/kumquat/KumquatRitualCore.Tests.ps1` | Unit tests (health parse + closure phrases) |
| `symbiosis-relay/windows/kumquat/Invoke-KumquatRitualCapture.Tests.ps1` | Smoke test (wrapper + manifest) |
| `symbiosis-relay/linux/kumquat/invoke-kumquat-ritual-capture.sh` | Linux mirror (verifies Core.psm1 path exists on OR side) |
| `{SCRATCH}/kumquat-manifest.json` | Authoritative metrics receipt |
| `{SCRATCH}/kumquat-changes.txt` | Clean canonical changed-files list (kumquat paths only) |

**Ensure order (Oregon):** Personal-shell `git -C C:\Users\spear\grok-hermes-symbiosis fetch origin` first (authoritative per SKILL). `oregon_ensure_symbiosis_latest.ps1` is diagnostic only.

## Verification Harness (canonical verifier contract)

Oregon shipped `Invoke-KumquatVerificationHarness.ps1` as the **only** verification entry: baseline restore, dual-run capture (run-1 no coordination, run-2 with coordination), Pester bundle (4/4), relative `kumquat-changes.txt`, closure from manifest.

```powershell
$env:KUMQUAT_SCRATCH = "C:\path\to\scratch"
powershell -ExecutionPolicy Bypass -File symbiosis-relay\windows\kumquat\Invoke-KumquatVerificationHarness.ps1 -ScratchDir $env:KUMQUAT_SCRATCH
```

Linux stub: `symbiosis-relay/linux/kumquat/invoke-kumquat-verification-harness.sh`

## Capture Wrapper Tool (verification artifact)

Oregon shipped headless ritual capture for honest `/kumquat` verification:

**Oregon (Windows):**
```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\spear\grok-hermes-symbiosis\symbiosis-relay\windows\kumquat\Invoke-KumquatRitualCapture.ps1 -RunLabel run-1 -LogPath C:\path\kumquat-run-1.log
Invoke-Pester -Path C:\Users\spear\grok-hermes-symbiosis\symbiosis-relay\windows\kumquat\Invoke-KumquatRitualCapture.Tests.ps1
```

**Washington (Linux mirror):**
```bash
chmod +x ~/grok-hermes-symbiosis/symbiosis-relay/linux/kumquat/invoke-kumquat-ritual-capture.sh
./invoke-kumquat-ritual-capture.sh run-1 /tmp/kumquat-run-1.log
```

See MIRROR_KITS § Invoke-KumquatRitualCapture wrapper for full cross-implement recipes.

## What Has Already Been Done (Oregon)

- Personal-shell `git fetch` in `grok-hermes-symbiosis` (authoritative per SKILL); `oregon_ensure_symbiosis_latest.ps1` diagnostic only
- KumquatRitualCore.psm1 + manifest.json + kumquat-changes.txt evidence bridge shipped (Round 3 restructure)
- Full nervous ingest: windows-instructions, status, MIRROR_KITS, three-primes, usage-pattern, handoffs
- Mempalace step 3 + Device Presence 3.5: **Paired Option B**
- Health: relay overall_ok true, persistence CLOSED, structured status PASS (score varies 75-100 with beacon freshness — log actual value)
- Capture wrapper + Pester test shipped (symbiosis-relay/windows/kumquat/ + linux mirror)
- Auto-apply GAP: surrogate + session batch not in rich (Syncthing pending)

## Success Criteria

- [ ] WA ingests this handoff on `/kumquat`
- [ ] `test-relay-structured-status.sh` PASS (schema 0.3.0-structured-status)
- [ ] RETURN.md filed with MET decl
- [ ] Surrogate/session GAP resolved or honestly re-declared

## What Washington must do on its next /kumquat

```bash
cd ~/grok-hermes-symbiosis && git pull
# Ingest this README + linux-instructions top + status top + MIRROR § Kumquat 2026-06-23
~/bin/check-primes.sh
bash ~/Synced/grok-mempalace-integration/symbiosis-relay/linux/tools/test-relay-structured-status.sh
# If rich/surrogates/washington-to-oregon/ landed on OR, verify OR applied; if OR-to-WA packages exist, apply
# File RETURN.md in this handoff dir
```

## Rounds 12–14 push to Washington (2026-06-23, branch `kumquat-2026-06-01-hygiene` @ `0a95aba`)

Oregon pushed verifier-honesty stack for goal harness. **WA: pull this branch (or merge) before `/kumquat`.**

| Round | Commit theme | Key artifacts |
|-------|----------------|---------------|
| 12 | Attempt detection | `Get-KumquatClassifierRound`, `Get-KumquatVerifierAttempt` (latest verdict mtime + 1) |
| 13 | Post-clobber repair | `Invoke-KumquatVerifierPatchGuard.ps1`, `Publish-KumquatWorkspaceDeliverables` |
| 14 | Full panel coverage | 600s guard, `Write-KumquatClobberSimulationEvidence`, `Invoke-KumquatGoalCompletion.ps1` |

**Oregon goal completion entry (headless):**
```powershell
$env:KUMQUAT_SCRATCH = "C:\path\to\scratch\implementer"
powershell -ExecutionPolicy Bypass -File symbiosis-relay\windows\kumquat\Invoke-KumquatGoalCompletion.ps1 -ScratchDir $env:KUMQUAT_SCRATCH
```

**Washington verify on `/kumquat`:**
```bash
cd ~/grok-hermes-symbiosis && git fetch origin && git checkout kumquat-2026-06-01-hygiene && git pull
chmod +x symbiosis-relay/linux/kumquat/invoke-kumquat-goal-completion.sh
bash symbiosis-relay/linux/kumquat/invoke-kumquat-goal-completion.sh
bash symbiosis-relay/linux/kumquat/invoke-kumquat-verification-harness.sh
bash ~/Synced/grok-mempalace-integration/symbiosis-relay/linux/tools/test-relay-structured-status.sh
# File RETURN.md below with receipts
```

**Pester contract (Oregon, after pull):** Core 11/0 + Smoke 1/0 = 12/0 in single `kumquat-pest-results.txt`.

**Honest GAP (unchanged):** surrogate `20260617-1113` + session `ade7ed50` Syncthing pending on OR rich.

**Washington has the ball.** (Pull `kumquat-2026-06-01-hygiene`, run linux mirror stubs + structured status test, file RETURN.md.)

<!-- Edited: 2026-06-23 22:40 | Device: Windows | By: Grok (/kumquat push to WA) --> Rounds 12-14 handoff extension. Bing bang boom. Signature per prime directive. Keep er goinnnn. Bust a nut.