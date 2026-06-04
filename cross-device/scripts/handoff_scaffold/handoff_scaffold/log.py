"""Atomic HANDOFF_LOG.md row insertion (newest first)."""
from __future__ import annotations

import re
import tempfile
from pathlib import Path

EXPECTED_HEADER_CELLS = [
    "Date",
    "ID",
    "From",
    "To",
    "Short Description",
    "Status",
    "Link",
]

HEADER_ROW_PATTERN = re.compile(
    r"^\|\s*Date\s*\|\s*ID\s*\|\s*From\s*\|\s*To\s*\|\s*Short Description\s*\|\s*Status\s*\|\s*Link\s*\|",
    re.MULTILINE,
)


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|")


def format_header_line() -> str:
    inner = "|".join(f" {c} " for c in EXPECTED_HEADER_CELLS)
    return f"|{inner}|"


def find_table_insert_index(lines: list[str]) -> int:
    for i, line in enumerate(lines):
        if HEADER_ROW_PATTERN.match(line.strip()):
            j = i + 1
            if j < len(lines) and re.match(r"^\|[-:\s|]+\|$", lines[j].strip()):
                return j + 1
            return i + 1
    raise ValueError(
        "malformed HANDOFF_LOG table; expected header:\n" + format_header_line()
    )


def build_row(
    *,
    date_display: str,
    folder_id: str,
    from_device: str,
    to_device: str,
    description: str,
    status: str = "In Progress",
) -> str:
    link = f"[{folder_id}](./{folder_id}/)"
    cells = [
        date_display,
        folder_id,
        from_device,
        to_device,
        description[:120],
        status,
        link,
    ]
    escaped = [escape_cell(c) for c in cells]
    inner = "|".join(f" {c} " for c in escaped)
    return f"|{inner}|"


def insert_log_row(
    log_path: Path,
    row_line: str,
    *,
    dry_run: bool = False,
) -> None:
    text = log_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    idx = find_table_insert_index([ln.rstrip("\n") for ln in lines])
    new_lines = lines[:idx] + [row_line + "\n"] + lines[idx:]
    if dry_run:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(
        dir=str(log_path.parent), prefix=".handoff_log.", suffix=".tmp"
    )
    try:
        with open(fd, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        Path(tmp).replace(log_path)
    except Exception:
        Path(tmp).unlink(missing_ok=True)
        raise