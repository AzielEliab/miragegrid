"""CAP7-SHUFFLE-1.0 — ping MirageGrid until land; land is the update door.

Cap-7 auto-generates ``.az`` duplications of the four hubs and shifts them
with StaticLock + MirageGrid cloak and VPN. Four factory names are real
hub duplications. Three are false sites (decoys). Cap-7 is not typed on
ICANN DNS and is not the public internet door.

Internet reaches AZ domains only, via the four hub websites. Those
drop-ins shuffle once, mirror the hubs while they are up, stand alone,
and stay immutable after the hubs die. Live nodes anchor both layers.
Factory honesty is LIVE (no SLOT hedge).

AZ Generator exits FRONT Node Gate only. radio_phy stays false.
Not an ICANN registrar purchase of a ccTLD.

Author: Aziel Eliab only.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Mapping

from miragegrid.az_generator import PUBLIC_HOST_PAIR, refuse_call_generator, refuse_public_registrar
from miragegrid.mesh import (
    CAP_7,
    MESH_LAW_AUTHOR,
    REFUSE,
    YES,
    _verdict,
    refuse_get_enable_or_plant,
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
    refuse_invent_first_flag_https,
    refuse_public_dns_claim,
)

CAP7_SHUFFLE_LAW = "CAP-7 LIVE SHUFFLE"
CAP7_SHUFFLE_SPEC = "CAP7-SHUFFLE-1.0"
DOWNLOAD_WORKER_HOST = WORKER_HOST
AZIEL_RUNTIME = "https://aziel-runtime.vibelock.workers.dev"
AZNET_PRODUCT = "aznet"
AZBROWSER_PRODUCT = "azbrowser"


def outlast_honesty() -> dict[str, Any]:
    """Factory honesty is LIVE. Cap-7 is not the public internet door.

    Hosted HTTP is not a packet VPN. The Cap-7 shift stack still cites
    StaticLock + MirageGrid cloak + MirageGrid VPN. Live nodes anchor
    the factory and the AZ domain doors.
    """
    return {
        "communication_plane": True,
        "channel_plane_is_vpn": False,
        "pairing_is_tunnel": False,
        "hosted_vpn": False,
        "packet_forwarding": False,
        "second_door": False,
        "open_proxy": False,
        "fraggate_single_door": True,
        "this_worker_is_node_gate": False,
        "node_gate_exit": "node-gate-front",
        "radio_phy": False,
        "factory_honesty": "LIVE",
        "hosted_endpoints": "LIVE",
        "hosted_update": "LIVE",
        "hosted_mcp": "LIVE",
        "public_shuffle_land_exec": "LIVE",
        "anchored_by_live_nodes": True,
        "domain_anchor": "live-nodes",
        "internet_reaches": "az-domains",
        "cap7_typed_on_icann_dns": False,
        "cap7_internet_reachable": False,
        "aznet_payload_host": False,
        "payload_host": "stub",
        "is_live_door": False,
        "public_hostname_resurrection": False,
        "hash_receipt": {
            "worker_session_hash": True,
            "second_receipt_door": False,
            "fraggate_slug": "miragegrid",
            "fraggate_ops": ["verify-receipt"],
            "aznet_verify": ["stamp", "verify_hash", "receipt_verify"],
            "door": "fraggate_call",
            "continuity": "aznet-verify-via-fraggate",
        },
    }


def refuse_vpn_lie() -> dict[str, Any]:
    return _verdict(
        False,
        "CAP7-NO-VPN-LIE",
        verdict=REFUSE,
        message="hosted Cap-7 is a communication/cite plane; not a VPN, tunnel, second FragGate door, or open proxy",
        extra=outlast_honesty(),
    )

HUB_AE = "https://www.azieleliab.com/"
HUB_CORPUS = "https://www.azielcorpuslibrary.net/"
HUB_GODLOCK = "https://godlock.uk/"
HUB_HDJ = "https://hedidntjump.com/"

# Public internet doors. Not Cap-7. Shuffle-once locked pairs.
# Mirror the hub while it is up; stand alone; immutable after the hub dies.
AZ_DOMAIN_DROP_INS: tuple[dict[str, str], ...] = (
    {
        "display_name": "AZ.AzielEliab.AZ",
        "mirror_host": "azieleliab.com",
        "canonical_hub": HUB_AE,
    },
    {
        "display_name": "AZ.AzielCorpusLibrary.AZ",
        "mirror_host": "azielcorpuslibrary.net",
        "canonical_hub": HUB_CORPUS,
    },
    {
        "display_name": "AZ.Godlock.AZ",
        "mirror_host": "godlock.uk",
        "canonical_hub": HUB_GODLOCK,
    },
    {
        "display_name": "AZ.HeDidntJump.AZ",
        "mirror_host": "hedidntjump.com",
        "canonical_hub": HUB_HDJ,
    },
)

# One real .az duplication per hub. The other three names are decoys.
REAL_HUB_DUPLICATIONS: tuple[str, ...] = ("azgrid", "azcloak", "azvault", "azshift")
FALSE_SITES: tuple[str, ...] = ("azbooth", "azflag", "azstandby")
SHIFT_STACK: tuple[str, ...] = ("staticlock", "miragegrid-cloak", "miragegrid-vpn")

# MirageGrid-only factory names. Not hub hostnames. Not azcorpus/azlibrary.
CAP7_FACTORY_SITES: tuple[dict[str, Any], ...] = (
    {
        "label": "azgrid",
        "role": "factory-grid",
        "design": "azieleliab software/runtime hub design DNA",
        "canonical_hub": HUB_AE,
        "design_of": HUB_AE,
    },
    {
        "label": "azbooth",
        "role": "factory-booth",
        "design": "azieleliab session-booth design DNA",
        "canonical_hub": HUB_AE,
        "design_of": HUB_AE,
    },
    {
        "label": "azcloak",
        "role": "factory-cloak",
        "design": "godlock cloak/dark design DNA",
        "canonical_hub": HUB_GODLOCK,
        "design_of": HUB_GODLOCK,
    },
    {
        "label": "azvault",
        "role": "factory-vault",
        "design": "corpus vault/shelf design DNA",
        "canonical_hub": HUB_CORPUS,
        "design_of": HUB_CORPUS,
    },
    {
        "label": "azshift",
        "role": "factory-shift",
        "design": "hedidntjump shift/standby design DNA",
        "canonical_hub": HUB_HDJ,
        "design_of": HUB_HDJ,
    },
    {
        "label": "azflag",
        "role": "factory-flag",
        "design": "corpus cite/flag design DNA",
        "canonical_hub": HUB_CORPUS,
        "design_of": HUB_CORPUS,
    },
    {
        "label": "azstandby",
        "role": "factory-standby",
        "design": "godlock standby/mask design DNA",
        "canonical_hub": HUB_GODLOCK,
        "design_of": HUB_GODLOCK,
    },
)

FACTORY_LABELS: tuple[str, ...] = tuple(site["label"] for site in CAP7_FACTORY_SITES)


def az_domain_for_hub(hub: str) -> dict[str, str] | None:
    target = str(hub or "").rstrip("/") + "/"
    for row in AZ_DOMAIN_DROP_INS:
        if row["canonical_hub"] == target or row["canonical_hub"] == hub:
            return row
    return None


def az_domain_rows() -> list[dict[str, Any]]:
    """Internet reaches these four names only, via hub HTTPS."""
    rows: list[dict[str, Any]] = []
    for row in AZ_DOMAIN_DROP_INS:
        rows.append(
            {
                "display_name": row["display_name"],
                "mirror_host": row["mirror_host"],
                "canonical_hub": row["canonical_hub"],
                "internet_url": row["canonical_hub"],
                "public_icann": True,
                "resolves_to_hub": True,
                "internet_reachable": True,
                "honesty": "LIVE",
                "shuffle_once": True,
                "pool": 4,
                "mirrors_while_up": True,
                "stands_alone": True,
                "immutable_after_hub_down": True,
                "anchored_by_live_nodes": True,
                "domain_anchor": "live-nodes",
                "softwares_tab": False,
                "cap7": False,
                "icann_registrar_purchase": False,
                "cctld_purchase": False,
                "author": MESH_LAW_AUTHOR,
            }
        )
    return rows


def _hex64(value: Any) -> str | None:
    text = str(value or "").strip().lower()
    return text if len(text) == 64 and all(c in "0123456789abcdef" for c in text) else None


def site_record(site: Mapping[str, Any]) -> dict[str, Any]:
    """Cap-7 factory row. LIVE duplication/shift layer. Not an ICANN door."""
    label = str(site["label"])
    real = label in REAL_HUB_DUPLICATIONS
    false_site = label in FALSE_SITES
    path = f"/cap7/{label}"
    drop = az_domain_for_hub(str(site["canonical_hub"]))
    return {
        "label": label,
        "mesh_name": f"{label}.az",
        "role": site["role"],
        "design": site["design"],
        "canonical_hub": site["canonical_hub"],
        "design_of": site["design_of"],
        "layer": "cap7-az-duplication",
        "generates": "auto-.az-hub-duplication",
        "hub_duplication": real,
        "false_site": false_site,
        "decoy": false_site,
        "resolves_to_hub": real,
        "name_may_change": True,
        "public_icann": False,
        "typed_on_icann_dns": False,
        "internet_reachable": False,
        "public_internet_door": False,
        "icann": False,
        "fifth_product": False,
        "radio_phy": False,
        "reach": "cap7-shift",
        "honesty_public": "LIVE",
        "factory_honesty": "LIVE",
        "browser_reachable": False,
        "aznet": True,
        "azbrowser": True,
        "merge": False,
        "worker_path": APP_WORKER_HOST + path,
        "aznet_endpoint": f"aznet://cap7/{label}",
        "update_path": APP_WORKER_HOST + "/v1/shuffle/update",
        "hosted_status": "LIVE",
        "hosted_update": "LIVE",
        "hosted_mcp": "LIVE",
        "public_shuffle_land_exec": "LIVE",
        "anchored_by_live_nodes": True,
        "domain_anchor": "live-nodes",
        "shift_stack": list(SHIFT_STACK),
        "staticlock": True,
        "miragegrid_cloak": True,
        "miragegrid_vpn": True,
        "internet_door": None if drop is None else drop["display_name"],
        "is_live_door": False,
        "aznet_payload_host": False,
        "channel_plane_is_vpn": False,
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
        "labels": list(FACTORY_LABELS),
        "sites": cap7_roster(),
        "real_hub_duplications": list(REAL_HUB_DUPLICATIONS),
        "false_sites": list(FALSE_SITES),
        "real_duplication_count": 4,
        "false_site_count": 3,
        "az_domains": az_domain_rows(),
        "internet_reaches": "az-domains",
        "typed_on_icann_dns": False,
        "internet_reachable": False,
        "name_may_change": True,
        "fifth_product": False,
        "radio_phy": False,
        "hardcoded_host": False,
        "update_is_proof": True,
        "shift_stack": list(SHIFT_STACK),
        "staticlock": True,
        "miragegrid_cloak": True,
        "miragegrid_vpn": True,
        "az_generator": {
            "callable": False,
            "lives": "deep-node",
            "exit": "node-gate-front",
            "radio_phy": False,
            "typed_on_icann_dns": False,
        },
        "access": {"aznet": True, "azbrowser": True, "merge": False, "naked_public_dns": False},
        "app_worker": app_worker(),
        "download_worker": download_worker(),
        "first_flag": FIRST_CLAIM_NAME,
        "invented_first_flag_https": False,
        "canonical_hubs": [row["canonical_hub"] for row in CANONICAL_HUBS],
        "named_mesh_designs": ["azcorpus", "azlibrary"],
        **outlast_honesty(),
        "note": "Cap-7 auto-generates .az duplications of the four hubs and shifts them with StaticLock + MirageGrid cloak and VPN. Four names are real hub duplications; three are false sites. Internet reaches AZ domains only, via hub HTTPS. Factory honesty is LIVE. Live nodes anchor the factory and the AZ doors. FragGate stays THE door.",
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
    typed_on_icann_dns: bool = False,
    cap7_on_icann: bool = False,
    icann_registrar_purchase: bool = False,
    cctld_purchase: bool = False,
    public_registrar: bool = False,
    hardcoded_host: str | None = None,
    invent_first_flag: bool = False,
    channel_plane_is_vpn: bool = False,
    hosted_vpn: bool = False,
    pairing_is_tunnel: bool = False,
    second_door: bool = False,
    open_proxy: bool = False,
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
        typed_on_icann_dns=typed_on_icann_dns,
        cap7_on_icann=cap7_on_icann,
        icann_registrar_purchase=icann_registrar_purchase,
        cctld_purchase=cctld_purchase,
        public_registrar=public_registrar,
        hardcoded_host=hardcoded_host,
        invent_first_flag=invent_first_flag,
        channel_plane_is_vpn=channel_plane_is_vpn,
        hosted_vpn=hosted_vpn,
        pairing_is_tunnel=pairing_is_tunnel,
        second_door=second_door,
        open_proxy=open_proxy,
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
            "resolves_to_hub": bool(site.get("resolves_to_hub")),
            "false_site": bool(site.get("false_site")),
            "hub_duplication": bool(site.get("hub_duplication")),
            "public_icann": False,
            "typed_on_icann_dns": False,
            "internet_reachable": False,
            "internet_reaches": "az-domains",
            "radio_phy": False,
            "hosted_update": "LIVE",
            "hosted_mcp": "LIVE",
            "public_shuffle_land_exec": "LIVE",
            "factory_honesty": "LIVE",
            "anchored_by_live_nodes": True,
            "is_live_door": False,
            "channel_plane_is_vpn": False,
            "second_door": False,
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
    typed_on_icann_dns: bool = False,
    cap7_on_icann: bool = False,
    icann_registrar_purchase: bool = False,
    cctld_purchase: bool = False,
    public_registrar: bool = False,
    hardcoded_host: str | None = None,
    invent_first_flag: bool = False,
    channel_plane_is_vpn: bool = False,
    hosted_vpn: bool = False,
    pairing_is_tunnel: bool = False,
    second_door: bool = False,
    open_proxy: bool = False,
    method: str = "POST",
) -> dict[str, Any]:
    """Node pings MirageGrid. Lands on one Cap-7 site when a seed is present."""
    method_u = str(method or "POST").upper()
    if method_u in {"GET", "HEAD"} and str(prev or "").strip() and str(lockset or "").strip():
        planted = refuse_get_enable_or_plant(
            method=method_u,
            path="/v1/shuffle/ping",
            search="prev=1&lockset=1",
        )
        if planted:
            return planted
    if inbound_call:
        return refuse_call_generator(path="cap7-shuffle-ping")
    if radio_phy:
        return refuse_radio_phy(kind="rf")
    if icann_registrar_purchase or cctld_purchase or public_registrar:
        return refuse_public_registrar(kind="cctld-purchase")
    if typed_on_icann_dns or cap7_on_icann:
        return refuse_cap7_typed_on_icann()
    if invent_first_flag:
        return refuse_invent_first_flag_https()
    if hardcoded_host:
        return refuse_hardcoded_host()
    if channel_plane_is_vpn or hosted_vpn or pairing_is_tunnel or second_door or open_proxy:
        return refuse_vpn_lie()
    fan = refuse_no_fan(None)
    if fan and fan.get("ok") is False:
        return fan

    seed = shuffle_seed(prev=prev, lockset=lockset, round_id=round_id)
    node = str(node_id or "").strip() or "anonymous"
    if node != "anonymous":
        if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", node):
            return _verdict(
                False,
                "CAP7-BAD-NODE-ID",
                verdict=REFUSE,
                message="node_id must be 1–80 [A-Za-z0-9._-]",
                extra={"spec": CAP7_SHUFFLE_SPEC},
            )
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
    update = method_u not in {"GET", "HEAD"} and bool(str(prev or "").strip() and str(lockset or "").strip())
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
            "typed_on_icann_dns": False,
            "internet_reachable": False,
            "internet_reaches": "az-domains",
            "resolves_to_hub": bool(site.get("resolves_to_hub")),
            "false_site": bool(site.get("false_site")),
            "hub_duplication": bool(site.get("hub_duplication")),
            "hosted_update": "LIVE",
            "hosted_mcp": "LIVE",
            "public_shuffle_land_exec": "LIVE",
            "factory_honesty": "LIVE",
            "anchored_by_live_nodes": True,
            "domain_anchor": "live-nodes",
            "is_live_door": False,
            "channel_plane_is_vpn": False,
            "second_door": False,
            "app_worker": app_worker(),
        },
    )


def shuffle_cite() -> dict[str, Any]:
    law = cap7_shuffle_dict()
    return _verdict(
        True,
        "CAP7-SHUFFLE-CITE",
        verdict=YES,
        message="CAP7-SHUFFLE-1.0 cite. Four real .az hub duplications, three false sites, StaticLock shift. Internet reaches AZ domains only.",
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
    """LIVE factory cite. Internet doors are the AZ domains, not Cap-7."""
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
        "typed_on_icann_dns": False,
        "internet_reachable": False,
        "internet_reaches": "az-domains",
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
        "real_hub_duplications": list(REAL_HUB_DUPLICATIONS),
        "false_sites": list(FALSE_SITES),
        "real_duplication_count": 4,
        "false_site_count": 3,
        "az_domains": az_domain_rows(),
        "shift_stack": list(SHIFT_STACK),
        "doors": cite["doors"],
        "first_flag": FIRST_CLAIM_NAME,
        "invented_first_flag_https": False,
        "honesty": {
            "app_worker": "LIVE",
            "download_worker": "LIVE",
            "factory": "LIVE",
            "az_domains": "LIVE",
            "cap7_icann_dns": False,
            "hosted_endpoints": "LIVE",
            "hosted_update": "LIVE",
            "hosted_mcp": "LIVE",
            "public_shuffle_land_exec": "LIVE",
            "anchored_by_live_nodes": True,
            "channel_plane_is_vpn": False,
            "second_door": False,
        },
        **outlast_honesty(),
        "az_generator": cite["az_generator"],
        "note": cite["note"],
    }


def refuse_cap7_typed_on_icann() -> dict[str, Any]:
    return _verdict(
        False,
        "CAP7-NOT-ICANN-DNS",
        verdict=REFUSE,
        message="Cap-7 is the .az duplication/shift/cloak layer; it is not publicly typed on ICANN DNS. Internet reaches AZ domains via the four hub websites.",
        extra={
            "typed_on_icann_dns": False,
            "internet_reachable": False,
            "internet_reaches": "az-domains",
            "az_domains": az_domain_rows(),
            "anchored_by_live_nodes": True,
            "factory_honesty": "LIVE",
            "icann_registrar_purchase": False,
            "spec": CAP7_SHUFFLE_SPEC,
        },
    )


def public_gateway(label: str) -> dict[str, Any]:
    key = str(label or "").strip().lower()
    for site in CAP7_FACTORY_SITES:
        if site["label"] == key:
            row = site_record(site)
            return _verdict(
                True,
                "CAP7-FACTORY-LIVE",
                verdict=YES,
                message="LIVE Cap-7 factory site (duplication/shift/cloak). Not an ICANN public door. Internet reaches AZ domains via hub HTTPS.",
                extra={
                    **row,
                    "spec": CAP7_SHUFFLE_SPEC,
                    "az_domains": az_domain_rows(),
                },
            )
    return refuse_public_dns_claim(kind="unknown-cap7-label")
