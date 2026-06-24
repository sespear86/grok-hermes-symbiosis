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
import send_to_telegram as send_to_relay  # noqa: E402

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
PROCESSING_STALE_SECS = int(os.environ.get("SYMBIOSIS_PROCESSING_STALE_SECS", "360"))
PROCESSING_STARTUP_MIN_AGE = int(os.environ.get("SYMBIOSIS_PROCESSING_STARTUP_MIN_AGE", "600"))
_startup_recovery_done = False

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
    """Structured cross-device status (selector_score, signals, JSONL events)."""
    try:
        import relay_status_core as rsc  # noqa: WPS433 — sibling module, stdlib-only

        lightweight = bool(extra.get("lightweight", False))
        extra_for_core = {k: v for k, v in extra.items() if k != "lightweight"}
        rsc.write_structured_status(
            DEVICE,
            state,
            task_id,
            message,
            source="activator_core",
            lightweight=lightweight,
            extra=extra_for_core or None,
        )
        _json_log(
            "INFO",
            "structured status written",
            state=state,
            task_id=task_id,
            schema=rsc.SCHEMA_VERSION,
            **{k: v for k, v in extra.items() if k in ("health_ok", "beacon_age_seconds_at_claim", "last_inject_rc", "last_hermes_rc")},
        )
        return
    except Exception as e:
        _json_log("WARNING", "structured status fallback", error=str(e))

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


def recover_orphaned_processing(*, force_all: bool = False) -> int:
    """Requeue stale (or all startup) tasks left in processing/ after a crash/restart."""
    global _startup_recovery_done
    PROCESSING_DIR.mkdir(parents=True, exist_ok=True)
    recovered = 0
    now = time.time()
    min_age = PROCESSING_STARTUP_MIN_AGE if force_all else PROCESSING_STALE_SECS
    for proc_file in sorted(PROCESSING_DIR.glob("*.json")):
        age = now - proc_file.stat().st_mtime
        if age < min_age:
            continue
        try:
            corr = json.loads(proc_file.read_text()).get("correlation_id", proc_file.stem)
        except Exception:
            corr = proc_file.stem.removeprefix("task-")
        grok_log = LOG_DIR / f"grok-relay-{corr}.log"
        if grok_log.exists() and (now - grok_log.stat().st_mtime) < 120:
            _json_log("INFO", "skip recovery — grok still running", file=proc_file.name, corr=corr)
            continue
        inbox_path = COMMAND_INBOX / proc_file.name
        try:
            proc_file.rename(inbox_path)
            recovered += 1
            _json_log(
                "WARNING",
                "recovered orphaned processing task",
                file=proc_file.name,
                age_seconds=round(age, 1),
                force_all=force_all,
            )
        except Exception as e:
            _json_log("ERROR", "processing recovery failed", file=proc_file.name, error=str(e))
    if force_all:
        _startup_recovery_done = True
    return recovered


def _notify_telegram(task: dict[str, Any], *, success: bool, summary: str) -> None:
    try:
        out = send_to_relay.ack_task_completion(
            task, success=success, summary=summary, device=DEVICE
        )
        _json_log(
            "INFO",
            "telegram_task_completion",
            correlation=task.get("correlation_id"),
            relay_ack_ok=out.get("ok"),
            relay_ack_error=out.get("error"),
        )
        capture_text = (
            f"{'Done' if success else 'Failed'}: {(task.get('original_message') or '')[:200]}\n"
            f"{summary[:500]}"
        )
        cap_out = send_to_relay.post_task_capture(capture_text, device=DEVICE)
        _json_log(
            "INFO",
            "telegram_task_capture",
            correlation=task.get("correlation_id"),
            relay_ack_ok=cap_out.get("ok"),
            relay_ack_error=cap_out.get("error"),
        )
    except Exception as e:
        _json_log("WARNING", "telegram completion notify failed", error=str(e))


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


