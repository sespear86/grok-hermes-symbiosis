"""Basic tests for task_schema (PR4 start, AUTON 19557e65)."""
import json
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import task_schema


def test_validate_good():
    t = {"type": "grok_build_task", "correlation_id": "slack-123", "original_message": "do it"}
    assert task_schema.validate_task(t) == t


def test_validate_missing():
    with pytest.raises(task_schema.TaskValidationError):
        task_schema.validate_task({"type": "x", "correlation_id": "ok"})


def test_validate_bad_corr():
    with pytest.raises(task_schema.TaskValidationError):
        task_schema.validate_task({"type": "x", "correlation_id": "!!", "original_message": "y"})


def test_validate_from_json_text():
    txt = json.dumps({"type": "t", "correlation_id": "c-1", "original_message": "msg"})
    t = task_schema.validate_task_from_json_text(txt)
    assert t["correlation_id"] == "c-1"
