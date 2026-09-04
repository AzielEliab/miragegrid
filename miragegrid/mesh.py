"""Persistent 25-node mesh: identities, adjacency, and peer routing.

The mesh is the network. Sessions are circuits *on* this mesh, not a
substitute for it. Topology is a circulant graph of degree 6
(offsets ±1, ±2, ±5). Paths are shortest-first, then SHA-256-stable
when two paths tie.

Author: Aziel Eliab
"""

from __future__ import annotations

import hashlib
from collections import deque
from dataclasses import dataclass, field
from typing import Iterable, Mapping

from miragegrid.crypto import fingerprint, node_identity_secret, x25519_keypair
from miragegrid.pool import POOL_SIZE, Node, NodePool, node_id_for
from miragegrid.rng import select_index

# Circulant generators. Diameter of C_25(1,2,5) is 3.
PEER_OFFSETS: tuple[int, ...] = (1, 2, 5, 20, 23, 24)

DEFAULT_MESH_SEED = b"miragegrid-mesh-v2-aziel-eliab-2026\x00\x00\x00\x00"


@dataclass(frozen=True)
class MeshPeer:
    """One persistent mesh member."""

    node: Node
    public_key: bytes
    secret: bytes = field(repr=False)
    listen_host: str = "127.0.0.1"
    listen_port: int = 0

    @property
    def id(self) -> str:
        return self.node.id

    @property
    def index(self) -> int:
        return self.node.index

    @property
    def fingerprint(self) -> str:
        return fingerprint(self.public_key)

    @property
    def endpoint(self) -> str:
        if self.node.endpoint:
            return self.node.endpoint
        if self.listen_port:
            return f"{self.listen_host}:{self.listen_port}"
        return f"{self.listen_host}:{19000 + self.node.number}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "label": self.node.label,
            "index": self.index,
            "number": self.node.number,
            "endpoint": self.endpoint,
            "fingerprint": self.fingerprint,
            "public_key": self.public_key.hex(),
        }


class NodeMesh:
    """The persistent 25-node mesh directory and routing table."""

    def __init__(
        self,
        pool: NodePool | None = None,
        *,
        seed: bytes = DEFAULT_MESH_SEED,
        endpoints: Mapping[str, str] | None = None,
    ) -> None:
        self.pool = pool if pool is not None else NodePool(endpoints=endpoints)
        self.seed = bytes(seed)
        peers: list[MeshPeer] = []
        for node in self.pool:
            secret, pub = x25519_keypair(node_identity_secret(self.seed, node.id))
            host, port = _split_endpoint(node.endpoint, node.number)
            peers.append(
                MeshPeer(
                    node=node,
                    public_key=pub,
                    secret=secret,
                    listen_host=host,
                    listen_port=port,
                )
            )
        self._peers: tuple[MeshPeer, ...] = tuple(peers)
        self._by_id: dict[str, MeshPeer] = {p.id: p for p in self._peers}
        self._adj: tuple[tuple[int, ...], ...] = tuple(
            _neighbors(i) for i in range(POOL_SIZE)
        )
        self._routes: tuple[tuple[int, ...], ...] = tuple(
            _shortest_path(self._adj, src) for src in range(POOL_SIZE)
        )

    def __len__(self) -> int:
        return POOL_SIZE

    def __iter__(self):
        return iter(self._peers)

    def peer(self, node_id: str) -> MeshPeer:
        return self._by_id[node_id]

    def peer_by_index(self, index: int) -> MeshPeer:
        return self._peers[index]

    @property
    def peers(self) -> tuple[MeshPeer, ...]:
        return self._peers

    def neighbors(self, index: int) -> tuple[int, ...]:
        return self._adj[index]

    def neighbor_ids(self, node_id: str) -> list[str]:
        idx = self.peer(node_id).index
        return [node_id_for(i) for i in self._adj[idx]]

    def next_hop(self, src: int, dst: int) -> int:
        if src == dst:
            return src
        hop = self._routes[src][dst]
        if hop < 0:
            raise RoutingError(f"no mesh path {src}->{dst}")
        return hop

    def path(self, src: int, dst: int) -> list[int]:
        """Node indices from src to dst inclusive."""
        if src == dst:
            return [src]
        hops: list[int] = [src]
        guard = 0
        cur = src
        while cur != dst:
            nxt = self.next_hop(cur, dst)
            if nxt == cur:
                raise RoutingError(f"routing loop at {cur}")
            hops.append(nxt)
            cur = nxt
            guard += 1
            if guard > POOL_SIZE + 2:
                raise RoutingError("path too long")
        return hops

    def path_ids(self, src_id: str, dst_id: str) -> list[str]:
        src = self.peer(src_id).index
        dst = self.peer(dst_id).index
        return [node_id_for(i) for i in self.path(src, dst)]

    def degree(self, index: int) -> int:
        return len(self._adj[index])

    def connected(self) -> bool:
        seen = {0}
        q = deque([0])
        while q:
            cur = q.popleft()
            for n in self._adj[cur]:
                if n not in seen:
                    seen.add(n)
                    q.append(n)
        return len(seen) == POOL_SIZE

    def to_dict(self) -> dict:
        return {
            "pool_size": POOL_SIZE,
            "topology": "circulant-25-1-2-5",
            "connected": self.connected(),
            "peers": [p.to_dict() for p in self._peers],
            "adjacency": {node_id_for(i): [node_id_for(n) for n in self._adj[i]] for i in range(POOL_SIZE)},
        }


