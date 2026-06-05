# BATCH3 — AUTON 3694a72b (launchers + Windows PS)

**Date:** 2026-06-04  
**Worktree:** `/tmp/wt-3694a72b-dashboard` (branch `auton-3694a72b-dashboard`)

## Delivered

| Artifact | Path |
|----------|------|
| WA launcher | `cross-device/scripts/start-handoff-dashboard.sh` |
| OR Get- | `windows/scripts/Get-SymbiosisHandoffDashboard.ps1` |
| OR start- | `windows/scripts/start-handoff-dashboard.ps1` |
| Pester | `windows/scripts/Get-SymbiosisHandoffDashboard.Tests.ps1` |
| Packaging | `pyproject.toml` → **0.3.0**, `README.md` launcher lines |

## Self-verification (PASS)

```bash
bash -n cross-device/scripts/start-handoff-dashboard.sh
cd cross-device/scripts && pytest tests -q -k handoff_dashboard   # 25 passed
./symbiosis-handoff-dashboard --device "Washington Linux" \
  --repo-root /tmp/wt-3694a72b-dashboard --check-only --no-presence  # exit 0
./start-handoff-dashboard.sh --device "Washington Linux" \
  --repo-root /tmp/wt-3694a72b-dashboard --check-only --no-presence  # exit 0; no long-lived PID
```

**PowerShell:** `pwsh` not installed on WA host — Pester file includes AST parse tests + flag-mapping tests (run on OR Kumquat per MIRROR §14).

## Notes

- Lock: `/tmp/symbiosis-handoff-dashboard.lock` stores **server PID** after `nohup`.
- Log: `/tmp/symbiosis-handoff-dashboard.log`
- No `shell=True` in new PS/Python; bash invokes `python3` directly.
- `BindAddress` maps to CLI `--host` (avoids automatic `$Host` collision).

**Batch 3 launchers + PS impl complete in wt. Self-tests (sh smoke + Pester syntax) PASS. Ready for full review + docs batch. Washington has the ball.**

<!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 3694a72b implementer batch3) -->