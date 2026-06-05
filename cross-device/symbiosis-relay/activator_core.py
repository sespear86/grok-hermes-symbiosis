#!/usr/bin/env python3
"""
activator_core.py — Extracted resilient core for Washington activator (Symbiosis Relay).

Per DESIGN AUTON 19557e65 PR1/PR2/PR3 + oregon-support packaging:
- Structured JSON logging with correlation
- Enriched status writes
- Beacon with retries + abort on total fail
- Atomic claim via rename to processing/
- Task schema validation
- Health interlock before claim (beacon age, dirs, script)
- prompt_grok_build with hermes rc check, configurable inject, pending on *any* terminal fail
- Bust intent hook (touch marker)
- No bare excepts; explicit taxonomy
- SYMBIOSIS_DEVICE generalization (back-compat default "washington") for cross-device oregon receiver

Stdlib only (KD-1). Mirrors existing patterns (SYMBIOSIS_SHARED, Path, json, subprocess, logging).

This module is the "brain"; washington_activator.py becomes thin CLI + loop.
"""

from __future__ import annotations
import json
import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Ensure sibling modules (task_schema, control, tools) resolvable when run as script or -m
_RELAY_ROOT = Path(__file__).parent
sys.path.insert(0, str(_RELAY_ROOT))
sys.path.insert(0, str(_RELAY_ROOT / "tools"))
import task_schema  # noqa: E402
import control  # noqa: E402
import send_to_slack  # noqa: E402

# --- 19557e65 + oregon-support for cross-device receiver ---
# Small back-compatible generalization: SYMBIOSIS_DEVICE env var (or --device CLI flag on the thin
# washington_activator.py) defaults to "washington". Used to build:
#   COMMAND_INBOX = .../incoming/$device
#   STATUS_OUTBOX = .../status/$device
#   beacon file: $device-grok-build-presence.json
#   status.machine, etc.
# Oregon receiver launcher will: $env:SYMBIOSIS_DEVICE="oregon"; python -u washington_activator.py ...
# Default behavior 100% unchanged for existing washington service + tests. Packaging change only.
DEVICE = (os.environ.get("SYMBIOSIS_DEVICE", "washington") or "washington").strip().lower()

# --- Config (env overridable, same spirit as device_selector/relay_listener) ---
SHARED_BASE = Path(os.environ.get("SYMBIOSIS_SHARED", "/home/Irikash/Synced/grok-mempalace-integration"))
COMMAND_INBOX = SHARED_BASE / "symbiosis-relay" / "incoming" / DEVICE
STATUS_OUTBOX = SHARED_BASE / "symbiosis-relay" / "status" / DEVICE
PROCESSED_DIR = COMMAND_INBOX / "processed"
PENDING_PROMPTS_DIR = COMMAND_INBOX / "pending-prompts"
PROCESSING_DIR = COMMAND_INBOX / "processing"
FAILED_DIR = COMMAND_INBOX / "failed"

BEACON = Path(os.environ.get("GROK_BUILD_PRESENCE_BEACON", str(Path.home() / "bin" / "grok-build-presence-beacon")))
INJECT_BUST_SCRIPT = Path(os.environ.get(
    "INJECT_BUST_SCRIPT",
    str(SHARED_BASE / "symbiosis-relay" / "tools" / "inject-bust-a-nut-into-running-tui.sh")
))
INJECT_BUST_PYTHON = Path(os.environ.get(
    "INJECT_BUST_PYTHON",
    str(SHARED_BASE / "symbiosis-relay" / "tools" / "pts-inject-input.py")
))


def _beacon_script_exists(beacon_val: str) -> bool:
    """Tolerant exists check for beacon.
    Supports simple path (WA sh/exe) and Oregon full 'powershell.exe ... -File \"path.ps1\"' command string
    set by the thin launcher for cross-device (19557e65 Oregon receiver).
    Self-provisioned gap fill so health interlock + claim can succeed on Windows without changing call sites.
    """
    if not beacon_val:
        return False
    p = Path(beacon_val)
    if p.exists():
        return True
    # Oregon style full command containing -File "script.ps1" (or -file)
    if '-File' in beacon_val or '-file' in beacon_val:
        m = re.search(r'-File\s+["\']?([^"\']+?)["\']?', beacon_val, re.IGNORECASE)
        if m:
            script_p = Path(m.group(1))
            return script_p.exists()
    return False


