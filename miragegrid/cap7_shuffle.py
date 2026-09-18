"""CAP7-SHUFFLE-1.0 — ping MirageGrid until land; land is the update door.

Cap-7 factory sites have different MirageGrid-only names. They inherit
hub design DNA only (resolves_to_hub false; name_may_change true).
Not a public ICANN .az registrar. AZ Generator exits FRONT Node Gate
only. radio_phy stays false.

Author: Aziel Eliab only.
"""

from __future__ import annotations

import hashlib
from typing import Any, Mapping

from miragegrid.az_generator import PUBLIC_HOST_PAIR, refuse_call_generator, refuse_public_registrar
from miragegrid.mesh import (
    CAP_7,
    MESH_LAW_AUTHOR,
    REFUSE,
    YES,
    _verdict,
    refuse_no_fan,
    refuse_radio_phy,
)
from miragegrid.semantic_bridge import (
    APP_WORKER_HOST,
    CANONICAL_HUBS,
    FIRST_CLAIM_NAME,
    PERSON_ID,
    SEMANTIC_BRIDGE_SPEC,
    WORKER_HOST,
    app_worker,
    download_worker,
    person_id,
    refuse_hub_resolution,
    refuse_invent_first_flag_https,
    refuse_public_dns_claim,
)

CAP7_SHUFFLE_LAW = "CAP-7 LIVE SHUFFLE"
CAP7_SHUFFLE_SPEC = "CAP7-SHUFFLE-1.0"
DOWNLOAD_WORKER_HOST = WORKER_HOST
AZIEL_RUNTIME = "https://aziel-runtime.vibelock.workers.dev"
AZNET_PRODUCT = "aznet"
AZBROWSER_PRODUCT = "azbrowser"

HUB_AE = "https://www.azieleliab.com/"
HUB_CORPUS = "https://www.azielcorpuslibrary.net/"
HUB_GODLOCK = "https://godlock.uk/"
HUB_HDJ = "https://hedidntjump.com/"

# MirageGrid-only factory names. Not hub hostnames. Not azcorpus/azlibrary.
CAP7_FACTORY_SITES: tuple[dict[str, Any], ...] = (
    {
        "label": "azgrid",
        "role": "factory-grid",
        "design": "azieleliab software/runtime hub design DNA",
        "canonical_hub": HUB_AE,
        "design_of": HUB_AE,
        "reach": "https-gateway",
        "honesty_public": "LIVE",
        "browser_reachable": True,
    },
    {
        "label": "azbooth",
        "role": "factory-booth",
        "design": "azieleliab session-booth design DNA",
        "canonical_hub": HUB_AE,
        "design_of": HUB_AE,
        "reach": "https-gateway",
        "honesty_public": "LIVE",
        "browser_reachable": True,
    },
    {
        "label": "azcloak",
        "role": "factory-cloak",
        "design": "godlock cloak/dark design DNA",
        "canonical_hub": HUB_GODLOCK,
        "design_of": HUB_GODLOCK,
        "reach": "aznet",
        "honesty_public": "SLOT",
        "browser_reachable": False,
    },
    {
        "label": "azvault",
        "role": "factory-vault",
        "design": "corpus vault/shelf design DNA",
        "canonical_hub": HUB_CORPUS,
        "design_of": HUB_CORPUS,
        "reach": "aznet",
        "honesty_public": "SLOT",
        "browser_reachable": False,
    },
    {
        "label": "azshift",
        "role": "factory-shift",
        "design": "hedidntjump shift/standby design DNA",
        "canonical_hub": HUB_HDJ,
        "design_of": HUB_HDJ,
        "reach": "aznet",
        "honesty_public": "SLOT",
        "browser_reachable": False,
    },
    {
        "label": "azflag",
        "role": "factory-flag",
        "design": "corpus cite/flag design DNA",
        "canonical_hub": HUB_CORPUS,
        "design_of": HUB_CORPUS,
        "reach": "aznet",
        "honesty_public": "SLOT",
        "browser_reachable": False,
    },
    {
        "label": "azstandby",
        "role": "factory-standby",
        "design": "godlock standby/mask design DNA",
        "canonical_hub": HUB_GODLOCK,
        "design_of": HUB_GODLOCK,
        "reach": "aznet",
        "honesty_public": "SLOT",
        "browser_reachable": False,
    },
)

