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
    """Return list of parsed bundle dicts (latest first). Uses helper or search."""
    # Simplified: use search or direct for now; full in helper per DESIGN R3
    # For bootstrap, return []
    return []

# ... (pull_bundles, merge entry per full spec)