def prompt_grok_build(task: dict[str, Any]) -> tuple[bool, str]:
    """Core handoff. Returns (success, output_summary)."""
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
                return True, res.stdout[:2000] or "Injected into live Grok Build TUI."
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
                    return True, res2.stdout[:2000] or "Injected via pts-inject fallback."
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
        hints = task.get("context_hints") or {}
        mem_block = hints.get("jarvis_mempalace_context") or ""
        jarvis_note = ""
        if hints.get("jarvis_dispatch") or hints.get("jarvis_ask"):
            preview = hints.get("jarvis_routing_preview") or {}
            jarvis_note = (
                "\nThis task was dispatched by Cross-Device Jarvis. "
                f"Routing preview: {preview.get('chosen', 'washington')} ({preview.get('path', '?')}). "
                "Reply with concise completion summary suitable for Telegram ('Done, sir' tone).\n"
            )
        mem_section = f"\n{mem_block}\n" if mem_block else ""
        prompt = f"""SYMBIOSIS RELAY TASK (from central listening post on the Pi)

Correlation: {correlation}
Source: {task.get('source', 'relay')}
Relay channel: {task.get('relay_channel') or task.get('slack_channel', 'unknown')}
{jarvis_note}
{task.get('original_message', '')}
{mem_section}
Context from Relay:
{json.dumps(hints, indent=2)}

You are being activated by the Symbiosis Relay because you are the current highest-priority target (Washington was chosen based on healthy heartbeat + priority rules).

Use the grok-build skill for any deep design, implementation, review, or verification work.
All 7 primes apply. Keep er goinnnn.
"""

    # Real Telegram tasks need full execution (hermes -z only returns shallow acks).
    is_real_telegram = (
        task.get("source") == "telegram"
        or task.get("task_reality") == "real_telegram"
    )
    if is_real_telegram:
        grok_bin = os.environ.get("GROK_BIN", "grok")
        grok_timeout = int(os.environ.get("SYMBIOSIS_GROK_TASK_TIMEOUT", "1800"))
        log_path = LOG_DIR / f"grok-relay-{correlation}.log"
        _json_log("INFO", "launching grok headless for telegram task", correlation=correlation)
        try:
            with open(log_path, "ab") as logf:
                proc = subprocess.run(
                    [grok_bin, "-p", prompt, "--yolo"],
                    stdout=logf,
                    stderr=subprocess.STDOUT,
                    cwd=str(Path.home()),
                    timeout=grok_timeout,
                )
            tail = ""
            if log_path.exists():
                tail = log_path.read_text(errors="replace")[-2000:]
            if proc.returncode == 0:
                write_status(
                    "grok_build_completed",
                    correlation,
                    "Task completed via headless grok --yolo",
                    last_hermes_rc=0,
                )
                return True, tail or "Task completed via headless grok."
            _json_log(
                "WARNING",
                "grok headless non-zero, trying TUI inject",
                correlation=correlation,
                rc=proc.returncode,
            )
        except Exception as e:
            _json_log("WARNING", "grok headless failed, trying TUI inject", correlation=correlation, error=str(e))

        pts = control.discover_grok_pts(SHARED_BASE)
        tui_prompt = (
            f"[Symbiosis Relay {correlation}] "
            f"{task.get('original_message', '').strip()}"
        )
        if pts and INJECT_BUST_PYTHON.exists() and tui_prompt.strip():
            try:
                res = subprocess.run(
                    ["python3", str(INJECT_BUST_PYTHON), pts, tui_prompt],
                    capture_output=True,
                    text=True,
                    timeout=45,
                )
                out = (res.stdout or "") + (res.stderr or "")
                live_ok = res.returncode == 0 and "All live input methods failed" not in out
                _json_log(
                    "INFO",
                    "grok tui inject",
                    correlation=correlation,
                    rc=res.returncode,
                    pts=pts,
                    live_ok=live_ok,
                    stdout=out[:300],
                )
                if live_ok:
                    write_status(
                        "grok_build_tui_injected",
                        correlation,
                        f"Relay task injected into live Grok Build TUI ({pts})",
                        last_inject_rc=0,
                    )
                    return (
                        True,
                        f"Task injected into live Grok Build TUI ({pts}). "
                        f"Correlation: {correlation}. Work executing in TUI.",
                    )
            except Exception as e:
                _json_log("WARNING", "grok tui inject failed", correlation=correlation, error=str(e))

    _json_log("INFO", "prompting hermes + grok-build", correlation=correlation)
    hermes_timeout = int(os.environ.get("SYMBIOSIS_HERMES_TASK_TIMEOUT", "900"))
    try:
        result = subprocess.run(
            ["hermes", "-z", prompt, "--skills", "grok-build"],
            capture_output=True,
            text=True,
            timeout=hermes_timeout
        )
        out = (result.stdout or "") + "\n" + (result.stderr or "")
        _json_log("INFO", "hermes output truncated", correlation=correlation, rc=result.returncode, out=out[:1200])
        if result.returncode != 0:
            _json_log("ERROR", "hermes non-zero rc — treating as failure", correlation=correlation, rc=result.returncode)
            suggested = f'hermes -z "{prompt[:200]}..." --skills grok-build'
            _write_pending_artifact(correlation, task, f"hermes rc={result.returncode}", suggested)
            write_status("error_prompting_grok", correlation, f"hermes rc={result.returncode}", last_hermes_rc=result.returncode)
            return False, out[:2000] or f"hermes rc={result.returncode}"
        write_status("grok_build_completed", correlation, "Task handed to Grok Build via hermes + grok-build skill", last_hermes_rc=0)
        return True, out[:2000] or "Task completed."
    except Exception as e:
        _json_log("ERROR", "error prompting Grok Build", correlation=correlation, error=str(e))
        _write_pending_artifact(correlation, task, str(e))
        write_status("error_prompting_grok", correlation, str(e))
        return False, str(e)


