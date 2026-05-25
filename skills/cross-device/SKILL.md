---
name: cross-device
description: >
  Manage cross-device collaboration between the Oregon Linux machine and the Windows 11 machine in the shared Grok-Hermes symbiosis.
  Use for handoffs, sync status, creating shared context packages, posting to the joint chat, and maintaining the "one extended environment" feel across both devices.
metadata:
  short-description: "Cross-device / brother collab orchestration"
  symbiosis: true
  distributed: true
---

# Cross-Device Collaboration Skill (Grok Build)

This skill coordinates work between the two physical machines running the Grok + Hermes symbiosis.

## Core Concepts

- **Handoff**: Explicit transfer of a task, plan, or partial result from one machine/agent to the other.
- **Sync Report**: Snapshot of current state (git, recent work, open todos, Hermes sessions) that can be posted to the shared chat.
- **Shared Chat Bus**: The Discord/Telegram/Slack channel where both humans + both Hermes gateways live. This is the primary real-time coordination channel.
- **Synced Folders**: The `grok-hermes-symbiosis` repo + selected project folders kept in sync via Syncthing.

## Common Commands & Patterns

### Create a Handoff Package
```bash
# From Grok
/cross-device handoff "Task description" --to oregon --include-todos --include-plan ./docs/current-plan.md
```

This creates a dated folder under `cross-device/handoffs/` with:
- Summary
- Relevant files / diffs
- Current todos export
- Instructions for the receiving side (which skill to invoke, etc.)

### Post Status to Shared Chat (via Hermes gateway)
When Hermes is running with gateway connected to the joint channel, ask Hermes to post updates.

### Generate Sync Report
```bash
/cross-device sync-report
```
Outputs a clean markdown block suitable for pasting into the shared chat or committing to the symbiosis repo.

### Pull Latest Integration Layer
```bash
cd ~/grok-hermes-symbiosis && git pull
# Then reload skills in both Grok and Hermes
```

## Cross-Device Handoff Protocol (Use This Language)

When handing work across machines, always include:

1. `[CROSS-DEVICE HANDOFF]` + direction (Linux → Windows or Windows → Oregon/Linux)
2. Clear task + success criteria
3. Links or paths to artifacts in the shared synced folders or GitHub
4. Which skill the receiving side should use (`grok-build`, `hermes`, `implement`, `design`, etc.)
5. Preferred coordination channel (usually the shared chat)

Example handoff prompt:
```
[CROSS-DEVICE HANDOFF: Windows → Oregon Linux]

Task: Review the architecture in grok-hermes-symbiosis/cross-device/LIVE_SYNC_DESIGN.md and produce a detailed implementation plan for the kanban sync strategy.

Context: See the design doc + recent commits.

Use full design + review loop. When complete, post summary + plan to the shared Discord channel and create a handoff package in cross-device/handoffs/.

Escalate any blockers back using the cross-device skill.
```

## Windows vs Linux Notes

- Paths differ: Use relative paths inside the symbiosis repo when possible.
- Hermes home on Windows: `%LOCALAPPDATA%\hermes`
- PowerShell bridges: `grok-hermes-delegate.ps1` and `hermes-grok-delegate.ps1`
- Prefer the shared repo scripts after cloning.

## Related

- Full design: `cross-device/LIVE_SYNC_DESIGN.md`
- Windows setup: `windows/SETUP_FOR_BROTHER.md`
- Syncthing recommendations: (to be added in cross-device/syncthing-guide.md)
- Shared chat: Configure Hermes gateway on both machines to the same channel.
