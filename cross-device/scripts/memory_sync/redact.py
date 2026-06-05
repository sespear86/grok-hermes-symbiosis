"""Redact secrets from bundles (align threat_patterns strict if present)."""
from __future__ import annotations
import json
import re
from typing import Any, Dict

SECRET_KEYS = {"api_key", "token", "secret", "password", "auth", "bearer"}

def _redact_value(v: Any) -> Any:
    if isinstance(v, str):
        if any(k in v.lower() for k in SECRET_KEYS):
            return "***REDACTED***"
    return v

def redact_bundle(b: Dict[str, Any]) -> Dict[str, Any]:
    def walk(x: Any) -> Any:
        if isinstance(x, dict):
            return {k: ( "***REDACTED***" if any(sk in k.lower() for sk in SECRET_KEYS) else walk(v) ) for k, v in x.items()}
        if isinstance(x, list):
            return [walk(i) for i in x]
        return _redact_value(x)
    return walk(b)
