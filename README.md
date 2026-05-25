# Grok Build ↔ Hermes Agent Symbiosis

**The ultimate local AI agent power couple.**  
Grok Build (xAI) + Hermes Agent (Nous Research) running on the same device, sharing the same primary model (grok-4.3 via xAI), deeply integrated for complementary superpowers.

**Status**: Actively configured and enhanced on this machine (2026 setup).

---

## Core Philosophy

- **Grok Build** = Deep specialist for software engineering, architecture, rigorous verification, professional artifact creation, parallel exploration, and high-stakes planning.
- **Hermes Agent** = Persistent, self-improving, long-horizon executor with world presence (gateway), kanban orchestration, massive skill library, cron automation, memory curation, and swarm capabilities.
- **Together**: Hand-off seamlessly. Grok designs and reviews; Hermes executes, persists, and connects to the world. Both powered by the same frontier Grok 4.3 model with excellent xAI native support in both.

This symbiosis turns two already-powerful systems into something greater than the sum.

---

## Current Shared Foundation (Pre-Symbiosis)

- Primary model in both: **grok-4.3** (Hermes via `xai-oauth` + SuperGrok; Grok Build native).
- Hermes plugins for xAI: image_gen, video_gen, web search, model proxy, auth.
- Grok Build: native xAI Imagine/Video generation tools + strong tool calling.
- Both support MCP (Model Context Protocol) — bidirectional potential.
- Hermes: 570+ built-in skills + optional + plugins; self-curating skills from experience.
- Grok Build: High-quality bundled SE skills (implement with multi-reviewer loops, design-doc writer/reviewer, check verifier, best-of-n parallel, docx/xlsx/pptx generators) + user skills + `/create-skill`.
- Hermes: Rich modern TUI, gateway (Telegram/Discord/Slack/WhatsApp/etc.), kanban swarms, worktree parallel agents, many terminal backends (Docker, SSH, Modal, Daytona...), cron, trajectory research tools.
- Grok Build: Plan mode, subagent spawning with specialized personas, structured todo discipline, surgical search_replace editing, background monitors/schedulers.
- User ecosystem: OpenClaw (predecessor, migrated), mission-control (Next.js control plane), GrokForge, .mempalace, extensive AI tooling.

---

## Symbiosis Layers Implemented

### 1. Invocation Bridges (Skills)

- **From Grok → Hermes**: `/hermes` (or `hermes` skill). Smart launch, resume with context, one-shot delegation, monitoring, handoff of plans/todos.
- **From Hermes → Grok**: `grok-build` / `grok-specialist` skill. Delegate heavy SE design, implement+review, verification, professional document generation, best-of-n exploration back to Grok Build CLI.

### 2. MCP Cross-Registration

- Grok config updated to consume Hermes MCP server (`hermes mcp serve`).
  - Enables Grok sessions to list/read/send Hermes gateway conversations, handle approvals, poll events via `search_tool` / `use_tool`.
- Recommendation + docs: Add powerful standard MCP servers to Hermes (GitHub, filesystem, etc.) via `hermes mcp add`.
- Grok's rich `grok_com_github` (42 tools) remains a Grok-session superpower; equivalent GitHub MCP easily added to Hermes for parity.

### 3. Context & State Sharing

- Skills encode explicit handoff protocols:
  - Export current Grok todos / design docs / code state → Hermes memory or prompt.
  - Hermes can "call grok" with structured task + artifacts.
- Shared workspace awareness (both respect same CWD, git worktrees, .env where appropriate).
- Future: scripts for memory/todo sync (todos ↔ Hermes memories / Honcho if used).

### 4. Workflow Specialization + Escalation

**Use Grok Build when**:
- Architecture / design doc needed (design loop with reviewer).
- Complex multi-file refactor or new feature (implement + reviewers + check verifier).
- Professional output (slides, spreadsheets, Word docs via pptx/xlsx/docx skills).
- Ambiguous or high-risk task → plan mode.
- Parallel what-if analysis (best-of-n).
- Surgical code review or verification subagent.

**Use Hermes when**:
- Long-running autonomous execution or monitoring.
- Need persistent presence on chat platforms (gateway).
- Kanban-driven multi-agent or human collab.
- Self-improving skills or experience curation over many sessions.
- Cron/scheduled reports or automations.
- Research batch trajectories or heavy browser/tool use.
- Swarm parallel work in isolated worktrees.

**Escalation patterns** (encoded in skills):
- Grok designs plan → hands to Hermes for execution + world delivery.
- Hermes hits wall on complex code → delegates back to Grok "grok-build implement this spec with reviews".
- Hermes gathers research → Grok synthesizes into polished deliverable.

### 5. Shared Resources & Extensions

- Central living doc: `~/grok-hermes-symbiosis/`
- Dedicated skills in both systems.
- Bridge scripts in `scripts/`.
- Config snippets in `configs/`.
- Recommended: Add GitHub MCP, other high-value MCPs to Hermes for tool parity on GitHub-heavy work.

