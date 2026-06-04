"""pytest fixtures for handoff_scaffold."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]


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