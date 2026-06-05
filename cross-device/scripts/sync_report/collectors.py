"""Read-only collectors for symbiosis sync report (AUTON 355e3993)."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from handoff_scaffold.log import HEADER_ROW_PATTERN, find_table_insert_index

from .paths import (
    brother_presence_filename,
    coordination_dir,
    handoff_log_path,
    local_presence_filename,
    open_items_path,
    presence_dir,
    relay_health_script,
    status_md_path,
)

STDOUT_CAP = 8192
GIT_TIMEOUT = 10
SYNCTHING_FOLDER_TIMEOUT = 3
SYNCTHING_SYSTEM_TIMEOUT = 5
RELAY_TIMEOUT = 15
RELAY_MAX_LINES = 40
CONFLICT_WALK_LIMIT = 500
STALE_HEARTBEAT_SECONDS = 3600
OPEN_ITEMS_SECTION = "## Current Top 3 Priorities (Symbiosis-Wide)"
DATA_ROW_RE = re.compile(r"^\|.+\|$")
SEPARATOR_ROW_RE = re.compile(r"^\|[-:\s|]+\|$")
UPDATE_LINE_RE = re.compile(r"^\*\*Update \(")
HEARTBEAT_RE = re.compile(
    r"^\*\*Last Heartbeat:\*\*\s*(.+)$",
    re.MULTILINE | re.IGNORECASE,
)
MODE_RE = re.compile(
    r"^\*\*Current Mode:\*\*\s*(.+)$",
    re.MULTILINE | re.IGNORECASE,
)


def run_argv(
    argv: list[str],
    *,
    timeout: float,
    cwd: Path | None = None,
) -> tuple[int, str]:
    """Run subprocess without shell; cap combined output."""
    try:
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(cwd) if cwd else None,
            check=False,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        return 127, str(exc)[:STDOUT_CAP]
    combined = (proc.stdout or "") + (proc.stderr or "")
    if len(combined) > STDOUT_CAP:
        combined = combined[:STDOUT_CAP] + "\n...[truncated]"
    return proc.returncode, combined


def collect_git(repo_root: Path) -> dict[str, Any]:
    repo = repo_root.resolve()
    out: dict[str, Any] = {
        "available": True,
        "branch": None,
        "ahead": 0,
        "behind": 0,
        "dirty_count": 0,
        "warnings": [],
    }
    rc, status = run_argv(
        ["git", "-C", str(repo), "status", "-sb"],
        timeout=GIT_TIMEOUT,
    )
    if rc != 0:
        out["available"] = False
        out["warnings"].append(f"git status failed (rc={rc})")
        return out
    lines = status.strip().splitlines()
    if lines:
        head = lines[0]
        if head.startswith("## "):
            rest = head[3:].strip()
            if "..." in rest:
                branch_part, tracking = rest.split("...", 1)
                out["branch"] = branch_part.strip()
                m = re.search(r"\[ahead\s+(\d+)(?:,\s*behind\s+(\d+))?\]", tracking)
                if m:
                    out["ahead"] = int(m.group(1))
                    if m.group(2):
                        out["behind"] = int(m.group(2))
                m2 = re.search(r"\[behind\s+(\d+)\]", tracking)
                if m2 and not m:
                    out["behind"] = int(m2.group(1))
            else:
                out["branch"] = rest
    dirty_lines = [ln for ln in lines[1:] if ln.strip()]
    out["dirty_count"] = len(dirty_lines)

    rc2, upstream = run_argv(
        [
            "git",
            "-C",
            str(repo),
            "rev-list",
            "--left-right",
            "--count",
            "@{u}...HEAD",
        ],
        timeout=GIT_TIMEOUT,
    )
    if rc2 == 0 and upstream.strip():
        parts = upstream.strip().split()
        if len(parts) == 2:
            try:
                out["behind"] = int(parts[0])
                out["ahead"] = int(parts[1])
            except ValueError:
                pass
    return out


def _syncthing_binary() -> str | None:
    which = shutil.which("syncthing")
    if which:
        return which
    home_bin = Path.home() / "bin" / "syncthing"
    if home_bin.is_file():
        return str(home_bin)
    return None


def collect_syncthing(*, no_syncthing: bool) -> dict[str, Any]:
    result: dict[str, Any] = {
        "available": False,
        "reason": None,
        "folders": [],
        "system": None,
        "warnings": [],
    }
    if no_syncthing:
        result["reason"] = "skipped by flag"
        return result
    binary = _syncthing_binary()
    if not binary:
        result["reason"] = "syncthing binary not found"
        result["warnings"].append("install syncthing or use --no-syncthing")
        return result
    raw = os.environ.get("SYMBIOSIS_SYNCTHING_FOLDERS", "").strip()
    if not raw:
        result["reason"] = "SYMBIOSIS_SYNCTHING_FOLDERS unset"
        result["warnings"].append(
            "set SYMBIOSIS_SYNCTHING_FOLDERS (comma-separated folder IDs, max 5)"
        )
        return result
    ids = [x.strip() for x in raw.split(",") if x.strip()][:5]
    result["available"] = True
    for fid in ids:
        rc, text = run_argv(
            [binary, "cli", "show", "folder", fid],
            timeout=SYNCTHING_FOLDER_TIMEOUT,
        )
        state = "unknown"
        lower = text.lower()
        if "error" in lower:
            state = "error"
        elif "syncing" in lower:
            state = "syncing"
        elif "idle" in lower:
            state = "idle"
        result["folders"].append(
            {"id": fid, "state": state, "rc": rc, "excerpt": text.strip()[:500]}
        )
    rc_sys, sys_out = run_argv(
        [binary, "cli", "show", "system"],
        timeout=SYNCTHING_SYSTEM_TIMEOUT,
    )
    if rc_sys == 0:
        result["system"] = sys_out.strip()[:1000]
    return result


def parse_handoff_rows(log_text: str, max_rows: int) -> list[dict[str, str]]:
    lines = log_text.splitlines()
    try:
        idx = find_table_insert_index(lines)
    except ValueError:
        return []
    rows: list[dict[str, str]] = []
    for line in lines[idx:]:
        s = line.strip()
        if not s or SEPARATOR_ROW_RE.match(s):
            continue
        if not DATA_ROW_RE.match(s):
            break
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 7:
            continue
        rows.append(
            {
                "date": cells[0],
                "id": cells[1],
                "from": cells[2],
                "to": cells[3],
                "description": cells[4],
                "status": cells[5],
                "link": cells[6],
            }
        )
        if len(rows) >= max_rows:
            break
    return rows


# Regression alias removed: use parse_handoff_rows (public, AUTON 6239aa70).


def extract_open_items_top3(text: str) -> str | None:
    if OPEN_ITEMS_SECTION not in text:
        return None
    start = text.index(OPEN_ITEMS_SECTION)
    chunk = text[start + len(OPEN_ITEMS_SECTION) :]
    lines: list[str] = []
    for line in chunk.splitlines():
        if line.startswith("## "):
            break
        lines.append(line)
    body = "\n".join(lines).strip()
    return body or None


def extract_status_excerpt(text: str) -> list[str]:
    no_comments: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            continue
        if "<!--" in stripped and "-->" in stripped:
            continue
        no_comments.append(line)
    for i, line in enumerate(no_comments):
        if UPDATE_LINE_RE.match(line.strip()):
            block: list[str] = [line]
            blank_run = 0
            for follow in no_comments[i + 1 :]:
                fs = follow.strip()
                if fs.startswith("<!--"):
                    break
                if not fs:
                    blank_run += 1
                    if blank_run >= 3:
                        break
                    block.append(follow)
                    continue
                blank_run = 0
                block.append(follow)
                if len(block) >= 8:
                    break
            return block[:8]
    fallback: list[str] = []
    for line in no_comments:
        s = line.strip()
        if not s or s.startswith("<!--"):
            continue
        fallback.append(line)
        if len(fallback) >= 10:
            break
    return fallback


def _heartbeat_age_seconds(text: str, path: Path) -> float | None:
    m = HEARTBEAT_RE.search(text)
    if m:
        raw = m.group(1).strip()
        for fmt in (
            "%Y-%m-%dT%H:%M:%S.%f%z",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
        ):
            try:
                dt = datetime.strptime(raw[:26], fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return max(0.0, (datetime.now(timezone.utc) - dt).total_seconds())
            except ValueError:
                continue
    try:
        mtime = path.stat().st_mtime
        return max(0.0, time.time() - mtime)
    except OSError:
        return None


def collect_coordination(repo_root: Path, *, handoff_rows: int) -> dict[str, Any]:
    out: dict[str, Any] = {
        "handoff_log": {"rows": [], "warnings": []},
        "open_items_top3": None,
        "status_excerpt": [],
        "warnings": [],
    }
    log_p = handoff_log_path(repo_root)
    if log_p.is_file():
        log_text = log_p.read_text(encoding="utf-8", errors="replace")
        if not HEADER_ROW_PATTERN.search(log_text):
            out["handoff_log"]["warnings"].append(
                "HANDOFF_LOG header drift; expected canonical table header"
            )
        out["handoff_log"]["rows"] = parse_handoff_rows(log_text, handoff_rows)
    else:
        out["warnings"].append(f"HANDOFF_LOG missing: {log_p}")

    oi = open_items_path(repo_root)
    if oi.is_file():
        oi_text = oi.read_text(encoding="utf-8", errors="replace")
        excerpt = extract_open_items_top3(oi_text)
        if excerpt is None:
            out["warnings"].append("OPEN_ITEMS Top 3 section not found")
        else:
            out["open_items_top3"] = excerpt
    else:
        out["warnings"].append(f"OPEN_ITEMS missing: {oi}")

    st = status_md_path(repo_root)
    if st.is_file():
        st_text = st.read_text(encoding="utf-8", errors="replace")
        out["status_excerpt"] = extract_status_excerpt(st_text)
    else:
        out["warnings"].append(f"status.md missing: {st}")
    return out


def collect_presence(
    mempalace_root: Path,
    *,
    local_device: str,
) -> dict[str, Any]:
    pres_dir = presence_dir(mempalace_root)
    local_name = local_presence_filename(local_device)
    brother_name = brother_presence_filename(local_device)
    out: dict[str, Any] = {
        "mempalace_root": str(mempalace_root),
        "local": None,
        "brother": None,
        "warnings": [],
    }

    def read_one(name: str, role: str) -> dict[str, Any] | None:
        p = pres_dir / name
        if not p.is_file():
            out["warnings"].append(f"presence file missing: {p}")
            return None
        text = p.read_text(encoding="utf-8", errors="replace")
        age = _heartbeat_age_seconds(text, p)
        mode_m = MODE_RE.search(text)
        return {
            "file": str(p),
            "role": role,
            "mode_hint": mode_m.group(1).strip() if mode_m else None,
            "age_seconds": age,
            "paired_hint": "paired" in text.lower(),
        }

    out["local"] = read_one(local_name, "local")
    out["brother"] = read_one(brother_name, "brother")
    return out


def collect_conflicts(repo_root: Path) -> dict[str, Any]:
    count = 0
    samples: list[str] = []
    root = repo_root.resolve()
    for i, p in enumerate(root.rglob(".sync-conflict-*")):
        if i >= CONFLICT_WALK_LIMIT:
            break
        if p.is_file() or p.is_dir():
            count += 1
            if len(samples) < 5:
                try:
                    samples.append(str(p.relative_to(root)))
                except ValueError:
                    samples.append(str(p))
    truncated = count >= CONFLICT_WALK_LIMIT
    return {"count": count, "samples": samples, "truncated": truncated}


def collect_coordination_dirty(repo_root: Path) -> int:
    coord = coordination_dir(repo_root)
    rc, status = run_argv(
        ["git", "-C", str(repo_root.resolve()), "status", "--porcelain", "--", str(coord)],
        timeout=GIT_TIMEOUT,
    )
    if rc != 0:
        return 0
    return len([ln for ln in status.splitlines() if ln.strip()])


def collect_relay(rich_root: Path, *, enabled: bool) -> dict[str, Any] | None:
    if not enabled:
        return None
    script = relay_health_script(rich_root)
    if not script.is_file():
        return {
            "available": False,
            "warnings": [f"relay-health.sh missing: {script}"],
            "lines": [],
        }
    rc, combined = run_argv(
        ["bash", str(script)],
        timeout=RELAY_TIMEOUT,
        cwd=script.parent,
    )
    lines = combined.splitlines()[:RELAY_MAX_LINES]
    return {"available": rc == 0, "rc": rc, "lines": lines}


def build_warnings(
    *,
    device: str,
    presence: dict[str, Any],
    conflicts: dict[str, Any],
    coordination_dirty: int,
    git_dirty: int,
) -> list[str]:
    warnings: list[str] = []
    brother = presence.get("brother")
    if brother and brother.get("age_seconds") is not None:
        if brother["age_seconds"] > STALE_HEARTBEAT_SECONDS:
            warnings.append(
                f"brother heartbeat stale ({int(brother['age_seconds'])}s > {STALE_HEARTBEAT_SECONDS}s)"
            )
    if coordination_dirty > 0:
        warnings.append(f"uncommitted changes under coordination/ ({coordination_dirty} paths)")
    if conflicts.get("count", 0) > 0:
        warnings.append(f".sync-conflict-* count: {conflicts['count']}")
    if git_dirty > 50:
        warnings.append(f"git dirty file count high ({git_dirty}); showing count only")
    return warnings


def collect_report(
    *,
    device: str,
    repo_root: Path,
    rich_root: Path,
    mempalace_root: Path,
    handoff_rows: int,
    no_syncthing: bool,
    include_relay: bool,
) -> dict[str, Any]:
    git = collect_git(repo_root)
    syncthing = collect_syncthing(no_syncthing=no_syncthing)
    coordination = collect_coordination(repo_root, handoff_rows=handoff_rows)
    presence = collect_presence(mempalace_root, local_device=device)
    conflicts = collect_conflicts(repo_root)
    relay = collect_relay(rich_root, enabled=include_relay)
    coord_dirty = collect_coordination_dirty(repo_root)
    warnings = build_warnings(
        device=device,
        presence=presence,
        conflicts=conflicts,
        coordination_dirty=coord_dirty,
        git_dirty=git.get("dirty_count", 0),
    )
    warnings.extend(git.get("warnings", []))
    warnings.extend(syncthing.get("warnings", []))
    warnings.extend(coordination.get("warnings", []))
    warnings.extend(coordination.get("handoff_log", {}).get("warnings", []))
    warnings.extend(presence.get("warnings", []))
    if relay and isinstance(relay, dict):
        warnings.extend(relay.get("warnings", []))

    return {
        "meta": {
            "device": device,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "repo_root": str(repo_root.resolve()),
            "rich_root": str(rich_root.resolve()),
            "mempalace_root": str(mempalace_root.resolve()),
        },
        "git": git,
        "syncthing": syncthing,
        "coordination": coordination,
        "presence": presence,
        "conflicts": conflicts,
        "warnings": warnings,
        "relay": relay,
    }


# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 6239aa70 batch1) -->