---

## Quick Start / Daily Usage

### From Grok Build TUI (this session)

```
/skills hermes          # List or inject
/hermes launch          # Start fresh Hermes chat (inherits CWD + context)
/hermes resume          # Resume recent or pick
/hermes delegate "Long running task description + any plans/todos from here" 
/hermes one-shot "Quick question for Hermes agent" --model grok-4.3
/hermes monitor         # Tail logs or check kanban
/hermes gateway status
```

The skill will guide precise commands, context injection, and post-handoff follow-up.

### From Hermes

In any Hermes session (CLI or gateway):

```
/grok-build implement the following spec with full review loop: ...
/grok-build design new architecture for X following our patterns
/grok-build verify this change with check skill
/grok-build create professional pitch deck from this outline
/grok-specialist "Use best-of-n to explore 3 approaches..."
```

Hermes skill provides exact CLI invocation patterns (using `grok` binary with appropriate flags for headless or TUI).

### Hybrid Patterns

- `grok-hermes-delegate` (script): Prepares rich context (git status, recent todos if present, summary of current Grok thinking) and launches Hermes with preloaded skills + prompt.
- Kanban in Hermes + subagents in Grok: Orchestrate from Hermes board, spin Grok specialists for branches.
- Gateway + Grok: Talk to Hermes from phone → it delegates deep work to local Grok session.

---

## Installation / Activation (Already Applied)

1. Skills created:
   - `~/.grok/skills/hermes/SKILL.md`
   - `~/.hermes/skills/grok-build/SKILL.md`

2. MCP:
   - `~/.grok/config.toml` updated with Hermes MCP server entry.
   - Run `hermes mcp add ...` for desired servers (GitHub recommended for parity).

3. Symbiosis workspace:
   - `~/grok-hermes-symbiosis/` with docs + scripts.

4. Verify:
   - In Grok: `/skills` should show hermes.
   - In Hermes: `/skills` or `/grok-build` should be available (may require restart or skill reload).

5. Optional enhancements:
   - Share GitHub PAT safely between both (via env or gh auth).
   - Configure Hermes gateway for your preferred platforms.
   - Explore mission-control for web UI orchestration.

---

## Advanced / Future Extensions (Roadmap in this repo)

- Custom MCP server (Python FastMCP) that exposes select Grok Build capabilities (image/video gen, todo system, verification) to Hermes and vice versa.
- Bidirectional memory sync (Grok todos ↔ Hermes memory / Honcho peers).
- Shared skill curation: Grok-generated high-quality SE skills auto-ported or symlinked for Hermes.
- Plugin for Hermes that treats Grok Build as a "specialist subagent" via CLI RPC.
- Kanban + Grok subagent integration scripts.
- Evaluation harness: run same complex task through pure Grok, pure Hermes, and symbiotic mode; compare.

---

## Relevant Paths on This Device

**Hermes**:
- Binary/launcher: `~/.local/bin/hermes` → `~/.hermes/hermes-agent/venv/bin/hermes`
- Source (editable): `~/.hermes/hermes-agent/`
- User config: `~/.hermes/config.yaml`, `.env`
- User skills: `~/.hermes/skills/`
- Sessions / state: `~/.hermes/sessions/`, `state.db`
- MCP serve: `hermes mcp serve`
- Doctor: `hermes doctor`

**Grok Build**:
- Binary: `~/.grok/bin/grok` (or in PATH)
- Config: `~/.grok/config.toml`
- User skills: `~/.grok/skills/`
- Bundled powerful skills: `~/.grok/bundled/skills/` (implement, review, design, etc.)
- Docs: `~/.grok/docs/user-guide/`
- Sessions / memory: `~/.grok/sessions/`, `memory/`

**Symbiosis**:
- `~/grok-hermes-symbiosis/`
- Skills as above

**User Assets**:
- GitHub token reference: `~/Documents/Github_Hermes_Token.txt`
- xAI reference: `~/Documents/Hermes_Agent_Xai_API.txt`
- Related projects: `~/mission-control/`, `~/openclaw/`, `~/GrokForge/`, `~/.mempalace/`

---

## Contributing to the Symbiosis

- Improve the skills (they are the primary interface).
- Add bridge scripts that make handoff frictionless.
- Propose / implement custom MCP bridges.
- Update this README and docs/ as patterns evolve.
- Share successful workflow examples in `shared/`.

Both systems are actively developed (Hermes by Nous Research, Grok Build TUI by xAI). This local symbiosis is user-owned and evolves with your workflows.

---

**Powered by grok-4.3 + excellent local tooling.**  
The best of frontier reasoning + agentic persistence + specialized SE discipline, all on one machine.

For questions or to activate a specific pattern, just ask in either interface using the symbiosis skills.