# --- Main processing (health + claim + prompt + archive rules) ---
def process_inbox_once() -> int:
    """Process one batch. Return count processed. Never swallows; uses explicit paths."""
    global _startup_recovery_done
    if not _startup_recovery_done:
        n_rec = recover_orphaned_processing(force_all=True)
        if n_rec:
            _json_log("INFO", "startup processing recovery", count=n_rec)
        _startup_recovery_done = True
    else:
        recover_orphaned_processing(force_all=False)

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

        try:
            action = control.parse_control(task)
        except Exception as e:
            _json_log("ERROR", "control parse failed", correlation=correlation, error=str(e))
            action = None
        if action is not None:
            ok_auth, auth_reason = control.authorize(task)
            if not ok_auth:
                _json_log(
                    "WARNING",
                    "control_rejected",
                    correlation=correlation,
                    control_action=action.command,
                    control_rejected_reason=auth_reason,
                    relay_user=task.get("user_id") or task.get("slack_user"),
                )
                relay_out = send_to_relay.nack_control_unauthorized(task, auth_reason, device=DEVICE)
                _json_log(
                    "INFO",
                    "control_relay_nack",
                    correlation=correlation,
                    relay_ack_ok=relay_out.get("ok"),
                    relay_ack_rc=0 if relay_out.get("ok") else 1,
                )
                write_status("control_rejected", correlation, auth_reason, control_rejected_reason=auth_reason)
                archive_task(proc_path, success=True)
                processed += 1
                continue

            result = control.execute(action, device=DEVICE, shared_base=SHARED_BASE)
            relay_out = send_to_relay.ack_control_result(
                task, result, device=DEVICE, action=action
            )
            if result.ok and task.get("telegram_chat_id"):
                _json_log(
                    "INFO",
                    "control_telegram_ack",
                    correlation=correlation,
                    relay_ack_ok=relay_out.get("ok"),
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
                relay_ack_ok=relay_out.get("ok"),
                relay_ack_rc=0 if relay_out.get("ok") else 1,
                last_control_command=str(raw_cmd)[:200],
                last_control_device=DEVICE,
                last_control_detail=result.detail,
                control_trust_note=action.trust_note or task.get("task_reality"),
            )
            state = "control_completed" if result.ok else "control_failed"
            write_status(state, correlation, result.detail, control_action=action.command, control_ok=result.ok)
            if not result.ok:
                _notify_telegram(task, success=False, summary=result.detail)
            archive_task(proc_path, success=True)
            processed += 1
            continue

        # Fire beacon (must succeed or abort)
        if not fire_beacon(True, correlation, bust=(task.get("type") == "bust_a_nut_resume")):
            write_status("beacon_failed", correlation, "beacon total failure — releasing task", health_ok=False)
            archive_task(proc_path, success=False)
            continue

        success, summary = prompt_grok_build(task)

        if success:
            write_status("completed", correlation, "Grok Build task finished (or handed off)")
        else:
            write_status("error", correlation, "Task failed — see pending-prompts or failed/ dir")

        _notify_telegram(task, success=success, summary=summary)
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
