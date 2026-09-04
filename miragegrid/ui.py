"""Localhost UI for the node-mesh VPN.

Binds 127.0.0.1 only. Self-contained HTML/CSS, no CDN.
Shows circuit hops, mesh route, and local SOCKS5 status.

Author: Aziel Eliab
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from miragegrid.mesh import NodeMesh
from miragegrid.session import MirageSession

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080

_TEMPLATE = Path(__file__).resolve().parent / "templates" / "ui.html"


def _html() -> bytes:
    return _TEMPLATE.read_bytes()


class _State:
    def __init__(self) -> None:
        self.mesh = NodeMesh()
        self.session: MirageSession | None = None
        self.vpn = None

    def snapshot(self, include_receipt: bool = False) -> dict[str, Any]:
        if self.session is None:
            return {
                "session_id": None,
                "node_id": None,
                "closed": True,
                "live_integrity": "FAIL",
                "kind": "mesh-vpn-circuit",
                "circuit": None,
                "vpn": None,
            }
        payload = self.session.to_dict(include_receipt=include_receipt)
        payload["live_integrity"] = self.session.integrity
        if include_receipt:
            try:
                payload["receipt"] = self.session.emit_receipt()
            except Exception:
                payload["receipt"] = None
        if self.vpn is not None:
            payload["vpn"] = self.vpn.status().to_dict()
        else:
            payload["vpn"] = None
        return payload

    def assign(self) -> dict[str, Any]:
        self._stop_vpn()
        if self.session is not None and not self.session.closed:
            self.session.end()
        self.session = MirageSession(mesh=self.mesh)
        return self.snapshot(include_receipt=False)

    def end(self) -> dict[str, Any]:
        self._stop_vpn()
        if self.session is not None and not self.session.closed:
            self.session.end()
        return self.snapshot(include_receipt=False)

    def start_vpn(self, port: int = 1080) -> dict[str, Any]:
        from miragegrid.vpn import MeshVpn

        if self.session is None or self.session.closed:
            self.assign()
        self._stop_vpn()
        self.vpn = MeshVpn(self.session, host=DEFAULT_HOST, port=int(port))
        self.vpn.start()
        return self.snapshot()

    def stop_vpn(self) -> dict[str, Any]:
        self._stop_vpn()
        return self.snapshot()

    def _stop_vpn(self) -> None:
        if self.vpn is not None:
            try:
                self.vpn.stop()
            except Exception:
                pass
            self.vpn = None


def make_handler(state: _State):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args: object) -> None:  # noqa: A003
            return

        def _json(self, body: dict[str, Any], status: int = 200) -> None:
            raw = json.dumps(body, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(raw)

        def _html(self) -> None:
            raw = _html()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path in ("/", "/index.html"):
                self._html()
                return
            if path == "/session":
                snap = state.snapshot(include_receipt=True)
                self._json(snap)
                return
            if path == "/nodes":
                self._json({"nodes": [n.to_dict() for n in state.mesh.pool]})
                return
            if path == "/mesh":
                self._json(state.mesh.to_dict())
                return
            if path == "/health":
                self._json(
                    {
                        "ok": True,
                        "bind_host": DEFAULT_HOST,
                        "kind": "node-mesh-vpn",
                        "product": "miragegrid",
                    }
                )
                return
            self._json({"error": "not found"}, 404)

        def do_POST(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path == "/assign":
                self._json(state.assign())
                return
            if path == "/end":
                self._json(state.end())
                return
            if path == "/vpn/start":
                self._json(state.start_vpn())
                return
            if path == "/vpn/stop":
                self._json(state.stop_vpn())
                return
            self._json({"error": "not found"}, 404)

    return Handler


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    if host not in ("127.0.0.1", "localhost", "::1"):
        host = DEFAULT_HOST
    httpd = ThreadingHTTPServer((host, int(port)), make_handler(_State()))
    print(f"miragegrid ui  http://{host}:{port}/  (loopback mesh-VPN console)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nmiragegrid ui stopped")
    finally:
        httpd.server_close()
