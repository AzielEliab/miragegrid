"""Persistent 25-node mesh: identities, adjacency, and peer routing.

The mesh is the network. Sessions are circuits *on* this mesh, not a
substitute for it. Topology is a circulant graph of degree 6
(offsets ±1, ±2, ±5). Paths are shortest-first, then SHA-256-stable
when two paths tie.

SPLIT THE WIRES (STW-1.0) is locked mesh law: the 0.5–1s tip tick is
presence + tip hash only (fixed-size; no body/diff/file). Payload is a
pull-only second plane (never sender fan-out). Update is proof, not a
timer (cite prev + lockset, fail-closed; 777s dwell after a valid cite;
clock desync is not yes; ambiguous tip isolates). Equivocation ends the
peer. Emit last locally after verify. Phoenix is local to the failed
node only. Partition does not auto-splice. The 1s tip socket and the
777s dwell socket never share.

COLD-COPY SURVIVAL (CCS-1.0) multiplies cold copies, refuses live body
sync, makes the tip expensive to erase, and keeps data after creators
are gone. A server pull cannot wipe cold replicas. Poison is
hash-absolute refuse.

REHEAL (RH-1.0) forbids neighbor talk-dirty-back-to-health. A node
heals from its own tip plus a trusted pull, or it phoenix-WAITs.
Allowed reheal fields are live / locked / isolated / tip-hash. Bodies,
diffs, and vote-to-fix are forbidden.

Assign stays live. Hosted mesh / vpn-hop / tunnel stubs remain refuse.
Author: Aziel Eliab only.
"""

from __future__ import annotations

import hashlib
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

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
            "assign_live": ASSIGN_LIVE,
            "split_wires": split_wires_dict(),
            "cold_copy": cold_copy_dict(),
            "reheal": reheal_dict(),
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


# ---------------------------------------------------------------------------
# Locked mesh law. Author: Aziel Eliab only.
# ---------------------------------------------------------------------------

MESH_LAW_AUTHOR = "Aziel Eliab"
SPLIT_WIRES_LAW = "SPLIT THE WIRES"
SPLIT_WIRES_SPEC = "STW-1.0"
COLD_COPY_LAW = "COLD-COPY SURVIVAL"
COLD_COPY_SPEC = "CCS-1.0"
REHEAL_LAW = "REHEAL"
REHEAL_SPEC = "RH-1.0"

ASSIGN_LIVE = True
HOSTED_STUB_OPS: frozenset[str] = frozenset(
    {"vpn", "hop", "tunnel", "vpn-hop", "mesh-hop"}
)

TIP_TICK_MIN_MS = 500
TIP_TICK_MAX_MS = 1000
DWELL_S = 777
TIP_TICK_SOCKET = "tip-1s"
DWELL_SOCKET = "dwell-777s"
TIP_HASH_LEN = 32
PRESENCE_LEN = 1
TIP_TICK_SIZE = PRESENCE_LEN + TIP_HASH_LEN
TIP_TICK_FIELDS: frozenset[str] = frozenset({"presence", "tip_hash"})
TIP_TICK_FORBIDDEN: frozenset[str] = frozenset(
    {"body", "diff", "file", "payload", "bytes"}
)

PRESENCE_LIVE = 1
PRESENCE_LOCKED = 2
PRESENCE_ISOLATED = 3
PRESENCE_NAMES: dict[int, str] = {
    PRESENCE_LIVE: "live",
    PRESENCE_LOCKED: "locked",
    PRESENCE_ISOLATED: "isolated",
}

YES = "yes"
NO = "no"
ISOLATE = "isolate"
LOCK = "lock"
REFUSE = "refuse"
WAIT = "phoenix-wait"
DWELL = "dwell"

PAYLOAD_PLANE = "pull-only"
MIN_COLD_COPIES = 2
REHEAL_ALLOWED: frozenset[str] = frozenset(
    {"live", "locked", "isolated", "tip_hash", "tip-hash"}
)
REHEAL_FORBIDDEN: frozenset[str] = frozenset(
    {
        "body",
        "bodies",
        "diff",
        "diffs",
        "file",
        "payload",
        "vote",
        "vote-to-fix",
        "vote_to_fix",
        "quorum_fix",
    }
)
REHEAL_SOURCES: frozenset[str] = frozenset(
    {"own-tip+trusted-pull", "phoenix-wait"}
)


