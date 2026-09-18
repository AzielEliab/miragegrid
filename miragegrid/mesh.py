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

REHEAL (RH-1.0 / REHEAL-1.0 / MESH-REHEAL) forbids neighbor
talk-dirty-back-to-health. A node heals from its own tip plus a trusted
pull, or it phoenix-WAITs. Allowed reheal fields are live / locked /
isolated / tip-hash. Bodies, diffs, and vote-to-fix are forbidden.
Public-stack auto-heal means this lawful reheal + archive re-expand.

AZ GENERATOR (AZ-GENERATOR-1.0) is a Cap-7 mesh DNS factory living
deep inside the node. It does not get called from outside. The 7m77s
(497s) claim tick exits outward through the FRONT Node Gate (claim /
plant / flag / restore). Cap-7 `.az` names per node. First claim
`www.survivalnetwork.az`. Restore / claim needs ≥49 local vault
papers (hash-absolute; cite don't merge). Mesh-authoritative zone +
claim receipts — not public ICANN. Every node MUST carry the full
paper set as a cold vault copy — vault multiply onto each node /
papers land as cold copies on bootstrap / join / Cap-7 claim /
grid-shift standby. No live body sync of paper bytes on the 1s tip
tick. Incomplete vault → AZG-UNVERIFIED-TIP / AZG-INCOMPLETE-VAULT;
phoenix-WAIT; do not invent.

MIRAGE GRID SHIFT (MIRAGE-GRID-SHIFT-1.0) restates MESH-VAULT as
snapshot plus official standby (IP-mask host). Grid shift keeps the
`.az` answerable and cloaks the node after a domain pull. Grid-shift
standby is a vault-multiply event.

AIRGAP (AIRGAP-1.0) is local vault + no bearer radios + no climb-back
onto pulled public hub hostnames. Downloads from the local cold shelf
stay allowed. Tip chatter is live / locked / isolated / tip-hash only.
Official hubs are not airgap Node Gate.

The 1s tip tick, 777s dwell, and 7m77s claim clock never share a socket.
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
            "az_generator": az_generator_dict(),
            "grid_shift": grid_shift_dict(),
            "airgap": airgap_dict(),
            "paper_vault": paper_vault_dict(),
            "public_stack": public_stack_dict(),
            "no_fan": no_fan_dict(),
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
REHEAL_1_0 = "REHEAL-1.0"
MESH_REHEAL_SPEC = "MESH-REHEAL"
AZ_GENERATOR_LAW = "AZ GENERATOR"
AZ_GENERATOR_SPEC = "AZ-GENERATOR-1.0"
GRID_SHIFT_LAW = "MIRAGE GRID SHIFT"
GRID_SHIFT_SPEC = "MIRAGE-GRID-SHIFT-1.0"
AIRGAP_LAW = "AIRGAP"
AIRGAP_SPEC = "AIRGAP-1.0"
PAPER_VAULT_LAW = "PAPER-VAULT-ON-NODE"
NO_LIE_LAW = "NO-LIE"
NO_REWRITE_LAW = "NO-REWRITE"
NO_FALSIFY_LAW = "NO-FALSIFY"
NO_AMBIGUITY_LAW = "NO-AMBIGUITY"
NO_MISLEAD_LAW = "NO-MISLEAD"
NO_FAN_LAW = "NO FALSIFICATION NO AMBIGUITY NO MISLEADING"
NO_FAN_SPEC = "NO-FAN-1.0"
NO_FAN_PHRASE = "No falsification. No ambiguity. No misleading."

ASSIGN_LIVE = True
RADIO_PHY = False
HOSTED_STUB_OPS: frozenset[str] = frozenset(
    {"vpn", "hop", "tunnel", "vpn-hop", "mesh-hop"}
)

TIP_TICK_MIN_MS = 500
TIP_TICK_MAX_MS = 1000
DWELL_S = 777
TIP_TICK_SOCKET = "tip-1s"
DWELL_SOCKET = "dwell-777s"
CLAIM_MINUTES = 7
CLAIM_EXTRA_S = 77
CLAIM_CLOCK_S = CLAIM_MINUTES * 60 + CLAIM_EXTRA_S  # 420 + 77 = 497
CLAIM_SOCKET = "claim-7m77s"
CAP_7 = 7
MIN_PAPERS = 49
FIRST_CLAIM_LABEL = "www.survivalnetwork"
FIRST_CLAIM_NAME = "www.survivalnetwork.az"
AZ_TLD = ".az"
AZIEL_TLD = ".aziel"
CLAIM_SUFFIX_ORDER: tuple[str, ...] = (AZ_TLD, AZIEL_TLD)
ICANN_PUBLIC_TLDS: frozenset[str] = frozenset(
    {".com", ".net", ".org", ".uk", ".io", ".dev", ".app", ".info", ".co"}
)
MESH_VAULT_KIND = "snapshot+official-standby"
MESH_VAULT_ROLE = "ip-mask-host"
TIP_HASH_LEN = 32
PRESENCE_LEN = 1
TIP_TICK_SIZE = PRESENCE_LEN + TIP_HASH_LEN
TIP_TICK_FIELDS: frozenset[str] = frozenset({"presence", "tip_hash"})
TIP_TICK_FORBIDDEN: frozenset[str] = frozenset(
    {"body", "diff", "file", "payload", "bytes", "papers", "paper", "vault"}
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

OFFICIAL_HUBS: frozenset[str] = frozenset(
    {
        "azieleliab.com",
        "www.azieleliab.com",
        "godlock.uk",
        "www.godlock.uk",
        "azielcorpuslibrary.net",
        "www.azielcorpuslibrary.net",
        "hedidntjump.com",
        "www.hedidntjump.com",
    }
)
HUB_NOT_NODE_GATE: frozenset[str] = frozenset(
    {"azieleliab.com", "godlock.uk", "corpus", "azielcorpuslibrary.net", "hedidntjump.com"}
)

NO_FAN_FALSIFY_VERBS: frozenset[str] = frozenset(
    {
        "falsify",
        "falsified",
        "falsification",
        "fake",
        "fake-flag",
        "fake_flag",
        "invent",
        "invent-continuity",
        "fabricate",
        "false-tip",
        "false_tip",
        "false-receipt",
        "false-claim",
        "false-live-nodes",
        "false-site-up",
        "site-up-lie",
        "false-paper-set",
        "false_paper_set",
        "we-have-49",
        "have-49-without-bytes",
        "have_49_without_bytes",
    }
)

VAULT_MULTIPLY_EVENTS: frozenset[str] = frozenset(
    {
        "bootstrap",
        "join",
        "cap-7-claim",
        "cap7-claim",
        "cap_7_claim",
        "grid-shift-standby",
        "grid_shift_standby",
    }
)
AIRGAP_TIP_FIELDS: frozenset[str] = frozenset(
    {"live", "locked", "isolated", "tip-hash", "tip_hash"}
)
NO_FAN_AMBIGUITY_VERBS: frozenset[str] = frozenset(
    {
        "ambiguous",
        "ambiguity",
        "dual-tip",
        "dual_tip",
        "soft-maybe",
        "soft_maybe",
        "maybe",
        "pretty-copy",
        "pretty_copy",
        "majority-paper-over",
        "majority_paper_over",
    }
)
NO_FAN_MISLEAD_VERBS: frozenset[str] = frozenset(
    {
        "misleading",
        "mislead",
        "pretend",
        "pretend-hub-cell",
        "pretend_hub_cell",
        "hub-still-cell",
        "unmarked-hydra",
        "neighbor-resurrection",
        "neighbor_resurrection",
    }
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
    """1s tip, 777s dwell, and 7m77s claim clocks never share a socket."""
    planes = {str(plane_a), str(plane_b)}
    families = (
        {TIP_TICK_SOCKET, "1s", "tip", "tip-tick"},
        {DWELL_SOCKET, "777s", "dwell", "update"},
        {CLAIM_SOCKET, "7m77s", "497s", "claim", "az-generator"},
    )
    hits = sum(1 for fam in families if planes & fam)
    if hits >= 2:
        return _verdict(
            False,
            "STW-SOCKET-SPLIT",
            verdict=REFUSE,
            message="1s tip tick, 777s dwell, and 7m77s claim clock never share a socket",
            extra={
                "tip_socket": TIP_TICK_SOCKET,
                "dwell_socket": DWELL_SOCKET,
                "claim_socket": CLAIM_SOCKET,
                "period_s": CLAIM_CLOCK_S,
            },
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


def refuse_radio_phy(*, kind: str | None = None) -> dict[str, Any]:
    """MirageGrid is not a qnm radio mesh. Invented PHY is NO-FAN refuse."""
    return _verdict(
        False,
        "AZG-NO-RADIO-PHY",
        verdict=REFUSE,
        message="MirageGrid is not RF/BT/Wi-Fi/photon radio PHY; local qnm radios are not this product",
        extra={
            "radio_phy": False,
            "kind": kind or "radio",
            "hub_get_enables_mesh": False,
            "bitmesh": False,
            "invented_phy": False,
        },
    )


GET_ENABLE_PLANT_INTENTS: frozenset[str] = frozenset(
    {
        "enable",
        "enabled",
        "radio",
        "radios",
        "bearer-radio",
        "bearer-radios",
        "mesh-enable",
        "claim",
        "plant",
        "claim-plant",
        "run-generator",
        "call-generator",
        "fielded",
        "fielded-100",
        "radio-on",
    }
)
PUBLIC_MESH_GET_DOORS: tuple[str, ...] = (
    "/v1/mesh",
    "/v1/mesh/status",
    "/v1/mesh/nodes",
    "/v1/mesh/az-generator",
    "/v1/mesh/grid-shift",
)
GET_MUTATION_PATHS: frozenset[str] = frozenset(
    {
        "/v1/mesh/enable",
        "/v1/mesh/join",
        "/v1/mesh/heartbeat",
        "/v1/mesh/leave",
        "/v1/mesh/broadcast",
        "/v1/mesh/plant",
        "/v1/mesh/claim",
        "/v1/mesh/radio",
        "/v1/mesh/radios",
        "/v1/mesh/call-generator",
        "/v1/mesh/run-generator",
        "/v1/shuffle/update",
    }
)


def _query_has_enable_or_plant(search: str | None) -> bool:
    raw = str(search or "")
    if raw.startswith("?"):
        raw = raw[1:]
    if not raw:
        return False
    from urllib.parse import parse_qsl

    pairs = dict(parse_qsl(raw, keep_blank_values=True))
    if str(pairs.get("prev") or "").strip() and str(pairs.get("lockset") or "").strip():
        return True
    for key, val in pairs.items():
        k = _norm_verb(key)
        v = _norm_verb(val)
        if k in GET_ENABLE_PLANT_INTENTS or v in GET_ENABLE_PLANT_INTENTS:
            return True
        if v in {"1", "true", "on", "yes"} and any(p in k for p in ("enable", "radio", "plant", "claim")):
            return True
    return False


def refuse_get_enable_or_plant(
    *,
    method: str,
    path: str,
    search: str | None = None,
) -> dict[str, Any] | None:
    """GET/HEAD never enables radios or plants Cap-7 claims."""
    if str(method or "GET").upper() not in {"GET", "HEAD"}:
        return None
    path_only = str(path or "").split("?")[0].rstrip("/") or "/"
    if not path_only.startswith("/"):
        path_only = "/" + path_only
    shuffle_update = path_only.endswith("/update") and ("/shuffle" in path_only or "/cap7/" in path_only)
    intent = (
        _query_has_enable_or_plant(search)
        or path_only in GET_MUTATION_PATHS
        or path_only.endswith("/enable")
        or shuffle_update
    )
    if not intent:
        return None
    return _verdict(
        False,
        "MESH-GET-NO-ENABLE",
        verdict=REFUSE,
        message="GET never enables radios or plants mesh claims",
        extra={
            "enabled": False,
            "default_off": True,
            "radio_phy": False,
            "claim_plant": False,
            "hub_get_enables_mesh": False,
            "path": path_only,
        },
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


def claim_clock_period_s() -> int:
    """7 minutes + 77 seconds = 420 + 77 = 497."""
    return CLAIM_CLOCK_S


def _norm_verb(value: Any) -> str:
    return str(value or "").strip().lower().replace(" ", "-").replace("_", "-")


def refuse_no_fan(
    verb: str | None = None,
    *,
    falsify: bool = False,
    ambiguous: bool = False,
    misleading: bool = False,
    kind: str | None = None,
) -> dict[str, Any] | None:
    """NO-FAN-1.0: No falsification. No ambiguity. No misleading."""
    key = _norm_verb(verb)
    if falsify or key in NO_FAN_FALSIFY_VERBS:
        return _verdict(
            False,
            "NO-FAN-FALSIFY",
            verdict=REFUSE,
            message="no falsified tip, receipt, domain claim, Live Nodes count, or site-up claim",
            extra={
                "law": NO_FAN_LAW,
                "spec": NO_FAN_SPEC,
                "phrase": NO_FAN_PHRASE,
                "kind": kind or key or "falsify",
                "no_lie": True,
                "no_rewrite": True,
            },
        )
    if ambiguous or key in NO_FAN_AMBIGUITY_VERBS:
        return _verdict(
            False,
            "NO-FAN-AMBIGUITY",
            verdict=ISOLATE,
            message="ambiguous tip isolates; do not paper over with majority or pretty copy",
            extra={
                "law": NO_FAN_LAW,
                "spec": NO_FAN_SPEC,
                "phrase": NO_FAN_PHRASE,
                "kind": kind or key or "ambiguous",
                "quorum_is_truth": False,
            },
        )
    if misleading or key in NO_FAN_MISLEAD_VERBS:
        return _verdict(
            False,
            "NO-FAN-MISLEAD",
            verdict=REFUSE,
            message="no misleading chrome: pulled hub is not still the cell; auto-heal is not neighbor resurrection",
            extra={
                "law": NO_FAN_LAW,
                "spec": NO_FAN_SPEC,
                "phrase": NO_FAN_PHRASE,
                "kind": kind or key or "misleading",
            },
        )
    return None


def refuse_falsify(*, kind: str) -> dict[str, Any]:
    out = refuse_no_fan("falsify", falsify=True, kind=kind)
    assert out is not None
    return out


def refuse_ambiguity(*, kind: str = "ambiguous-tip") -> dict[str, Any]:
    out = refuse_no_fan("ambiguous", ambiguous=True, kind=kind)
    assert out is not None
    return out


def refuse_misleading(*, kind: str) -> dict[str, Any]:
    out = refuse_no_fan("misleading", misleading=True, kind=kind)
    assert out is not None
    return out


def _site_text(site: Any) -> str:
    if isinstance(site, Mapping):
        parts = [
            site.get("name"),
            site.get("host"),
            site.get("domain"),
            site.get("url"),
            site.get("site"),
        ]
        return " ".join(str(p) for p in parts if p)
    return str(site or "")


def normalize_claim_suffix(value: str | None) -> str:
    text = str(value or "").strip().lower()
    if not text:
        return ""
    if not text.startswith("."):
        text = "." + text
    return text


def first_claim_for_suffix(suffix: str | None = None) -> str:
    """First-flag name follows the ACTIVE honest suffix. Do not fake a dead suffix."""
    s = normalize_claim_suffix(suffix) or AZ_TLD
    return FIRST_CLAIM_LABEL + s


def select_claim_suffix(
    *,
    az_usable: bool = True,
    aziel_usable: bool = True,
    pivot_suffix: str | None = None,
) -> dict[str, Any]:
    """Honest suffix order: .az → .aziel → mesh-authoritative pivot. Never fake ICANN."""
    if az_usable:
        return _verdict(
            True,
            "AZG-SUFFIX-AZ",
            verdict=YES,
            message="active claim suffix is .az",
            extra={
                "suffix": AZ_TLD,
                "first_claim": first_claim_for_suffix(AZ_TLD),
                "order": list(CLAIM_SUFFIX_ORDER),
                "public_icann": False,
                "pretended_az": True,
                "pretended_aziel": False,
            },
        )
    if aziel_usable:
        return _verdict(
            True,
            "AZG-SUFFIX-AZIEL",
            verdict=YES,
            message=".az cannot be honestly claimed; active suffix is .aziel",
            extra={
                "suffix": AZIEL_TLD,
                "first_claim": first_claim_for_suffix(AZIEL_TLD),
                "order": list(CLAIM_SUFFIX_ORDER),
                "public_icann": False,
                "pretended_az": False,
                "dead_suffix": AZ_TLD,
            },
        )
    pivot = normalize_claim_suffix(pivot_suffix)
    if pivot and pivot not in ICANN_PUBLIC_TLDS and pivot not in {AZ_TLD, AZIEL_TLD, "."}:
        return _verdict(
            True,
            "AZG-SUFFIX-PIVOT",
            verdict=YES,
            message=".az and .aziel cannot be honestly claimed; pivoted to mesh-authoritative suffix",
            extra={
                "suffix": pivot,
                "first_claim": first_claim_for_suffix(pivot),
                "order": list(CLAIM_SUFFIX_ORDER) + ["pivot"],
                "public_icann": False,
                "registrar": False,
                "pretended_az": False,
                "pretended_aziel": False,
                "dead_suffixes": [AZ_TLD, AZIEL_TLD],
            },
        )
    return _verdict(
        False,
        "AZG-SUFFIX-NONE",
        verdict=REFUSE,
        message="no honest claim suffix; do not invent ICANN success or fake the flag",
        extra={
            "order": list(CLAIM_SUFFIX_ORDER),
            "public_icann": False,
            "fake_flag": False,
        },
    )


def known_contains_first_claim(known_sites: Iterable[Any], suffix: str | None = None) -> bool:
    """True when any known site contains www.survivalnetwork.<active-suffix>."""
    needle = first_claim_for_suffix(suffix)
    for site in known_sites:
        if needle in _site_text(site).lower():
            return True
    return False


def _normalize_az_name(name: str | None) -> str:
    text = str(name or "").strip().lower()
    if text.startswith("https://"):
        text = text[len("https://") :]
    if text.startswith("http://"):
        text = text[len("http://") :]
    text = text.split("/")[0].split(":")[0].strip(".")
    return text


def _is_az_name(name: str) -> bool:
    host = _normalize_az_name(name)
    return bool(host) and host.endswith(AZ_TLD) and host != AZ_TLD.lstrip(".")


def _is_claim_name(name: str, *, suffix: str | None = None) -> bool:
    """Mesh claim name: .az, .aziel, or a declared honest pivot suffix. Not ICANN TLDs."""
    host = _normalize_az_name(name)
    if not host or "." not in host:
        return False
    if suffix:
        s = normalize_claim_suffix(suffix)
        return bool(s) and host.endswith(s) and host != s.lstrip(".")
    if host.endswith(AZ_TLD) and host != "az":
        return True
    if host.endswith(AZIEL_TLD) and host != "aziel":
        return True
    return False


def _is_official_hub(name: str) -> bool:
    host = _normalize_az_name(name)
    if host in OFFICIAL_HUBS:
        return True
    return any(host == h or host.endswith("." + h) for h in OFFICIAL_HUBS)


def _paper_ok(paper: Any) -> bool:
    """Hash-absolute Aziel Eliab paper. Cite don't merge. bytes↔hash."""
    if not isinstance(paper, Mapping):
        return False
    author = str(paper.get("author") or paper.get("identity") or "").strip()
    if author != MESH_LAW_AUTHOR:
        return False
    digest = paper.get("hash") or paper.get("sha256") or paper.get("tip_hash")
    body = paper.get("bytes") or paper.get("body") or paper.get("data")
    if digest is None:
        return False
    try:
        claimed = _hex32(digest)
    except MeshLawError:
        return False
    if body is not None:
        raw = body if isinstance(body, (bytes, bytearray)) else str(body).encode("utf-8")
        if hashlib.sha256(raw).hexdigest() != claimed:
            return False
    return True


def _paper_bytes(paper: Mapping[str, Any]) -> bytes | None:
    body = paper.get("bytes") or paper.get("body") or paper.get("data")
    if body is None:
        return None
    if isinstance(body, (bytes, bytearray)):
        return bytes(body)
    return str(body).encode("utf-8")


def _paper_vault_ok(paper: Any) -> bool:
    """Vault paper: hash-absolute AND bytes present. No 'we have 49' without bytes."""
    if not _paper_ok(paper):
        return False
    if not isinstance(paper, Mapping):
        return False
    raw = _paper_bytes(paper)
    if raw is None:
        return False
    digest = _hex32(paper.get("hash") or paper.get("sha256") or paper.get("tip_hash"))
    return hashlib.sha256(raw).hexdigest() == digest


def count_aziel_papers(papers: Iterable[Any] | None) -> int:
    seen: set[str] = set()
    count = 0
    for paper in papers or ():
        if not _paper_ok(paper):
            continue
        digest = _hex32(
            paper.get("hash") or paper.get("sha256") or paper.get("tip_hash")  # type: ignore[union-attr]
        )
        if digest in seen:
            continue
        seen.add(digest)
        count += 1
    return count


def count_vault_papers(papers: Iterable[Any] | None) -> int:
    """Unique hash-absolute papers that carry matching bytes."""
    seen: set[str] = set()
    count = 0
    for paper in papers or ():
        if not _paper_vault_ok(paper):
            continue
        digest = _hex32(
            paper.get("hash") or paper.get("sha256") or paper.get("tip_hash")  # type: ignore[union-attr]
        )
        if digest in seen:
            continue
        seen.add(digest)
        count += 1
    return count


def vault_complete(papers: Iterable[Any] | None) -> bool:
    """Full verified Aziel paper set (≥49 with bytes)."""
    return count_vault_papers(papers) >= MIN_PAPERS


def refuse_incomplete_vault(
    *,
    papers: Iterable[Any] | None = None,
    have_49: bool = False,
    claimed_count: int | None = None,
) -> dict[str, Any] | None:
    """Incomplete vault or 'we have 49' without bytes. phoenix-WAIT; do not invent."""
    n_vault = count_vault_papers(papers)
    n_cite = count_aziel_papers(papers)
    if have_49 or claimed_count == MIN_PAPERS:
        if n_vault < MIN_PAPERS:
            return refuse_falsify(kind="false-paper-set")
    if n_vault >= MIN_PAPERS:
        return None
    if n_cite < MIN_PAPERS:
        return None
    return _verdict(
        False,
        "AZG-INCOMPLETE-VAULT",
        verdict=WAIT,
        message="incomplete vault: no full verified paper set; AZG-UNVERIFIED-TIP; phoenix-WAIT / hold; do not invent",
        extra={
            "papers": n_vault,
            "cites": n_cite,
            "min_papers": MIN_PAPERS,
            "false_tip": False,
            "phoenix": "wait",
            "unverified_tip": True,
            "azg_unverified_tip": True,
            "code_alias": "AZG-UNVERIFIED-TIP",
            "have_49_without_bytes": n_cite >= MIN_PAPERS,
        },
    )


def restore_chain(
    *,
    papers: Iterable[Any] | None = None,
    broken: bool = True,
    most_active_point: str | None = None,
    have_49: bool = False,
) -> dict[str, Any]:
    """Restore at the most active guaranteed point. Incomplete vault → phoenix-WAIT."""
    fake = refuse_incomplete_vault(papers=papers, have_49=have_49)
    if fake and fake.get("code") == "NO-FAN-FALSIFY":
        return fake
    n = count_aziel_papers(papers)
    n_vault = count_vault_papers(papers)
    if n < MIN_PAPERS:
        return _verdict(
            False,
            "AZG-PAPERS",
            verdict=WAIT,
            message="fewer than 49 Aziel Eliab papers; do not claim a false tip; phoenix-WAIT / hold",
            extra={
                "papers": n,
                "min_papers": MIN_PAPERS,
                "false_tip": False,
                "phoenix": "wait",
                "incomplete_vault": True,
            },
        )
    if fake:
        return fake
    if n_vault < MIN_PAPERS:
        return _verdict(
            False,
            "AZG-INCOMPLETE-VAULT",
            verdict=WAIT,
            message="incomplete vault: AZG-UNVERIFIED-TIP; phoenix-WAIT / hold; do not invent",
            extra={
                "papers": n_vault,
                "min_papers": MIN_PAPERS,
                "false_tip": False,
                "phoenix": "wait",
                "unverified_tip": True,
                "azg_unverified_tip": True,
                "code_alias": "AZG-UNVERIFIED-TIP",
            },
        )
    if not broken:
        return _verdict(
            True,
            "AZG-RESTORE-INTACT",
            verdict=YES,
            message="chain intact; no restore claimed",
            extra={"papers": n_vault, "min_papers": MIN_PAPERS, "cite_dont_merge": True},
        )
    return _verdict(
        True,
        "AZG-RESTORE-OK",
        verdict=YES,
        message="restore at most active guaranteed point",
        extra={
            "papers": n_vault,
            "min_papers": MIN_PAPERS,
            "point": most_active_point or "most-active-guaranteed",
            "cite_dont_merge": True,
            "vault_complete": True,
        },
    )


def claim_az_domain(
    *,
    origin_node: str,
    known_sites: Iterable[Any] | None = None,
    claimed: int = 0,
    name: str | None = None,
    claimable: bool = True,
    papers: Iterable[Any] | None = None,
    vault: Iterable[Any] | None = None,
    tip_verified: bool = True,
    invent_continuity: bool = False,
    fake_flag: bool = False,
    have_49: bool = False,
    needs_papers: bool = False,
    public_registrar: bool = False,
    icann: bool = False,
    inbound_call: bool = False,
    az_usable: bool = True,
    aziel_usable: bool = True,
    pivot_suffix: str | None = None,
) -> dict[str, Any]:
    """7m77s claim. First claim follows the ACTIVE suffix. Cap-7. Origin hosts.

    Low-level law primitive. The executable factory tick lives deep in
    the node (``miragegrid.az_generator.AzGenerator``) and exits the
    FRONT Node Gate. This function does not publish ICANN DNS.
    """
    if inbound_call:
        return _verdict(
            False,
            "AZG-NOT-CALLABLE",
            verdict=REFUSE,
            message="AZ Generator lives deep in the node; it is not called from outside",
            extra={"callable": False, "lives": "deep-node", "exit": "node-gate-front"},
        )
    if public_registrar or icann:
        return _verdict(
            False,
            "AZG-NOT-PUBLIC-REGISTRAR",
            verdict=REFUSE,
            message="mesh DNS factory is not a public ICANN/Cloudflare registrar; do not fake registration success",
            extra={
                "public_icann": False,
                "registrar": False,
                "unbounded_public_dns": False,
                "dns_factory": "cap-7-mesh-authoritative",
            },
        )
    if invent_continuity or fake_flag:
        return refuse_falsify(kind="invent-continuity" if invent_continuity else "fake-flag")
    vault_papers = list(vault if vault is not None else (papers or ()))
    if papers is None and vault is not None:
        papers = vault
    if have_49 and count_vault_papers(vault_papers) < MIN_PAPERS:
        return refuse_falsify(kind="false-paper-set")
    if not tip_verified:
        return _verdict(
            False,
            "AZG-UNVERIFIED-TIP",
            verdict=WAIT,
            message="unverified tip: refuse claim rather than invent continuity; phoenix-WAIT / hold",
            extra={"false_tip": False, "phoenix": "wait", "no_lie": True, "phrase": NO_FAN_PHRASE},
        )
    if papers is not None and count_aziel_papers(papers) < MIN_PAPERS:
        return _verdict(
            False,
            "AZG-INCOMPLETE-VAULT",
            verdict=WAIT,
            message="incomplete local vault; refuse claim rather than invent continuity; phoenix-WAIT / hold",
            extra={
                "papers": count_aziel_papers(papers),
                "min_papers": MIN_PAPERS,
                "false_tip": False,
                "phoenix": "wait",
                "phrase": NO_FAN_PHRASE,
            },
        )
    chosen = select_claim_suffix(
        az_usable=az_usable, aziel_usable=aziel_usable, pivot_suffix=pivot_suffix
    )
    if not chosen.get("ok"):
        return chosen
    suffix = str(chosen["suffix"])
    first_name = first_claim_for_suffix(suffix)
    known = list(known_sites or ())
    if int(claimed) >= CAP_7:
        return _verdict(
            False,
            "AZG-CAP-7",
            verdict=REFUSE,
            message="Cap-7: at most 7 claim names per covered node",
            extra={"claimed": int(claimed), "cap": CAP_7, "origin_node": origin_node, "suffix": suffix},
        )
    first_needed = not known_contains_first_claim(known, suffix=suffix)
    target = _normalize_az_name(name) if name else ""
    if first_needed:
        target = first_name
        if not claimable:
            return _verdict(
                True,
                "AZG-FIRST-CLAIM-RESUME",
                verdict=YES,
                message=f"{first_name} cannot be claimed; resume 7m77s clock under Cap-7; do not fake the flag on a dead suffix",
                extra={
                    "first_claim": first_name,
                    "resume": True,
                    "fake_flag": False,
                    "period_s": CLAIM_CLOCK_S,
                    "origin_node": origin_node,
                    "hosted_by": origin_node,
                    "phrase": NO_FAN_PHRASE,
                    "suffix": suffix,
                    "dead_suffix": False,
                },
            )
        return _verdict(
            True,
            "AZG-FIRST-CLAIM",
            verdict=YES,
            message=f"first claim is {first_name}",
            extra={
                "name": first_name,
                "origin_node": origin_node,
                "hosted_by": origin_node,
                "period_s": CLAIM_CLOCK_S,
                "cap": CAP_7,
                "suffix": suffix,
            },
        )
    if not target:
        return _verdict(
            True,
            "AZG-CLOCK-TICK",
            verdict=YES,
            message="7m77s clock continues under Cap-7",
            extra={"period_s": CLAIM_CLOCK_S, "origin_node": origin_node, "cap": CAP_7},
        )
    if _is_official_hub(target):
        return _verdict(
            False,
            "AZG-NOT-HUB",
            verdict=REFUSE,
            message="official hubs are not Node Gate and are not claimed .az names",
            extra={"name": target, "origin_node": origin_node},
        )
    if not _is_claim_name(target, suffix=suffix):
        return _verdict(
            False,
            "AZG-TLD",
            verdict=REFUSE,
            message="AZ Generator claims the active honest suffix only (.az → .aziel → pivot); not ICANN TLDs",
            extra={"name": target, "origin_node": origin_node, "suffix": suffix},
        )
    if (papers is not None or vault is not None or needs_papers) and first_needed is False:
        if needs_papers or not vault_complete(vault_papers if vault_papers else papers):
            held = restore_chain(papers=papers if papers is not None else vault_papers, broken=True, have_49=have_49)
            if not held["ok"]:
                return held
    return _verdict(
        True,
        "AZG-CLAIM-OK",
        verdict=YES,
        message="domain claimed; site + server hosted by origin node (mesh-authoritative .az, not ICANN)",
        extra={
            "name": target,
            "origin_node": origin_node,
            "hosted_by": origin_node,
            "period_s": CLAIM_CLOCK_S,
            "cap": CAP_7,
            "public_icann": False,
            "registrar": False,
            "dns_factory": "cap-7-mesh-authoritative",
        },
    )


def vault_multiply(
    *,
    event: str,
    papers: Iterable[Any] | None = None,
    live_body_sync: bool = False,
    tip_tick: bool = False,
    fanout: bool = False,
    sender_fanout: bool = False,
) -> dict[str, Any]:
    """Vault multiply onto each node. Papers land as cold copies. Pull-only."""
    if live_body_sync or fanout or sender_fanout:
        return _verdict(
            False,
            "STW-NO-FANOUT",
            verdict=REFUSE,
            message="no live body sync / sender fan-out of paper bytes; payload plane is pull-only",
            extra={"live_body_sync": False, "plane": PAYLOAD_PLANE},
        )
    if tip_tick:
        return _verdict(
            False,
            "STW-TIP-BODY",
            verdict=REFUSE,
            message="tip tick is presence+tip hash only; no paper bytes on the 1s tick",
            extra={"tip_tick_bodies": False},
        )
    key = str(event or "").strip().lower().replace("_", "-").replace(" ", "-")
    if key not in VAULT_MULTIPLY_EVENTS:
        return _verdict(
            False,
            "AZG-VAULT-EVENT",
            verdict=REFUSE,
            message="vault multiply is bootstrap / join / Cap-7 claim / grid-shift standby only",
            extra={"event": key, "events": sorted(VAULT_MULTIPLY_EVENTS)},
        )
    incomplete = refuse_incomplete_vault(papers=papers)
    if incomplete:
        return incomplete
    if not vault_complete(papers):
        return _verdict(
            False,
            "AZG-INCOMPLETE-VAULT",
            verdict=WAIT,
            message="incomplete vault: AZG-UNVERIFIED-TIP; phoenix-WAIT / hold; do not invent",
            extra={
                "papers": count_vault_papers(papers),
                "min_papers": MIN_PAPERS,
                "false_tip": False,
                "phoenix": "wait",
                "unverified_tip": True,
                "azg_unverified_tip": True,
                "code_alias": "AZG-UNVERIFIED-TIP",
            },
        )
    return _verdict(
        True,
        "AZG-VAULT-MULTIPLY",
        verdict=YES,
        message="vault multiply onto each node; papers land as cold copies",
        extra={
            "event": key,
            "papers": count_vault_papers(papers),
            "min_papers": MIN_PAPERS,
            "plane": PAYLOAD_PLANE,
            "live_body_sync": False,
            "tip_tick_bodies": False,
            "cite_dont_merge": True,
            "cold_copy": True,
        },
    )


def refuse_paper_body_on_tip(
    extra: Mapping[str, Any] | None = None,
    *,
    papers: Iterable[Any] | None = None,
) -> dict[str, Any] | None:
    """No paper bytes on the 1s tip tick."""
    payload = dict(extra or {})
    if papers is not None:
        payload["papers"] = list(papers)
    forbidden = sorted(k for k in payload if str(k).lower() in TIP_TICK_FORBIDDEN)
    if forbidden:
        return _verdict(
            False,
            "STW-TIP-BODY",
            verdict=REFUSE,
            message="tip tick is presence+tip hash only; no paper bytes on the 1s tick",
            extra={"forbid": forbidden, "tip_tick_bodies": False},
        )
    return None


def airgap_mode(
    *,
    enabled: bool = True,
    bearer_radios: bool = False,
    climb_back: bool = False,
    body_gossip: bool = False,
    hub_as_gate: str | bool | None = None,
    vault_papers: Iterable[Any] | None = None,
    neighbor_majority: bool = False,
    serve_local: bool = True,
) -> dict[str, Any]:
    """AIRGAP-1.0: local vault + no bearer radios + no climb-back."""
    if not enabled:
        return _verdict(
            True,
            "AIRGAP-OFF",
            verdict=YES,
            message="airgap mode off",
            extra={"airgap": False, "spec": AIRGAP_SPEC},
        )
    if bearer_radios:
        return _verdict(
            False,
            "AIRGAP-NO-BEARER",
            verdict=REFUSE,
            message="airgap forbids bearer radios",
            extra={"airgap": True, "bearer_radios": False, "spec": AIRGAP_SPEC},
        )
    if climb_back:
        return _verdict(
            False,
            "AIRGAP-NO-CLIMB-BACK",
            verdict=REFUSE,
            message="airgap forbids climb-back onto pulled public hub hostnames",
            extra={"airgap": True, "climb_back": False, "spec": AIRGAP_SPEC},
        )
    if body_gossip:
        return _verdict(
            False,
            "AIRGAP-NO-BODY-GOSSIP",
            verdict=REFUSE,
            message="airgap tip chatter is live/locked/isolated/tip-hash only; no body gossip",
            extra={"airgap": True, "tip_chatter": sorted(AIRGAP_TIP_FIELDS), "spec": AIRGAP_SPEC},
        )
    if neighbor_majority:
        return _verdict(
            False,
            "RH-NO-VOTE-TO-FIX",
            verdict=REFUSE,
            message="airgap reheal never uses neighbor majority",
            extra={"airgap": True, "neighbor_majority": False, "spec": AIRGAP_SPEC},
        )
    if hub_as_gate:
        host = "" if hub_as_gate is True else str(hub_as_gate)
        if hub_as_gate is True or _is_official_hub(host) or host in HUB_NOT_NODE_GATE:
            return _verdict(
                False,
                "MGS-NOT-NODE-GATE",
                verdict=REFUSE,
                message="official hubs are not airgap Node Gate",
                extra={"airgap": True, "official_hubs_are_airgap_node_gate": False, "spec": AIRGAP_SPEC},
            )
    if vault_papers is not None and not vault_complete(vault_papers):
        incomplete = refuse_incomplete_vault(papers=vault_papers)
        if incomplete:
            return incomplete
        return _verdict(
            False,
            "AZG-INCOMPLETE-VAULT",
            verdict=WAIT,
            message="airgap requires the full verified local vault; AZG-UNVERIFIED-TIP; phoenix-WAIT",
            extra={
                "airgap": True,
                "papers": count_vault_papers(vault_papers),
                "min_papers": MIN_PAPERS,
                "phoenix": "wait",
                "unverified_tip": True,
                "azg_unverified_tip": True,
                "code_alias": "AZG-UNVERIFIED-TIP",
            },
        )
    return _verdict(
        True,
        "AIRGAP-OK",
        verdict=YES,
        message="airgap: local vault; no bearer radios; no climb-back; local cold shelf may serve",
        extra={
            "airgap": True,
            "spec": AIRGAP_SPEC,
            "local_vault": True,
            "bearer_radios": False,
            "climb_back": False,
            "body_gossip": False,
            "downloads_from_local_cold_shelf": bool(serve_local),
            "tip_chatter": ["live", "locked", "isolated", "tip-hash"],
            "official_hubs_are_airgap_node_gate": False,
        },
    )


def airgap_reheal(
    *,
    own_tip: bytes | str | None = None,
    trusted_pull: bool = False,
    already_trusted: bool = False,
    phoenix_wait: bool = False,
    neighbor_majority: bool = False,
    body_gossip: bool = False,
) -> dict[str, Any]:
    """Airgap re-expand / reheal: own tip + trusted already-trusted bytes, or phoenix-WAIT."""
    if neighbor_majority:
        return _verdict(
            False,
            "RH-NO-VOTE-TO-FIX",
            verdict=REFUSE,
            message="airgap reheal never uses neighbor majority",
            extra={"airgap": True, "spec": AIRGAP_SPEC},
        )
    if body_gossip:
        return _verdict(
            False,
            "AIRGAP-NO-BODY-GOSSIP",
            verdict=REFUSE,
            message="airgap tip chatter is live/locked/isolated/tip-hash only; no body gossip",
            extra={"airgap": True, "spec": AIRGAP_SPEC},
        )
    if phoenix_wait:
        return _verdict(
            True,
            "RH-PHOENIX-WAIT",
            verdict=WAIT,
            message="airgap reheal phoenix-WAIT",
            extra={"airgap": True, "source": "phoenix-wait", "auto_heal": False, "spec": AIRGAP_SPEC},
        )
    if own_tip and trusted_pull and already_trusted:
        return _verdict(
            True,
            "RH-OWN-TIP",
            verdict=YES,
            message="airgap reheal from own tip plus trusted pull of bytes already trusted",
            extra={
                "airgap": True,
                "source": "own-tip+trusted-pull",
                "already_trusted": True,
                "auto_heal": False,
                "spec": AIRGAP_SPEC,
            },
        )
    return _verdict(
        False,
        "RH-FAIL-CLOSED",
        verdict=WAIT,
        message="airgap reheal fail-closed without own tip + already-trusted pull or phoenix-WAIT",
        extra={"airgap": True, "phoenix": "wait", "spec": AIRGAP_SPEC},
    )


def plant_flag_and_repost(
    *,
    sites: Iterable[Any] | None = None,
    node_data: Mapping[str, Any] | None = None,
    fake_flag: bool = False,
) -> dict[str, Any]:
    """Constantly plant a flag and repost current known sites from node data."""
    if fake_flag:
        return refuse_falsify(kind="fake-flag")
    listed = list(sites or ())
    if node_data and isinstance(node_data.get("sites"), list):
        listed.extend(node_data["sites"])
    names = []
    for site in listed:
        text = _site_text(site)
        if text and text not in names:
            names.append(text)
    return _verdict(
        True,
        "AZG-FLAG-REPOST",
        verdict=YES,
        message="flag planted; current known sites reposted from node data",
        extra={"sites": names, "flag": True, "rewrite": False},
    )


def offline_download_stay_up(
    *,
    origin_offline: bool,
    download_plane: str = "pull-only",
    tip_presence: str = "isolated",
) -> dict[str, Any]:
    """Origin offline: sites stay up for downloads. Tip may isolate/lock."""
    if str(download_plane).lower() not in {"pull-only", "pull", PAYLOAD_PLANE}:
        return _verdict(
            False,
            "AZG-DOWNLOAD-PULL-ONLY",
            verdict=REFUSE,
            message="download plane stays pull-only when origin is offline",
        )
    presence = str(tip_presence).lower()
    if origin_offline and presence not in {"isolated", "locked"}:
        presence = "isolated"
    return _verdict(
        True,
        "AZG-OFFLINE-STAY-UP",
        verdict=YES,
        message="origin offline: sites stay up for downloads (cold-copy / standby / MESH-VAULT)",
        extra={
            "origin_offline": bool(origin_offline),
            "downloads_stay_up": True,
            "download_plane": PAYLOAD_PLANE,
            "tip_plane": presence if origin_offline else "live",
            "mesh_vault": MESH_VAULT_KIND,
        },
    )


def auto_heal(
    *,
    source: str = "own-tip+trusted-pull",
    own_tip: bytes | str | None = None,
    trusted_pull: bool = False,
    phoenix_wait: bool = False,
    neighbor_talk: bool = False,
    vote_to_fix: bool = False,
    labeled_auto_heal: bool = True,
    fields: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Public-stack auto-heal = lawful REHEAL. Vote-to-fix labeled auto-heal refuses."""
    if vote_to_fix or neighbor_talk:
        return _verdict(
            False,
            "RH-NO-VOTE-TO-FIX" if vote_to_fix else "RH-NO-NEIGHBOR-TALK",
            verdict=REFUSE,
            message="neighbor vote-to-fix labeled as auto-heal is refused",
            extra={"labeled_auto_heal": labeled_auto_heal, "public_stack_auto_heal": False},
        )
    out = reheal(
        source=source,
        own_tip=own_tip,
        trusted_pull=trusted_pull,
        phoenix_wait=phoenix_wait,
        neighbor_talk=False,
        vote_to_fix=False,
        fields=fields,
    )
    out["public_stack_auto_heal"] = bool(out.get("ok"))
    out["means"] = "lawful reheal + archive re-expand (REHEAL-1.0 / MESH-REHEAL)"
    out["suite_mesh_auto_heal"] = False
    return out


def node_gate_admit(*, name: str, suffix: str | None = None) -> dict[str, Any]:
    """Node Gate admits honest claim suffixes (.az / .aziel / pivot). Official hubs are not Node Gate."""
    host = _normalize_az_name(name)
    if _is_official_hub(host) or host in HUB_NOT_NODE_GATE or "corpus" in host:
        return _verdict(
            False,
            "MGS-NOT-NODE-GATE",
            verdict=REFUSE,
            message="official hubs are not Node Gate",
            extra={"name": host, "node_gate": False, "softwares_tab": False},
        )
    if not _is_claim_name(host, suffix=suffix) and not _is_claim_name(host):
        return _verdict(
            False,
            "MGS-AZ-ONLY",
            verdict=REFUSE,
            message="Node Gate is the MirageGrid admission/claim surface for honest .az / .aziel / pivot names",
            extra={"name": host, "softwares_tab": False},
        )
    return _verdict(
        True,
        "MGS-NODE-GATE-OK",
        verdict=YES,
        message="admitted on MirageGrid Node Gate (.az)",
        extra={
            "name": host,
            "softwares_tab": False,
            "product": "miragegrid",
            "front": True,
            "callable": False,
        },
    )


def grid_shift(
    *,
    domain_pulled: str,
    az_name: str,
    cloak: bool = True,
    resurrect_hub: bool = False,
    pretend_hub_cell: bool = False,
    neighbor_resurrection: bool = False,
) -> dict[str, Any]:
    """Grid shift: .az stays answerable; node cloaked. Official hub tunnels die."""
    if pretend_hub_cell or neighbor_resurrection:
        return refuse_misleading(
            kind="pretend-hub-cell" if pretend_hub_cell else "neighbor-resurrection"
        )
    if resurrect_hub or _is_official_hub(domain_pulled) and not _is_claim_name(az_name):
        return _verdict(
            False,
            "MGS-NO-HUB-RESURRECT",
            verdict=REFUSE,
            message="grid shift is not resurrection of godlock.uk / corpus hostnames",
            extra={"domain_pulled": domain_pulled, "az_name": az_name},
        )
    if not _is_claim_name(az_name):
        return _verdict(
            False,
            "MGS-AZ-ONLY",
            verdict=REFUSE,
            message="grid shift keeps a .az (or standby) name answerable",
            extra={"az_name": az_name},
        )
    hub_pull = _is_official_hub(domain_pulled)
    return _verdict(
        True,
        "MGS-SHIFT-OK",
        verdict=YES,
        message="grid shift: .az stays answerable; node cloaked/hidden after domain pull",
        extra={
            "domain_pulled": domain_pulled,
            "az_name": _normalize_az_name(az_name),
            "answerable": True,
            "node_cloaked": bool(cloak),
            "mesh_vault": MESH_VAULT_KIND,
            "ip_mask_host": True,
            "hub_tunnels_die_with_pull": True,
            "official_hub_pull": hub_pull,
            "resurrection": False,
        },
    )


def cloak_burst(
    *,
    origin_node: str,
    names: Iterable[str] | None = None,
    heal_fired: bool = True,
    already_claimed: int = 0,
) -> dict[str, Any]:
    """When lawful auto-heal fires, plant up to Cap-7 spare .az names with a cloak."""
    if not heal_fired:
        return _verdict(
            False,
            "MGS-CLOAK-NEED-HEAL",
            verdict=REFUSE,
            message="cloak burst only when lawful auto-heal fires",
            extra={"origin_node": origin_node},
        )
    listed = [_normalize_az_name(n) for n in (names or ())]
    listed = [n for n in listed if n]
    if any(_is_official_hub(n) for n in listed):
        return _verdict(
            False,
            "MGS-NOT-NODE-GATE",
            verdict=REFUSE,
            message="cloak burst does not plant official hub hostnames",
            extra={"origin_node": origin_node},
        )
    if any(not _is_claim_name(n) for n in listed):
        return _verdict(
            False,
            "MGS-AZ-ONLY",
            verdict=REFUSE,
            message="cloak burst plants .az names only",
            extra={"origin_node": origin_node},
        )
    room = CAP_7 - int(already_claimed)
    if room <= 0 or len(listed) > max(room, 0) or len(listed) > CAP_7:
        return _verdict(
            False,
            "AZG-CAP-7",
            verdict=REFUSE,
            message="cloak burst cannot exceed Cap-7 spare/claimed .az names",
            extra={"origin_node": origin_node, "cap": CAP_7, "names": listed},
        )
    return _verdict(
        True,
        "MGS-CLOAK-BURST",
        verdict=YES,
        message="cloak burst planted spare .az names; originating node IP hidden",
        extra={
            "origin_node": origin_node,
            "names": listed,
            "count": len(listed),
            "cap": CAP_7,
            "cloak": True,
            "softwares_tab": False,
        },
    )


def refuse_hub_tunnel_hydra(*, host: str, unmarked: bool = True) -> dict[str, Any]:
    """Unmarked Cloudflare tunnel hydra on official hubs is refuse."""
    if _is_official_hub(host) and unmarked:
        return _verdict(
            False,
            "MGS-HUB-TUNNEL-HYDRA",
            verdict=REFUSE,
            message="unmarked Cloudflare tunnel hydra on official hubs is refused",
            extra={"host": _normalize_az_name(host), "tun_wp": True, "node_ops": True},
        )
    return _verdict(
        True,
        "MGS-HUB-TUNNEL-CLEAR",
        verdict=YES,
        message="not an unmarked official-hub tunnel hydra",
        extra={"host": _normalize_az_name(host)},
    )


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
            "claim": CLAIM_SOCKET,
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
        "public_stack_auto_heal": "REHEAL-1.0 / MESH-REHEAL",
        "reheal_1_0": REHEAL_1_0,
        "mesh_reheal": MESH_REHEAL_SPEC,
        "phoenix": "wait",
    }


def az_generator_dict() -> dict[str, Any]:
    return {
        "law": AZ_GENERATOR_LAW,
        "spec": AZ_GENERATOR_SPEC,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "softwares_tab": False,
        "callable": False,
        "lives": "deep-node",
        "exit": "node-gate-front",
        "dns_factory": "cap-7-mesh-authoritative",
        "public_icann": False,
        "registrar": False,
        "unbounded_public_dns": False,
        "airgap": "AIRGAP-1.0",
        "clock": {
            "minutes": CLAIM_MINUTES,
            "extra_s": CLAIM_EXTRA_S,
            "period_s": CLAIM_CLOCK_S,
            "socket": CLAIM_SOCKET,
            "alias": "7m77s",
        },
        "cap": CAP_7,
        "public_host_pair": 2,
        "first_claim": FIRST_CLAIM_NAME,
        "first_claim_label": FIRST_CLAIM_LABEL,
        "suffix_order": list(CLAIM_SUFFIX_ORDER) + ["pivot"],
        "min_papers": MIN_PAPERS,
        "paper_vault": paper_vault_dict(),
        "tld": AZ_TLD,
        "aziel_tld": AZIEL_TLD,
        "access": {"aznet": True, "azbrowser": True, "merge": False, "naked_public_dns": False},
        "cctld_takeover": False,
        "radio_phy": False,
        "no_lie": True,
        "no_rewrite": True,
        "rewrite_key": False,
        "no_falsify": True,
        "no_ambiguity": True,
        "no_mislead": True,
        "no_fan": NO_FAN_SPEC,
        "no_fan_phrase": NO_FAN_PHRASE,
    }


def grid_shift_dict() -> dict[str, Any]:
    return {
        "law": GRID_SHIFT_LAW,
        "spec": GRID_SHIFT_SPEC,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "softwares_tab": False,
        "mesh_vault": {"kind": MESH_VAULT_KIND, "role": MESH_VAULT_ROLE},
        "cap": CAP_7,
        "cloak_burst": True,
        "node_gate": "miragegrid-.az-only",
        "official_hubs_are_node_gate": False,
        "hub_tunnels_die_with_pull": True,
        "resurrection_of_official_hubs": False,
        "pretend_pulled_hub_still_cell": False,
        "no_lie": True,
        "no_rewrite": True,
        "no_falsify": True,
        "no_ambiguity": True,
        "no_mislead": True,
        "no_fan": NO_FAN_SPEC,
        "no_fan_phrase": NO_FAN_PHRASE,
    }


def public_stack_dict() -> dict[str, Any]:
    return {
        "author": MESH_LAW_AUTHOR,
        "pieces": [
            "anonymity-network",
            "node-gate",
            "auto-heal",
        ],
        "anonymity_network": "onion/mesh privacy (existing MVP; lawful privacy tool)",
        "node_gate": "MirageGrid admission/claim surface for .az names (not official hubs)",
        "auto_heal": "REHEAL-1.0 / MESH-REHEAL: own last good tip + verified trusted pull, or phoenix-WAIT",
        "softwares_tab_products": ["miragegrid"],
        "az_generator_softwares_tab": False,
        "node_gate_softwares_tab": False,
    }


def _semantic_bridge_stamp() -> dict[str, Any]:
    from miragegrid.semantic_bridge import semantic_bridge_dict

    return semantic_bridge_dict()


def _redline_stamp() -> dict[str, Any]:
    from miragegrid.redline import redline_dict

    return redline_dict()


def _cap7_shuffle_stamp() -> dict[str, Any]:
    from miragegrid.cap7_shuffle import cap7_shuffle_dict

    return cap7_shuffle_dict()


def mesh_law_dict() -> dict[str, Any]:
    return {
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "assign_live": ASSIGN_LIVE,
        "public_stack": public_stack_dict(),
        "split_wires": split_wires_dict(),
        "cold_copy": cold_copy_dict(),
        "reheal": reheal_dict(),
        "az_generator": az_generator_dict(),
        "grid_shift": grid_shift_dict(),
        "airgap": airgap_dict(),
        "paper_vault": paper_vault_dict(),
        "no_lie": True,
        "no_rewrite": True,
        "no_fan": no_fan_dict(),
        "radio_phy": False,
        "semantic_bridge": _semantic_bridge_stamp(),
        "get_never_enables": True,
        "claim_complete": False,
        "redline": _redline_stamp(),
        "cap7_shuffle": _cap7_shuffle_stamp(),
    }


def paper_vault_dict() -> dict[str, Any]:
    return {
        "law": PAPER_VAULT_LAW,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "on_every_node": True,
        "full_set": True,
        "min_papers": MIN_PAPERS,
        "multiply": "cold-copy",
        "wording": "vault multiply onto each node / papers land on every node as cold copies",
        "events": ["bootstrap", "join", "cap-7-claim", "grid-shift-standby"],
        "plane": PAYLOAD_PLANE,
        "live_body_sync": False,
        "tip_tick_bodies": False,
        "cite_dont_merge": True,
        "hash_absolute": True,
        "no_have_49_without_bytes": True,
        "incomplete": "AZG-INCOMPLETE-VAULT / AZG-UNVERIFIED-TIP / phoenix-WAIT",
    }


def airgap_dict() -> dict[str, Any]:
    return {
        "law": AIRGAP_LAW,
        "spec": AIRGAP_SPEC,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "softwares_tab": False,
        "local_vault": True,
        "bearer_radios": False,
        "climb_back_pulled_hubs": False,
        "downloads_from_local_cold_shelf": True,
        "origin_offline_downloads_stay_up": True,
        "tip_chatter": ["live", "locked", "isolated", "tip-hash"],
        "body_gossip": False,
        "reheal": "own-tip+trusted-pull-already-trusted-or-phoenix-wait",
        "neighbor_majority": False,
        "official_hubs_are_node_gate": False,
        "official_hubs_are_airgap_node_gate": False,
        "no_lie": True,
        "no_rewrite": True,
        "no_fan": NO_FAN_SPEC,
        "radio_phy": False,
    }


def no_fan_dict() -> dict[str, Any]:
    return {
        "law": NO_FAN_LAW,
        "spec": NO_FAN_SPEC,
        "phrase": NO_FAN_PHRASE,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "beside": [NO_LIE_LAW, NO_REWRITE_LAW],
        "no_lie": True,
        "no_rewrite": True,
        "no_falsify": True,
        "no_ambiguity": True,
        "no_mislead": True,
        "verbs": {
            "falsify": sorted(NO_FAN_FALSIFY_VERBS),
            "ambiguous": sorted(NO_FAN_AMBIGUITY_VERBS),
            "misleading": sorted(NO_FAN_MISLEAD_VERBS),
        },
        "ambiguous_tip": ISOLATE,
        "rewrite_key": False,
    }
