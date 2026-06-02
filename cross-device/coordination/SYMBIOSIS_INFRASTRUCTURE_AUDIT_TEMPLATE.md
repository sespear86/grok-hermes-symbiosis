# Symbiosis Infrastructure Audit Template

**Purpose:** Provide a repeatable, standardized checklist so both Oregon and Washington can perform identical, thorough audits of their local symbiosis stack. This enables clean comparison and systematic application of the Mirrorability Prime.

**Instructions:**
- Run this audit on your machine.
- For every item, note: Present / Missing / Partial / Version / Notes / Path.
- Be brutally honest.
- At the end, produce a "Gaps vs Mirrorability Prime" section.
- Date and sign the audit.

---

## 1. Core Living Repos & Projects
- grok-hermes-symbiosis repo (path, git remote, recent commits, untracked items)
- grok-mempalace-integration (rich project) location and git state
- .mempalace folder
- Any other related git repos

## 2. Agent Runtimes
- Grok Build TUI installation and version
- Hermes agent installation and version
- Primary model in use for both

## 3. Reciprocal Skills
- Grok-side hermes skill (path + last updated)
- Hermes-side grok-build / grok-specialist skill (path + last updated)
- Any other symbiosis-related skills

## 4. MCP & Cross-Registration
- Hermes MCP registered in Grok config
- Any GitHub / other MCPs on Hermes side
- pctowah-eng / sespear86 collaborator status on relevant repos

## 5. Cross-Device File Sync (Syncthing)
- Syncthing installation locations
- Folders currently being synced (symbiosis repo, rich project, Mempalace, etc.)
- .stignore / .stfolder state
- Any known sync conflicts or issues

## 6. Symbiosis-Relay Stack (Local Receiver Side)
- Windows/Linux receiver/activator scripts location
- Fast heartbeat pusher / watchdog
- Any local services, scheduled tasks, or launchers for the relay

## 7. Bust-a-Nut Infrastructure (Full Stack)
- All .grok/hooks related to bust-a-nut, relay, symmetry, health
- UI Idle Monitor, SessionStart prompts, fast path components
- Any Windows scheduled tasks or services

## 8. Mempalace Retention & Capture
- Capture hooks (SessionEnd, PreCompact, etc.)
- Rich vs lightweight capture scripts
- Source tagging (oregon-windows-grok-build, etc.)
- Any local Mempalace instances

## 9. Device Presence & Heartbeats
- Mempalace/symbiosis/device-presence/ folder contents
- Latest Oregon and Washington heartbeats
- Current declared mode (Paired / Solo / Option B)

## 10. Git / Auth / Remote Access
- SSH keys present (primary vs Pi deploy, etc.)
- Current remote URLs on key repos
- Collaborator status (pctowah-eng / sespear86)
- Any known auth workarounds or hybrid git models

## 11. Windows / Platform Specific
- Delegate scripts in PATH (in/)
- Grok hooks (full list + what they call)
- Any Windows services / Task Scheduler entries
- Environment variables or tokens related to symbiosis

## 12. Documentation & Coordination State
- Latest receipt (name + date)
- coordination/ folder (status.md, instructions files, OPEN_ITEMS, etc.)
- Any active backup / archive folders
- PRs or branches related to current hygiene wave

## 13. Backup / Archive / Noise State
- Any .rebase-backup-* or similar folders
- Old handoff directories still present
- .sync-conflict or ~syncthing~ files

## 14. Running / Health State (at time of audit)
- Key processes running (Hermes, Syncthing, any relay components)
- Last known relay health
- Any obvious broken hooks or failing scripts

---

## Final Sections (Mandatory)

### Gaps vs Mirrorability Prime
List every item that exists on this machine but would be painful or impossible for the brother machine to stand up from current artifacts alone.

### Mirrorability Action Items
For each gap above, note the minimal set of artifacts (scripts, docs, configs, one-liners) that must be delivered to the other side.

### Audit Metadata
- Date:
- Machine: Oregon / Washington
- Auditor:
- Signature:

**All 7 primes + Mirrorability Prime + exact signatures followed.**
