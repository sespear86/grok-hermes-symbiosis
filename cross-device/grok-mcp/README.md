# symbiosis-grok-mcp (AUTON b045169b)

Hermes-native **FastMCP** stdio server that wraps `grok -z` for Grok Build specialist workflows (implement, design, check, review, best-of-n). Structured results use the `SYMBIOSIS_RESULT` JSON fence (see `DESIGN.md`).

| Doc | Path |
|-----|------|
| Design | [`DESIGN.md`](./DESIGN.md) |
| Research | [`../auton-artifacts/b045169b/RESEARCH_SYNTHESIS.md`](../auton-artifacts/b045169b/RESEARCH_SYNTHESIS.md) |
| Hermes MCP block | [`../../configs/hermes-mcp-recommendations.md`](../../configs/hermes-mcp-recommendations.md) |
| Mirror | [`../MIRROR_KITS_AND_INFRASTRUCTURE.md`](../MIRROR_KITS_AND_INFRASTRUCTURE.md) §16 |

## Install (Washington / Oregon)

```bash
cd ~/grok-hermes-symbiosis/cross-device/grok-mcp
python3.11 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest tests -q
```

Windows: `py -3.11 -m venv .venv` then `.\.venv\Scripts\pip install -e ".[dev]"`.

## Register with Hermes

```bash
hermes mcp add grok \
  --command "$HOME/grok-hermes-symbiosis/cross-device/grok-mcp/.venv/bin/python" \
  --args "-m" "grok_mcp" \
  --env GROK_BIN="$HOME/.grok/bin/grok" \
  --env SYMBIOSIS_REPO_ROOT="$HOME/grok-hermes-symbiosis" \
  --startup-timeout-sec 15 \
  --tool-timeout-sec 3600

hermes mcp test grok
hermes mcp list   # tools appear as grok__grok_implement, etc.
```

Oregon: use `C:\Users\spear\grok-hermes-symbiosis` paths and `Scripts\python.exe` (see configs + MIRROR §16).

## Run manually (stdio)

```bash
./symbiosis-grok-mcp --help
./symbiosis-grok-mcp    # blocks — same as python -m grok_mcp
```

Optional PATH shim:

```bash
ln -sf ~/grok-hermes-symbiosis/cross-device/grok-mcp/symbiosis-grok-mcp ~/bin/symbiosis-grok-mcp
```

Windows: `.\windows\scripts\Invoke-SymbiosisGrokMcp.ps1 -Help`

## MCP tools (v1)

| Hermes tool name | Purpose |
|------------------|---------|
| `grok__grok_implement` | implement + reviewers (default timeout 3600s) |
| `grok__grok_design` | design doc loop (1800s) |
| `grok__grok_check` | verification / VERDICT (600s) |
| `grok__grok_review` | code review (1200s) |
| `grok__grok_best_of_n` | parallel exploration (2400s) |

Prefer these over shell `hermes-grok-delegate` when Hermes lists `grok__*` tools.

## Tests & smoke

```bash
cd cross-device/grok-mcp
.venv/bin/pytest tests -q
./tools/smoke_grok_mcp.sh
# optional live: GROK_MCP_SMOKE_LIVE=1 ./tools/smoke_grok_mcp.sh
```

## Security notes

- No `shell=True`; user text goes only into the `-z` prompt string.
- `cwd` / `context_paths` confined under `SYMBIOSIS_REPO_ROOT` (or `GROK_MCP_ALLOWED_ROOTS`).
- `SYMBIOSIS_GROK_DELEGATE_YOLO=1` adds `--always-approve` — symbiosis hosts only.

<!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON b045169b PR5–PR7) -->