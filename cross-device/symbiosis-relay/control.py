#!/usr/bin/env python3
"""
control.py — Slack→Grok Build command parser + executor (AUTON 474101a5).

Imported by activator_core after claim, before fire_beacon / prompt_grok_build.
Stdlib + subprocess only. No shell=True on user text.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

CommandName = Literal["close", "open", "continue", "instruct", "autonomous", "status"]

def _allow_all() -> bool:
    return os.environ.get("SYMBIOSIS_CONTROL_ALLOW_ALL", "0") == "1"


def _dry_run() -> bool:
    return os.environ.get("SYMBIOSIS_CONTROL_DRY_RUN", "0") == "1"


@dataclass
class ControlAction:
    command: CommandName
    payload: str
    raw_line: str
    trust_note: str = ""
    run_in_tui: bool = False
    device_hint: str | None = None


@dataclass
class ControlResult:
    ok: bool
    detail: str = ""
    command: str = ""


def _control_users() -> list[str]:
    return [u.strip() for u in os.environ.get("SYMBIOSIS_CONTROL_SLACK_USERS", "").split(",") if u.strip()]


def _control_trust_text(task: dict[str, Any]) -> str:
    hints = task.get("context_hints") or {}
    if isinstance(hints, dict):
        return str(task.get("original_message") or hints.get("original_user_command") or "")
    return str(task.get("original_message") or "")


def _trust_gate(task: dict[str, Any]) -> tuple[bool, str]:
    if _allow_all():
        return True, "allow_all"
    hints = task.get("context_hints") or {}
    if hints.get("force_control"):
        print(
            json.dumps({"event": "control_trust_override", "note": "force_control_hint"}),
            file=sys.stderr,
        )
        return True, "force_control_hint"
    text = _control_trust_text(task)
    first = _first_line(text).lower()
    low = text.lower()
    if "/autonomous" in low or first.startswith(
        ("have grok build run", "grok build run", "run /autonomous", "run the autonomous")
    ):
        print(
            json.dumps({"event": "control_trust_override", "note": "control_command_override"}),
            file=sys.stderr,
        )
        return True, "control_command_override"
    if task.get("task_reality") == "real_slack":
        return True, "real_slack"
    if task.get("is_real") is True:
        return True, "is_real"
    return False, "no_trust"


def enrich_control_hints(text: str, hints: dict[str, Any]) -> dict[str, Any]:
    """Pre-parse Slack text for explicit device + force_control (AUTON 98822e73)."""
    low = (text or "").lower()
    if "on the washington device" in low or ("washington" in low and "device" in low):
        hints["explicit_target_device"] = "washington"
    elif "on the oregon device" in low or ("oregon" in low and "device" in low):
        hints["explicit_target_device"] = "oregon"
    if "/autonomous" in low or low.strip().startswith(("have grok build run", "grok build run")):
        hints["force_control"] = True
        hints["original_user_command"] = text
        hints.setdefault("run_in_tui", True)
    return hints


_DEVICE_SUFFIX_RE = re.compile(
    r",?\s*on the (washington|oregon) device\.?\s*$",
    re.IGNORECASE,
)


def _strip_device_suffix(idea: str) -> str:
    return _DEVICE_SUFFIX_RE.sub("", (idea or "").strip()).strip()


def _device_hint_from_text(text: str) -> str | None:
    low = (text or "").lower()
    if "on the washington device" in low or ("washington" in low and "device" in low):
        return "washington"
    if "on the oregon device" in low or ("oregon" in low and "device" in low):
        return "oregon"
    return None


def _parse_natural_autonomous_command(text: str) -> tuple[str | None, str | None]:
    """Return (full_payload `/autonomous <idea>`, device_hint) or (None, None)."""
    if not (text or "").strip():
        return None, None
    raw = text
    device_hint = _device_hint_from_text(raw)
    patterns = [
        r'have\s+grok\s+build\s+run\s+"?/autonomous\s+([^"]+)"?',
        r"grok\s+build\s+run\s+/autonomous\s+(.+)",
        r"run\s+(?:the\s+)?/autonomous\s+(.+)",
        r'"/autonomous\s+([^"]+)"',
    ]
    idea: str | None = None
    for pat in patterns:
        m = re.search(pat, raw, re.IGNORECASE | re.DOTALL)
        if m:
            idea = _strip_device_suffix(m.group(1))
            break
    if not idea:
        return None, device_hint
    full_payload = f"/autonomous {idea}"
    print(
        json.dumps(
            {
                "event": "control_nl_parse",
                "payload_len": len(full_payload),
                "device": device_hint,
            }
        ),
        file=sys.stderr,
    )
    return full_payload, device_hint


def _first_line(text: str) -> str:
    for line in (text or "").splitlines():
        s = line.strip()
        if s:
            return s
    return ""


def parse_control(task: dict[str, Any]) -> ControlAction | None:
    """Return ControlAction if message is a control prefix and trust gate passes."""
    ok_trust, trust_note = _trust_gate(task)
    if not ok_trust:
        return None

    hints = task.get("context_hints") or {}
    if not isinstance(hints, dict):
        hints = {}
    run_in_tui = bool(hints.get("run_in_tui", True))

    if hints.get("command"):
        cmd = str(hints["command"]).strip().lower()
        if cmd in ("close", "open", "continue", "instruct", "autonomous", "status"):
            payload = str(hints.get("autonomous_idea") or hints.get("payload") or "")
            if cmd == "instruct" and not payload:
                payload = _parse_instruct_payload(task.get("original_message") or "")
            if cmd == "autonomous" and not payload:
                idea = str(hints.get("autonomous_idea") or "")
                payload = f"/autonomous {idea}" if idea else _parse_autonomous_payload(task.get("original_message") or "")
            raw = (task.get("original_message") or "").strip().splitlines()[0] if task.get("original_message") else cmd
            if cmd == "autonomous" and payload and not str(payload).startswith("/autonomous"):
                payload = f"/autonomous {payload}"
            if cmd in ("instruct", "autonomous") and run_in_tui and str(payload).startswith("/autonomous"):
                return ControlAction(
                    "instruct",
                    str(payload),
                    raw,
                    trust_note=trust_note,
                    run_in_tui=True,
                )
            return ControlAction(
                cmd,  # type: ignore[arg-type]
                payload,
                raw,
                trust_note=trust_note,
                run_in_tui=run_in_tui,
            )

    text = _control_trust_text(task)
    first = _first_line(text).lower()
    if not first:
        return None

    if first.startswith("grok close") or first.startswith("grok stand-down"):
        return ControlAction("close", "", _first_line(text), trust_note=trust_note)
    if first.startswith("grok open") or first.startswith("grok bust") or first == "bust a nut":
        return ControlAction("open", "", _first_line(text), trust_note=trust_note)
    if first.startswith("grok continue"):
        return ControlAction("continue", "", _first_line(text), trust_note=trust_note)
    if first.startswith("grok instruct:"):
        return ControlAction("instruct", text.split(":", 1)[1].strip(), _first_line(text), trust_note=trust_note)
    if first.startswith("grok autonomous:") or first.startswith("autonomous:"):
        idea = _parse_autonomous_payload(text)
        payload = f"/autonomous {idea}" if idea else ""
        if run_in_tui and payload:
            return ControlAction("instruct", payload, _first_line(text), trust_note=trust_note, run_in_tui=True)
        return ControlAction("autonomous", idea, _first_line(text), trust_note=trust_note, run_in_tui=run_in_tui)
    if first.startswith("grok status"):
        return ControlAction("status", "", _first_line(text), trust_note=trust_note)

    nl_payload, device_hint = _parse_natural_autonomous_command(text)
    if nl_payload:
        if hints.get("parsed_device") is None and device_hint:
            hints = dict(hints)
            hints["parsed_device"] = device_hint
        return ControlAction(
            "instruct",
            nl_payload,
            _first_line(text),
            trust_note=trust_note,
            run_in_tui=run_in_tui,
            device_hint=device_hint,
        )

    return None


def _parse_instruct_payload(text: str) -> str:
    if ":" in text:
        return text.split(":", 1)[1].strip()
    return text.strip()


def _parse_autonomous_payload(text: str) -> str:
    first = _first_line(text)
    low = first.lower()
    if low.startswith("grok autonomous:"):
        return first.split(":", 1)[1].strip()
    if low.startswith("autonomous:"):
        return first.split(":", 1)[1].strip()
    return ""


def authorize(task: dict[str, Any]) -> tuple[bool, str]:
    """Deny-by-default for real_slack unless user in allowlist or ALLOW_ALL."""
    if _allow_all():
        return True, "allow_all"
    users = _control_users()
    if not users:
        return False, "allowlist_empty"
    uid = task.get("slack_user") or task.get("user_id")
    if uid and uid in users:
        return True, "ok"
    return False, "not_in_allowlist"


def discover_grok_pts(shared_base: Path) -> str | None:
    """Return bare pts/N for pts-inject-input.py, or None."""
    marker_path = shared_base / "device-presence" / ".current_bust_tui_pane"
    if marker_path.exists():
        raw = marker_path.read_text().strip()
        if raw.startswith("grok:pts:"):
            return raw.split("grok:pts:", 1)[1].strip()
        if raw.startswith("pts/"):
            return raw

    try:
        r = subprocess.run(
            ["pgrep", "-u", os.environ.get("USER", os.getlogin()), "-x", "grok"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if r.returncode != 0 or not r.stdout.strip():
            return None
        pid = r.stdout.strip().splitlines()[0].strip()
        fd_dir = Path(f"/proc/{pid}/fd")
        if not fd_dir.is_dir():
            return None
        for link in fd_dir.iterdir():
            try:
                target = os.readlink(link)
                if "/dev/pts/" in target:
                    return "pts/" + target.rsplit("/dev/pts/", 1)[-1]
            except OSError:
                continue
    except Exception:
        return None
    return None


def _tool_paths(shared_base: Path) -> dict[str, Path]:
    tools = shared_base / "symbiosis-relay" / "tools"
    stand = Path(os.environ.get("SYMBIOSIS_STAND_DOWN_SCRIPT", str(tools / "bust-a-nut-stand-down.sh")))
    return {
        "stand_down": stand,
        "inject": tools / "inject-bust-a-nut-into-running-tui.sh",
        "continue": tools / "bust-a-nut-continue.sh",
        "pts": tools / "pts-inject-input.py",
    }


def execute(
    action: ControlAction,
    *,
    device: str,
    shared_base: Path,
) -> ControlResult:
    """Run mapped scripts / grok launch. Respects SYMBIOSIS_CONTROL_DRY_RUN."""
    paths = _tool_paths(shared_base)
    cmd = action.command

    if _dry_run():
        return ControlResult(ok=True, detail=f"dry_run:{cmd}", command=cmd)

    try:
        if cmd == "close":
            subprocess.run([str(paths["stand_down"])], check=False, timeout=30)
            return ControlResult(ok=True, detail="stand-down executed (does not kill TUI)", command=cmd)

        if cmd == "open":
            marker = shared_base / "device-presence" / ".bust_a_nut_intent_active"
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.touch()
            subprocess.run([str(paths["inject"])], check=False, timeout=60)
            return ControlResult(ok=True, detail="open: intent + inject attempted", command=cmd)

        if cmd == "continue":
            subprocess.run([str(paths["continue"])], check=False, timeout=30)
            return ControlResult(ok=True, detail="continue script invoked", command=cmd)

        if cmd == "instruct":
            pts = discover_grok_pts(shared_base)
            text = action.payload
            if pts and paths["pts"].is_file():
                subprocess.run(
                    ["python3", str(paths["pts"]), pts, text],
                    check=False,
                    timeout=30,
                )
                return ControlResult(ok=True, detail=f"instruct injected on {pts}", command=cmd)
            if text.strip().startswith("/autonomous"):
                log_dir = Path.home() / "symbiosis-relay" / "logs"
                log_dir.mkdir(parents=True, exist_ok=True)
                log_path = log_dir / f"auton-launch-{int(time.time())}.log"
                argv = ["grok", "-p", text.strip(), "--yolo"]
                with open(log_path, "ab") as logf:
                    subprocess.Popen(
                        argv,
                        stdout=logf,
                        stderr=subprocess.STDOUT,
                        cwd=str(Path.home()),
                        start_new_session=True,
                    )
                return ControlResult(
                    ok=True,
                    detail=f"no pts; headless fallback {text.strip()[:120]}",
                    command=cmd,
                )
            if paths["inject"].is_file():
                subprocess.run([str(paths["inject"])], check=False, timeout=60)
            return ControlResult(
                ok=True,
                detail="no live TUI pts; inject script attempted or queue via activator",
                command=cmd,
            )

        if cmd == "autonomous":
            idea = action.payload or "user request via Slack control"
            launch_text = idea if str(idea).startswith("/autonomous") else f"/autonomous {idea}"
            if action.run_in_tui or str(idea).startswith("/autonomous"):
                pts = discover_grok_pts(shared_base)
                if pts and paths["pts"].is_file():
                    subprocess.run(
                        ["python3", str(paths["pts"]), pts, launch_text],
                        check=False,
                        timeout=30,
                    )
                    return ControlResult(
                        ok=True,
                        detail=f"autonomous injected on {pts}: {launch_text[:120]}",
                        command=cmd,
                    )
            log_dir = Path.home() / "symbiosis-relay" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_path = log_dir / f"auton-launch-{int(time.time())}.log"
            argv = ["grok", "-p", launch_text, "--yolo"]
            with open(log_path, "ab") as logf:
                subprocess.Popen(
                    argv,
                    stdout=logf,
                    stderr=subprocess.STDOUT,
                    cwd=str(Path.home()),
                    start_new_session=True,
                )
            auton_id = _poll_newest_auton_id(timeout=2.0)
            detail = f"Launched {launch_text} on {device}"
            if auton_id:
                detail += f" (AUTON {auton_id})"
            return ControlResult(ok=True, detail=detail, command=cmd)

        if cmd == "status":
            status_path = shared_base / "symbiosis-relay" / "status" / device / "status.json"
            presence = shared_base / "device-presence" / f"{device}-grok-build-presence.json"
            parts = [f"status for {device}"]
            if status_path.exists():
                parts.append(status_path.read_text()[:500])
            if presence.exists():
                parts.append(f"beacon: {presence.read_text()[:300]}")
            return ControlResult(ok=True, detail="\n".join(parts), command=cmd)

    except Exception as e:
        return ControlResult(ok=False, detail=str(e), command=cmd)

    return ControlResult(ok=False, detail="unknown command", command=cmd)


def _poll_newest_auton_id(timeout: float) -> str | None:
    root = Path.home() / ".grok" / "auton-projects"
    if not root.is_dir():
        return None
    deadline = time.time() + timeout
    while time.time() < deadline:
        dirs = [d for d in root.iterdir() if d.is_dir()]
        if dirs:
            newest = max(dirs, key=lambda p: p.stat().st_mtime)
            name = newest.name
            if len(name) >= 8:
                return name[:8]
        time.sleep(0.2)
    return None