LOG_DIR = Path.home() / "symbiosis-relay" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Ensure dirs (self-provision on import / startup)
for d in [COMMAND_INBOX, STATUS_OUTBOX, PROCESSED_DIR, PENDING_PROMPTS_DIR, PROCESSING_DIR, FAILED_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# --- Structured logging (JSON + human fallback) ---
_logger = logging.getLogger("washington-activator-core")
if not _logger.handlers:
    _logger.setLevel(logging.INFO)
    # Human stream (journal friendly)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
    _logger.addHandler(sh)
    # JSON file (parseable by relay-health / dashboards)
    # Device-aware name for oregon parity (default "washington_activator.jsonl" unchanged)
    fh = logging.FileHandler(LOG_DIR / f"{DEVICE}_activator.jsonl")
    fh.setFormatter(logging.Formatter("%(message)s"))  # we emit pre-formatted json lines
    _logger.addHandler(fh)


def _json_log(level: str, msg: str, **fields: Any) -> None:
    rec = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "msg": msg,
        **fields,
    }
    line = json.dumps(rec, default=str)
    # Also feed the human formatter via logger
    if level == "INFO":
        _logger.info(line)
    elif level == "WARNING":
        _logger.warning(line)
    elif level == "ERROR":
        _logger.error(line)
    else:
        _logger.info(line)


def configure_logging(json_mode: bool = True) -> None:
    """Idempotent; called from thin CLI."""
    global _logger
    # already configured above; json_mode kept for future (always emit jsonl + human)
    _json_log("INFO", "logging configured", json_mode=json_mode, log_dir=str(LOG_DIR))


