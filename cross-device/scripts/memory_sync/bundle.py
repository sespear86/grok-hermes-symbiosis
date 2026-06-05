"""SYMBIOSIS_MEMORY_BUNDLE v1 and helpers (per DESIGN.md AUTON 7eb7d1b7).

Lightweight, redacted, provenance-carrying interchange for cross-agent
(Grok/Hermes) + Mempalace shared symbiosis memory.

Mempalace is canonical shared truth; native stores remain locally authoritative.
"""

from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

BUNDLE_VERSION = "1.0"
MAX_BUNDLE_BYTES = 32 * 1024  # 32KB cap

@dataclass
class TodoItem:
    id: str
    content: str
    status: str  # pending | in_progress | completed | cancelled

@dataclass
class Decision:
    text: str
    source: str  # e.g. "grok-updates", "hermes-MEMORY.md:12"
    ts: Optional[str] = None

@dataclass
class SymbiosisMemoryBundle:
    bundle_id: str
    version: str
    exported_at: str  # ISO
    agent: str  # "grok" | "hermes"
    device: str  # "Washington Linux" | "Oregon Windows"
    project_slug: str
    todos: List[Dict[str, Any]]
    decisions: List[Dict[str, Any]]
    open_items_excerpt: Optional[str]
    native_memory_excerpt: Optional[str]
    mempalace_refs: List[str]
    warnings: List[str]
    kanban_excerpt: Optional[str] = None
    content_hash: Optional[str] = None

    def to_json(self, include_hash: bool = True) -> str:
        d = asdict(self)
        if not include_hash:
            d.pop("content_hash", None)
        return json.dumps(d, sort_keys=True, indent=2)

    @classmethod
    def compute_hash(cls, data: Dict[str, Any]) -> str:
        # Exclude hash and warnings for stable hash
        payload = {k: v for k, v in data.items() if k not in ("content_hash", "warnings")}
        s = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def make_bundle_id(project: str, exported_at: str, agent: str, h8: str) -> str:
    return f"{project}-{exported_at.replace(':', '').replace('-', '')[:13]}-{agent}-{h8}"

# ... (full redact, from_dict, validate in B1/B2 per DESIGN)
