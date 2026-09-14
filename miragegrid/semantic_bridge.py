"""SEMANTIC-BRIDGE-1.0 — AI discovery of Cap-7 names without faking ICANN DNS.

Public Plane-A hosts + the MirageGrid Worker publish machine maps.
Mesh names stay mesh-authoritative (public_icann:false). They inherit
hub *design* only. They do not resolve, redirect, or CNAME to the four
ICANN hubs.

Author: Aziel Eliab only. Person @id https://www.azieleliab.com/#aziel
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from miragegrid.az_generator import ACCESS_CLIENTS, PUBLIC_HOST_PAIR
from miragegrid.mesh import (
    AZ_TLD,
    AZIEL_TLD,
    CAP_7,
    FIRST_CLAIM_NAME,
    MESH_LAW_AUTHOR,
    REFUSE,
    YES,
    _verdict,
)

SEMANTIC_BRIDGE_LAW = "SEMANTIC BRIDGE"
SEMANTIC_BRIDGE_SPEC = "SEMANTIC-BRIDGE-1.0"
CROSS_NETWORK_SURVIVAL = "CROSS-NETWORK-SURVIVAL-1.0"
PERSON_ID = "https://www.azieleliab.com/#aziel"
WORKER_HOST = "https://miragegrid-download-tracker.vibelock.workers.dev"
AZ_GENERATOR_CITE = WORKER_HOST + "/v1/mesh/az-generator"
GROWTH = "Growth-ON"
REEXPAND = "archive-not-index"

DESIGN_HUBS: tuple[dict[str, Any], ...] = (
    {
        "design_of": "https://www.azieleliab.com/",
        "label": "azieleliab",
        "role": "design-provenance",
        "resolves_to_hub": False,
    },
    {
        "design_of": "https://www.azielcorpuslibrary.net/",
        "label": "azielcorpuslibrary",
        "designs": ["azcorpus", "azlibrary"],
        "role": "design-provenance",
        "resolves_to_hub": False,
    },
    {
        "design_of": "https://godlock.uk/",
        "label": "godlock",
        "role": "design-provenance",
        "resolves_to_hub": False,
    },
    {
        "design_of": "https://hedidntjump.com/",
        "label": "hedidntjump",
        "role": "design-provenance",
        "resolves_to_hub": False,
    },
)

HUB_HOSTS: frozenset[str] = frozenset(
    {
        "azieleliab.com",
        "www.azieleliab.com",
        "azielcorpuslibrary.net",
        "www.azielcorpuslibrary.net",
        "godlock.uk",
        "www.godlock.uk",
        "hedidntjump.com",
        "www.hedidntjump.com",
    }
)

_DESIGN_BY_HOST: dict[str, str] = {
    "azieleliab.com": "https://www.azieleliab.com/",
    "www.azieleliab.com": "https://www.azieleliab.com/",
    "azielcorpuslibrary.net": "https://www.azielcorpuslibrary.net/",
    "www.azielcorpuslibrary.net": "https://www.azielcorpuslibrary.net/",
    "godlock.uk": "https://godlock.uk/",
    "www.godlock.uk": "https://godlock.uk/",
    "hedidntjump.com": "https://hedidntjump.com/",
    "www.hedidntjump.com": "https://hedidntjump.com/",
}

ACCESS_VALUES: frozenset[str] = frozenset({"aznet", "azbrowser", "https-gateway"})


def person_id() -> dict[str, str]:
    return {"@id": PERSON_ID, "name": MESH_LAW_AUTHOR}


def semantic_bridge_dict() -> dict[str, Any]:
    return {
        "law": SEMANTIC_BRIDGE_LAW,
        "spec": SEMANTIC_BRIDGE_SPEC,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "person": person_id(),
        "growth": GROWTH,
        "public_icann": False,
        "registrar": False,
        "unbounded_public_dns": False,
        "cctld_takeover": False,
        "resolves_to_hub": False,
        "name_may_change": True,
        "reexpand": REEXPAND,
        "cross_network_survival": CROSS_NETWORK_SURVIVAL,
        "no_lie": True,
        "no_rewrite": True,
        "no_fan": "NO-FAN-1.0",
        "first_flag": FIRST_CLAIM_NAME,
        "suffix_order": [AZ_TLD, AZIEL_TLD, "pivot"],
        "public_host_pair": PUBLIC_HOST_PAIR,
        "cap": CAP_7,
        "az_generator_cite": AZ_GENERATOR_CITE,
        "access": {
            "aznet": True,
            "azbrowser": True,
            "merge": False,
            "naked_public_dns": False,
        },
        "design_catalog": [dict(row) for row in DESIGN_HUBS],
        "plane_a": [WORKER_HOST + "/"] + [row["design_of"] for row in DESIGN_HUBS],
        "softwares_tab": False,
        "callable": False,
    }


def cap7_bridge_cite() -> dict[str, Any]:
    """cite.json Cap-7 bridge section. Law stamps only — not a live name list."""
    return {
        "spec": SEMANTIC_BRIDGE_SPEC,
        "first_flag": FIRST_CLAIM_NAME,
        "suffix_order": [AZ_TLD, AZIEL_TLD, "pivot"],
        "public_host_pair": PUBLIC_HOST_PAIR,
        "public_icann": False,
        "access": {
            "aznet": True,
            "azbrowser": True,
            "merge": False,
            "naked_public_dns": False,
        },
        "aznet": True,
        "azbrowser": True,
        "cite": AZ_GENERATOR_CITE,
        "person": person_id(),
        "resolves_to_hub": False,
        "name_may_change": True,
        "growth": GROWTH,
        "cross_network_survival": CROSS_NETWORK_SURVIVAL,
        "no_lie": True,
    }


def refuse_public_dns_claim(*, kind: str = "az-public-dns") -> dict[str, Any]:
    return _verdict(
        False,
        "BRIDGE-NO-PUBLIC-DNS",
        verdict=REFUSE,
        message="mesh .az is not public ICANN DNS; do not claim public resolution",
        extra={
            "kind": kind,
            "public_icann": False,
            "spec": SEMANTIC_BRIDGE_SPEC,
            "no_lie": True,
        },
    )


def refuse_azg_icann_publish(*, kind: str = "azg-icann-publish") -> dict[str, Any]:
    return _verdict(
        False,
        "BRIDGE-NO-ICANN-PUBLISH",
        verdict=REFUSE,
        message="AZ Generator does not live-publish to ICANN; Worker cites only",
        extra={
            "kind": kind,
            "public_icann": False,
            "callable": False,
            "spec": SEMANTIC_BRIDGE_SPEC,
        },
    )


def refuse_hub_resolution(*, name: str = "", hub: str = "") -> dict[str, Any]:
    return _verdict(
        False,
        "BRIDGE-NO-HUB-RESOLVE",
        verdict=REFUSE,
        message="mesh names do not resolve, redirect, or CNAME to ICANN hubs; design_of is provenance only",
        extra={
            "name": name,
            "hub": hub,
            "resolves_to_hub": False,
            "public_icann": False,
            "spec": SEMANTIC_BRIDGE_SPEC,
        },
    )


def refuse_invent_first_flag_https(*, name: str = FIRST_CLAIM_NAME) -> dict[str, Any]:
    return _verdict(
        False,
        "BRIDGE-NO-INVENT-HTTPS",
        verdict=REFUSE,
        message="empty Cap-7: do not invent www.survivalnetwork.az as live HTTPS",
        extra={
            "name": name,
            "invented_first_flag_https": False,
            "honesty": "empty-cap-7",
            "spec": SEMANTIC_BRIDGE_SPEC,
            "no_lie": True,
        },
    )


def _host_of(value: Any) -> str:
    text = str(value or "").strip().lower()
    if text.startswith("https://"):
        text = text[8:]
    elif text.startswith("http://"):
        text = text[7:]
    return text.split("/")[0].split(":")[0].rstrip(".")


def _is_hub_host(value: Any) -> bool:
    return _host_of(value) in HUB_HOSTS


def normalize_design_of(value: Any) -> str | None:
    """Canonical hub URL for design provenance. None if not a known hub."""
    if value is None or value is False:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    host = _host_of(raw)
    if host in _DESIGN_BY_HOST:
        return _DESIGN_BY_HOST[host]
    for row in DESIGN_HUBS:
        if raw.rstrip("/") + "/" == row["design_of"] or raw == row["design_of"]:
            return row["design_of"]
        if raw.rstrip("/") == row["design_of"].rstrip("/"):
            return row["design_of"]
    return None


def _hex64(value: Any) -> str | None:
    text = str(value or "").strip().lower()
    if len(text) == 64 and all(c in "0123456789abcdef" for c in text):
        return text
    return None


def _as_claim(raw: Any) -> dict[str, Any] | None:
    if raw is None:
        return None
    if isinstance(raw, str):
        host = _host_of(raw)
        if not host:
            return None
        return {"name": host}
    if not isinstance(raw, Mapping):
        return None
    name = raw.get("name") or raw.get("host") or raw.get("mesh_name") or raw.get("url")
    host = _host_of(name)
    if not host:
        return None
    return {**dict(raw), "name": host}


def _access_for(claim: Mapping[str, Any], *, hosted_gateway: bool) -> str:
    requested = str(claim.get("access") or "").strip().lower().replace("_", "-")
    if hosted_gateway:
        return "https-gateway"
    if requested in ACCESS_VALUES and requested != "https-gateway":
        return requested
    return "aznet"


def _entry_from_claim(claim: Mapping[str, Any]) -> dict[str, Any]:
    host = str(claim.get("name") or "")
    if _is_hub_host(host):
        return refuse_hub_resolution(name=host, hub=host)
    if claim.get("resolves_to_hub") is True or claim.get("cname_to_hub") or claim.get("redirect_to_hub"):
        return refuse_hub_resolution(name=host, hub=str(claim.get("hub") or claim.get("design_of") or ""))
    gateway = claim.get("public_gateway_url") or claim.get("gateway_url")
    if gateway and _is_hub_host(gateway):
        return refuse_hub_resolution(name=host, hub=str(gateway))
    if claim.get("icann") is True or claim.get("public_icann") is True:
        return refuse_public_dns_claim(kind="claim-icann")

    design_of = normalize_design_of(claim.get("design_of"))
    if claim.get("design_of") and design_of is None and _is_hub_host(claim.get("design_of")):
        design_of = normalize_design_of(claim.get("design_of"))
    if claim.get("design_of") and design_of is None:
        # Unknown design_of is not a hub map; drop rather than invent.
        design_of = None

    public_host = bool(claim.get("public_host") or claim.get("plane") == "public-gateway")
    hosted = bool(gateway) and not _is_hub_host(gateway) and public_host
    if public_host and hosted:
        status = "https-gateway"
    elif public_host:
        status = "claimed-unhosted"
        gateway = None
    else:
        status = "mesh-only"
        gateway = None

    tip = _hex64(
        claim.get("tip_sha256")
        or claim.get("tip_hash")
        or claim.get("sha256")
        or ((claim.get("receipt") or {}) if isinstance(claim.get("receipt"), Mapping) else {}).get("hash")
    )
    pack = _hex64(claim.get("design_pack_sha256") or claim.get("design_pack") or claim.get("pack_sha256"))

    entry: dict[str, Any] = {
        "status": status,
        "access": _access_for(claim, hosted_gateway=hosted),
        "icann": False,
        "resolves_to_hub": False,
        "name_may_change": True,
    }
    if tip:
        entry["tip_sha256"] = tip
    if pack:
        entry["design_pack_sha256"] = pack
    if hosted and gateway:
        entry["public_gateway_url"] = str(gateway).strip()
    if design_of:
        entry["design_of"] = design_of
    return entry


def build_bridge_registry(
    claims: Iterable[Any] | None = None,
    *,
    zone: Any = None,
    invent_first_flag: bool = False,
    resolve_to_hub: bool = False,
    public_icann: bool = False,
    icann_publish: bool = False,
    public_dns: bool = False,
) -> dict[str, Any]:
    """Honest mesh_name → row map. Empty Cap-7 stays an empty SLOT list."""
    if public_icann or public_dns:
        return refuse_public_dns_claim(kind="registry-public-dns")
    if icann_publish:
        return refuse_azg_icann_publish()
    if resolve_to_hub:
        return refuse_hub_resolution()

    records: list[Any] = []
    if zone is not None:
        raw_records = getattr(zone, "records", None)
        if raw_records is None and hasattr(zone, "names"):
            raw_records = [{"name": n} for n in zone.names()]
        records.extend(list(raw_records or []))
    if claims is not None:
        records.extend(list(claims))

    names: dict[str, Any] = {}
    for raw in records:
        claim = _as_claim(raw)
        if not claim:
            continue
        row = _entry_from_claim(claim)
        if row.get("ok") is False:
            return row
        names[claim["name"]] = row

    if invent_first_flag and FIRST_CLAIM_NAME not in names:
        return refuse_invent_first_flag_https()

    # Honesty: first-flag is law, not a live HTTPS row when absent / unhosted.
    first = names.get(FIRST_CLAIM_NAME)
    invented_https = bool(
        first
        and first.get("status") == "https-gateway"
        and not first.get("public_gateway_url")
    )
    if invented_https:
        return refuse_invent_first_flag_https()

    honesty = "empty-cap-7" if not names else "claimed"
    return _verdict(
        True,
        "BRIDGE-EMPTY" if not names else "BRIDGE-OK",
        verdict=YES,
        message=(
            "empty Cap-7: SLOT empty list; first-flag is cited, not hosted HTTPS"
            if not names
            else "Cap-7 claims listed honestly; mesh-authoritative; not ICANN; design_of is provenance only"
        ),
        extra={
            "spec": SEMANTIC_BRIDGE_SPEC,
            "public_icann": False,
            "resolves_to_hub": False,
            "name_may_change": True,
            "honesty": honesty,
            "names": names,
            "slots": [],
            "claimed": len(names),
            "cap": CAP_7,
            "public_host_pair": PUBLIC_HOST_PAIR,
            "invented_first_flag_https": False,
            "first_flag": FIRST_CLAIM_NAME,
            "suffix_order": [AZ_TLD, AZIEL_TLD, "pivot"],
            "design_catalog": [dict(row) for row in DESIGN_HUBS],
            "person": person_id(),
            "cite": AZ_GENERATOR_CITE,
            "access": {
                "aznet": True,
                "azbrowser": True,
                "merge": False,
                "naked_public_dns": False,
            },
            "reexpand": REEXPAND,
            "growth": GROWTH,
            "cross_network_survival": CROSS_NETWORK_SURVIVAL,
            "no_lie": True,
            "no_rewrite": True,
        },
    )


def hosted_bridge_document() -> dict[str, Any]:
    """Worker default: no local Cap-7 claims. Honest empty SLOT list."""
    doc = build_bridge_registry([])
    doc.update(semantic_bridge_dict())
    doc["code"] = "BRIDGE-EMPTY"
    doc["honesty"] = "empty-cap-7"
    doc["names"] = {}
    doc["slots"] = []
    doc["claimed"] = 0
    doc["invented_first_flag_https"] = False
    return doc