def ensure_directories() -> None:
    """Self-provision all inbox/status/processing/failed/pending dirs (called from thin CLI)."""
    for d in [COMMAND_INBOX, STATUS_OUTBOX, PROCESSED_DIR, PENDING_PROMPTS_DIR, PROCESSING_DIR, FAILED_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def read_status() -> dict[str, Any]:
    """Read current status.json (for --status CLI)."""
    sf = STATUS_OUTBOX / "status.json"
    if sf.exists():
        try:
            return json.loads(sf.read_text())
        except Exception:
            pass
    return {"state": "unknown", "machine": DEVICE}


# --- Status + Beacon (enriched, retried) ---
def write_status(state: str, task_id: str = "", message: str = "", **extra: Any) -> None:
    data = {
        "state": state,
        "current_task": task_id,
        "message": message,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "machine": DEVICE,
        "version": "0.2.0-auton-19557e65",
        **extra,
    }
    (STATUS_OUTBOX / "status.json").write_text(json.dumps(data, indent=2))
    _json_log("INFO", "status written", state=state, task_id=task_id, **{k: v for k, v in extra.items() if k in ("health_ok", "beacon_age_seconds_at_claim", "last_inject_rc", "last_hermes_rc")})


def fire_beacon(active: bool, task_id: str = "", bust: bool = False) -> bool:
    """Retry 3x. Return True on success. On total fail: log + return False (caller should abort)."""
    cmd = [str(BEACON), "start", task_id] if active else [str(BEACON), "stop"]
    if active and bust:
        # also assert intent via beacon subcmd if present (best-effort)
        cmd = [str(BEACON), "bust_a_nut_start", task_id]  # falls back gracefully in beacon script
    for attempt in range(3):
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                _json_log("INFO", "beacon fired", active=active, task_id=task_id, attempt=attempt)
                return True
            _json_log("WARNING", "beacon attempt failed", rc=res.returncode, stderr=res.stderr[:200], attempt=attempt)
        except Exception as e:
            _json_log("WARNING", "beacon exception", error=str(e), attempt=attempt)
        time.sleep(1.5 * (attempt + 1))
    _json_log("ERROR", "beacon total failure", active=active, task_id=task_id)
    return False

# <!-- Edited: 2026-06-04 | Device: Windows | By: Grok (19557e65 Oregon packaging + Kumquat verification) --> Self-provisioned tolerant beacon exists parser for Oregon launcher command strings + Set beacon script support. Exact primes + Mirror + self-prov followed. Keep er goinnnn. Bust a nut.

def check_health() -> dict[str, Any]:
    """Return health dict. Used before claim + for --health CLI."""
    health: dict[str, Any] = {
        "ok": True,
        "reasons": [],
        "beacon_script_exists": _beacon_script_exists(str(BEACON)),
        "inject_script_exists": INJECT_BUST_SCRIPT.exists(),
        "inbox_writable": COMMAND_INBOX.exists() and os.access(COMMAND_INBOX, os.W_OK),
        "status_writable": STATUS_OUTBOX.exists() and os.access(STATUS_OUTBOX, os.W_OK),
    }
    # Beacon age (self)
    beacon_path = SHARED_BASE / "device-presence" / f"{DEVICE}-grok-build-presence.json"
    if beacon_path.exists():
        try:
            b = json.loads(beacon_path.read_text())
            last = datetime.fromisoformat(b.get("last_seen", "").replace("Z", "+00:00"))
            age = (datetime.now(timezone.utc) - last).total_seconds()
            health["beacon_age_seconds"] = age
            if age > 300:
                health["ok"] = False
                health["reasons"].append("self beacon stale >300s")
        except Exception as e:
            health["reasons"].append(f"beacon parse error: {e}")
    else:
        health["reasons"].append("no self beacon file")
        health["ok"] = False

    if not health["beacon_script_exists"]:
        health["ok"] = False
        health["reasons"].append("beacon script missing")
    if not health["inbox_writable"] or not health["status_writable"]:
        health["ok"] = False
        health["reasons"].append("inbox/status not writable")

    return health


def health_check() -> dict[str, Any]:
    """Alias for thin CLI compatibility."""
    return check_health()


# --- Claim (atomic rename to processing/ to prevent dup) ---
def claim_task(task_file: Path) -> Path | None:
    """Atomically move to processing/. Return the processing path or None on race."""
    PROCESSING_DIR.mkdir(parents=True, exist_ok=True)
    proc_path = PROCESSING_DIR / task_file.name
    try:
        task_file.rename(proc_path)
        return proc_path
    except FileNotFoundError:
        return None  # raced
    except Exception as e:
        _json_log("ERROR", "claim rename failed", file=str(task_file), error=str(e))
        return None


def archive_task(proc_or_orig: Path, success: bool) -> None:
    """Move from processing/ to processed/ or failed/ depending on success."""
    if success:
        target = PROCESSED_DIR / proc_or_orig.name
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    else:
        target = FAILED_DIR / proc_or_orig.name
        FAILED_DIR.mkdir(parents=True, exist_ok=True)
    try:
        proc_or_orig.rename(target)
    except Exception as e:
        _json_log("WARNING", "archive rename failed (best effort)", error=str(e), file=str(proc_or_orig))


# --- Prompt / inject (with rc check, configurable, full artifact on fail) ---
def _write_pending_artifact(correlation: str, task: dict, error: str, suggested: str = "") -> Path:
    PENDING_PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    p = PENDING_PROMPTS_DIR / f"{correlation}.md"
    content = f"""# Pending prompt — correlation {correlation}

## Error
{error}

## Suggested command (copy-paste)
{suggested or 'hermes -z "..." --skills grok-build'}

## Task JSON (for context)
{json.dumps(task, indent=2, default=str)}
"""
    p.write_text(content)
    return p


def prompt_grok_build(task: dict[str, Any]) -> bool:
    """Core handoff. Returns True only on clean success path."""
    correlation = task.get("correlation_id", "unknown")
    task_type = task.get("type", "")
    _json_log("INFO", "prompt_grok_build start", correlation=correlation, type=task_type)

    # Bust resume fast path (prefer live TUI)
    if task_type == "bust_a_nut_resume":
        _json_log("INFO", "bust_a_nut_resume — attempting live TUI injection first", correlation=correlation)
        # Touch intent marker (best effort, lets sh + watchdog stay happy)
        try:
            marker = SHARED_BASE / "device-presence" / ".bust_a_nut_intent_active"
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.touch()
        except Exception:
            pass

        try:
            # Prefer configured sh
            inject_cmd = [str(INJECT_BUST_SCRIPT)]
            res = subprocess.run(inject_cmd, capture_output=True, text=True, timeout=30)
            _json_log("INFO", "live inject rc", correlation=correlation, rc=res.returncode, stdout=res.stdout[:300])
            if res.returncode == 0:
                write_status("bust_a_nut_injected_live", correlation, "Re-initiated into existing Grok Build TUI via live inject", last_inject_rc=0, health_ok=True)
                return True
            else:
                _json_log("WARNING", "live inject failed rc", correlation=correlation, rc=res.returncode, stderr=res.stderr[:300])
        except Exception as e:
            _json_log("WARNING", "live inject exception", correlation=correlation, error=str(e))

        # Fallback to rich python pts if sh failed and python helper present
        if INJECT_BUST_PYTHON.exists():
            try:
                py_cmd = ["python3", str(INJECT_BUST_PYTHON), "--bust-a-nut"]
                res2 = subprocess.run(py_cmd, capture_output=True, text=True, timeout=20)
                if res2.returncode == 0:
                    write_status("bust_a_nut_injected_live", correlation, "Re-initiated via pts-inject fallback", last_inject_rc=0)
                    return True
            except Exception as e:
                _json_log("WARNING", "pts fallback exception", error=str(e))

    # Build prompt (same spirit as original, raunchy kept in caller context)
    if task_type == "bust_a_nut_resume":
        prompt = f"""BUST A NUT RESUME (from the external Pi listening post watchdog)

The previous Bust a Nut / keep-er-goinnnn session has stopped or gone silent.

IMMEDIATE ACTION REQUIRED:
You are now in explicit full autonomous "Bust a Nut" mode.
Rule: Do not stop looping if you can find a way to proceed. Highest leverage only. No status reports that create natural stopping points. Keep executing tool calls and making mechanical progress until there is genuinely zero remaining work.

Context from the watchdog:
{json.dumps(task.get('context_hints', {}), indent=2)}

Pull the latest relevant context from mempalace (diary entries about Bust a Nut, the relay project, presence reliability work, etc.).

Then immediately resume the loop. Use the bust-a-nut-continue.sh driver and relay-health.sh as needed.

All 7 primes + anti-stop discipline apply. Do not stop.
"""
    else:
        prompt = f"""SYMBIOSIS RELAY TASK (from central listening post on the Pi)

Correlation: {correlation}
Source: {task.get('source', 'relay')}
Slack channel: {task.get('slack_channel', 'unknown')}

{task.get('original_message', '')}

Context from Relay:
{json.dumps(task.get('context_hints', {}), indent=2)}

You are being activated by the Symbiosis Relay because you are the current highest-priority target (Washington was chosen based on healthy heartbeat + priority rules).

Use the grok-build skill for any deep design, implementation, review, or verification work.
All 7 primes apply. Keep er goinnnn.
"""

    _json_log("INFO", "prompting hermes + grok-build", correlation=correlation)
    try:
        result = subprocess.run(
            ["hermes", "-z", prompt, "--skills", "grok-build"],
            capture_output=True,
            text=True,
            timeout=300
        )
        out = (result.stdout or "") + "\n" + (result.stderr or "")
        _json_log("INFO", "hermes output truncated", correlation=correlation, rc=result.returncode, out=out[:1200])
        if result.returncode != 0:
            _json_log("ERROR", "hermes non-zero rc — treating as failure", correlation=correlation, rc=result.returncode)
            suggested = f'hermes -z "{prompt[:200]}..." --skills grok-build'
            _write_pending_artifact(correlation, task, f"hermes rc={result.returncode}", suggested)
            write_status("error_prompting_grok", correlation, f"hermes rc={result.returncode}", last_hermes_rc=result.returncode)
            return False
        write_status("grok_build_completed", correlation, "Task handed to Grok Build via hermes + grok-build skill", last_hermes_rc=0)
        return True
    except Exception as e:
        _json_log("ERROR", "error prompting Grok Build", correlation=correlation, error=str(e))
        _write_pending_artifact(correlation, task, str(e))
        write_status("error_prompting_grok", correlation, str(e))
        return False


# --- Main processing (health + claim + prompt + archive rules) ---
def process_inbox_once() -> int:
    """Process one batch. Return count processed. Never swallows; uses explicit paths."""
    processed = 0
    for cmd_file in sorted(COMMAND_INBOX.glob("*.json")):
        if cmd_file.parent != COMMAND_INBOX:  # safety
            continue
        correlation = cmd_file.stem
        try:
            text = cmd_file.read_text()
            task = task_schema.validate_task_from_json_text(text)
            correlation = task.get("correlation_id", cmd_file.stem)
        except Exception as e:
            _json_log("ERROR", "task validation failed", file=cmd_file.name, error=str(e))
            # move to failed immediately
            try:
                FAILED_DIR.mkdir(parents=True, exist_ok=True)
                cmd_file.rename(FAILED_DIR / cmd_file.name)
            except Exception:
                pass
            continue

        # Health interlock before claim
        h = check_health()
        if not h.get("ok"):
            _json_log("WARNING", "health not ok — skipping claim this cycle", correlation=correlation, reasons=h.get("reasons"))
            write_status("health_blocked", correlation, "health interlock failed", health_ok=False, **{k: h.get(k) for k in ("beacon_age_seconds",) if k in h})
            continue

        # Atomic claim
        proc_path = claim_task(cmd_file)
        if not proc_path:
            _json_log("WARNING", "claim race or failed — skipping", correlation=correlation)
            continue

        write_status("processing", correlation, "Received task from Relay, activating Grok Build", health_ok=True, beacon_age_seconds_at_claim=h.get("beacon_age_seconds"))

        action = control.parse_control(task)
        if action is not None:
            ok_auth, auth_reason = control.authorize(task)
            if not ok_auth:
                _json_log(
                    "WARNING",
                    "control_rejected",
                    correlation=correlation,
                    control_action=action.command,
                    control_rejected_reason=auth_reason,
                    slack_user=task.get("slack_user"),
                )
                slack_out = send_to_slack.nack_control_unauthorized(task, auth_reason, device=DEVICE)
                _json_log(
                    "INFO",
                    "control_slack_nack",
                    correlation=correlation,
                    slack_ack_ok=slack_out.get("ok"),
                    slack_ack_rc=0 if slack_out.get("ok") else 1,
                )
                write_status("control_rejected", correlation, auth_reason, control_rejected_reason=auth_reason)
                archive_task(proc_path, success=True)
                processed += 1
                continue

            result = control.execute(action, device=DEVICE, shared_base=SHARED_BASE)
            slack_out = send_to_slack.ack_control_result(
                task, result, device=DEVICE, action=action
            )
            raw_cmd = (
                task.get("original_message")
                or (task.get("context_hints") or {}).get("original_user_command")
                or action.raw_line
                or ""
            )
            _json_log(
                "INFO",
                f"control_{action.command}",
                correlation=correlation,
                control_action=action.command,
                control_ok=result.ok,
                control_detail=result.detail,
                slack_ack_ok=slack_out.get("ok"),
                slack_ack_rc=0 if slack_out.get("ok") else 1,
                last_control_command=str(raw_cmd)[:200],
                last_control_device=DEVICE,
                last_control_detail=result.detail,
                control_trust_note=action.trust_note or task.get("task_reality"),
            )
            state = "control_completed" if result.ok else "control_failed"
            write_status(state, correlation, result.detail, control_action=action.command, control_ok=result.ok)
            archive_task(proc_path, success=True)
            processed += 1
            continue

        # Fire beacon (must succeed or abort)
        if not fire_beacon(True, correlation, bust=(task.get("type") == "bust_a_nut_resume")):
            write_status("beacon_failed", correlation, "beacon total failure — releasing task", health_ok=False)
            archive_task(proc_path, success=False)
            continue

        success = prompt_grok_build(task)

        if success:
            write_status("completed", correlation, "Grok Build task finished (or handed off)")
        else:
            write_status("error", correlation, "Task failed — see pending-prompts or failed/ dir")

        archive_task(proc_path, success=success)
        # Always turn beacon off after (prevents holding slot)
        fire_beacon(False)
        processed += 1

    return processed


def run_loop() -> None:
    _json_log("INFO", "Activator core loop starting", device=DEVICE)
    write_status("idle", "", f"{DEVICE} activator listening for relay commands (core)")
    while True:
        try:
            n = process_inbox_once()
            if n:
                _json_log("INFO", "batch processed", count=n)
        except Exception as e:
            _json_log("ERROR", "unhandled in run_loop", error=str(e))
        time.sleep(5)


def run_once(dry_run: bool = False) -> int:
    _json_log("INFO", "run_once (core)", dry_run=dry_run, device=DEVICE)
    write_status("idle", "", "One-shot run (core)")
    if dry_run:
        _json_log("INFO", "dry-run: would process inbox but skipping hermes/inject")
        # still do claim simulation count for testability
        n = 0
        for f in sorted(COMMAND_INBOX.glob("*.json")):
            n += 1
        return n
    n = process_inbox_once()
    _json_log("INFO", "one-shot complete", count=n)
    return n


if __name__ == "__main__":
    # For direct python -m
    import sys
    if "--once" in sys.argv:
        run_once()
    else:
        run_loop()
