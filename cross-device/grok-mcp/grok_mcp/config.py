"""Environment-backed configuration for symbiosis-grok-mcp (AUTON b045169b)."""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_TIMEOUT_IMPLEMENT = 3600
DEFAULT_TIMEOUT_DESIGN = 1800
DEFAULT_TIMEOUT_CHECK = 600
DEFAULT_TIMEOUT_REVIEW = 1200
DEFAULT_TIMEOUT_BEST_OF_N = 2400
MAX_TIMEOUT_SEC = 7200


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    grok_bin: str
    repo_root: str | None
    max_timeout_sec: int
    save_stdout: bool
    log_dir: str

    @classmethod
    def from_environ(cls) -> Settings:
        home = os.path.expanduser("~")
        return cls(
            grok_bin=os.environ.get("GROK_BIN", "grok").strip() or "grok",
            repo_root=(os.environ.get("SYMBIOSIS_REPO_ROOT") or "").strip() or None,
            max_timeout_sec=_env_int("GROK_MCP_MAX_TIMEOUT", MAX_TIMEOUT_SEC),
            save_stdout=os.environ.get("GROK_MCP_SAVE_STDOUT", "").strip() == "1",
            log_dir=os.environ.get(
                "GROK_MCP_LOG_DIR",
                os.path.join(home, ".grok", "logs", "grok-mcp"),
            ),
        )


def clamp_timeout(requested: int | None, default: int, settings: Settings) -> int:
    """Cap per-invocation timeout to env max."""
    value = default if requested is None else requested
    if value < 1:
        value = default
    return min(value, settings.max_timeout_sec)


ALLOWLIST_EXTRA_ARGV: frozenset[str] = frozenset(
    {
        "--best-of-n",
        "--effort",
        "--check",
        "--no-alt-screen",
    }
)