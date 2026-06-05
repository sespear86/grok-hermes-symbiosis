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
        # Build bundle (dry-run friendly)
        if args.agent == "grok":
            sess = grok_session.find_latest_session(Path.cwd())
            todos, warns = grok_session.collect_todos(sess) if sess else ([], ["no session dir or no todo_write events"])
        else:
            todos, warns = [], []
        try:
            open_items = coordination.extract_open_items_top3(repo) if hasattr(coordination, "extract_open_items_top3") else None
        except Exception:
            open_items = None
        b = {
            "bundle_id": bundle_mod.make_bundle_id(args.project, datetime.now(timezone.utc).isoformat(), args.agent, "cafebabe"),
            "version": bundle_mod.BUNDLE_VERSION,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "agent": args.agent,
            "device": args.device,
            "project_slug": args.project,
            "todos": todos,
            "decisions": [],
            "open_items_excerpt": open_items,
            "native_memory_excerpt": None,
            "mempalace_refs": [f"projects/{args.project}-snapshots"],
            "warnings": warns,
        }
        try:
            from . import redact
            b = redact.redact_bundle(b)
        except Exception:
            pass
        print(json.dumps(b, indent=2))
        return 0

    if args.cmd == "push":
        # Real push: build bundle then file via palace_io
        if args.agent == "grok":
            sess = grok_session.find_latest_session(Path.cwd())
            todos, warns = grok_session.collect_todos(sess) if sess else ([], ["no session"])
        else:
            todos, warns = [], []
        try:
            open_items = coordination.extract_open_items_top3(repo) if hasattr(coordination, "extract_open_items_top3") else None
        except Exception:
            open_items = None
        b = {
            "bundle_id": bundle_mod.make_bundle_id(args.project, datetime.now(timezone.utc).isoformat(), args.agent, "feedface"),
            "version": bundle_mod.BUNDLE_VERSION,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "agent": args.agent,
            "device": args.device,
            "project_slug": args.project,
            "todos": todos,
            "decisions": [],
            "open_items_excerpt": open_items,
            "native_memory_excerpt": None,
            "mempalace_refs": [f"projects/{args.project}-snapshots"],
            "warnings": warns,
        }
        try:
            from . import redact
            b = redact.redact_bundle(b)
        except Exception:
            pass
        if args.dry_run:
            print(json.dumps({"dry_run": True, "would_push": b}, indent=2))
            return 0
        try:
            from . import palace_io as pio
            drawer_ref = pio.push_bundle(palace, b, args.project)
            try:
                from . import palace_io as _pio
                _pio.record_push(args.project, args.agent, args.device, b["bundle_id"])
            except Exception:
                pass
            print(json.dumps({"pushed": True, "bundle_id": b["bundle_id"], "drawer": drawer_ref}, indent=2))
            return 0
        except Exception as e:
            print(json.dumps({"pushed": False, "error": str(e)}, indent=2))
            return 2

    if args.cmd == "pull":
        try:
            from . import palace_io as pio
            bundles = pio.pull_bundles(palace, args.project, agent=args.agent, limit=3)
            if args.dry_run:
                print(json.dumps({"dry_run": True, "would_pull": [bb.get("bundle_id") for bb in bundles]}, indent=2))
                return 0
            text = pio.render_inject(bundles)
            print(text)
            return 0
        except Exception as e:
            print(f"pull failed: {e}")
            return 2

    if args.cmd == "status":
        try:
            from . import palace_io as pio
            last = pio.get_last_push(args.project, args.device)
            print(json.dumps({"project": args.project, "device": args.device, "last_push": last or "none recorded in this process", "note": "use push to record; palace query for cross-process"}, indent=2))
            return 0
        except Exception as e:
            print(json.dumps({"error": str(e)}, indent=2))
            return 2

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
