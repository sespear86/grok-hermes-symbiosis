"""Palace I/O for memory bundles (Mempalace canonical).

Uses venv python + direct mempalace.mcp_server tool calls for add/list (MCP-only in 3.3.5);
falls back to `mempalace --palace ... mine` / search for CLI paths.

See DESIGN round 2/3 fixes + mempalace_symbiosis_bundle_io.py helper.
"""

from __future__ import annotations
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

VENV_PY = os.environ.get(
    "SYMBIOSIS_MEMPALACE_VENV_PYTHON",
    str(Path.home() / "grokforge-palaces" / "mempalace-venv" / "bin" / "python")
)
HELPER = Path(__file__).parent.parent / "Mempalace" / "scripts" / "mempalace_symbiosis_bundle_io.py"  # will be created in B2b or here

# Fallback to inline if helper missing (for bootstrap)
def _call_tool_add_drawer(palace: str, wing: str, room: str, content: str) -> bool:
    code = f"""
import sys
sys.path.insert(0, "{os.path.dirname(VENV_PY)}/lib/python*/site-packages")
from mempalace.mcp_server import tool_add_drawer
print(tool_add_drawer(palace_path="{palace}", wing="{wing}", room="{room}", content={json.dumps(content)}))
"""
    try:
        r = subprocess.run([VENV_PY, "-c", code], capture_output=True, text=True, timeout=60)
        return r.returncode == 0 and "ok" in r.stdout.lower()
    except Exception:
        return False

def push_bundle(palace_root: Path, bundle: Dict[str, Any], project_slug: str) -> str:
    """File bundle as drawer. Returns drawer-ish id or path."""
    room = f"{project_slug}-snapshots"
    content = f"# Symbiosis Memory Bundle {bundle.get('bundle_id')}\n\n```json\n{json.dumps(bundle, indent=2)}\n```\n"
    wing = "projects"
    palace = str(palace_root)
    # Prefer the venv helper (runs under correct python + mempalace env)
    helper = str(Path(__file__).parent.parent / "Mempalace" / "scripts" / "mempalace_symbiosis_bundle_io.py")
    if Path(helper).exists() and Path(VENV_PY).exists():
        try:
            r = subprocess.run([VENV_PY, helper, "add", "--palace", palace, "--wing", wing, "--room", room, "--content", content], capture_output=True, text=True, timeout=60)
            if r.returncode == 0:
                return f"projects/{room}/{bundle.get('bundle_id')}"
        except Exception:
            pass
    if _call_tool_add_drawer(palace, wing, room, content):
        return f"projects/{room}/{bundle.get('bundle_id')}"
    # Fallback mine
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "bundle.md"
        p.write_text(content)
        cmd = ["mempalace", "--palace", palace, "mine", str(p), "--wing", wing]
        subprocess.run(cmd, check=False, timeout=60)
    return f"projects/{room} (mine fallback)"

def list_latest_bundles(palace_root: Path, project_slug: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Return list of parsed bundle dicts (latest first) by calling the venv helper for full docs."""
    import re
    room = f"{project_slug}-snapshots"
    venv_py = VENV_PY
    helper = str(Path(__file__).parent.parent / "Mempalace" / "scripts" / "mempalace_symbiosis_bundle_io.py")
    if not Path(helper).exists():
        return []
    cmd = [venv_py, helper, "list", "--palace", str(palace_root), "--wing", "projects", "--room", room]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            return []
        data = json.loads(r.stdout or "{}")
        drawers = data.get("drawers", []) or []
        bundles = []
        for d in drawers:
            doc = d.get("document", "") or ""
            # Extract the first fenced json block
            m = re.search(r"```json\s*(.*?)\s*```", doc, re.DOTALL | re.IGNORECASE)
            if m:
                try:
                    b = json.loads(m.group(1))
                    bundles.append(b)
                except Exception:
                    pass
        # Sort newest first by exported_at if present
        bundles.sort(key=lambda x: x.get("exported_at", ""), reverse=True)
        return bundles[:limit]
    except Exception:
        return []

def pull_bundles(palace_root: Path, project_slug: str, agent: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
    """Pull latest bundles (optionally filtered by agent)."""
    all_b = list_latest_bundles(palace_root, project_slug, limit=limit*2)
    if agent:
        all_b = [b for b in all_b if b.get("agent") == agent]
    return all_b[:limit]

def render_inject(bundles: List[Dict[str, Any]]) -> str:
    """Simple inject renderer for pull --format markdown."""
    if not bundles:
        return "# No memory bundles found\n"
    parts = ["# Symbiosis Memory Pull (latest bundles)\n"]
    for b in bundles:
        parts.append(f"\n## Bundle {b.get('bundle_id')} from {b.get('agent')}@{b.get('device')} at {b.get('exported_at')}\n")
        if b.get("todos"):
            parts.append("**Todos:**\n")
            for t in b["todos"]:
                parts.append(f"- [{t.get('status','?')}] {t.get('content','')}\n")
        if b.get("decisions"):
            parts.append("**Decisions:**\n" + "\n".join(f"- {d}" for d in b["decisions"][:5]) + "\n")
        if b.get("open_items_excerpt"):
            parts.append("**Open Items (top):** " + str(b["open_items_excerpt"])[:300] + "\n")
        if b.get("warnings"):
            parts.append("**Warnings:** " + "; ".join(b["warnings"]) + "\n")
    return "\n".join(parts)

# Simple in-memory last-push tracking for status (real impl would use sidecar or palace query)
_LAST_PUSH = {}

def record_push(project: str, agent: str, device: str, bundle_id: str):
    _LAST_PUSH[(project, agent, device)] = {"bundle_id": bundle_id, "ts": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()}

def get_last_push(project: str, device: str) -> Dict[str, Any]:
    # Return info for both agents if present
    res = {}
    for ag in ("grok", "hermes"):
        key = (project, ag, device)
        if key in _LAST_PUSH:
            res[ag] = _LAST_PUSH[key]
    return res

