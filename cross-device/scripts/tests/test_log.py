"""HANDOFF_LOG insertion."""
from __future__ import annotations

from handoff_scaffold.log import build_row, escape_cell, insert_log_row
from handoff_scaffold.paths import handoff_log_path


def test_escape_pipe():
    assert escape_cell("a|b") == r"a\|b"


def test_insert_row_newest_first(repo_root):
    log_p = handoff_log_path(repo_root)
    before = log_p.read_text(encoding="utf-8")
    row = build_row(
        date_display="2026-06-04",
        folder_id="20260604-9999-Unit-Test-Row",
        from_device="Washington Linux",
        to_device="Oregon Windows",
        description="unit test",
    )
    insert_log_row(log_p, row, dry_run=False)
    after = log_p.read_text(encoding="utf-8")
    assert "20260604-9999-Unit-Test-Row" in after
    # New row should appear before first data row from original log
    idx_new = after.index("20260604-9999-Unit-Test-Row")
    idx_old = after.index("| 2026-05-25 |")
    assert idx_new < idx_old
    log_p.write_text(before, encoding="utf-8")