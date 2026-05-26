# Cross-Device Live Sync & Collaboration Layer

**Vision**: Make the Oregon Linux machine and the Windows 11 machine feel as close as possible to a single coherent environment for joint projects — while preserving the ability for either person (or agent) to work independently when needed.

This document designs the "Distributed Symbiosis" on top of the local Grok ↔ Hermes symbiosis.

---

## Core Principles

1. **Git is the source of truth** for all code, plans, designs, and serious work.
2. **Live file sync** (Syncthing or equivalent) for project assets, skills, scripts, and context that benefit from immediacy.
3. **Hermes Gateway + shared chat** is the human + agent coordination bus (notifications, status, handoffs, approvals).
4. **Explicit handoff protocols** via the `cross-device` and `brother-collab` skills.
5. **Selective sync** — never blindly sync full agent homes (secrets, machine-specific state, large caches).
6. **Idempotent + observable** — anyone or any agent can ask "what's the current state across devices?"

---

## Recommended Architecture (Current Best Feasible)

### Layer 1: Code & Integration — Git (Shared GitHub Repo)

- One or more shared GitHub repositories for the actual projects.
- The `grok-hermes-symbiosis` repo itself (private recommended) as the **integration and tooling layer**.
  - Both machines clone it.
  - Skills, bridge scripts, sync helpers, and this design live here.
  - Frequent pulls (or a small watcher script).

### Layer 2: Live File & Context Sync — Syncthing (Primary)

**Why Syncthing**:
- Real-time bidirectional sync with conflict resolution.
- Works great Windows ↔ Linux.
- Per-folder control + ignore patterns.
- Runs locally, no central server required.
- Resumes after disconnects.

**Recommended Synced Folders** (start conservative):

| Folder Purpose                  | Sync? | Notes |
|--------------------------------|-------|-------|
| `grok-hermes-symbiosis`        | Yes   | Core — skills, scripts, docs, cross-device tools |
| Joint project root(s)          | Yes   | With .stignore for node_modules, .venv, builds, secrets |
| Exported context / handoffs    | Yes   | `cross-device/handoffs/` or similar |
| Personal notes / scratch       | No    | Or separate "shared-notes" folder |
| Full `~/.hermes` or `%LOCALAPPDATA%\hermes` | No | Too many secrets + machine state |
| Full `~/.grok`                 | No    | Same reason |
| Large model caches / downloads | No    | Wasteful |

**Ignore patterns** (example `.stignore`):
```
node_modules
.venv
__pycache__
dist
build
*.log
.env*
secrets/
**/.git
```

### Layer 3: Agent & Human Coordination — Hermes Gateway

- Both machines run the Hermes gateway connected to the **same shared chat** (Discord, Telegram, Slack, etc.).
- Agents and humans post status, handoffs, and questions in a dedicated thread or channel.
- Example messages:
  - `[CROSS-DEVICE] Linux → Windows: Design for X complete in grok-hermes-symbiosis/docs/X-design.md. Please review + implement with grok-build.`
  - Oregon machine can then pick it up via its local Hermes or Grok.

This gives "live updates" for intent and progress without needing a custom realtime protocol yet.

### Layer 4: Structured Handoff & Context Export

Custom skills + scripts for:
- Exporting current todos / plans / recent decisions as markdown.
- Summarizing the last N Hermes sessions.
- Creating "handoff packages" in the shared synced folder.
- "Sync report" command that both sides can run.

### Layer 5: Future / Advanced (Build as Needed)

- Lightweight coordination MCP server (exposed carefully).
- Shared Honcho or other memory backend (if both want the same long-term user/project model).
- Custom "team kanban" on top of Hermes kanban (or export Hermes kanban to markdown/git).
- Automated sync watchers + notifications via Hermes cron.
- Conflict detection helpers for simultaneous edits.

---

## Concrete Next Pieces to Implement

1. **Cross-device skills** (Grok + Hermes versions) — encode the handoff language and protocols.
2. **Context export / import scripts** (PowerShell + bash).
3. **Syncthing setup guide** with exact recommended folders and ignore patterns.
4. **"Sync report" skill/script** — both sides can run it and post the result to the shared chat.
5. **Kanban sync strategy** — how to keep a shared task view (Hermes kanban.db is SQLite; careful syncing or export-to-git is safer initially).
6. **Package / environment parity helpers** (for tools, skills, and project-specific runtimes).

---

## Immediate Action Plan (This Setup)

- [ ] Both machines have the local symbiosis applied (using the Windows guide + Linux baseline).
- [ ] Shared private GitHub repo for `grok-hermes-symbiosis` created and cloned on both sides.
- [ ] Syncthing installed and paired on both machines; initial folders shared.
- [ ] Hermes gateway on both machines joined to the same chat.
- [ ] First successful cross-device handoff using the new skills/scripts.
- [ ] Sync report script created and tested.

This document lives in the shared repo so both sides stay aligned on the design.

---

**Status**: Initial design. Being actively built as part of the Grok-Hermes symbiosis project.
