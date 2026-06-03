# OPERATIONS — Washington Activator (symbiosis-relay)

## Run
```bash
export SYMBIOSIS_SHARED=...
python3 washington_activator.py            # loop
python3 washington_activator.py --once
python3 washington_activator.py --health
python3 washington_activator.py --status
```

## Service
systemctl --user restart washington-activator.service
journalctl --user -u washington-activator -f

## Health
- `relay-health.sh` (rich)
- status/washington/status.json (enriched: health_ok, beacon_age, last_*_rc)
- beacon in device-presence/

## Failure
- pending-prompts/<corr>.md (ready paste)
- failed/ dir (task snapshots)
- logs/washington_activator.jsonl + .log

## Update (after git edit)
cp .../washington_activator.py .../activator_core.py .../task_schema.py $SYMBIOSIS_SHARED/symbiosis-relay/
systemctl --user restart washington-activator.service

**Washington has the ball.** (Monitor first prod traffic.)
<!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (auton 19557e65) -->