class MeshLawError(Exception):
    """SPLIT THE WIRES / COLD-COPY / REHEAL refuse."""

    def __init__(self, code: str, message: str, *, verdict: str = REFUSE) -> None:
        super().__init__(message)
        self.code = code
        self.verdict = verdict

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": False,
            "code": self.code,
            "verdict": self.verdict,
            "yes": False,
            "message": str(self),
            "author": MESH_LAW_AUTHOR,
        }


def _hex32(value: bytes | str) -> str:
    if isinstance(value, bytes):
        if len(value) != TIP_HASH_LEN:
            raise MeshLawError("STW-TIP-HASH", "tip hash must be 32 bytes")
        return value.hex()
    text = str(value).strip().lower()
    if len(text) != 64 or any(c not in "0123456789abcdef" for c in text):
        raise MeshLawError("STW-TIP-HASH", "tip hash must be 64 hex")
    return text


def _hash_bytes(value: bytes | str) -> bytes:
    return bytes.fromhex(_hex32(value))


def _verdict(
    ok: bool,
    code: str,
    *,
    verdict: str,
    message: str,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "ok": ok,
        "code": code,
        "verdict": verdict,
        "yes": verdict == YES,
        "message": message,
        "author": MESH_LAW_AUTHOR,
    }
    if extra:
        out.update(dict(extra))
    return out


@dataclass(frozen=True)
class TipTick:
    """Fixed-size presence + tip hash. No body, diff, or file."""

    presence: int
    tip_hash: bytes

    def __post_init__(self) -> None:
        if self.presence not in PRESENCE_NAMES:
            raise MeshLawError("STW-PRESENCE", "presence must be live, locked, or isolated")
        if len(self.tip_hash) != TIP_HASH_LEN:
            raise MeshLawError("STW-TIP-HASH", "tip hash must be 32 bytes")

    def encode(self) -> bytes:
        return bytes([self.presence & 0xFF]) + self.tip_hash

    @classmethod
    def decode(cls, blob: bytes) -> "TipTick":
        if len(blob) != TIP_TICK_SIZE:
            raise MeshLawError(
                "STW-TIP-SIZE",
                f"tip tick is fixed {TIP_TICK_SIZE} bytes (presence+hash only)",
            )
        return cls(presence=blob[0], tip_hash=blob[1:])

    def to_dict(self) -> dict[str, Any]:
        return {
            "presence": PRESENCE_NAMES[self.presence],
            "presence_code": self.presence,
            "tip_hash": self.tip_hash.hex(),
            "bytes": TIP_TICK_SIZE,
        }


def encode_tip_tick(
    presence: int | str,
    tip_hash: bytes | str,
    extra: Mapping[str, Any] | None = None,
) -> bytes:
    """Encode a 0.5–1s tip tick. Refuses body/diff/file and extra fields."""
    extra = extra or {}
    forbidden = sorted(k for k in extra if str(k).lower() in TIP_TICK_FORBIDDEN)
    if forbidden:
        raise MeshLawError(
            "STW-TIP-BODY",
            "tip tick is presence+tip hash only (no body/diff/file)",
        )
    unknown = sorted(k for k in extra if str(k) not in TIP_TICK_FIELDS)
    if unknown:
        raise MeshLawError("STW-TIP-FIXED", "tip tick is fixed-size; no extra fields")
    if isinstance(presence, str):
        names = {v: k for k, v in PRESENCE_NAMES.items()}
        if presence not in names:
            raise MeshLawError("STW-PRESENCE", "presence must be live, locked, or isolated")
        presence = names[presence]
    return TipTick(presence=int(presence), tip_hash=_hash_bytes(tip_hash)).encode()


def decode_tip_tick(blob: bytes) -> TipTick:
    return TipTick.decode(blob)


