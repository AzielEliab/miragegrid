"""Mesh frame forwarding: in-process hop and optional TCP peer links.

Frames are length-prefixed. Each hop unwraps one onion layer when it is
an onion node; otherwise it only forwards along the mesh path.

Author: Aziel Eliab
"""

from __future__ import annotations

import socket
import struct
import threading
from dataclasses import dataclass, field
from typing import Callable

from miragegrid.circuit import Circuit
from miragegrid.crypto import aead_decrypt, aead_encrypt, hkdf_sha256, x25519
from miragegrid.mesh import NodeMesh
from miragegrid.pool import POOL_SIZE

MAGIC = b"MG20"
KIND_DATA = 1
KIND_OPEN = 2
KIND_CLOSE = 3
MAX_FRAME = 65535


def _link_key(secret_a: bytes, public_b: bytes) -> bytes:
    shared = x25519(secret_a, public_b)
    return hkdf_sha256(shared, salt=b"mirage-link", info=b"chacha", length=32)


def _link_nonce(src: int, dst: int, seq: int) -> bytes:
    raw = src.to_bytes(1, "big") + dst.to_bytes(1, "big") + seq.to_bytes(4, "big")
    return hkdf_sha256(raw, salt=b"mirage-link-nonce", info=b"n", length=12)


@dataclass
class MeshFrame:
    kind: int
    ttl: int
    src: int
    dst: int
    circuit_id: bytes
    seq: int
    payload: bytes

    def encode(self) -> bytes:
        if len(self.circuit_id) != 16:
            raise ValueError("circuit_id must be 16 bytes")
        if len(self.payload) > MAX_FRAME:
            raise ValueError("payload too large")
        header = (
            MAGIC
            + bytes([1, self.kind & 0xFF, self.ttl & 0xFF, self.src & 0xFF, self.dst & 0xFF])
            + self.circuit_id
            + self.seq.to_bytes(4, "big")
            + len(self.payload).to_bytes(2, "big")
        )
        return header + self.payload

    @classmethod
    def decode(cls, blob: bytes) -> "MeshFrame":
        if len(blob) < 4 + 5 + 16 + 4 + 2:
            raise ValueError("truncated frame")
        if blob[:4] != MAGIC:
            raise ValueError("bad magic")
        kind, ttl, src, dst = blob[5], blob[6], blob[7], blob[8]
        circuit_id = blob[9:25]
        seq = int.from_bytes(blob[25:29], "big")
        plen = int.from_bytes(blob[29:31], "big")
        payload = blob[31 : 31 + plen]
        if len(payload) != plen:
            raise ValueError("truncated payload")
        return cls(kind=kind, ttl=ttl, src=src, dst=dst, circuit_id=circuit_id, seq=seq, payload=payload)


def encode_cell(kind: int, src: int, dst: int, circuit: Circuit, plaintext: bytes, *, ttl: int = 16) -> bytes:
    wrapped = circuit.wrap(plaintext)
    frame = MeshFrame(
        kind=kind,
        ttl=ttl,
        src=src,
        dst=dst,
        circuit_id=circuit.circuit_id,
        seq=0,
        payload=wrapped,
    )
    return frame.encode()


class InProcessMesh:
    """All 25 nodes in one process. Real onion unwrap + mesh forwarding."""

    def __init__(self, mesh: NodeMesh, circuit: Circuit) -> None:
        self.mesh = mesh
        self.circuit = circuit
        self._lock = threading.Lock()
        self._seq = 0

    def send(self, plaintext: bytes) -> bytes:
        """Inject at the entry hop; return the exit-unwrapped payload."""
        with self._lock:
            cell = self.circuit.wrap(plaintext)
            body = cell
            for i in range(len(self.circuit.hops)):
                body = self.circuit.unwrap_hop(body, i)
            return body

    def forward_path(self) -> list[str]:
        return self.circuit.path_ids


class MeshListener:
    """TCP mesh peer. Length-prefixed frames, X25519 link keys."""

    def __init__(
        self,
        mesh: NodeMesh,
        node_id: str,
        *,
        host: str = "127.0.0.1",
        port: int | None = None,
        handler: Callable[[MeshFrame], None] | None = None,
    ) -> None:
        self.mesh = mesh
        self.node_id = node_id
        self.peer = mesh.peer(node_id)
        self.host = host
        self.port = int(port if port is not None else self.peer.listen_port)
        self.handler = handler
        self._sock: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._clients: list[socket.socket] = []

    def start(self) -> tuple[str, int]:
        if self.host not in ("127.0.0.1", "localhost", "::1"):
            # Default refuse non-loopback. Operator must pass host explicitly
            # and we still require an explicit listen; this start() path is
            # the local mesh node.
            self.host = "127.0.0.1"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(16)
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
        for c in list(self._clients):
            try:
                c.close()
            except OSError:
                pass
        self._clients.clear()
        if self._thread is not None:
            self._thread.join(timeout=2)
            self._thread = None

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
            threading.Thread(target=self._serve, args=(conn,), daemon=True).start()

    def _serve(self, conn: socket.socket) -> None:
        try:
            while not self._stop.is_set():
                header = _recv_exact(conn, 4)
                if not header:
                    return
                (length,) = struct.unpack("!I", header)
                if length == 0 or length > 1_000_000:
                    return
                blob = _recv_exact(conn, length)
                if not blob:
                    return
                frame = MeshFrame.decode(blob)
                if self.handler:
                    self.handler(frame)
        except OSError:
            return
        finally:
            try:
                conn.close()
            except OSError:
                pass

    def send_frame(self, host: str, port: int, frame: MeshFrame) -> None:
        blob = frame.encode()
        with socket.create_connection((host, port), timeout=5) as conn:
            conn.sendall(struct.pack("!I", len(blob)) + blob)


def _recv_exact(conn: socket.socket, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            return b""
        buf += chunk
    return buf


def seal_link(mesh: NodeMesh, src_id: str, dst_id: str, plaintext: bytes, *, seq: int = 0) -> bytes:
    """Encrypt a hop-to-hop payload with the pairwise X25519 link key."""
    src = mesh.peer(src_id)
    dst = mesh.peer(dst_id)
    key = _link_key(src.secret, dst.public_key)
    nonce = _link_nonce(src.index, dst.index, seq)
    return aead_encrypt(key, nonce, plaintext, aad=b"link|" + src_id.encode() + b"|" + dst_id.encode())


def open_link(mesh: NodeMesh, src_id: str, dst_id: str, blob: bytes, *, seq: int = 0) -> bytes:
    src = mesh.peer(src_id)
    dst = mesh.peer(dst_id)
    # Receiver uses its secret and the sender's public key.
    key = _link_key(dst.secret, src.public_key)
    nonce = _link_nonce(src.index, dst.index, seq)
    return aead_decrypt(key, nonce, blob, aad=b"link|" + src_id.encode() + b"|" + dst_id.encode())


def default_listen_port(index: int) -> int:
    if index < 0 or index >= POOL_SIZE:
        raise IndexError("node index")
    return 19000 + index + 1


def peer_endpoint(mesh: NodeMesh, node_id: str) -> tuple[str, int]:
    p = mesh.peer(node_id)
    return p.listen_host, p.listen_port
