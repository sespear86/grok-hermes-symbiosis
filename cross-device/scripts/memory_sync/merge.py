"""Bundle merge rules (per-agent latest + field union). Stub for bootstrap."""
from __future__ import annotations
from typing import Any, Dict, List

def merge_bundles(bundles: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not bundles:
        return {}
    # Newer first simplistic
    bundles = sorted(bundles, key=lambda b: b.get("exported_at", ""), reverse=True)
    return bundles[0]  # full in B3
