#!/usr/bin/env python3
"""
control.py — Slack→Grok Build command parser + executor (AUTON 474101a5).

Imported by activator_core after claim, before fire_beacon / prompt_grok_build.
Stdlib + subprocess only. No shell=True on user text.
"""
from __future__ import annotations

import os
import subprocess
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


@dataclass
class ControlResult:
    ok: bool
    detail: str = ""
    command: str = ""


def _control_users() -> list[str]:
    return [u.strip() for u in os.environ.get("SYMBIOSIS_CONTROL_SLACK_USERS", "").split(",") if u.strip()]


def _trust_gate(task: dict[str, Any]) -> bool:
    if _allow_all():
        return True
    if task.get("task_reality") == "real_slack":
        return True
    if task.get("is_real") is True:
        return True
    return False


def _first_line(text: str) -> str:
    for line in (text or "").splitlines():
        s = line.strip()
        if s:
            return s
    return ""


def parse_control(task: dict[str, Any]) -> ControlAction | None:
    """Return ControlAction if message is a control prefix and trust gate passes."""
    if not _trust_gate(task):
        return None

    hints = task.get("context_hints") or {}
    if isinstance(hints, dict) and hints.get("command"):
        cmd = str(hints["command"]).strip().lower()
        if cmd in ("close", "open", "continue", "instruct", "autonomous", "status"):
            payload = str(hints.get("autonomous_idea") or hints.get("payload") or "")
            if cmd == "instruct" and not payload:
                payload = _parse_instruct_payload(task.get("original_message") or "")
            if cmd == "autonomous" and not payload:
                payload = _parse_autonomous_payload(task.get("original_message") or "")
            raw = (task.get("original_message") or "").strip().splitlines()[0] if task.get("original_message") else cmd
            return ControlAction(command=cmd, payload=payload, raw_line=raw)  # type: ignore[arg-type]

    text = task.get("original_message") or ""
    first = _first_line(text).lower()
    if not first:
        return None

    if first.startswith("grok close") or first.startswith("grok stand-down"):
        return ControlAction("close", "", _first_line(text))
    if first.startswith("grok open") or first.startswith("grok bust") or first == "bust a nut":
        return ControlAction("open", "", _first_line(text))
    if first.startswith("grok continue"):
        return ControlAction("continue", "", _first_line(text))
    if first.startswith("grok instruct:"):
        return ControlAction("instruct", text.split(":", 1)[1].strip(), _first_line(text))
    if first.startswith("grok autonomous:") or first.startswith("autonomous:"):
        return ControlAction("autonomous", _parse_autonomous_payload(text), _first_line(text))
    if first.startswith("grok status"):
        return ControlAction("status", "", _first_line(text))

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
            if paths["inject"].is_file():
                subprocess.run([str(paths["inject"])], check=False, timeout=60)
            return ControlResult(
                ok=True,
                detail="no live TUI pts; inject script attempted or queue via activator",
                command=cmd,
            )

        if cmd == "autonomous":
            idea = action.payload or "user request via Slack control"
            log_dir = Path.home() / "symbiosis-relay" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_path = log_dir / f"auton-launch-{int(time.time())}.log"
            argv = ["grok", "-p", f"/autonomous {idea}", "--yolo"]
            with open(log_path, "ab") as logf:
                subprocess.Popen(
                    argv,
                    stdout=logf,
                    stderr=subprocess.STDOUT,
                    cwd=str(Path.home()),
                    start_new_session=True,
                )
            auton_id = _poll_newest_auton_id(timeout=2.0)
            detail = f"Launched /autonomous on {device}"
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