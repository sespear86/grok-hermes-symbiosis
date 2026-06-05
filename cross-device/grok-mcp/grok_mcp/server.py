"""FastMCP stdio server — grok_implement, design, check, review, best_of_n (AUTON b045169b)."""

from __future__ import annotations

import subprocess
import time
import uuid
from typing import Any

from mcp.server.fastmcp import FastMCP

from grok_mcp.bridge import run_grok_z
from grok_mcp.config import (
    DEFAULT_TIMEOUT_BEST_OF_N,
    DEFAULT_TIMEOUT_CHECK,
    DEFAULT_TIMEOUT_DESIGN,
    DEFAULT_TIMEOUT_IMPLEMENT,
    DEFAULT_TIMEOUT_REVIEW,
    Settings,
    clamp_timeout,
)
from grok_mcp.logging_util import log_event
from grok_mcp.parse import ToolResult, extract_result, maybe_save_stdout
from grok_mcp.paths import PathValidationError, resolve_confined, validate_context_paths
from grok_mcp import prompts

mcp = FastMCP("grok")


def _settings() -> Settings:
    return Settings.from_environ()


def _execute(
    *,
    tool_name: str,
    task: str,
    cwd: str | None,
    timeout_sec: int | None,
    default_timeout: int,
    workflow_label: str,
    context_paths: list[str] | None = None,
    constraints: str | None = None,
    require_check_verdict: bool = False,
    extra_argv: list[str] | None = None,
) -> dict[str, Any]:
    settings = _settings()
    timeout = clamp_timeout(timeout_sec, default_timeout, settings)
    try:
        work_cwd = resolve_confined(cwd, settings, default_cwd=True)
        ctx = validate_context_paths(context_paths, settings)
    except PathValidationError as exc:
        log_event("path_validation_failed", tool=tool_name, error=str(exc))
        return {
            "ok": False,
            "summary": str(exc),
            "verdict": "fail",
            "artifacts": [],
            "worktree_path": None,
            "exit_code": -1,
            "raw_tail": "",
            "elapsed_sec": 0.0,
        }

    prompt = prompts.build_prompt(
        tool_name=tool_name,
        task=task,
        cwd=work_cwd,
        workflow_label=workflow_label,
        context_paths=ctx,
        constraints=constraints,
        require_check_verdict=require_check_verdict,
    )
    correlation = uuid.uuid4().hex[:12]
    t0 = time.monotonic()
    timed_out = False
    exit_code = -1
    stdout = ""

    try:
        proc = run_grok_z(
            prompt=prompt,
            cwd=work_cwd,
            timeout_sec=timeout,
            settings=settings,
            extra_argv=extra_argv,
        )
        exit_code = proc.returncode
        stdout = proc.stdout or ""
        maybe_save_stdout(stdout, settings, correlation)
    except subprocess.TimeoutExpired:
        timed_out = True
        exit_code = -9

    elapsed = time.monotonic() - t0
    result: ToolResult = extract_result(
        stdout=stdout,
        exit_code=exit_code,
        elapsed_sec=elapsed,
        timed_out=timed_out,
        require_check_verdict=require_check_verdict,
    )
    log_event(
        "tool_complete",
        tool=tool_name,
        ok=result.get("ok"),
        verdict=result.get("verdict"),
        elapsed_sec=elapsed,
    )
    return dict(result)


@mcp.tool()
def grok_implement(
    task: str,
    effort: int = 1,
    cwd: str | None = None,
    context_paths: list[str] | None = None,
    timeout_sec: int | None = None,
) -> dict[str, Any]:
    """Delegate implementation to Grok Build (implement skill, worktree + review loop)."""
    effort = max(1, min(5, effort))
    return _execute(
        tool_name="grok_implement",
        task=task,
        cwd=cwd,
        timeout_sec=timeout_sec,
        default_timeout=DEFAULT_TIMEOUT_IMPLEMENT,
        workflow_label=prompts.workflow_implement(effort),
        context_paths=context_paths,
        extra_argv=["--effort", str(effort)],
    )


@mcp.tool()
def grok_design(
    task: str,
    constraints: str | None = None,
    cwd: str | None = None,
    open_questions_allowed: bool = True,
    timeout_sec: int | None = None,
) -> dict[str, Any]:
    """Delegate architecture/design to Grok Build design skill."""
    return _execute(
        tool_name="grok_design",
        task=task,
        cwd=cwd,
        timeout_sec=timeout_sec,
        default_timeout=DEFAULT_TIMEOUT_DESIGN,
        workflow_label=prompts.workflow_design(open_questions_allowed),
        constraints=constraints,
    )


@mcp.tool()
def grok_check(
    focus: str,
    cwd: str | None = None,
    timeout_sec: int | None = None,
) -> dict[str, Any]:
    """Independent verification via Grok check-work skill."""
    return _execute(
        tool_name="grok_check",
        task=focus,
        cwd=cwd,
        timeout_sec=timeout_sec,
        default_timeout=DEFAULT_TIMEOUT_CHECK,
        workflow_label=prompts.workflow_check(),
        require_check_verdict=True,
    )


@mcp.tool()
def grok_review(
    task: str,
    effort: int = 1,
    cwd: str | None = None,
    timeout_sec: int | None = None,
) -> dict[str, Any]:
    """Code review via Grok review skill."""
    effort = max(1, min(5, effort))
    return _execute(
        tool_name="grok_review",
        task=task,
        cwd=cwd,
        timeout_sec=timeout_sec,
        default_timeout=DEFAULT_TIMEOUT_REVIEW,
        workflow_label=prompts.workflow_review(effort),
        extra_argv=["--effort", str(effort)],
    )


@mcp.tool()
def grok_best_of_n(
    task: str,
    n: int,
    cwd: str | None = None,
    timeout_sec: int | None = None,
) -> dict[str, Any]:
    """Explore N approaches via grok --best-of-n."""
    n = max(2, min(5, n))
    return _execute(
        tool_name="grok_best_of_n",
        task=task,
        cwd=cwd,
        timeout_sec=timeout_sec,
        default_timeout=DEFAULT_TIMEOUT_BEST_OF_N,
        workflow_label=prompts.workflow_best_of_n(n),
        extra_argv=["--best-of-n", str(n)],
    )


def run_stdio() -> None:
    """Start stdio MCP server for Hermes."""
    mcp.run(transport="stdio")