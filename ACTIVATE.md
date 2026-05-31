# Grok ↔ Hermes Symbiosis — Activation & Quick Reference

Everything below has been set up on this device.

## What Was Created / Changed

1. **Grok skill** (primary bridge from here):
   - `~/.grok/skills/hermes/SKILL.md`
   - Activate: `/hermes` or `/skills hermes`

2. **Hermes skill** (reciprocal bridge):
   - `~/.hermes/skills/grok-build/SKILL.md`
   - Activate in Hermes: `/grok-build` or mention the skill

3. **MCP cross link**:
   - `~/.grok/config.toml` now registers `hermes` MCP server via `hermes mcp serve`
   - In any Grok session, use `/mcps` or `search_tool` to discover Hermes messaging/approval tools.

4. **Bridge scripts** (in PATH via symlinks):
   - `grok-hermes-delegate "task..."` — rich-context handoff to Hermes
   - `hermes-grok-delegate "task..."` — reciprocal to Grok

5. **Living documentation & extensions**:
   - `~/grok-hermes-symbiosis/README.md` (full architecture + usage)
   - `scripts/`, `configs/`, `docs/`

## Immediate Things You Can Do

### In This Grok Build Session
```
/hermes launch
/hermes delegate "Long running research + implementation task with these requirements..."
grok-hermes-delegate "Hand this entire plan to Hermes for execution and gateway delivery"
```

Then ask Hermes (once running) to use its `grok-build` skill for any deep SE work.

### From Hermes (any interface)
Use the `grok-build` skill for:
- Architecture / design docs
- Full implement + reviewer loops
- Verification (`check`)
- Parallel exploration (`best-of-n`)
- Professional slides / spreadsheets / specs

### Strengthen Hermes Tooling (Recommended)
```bash
hermes mcp add github --command npx --args "-y @modelcontextprotocol/server-github" --env GITHUB_PERSONAL_ACCESS_TOKEN=...
```
(See `configs/hermes-mcp-recommendations.md`)

### Test the MCP Bridge
In a Grok session:
- `/mcps` → look for "hermes"
- `search_tool` with query containing "hermes" or "conversation"
- Use the discovered tools to read/send via Hermes gateway channels

## Daily Symbiosis Pattern (Example)

1. Start in Grok → use design or implement to produce solid spec + plan + initial code.
2. `grok-hermes-delegate "Execute the attached plan to completion. Deliver status via gateway/kanban. Escalate blockers via grok-build."`
3. Hermes runs autonomously (or via gateway on your phone).
4. When Hermes needs heavy review/verification/polish → it (or you) calls `grok-build`.
5. Grok finishes specialist piece → hands results back (or user pastes into Hermes).
6. Hermes continues / delivers / schedules follow-ups.

## Verification Commands

- Grok: `grok inspect` (or `/skills`) — hermes skill should appear.
- Hermes: `hermes doctor` (already healthy), `hermes mcp list`
- Both: `hermes --version`, `grok --version`

## Next-Level (Future Work in this Dir)

- Custom MCP server exposing more Grok-specific tools (image gen, todo mgmt, verification) to Hermes.
- Memory/todo sync scripts.
- Kanban + Grok subagent orchestration helpers.
- Evaluation harness comparing pure vs symbiotic performance on complex tasks.

---

**The symbiosis is live.** Use the skills and scripts. Improve them as you discover better patterns.

Full details: `~/grok-hermes-symbiosis/README.md`
