"""SYMBIOSIS ESCALATION prompts + per-tool workflow labels (AUTON b045169b)."""

from __future__ import annotations

from pathlib import Path

from grok_mcp.paths import git_snippet

JSON_CONTRACT_FOOTER = """
MCP output contract — your FINAL message MUST end with:

```json SYMBIOSIS_RESULT
{
  "ok": true,
  "summary": "...",
  "verdict": "complete|pass|fail|timeout",
  "artifacts": [{"path": "...", "role": "..."}],
  "worktree_path": null,
  "notes": ""
}
```
"""

CHECK_VERDICT_LINE = """
For this check workflow, also include a line in your prose:
VERDICT: PASS
or
VERDICT: FAIL
"""


def _context_block(paths: list[Path]) -> str:
    if not paths:
        return "(none)"
    return "\n".join(f"- {p}" for p in paths)


def build_prompt(
    *,
    tool_name: str,
    task: str,
    cwd: Path,
    workflow_label: str,
    context_paths: list[Path] | None = None,
    constraints: str | None = None,
    require_check_verdict: bool = False,
) -> str:
    ctx_paths = context_paths or []
    git = git_snippet(cwd)
    extra = f"\nConstraints:\n{constraints}\n" if constraints else ""
    verdict = CHECK_VERDICT_LINE if require_check_verdict else ""

    return f"""SYMBIOSIS ESCALATION from Hermes Agent to Grok Build TUI (MCP grok__{tool_name}).

Working directory: {cwd}
Git context:
{git}

Task:
{task}
{extra}
Context paths (read if relevant):
{_context_block(ctx_paths)}

Required Grok workflow: {workflow_label}
{verdict}
{JSON_CONTRACT_FOOTER}
"""


def workflow_implement(effort: int = 1) -> str:
    return f"implement with --effort {effort} (full implement-review-fix loop, worktree isolation)"


def workflow_design(open_questions_allowed: bool = True) -> str:
    oq = "allowed" if open_questions_allowed else "discouraged — resolve via design doc"
    return f"design (full design-doc + reviewer loop; open questions {oq})"


def workflow_check() -> str:
    return "check-work / independent verification on the stated focus"


def workflow_review(effort: int = 1) -> str:
    return f"review with --effort {effort}"


def workflow_best_of_n(n: int) -> str:
    return f"implement or solve task with --best-of-n {n} for pivotal approach selection"