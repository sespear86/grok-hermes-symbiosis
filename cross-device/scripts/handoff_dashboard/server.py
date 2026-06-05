# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 3694a72b implementer batch1) -->
"""Stdlib HTTP server for read-only handoff kanban dashboard."""
from __future__ import annotations

import json
import mimetypes
import re
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .collectors import collect_board_for_device, render_format
from .paths import handoff_format_path, static_dir

_COMPLETED_LIMIT_RE = re.compile(r"^[1-9][0-9]?$|^50$")


def _parse_completed_limit(raw: str | None, default: int) -> int | None:
    if raw is None or raw == "":
        return default
    if not _COMPLETED_LIMIT_RE.match(raw.strip()):
        return None
    n = int(raw)
    return n if 1 <= n <= 50 else None


def make_handler(
    *,
    device: str,
    repo_root: Path,
    mempalace_root: Path,
    completed_limit_default: int,
    include_presence: bool,
) -> type[BaseHTTPRequestHandler]:
    repo_root = repo_root.resolve()
    mempalace_root = mempalace_root.resolve()
    static_root = static_dir().resolve()

    class DashboardHandler(BaseHTTPRequestHandler):
        server_version = "SymbiosisHandoffDashboard/1.0"

        def _send_cors(self) -> None:
            self.send_header("Access-Control-Allow-Origin", "*")

        def _send_json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self._send_cors()
            self.end_headers()
            self.wfile.write(body)

        def _send_bytes(
            self, status: int, body: bytes, content_type: str
        ) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self._send_cors()
            self.end_headers()
            self.wfile.write(body)

        def _repo_valid(self) -> bool:
            return handoff_format_path(repo_root).is_file()

        def _handle_healthz(self) -> None:
            payload = {
                "status": "ok",
                "device": device,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self._send_json(HTTPStatus.OK, payload)

        def _handle_kanban(self, query: dict[str, list[str]]) -> None:
            if not self._repo_valid():
                self._send_bytes(
                    HTTPStatus.BAD_REQUEST,
                    b"invalid repo\n",
                    "text/plain; charset=utf-8",
                )
                return
            fmt_list = query.get("format", ["json"])
            fmt = (fmt_list[0] if fmt_list else "json").strip().lower()
            if fmt == "markdown":
                fmt = "md"
            if fmt not in ("json", "md", "board"):
                self._send_bytes(
                    HTTPStatus.BAD_REQUEST,
                    b"format must be json, md, or board\n",
                    "text/plain; charset=utf-8",
                )
                return
            limit_raw = query.get("completed_limit", [None])
            limit_s = limit_raw[0] if limit_raw else None
            limit = _parse_completed_limit(limit_s, completed_limit_default)
            if limit is None:
                self._send_bytes(
                    HTTPStatus.BAD_REQUEST,
                    b"completed_limit must be 1-50\n",
                    "text/plain; charset=utf-8",
                )
                return
            model = collect_board_for_device(
                device=device,
                repo_root=repo_root,
                mempalace_root=mempalace_root,
                completed_limit=limit,
                include_presence=include_presence,
            )
            model["meta"]["format"] = fmt
            body_s, ctype = render_format(model, fmt)
            self._send_bytes(HTTPStatus.OK, body_s.encode("utf-8"), ctype)

        def _safe_static_path(self, url_path: str) -> Path | None:
            rel = url_path.lstrip("/")
            if rel.startswith("static/"):
                rel = rel[len("static/") :]
            candidate = (static_root / rel).resolve()
            try:
                ok = candidate.is_relative_to(static_root)
            except AttributeError:
                ok = str(candidate).startswith(str(static_root) + "/") or candidate == static_root
            if not ok or not candidate.is_file():
                return None
            return candidate

        def _serve_static_file(self, path: Path) -> None:
            data = path.read_bytes()
            ctype, _ = mimetypes.guess_type(str(path))
            if not ctype:
                if path.suffix == ".js":
                    ctype = "application/javascript; charset=utf-8"
                elif path.suffix == ".css":
                    ctype = "text/css; charset=utf-8"
                else:
                    ctype = "application/octet-stream"
            self._send_bytes(HTTPStatus.OK, data, ctype)

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            path = parsed.path.rstrip("/") or "/"
            query = parse_qs(parsed.query)

            if path == "/healthz":
                self._handle_healthz()
                return
            if path == "/api/kanban":
                self._handle_kanban(query)
                return
            if path in ("/", "/index.html"):
                index = static_root / "index.html"
                if index.is_file():
                    self._serve_static_file(index)
                else:
                    self._send_bytes(HTTPStatus.NOT_FOUND, b"index missing\n", "text/plain")
                return
            if path.startswith("/static/"):
                rel = self._safe_static_path(path)
                if rel:
                    self._serve_static_file(rel)
                    return
            self._send_bytes(HTTPStatus.NOT_FOUND, b"not found\n", "text/plain; charset=utf-8")

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
            pass

    return DashboardHandler


def create_server(
    host: str,
    port: int,
    handler_cls: type[BaseHTTPRequestHandler],
) -> HTTPServer:
    return HTTPServer((host, port), handler_cls)


def validate_bind_host(host: str, allow_lan: bool) -> str | None:
    """Return error message if bind should be refused."""
    h = host.strip().lower()
    if h in ("127.0.0.1", "localhost", "::1"):
        return None
    if h in ("0.0.0.0", "::", "") and not allow_lan:
        return (
            "refusing to bind to all interfaces without --allow-lan; "
            "use 127.0.0.1 or pass --allow-lan"
        )
    if not allow_lan and h not in ("127.0.0.1", "localhost", "::1"):
        return f"refusing non-localhost bind {host!r} without --allow-lan"
    return None