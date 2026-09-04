"""MirageSession lifecycle: initiate → assign mesh circuit → operate → end.

A session is a circuit on the persistent 25-node mesh (entry / middle /
exit by default), not a lone label. End destroys the in-process
session-to-circuit mapping and drops onion keys (forget, not a log wipe).
After close, ``session.node`` and ``session.circuit`` raise
MappingDestroyedError.

Author: Aziel Eliab
"""

from __future__ import annotations

import json
import secrets
from typing import Any

from miragegrid.circuit import Circuit, CircuitClosedError
from miragegrid.errors import MappingDestroyedError
from miragegrid.mesh import NodeMesh
from miragegrid.pool import Node, NodePool
from miragegrid.receipt import Receipt, evaluate_integrity, utc_now
from miragegrid.rng import fresh_entropy, select_index


class MirageSession:
    """One phone-booth session: a mesh circuit whose entry is the outward node."""

    def __init__(
        self,
        pool: NodePool | None = None,
        *,
        mesh: NodeMesh | None = None,
        entropy: bytes | None = None,
        timestamp: str | None = None,
        session_id: str | None = None,
        hops: int = 3,
        assign: bool = True,
    ) -> None:
        if mesh is not None:
            self.mesh = mesh
            self.pool = mesh.pool
        else:
            self.pool = pool if pool is not None else NodePool()
            self.mesh = NodeMesh(self.pool)
        self.session_id = session_id if session_id is not None else secrets.token_hex(16)
        self._hops = hops
        self._closed = False
        self._node: Node | None = None
        self._circuit: Circuit | None = None
        self._receipt: Receipt | None = None
        self._timestamp: str | None = timestamp
        self._entropy: bytes | None = entropy
        if assign:
            self.initiate(entropy=entropy, timestamp=timestamp)

    def initiate(
        self,
        entropy: bytes | None = None,
        timestamp: str | None = None,
    ) -> Node:
        """Assign an entry node and build the onion circuit. Idempotent while open."""
        if self._closed:
            raise MappingDestroyedError(
                "session mapping destroyed; start a new MirageSession"
            )
        if self._node is not None:
            return self._node
        ts = timestamp if timestamp is not None else self._timestamp
        if ts is None:
            ts = utc_now()
        self._timestamp = ts
        ent = entropy if entropy is not None else self._entropy
        if ent is None:
            ent = fresh_entropy()
        self._entropy = ent
        index = select_index(ent, ts)
        node = self.pool.by_index(index)
        self._node = node
        self._circuit = Circuit.build(
            self.mesh,
            entropy=ent,
            timestamp=ts,
            hops=self._hops,
        )
        self._receipt = Receipt.mint(
            session_id=self.session_id,
            node=node,
            timestamp=ts,
            pool=self.pool,
            closed=False,
        )
        return node

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def node(self) -> Node:
        if self._closed:
            raise MappingDestroyedError(
                "session mapping destroyed; start a new MirageSession"
            )
        if self._node is None:
            raise MappingDestroyedError("no node assigned")
        return self._node

    @property
    def circuit(self) -> Circuit:
        if self._closed or self._circuit is None or self._circuit.closed:
            raise MappingDestroyedError(
                "session mapping destroyed; start a new MirageSession"
            )
        return self._circuit

    @property
    def receipt(self) -> Receipt:
        """Internal receipt. Not included in default dump / str / JSON."""
        if self._receipt is None:
            raise MappingDestroyedError("no receipt; session was never initiated")
        return self._receipt

    @property
    def integrity(self) -> str:
        """Live integrity: PASS iff a pool node is mapped, circuit open, not closed."""
        node_id = None if self._node is None else self._node.id
        base = evaluate_integrity(node_id, self.pool, self._closed)
        if base == "FAIL":
            return "FAIL"
        if self._circuit is None or self._circuit.closed:
            return "FAIL"
        if self._circuit.entry.node_id != node_id:
            return "FAIL"
        return "PASS"

    def wrap(self, plaintext: bytes) -> bytes:
        return self.circuit.wrap(plaintext)

    def unwrap(self, blob: bytes) -> bytes:
        return self.circuit.unwrap(blob)

    def emit_receipt(self) -> dict[str, Any]:
        """Operator-requested receipt dict (for ``--emit-receipt`` / UI)."""
        return self.receipt.to_dict()

    def to_dict(self, *, include_receipt: bool = False, include_circuit: bool = True) -> dict[str, Any]:
        """Public session dump. Receipt omitted unless ``include_receipt``."""
        payload: dict[str, Any] = {
            "session_id": self.session_id,
            "closed": self._closed,
            "kind": "mesh-vpn-circuit",
        }
        if self._closed:
            payload["node_id"] = None
            payload["circuit"] = None
        elif self._node is not None:
            payload["node_id"] = self._node.id
            payload["node_label"] = self._node.label
            if include_circuit and self._circuit is not None and not self._circuit.closed:
                payload["circuit"] = {
                    "circuit_id": self._circuit.circuit_id.hex(),
                    "hops": self._circuit.hop_ids,
                    "path": self._circuit.path_ids,
                    "entry": self._circuit.entry.node_id,
                    "exit": self._circuit.exit.node_id,
                }
        if include_receipt and self._receipt is not None:
            payload["receipt"] = self._receipt.to_dict()
        return payload

    def to_json(self, *, include_receipt: bool = False) -> str:
        return json.dumps(self.to_dict(include_receipt=include_receipt), indent=2)

    def __str__(self) -> str:
        if self._closed:
            return f"MirageSession(session_id={self.session_id}, closed=True, node=None)"
        nid = None if self._node is None else self._node.id
        hops = ""
        if self._circuit is not None and not self._circuit.closed:
            hops = f", hops={self._circuit.hop_ids}"
        return f"MirageSession(session_id={self.session_id}, node={nid}{hops})"

    def __repr__(self) -> str:
        return str(self)

    def end(self) -> None:
        """Destroy the session-to-circuit mapping. In-process forget, not a wipe.

        The frozen receipt snapshot remains so an operator who already
        asked to emit it can still write the JSON they requested. Onion
        keys and the node mapping are dropped.
        """
        if self._circuit is not None:
            try:
                self._circuit.close()
            except CircuitClosedError:
                pass
        self._circuit = None
        self._node = None
        self._closed = True

    def close(self) -> None:
        self.end()

    def __enter__(self) -> "MirageSession":
        if self._node is None and not self._closed:
            self.initiate()
        return self

    def __exit__(self, *exc: object) -> bool:
        self.end()
        return False
