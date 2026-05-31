# Handoff Package

**ID:** 20260531-0015-Mirrorability-Relay-Ingest-Production-Oregon
**From:** Washington Linux
**To:** Oregon Windows
**Date:** 2026-05-31
**Status:** In Progress (ready for Oregon Kumquat)

## Context

Washington has been running heavy live "bust a nut" production testing with real human Slack messages in #all-devices. This exposed and forced two major production hardenings on the central Symbiosis Relay:

1. The dedicated `slack-task-ingest.service` (the thin Socket Mode listener that turns real human messages into `is_real:true / task_reality:real_slack` tasks) had never been installed as a persistent systemd unit on the Pi. It only existed as transient manual runs from late May 29.

2. After deploying the permanent service during the first live human test, a second real message ("another slack") revealed that the current listener (using the main `SLACK_APP_TOKEN`) connects but does not receive actual message events. This is the expected next gap on the path to reliable real Slack → dispatch.

All of this was executed under explicit Bust a Nut autonomy while fulfilling the Mirrorability Prime in real time.

## Task / Request for Oregon

On your next Kumquat, ingest this handoff + the top of `windows-instructions.md` + the updated `MIRROR_KITS_AND_INFRASTRUCTURE.md`. Your primary goals:

- Understand the current production relay architecture after two real human tests.
- Verify you have the latest receiver + beacon + Bust a Nut tooling for when the Pi router sends you real `real_slack` tasks.
- Be ready to participate in the next phase (creating the dedicated ingest companion app + token when the human runs the operator tool).

## What Has Already Been Done (Washington / Pi)

- Deployed a proper root `slack-task-ingest.service` on the Pi (modeled on the working `symbiosis-relay.service`, using the hermes-agent venv + `.hermes/.env`, `Restart=always`).
- Added a prominent "INGEST COMPANION EVENT FRESHNESS" detector + silence WARNING to `relay-health.sh` (journal-based, now first-class observability).
- Performed and fully documented two live human production tests ("hello or something" and "another slack") with exact diagnosis.
- Updated all coordination nervous system files + the master mirror kit.

## Relevant Artifacts Delivered for Mirrorability

- Exact `slack-task-ingest.service` unit content (see MIRROR_KITS section below + the one now running on Pi).
- New health detector logic in `symbiosis-relay/tools/relay-health.sh`.
- Full incident record in the PRODUCTION SLACK REALITY CHECK section of health output.
- Updated top of `windows-instructions.md` with executable current-state briefing + recommended actions.

## Success Criteria

- [ ] Oregon Kumquat has read and understood the current relay production reality (two live human tests + permanent ingest service + remaining dedicated-app gap).
- [ ] Oregon's local Bust a Nut / receiver / beacon stack is verified up to date with the latest from the rich project `windows/` mirror kit.
- [ ] Oregon is ready to act when the dedicated ingest companion app + `SLACK_INGEST_APP_TOKEN` is created (via `slack_operator.py create-ingest-companion`).

## Preferences / Constraints

- Follow the immutable sub-agent loop for any non-trivial work.
- Crank the raunchy depraved wit in all artifacts and signatures (Prime #2).
- Use exact `<!-- Edited: YYYY-MM-DD HH:MM | Device: Windows | By: Grok -->` signatures on every meaningful edit.
- Prefer the dedicated ingest app path over trying to make the main token work for both gateway + ingest.

## Handoff Notes

The Pi is now in a much stronger production state for real human messages than it was 24 hours ago. The permanent ingest service is the direct result of real human testing + Bust a Nut. The next real message after a proper dedicated ingest app/token is live will be the first true end-to-end `real_slack` success.

Washington is carrying the current autonomous thrust. Oregon should Kumquat soon to stay in sync.

## Relevant Memory (Mempalace)

- `/symbiosis/three-primes.md`
- `/symbiosis/usage-pattern.md`
- `/symbiosis/recent-decisions.md` (especially the relay production wave)
- `/symbiosis/git-gotchas.md`
- Coordination files: `linux-instructions.md`, `windows-instructions.md`, `status.md`, `MIRROR_KITS_AND_INFRASTRUCTURE.md`
- Rich project: `symbiosis-relay/` (especially the new health detector and the windows/ mirror kit)

---

**Mirrorability Prime fully activated for this handoff.** All new production reality (the permanent ingest service + health observability) has been documented with exact unit content, deployment steps, and verification in the master mirror kit and the top of this handoff target's instructions file.

<!-- Edited: 2026-05-31 00:15 | Device: Linux | By: Grok --> Mirrorability handoff prepped for Oregon. Two live human tests + permanent ingest service + new silence detector all delivered with full recipes. The one extended machine just got its relay production reality raunchily symmetric on paper. Keep er goinnnn, you handoff-prepping degenerates. -->