"""Userspace node-mesh VPN gateway.

Local SOCKS5 on loopback. Streams are onion-wrapped through a MirageGrid
circuit and forwarded along the 25-node mesh. Default bind is 127.0.0.1.

This is a lawful privacy tool. It is not a crime kit. It does not wipe
logs and it does not claim to defeat a global adversary.

Author: Aziel Eliab
"""

from __future__ import annotations

import socket
import struct
import threading
from dataclasses import dataclass
from typing import Callable

from miragegrid.circuit import Circuit
from miragegrid.mesh import NodeMesh
from miragegrid.session import MirageSession
from miragegrid.transport import InProcessMesh

DEFAULT_VPN_HOST = "127.0.0.1"
DEFAULT_VPN_PORT = 1080


class VpnError(Exception):
    """SOCKS / mesh VPN error."""


@dataclass
class VpnStatus:
    host: str
    port: int
    listening: bool
    session_id: str | None
    entry: str | None
    exit: str | None
    hops: list[str]
    path: list[str]

    def to_dict(self) -> dict:
        return {
            "host": self.host,
            "port": self.port,
            "listening": self.listening,
            "session_id": self.session_id,
            "entry": self.entry,
            "exit": self.exit,
            "hops": self.hops,
            "path": self.path,
            "kind": "socks5-mesh-vpn",
        }


