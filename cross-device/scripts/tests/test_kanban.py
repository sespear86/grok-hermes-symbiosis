"""Tests for symbiosis-handoff-kanban (AUTON 6239aa70)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from kanban.collectors import (
    _readme_short_description,
    _sort_archived_column,
    build_kanban_warnings,
    collect_board,
    column_for_card,
    effective_status,
    extract_ball_holder,
    normalize_status_token,
)
from kanban.paths import archived_dir, handoffs_dir
from kanban.render import render_board, render_json, render_md
from sync_report.collectors import parse_handoff_rows

SCRIPTS = Path(__file__).resolve().parents[1]
KANBAN_PKG = SCRIPTS / "kanban"
SHIM = SCRIPTS / "symbiosis-kanban"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
REPO_ROOT = Path(__file__).resolve().parents[3]

JSON_KEYS = {
    "schema_version",
    "meta",
    "presence",
    "coordination",
    "columns",
    "counts",
    "truncation",
    "warnings",
}


def test_parse_handoff_rows_public_api():
    text = (FIXTURES / "kanban_handoff_log.md").read_text(encoding="utf-8")
    rows = parse_handoff_rows(text, 10)
    assert len(rows) == 3
    assert rows[0]["id"].startswith("2099")


@pytest.mark.parametrize(
    "in_archived,has_return,log_status,effective,expected",
    [
        (False, True, "In Progress", "In Progress", "completed"),
        (True, False, "In Progress", "In Progress", "archived"),
        (False, False, "Completed", "In Progress", "completed"),
        (False, False, "Awaiting Oregon Kumquat", "x", "awaiting"),
    ],
)
def test_column_for_card_matrix(in_archived, has_return, log_status, effective, expected):
    assert (
        column_for_card(
            effective=effective,
            in_archived=in_archived,
            log_status=log_status,
            has_return=has_return,
        )
        == expected
    )


def test_effective_status_return_overrides():
    assert (
        effective_status("In Progress", "In Progress", True)
        == "Completed (RETURN present)"
    )


def test_normalize_status_token_parenthetical():
    assert normalize_status_token("Completed (foo)") == normalize_status_token("Completed")


def test_extract_ball_holder_prefers_excerpt():
    text = (FIXTURES / "kanban_status_snippet.md").read_text(encoding="utf-8")
    assert extract_ball_holder(text) == "Washington has the ball."


def test_collect_board_mini(kanban_mini_tree):
    root, mp = kanban_mini_tree
    model = collect_board(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        completed_limit=5,
        include_presence=True,
    )
    assert model["meta"]["ball_holder"] == "Washington has the ball."
    assert model["counts"]["awaiting"] == 1
    assert model["counts"]["in_progress"] >= 1
    assert model["counts"]["completed_total"] >= 1
    assert any("verifier_smoke_dummy_row" in w for w in model["warnings"])
    assert any("stale" in w for w in model["warnings"])
    assert model["coordination"]["open_items_top3"] is not None
    archived_ids = [c["id"] for c in model["columns"]["archived"]]
    assert "20260101-Archived-Only" in archived_ids


def test_completed_limit_truncation(kanban_mini_tree):
    root, mp = kanban_mini_tree
    model = collect_board(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        completed_limit=1,
        include_presence=False,
    )
    assert model["counts"]["completed_shown"] == 1
    assert model["truncation"]["completed_omitted"] >= 0


def test_kanban_json_schema_keys(kanban_mini_tree):
    root, mp = kanban_mini_tree
    model = collect_board(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        include_presence=False,
    )
    parsed = json.loads(render_json(model))
    assert set(parsed.keys()) == JSON_KEYS
    assert parsed["schema_version"] == 1


def test_render_md_sections(kanban_mini_tree):
    root, mp = kanban_mini_tree
    model = collect_board(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        include_presence=False,
    )
    md = render_md(model)
    for needle in (
        "# Symbiosis Handoff Kanban",
        "## Top Priorities",
        "## Board",
        "### Awaiting",
        "## Warnings",
    ):
        assert needle in md


def test_render_board_ascii(kanban_mini_tree):
    root, mp = kanban_mini_tree
    model = collect_board(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        include_presence=False,
    )
    board = render_board(model)
    assert "AWAITING" in board
    assert "20260602-Awaiting-Row" in board


def test_paths_handoffs_archived(kanban_mini_tree):
    root, _ = kanban_mini_tree
    assert handoffs_dir(root).name == "handoffs"
    assert archived_dir(root).name == "archived"


def test_readme_log_status_mismatch_emitted(kanban_mini_tree):
    root, mp = kanban_mini_tree
    model = collect_board(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        include_presence=False,
    )
    completed_cards = model["columns"]["completed"]
    row = next(c for c in completed_cards if c["id"] == "20260603-Test-Row")
    assert "readme_log_status_mismatch" in row["warnings"]
    assert any("readme_log_status_mismatch:20260603-Test-Row" in w for w in model["warnings"])


def test_handoff_log_drift_merged_into_warnings(kanban_mini_tree):
    root, mp = kanban_mini_tree
    shutil = __import__("shutil")
    handoffs = root / "cross-device" / "handoffs"
    shutil.copy(
        FIXTURES / "sync_handoff_log_drift.md",
        handoffs / "HANDOFF_LOG.md",
    )
    model = collect_board(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        include_presence=False,
    )
    assert any("HANDOFF_LOG header drift" in w for w in model["warnings"])


def test_build_kanban_warnings_stale_brother():
    presence = {"brother": {"age_seconds": 5000}, "warnings": []}
    w = build_kanban_warnings(presence=presence, cards=[], log_header_drift=False)
    assert any("stale" in x for x in w)


def test_2099_row_without_folder(kanban_mini_tree):
    root, mp = kanban_mini_tree
    model = collect_board(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        include_presence=False,
    )
    smoke = next(
        c
        for c in model["columns"]["in_progress"]
        if c["id"].startswith("2099")
    )
    assert smoke["folder_exists"] is False
    assert "missing_folder" in smoke["warnings"]
    assert any("verifier_smoke_dummy_row" in w for w in model["warnings"])


def test_short_description_readme_fallback(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "README.md").write_text(
        "# Title From Readme\n\n**Status:** In Progress\n",
        encoding="utf-8",
    )
    assert _readme_short_description(pkg / "README.md") == "Title From Readme"


def test_sort_archived_column_log_derived_before_synthetic():
    cards = [
        {"id": "syn", "_sort_key": "20260102", "_synthetic_archived": True},
        {"id": "log", "_sort_key": "20260102", "_synthetic_archived": False},
    ]
    out = _sort_archived_column(cards)
    assert [c["id"] for c in out] == ["log", "syn"]


def test_cli_invalid_device(repo_root):
    r = subprocess.run(
        [sys.executable, str(SHIM), "--device", "Mars"],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
        env={**__import__("os").environ, "SYMBIOSIS_REPO_ROOT": str(repo_root)},
    )
    assert r.returncode == 1
    assert "Washington Linux" in r.stderr


def test_cli_invalid_repo_root(tmp_path):
    bad = tmp_path / "not-a-repo"
    bad.mkdir()
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "--device",
            "Washington Linux",
            "--repo-root",
            str(bad),
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 2
    assert "HANDOFF_FORMAT" in r.stderr


def test_cli_completed_limit_bounds(repo_root):
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "--device",
            "Washington Linux",
            "--completed-limit",
            "51",
            "--no-presence",
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
        env={**__import__("os").environ, "SYMBIOSIS_REPO_ROOT": str(repo_root)},
    )
    assert r.returncode == 1


def test_cli_board_format(kanban_mini_tree):
    root, mp = kanban_mini_tree
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "--device",
            "Washington Linux",
            "--format",
            "board",
            "--no-presence",
        ],
        capture_output=True,
        text=True,
        env={
            **__import__("os").environ,
            "SYMBIOSIS_REPO_ROOT": str(root),
            "SYMBIOSIS_MEMPALACE_ROOT": str(mp),
        },
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 0, r.stderr
    assert "--- AWAITING" in r.stdout
    assert "20260602-Awaiting-Row" in r.stdout


def test_cli_json_format(kanban_mini_tree):
    root, mp = kanban_mini_tree
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "--device",
            "Washington Linux",
            "--format",
            "json",
            "--no-presence",
        ],
        capture_output=True,
        text=True,
        env={
            **__import__("os").environ,
            "SYMBIOSIS_REPO_ROOT": str(root),
            "SYMBIOSIS_MEMPALACE_ROOT": str(mp),
        },
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert JSON_KEYS.issubset(set(data.keys()))


def test_no_shell_true_in_kanban_sources():
    for py in KANBAN_PKG.rglob("*.py"):
        text = py.read_text(encoding="utf-8")
        assert "shell=True" not in text, f"shell=True found in {py}"


def test_sync_report_still_imports_parse_handoff_rows():
    from sync_report import collectors as sr

    assert callable(sr.parse_handoff_rows)


# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 6239aa70 batch3) -->