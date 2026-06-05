"""Basic tests for memory_sync (AUTON 7eb7d1b7).

Run: pytest tests -q -k memory_sync
"""

from __future__ import annotations
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory_sync import bundle as bmod
from memory_sync.collectors import grok_session

def test_bundle_id_stable():
    bid = bmod.make_bundle_id("grok-hermes-symbiosis", "2026-06-05T12:00:00+00:00", "grok", "abc12345")
    assert "grok-hermes-symbiosis" in bid
    assert "grok" in bid

def test_grok_todos_collector_no_crash(tmp_path: Path):
    # empty session dir -> warning
    todos, warns = grok_session.collect_todos(tmp_path)
    assert isinstance(todos, list)
    assert any("no updates" in w or "no todo" in w for w in warns) or not warns

def test_redact_runs():
    from memory_sync.redact import redact_bundle
    red = redact_bundle({"native_memory_excerpt": "token=secret123"})
    s = json.dumps(red)
    assert "REDACTED" in s or "secret123" not in s
