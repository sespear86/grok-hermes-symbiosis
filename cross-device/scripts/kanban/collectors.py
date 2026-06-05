"""Read-only collectors for symbiosis handoff kanban (AUTON 6239aa70)."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from handoff_scaffold.log import HEADER_ROW_PATTERN

from sync_report.collectors import (
    STALE_HEARTBEAT_SECONDS,
    collect_presence,
    extract_open_items_top3,
    extract_status_excerpt,
    parse_handoff_rows,
)

from .paths import (
    archived_dir,
    handoff_log_path,
    handoffs_dir,
    open_items_path,
    status_md_path,
)

STDOUT_CAP = 8192
MAX_LOG_ROWS = 10_000
ARCHIVED_SCAN_LIMIT = 200
README_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+)$", re.MULTILINE)
BALL_HOLDER_RE = re.compile(
    r"\*\*(Washington|Oregon)\s+has\s+the\s+ball\.\*\*",
    re.IGNORECASE,
)
ID_DATE_PREFIX_RE = re.compile(r"^(\d{8})")


def normalize_status_token(s: str) -> str:
    """Casefold; strip; drop parenthetical tails for compare only."""
    base = s.strip().casefold()
    if "(" in base:
        base = base.split("(", 1)[0].strip()
    return base


def effective_status(log_status: str, readme_status: str | None, has_return: bool) -> str:
    if has_return:
        return "Completed (RETURN present)"
    return (readme_status or log_status).strip()


def column_for_card(
    *,
    effective: str,
    in_archived: bool,
    log_status: str,
    has_return: bool,
) -> str:
    """Evaluation order is fixed — do not reorder."""
    if in_archived:
        return "archived"
    if has_return:
        return "completed"
    el = effective.lower()
    ls = log_status.lower()
    if "archived" in el or "archived" in ls:
        return "archived"
    if "completed" in el or "completed" in ls:
        return "completed"
    if "awaiting" in el or "awaiting" in ls:
        return "awaiting"
    return "in_progress"


def extract_ball_holder(status_text: str) -> str | None:
    excerpt = extract_status_excerpt(status_text)
    for line in excerpt:
        m = BALL_HOLDER_RE.search(line)
        if m:
            return f"{m.group(1)} has the ball."
    last: str | None = None
    for line in status_text.splitlines():
        m = BALL_HOLDER_RE.search(line)
        if m:
            last = f"{m.group(1)} has the ball."
    return last


def _readme_text(readme_path: Path) -> str:
    if not readme_path.is_file():
        return ""
    return readme_path.read_text(encoding="utf-8", errors="replace")[:STDOUT_CAP]


def _readme_status(readme_path: Path) -> str | None:
    text = _readme_text(readme_path)
    m = README_STATUS_RE.search(text)
    return m.group(1).strip() if m else None


def _readme_short_description(readme_path: Path) -> str | None:
    """Fallback when LOG description cell is empty (DESIGN per-card enrichment)."""
    text = _readme_text(readme_path)
    if not text.strip():
        return None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
        if s.startswith("**Status:**"):
            continue
        if s and not s.startswith("#"):
            return s[:120]
    return None


def _resolve_folder(repo_root: Path, folder_id: str) -> tuple[Path | None, bool]:
    active = handoffs_dir(repo_root) / folder_id
    if active.is_dir():
        return active, False
    arch = archived_dir(repo_root) / folder_id
    if arch.is_dir():
        return arch, True
    return None, False


def _date_sort_key(row_date: str, folder_id: str) -> str:
    m = ID_DATE_PREFIX_RE.match(folder_id)
    if m:
        return m.group(1)
    digits = re.sub(r"\D", "", row_date)[:8]
    return digits or "00000000"


def _age_days(row_date: str, folder_id: str) -> int | None:
    key = _date_sort_key(row_date, folder_id)
    if len(key) != 8 or not key.isdigit():
        return None
    try:
        dt = datetime.strptime(key, "%Y%m%d").replace(tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - dt
        return max(0, delta.days)
    except ValueError:
        return None


def _card_from_row(
    repo_root: Path,
    row: dict[str, str],
    *,
    global_warnings: list[str],
) -> dict[str, Any]:
    folder_id = row["id"]
    card_warnings: list[str] = []
    folder_path, in_archived = _resolve_folder(repo_root, folder_id)
    has_return = bool(folder_path and (folder_path / "RETURN.md").is_file())
    readme_status = _readme_status(folder_path / "README.md") if folder_path else None
    log_status = row["status"]
    eff = effective_status(log_status, readme_status, has_return)
    column = column_for_card(
        effective=eff,
        in_archived=in_archived,
        log_status=log_status,
        has_return=has_return,
    )

    if row["date"].startswith("2099") or folder_id.startswith("2099"):
        global_warnings.append("verifier_smoke_dummy_row")
    if folder_path is None:
        card_warnings.append("missing_folder")
        global_warnings.append(f"log_folder_missing:{folder_id}")
    if (
        readme_status
        and log_status
        and column != "archived"
        and normalize_status_token(readme_status) != normalize_status_token(log_status)
    ):
        card_warnings.append("readme_log_status_mismatch")
        global_warnings.append(f"readme_log_status_mismatch:{folder_id}")

    desc = (row.get("description") or "").strip()
    if not desc and folder_path:
        desc = _readme_short_description(folder_path / "README.md") or ""
    if not desc:
        desc = row.get("description") or folder_id

    link = row.get("link") or f"[{folder_id}](./{folder_id}/)"
    return {
        "id": folder_id,
        "date": row["date"],
        "from": row["from"],
        "to": row["to"],
        "short_description": desc,
        "log_status": log_status,
        "readme_status": readme_status,
        "effective_status": eff,
        "column": column,
        "link": link,
        "folder_exists": folder_path is not None,
        "has_return": has_return,
        "age_days": _age_days(row["date"], folder_id),
        "warnings": card_warnings,
        "_sort_key": _date_sort_key(row["date"], folder_id),
        "_synthetic_archived": False,
    }


def _synthetic_archived_card(repo_root: Path, folder_id: str) -> dict[str, Any]:
    folder_path = archived_dir(repo_root) / folder_id
    readme_status = _readme_status(folder_path / "README.md")
    has_return = (folder_path / "RETURN.md").is_file()
    log_status = readme_status or "Archived"
    eff = effective_status(log_status, readme_status, has_return)
    return {
        "id": folder_id,
        "date": "",
        "from": "",
        "to": "",
        "short_description": folder_id,
        "log_status": log_status,
        "readme_status": readme_status,
        "effective_status": eff,
        "column": "archived",
        "link": f"[{folder_id}](./archived/{folder_id}/)",
        "folder_exists": True,
        "has_return": has_return,
        "age_days": _age_days("", folder_id),
        "warnings": ["folder_not_in_log"],
        "_sort_key": _date_sort_key("", folder_id),
        "_synthetic_archived": True,
    }


def build_kanban_warnings(
    *,
    presence: dict[str, Any] | None,
    cards: list[dict[str, Any]],
    log_header_drift: bool,
) -> list[str]:
    warnings: list[str] = []
    if log_header_drift:
        warnings.append("HANDOFF_LOG header drift; expected canonical table header")
    if presence:
        brother = presence.get("brother")
        if brother and brother.get("age_seconds") is not None:
            if brother["age_seconds"] > STALE_HEARTBEAT_SECONDS:
                warnings.append(
                    f"brother heartbeat stale ({int(brother['age_seconds'])}s > "
                    f"{STALE_HEARTBEAT_SECONDS}s)"
                )
        warnings.extend(presence.get("warnings") or [])
    seen: set[str] = set()
    for w in warnings:
        seen.add(w)
    for card in cards:
        for cw in card.get("warnings") or []:
            if cw not in seen:
                seen.add(cw)
    return list(seen)


def _strip_internal(card: dict[str, Any]) -> dict[str, Any]:
    out = dict(card)
    out.pop("_sort_key", None)
    out.pop("_synthetic_archived", None)
    return out


def _sort_archived_column(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """LOG-derived archived first (id desc), then synthesised archived-only (id desc)."""
    log_derived = [c for c in cards if not c.get("_synthetic_archived")]
    synthetic = [c for c in cards if c.get("_synthetic_archived")]
    log_derived.sort(key=lambda c: c["_sort_key"], reverse=True)
    synthetic.sort(key=lambda c: c["_sort_key"], reverse=True)
    return log_derived + synthetic


def collect_board(
    *,
    device: str,
    repo_root: Path,
    mempalace_root: Path,
    completed_limit: int = 5,
    include_presence: bool = True,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    global_warnings: list[str] = []
    coordination: dict[str, Any] = {
        "open_items_top3": None,
        "status_excerpt": [],
    }

    oi_path = open_items_path(repo_root)
    if oi_path.is_file():
        coordination["open_items_top3"] = extract_open_items_top3(
            oi_path.read_text(encoding="utf-8", errors="replace")
        )

    status_text = ""
    ball_holder: str | None = None
    st_path = status_md_path(repo_root)
    if st_path.is_file():
        status_text = st_path.read_text(encoding="utf-8", errors="replace")
        coordination["status_excerpt"] = extract_status_excerpt(status_text)
        ball_holder = extract_ball_holder(status_text)

    log_header_drift = False
    cards: list[dict[str, Any]] = []
    log_ids: set[str] = set()
    log_p = handoff_log_path(repo_root)
    if log_p.is_file():
        log_text = log_p.read_text(encoding="utf-8", errors="replace")
        if not HEADER_ROW_PATTERN.search(log_text):
            log_header_drift = True
        for row in parse_handoff_rows(log_text, MAX_LOG_ROWS):
            log_ids.add(row["id"])
            cards.append(
                _card_from_row(repo_root, row, global_warnings=global_warnings)
            )
    else:
        global_warnings.append(f"HANDOFF_LOG missing: {log_p}")

    arch_root = archived_dir(repo_root)
    if arch_root.is_dir():
        dirs = sorted(
            [p for p in arch_root.iterdir() if p.is_dir()],
            key=lambda p: p.name,
            reverse=True,
        )
        if len(dirs) > ARCHIVED_SCAN_LIMIT:
            global_warnings.append("scan_truncated")
            dirs = dirs[:ARCHIVED_SCAN_LIMIT]
        for p in dirs:
            if p.name not in log_ids:
                global_warnings.append(f"folder_not_in_log:{p.name}")
                cards.append(_synthetic_archived_card(repo_root, p.name))

    awaiting: list[dict[str, Any]] = []
    in_progress: list[dict[str, Any]] = []
    archived: list[dict[str, Any]] = []
    completed_all: list[dict[str, Any]] = []

    for card in cards:
        col = card["column"]
        if col == "awaiting":
            awaiting.append(card)
        elif col == "in_progress":
            in_progress.append(card)
        elif col == "archived":
            archived.append(card)
        elif col == "completed":
            completed_all.append(card)

    completed_all.sort(key=lambda c: c["_sort_key"], reverse=True)
    completed_shown = [_strip_internal(c) for c in completed_all[:completed_limit]]
    completed_omitted = max(0, len(completed_all) - len(completed_shown))

    presence: dict[str, Any] | None = None
    if include_presence:
        presence = collect_presence(mempalace_root, local_device=device)

    warnings = build_kanban_warnings(
        presence=presence,
        cards=cards,
        log_header_drift=log_header_drift,
    )
    for w in global_warnings:
        if w not in warnings:
            warnings.append(w)

    archived = _sort_archived_column(archived)

    return {
        "schema_version": 1,
        "meta": {
            "device": device,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "repo_root": str(repo_root),
            "mempalace_root": str(mempalace_root.resolve()),
            "ball_holder": ball_holder,
            "format": "md",
        },
        "presence": presence,
        "coordination": coordination,
        "columns": {
            "awaiting": [_strip_internal(c) for c in awaiting],
            "in_progress": [_strip_internal(c) for c in in_progress],
            "completed": completed_shown,
            "archived": [_strip_internal(c) for c in archived],
        },
        "counts": {
            "awaiting": len(awaiting),
            "in_progress": len(in_progress),
            "archived": len(archived),
            "completed_shown": len(completed_shown),
            "completed_total": len(completed_all),
            "total_log_rows": len(log_ids),
        },
        "truncation": {"completed_omitted": completed_omitted},
        "warnings": warnings,
    }


# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 6239aa70 batch1 review fixes) -->