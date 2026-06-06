"""Tests for symbiosis-mirror-audit (sym-build-04 starter)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from mirror_audit.checklist import CHECKLIST
from mirror_audit.collectors import collect_audit, parse_mirror_sections
from mirror_audit.render import render_json, render_markdown

SCRIPTS = Path(__file__).resolve().parents[1]
SHIM = SCRIPTS / "symbiosis-mirror-audit"
REPO_ROOT = Path(__file__).resolve().parents[3]


def test_checklist_non_empty():
    assert len(CHECKLIST) >= 5
    assert any(c.component_id == "symbiosis-mirror-audit" for c in CHECKLIST)


def test_parse_mirror_sections():
    mk = REPO_ROOT / "cross-device" / "MIRROR_KITS_AND_INFRASTRUCTURE.md"
    if not mk.is_file():
        pytest.skip("MIRROR_KITS not in tree")
    sections = parse_mirror_sections(mk)
    assert any("§11" in s or s.startswith("§11 ") for s in sections)


def test_collect_audit_on_repo():
    model = collect_audit(
        device="Washington Linux",
        repo_root=REPO_ROOT,
        rich_root=REPO_ROOT / "cross-device",
        grok_root=Path.home() / ".grok",
        bin_dir=Path.home() / "bin",
    )
    assert model.mirror_kits_present
    assert model.gap_count >= 0
    md = render_markdown(model)
    assert "Symbiosis mirror audit" in md
    payload = json.loads(render_json(model))
    assert "components" in payload


def test_cli_device_validation():
    proc = subprocess.run(
        [sys.executable, str(SHIM), "--device", "Bad Device"],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
        check=False,
    )
    assert proc.returncode == 1