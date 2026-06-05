"""Parse SYMBIOSIS_RESULT from grok stdout (AUTON b045169b)."""

from __future__ import annotations

import json
import os
import re
from typing import Any, TypedDict

from grok_mcp.config import Settings

RAW_TAIL_CAP = 8192
SUMMARY_FALLBACK_TAIL = 4096

_FENCE_RE = re.compile(
    r"```json\s+SYMBIOSIS_RESULT\s*\n(.*?)\n```",
    re.DOTALL | re.IGNORECASE,
)
_VERDICT_RE = re.compile(r"^VERDICT:\s*(PASS|FAIL)\s*$", re.IGNORECASE | re.MULTILINE)


class Artifact(TypedDict, total=False):
    path: str
    role: str


class ToolResult(TypedDict, total=False):
    ok: bool
    summary: str
    verdict: str
    artifacts: list[Artifact]
    worktree_path: str | None
    exit_code: int
    raw_tail: str
    elapsed_sec: float
    parse_warning: str
    notes: str


def _parse_json_block(text: str) -> dict[str, Any] | None:
    m = _FENCE_RE.search(text)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            pass
    for candidate in reversed(list(_iter_json_objects(text))):
        if "summary" in candidate:
            return candidate
    return None


def _iter_json_objects(text: str):
    for match in re.finditer(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text, re.DOTALL):
        try:
            obj = json.loads(match.group(0))
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            yield obj


def _verdict_from_prose(stdout: str) -> str | None:
    m = _VERDICT_RE.search(stdout)
    if not m:
        return None
    return "pass" if m.group(1).upper() == "PASS" else "fail"


def extract_result(
    *,
    stdout: str,
    exit_code: int,
    elapsed_sec: float,
    timed_out: bool = False,
    require_check_verdict: bool = False,
) -> ToolResult:
    if timed_out:
        tail = (stdout or "")[-RAW_TAIL_CAP:]
        return {
            "ok": False,
            "summary": "grok -z timed out",
            "verdict": "timeout",
            "artifacts": [],
            "worktree_path": None,
            "exit_code": exit_code,
            "raw_tail": tail,
            "elapsed_sec": elapsed_sec,
            "parse_warning": "timeout",
        }

    parsed = _parse_json_block(stdout or "")
    prose_verdict = _verdict_from_prose(stdout or "") if require_check_verdict else None
    tail = (stdout or "")[-RAW_TAIL_CAP:]

    if parsed:
        ok = bool(parsed.get("ok", exit_code == 0))
        summary = str(parsed.get("summary") or "")
        verdict = str(parsed.get("verdict") or ("complete" if ok else "fail"))
        if prose_verdict:
            verdict = prose_verdict
        artifacts = parsed.get("artifacts") or []
        if not isinstance(artifacts, list):
            artifacts = []
        wt = parsed.get("worktree_path")
        result: ToolResult = {
            "ok": ok,
            "summary": summary,
            "verdict": verdict,
            "artifacts": artifacts,
            "worktree_path": wt if isinstance(wt, (str, type(None))) else None,
            "exit_code": exit_code,
            "raw_tail": tail,
            "elapsed_sec": elapsed_sec,
        }
        if parsed.get("notes"):
            result["notes"] = str(parsed["notes"])
        return result

    summary_tail = (stdout or "")[-SUMMARY_FALLBACK_TAIL:].strip()
    ok = exit_code == 0
    verdict = prose_verdict or ("complete" if ok else "fail")
    return {
        "ok": ok,
        "summary": summary_tail or "(no parseable summary)",
        "verdict": verdict,
        "artifacts": [],
        "worktree_path": None,
        "exit_code": exit_code,
        "raw_tail": tail,
        "elapsed_sec": elapsed_sec,
        "parse_warning": "missing SYMBIOSIS_RESULT fence; used exit code + tail",
    }


def maybe_save_stdout(stdout: str, settings: Settings, correlation: str) -> None:
    if not settings.save_stdout or not stdout:
        return
    os.makedirs(settings.log_dir, exist_ok=True)
    path = os.path.join(settings.log_dir, f"{correlation}.stdout")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(stdout)