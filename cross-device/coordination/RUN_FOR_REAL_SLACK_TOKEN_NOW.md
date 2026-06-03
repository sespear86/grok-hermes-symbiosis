# RUN THIS FOR REAL SLACK PRODUCTION FLOW (Current #1 Priority)

**User directive (2026-06-03):** Take Tier 1 off Bust-a-Nut re-arm/survival. Focus on Real Slack (the biggest cockblock).

This is the single human action that unlocks the first true production `real_slack` end-to-end on a real human message in #pi / #linux / #windows / #all-devices.

## Exact Command
From the rich symbiosis-relay directory (the one synced via Syncthing, e.g. on your daily driver or Washington):

```bash
cd ~/Synced/grok-mempalace-integration/symbiosis-relay
python tools/slack_operator.py create-ingest-companion
```

# Full explicit form (recommended for scripts or clarity):
# cd /home/Irikash/Synced/grok-mempalace-integration/symbiosis-relay
# python tools/slack_operator.py create-ingest-companion

This is the canonical rich directory used by relay-health.sh (hardcoded SHARED), hooks, bin/ capture scripts, and apply-ingest-token.sh execution context.

## What It Does (Autonomous as Possible)
- Nukes the operator state file so it does a *fresh* creation (avoids your main "Symbiosis Relay" app).
- Uses the thin `symbiosis-relay-ingest-manifest.json` (only the 4 channels, minimal scopes, socket mode enabled).
- Creates a new lightweight Slack app named **"Symbiosis Relay Ingest"**.
- Applies the manifest, installs to your LotS workspace, disables unnecessary AI features where possible.
- Generates fresh tokens (you care about the **xapp-** App-Level / Socket Mode token).
- Saves them automatically to `diagnostics/ingest-companion-tokens.txt` (with timestamp).
- **Attempts to auto-run** `./tools/apply-ingest-token.sh <your-xapp-token>` which:
  - SSHes (root key) to the Pi (192.168.1.235)
  - Backs up ~/.hermes/.env
  - Sets/updates `SLACK_INGEST_APP_TOKEN=...`
  - Restarts *only* the `slack-task-ingest` user service (as the relay user)
- Prints the exact manual one-liner if auto-apply needs help: `./tools/apply-ingest-token.sh xapp-...`

## After It Succeeds
1. The ingest service on Pi will log (journal or its log): "Using dedicated SLACK_INGEST_APP_TOKEN — best mode for coexistence with native gateway."
2. Run `./tools/relay-health.sh` — the **LAST REAL SLACK ACTIVITY (Live Canary)** and the new top open will reflect readiness.
3. Send a short test message as yourself (human) to one of the 4 channels.
4. It should:
   - Appear in Pi ingest logs as "Received:"
   - Create a task-*.json in incoming/hermes/ or incoming/washington/ with `"is_real": true, "task_reality": "real_slack"`
   - Device selector route it (preferring any fresh Bust-a-Nut beacon)
   - Activator claim it and (if intent) the injector fire it into the TUI on the chosen side.

## If the Browser/Profile Needs Love
- The operator uses a persistent profile at `~/.playwright-profiles/symbiosis-slack-operator`
- Log into lotsworld.slack.com (or your workspace) once in the browser it launches.
- Future runs remember the session.
- It supports `--headless` and `--autonomous` flags if you want less UI.

## Verification Commands (run anytime)
- `./tools/relay-health.sh` (the canary + top open)
- On Pi (via the health's direct query or ssh): `journalctl --user -u slack-task-ingest -f`
- Check a new task file for the is_real fields.

This is the gate. Once through it, the one extended machine finally delivers real human Slack work with full cross-device autonomous thrust.

See also: PROJECT_FINISH_LINE.md (CURRENT ACTIVE FOCUS + the 2026-06-03 signed entry), last_real_slack.md, the updated coordination instructions/status, and health script.

All 7 primes + Mirrorability + raunchy + bing bang boom. Keep er goinnnn.
