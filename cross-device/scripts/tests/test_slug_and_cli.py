"""Slug parsing and CLI safety."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
SHIM = SCRIPTS / "symbiosis-new-handoff"

SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{2,80}$")


@pytest.mark.parametrize(
    "slug,ok",
    [
        ("Symbiosis-Handoff-Scaffold-Ship", True),
        ("Test-Handoff", True),
        ("ab", False),
        ("-bad", False),
        ("has space", False),
    ],
)
def test_slug_regex(slug, ok):
    assert bool(SLUG_RE.match(slug)) is ok


def test_cli_rejects_unsafe_context(repo_root, monkeypatch):
    monkeypatch.chdir(SCRIPTS)
    env = {"SYMBIOSIS_REPO_ROOT": str(repo_root)}
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "--from",
            "Washington Linux",
            "--to",
            "Oregon Windows",
            "--slug",
            "Safe-Slug",
            "--context",
            "bad $var",
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        env={**__import__("os").environ, **env},
    )
    assert r.returncode != 0
    assert "$" in r.stderr or "template safety" in r.stderr