def admit_payload(
    *,
    mode: str,
    tip_hash: bytes | str | None = None,
    fanout: bool = False,
    body: bytes | None = None,
) -> dict[str, Any]:
    """Payload is pull-only. Sender fan-out is refused."""
    if fanout or str(mode).lower() in {"fanout", "push", "broadcast-body", "sender-fanout"}:
        return _verdict(
            False,
            "STW-NO-FANOUT",
            verdict=REFUSE,
            message="payload plane is pull-only; sender fan-out is refused",
        )
    if str(mode).lower() != "pull":
        return _verdict(
            False,
            "STW-PULL-ONLY",
            verdict=REFUSE,
            message="payload plane is pull-only",
        )
    if not tip_hash:
        return _verdict(
            False,
            "STW-UPDATE-FAIL-CLOSED",
            verdict=REFUSE,
            message="payload pull fail-closed without a tip hash",
        )
    digest = _hex32(tip_hash)
    if body is not None and hashlib.sha256(body).hexdigest() != digest:
        return _verdict(
            False,
            "CCS-POISON-HASH",
            verdict=REFUSE,
            message="hash-absolute poison refuse",
            extra={"tip_hash": digest},
        )
    return _verdict(
        True,
        "STW-PULL-OK",
        verdict=YES,
        message="payload admitted on pull-only plane",
        extra={"tip_hash": digest, "plane": PAYLOAD_PLANE},
    )


def cite_update(
    *,
    prev: bytes | str | None,
    tip: bytes | str | None,
    lockset: Mapping[str, Any] | None,
    clock_desync: bool = False,
    ambiguous: bool = False,
    dwell_elapsed_s: float | None = None,
) -> dict[str, Any]:
    """Update is proof, not a timer. Cite prev + lockset; fail-closed."""
    if not prev or not tip or not lockset:
        return _verdict(
            False,
            "STW-UPDATE-FAIL-CLOSED",
            verdict=REFUSE,
            message="update fail-closed without cite prev+lockset",
        )
    prev_h = _hex32(prev)
    tip_h = _hex32(tip)
    if prev_h == tip_h:
        return _verdict(
            False,
            "STW-UPDATE-FAIL-CLOSED",
            verdict=REFUSE,
            message="update fail-closed: tip must cite a distinct prev",
        )
    if clock_desync:
        return _verdict(
            False,
            "STW-CLOCK-DESYNC",
            verdict=NO,
            message="clock desync is not yes",
            extra={"prev": prev_h, "tip": tip_h},
        )
    if ambiguous:
        return _verdict(
            False,
            "STW-AMBIGUOUS-TIP",
            verdict=ISOLATE,
            message="ambiguous tip isolates",
            extra={"prev": prev_h, "tip": tip_h},
        )
    if dwell_elapsed_s is not None and dwell_elapsed_s < DWELL_S:
        return _verdict(
            True,
            "STW-DWELL",
            verdict=DWELL,
            message="777s dwell after a valid cite",
            extra={"prev": prev_h, "tip": tip_h, "dwell_s": DWELL_S},
        )
    return _verdict(
        True,
        "STW-CITE-OK",
        verdict=YES,
        message="valid cite prev+lockset",
        extra={"prev": prev_h, "tip": tip_h, "dwell_s": DWELL_S},
    )


def equivocation_check(
    *,
    peer: str,
    prev: bytes | str,
    tips: Iterable[bytes | str],
    quorum_votes: int | None = None,
) -> dict[str, Any]:
    """Same prev with two tips ends the peer. Quorum is not truth."""
    prev_h = _hex32(prev)
    unique = { _hex32(t) for t in tips }
    if len(unique) >= 2:
        return _verdict(
            False,
            "STW-EQUIVOCATION",
            verdict=LOCK,
            message="same prev with two tips locks and isolates the peer",
            extra={
                "peer": peer,
                "prev": prev_h,
                "tips": sorted(unique),
                "isolate": True,
                "quorum_is_truth": False,
                "quorum_votes": quorum_votes,
            },
        )
    if quorum_votes is not None and not unique:
        return _verdict(
            False,
            "STW-QUORUM-NOT-TRUTH",
            verdict=REFUSE,
            message="quorum is not truth",
            extra={"peer": peer, "prev": prev_h},
        )
    return _verdict(
        True,
        "STW-EQUIVOCATION-CLEAR",
        verdict=YES,
        message="single tip for prev",
        extra={"peer": peer, "prev": prev_h, "quorum_is_truth": False},
    )