PUBLIC_PAIR_LABELS: tuple[str, ...] = ("azgrid", "azbooth")
AZNET_SIDE_LABELS: tuple[str, ...] = ("azcloak", "azvault", "azshift", "azflag", "azstandby")
FACTORY_LABELS: tuple[str, ...] = tuple(site["label"] for site in CAP7_FACTORY_SITES)


def _hex64(value: Any) -> str | None:
    text = str(value or "").strip().lower()
    return text if len(text) == 64 and all(c in "0123456789abcdef" for c in text) else None


def site_record(site: Mapping[str, Any]) -> dict[str, Any]:
    label = str(site["label"])
    public = bool(site.get("browser_reachable"))
    honesty = "LIVE" if public else "SLOT"
    path = f"/cap7/{label}" if public else f"/aznet/cap7/{label}"
    return {
        "label": label,
        "mesh_name": f"{label}.az",
        "role": site["role"],
        "design": site["design"],
        "canonical_hub": site["canonical_hub"],
        "design_of": site["design_of"],
        "resolves_to_hub": False,
        "name_may_change": True,
        "public_icann": False,
        "icann": False,
        "fifth_product": False,
        "radio_phy": False,
        "reach": site["reach"],
        "honesty_public": honesty,
        "browser_reachable": public,
        "aznet": True,
        "azbrowser": True,
        "merge": False,
        "mesh_name_icann": "SLOT",
        "worker_path": APP_WORKER_HOST + path,
        "aznet_endpoint": f"aznet://cap7/{label}",
        "update_path": (APP_WORKER_HOST + path + "/update") if public else f"aznet://cap7/{label}/update",
        "person": person_id(),
        "author": MESH_LAW_AUTHOR,
    }


def cap7_roster() -> list[dict[str, Any]]:
    return [site_record(site) for site in CAP7_FACTORY_SITES]


def cap7_shuffle_dict() -> dict[str, Any]:
    return {
        "law": CAP7_SHUFFLE_LAW,
        "spec": CAP7_SHUFFLE_SPEC,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "person": person_id(),
        "cap": CAP_7,
        "public_host_pair": PUBLIC_HOST_PAIR,
        "public_pair": list(PUBLIC_PAIR_LABELS),
        "aznet_side": list(AZNET_SIDE_LABELS),
        "labels": list(FACTORY_LABELS),
        "sites": cap7_roster(),
        "resolves_to_hub": False,
        "name_may_change": True,
        "public_icann": False,
        "fifth_product": False,
        "radio_phy": False,
        "hardcoded_host": False,
        "update_is_proof": True,
        "az_generator": {
            "callable": False,
            "lives": "deep-node",
            "exit": "node-gate-front",
            "radio_phy": False,
            "public_icann": False,
        },
        "access": {"aznet": True, "azbrowser": True, "merge": False, "naked_public_dns": False},
        "app_worker": app_worker(),
        "download_worker": download_worker(),
        "first_flag": FIRST_CLAIM_NAME,
        "invented_first_flag_https": False,
        "canonical_hubs": [row["canonical_hub"] for row in CANONICAL_HUBS],
        "named_mesh_designs": ["azcorpus", "azlibrary"],
        "note": "Nodes ping the app Worker until they land on one Cap-7 site. That land is the update endpoint for the round. No single hard-coded Cap-7 host.",
    }


def shuffle_seed(*, prev: str | None = None, lockset: str | None = None, round_id: str | None = None) -> str | None:
    """Update seed is prev|lockset (proof). Coordination seed is round_id. No timer."""
    p = str(prev or "").strip()
    lock = str(lockset or "").strip()
    rid = str(round_id or "").strip()
    if p and lock:
        raw = f"{p}|{lock}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()
    if rid:
        return hashlib.sha256(f"round|{rid}".encode("utf-8")).hexdigest()
    return None


def land_index(seed_hex: str) -> int:
    digest = _hex64(seed_hex) or hashlib.sha256(str(seed_hex).encode("utf-8")).hexdigest()
    return int(digest[:16], 16) % CAP_7


def land_site(seed_hex: str) -> dict[str, Any]:
    return site_record(CAP7_FACTORY_SITES[land_index(seed_hex)])


