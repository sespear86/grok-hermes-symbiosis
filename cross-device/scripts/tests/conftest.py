"""pytest fixtures for handoff_scaffold and symbiosis-kanban."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def kanban_mini_tree(tmp_path):
    """Mini repo tree for kanban golden + collector tests (AUTON 6239aa70)."""
    root = tmp_path / "repo"
    handoffs = root / "cross-device" / "handoffs"
    coord = root / "cross-device" / "coordination"
    handoffs.mkdir(parents=True)
    coord.mkdir(parents=True)
    src = REPO_ROOT / "cross-device" / "handoffs"
    shutil.copy(src / "HANDOFF_FORMAT.md", handoffs / "HANDOFF_FORMAT.md")
    shutil.copy(FIXTURES / "kanban_handoff_log.md", handoffs / "HANDOFF_LOG.md")
    shutil.copy(FIXTURES / "sync_open_items_snippet.md", coord / "OPEN_ITEMS.md")
    shutil.copy(FIXTURES / "kanban_status_snippet.md", coord / "status.md")

    completed = handoffs / "20260603-Test-Row"
    completed.mkdir()
    (completed / "README.md").write_text(
        "**Status:** In Progress\n\nDone work.\n",
        encoding="utf-8",
    )
    (completed / "RETURN.md").write_text("# RETURN\n", encoding="utf-8")

    awaiting = handoffs / "20260602-Awaiting-Row"
    awaiting.mkdir()
    (awaiting / "README.md").write_text(
        "**Status:** Awaiting Oregon Kumquat\n",
        encoding="utf-8",
    )

    arch = handoffs / "archived" / "20260101-Archived-Only"
    arch.mkdir(parents=True)
    (arch / "README.md").write_text("**Status:** Archived\n", encoding="utf-8")

    mp = tmp_path / "mempalace" / "symbiosis" / "device-presence"
    mp.mkdir(parents=True)
    (mp / "washington.md").write_text(
        "**Last Heartbeat:** 2026-06-04T12:00:00+00:00\n**Current Mode:** **Paired**\n",
        encoding="utf-8",
    )
    (mp / "oregon.md").write_text(
        "**Last Heartbeat:** 2020-01-01T00:00:00+00:00\n",
        encoding="utf-8",
    )
    return root, tmp_path / "mempalace"


@pytest.fixture
def repo_root(tmp_path):
    """Minimal repo tree with FORMAT + LOG copied from real repo."""
    root = tmp_path / "repo"
    handoffs = root / "cross-device" / "handoffs"
    handoffs.mkdir(parents=True)
    src_handoffs = REPO_ROOT / "cross-device" / "handoffs"
    shutil.copy(src_handoffs / "HANDOFF_FORMAT.md", handoffs / "HANDOFF_FORMAT.md")
    shutil.copy(src_handoffs / "HANDOFF_LOG.md", handoffs / "HANDOFF_LOG.md")
    return root


@pytest.fixture
def projects_mini_tree(tmp_path, kanban_mini_tree):
    """Projects root + mini symbiosis repo for joint_projects list tests."""
    root, _mp = kanban_mini_tree
    projects_root = tmp_path / "projects"
    projects_root.mkdir()
    alpha = projects_root / "Alpha-App"
    alpha.mkdir()
    (alpha / "README.md").write_text("# Alpha\n", encoding="utf-8")
    (alpha / ".stignore").write_text(".git/\n", encoding="utf-8")
    beta = projects_root / "Beta-Only-Readme"
    beta.mkdir()
    (beta / "README.md").write_text("# Beta\n", encoding="utf-8")
    (projects_root / ".hidden").mkdir()
    (projects_root / "notes.txt").write_text("skip\n", encoding="utf-8")
    return root, projects_root


# <!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 61cdeb81 PR1) -->