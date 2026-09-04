"""Localhost UI smoke: bind 127.0.0.1, assign, health, no CDN."""

from __future__ import annotations

import threading
from http.client import HTTPConnection

from miragegrid.ui import _State, make_handler
from http.server import ThreadingHTTPServer

from pathlib import Path


def test_ui_html_is_self_contained() -> None:
    html = (Path(__file__).resolve().parents[1] / "miragegrid" / "templates" / "ui.html").read_text(encoding="utf-8")
    assert "cdn" not in html.lower()
    assert "http://" not in html
    assert "https://" not in html
    assert "<style>" in html
    assert "127.0.0.1" in html or "loopback" in html.lower()
    assert "VPN" in html or "anonymity" in html.lower()
    assert "node-mesh" in html.lower() or "mesh" in html.lower()


def test_ui_http_assign_and_end() -> None:
    handler = make_handler(_State())
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    host, port = httpd.server_address[:2]
    assert host == "127.0.0.1"
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", "/health")
        health = json_body(conn)
        assert health["ok"] is True
        assert health["bind_host"] == "127.0.0.1"

        conn.request("GET", "/")
        page = conn.getresponse()
        body = page.read().decode("utf-8")
        assert page.status == 200
        assert "MirageGrid" in body
        assert "cdn" not in body.lower()

        conn.request("POST", "/assign")
        assigned = json_body(conn)
        assert assigned["node_id"].startswith("node-")
        assert assigned["closed"] is False
        assert assigned["live_integrity"] == "PASS"

        conn.request("GET", "/session")
        snap = json_body(conn)
        assert snap["session_id"] == assigned["session_id"]

        conn.request("POST", "/end")
        ended = json_body(conn)
        assert ended["closed"] is True
        assert ended["node_id"] is None
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()


def json_body(conn: HTTPConnection) -> dict:
    import json

    resp = conn.getresponse()
    return json.loads(resp.read().decode("utf-8"))