def apply_update(
    *,
    node_id: str | None = None,
    prev: str | None = None,
    lockset: str | None = None,
    round_id: str | None = None,
    radio_phy: bool = False,
    inbound_call: bool = False,
    public_icann: bool = False,
    resolves_to_hub: bool = False,
    hardcoded_host: str | None = None,
    invent_first_flag: bool = False,
) -> dict[str, Any]:
    """Third hop: ping must already be able to land; land is this round's update door."""
    landed = ping(
        node_id=node_id,
        prev=prev,
        lockset=lockset,
        round_id=round_id,
        radio_phy=radio_phy,
        inbound_call=inbound_call,
        public_icann=public_icann,
        resolves_to_hub=resolves_to_hub,
        hardcoded_host=hardcoded_host,
        invent_first_flag=invent_first_flag,
        method="POST",
    )
    if not landed.get("ok"):
        return landed
    if landed.get("phase") != "land" or not landed.get("land"):
        return _verdict(
            True,
            "CAP7-PING",
            verdict=YES,
            message="update waits on land; ping MirageGrid with prev+lockset or round_id",
            extra={
                "phase": "ping",
                "continue": True,
                "land": None,
                "update": False,
                "hardcoded_host": False,
                "spec": CAP7_SHUFFLE_SPEC,
            },
        )
    site = landed["land"]
    return _verdict(
        True,
        "CAP7-UPDATE",
        verdict=YES,
        message="update endpoint is the landed Cap-7 site for this round; no hard-coded host",
        extra={
            "phase": "update",
            "continue": False,
            "land": site,
            "update": True,
            "update_endpoint": site["update_path"],
            "round_seed": landed.get("round_seed"),
            "node_id": landed.get("node_id"),
            "hardcoded_host": False,
            "resolves_to_hub": False,
            "public_icann": False,
            "radio_phy": False,
            "spec": CAP7_SHUFFLE_SPEC,
            "app_worker": app_worker(),
        },
    )


def refuse_hardcoded_host() -> dict[str, Any]:
    return _verdict(
        False,
        "CAP7-NO-HARDCODED-HOST",
        verdict=REFUSE,
        message="update shuffle has no single hard-coded Cap-7 host; land comes from the ping seed",
        extra={"hardcoded_host": False, "spec": CAP7_SHUFFLE_SPEC},
    )


def ping(
    *,
    node_id: str | None = None,
    prev: str | None = None,
    lockset: str | None = None,
    round_id: str | None = None,
    radio_phy: bool = False,
    inbound_call: bool = False,
    public_icann: bool = False,
    resolves_to_hub: bool = False,
    hardcoded_host: str | None = None,
    invent_first_flag: bool = False,
    method: str = "POST",
) -> dict[str, Any]:
    """Node pings MirageGrid. Lands on one Cap-7 site when a seed is present."""
    if str(method or "POST").upper() in {"GET", "HEAD"} and (prev or lockset) and not round_id:
        # GET may cite a land for a supplied round_id; it never plants an update.
        pass
    if inbound_call:
        return refuse_call_generator(path="cap7-shuffle-ping")
    if radio_phy:
        return refuse_radio_phy(kind="rf")
    if public_icann:
        return refuse_public_registrar(kind="shuffle-icann")
    if resolves_to_hub:
        return refuse_hub_resolution()
    if invent_first_flag:
        return refuse_invent_first_flag_https()
    if hardcoded_host:
        return refuse_hardcoded_host()
    fan = refuse_no_fan(None)
    if fan and fan.get("ok") is False:
        return fan

    seed = shuffle_seed(prev=prev, lockset=lockset, round_id=round_id)
    node = str(node_id or "").strip() or "anonymous"
    if not seed:
        return _verdict(
            True,
            "CAP7-PING",
            verdict=YES,
            message="ping accepted; supply prev+lockset (update proof) or round_id to land",
            extra={
                "phase": "ping",
                "continue": True,
                "land": None,
                "update": False,
                "node_id": node,
                "hardcoded_host": False,
                "spec": CAP7_SHUFFLE_SPEC,
                "sites": cap7_roster(),
                "app_worker": app_worker(),
            },
        )

    site = land_site(seed)
    update = bool(str(prev or "").strip() and str(lockset or "").strip())
    return _verdict(
        True,
        "CAP7-LAND",
        verdict=YES,
        message="landed on one Cap-7 site; that land is the update endpoint for this round" if update else "landed on one Cap-7 site for this shuffle round",
        extra={
            "phase": "land",
            "continue": False,
            "land": site,
            "update": update,
            "update_endpoint": site["update_path"],
            "round_seed": seed,
            "node_id": node,
            "hardcoded_host": False,
            "spec": CAP7_SHUFFLE_SPEC,
            "radio_phy": False,
            "public_icann": False,
            "resolves_to_hub": False,
            "app_worker": app_worker(),
        },
    )