def emit_last(*, verified: bool, local: bool = True, unsend: bool = False) -> dict[str, Any]:
    """Emit last locally after verify. No unsend of an unverified body."""
    if unsend:
        return _verdict(
            False,
            "STW-NO-UNSEND",
            verdict=REFUSE,
            message="unsend of an unverified body is refused",
        )
    if not verified:
        return _verdict(
            False,
            "STW-UNVERIFIED-BODY",
            verdict=REFUSE,
            message="unverified body is not emitted",
        )
    if not local:
        return _verdict(
            False,
            "STW-EMIT-LOCAL",
            verdict=REFUSE,
            message="last is emitted locally after verify",
        )
    return _verdict(True, "STW-EMIT-OK", verdict=YES, message="emit last locally after verify")


def phoenix(*, failed_node: str, target: str | None = None, hunt: bool = False) -> dict[str, Any]:
    """Phoenix is local to the failed node only."""
    if hunt or (target and target != failed_node):
        return _verdict(
            False,
            "STW-PHOENIX-LOCAL",
            verdict=REFUSE,
            message="phoenix is local to the failed node only",
            extra={"failed_node": failed_node, "target": target},
        )
    return _verdict(
        True,
        "STW-PHOENIX-WAIT",
        verdict=WAIT,
        message="phoenix-WAIT local to the failed node",
        extra={"failed_node": failed_node, "phoenix": "local-wait"},
    )


def partition_rejoin(
    *,
    cite: bytes | str | None,
    operator: bool,
    lockset: Mapping[str, Any] | None,
    auto_splice: bool = False,
) -> dict[str, Any]:
    """Partition does not auto-splice. Rejoin is cite + operator/lockset."""
    if auto_splice:
        return _verdict(
            False,
            "STW-NO-AUTO-SPLICE",
            verdict=REFUSE,
            message="partition does not auto-splice",
        )
    if not cite or not lockset or not operator:
        return _verdict(
            False,
            "STW-REJOIN-FAIL-CLOSED",
            verdict=REFUSE,
            message="rejoin fail-closed without cite+operator/lockset",
        )
    return _verdict(
        True,
        "STW-REJOIN-OK",
        verdict=YES,
        message="rejoin cited with operator lockset",
        extra={"cite": _hex32(cite)},
    )


def heartbeat_loss(*, apply_last: bool = False, mark_poison: bool = False) -> dict[str, Any]:
    """Heartbeat loss is not poison and does not apply the last packet."""
    if mark_poison:
        return _verdict(
            False,
            "STW-HB-NOT-POISON",
            verdict=REFUSE,
            message="heartbeat loss is not poison",
        )
    if apply_last:
        return _verdict(
            False,
            "STW-HB-NOT-APPLY",
            verdict=REFUSE,
            message="heartbeat loss does not apply the last packet",
        )
    return _verdict(
        True,
        "STW-HB-LOSS",
        verdict=NO,
        message="heartbeat loss is not poison and does not apply last",
    )


def sockets_share(plane_a: str, plane_b: str) -> dict[str, Any]:
    """The 1s tip socket and the 777s dwell socket never share."""
    planes = {str(plane_a), str(plane_b)}
    tip_aliases = {TIP_TICK_SOCKET, "1s", "tip", "tip-tick"}
    dwell_aliases = {DWELL_SOCKET, "777s", "dwell", "update"}
    if planes & tip_aliases and planes & dwell_aliases:
        return _verdict(
            False,
            "STW-SOCKET-SPLIT",
            verdict=REFUSE,
            message="1s tip tick and 777s dwell never share a socket",
            extra={"tip_socket": TIP_TICK_SOCKET, "dwell_socket": DWELL_SOCKET},
        )
    return _verdict(
        True,
        "STW-SOCKET-OK",
        verdict=YES,
        message="planes stay on separate sockets",
    )


