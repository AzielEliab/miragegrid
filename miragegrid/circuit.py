"""Onion circuits over the persistent mesh.

A session is a multi-hop circuit, not a single label. Default length is
three hops (entry / middle / exit). Each hop holds only the next-hop
key. End-to-end payload is wrapped entry→exit so intermediates see
ciphertext.

Author: Aziel Eliab
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from typing import Any

from miragegrid.crypto import aead_decrypt, aead_encrypt, hkdf_sha256
from miragegrid.mesh import NodeMesh, expand_circuit_path, select_circuit_indices
from miragegrid.pool import node_id_for

DEFAULT_HOPS = 3
CIRCUIT_ID_LEN = 16


def _hop_key(secret: bytes, circuit_id: bytes, hop_index: int, node_id: str) -> bytes:
    info = b"hop|" + hop_index.to_bytes(2, "big") + b"|" + node_id.encode("ascii")
    return hkdf_sha256(secret, salt=circuit_id, info=info, length=32)


def _nonce(circuit_id: bytes, hop_index: int, counter: int) -> bytes:
    raw = circuit_id + hop_index.to_bytes(2, "big") + counter.to_bytes(4, "big")
    return hkdf_sha256(raw, salt=b"mirage-nonce", info=b"n", length=12)


@dataclass
class CircuitHop:
    index: int
    node_id: str
    role: str
    key: bytes = field(repr=False)

    def to_dict(self) -> dict[str, Any]:
        return {"index": self.index, "node_id": self.node_id, "role": self.role}


@dataclass
class Circuit:
    """One anonymity circuit on the 25-node mesh."""

    circuit_id: bytes
    hops: tuple[CircuitHop, ...]
    path: tuple[int, ...]
    secret: bytes = field(repr=False)
    _closed: bool = False
    _counter: int = 0
    _pending_counter: int = 0

    @classmethod
    def build(
        cls,
        mesh: NodeMesh,
        *,
        entropy: bytes,
        timestamp: str,
        hops: int = DEFAULT_HOPS,
        circuit_id: bytes | None = None,
        secret: bytes | None = None,
    ) -> "Circuit":
        indices = select_circuit_indices(entropy, timestamp, hops=hops)
        cid = circuit_id if circuit_id is not None else secrets.token_bytes(CIRCUIT_ID_LEN)
        sec = secret if secret is not None else hkdf_sha256(
            entropy, salt=timestamp.encode("utf-8"), info=b"circuit-secret|" + cid, length=32
        )
        roles = _roles(len(indices))
        hop_objs = []
        for i, idx in enumerate(indices):
            nid = node_id_for(idx)
            hop_objs.append(
                CircuitHop(
                    index=idx,
                    node_id=nid,
                    role=roles[i],
                    key=_hop_key(sec, cid, i, nid),
                )
            )
        path = tuple(expand_circuit_path(mesh, indices))
        return cls(circuit_id=cid, hops=tuple(hop_objs), path=path, secret=sec)

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def entry(self) -> CircuitHop:
        self._require_open()
        return self.hops[0]

    @property
    def exit(self) -> CircuitHop:
        self._require_open()
        return self.hops[-1]

    @property
    def hop_ids(self) -> list[str]:
        return [h.node_id for h in self.hops]

    @property
    def path_ids(self) -> list[str]:
        return [node_id_for(i) for i in self.path]

    def wrap(self, plaintext: bytes, *, aad: bytes = b"") -> bytes:
        """Onion-encrypt for the full hop list (exit layer innermost)."""
        self._require_open()
        blob = plaintext
        counter = self._counter
        self._counter += 1
        for i in range(len(self.hops) - 1, -1, -1):
            hop = self.hops[i]
            nonce = _nonce(self.circuit_id, i, counter)
            layer_aad = aad + bytes([i]) + self.circuit_id
            blob = aead_encrypt(hop.key, nonce, blob, layer_aad)
        return counter.to_bytes(4, "big") + blob

    def unwrap_hop(self, blob: bytes, hop_index: int, *, aad: bytes = b"") -> bytes:
        """Peel one onion layer at ``hop_index``. First call includes the counter prefix."""
        self._require_open()
        if hop_index == 0:
            if len(blob) < 4:
                raise ValueError("circuit cell too short")
            counter = int.from_bytes(blob[:4], "big")
            body = blob[4:]
        else:
            counter, body = self._pending_counter, blob
        hop = self.hops[hop_index]
        nonce = _nonce(self.circuit_id, hop_index, counter)
        layer_aad = aad + bytes([hop_index]) + self.circuit_id
        plain = aead_decrypt(hop.key, nonce, body, layer_aad)
        self._pending_counter = counter
        return plain

    def unwrap(self, blob: bytes, *, aad: bytes = b"") -> bytes:
        """Peel every layer (operator / test helper)."""
        self._require_open()
        body = blob
        for i in range(len(self.hops)):
            body = self.unwrap_hop(body, i, aad=aad)
        return body

    def close(self) -> None:
        self._closed = True
        self.secret = b""
        self.hops = tuple(
            CircuitHop(index=h.index, node_id=h.node_id, role=h.role, key=b"")
            for h in self.hops
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "circuit_id": self.circuit_id.hex(),
            "hops": [h.to_dict() for h in self.hops],
            "path": self.path_ids,
            "closed": self._closed,
        }

    def _require_open(self) -> None:
        if self._closed:
            raise CircuitClosedError("circuit keys destroyed")


class CircuitClosedError(Exception):
    """Raised after circuit keys are dropped."""


def _roles(n: int) -> list[str]:
    if n == 1:
        return ["entry-exit"]
    if n == 2:
        return ["entry", "exit"]
    roles = ["entry"]
    roles.extend(["middle"] * (n - 2))
    roles.append("exit")
    return roles