def shuffle_cite() -> dict[str, Any]:
    law = cap7_shuffle_dict()
    return _verdict(
        True,
        "CAP7-SHUFFLE-CITE",
        verdict=YES,
        message="CAP7-SHUFFLE-1.0 cite. Ping the app Worker until land. No hard-coded Cap-7 host. Empty ICANN claims stay SLOT.",
        extra={
            **law,
            "doors": {
                "bridge": APP_WORKER_HOST + "/bridge",
                "bridge_json": APP_WORKER_HOST + "/bridge.json",
                "v1_bridge": APP_WORKER_HOST + "/v1/bridge",
                "shuffle": APP_WORKER_HOST + "/v1/shuffle",
                "ping": APP_WORKER_HOST + "/v1/shuffle/ping",
                "land": APP_WORKER_HOST + "/v1/shuffle/land",
                "update": APP_WORKER_HOST + "/v1/shuffle/update",
                "cap7": APP_WORKER_HOST + "/v1/cap7",
            },
            "phase": "cite",
            "continue": False,
            "land": None,
        },
    )


def hosted_bridge_doors() -> dict[str, Any]:
    """LIVE doors aziel-runtime can cite. Honest SLOT vs LIVE."""
    cite = shuffle_cite()
    return {
        "ok": True,
        "code": "BRIDGE-CAP7-SHUFFLE",
        "spec": SEMANTIC_BRIDGE_SPEC,
        "shuffle_spec": CAP7_SHUFFLE_SPEC,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "person": {"@id": PERSON_ID, "name": MESH_LAW_AUTHOR},
        "public_icann": False,
        "resolves_to_hub": False,
        "name_may_change": True,
        "fifth_product": False,
        "radio_phy": False,
        "hardcoded_host": False,
        "app_worker": app_worker(),
        "download_worker": download_worker(),
        "runtime": AZIEL_RUNTIME,
        "aznet": AZNET_PRODUCT,
        "azbrowser": AZBROWSER_PRODUCT,
        "merge": False,
        "cap7": cite["sites"],
        "public_pair": list(PUBLIC_PAIR_LABELS),
        "aznet_side": list(AZNET_SIDE_LABELS),
        "doors": cite["doors"],
        "first_flag": FIRST_CLAIM_NAME,
        "invented_first_flag_https": False,
        "honesty": {
            "app_worker": "LIVE",
            "download_worker": "LIVE",
            "public_pair_https": "LIVE",
            "aznet_side_https": "SLOT",
            "mesh_az_icann": "SLOT",
            "first_flag_https": "SLOT",
        },
        "az_generator": cite["az_generator"],
        "note": cite["note"],
    }


def refuse_slot_as_live(label: str) -> dict[str, Any]:
    return _verdict(
        False,
        "CAP7-SLOT-NOT-LIVE",
        verdict=REFUSE,
        message="this Cap-7 slot is AZNet-side; do not invent public HTTPS LIVE",
        extra={
            "label": label,
            "honesty_public": "SLOT",
            "browser_reachable": False,
            "aznet": True,
            "public_icann": False,
            "spec": CAP7_SHUFFLE_SPEC,
        },
    )


def public_gateway(label: str) -> dict[str, Any]:
    key = str(label or "").strip().lower()
    for site in CAP7_FACTORY_SITES:
        if site["label"] == key:
            row = site_record(site)
            if not row["browser_reachable"]:
                return refuse_slot_as_live(key)
            return _verdict(
                True,
                "CAP7-GATEWAY-LIVE",
                verdict=YES,
                message="browser-reachable Cap-7 public pair mirror on the app Worker (not ICANN .az)",
                extra={**row, "spec": CAP7_SHUFFLE_SPEC, "public_icann": False},
            )
    return refuse_public_dns_claim(kind="unknown-cap7-label")