class RoutingError(Exception):
    """No path in the mesh."""


def _neighbors(index: int) -> tuple[int, ...]:
    seen = []
    for off in PEER_OFFSETS:
        n = (index + off) % POOL_SIZE
        if n != index and n not in seen:
            seen.append(n)
    return tuple(sorted(seen))


def _shortest_path(adj: tuple[tuple[int, ...], ...], src: int) -> tuple[int, ...]:
    """next_hop[dst] for a BFS tree rooted at src. -1 if unreachable."""
    nxt = [-1] * POOL_SIZE
    nxt[src] = src
    q = deque([src])
    parent = [-1] * POOL_SIZE
    parent[src] = src
    while q:
        cur = q.popleft()
        for n in adj[cur]:
            if parent[n] == -1 and n != src:
                parent[n] = cur
                q.append(n)
    for dst in range(POOL_SIZE):
        if dst == src:
            nxt[dst] = src
            continue
        if parent[dst] == -1:
            nxt[dst] = -1
            continue
        walk = dst
        while parent[walk] != src:
            walk = parent[walk]
        nxt[dst] = walk
    return tuple(nxt)


def _split_endpoint(endpoint: str | None, number: int) -> tuple[str, int]:
    default_port = 19000 + number
    if not endpoint:
        return "127.0.0.1", default_port
    text = str(endpoint).strip()
    if ":" in text:
        host, _, port_s = text.rpartition(":")
        try:
            return (host or "127.0.0.1"), int(port_s)
        except ValueError:
            return "127.0.0.1", default_port
    return text, default_port


def select_circuit_indices(
    entropy: bytes,
    timestamp: str,
    hops: int = 3,
    *,
    pool_size: int = POOL_SIZE,
) -> list[int]:
    """Pick ``hops`` distinct node indices via SHA-256, no ``random.choice``.

    Hop 0 is the session entry (same function as ``select_index``).
    Later hops use ``entropy || timestamp || b'|hop|' || i``.
    """
    if hops < 1 or hops > pool_size:
        raise ValueError(f"hops must be 1..{pool_size}")
    chosen: list[int] = [select_index(entropy, timestamp)]
    used = set(chosen)
    salt = 0
    while len(chosen) < hops:
        digest = hashlib.sha256(
            bytes(entropy) + timestamp.encode("utf-8") + b"|hop|" + salt.to_bytes(4, "big")
        ).digest()
        idx = int.from_bytes(digest, "big") % pool_size
        if idx not in used:
            chosen.append(idx)
            used.add(idx)
        salt += 1
        if salt > 10_000:
            raise RuntimeError("unable to select distinct circuit hops")
    return chosen


def expand_circuit_path(mesh: NodeMesh, hop_indices: Iterable[int]) -> list[int]:
    """Expand onion hops into the full mesh walk (including intermediate peers)."""
    hops = list(hop_indices)
    if not hops:
        return []
    walk = [hops[0]]
    for a, b in zip(hops, hops[1:]):
        segment = mesh.path(a, b)
        walk.extend(segment[1:])
    return walk
