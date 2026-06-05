"""Subprocess bridge to `grok -z` with fixed argv (AUTON b045169b)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from grok_mcp.config import ALLOWLIST_EXTRA_ARGV, Settings
from grok_mcp.logging_util import log_event


class BridgeArgumentError(ValueError):
    """Disallowed extra_argv token."""


def _validate_extra_argv(extra_argv: list[str] | None) -> list[str]:
    if not extra_argv:
        return []
    out: list[str] = []
    i = 0
    while i < len(extra_argv):
        token = extra_argv[i]
        if token not in ALLOWLIST_EXTRA_ARGV:
            raise BridgeArgumentError(f"extra argv not allowlisted: {token}")
        out.append(token)
        if token in ("--best-of-n", "--effort") and i + 1 < len(extra_argv):
            nxt = extra_argv[i + 1]
            if not nxt.startswith("-"):
                out.append(nxt)
                i += 1
        i += 1
    return out


def run_grok_z(
    *,
    prompt: str,
    cwd: Path,
    timeout_sec: int,
    settings: Settings | None = None,
    extra_argv: list[str] | None = None,
) -> subprocess.CompletedProcess[str]:
    settings = settings or Settings.from_environ()
    grok = settings.grok_bin
    argv: list[str] = [grok, "-z", prompt]
    if os.environ.get("SYMBIOSIS_GROK_DELEGATE_YOLO") == "1":
        argv.append("--always-approve")
    argv.extend(_validate_extra_argv(extra_argv))

    log_event(
        "grok_invoke_start",
        cwd=str(cwd),
        timeout_sec=timeout_sec,
        argv0=grok,
    )
    try:
        proc = subprocess.run(
            argv,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False,
        )
    except subprocess.TimeoutExpired:
        log_event("grok_invoke_timeout", cwd=str(cwd), timeout_sec=timeout_sec)
        raise

    log_event(
        "grok_invoke_end",
        cwd=str(cwd),
        exit_code=proc.returncode,
        stdout_len=len(proc.stdout or ""),
        stderr_len=len(proc.stderr or ""),
    )
    return proc