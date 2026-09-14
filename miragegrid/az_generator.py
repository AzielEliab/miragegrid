"""AZ Generator — Cap-7 mesh DNS factory living deep inside the node.

The generator does NOT get called from outside. It is not POST
``/call-generator``, not a Worker-invoked back door, and not a hosted
cron that reaches into the node. Flow is:

    deep node → 7m77s (497s) claim tick → FRONT Node Gate
    (claim / plant / flag / restore)

Node Gate is the outward admission surface. The hosted Worker may
stamp, refuse, and cite law. It must not run the generator.

This is a **Cap-7 mesh DNS factory**: the generator authors at most
seven ``.az`` names per node into a mesh-authoritative / node-local
zone (zone records + claim receipts + tip/hash continuity). All
resolution / browsing goes through **AZNet** and **AZBrowser**
(separate Softwares products; functional pairing only — never merged).
Exactly **2** of the Cap-7 names become hosted public HTTPS
mirrors/gateways for standard browsers. The other slots stay
mesh/AZNet-side. Mesh tip remains authoritative. It is **not** a
public unbounded registrar and does **not** invent ICANN writes or
claim the public ``.az`` ccTLD. ``public_icann`` stays false.

AIRGAP-1.0: the local paper vault is air-gapped from the 1s tip plane.
Paper bodies never ride a tip tick. Vault multiply is allowed only on
bootstrap, join, Cap-7 claim, and grid-shift standby.

Restore / claim requires ≥49 hash-absolute Aziel Eliab papers from the
LOCAL vault. Incomplete vault → AZG-INCOMPLETE-VAULT / phoenix-WAIT.
NO-FAN / NO-LIE / NO-REWRITE. Author: Aziel Eliab only.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from miragegrid.mesh import (
    AZ_GENERATOR_SPEC,
    AZ_TLD,
    AZIEL_TLD,
    CAP_7,
    CLAIM_CLOCK_S,
    CLAIM_SOCKET,
    CLAIM_SUFFIX_ORDER,
    DWELL_SOCKET,
    FIRST_CLAIM_NAME,
    ICANN_PUBLIC_TLDS,
    MESH_LAW_AUTHOR,
    MIN_PAPERS,
    NO_FAN_PHRASE,
    REFUSE,
    TIP_TICK_SOCKET,
    WAIT,
    YES,
    _is_claim_name,
    _verdict,
    claim_az_domain,
    count_aziel_papers,
    first_claim_for_suffix,
    known_contains_first_claim,
    multiply_cold_copies,
    node_gate_admit,
    plant_flag_and_repost,
    refuse_falsify,
    refuse_live_body_sync,
    refuse_no_fan,
    restore_chain,
    select_claim_suffix,
    sockets_share,
)

AIRGAP_LAW = "AIRGAP"
AIRGAP_SPEC = "AIRGAP-1.0"
DNS_FACTORY_KIND = "cap-7-mesh-authoritative"
PUBLIC_HOST_PAIR = 2
AZNET_PRODUCT = "aznet"
AZBROWSER_PRODUCT = "azbrowser"
ACCESS_CLIENTS: frozenset[str] = frozenset({AZNET_PRODUCT, AZBROWSER_PRODUCT})
PUBLIC_BROWSER_CLIENTS: frozenset[str] = frozenset(
    {"browser", "https", "public", "standard-browser", "internet-browser"}
)
ICANN_TLD_REFUSE: frozenset[str] = frozenset(
    {".com", ".net", ".org", ".uk", ".io", ".dev", ".app", ".info", ".co"}
)
VAULT_MULTIPLY_REASONS: frozenset[str] = frozenset(
    {"bootstrap", "join", "cap-7-claim", "grid-shift-standby"}
)
POISON_MARKERS: frozenset[str] = frozenset(
    {
        "poison",
        "poison-marker",
        "poison_marker",
        "rewrite-key",
        "rewrite_key",
        "inject-body",
        "inject_body",
        "false-tip",
        "false_tip",
        "vote-to-fix",
        "vote_to_fix",
    }
)
GENERATOR_SOURCES: frozenset[str] = frozenset(
    {"az-generator", "deep-node", "generator-tick", "node-local"}
)


def refuse_call_generator(*, path: str | None = None) -> dict[str, Any]:
    """Inbound run-generator / back-gate RPC is refuse."""
    return _verdict(
        False,
        "AZG-NOT-CALLABLE",
        verdict=REFUSE,
        message="AZ Generator lives deep in the node; it is not called from outside",
        extra={
            "callable": False,
            "lives": "deep-node",
            "exit": "node-gate-front",
            "path": path or "",
            "softwares_tab": False,
            "public_icann": False,
        },
    )


def refuse_public_registrar(*, kind: str = "icann") -> dict[str, Any]:
    """Do not fake ICANN / public-registrar success or .az ccTLD takeover."""
    return _verdict(
        False,
        "AZG-NOT-PUBLIC-REGISTRAR",
        verdict=REFUSE,
        message="mesh DNS factory is not a public ICANN/Cloudflare registrar; do not fake registration success or .az ccTLD takeover",
        extra={
            "kind": kind,
            "public_icann": False,
            "registrar": False,
            "unbounded_public_dns": False,
            "cctld_takeover": False,
            "dns_factory": DNS_FACTORY_KIND,
        },
    )


def refuse_icann_tld(
    name: str,
    *,
    active_suffix: str | None = None,
    pivot_suffix: str | None = None,
) -> dict[str, Any] | None:
    """Generator claims the active honest suffix only. Never ICANN TLDs."""
    host = str(name or "").strip().lower().split("/")[0]
    if not host:
        return None
    if _is_claim_name(host, suffix=active_suffix):
        return None
    if _is_claim_name(host):
        return None
    if pivot_suffix and _is_claim_name(host, suffix=pivot_suffix):
        return None
    suffix = ""
    for tld in sorted(ICANN_PUBLIC_TLDS | ICANN_TLD_REFUSE, key=len, reverse=True):
        if host.endswith(tld):
            suffix = tld
            break
    return _verdict(
        False,
        "AZG-TLD",
        verdict=REFUSE,
        message="AZ Generator claims the active honest suffix (.az → .aziel → pivot) — not ICANN TLDs",
        extra={
            "name": host,
            "tld": suffix or host,
            "active_suffix": active_suffix or AZ_TLD,
            "public_icann": False,
        },
    )


def refuse_product_merge() -> dict[str, Any]:
    return _verdict(
        False,
        "AZG-NO-MERGE-PRODUCTS",
        verdict=REFUSE,
        message="AZNet and AZBrowser stay separate Softwares products; functional pairing only",
        extra={
            "aznet": AZNET_PRODUCT,
            "azbrowser": AZBROWSER_PRODUCT,
            "merge": False,
            "softwares_tab_az_generator": False,
        },
    )


def refuse_naked_dns() -> dict[str, Any]:
    return _verdict(
        False,
        "AZG-NO-NAKED-DNS",
        verdict=REFUSE,
        message="resolution/browsing goes through AZNet + AZBrowser; not a naked public DNS story",
        extra={
            "access": sorted(ACCESS_CLIENTS),
            "naked_public_dns": False,
            "public_icann": False,
        },
    )


def refuse_poison_marker(marker: str | None = None) -> dict[str, Any]:
    key = str(marker or "poison").strip().lower().replace(" ", "-").replace("_", "-")
    return _verdict(
        False,
        "CCS-POISON-MARKER",
        verdict=REFUSE,
        message="poison marker is hash-absolute refuse",
        extra={"marker": key, "airgap": AIRGAP_SPEC},
    )


def claim_clock_ready(*, now_s: float, last_tick_s: float | None) -> dict[str, Any]:
    """Claim clock may advance only as a law-documented local generator tick.

    777s cite-dwell is a stranger clock (update is proof, not a timer).
    """
    if last_tick_s is None:
        return _verdict(
            True,
            "AZG-CLOCK-READY",
            verdict=YES,
            message="first local generator tick may attempt a claim",
            extra={"period_s": CLAIM_CLOCK_S, "socket": CLAIM_SOCKET, "elapsed_s": 0},
        )
    elapsed = float(now_s) - float(last_tick_s)
    if elapsed < CLAIM_CLOCK_S:
        return _verdict(
            False,
            "AZG-CLOCK-HOLD",
            verdict=REFUSE,
            message="7m77s claim clock has not elapsed; dwell/tip sockets stay strangers",
            extra={
                "period_s": CLAIM_CLOCK_S,
                "elapsed_s": elapsed,
                "socket": CLAIM_SOCKET,
                "tip_socket": TIP_TICK_SOCKET,
                "dwell_socket": DWELL_SOCKET,
            },
        )
    return _verdict(
        True,
        "AZG-CLOCK-READY",
        verdict=YES,
        message="7m77s claim clock elapsed; local generator tick may attempt a claim",
        extra={"period_s": CLAIM_CLOCK_S, "elapsed_s": elapsed, "socket": CLAIM_SOCKET},
    )


def vault_multiply(*, reason: str, copies: int = 2) -> dict[str, Any]:
    """Cold vault multiply only on bootstrap / join / Cap-7 claim / grid-shift standby."""
    key = str(reason or "").strip().lower().replace(" ", "-").replace("_", "-")
    if key not in VAULT_MULTIPLY_REASONS:
        return _verdict(
            False,
            "AZG-VAULT-MULTIPLY",
            verdict=REFUSE,
            message="vault multiply only on bootstrap, join, Cap-7 claim, or grid-shift standby",
            extra={"reason": key, "allowed": sorted(VAULT_MULTIPLY_REASONS), "airgap": AIRGAP_SPEC},
        )
    out = multiply_cold_copies(copies)
    out["reason"] = key
    out["airgap"] = AIRGAP_SPEC
    return out


def vault_live_sync_on_tip(*, live_body_sync: bool = True) -> dict[str, Any]:
    """AIRGAP-1.0: paper bodies never ride the 1s tip tick."""
    if live_body_sync:
        out = refuse_live_body_sync(live_body_sync=True)
        out["code"] = "AZG-AIRGAP"
        out["airgap"] = AIRGAP_SPEC
        out["message"] = "AIRGAP-1.0: paper vault is air-gapped from the tip plane; no live body sync on tip tick"
        return out
    return _verdict(
        True,
        "AZG-AIRGAP-OK",
        verdict=YES,
        message="vault stays air-gapped from the tip plane",
        extra={"airgap": AIRGAP_SPEC, "live_body_sync": False},
    )


def _paper_digest(paper: Mapping[str, Any]) -> str:
    digest = paper.get("hash") or paper.get("sha256") or paper.get("tip_hash")
    raw = str(digest or "").strip().lower()
    return raw


class PaperVault:
    """LOCAL hash-absolute Aziel Eliab paper vault. Cold-copy only."""

    def __init__(self, papers: Iterable[Any] | None = None) -> None:
        self._by_hash: dict[str, dict[str, Any]] = {}
        self._copies = 0
        if papers:
            self._ingest(papers, multiply=False)

    def _ingest(self, papers: Iterable[Any], *, multiply: bool) -> int:
        added = 0
        for paper in papers or ():
            if not isinstance(paper, Mapping):
                continue
            if count_aziel_papers([paper]) != 1:
                continue
            digest = _paper_digest(paper)
            if digest in self._by_hash:
                continue
            body = paper.get("bytes") or paper.get("body") or paper.get("data")
            raw = body if isinstance(body, (bytes, bytearray)) else None
            self._by_hash[digest] = {
                "author": MESH_LAW_AUTHOR,
                "hash": digest,
                "bytes": bytes(raw) if raw is not None else None,
            }
            added += 1
        if multiply and added:
            self._copies = max(self._copies, 2)
        return added

    @property
    def papers(self) -> list[dict[str, Any]]:
        return [dict(p) for p in self._by_hash.values()]

    def verified_count(self) -> int:
        return count_aziel_papers(self.papers)

    def complete(self) -> bool:
        return self.verified_count() >= MIN_PAPERS

    def bootstrap(self, cold_copy: Iterable[Any] | None) -> dict[str, Any]:
        n = self._ingest(cold_copy or (), multiply=True)
        mul = vault_multiply(reason="bootstrap", copies=max(self._copies, 2))
        if not self.complete():
            return _verdict(
                False,
                "AZG-INCOMPLETE-VAULT",
                verdict=WAIT,
                message="bootstrap obtained a cold vault copy; fewer than 49 verified papers; phoenix-WAIT / hold",
                extra={
                    "papers": self.verified_count(),
                    "min_papers": MIN_PAPERS,
                    "added": n,
                    "copies": mul.get("copies", self._copies),
                    "false_tip": False,
                    "phoenix": "wait",
                    "airgap": AIRGAP_SPEC,
                },
            )
        return _verdict(
            True,
            "AZG-VAULT-BOOTSTRAP",
            verdict=YES,
            message="bootstrap obtained a complete cold vault copy",
            extra={
                "papers": self.verified_count(),
                "min_papers": MIN_PAPERS,
                "added": n,
                "copies": mul.get("copies", self._copies),
                "airgap": AIRGAP_SPEC,
            },
        )

    def join(self, cold_copy: Iterable[Any] | None) -> dict[str, Any]:
        n = self._ingest(cold_copy or (), multiply=True)
        vault_multiply(reason="join", copies=max(self._copies, 2))
        if not self.complete():
            return _verdict(
                False,
                "AZG-INCOMPLETE-VAULT",
                verdict=WAIT,
                message="join obtained a cold vault copy; fewer than 49 verified papers; phoenix-WAIT / hold",
                extra={
                    "papers": self.verified_count(),
                    "min_papers": MIN_PAPERS,
                    "added": n,
                    "false_tip": False,
                    "phoenix": "wait",
                    "airgap": AIRGAP_SPEC,
                },
            )
        return _verdict(
            True,
            "AZG-VAULT-JOIN",
            verdict=YES,
            message="join obtained a complete cold vault copy",
            extra={"papers": self.verified_count(), "min_papers": MIN_PAPERS, "added": n, "airgap": AIRGAP_SPEC},
        )

    def gate_claim(self) -> dict[str, Any] | None:
        if self.complete():
            return None
        return _verdict(
            False,
            "AZG-INCOMPLETE-VAULT",
            verdict=WAIT,
            message="incomplete local vault; refuse claim rather than invent continuity; phoenix-WAIT / hold",
            extra={
                "papers": self.verified_count(),
                "min_papers": MIN_PAPERS,
                "false_tip": False,
                "phoenix": "wait",
                "phrase": NO_FAN_PHRASE,
                "airgap": AIRGAP_SPEC,
            },
        )


def _receipt_hash(payload: Mapping[str, Any]) -> str:
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


@dataclass
class MeshDnsZone:
    """Cap-7 mesh-authoritative zone. Not ICANN. Not Cloudflare registrar."""

    origin_node: str
    active_suffix: str = AZ_TLD
    records: list[dict[str, Any]] = field(default_factory=list)

    def names(self) -> list[str]:
        return [str(r["name"]) for r in self.records]

    def public_hosts(self) -> list[str]:
        return [str(r["name"]) for r in self.records if r.get("public_host")]

    def mesh_only(self) -> list[str]:
        return [str(r["name"]) for r in self.records if not r.get("public_host")]

    def __len__(self) -> int:
        return len(self.records)

    def resolve(self, name: str, *, public_icann: bool = False, naked_dns: bool = False) -> dict[str, Any]:
        if public_icann:
            return refuse_public_registrar(kind="resolve-icann")
        if naked_dns:
            return refuse_naked_dns()
        host = str(name or "").strip().lower()
        tld = refuse_icann_tld(host)
        if tld:
            return tld
        for rec in self.records:
            if rec["name"] == host:
                return _verdict(
                    True,
                    "AZG-ZONE-HIT",
                    verdict=YES,
                    message="mesh-authoritative .az resolve via AZNet/AZBrowser",
                    extra={
                        "name": host,
                        "record": dict(rec),
                        "public_icann": False,
                        "registrar": False,
                        "cctld_takeover": False,
                        "dns_factory": DNS_FACTORY_KIND,
                        "access": sorted(ACCESS_CLIENTS),
                        "mesh_tip_authoritative": True,
                    },
                )
        return _verdict(
            False,
            "AZG-ZONE-MISS",
            verdict=REFUSE,
            message="name is not in this node's Cap-7 mesh zone",
            extra={"name": host, "public_icann": False, "dns_factory": DNS_FACTORY_KIND},
        )

    def publish(
        self,
        *,
        name: str,
        tip_hash: str | None = None,
        claim: Mapping[str, Any] | None = None,
        design_of: str | None = None,
        design_pack_sha256: str | None = None,
        public_gateway_url: str | None = None,
    ) -> dict[str, Any]:
        host = str(name or "").strip().lower()
        tld = refuse_icann_tld(host, active_suffix=self.active_suffix)
        if tld:
            return tld
        if host in self.names():
            return _verdict(
                True,
                "AZG-ZONE-EXISTS",
                verdict=YES,
                message="name already in mesh-authoritative zone",
                extra={"name": host, "public_icann": False},
            )
        if len(self.records) >= CAP_7:
            return _verdict(
                False,
                "AZG-CAP-7",
                verdict=REFUSE,
                message="Cap-7: at most 7 .az names per covered node",
                extra={"claimed": len(self.records), "cap": CAP_7, "origin_node": self.origin_node},
            )
        public_host, demote = self._prefer_public_host(host)
        for rec in demote:
            rec["public_host"] = False
            rec["plane"] = "mesh-aznet"
        plane = "public-gateway" if public_host else "mesh-aznet"
        receipt_body = {
            "kind": "azg-claim-receipt",
            "spec": AZ_GENERATOR_SPEC,
            "name": host,
            "origin_node": self.origin_node,
            "period_s": CLAIM_CLOCK_S,
            "cap": CAP_7,
            "public_host_pair": PUBLIC_HOST_PAIR,
            "public_host": public_host,
            "plane": plane,
            "public_icann": False,
            "registrar": False,
            "unbounded_public_dns": False,
            "cctld_takeover": False,
            "dns_factory": DNS_FACTORY_KIND,
            "mesh_authoritative": True,
            "mesh_tip_authoritative": True,
            "access": sorted(ACCESS_CLIENTS),
            "tip_hash": tip_hash or "",
            "claim_code": (claim or {}).get("code"),
            "author": MESH_LAW_AUTHOR,
        }
        receipt_body["hash"] = _receipt_hash(receipt_body)
        rec = {
            "name": host,
            "type": "TXT",
            "origin_node": self.origin_node,
            "ttl_s": CLAIM_CLOCK_S,
            "tip_hash": tip_hash or receipt_body["hash"],
            "receipt": receipt_body,
            "public_host": public_host,
            "plane": plane,
            "mesh_tip_authoritative": True,
            "access": sorted(ACCESS_CLIENTS),
            "public_icann": False,
            "registrar": False,
            "resolves_to_hub": False,
            "name_may_change": True,
        }
        if design_of:
            rec["design_of"] = design_of
        if design_pack_sha256:
            rec["design_pack_sha256"] = design_pack_sha256
        if public_gateway_url:
            rec["public_gateway_url"] = public_gateway_url
        self.records.append(rec)
        vault_multiply(reason="cap-7-claim", copies=2)
        return _verdict(
            True,
            "AZG-ZONE-PUBLISH",
            verdict=YES,
            message=(
                "authored into mesh-authoritative .az zone (not ICANN); "
                + ("hosted public gateway/mirror of mesh tip" if public_host else "mesh/AZNet-side only")
            ),
            extra={
                "name": host,
                "record": rec,
                "receipt": receipt_body,
                "claimed": len(self.records),
                "cap": CAP_7,
                "public_host": public_host,
                "public_hosts": self.public_hosts(),
                "public_host_pair": PUBLIC_HOST_PAIR,
                "plane": plane,
                "mesh_tip_authoritative": True,
                "public_icann": False,
                "registrar": False,
                "cctld_takeover": False,
                "dns_factory": DNS_FACTORY_KIND,
                "access": sorted(ACCESS_CLIENTS),
            },
        )

    def _prefer_public_host(self, host: str) -> tuple[bool, list[dict[str, Any]]]:
        """Prefer azcorpus + azlibrary as the Cap-7 public HTTPS pair when claimed."""
        from miragegrid.semantic_bridge import preferred_public_pair_label

        preferred = preferred_public_pair_label(host) is not None
        public = [r for r in self.records if r.get("public_host")]
        if len(public) < PUBLIC_HOST_PAIR:
            return True, []
        if preferred:
            bumpable = [r for r in public if preferred_public_pair_label(str(r.get("name") or "")) is None]
            if bumpable:
                return True, [bumpable[0]]
        return False, []

    def designate_public_pair(self, names: Iterable[str]) -> dict[str, Any]:
        """Exactly 2 Cap-7 names may be hosted public browser gateways."""
        listed = [str(n).strip().lower() for n in names]
        if len(listed) != PUBLIC_HOST_PAIR:
            return _verdict(
                False,
                "AZG-PUBLIC-PAIR",
                verdict=REFUSE,
                message="exactly 2 of the Cap-7 .az names become hosted public servers",
                extra={"count": len(listed), "pair": PUBLIC_HOST_PAIR, "cap": CAP_7},
            )
        if any(n not in self.names() for n in listed):
            return _verdict(
                False,
                "AZG-PUBLIC-PAIR",
                verdict=REFUSE,
                message="public pair must be names already in this node's Cap-7 zone",
                extra={"names": listed, "zone": self.names()},
            )
        if len(set(listed)) != PUBLIC_HOST_PAIR:
            return _verdict(
                False,
                "AZG-PUBLIC-PAIR",
                verdict=REFUSE,
                message="public pair must be two distinct .az names",
                extra={"names": listed},
            )
        for rec in self.records:
            rec["public_host"] = rec["name"] in listed
            rec["plane"] = "public-gateway" if rec["public_host"] else "mesh-aznet"
        return _verdict(
            True,
            "AZG-PUBLIC-PAIR-OK",
            verdict=YES,
            message="exactly 2 hosted public HTTPS gateways/mirrors; mesh tip remains authoritative",
            extra={
                "public_hosts": self.public_hosts(),
                "mesh_only": self.mesh_only(),
                "pair": PUBLIC_HOST_PAIR,
                "cap": CAP_7,
                "mesh_tip_authoritative": True,
                "public_icann": False,
                "cctld_takeover": False,
            },
        )

    def bridge_registry(self) -> dict[str, Any]:
        """Honest SEMANTIC-BRIDGE map of this zone. Never invents hub resolution."""
        from miragegrid.semantic_bridge import build_bridge_registry

        return build_bridge_registry(zone=self)

    def zone_file(self) -> str:
        lines = [
            "; MirageGrid Cap-7 mesh-authoritative .az zone",
            "; NOT ICANN. NOT a Cloudflare/public registrar write. NOT .az ccTLD takeover.",
            f"; origin={self.origin_node} cap={CAP_7} public_pair={PUBLIC_HOST_PAIR} clock={CLAIM_CLOCK_S}s",
            f"; access=aznet,azbrowser author={MESH_LAW_AUTHOR}",
        ]
        for rec in self.records:
            receipt = rec.get("receipt") or {}
            digest = receipt.get("hash") or rec.get("tip_hash") or ""
            plane = rec.get("plane") or "mesh-aznet"
            lines.append(
                f"{rec['name']}. {rec['ttl_s']} IN TXT \"azg-claim origin={rec['origin_node']} plane={plane} hash={digest}\""
            )
        return "\n".join(lines) + "\n"


def access_name(
    *,
    name: str,
    client: str,
    zone: MeshDnsZone,
    merge_products: bool = False,
    naked_dns: bool = False,
    cctld_takeover: bool = False,
) -> dict[str, Any]:
    """All names via AZNet/AZBrowser. Standard browsers reach only the public pair."""
    if merge_products:
        return refuse_product_merge()
    if cctld_takeover:
        return refuse_public_registrar(kind="cctld-takeover")
    if naked_dns:
        return refuse_naked_dns()
    host = str(name or "").strip().lower()
    tld = refuse_icann_tld(host)
    if tld:
        return tld
    hit = zone.resolve(host)
    if not hit.get("ok"):
        return hit
    rec = next(r for r in zone.records if r["name"] == host)
    key = str(client or "").strip().lower().replace("_", "-")
    if key in ACCESS_CLIENTS:
        return _verdict(
            True,
            "AZG-ACCESS-MESH",
            verdict=YES,
            message="name accessible via AZNet/AZBrowser (separate Softwares; pairing only)",
            extra={
                "name": host,
                "client": key,
                "public_host": bool(rec.get("public_host")),
                "plane": rec.get("plane"),
                "mesh_tip_authoritative": True,
                "merge": False,
                "access": sorted(ACCESS_CLIENTS),
            },
        )
    if key in PUBLIC_BROWSER_CLIENTS:
        if rec.get("public_host"):
            return _verdict(
                True,
                "AZG-ACCESS-PUBLIC-GATEWAY",
                verdict=YES,
                message="hosted public HTTPS gateway/mirror of a mesh .az name; mesh tip remains authoritative",
                extra={
                    "name": host,
                    "client": key,
                    "public_host": True,
                    "plane": "public-gateway",
                    "mesh_tip_authoritative": True,
                    "public_icann": False,
                    "pair": PUBLIC_HOST_PAIR,
                },
            )
        return _verdict(
            False,
            "AZG-PUBLIC-PAIR",
            verdict=REFUSE,
            message="standard browsers reach exactly 2 hosted public gateways; this name stays mesh/AZNet-side",
            extra={
                "name": host,
                "client": key,
                "public_hosts": zone.public_hosts(),
                "pair": PUBLIC_HOST_PAIR,
                "access": sorted(ACCESS_CLIENTS),
            },
        )
    return refuse_naked_dns()


def node_gate_exit(
    *,
    source: str,
    action: str,
    name: str | None = None,
    payload: Mapping[str, Any] | None = None,
    suffix: str | None = None,
) -> dict[str, Any]:
    """FRONT Node Gate: generator exits here. Inbound run-generator refuses."""
    src = str(source or "").strip().lower()
    act = str(action or "").strip().lower().replace("_", "-")
    if act in {"call-generator", "run-generator", "call", "invoke"} or src in {"back-gate", "rpc", "worker", "hosted"}:
        return refuse_call_generator(path=act)
    if src not in GENERATOR_SOURCES:
        return refuse_call_generator(path=src or "unknown")
    if name:
        admitted = node_gate_admit(name=name, suffix=suffix)
        if not admitted.get("ok"):
            return admitted
    return _verdict(
        True,
        "MGS-NODE-GATE-EXIT",
        verdict=YES,
        message="generator exited through FRONT Node Gate",
        extra={
            "source": src,
            "action": act,
            "name": name or "",
            "front": True,
            "back_gate": False,
            "softwares_tab": False,
            "product": "miragegrid",
            "payload_keys": sorted((payload or {}).keys()),
        },
    )


def attempt_claim(
    *,
    origin_node: str,
    vault: PaperVault,
    zone: MeshDnsZone | None = None,
    known_sites: Iterable[Any] | None = None,
    name: str | None = None,
    claimable: bool = True,
    tip_verified: bool = True,
    now_s: float | None = None,
    last_tick_s: float | None = None,
    invent_continuity: bool = False,
    fake_flag: bool = False,
    public_registrar: bool = False,
    inbound_call: bool = False,
    poison: str | None = None,
    az_usable: bool = True,
    aziel_usable: bool = True,
    pivot_suffix: str | None = None,
) -> dict[str, Any]:
    """Local 497s claim pipeline. Vault-gated. Exits FRONT Node Gate. Not DNS/ICANN."""
    if inbound_call:
        return refuse_call_generator(path="attempt_claim")
    if poison:
        return refuse_poison_marker(poison)
    fan = refuse_no_fan(
        "invent" if invent_continuity else ("fake-flag" if fake_flag else None),
        falsify=invent_continuity or fake_flag,
    )
    if fan:
        return fan
    if public_registrar:
        return refuse_public_registrar()
    if now_s is not None:
        clock = claim_clock_ready(now_s=now_s, last_tick_s=last_tick_s)
        if not clock.get("ok"):
            return clock
    held = vault.gate_claim()
    if held:
        return held
    chosen = select_claim_suffix(
        az_usable=az_usable, aziel_usable=aziel_usable, pivot_suffix=pivot_suffix
    )
    if not chosen.get("ok"):
        return chosen
    suffix = str(chosen["suffix"])
    zone = zone if zone is not None else MeshDnsZone(origin_node=origin_node, active_suffix=suffix)
    zone.active_suffix = suffix
    claimed = len(zone)
    claim = claim_az_domain(
        origin_node=origin_node,
        known_sites=known_sites,
        claimed=claimed,
        name=name,
        claimable=claimable,
        papers=vault.papers,
        tip_verified=tip_verified,
        invent_continuity=False,
        fake_flag=False,
        public_registrar=False,
        az_usable=az_usable,
        aziel_usable=aziel_usable,
        pivot_suffix=pivot_suffix,
    )
    if not claim.get("ok"):
        return claim
    if claim.get("code") == "AZG-FIRST-CLAIM-RESUME":
        claim["fake_flag"] = False
        claim["zone_written"] = False
        claim["public_icann"] = False
        return claim
    target = str(claim.get("name") or name or "")
    if not target:
        return claim
    gate = node_gate_exit(source="az-generator", action="claim", name=target, payload=claim, suffix=suffix)
    if not gate.get("ok"):
        return gate
    published = zone.publish(name=target, tip_hash=str(claim.get("code") or ""), claim=claim)
    if not published.get("ok"):
        return published
    flag = plant_flag_and_repost(sites=list(known_sites or []) + [target], fake_flag=False)
    out = dict(claim)
    out["exit"] = "node-gate-front"
    out["lives"] = "deep-node"
    out["callable"] = False
    out["public_icann"] = False
    out["registrar"] = False
    out["dns_factory"] = DNS_FACTORY_KIND
    out["zone"] = published.get("record")
    out["receipt"] = published.get("receipt")
    out["flag"] = flag.get("flag")
    out["node_gate"] = gate
    out["claimed"] = len(zone)
    out["cap"] = CAP_7
    out["suffix"] = suffix
    out["first_claim"] = first_claim_for_suffix(suffix)
    out["public_host"] = bool((published.get("record") or {}).get("public_host"))
    out["public_hosts"] = zone.public_hosts()
    out["access"] = sorted(ACCESS_CLIENTS)
    return out


class AzGenerator:
    """Deep-node Cap-7 mesh DNS factory. Not callable from outside."""

    callable = False
    lives = "deep-node"
    exit = "node-gate-front"

    def __init__(
        self,
        origin_node: str,
        *,
        vault: PaperVault | None = None,
        known_sites: Iterable[Any] | None = None,
        tip_hash: str | None = None,
    ) -> None:
        self.origin_node = origin_node
        self.vault = vault if vault is not None else PaperVault()
        self.az_usable = True
        self.aziel_usable = True
        self.pivot_suffix: str | None = None
        chosen = select_claim_suffix(az_usable=True, aziel_usable=True)
        self.zone = MeshDnsZone(origin_node=origin_node, active_suffix=str(chosen.get("suffix") or AZ_TLD))
        self.known_sites: list[Any] = list(known_sites or [])
        self.last_tick_s: float | None = None
        self.tip_hash = tip_hash or ""
        self.tip_verified = True

    def set_suffix_availability(
        self,
        *,
        az_usable: bool = True,
        aziel_usable: bool = True,
        pivot_suffix: str | None = None,
    ) -> dict[str, Any]:
        """Stamp the active honest suffix. Do not pretend .az/.aziel succeeded."""
        self.az_usable = bool(az_usable)
        self.aziel_usable = bool(aziel_usable)
        self.pivot_suffix = pivot_suffix
        chosen = select_claim_suffix(
            az_usable=self.az_usable, aziel_usable=self.aziel_usable, pivot_suffix=self.pivot_suffix
        )
        if chosen.get("ok"):
            self.zone.active_suffix = str(chosen["suffix"])
        return chosen

    def call(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return refuse_call_generator(path="AzGenerator.call")

    __call__ = call

    def tick(
        self,
        *,
        now_s: float,
        name: str | None = None,
        claimable: bool = True,
        tip_verified: bool | None = None,
    ) -> dict[str, Any]:
        """Local 7m77s generator tick. Operator/local loop OK. Not a hosted cron."""
        clock = claim_clock_ready(now_s=now_s, last_tick_s=self.last_tick_s)
        if not clock.get("ok"):
            return clock
        verified = self.tip_verified if tip_verified is None else tip_verified
        out = attempt_claim(
            origin_node=self.origin_node,
            vault=self.vault,
            zone=self.zone,
            known_sites=self.known_sites,
            name=name,
            claimable=claimable,
            tip_verified=verified,
            now_s=now_s,
            last_tick_s=self.last_tick_s,
            az_usable=self.az_usable,
            aziel_usable=self.aziel_usable,
            pivot_suffix=self.pivot_suffix,
        )
        self.last_tick_s = float(now_s)
        if out.get("name") and out.get("ok") and out.get("code") not in {"AZG-FIRST-CLAIM-RESUME", "AZG-CLOCK-TICK"}:
            if out["name"] not in [_site(s) for s in self.known_sites]:
                self.known_sites.append(out["name"])
        return out

    def plant_and_repost(self, *, fake_flag: bool = False) -> dict[str, Any]:
        return plant_flag_and_repost(sites=self.known_sites + self.zone.names(), node_data={"sites": self.zone.names()}, fake_flag=fake_flag)

    def restore_from_active_point(self, *, most_active_point: str | None = None, broken: bool = True) -> dict[str, Any]:
        held = self.vault.gate_claim()
        if held:
            return held
        return restore_chain(papers=self.vault.papers, broken=broken, most_active_point=most_active_point)

    def to_dict(self) -> dict[str, Any]:
        return {
            "origin_node": self.origin_node,
            "callable": False,
            "lives": self.lives,
            "exit": self.exit,
            "dns_factory": DNS_FACTORY_KIND,
            "public_icann": False,
            "registrar": False,
            "unbounded_public_dns": False,
            "softwares_tab": False,
            "spec": AZ_GENERATOR_SPEC,
            "period_s": CLAIM_CLOCK_S,
            "cap": CAP_7,
            "first_claim": first_claim_for_suffix(self.zone.active_suffix),
            "suffix": self.zone.active_suffix,
            "suffix_order": list(CLAIM_SUFFIX_ORDER) + ["pivot"],
            "min_papers": MIN_PAPERS,
            "papers": self.vault.verified_count(),
            "vault_complete": self.vault.complete(),
            "claimed": len(self.zone),
            "zone_names": self.zone.names(),
            "public_hosts": self.zone.public_hosts(),
            "public_host_pair": PUBLIC_HOST_PAIR,
            "access": sorted(ACCESS_CLIENTS),
            "known_contains_first": known_contains_first_claim(self.known_sites, suffix=self.zone.active_suffix),
            "airgap": AIRGAP_SPEC,
            "author": MESH_LAW_AUTHOR,
            "three_clocks_strangers": sockets_share("1s", "7m77s")["code"] == "STW-SOCKET-SPLIT",
        }


class DeepNode:
    """One node process. The generator lives inside; the front gate is the only exit."""

    def __init__(
        self,
        node_id: str,
        *,
        vault: PaperVault | None = None,
        known_sites: Iterable[Any] | None = None,
    ) -> None:
        self.node_id = node_id
        self.generator = AzGenerator(node_id, vault=vault, known_sites=known_sites)

    def call_generator(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return refuse_call_generator(path="DeepNode.call_generator")

    def tick(self, *, now_s: float, **kwargs: Any) -> dict[str, Any]:
        return self.generator.tick(now_s=now_s, **kwargs)

    def node_gate(self, *, action: str, name: str | None = None) -> dict[str, Any]:
        return node_gate_exit(source="az-generator", action=action, name=name)


def _site(site: Any) -> str:
    if isinstance(site, Mapping):
        return str(site.get("name") or site.get("host") or site.get("url") or "")
    return str(site or "")


def synthetic_papers(n: int) -> list[dict[str, Any]]:
    """Operator/test helper. Hash-absolute Aziel Eliab papers. Not a public corpus fill."""
    out: list[dict[str, Any]] = []
    for i in range(int(n)):
        body = f"aziel-eliab-paper-{i}".encode("utf-8")
        out.append({"author": MESH_LAW_AUTHOR, "hash": hashlib.sha256(body).hexdigest(), "bytes": body})
    return out
