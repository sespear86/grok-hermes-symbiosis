"""symbiosis-memory-sync CLI (AUTON 7eb7d1b7).

push, pull, status, bundle per DESIGN.

Example:
  python -m memory_sync.cli bundle --agent grok --device "Washington Linux" --dry-run
  ./symbiosis-memory-sync push --agent grok --device "Washington Linux"
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

# Local imports (when run as module or after pythonpath)
try:
    from . import paths, bundle as bundle_mod
    from .collectors import grok_session, hermes_memory, coordination
    from . import palace_io, render  # optional others in full impl
except Exception:
    # Fallback when executed directly
    sys.path.insert(0, str(Path(__file__).parent))
    import paths  # type: ignore
    import bundle as bundle_mod  # type: ignore
    from collectors import grok_session, hermes_memory, coordination  # type: ignore
    try:
        import palace_io, render  # type: ignore
    except Exception:
        palace_io = render = None  # type: ignore

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="symbiosis-memory-sync")
    ap.add_argument("cmd", choices=["push", "pull", "status", "bundle"])
    ap.add_argument("--agent", choices=["grok", "hermes"], required=True)
    ap.add_argument("--device", required=True)
    ap.add_argument("--project", default=paths.DEFAULT_PROJECT_SLUG)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)

    repo = paths.default_repo_root()
    palace = paths.default_mempalace_root()

    if args.cmd == "bundle":
        # minimal dry-run bundle
        if args.agent == "grok":
            sess = grok_session.find_latest_session(Path.cwd())
            todos, warns = grok_session.collect_todos(sess) if sess else ([], ["no session"])
        else:
            todos, warns = [], []
        b = {
            "bundle_id": bundle_mod.make_bundle_id(args.project, datetime.now(timezone.utc).isoformat(), args.agent, "deadbeef"),
            "version": bundle_mod.BUNDLE_VERSION,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "agent": args.agent,
            "device": args.device,
            "project_slug": args.project,
            "todos": todos,
            "decisions": [],
            "open_items_excerpt": coordination.extract_open_items_top3(repo) if hasattr(coordination, "extract_open_items_top3") else None,
            "native_memory_excerpt": None,
            "mempalace_refs": [f"projects/{args.project}-snapshots"],
            "warnings": warns,
        }
        print(json.dumps(b, indent=2))
        return 0

    if args.cmd == "push":
        # stub: build + push (real in full B3)
        print(f"push {args.agent} {args.device} to {palace} (stub; see DESIGN B3 + palace_io)")
        return 0

    if args.cmd == "pull":
        print(f"pull {args.agent} {args.device} (stub inject to stdout)")
        return 0

    if args.cmd == "status":
        print(json.dumps({"last": None, "device": args.device, "project": args.project, "note": "stub per B3"}, indent=2))
        return 0

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