def multiply_cold_copies(copies: int) -> dict[str, Any]:
    """Cold copies multiply. One replica is not survival."""
    if int(copies) < MIN_COLD_COPIES:
        return _verdict(
            False,
            "CCS-MULTIPLY",
            verdict=REFUSE,
            message=f"cold copies must multiply (min {MIN_COLD_COPIES})",
            extra={"copies": int(copies), "min": MIN_COLD_COPIES},
        )
    return _verdict(
        True,
        "CCS-MULTIPLY-OK",
        verdict=YES,
        message="cold copies multiplied",
        extra={"copies": int(copies)},
    )


def refuse_live_body_sync(*, live_body_sync: bool) -> dict[str, Any]:
    if live_body_sync:
        return _verdict(
            False,
            "CCS-NO-LIVE-BODY-SYNC",
            verdict=REFUSE,
            message="live body sync is refused; payload is pull-only",
        )
    return _verdict(True, "CCS-NO-SYNC-OK", verdict=YES, message="no live body sync")


def erase_tip(*, expensive_proof: bool = False, lockset: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Tip is expensive to erase. Cheap erase is refused."""
    if not expensive_proof or not lockset:
        return _verdict(
            False,
            "CCS-TIP-EXPENSIVE",
            verdict=REFUSE,
            message="tip is expensive to erase; cheap erase is refused",
        )
    return _verdict(
        True,
        "CCS-TIP-ERASE-EXPENSIVE",
        verdict=YES,
        message="expensive tip erase cited; cold replicas are not wiped",
        extra={"wipes_cold": False},
    )


def server_pull_wipe_cold() -> dict[str, Any]:
    return _verdict(
        False,
        "CCS-SERVER-PULL-NO-WIPE",
        verdict=REFUSE,
        message="server pull cannot wipe cold replicas",
    )


def poison_refuse(*, claimed: bytes | str, actual: bytes | str) -> dict[str, Any]:
    """Hash-absolute poison refuse."""
    if _hex32(claimed) != _hex32(actual):
        return _verdict(
            False,
            "CCS-POISON-HASH",
            verdict=REFUSE,
            message="hash-absolute poison refuse",
            extra={"claimed": _hex32(claimed), "actual": _hex32(actual)},
        )
    return _verdict(True, "CCS-HASH-MATCH", verdict=YES, message="hash matches")


def data_outlives_creators(*, creator_gone: bool) -> dict[str, Any]:
    return _verdict(
        True,
        "CCS-OUTLIVES",
        verdict=YES,
        message="data outlives creators",
        extra={"creator_gone": bool(creator_gone), "kept": True},
    )


def reheal(
    *,
    source: str,
    own_tip: bytes | str | None = None,
    trusted_pull: bool = False,
    phoenix_wait: bool = False,
    neighbor_talk: bool = False,
    vote_to_fix: bool = False,
    fields: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """REHEAL: own tip + trusted pull, or phoenix-WAIT. No neighbor talk-back."""
    fields = fields or {}
    if neighbor_talk:
        return _verdict(
            False,
            "RH-NO-NEIGHBOR-TALK",
            verdict=REFUSE,
            message="neighbor talk-dirty-back-to-health is refused",
        )
    if vote_to_fix:
        return _verdict(
            False,
            "RH-NO-VOTE-TO-FIX",
            verdict=REFUSE,
            message="vote-to-fix is forbidden",
        )
    forbidden = sorted(
        k
        for k in fields
        if str(k).lower().replace(" ", "-") in REHEAL_FORBIDDEN
        or str(k).lower() in TIP_TICK_FORBIDDEN
    )
    if forbidden:
        return _verdict(
            False,
            "RH-NO-BODY",
            verdict=REFUSE,
            message="reheal forbids bodies, diffs, and vote-to-fix",
            extra={"forbidden": forbidden},
        )
    unknown = sorted(
        k
        for k in fields
        if str(k).lower().replace(" ", "-") not in REHEAL_ALLOWED
    )
    if unknown:
        return _verdict(
            False,
            "RH-FIELDS",
            verdict=REFUSE,
            message="reheal allows only live, locked, isolated, tip-hash",
            extra={"unknown": unknown},
        )
    src = str(source).strip().lower()
    if phoenix_wait or src in {"phoenix-wait", "phoenix_wait", WAIT}:
        return _verdict(
            True,
            "RH-PHOENIX-WAIT",
            verdict=WAIT,
            message="reheal phoenix-WAIT (not neighbor talk-back)",
            extra={"source": "phoenix-wait", "auto_heal": False},
        )
    if (src in {"own-tip+trusted-pull", "own_tip+trusted_pull", "trusted-pull"} or trusted_pull) and own_tip:
        return _verdict(
            True,
            "RH-OWN-TIP",
            verdict=YES,
            message="reheal from own tip plus trusted pull",
            extra={"source": "own-tip+trusted-pull", "own_tip": _hex32(own_tip), "auto_heal": False},
        )
    return _verdict(
        False,
        "RH-FAIL-CLOSED",
        verdict=REFUSE,
        message="reheal fail-closed without own tip+trusted pull or phoenix-WAIT",
    )


def hosted_stub_refuse(op: str) -> dict[str, Any] | None:
    """Hosted mesh / vpn-hop / tunnel stubs remain refuse. Assign stays live."""
    key = str(op).strip().lower().lstrip("/")
    for prefix in ("v1/mesh/", "mesh/", "v1/"):
        if key.startswith(prefix):
            key = key[len(prefix) :]
    if key == "assign":
        return None
    if key in HOSTED_STUB_OPS:
        return _verdict(
            False,
            "MESH-STUB",
            verdict=REFUSE,
            message=f"hosted {key} remains refuse; assign stays live",
            extra={"op": key, "assign_live": ASSIGN_LIVE},
        )
    return None


def split_wires_dict() -> dict[str, Any]:
    return {
        "law": SPLIT_WIRES_LAW,
        "spec": SPLIT_WIRES_SPEC,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "tip_tick": {
            "min_ms": TIP_TICK_MIN_MS,
            "max_ms": TIP_TICK_MAX_MS,
            "size": TIP_TICK_SIZE,
            "fields": sorted(TIP_TICK_FIELDS),
            "forbid": sorted(TIP_TICK_FORBIDDEN),
        },
        "payload": {"plane": PAYLOAD_PLANE, "sender_fanout": False},
        "update": {
            "kind": "proof",
            "timer": False,
            "cite": ["prev", "lockset"],
            "fail_closed": True,
            "dwell_s": DWELL_S,
            "clock_desync_is_yes": False,
            "ambiguous_tip": ISOLATE,
        },
        "equivocation": {
            "same_prev_two_tips": "lock-isolate",
            "quorum_is_truth": False,
        },
        "emit": {
            "last": "local-after-verify",
            "phoenix": "failed-node-only",
            "unsend_unverified_body": False,
        },
        "partition": {
            "auto_splice": False,
            "rejoin": ["cite", "operator", "lockset"],
            "heartbeat_loss_is_poison": False,
            "heartbeat_loss_applies_last": False,
        },
        "sockets": {
            "tip": TIP_TICK_SOCKET,
            "dwell": DWELL_SOCKET,
            "shared": False,
        },
        "assign_live": ASSIGN_LIVE,
        "hosted_stubs": sorted(HOSTED_STUB_OPS),
    }


def cold_copy_dict() -> dict[str, Any]:
    return {
        "law": COLD_COPY_LAW,
        "spec": COLD_COPY_SPEC,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "multiply": True,
        "min_copies": MIN_COLD_COPIES,
        "live_body_sync": False,
        "tip_erase": "expensive",
        "server_pull_wipes_cold": False,
        "poison": "hash-absolute-refuse",
        "data_outlives_creators": True,
    }


def reheal_dict() -> dict[str, Any]:
    return {
        "law": REHEAL_LAW,
        "spec": REHEAL_SPEC,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "neighbor_talk_dirty_back_to_health": False,
        "sources": sorted(REHEAL_SOURCES),
        "allowed": ["live", "locked", "isolated", "tip-hash"],
        "forbid": ["bodies", "diffs", "vote-to-fix"],
        "auto_heal": False,
        "phoenix": "wait",
    }


def mesh_law_dict() -> dict[str, Any]:
    return {
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "assign_live": ASSIGN_LIVE,
        "split_wires": split_wires_dict(),
        "cold_copy": cold_copy_dict(),
        "reheal": reheal_dict(),
    }
