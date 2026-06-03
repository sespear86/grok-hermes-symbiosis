# Symbiosis Relay — Washington Activator (nervous source)

Core Washington-side listener/activator + injection + presence for the live Hermes Symbiosis Relay.

**AUTON**: 19557e65 (harden & productionize)

See DESIGN.md, RESEARCH_SYNTHESIS.md, OPERATIONS.md (future), and parent coordination/.

## Quick
```bash
SYMBIOSIS_SHARED=... python3 washington_activator.py --health
SYMBIOSIS_SHARED=... python3 washington_activator.py --once
python3 inject_hermes_task.py "test message"
```

## Production
- Runs as `washington-activator.service` (user)
- Expects rich `~/Synced/.../symbiosis-relay/` at runtime (cp from this git source for updates)
- Health via --health + status.json + relay-health.sh

All 7 primes + Mirrorability + exact sigs.

**Washington has the ball.**
