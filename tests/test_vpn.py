"""Userspace SOCKS mesh VPN on loopback."""

from __future__ import annotations

import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from miragegrid.session import MirageSession
from miragegrid.vpn import MeshVpn


class _Echo(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:  # noqa: A003
        return

    def do_GET(self) -> None:  # noqa: N802
        body = b"mesh-vpn-ok"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def test_relay_connect_through_circuit() -> None:
    httpd = HTTPServer(("127.0.0.1", 0), _Echo)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        with MirageSession() as session:
            vpn = MeshVpn(session, port=0)
            raw = vpn.relay_connect(host, port, b"GET / HTTP/1.1\r\nHost: x\r\n\r\n")
            assert b"mesh-vpn-ok" in raw
            st = vpn.status()
            assert st.entry == session.circuit.entry.node_id
            assert st.exit == session.circuit.exit.node_id
            assert len(st.hops) == 3
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_socks5_connect_loopback() -> None:
    httpd = HTTPServer(("127.0.0.1", 0), _Echo)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    dest_host, dest_port = httpd.server_address[:2]
    session = MirageSession()
    vpn = MeshVpn(session, port=0)
    try:
        host, port = vpn.start()
        assert host == "127.0.0.1"
        sock = socket.create_connection((host, port), timeout=5)
        sock.sendall(b"\x05\x01\x00")
        greet = sock.recv(2)
        assert greet == b"\x05\x00"
        req = b"\x05\x01\x00\x01" + socket.inet_aton("127.0.0.1") + dest_port.to_bytes(2, "big")
        sock.sendall(req)
        reply = sock.recv(10)
        assert reply[:2] == b"\x05\x00"
        sock.sendall(b"GET / HTTP/1.1\r\nHost: x\r\n\r\n")
        data = b""
        sock.settimeout(5)
        while b"mesh-vpn-ok" not in data:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        sock.close()
        assert b"mesh-vpn-ok" in data
    finally:
        vpn.stop()
        session.end()
        httpd.shutdown()
        httpd.server_close()