class MeshVpn:
    """SOCKS5 gateway bound to a live ``MirageSession`` circuit."""

    def __init__(
        self,
        session: MirageSession,
        *,
        host: str = DEFAULT_VPN_HOST,
        port: int = DEFAULT_VPN_PORT,
        connect: Callable[[str, int], socket.socket] | None = None,
    ) -> None:
        if session.closed:
            raise VpnError("session mapping destroyed")
        self.session = session
        self.host = host if host in ("127.0.0.1", "localhost", "::1") else DEFAULT_VPN_HOST
        self.port = int(port)
        self._connect = connect or _tcp_connect
        self._sock: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._clients: list[socket.socket] = []
        self._mesh = InProcessMesh(session.mesh, session.circuit)

    @property
    def circuit(self) -> Circuit:
        return self.session.circuit

    def status(self) -> VpnStatus:
        c = None if self.session.closed else self.session.circuit
        return VpnStatus(
            host=self.host,
            port=self.port if self._sock is None else self._sock.getsockname()[1],
            listening=self._sock is not None and not self._stop.is_set(),
            session_id=self.session.session_id,
            entry=None if c is None else c.entry.node_id,
            exit=None if c is None else c.exit.node_id,
            hops=[] if c is None else c.hop_ids,
            path=[] if c is None else c.path_ids,
        )

    def start(self) -> tuple[str, int]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(32)
        sock.settimeout(0.5)
        self._sock = sock
        self.port = sock.getsockname()[1]
        self._stop.clear()
        self._thread = threading.Thread(target=self._accept_loop, daemon=True)
        self._thread.start()
        return self.host, self.port

    def stop(self) -> None:
        self._stop.set()
        if self._sock is not None:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None
        for c in list(self._clients):
            try:
                c.close()
            except OSError:
                pass
        self._clients.clear()
        if self._thread is not None:
            self._thread.join(timeout=2)
            self._thread = None

    def relay_connect(self, host: str, port: int, payload: bytes = b"") -> bytes:
        """Build a CONNECT through the onion mesh and optionally send ``payload``.

        Used by tests and the SOCKS handler. The destination is reached from
        the exit hop after the circuit unwraps.
        """
        request = _pack_connect(host, port, payload)
        opened = self._mesh.send(request)
        dest_host, dest_port, rest = _unpack_connect(opened)
        remote = self._connect(dest_host, dest_port)
        try:
            if rest:
                remote.sendall(rest)
                remote.settimeout(5)
                return _recv_some(remote)
            return b""
        finally:
            remote.close()

    def _accept_loop(self) -> None:
        assert self._sock is not None
        while not self._stop.is_set():
            try:
                conn, _addr = self._sock.accept()
            except TimeoutError:
                continue
            except OSError:
                break
            self._clients.append(conn)
            threading.Thread(target=self._socks_client, args=(conn,), daemon=True).start()

    def _socks_client(self, conn: socket.socket) -> None:
        remote: socket.socket | None = None
        try:
            dest = _socks5_handshake(conn)
            if dest is None:
                return
            host, port = dest
            opened = self._mesh.send(_pack_connect(host, port, b""))
            dest_host, dest_port, _rest = _unpack_connect(opened)
            remote = self._connect(dest_host, dest_port)
            conn.sendall(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
            _pipe(conn, remote, self._stop)
        except OSError:
            return
        finally:
            try:
                conn.close()
            except OSError:
                pass
            if remote is not None:
                try:
                    remote.close()
                except OSError:
                    pass


def _tcp_connect(host: str, port: int) -> socket.socket:
    return socket.create_connection((host, port), timeout=10)


def _recv_some(sock: socket.socket, limit: int = 65536) -> bytes:
    chunks = []
    sock.settimeout(2)
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            chunks.append(data)
            if sum(len(c) for c in chunks) >= limit:
                break
    except TimeoutError:
        pass
    return b"".join(chunks)


def _pack_connect(host: str, port: int, payload: bytes) -> bytes:
    hb = host.encode("utf-8")
    if len(hb) > 255:
        raise VpnError("hostname too long")
    return bytes([len(hb)]) + hb + port.to_bytes(2, "big") + payload


def _unpack_connect(blob: bytes) -> tuple[str, int, bytes]:
    if not blob:
        raise VpnError("empty circuit payload")
    n = blob[0]
    host = blob[1 : 1 + n].decode("utf-8")
    port = int.from_bytes(blob[1 + n : 3 + n], "big")
    rest = blob[3 + n :]
    return host, port, rest


def _socks5_handshake(conn: socket.socket) -> tuple[str, int] | None:
    greeting = _recv_exact(conn, 2)
    if len(greeting) < 2 or greeting[0] != 5:
        return None
    nmethods = greeting[1]
    _recv_exact(conn, nmethods)
    conn.sendall(b"\x05\x00")
    req = _recv_exact(conn, 4)
    if len(req) < 4 or req[0] != 5 or req[1] != 1:
        conn.sendall(b"\x05\x07\x00\x01\x00\x00\x00\x00\x00\x00")
        return None
    atyp = req[3]
    if atyp == 1:
        raw = _recv_exact(conn, 4)
        host = socket.inet_ntoa(raw)
    elif atyp == 3:
        ln = _recv_exact(conn, 1)
        if not ln:
            return None
        host = _recv_exact(conn, ln[0]).decode("ascii", errors="replace")
    elif atyp == 4:
        raw = _recv_exact(conn, 16)
        host = socket.inet_ntop(socket.AF_INET6, raw)
    else:
        conn.sendall(b"\x05\x08\x00\x01\x00\x00\x00\x00\x00\x00")
        return None
    port_b = _recv_exact(conn, 2)
    port = int.from_bytes(port_b, "big")
    return host, port


def _recv_exact(conn: socket.socket, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            return buf
        buf += chunk
    return buf


def _pipe(a: socket.socket, b: socket.socket, stop: threading.Event) -> None:
    def one_way(src: socket.socket, dst: socket.socket) -> None:
        try:
            while not stop.is_set():
                data = src.recv(4096)
                if not data:
                    break
                dst.sendall(data)
        except OSError:
            return

    t = threading.Thread(target=one_way, args=(b, a), daemon=True)
    t.start()
    one_way(a, b)
    t.join(timeout=2)


def serve_vpn(
    host: str = DEFAULT_VPN_HOST,
    port: int = DEFAULT_VPN_PORT,
    *,
    session: MirageSession | None = None,
) -> None:
    mesh = NodeMesh()
    sess = session if session is not None else MirageSession(mesh=mesh)
    vpn = MeshVpn(sess, host=host, port=port)
    h, p = vpn.start()
    print(f"miragegrid vpn  socks5://{h}:{p}/  entry={vpn.circuit.entry.node_id} exit={vpn.circuit.exit.node_id}")
    print("Lawful privacy tool. Loopback SOCKS5 over the 25-node mesh.")
    try:
        while True:
            threading.Event().wait(3600)
    except KeyboardInterrupt:
        print("\nmiragegrid vpn stopped")
    finally:
        vpn.stop()
        sess.end()
