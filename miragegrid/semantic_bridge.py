"""SEMANTIC-BRIDGE-1.0 — AI discovery of Cap-7 names without faking ICANN DNS.

Public Plane-A hosts + the MirageGrid Worker publish machine maps.
Mesh names are relocatable claim labels (name_may_change). They are
not a fifth public product. The four online hubs stay canonical.
azcorpus and azlibrary are designs inside azielcorpuslibrary.net.

Author: Aziel Eliab only. Person @id https://www.azieleliab.com/#aziel
"""

from __future__ import annotations

import hashlib
import json
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
DEAD_NAMED_WORKER = "https://miragegrid.vibelock.workers.dev"
CORPUS_SHELVES = "https://www.azielcorpuslibrary.net/shelves"
AZ_GENERATOR_CITE = WORKER_HOST + "/v1/mesh/az-generator"
GROWTH = "Growth-ON"
REEXPAND = "archive-not-index"
PREFERRED_PUBLIC_PAIR: tuple[str, ...] = ("azcorpus", "azlibrary")

CANONICAL_HUBS: tuple[dict[str, Any], ...] = (
    {
        "canonical_hub": "https://www.azieleliab.com/",
        "label": "azieleliab",
        "role": "canonical-hub",
        "fifth_product": False,
    },
    {
        "canonical_hub": "https://www.azielcorpuslibrary.net/",
        "label": "azielcorpuslibrary",
        "designs": ["azcorpus", "azlibrary"],
        "role": "canonical-hub",
        "fifth_product": False,
    },
    {
        "canonical_hub": "https://godlock.uk/",
        "label": "godlock",
        "role": "canonical-hub",
        "fifth_product": False,
    },
    {
        "canonical_hub": "https://hedidntjump.com/",
        "label": "hedidntjump",
        "role": "canonical-hub",
        "fifth_product": False,
    },
)

DESIGN_HUBS = CANONICAL_HUBS

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

CORPUS_HUB = "https://www.azielcorpuslibrary.net/"

NAMED_MESH_SITES: tuple[dict[str, Any], ...] = (
    {
        "label": "azcorpus",
        "role": "public-corpus-shelf",
        "design": "public Corpus shelf site design",
        "canonical_hub": CORPUS_HUB,
        "design_of": CORPUS_HUB,
        "download_open": True,
        "upload_auth": "none",
        "preferred_public_pair": True,
        "fifth_product": False,
    },
    {
        "label": "azlibrary",
        "role": "aziel-library",
        "design": "Aziel Library site design",
        "canonical_hub": CORPUS_HUB,
        "design_of": CORPUS_HUB,
        "download_open": True,
        "upload_auth": "token",
        "upload_plane": "plane-a",
        "preferred_public_pair": True,
        "fifth_product": False,
    },
)

ACCESS_VALUES: frozenset[str] = frozenset({"aznet", "azbrowser", "https-gateway"})


def person_id() -> dict[str, str]:
    return {"@id": PERSON_ID, "name": MESH_LAW_AUTHOR}


def honest_mesh_name(label: str, suffix: str = AZ_TLD) -> str:
    host = str(label or "").strip().lower().split(".")[0]
    suf = str(suffix or AZ_TLD).strip().lower()
    if not suf.startswith("."):
        suf = "." + suf
    return host + suf


def preferred_public_pair_label(name: str) -> str | None:
    host = str(name or "").strip().lower().split("/")[0]
    for label in PREFERRED_PUBLIC_PAIR:
        if host == label or host.startswith(label + "."):
            return label
    return None


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def design_pack_body(label: str) -> dict[str, Any] | None:
    for site in NAMED_MESH_SITES:
        if site["label"] == label:
            pack = {
                "kind": "azg-design-pack",
                "spec": SEMANTIC_BRIDGE_SPEC,
                "label": site["label"],
                "role": site["role"],
                "design": site["design"],
                "canonical_hub": site["canonical_hub"],
                "design_of": site["design_of"],
                "public_icann": False,
                "download_open": site["download_open"],
                "upload_auth": site["upload_auth"],
                "fifth_product": False,
                "plane": "pull-only",
                "author": MESH_LAW_AUTHOR,
            }
            if site.get("upload_plane"):
                pack["upload_plane"] = site["upload_plane"]
            return pack
    return None


def design_pack_bytes(label: str) -> bytes | None:
    body = design_pack_body(label)
    if body is None:
        return None
    return canonical_json(body).encode("utf-8")


def design_pack_sha256(label: str) -> str | None:
    blob = design_pack_bytes(label)
    if blob is None:
        return None
    return hashlib.sha256(blob).hexdigest()


def design_pack_url(label: str) -> str:
    return WORKER_HOST + "/design-packs/" + label + ".json"


def named_mesh_entry(site: Mapping[str, Any], *, suffix: str = AZ_TLD) -> dict[str, Any]:
    label = str(site["label"])
    digest = design_pack_sha256(label)
    entry = {
        "status": "named-mesh-site",
        "label": label,
        "role": site["role"],
        "design": site["design"],
        "mesh_name": honest_mesh_name(label, suffix),
        "suffix": suffix if str(suffix).startswith(".") else "." + str(suffix),
        "suffix_order": [AZ_TLD, AZIEL_TLD, "pivot"],
        "name_may_change": True,
        "canonical_hub": site["canonical_hub"],
        "design_of": site["design_of"],
        "resolves_to_hub": False,
        "public_icann": False,
        "icann": False,
        "download_open": bool(site["download_open"]),
        "upload_auth": site["upload_auth"],
        "preferred_public_pair": True,
        "fifth_product": False,
        "access": {"aznet": True, "azbrowser": True, "merge": False, "naked_public_dns": False},
        "design_pack": {
            "url": design_pack_url(label),
            "sha256": digest,
            "download_open": True,
            "plane": "pull-only",
        },
        "tip": digest,
        "tip_sha256": digest,
        "person": person_id(),
    }
    if site.get("upload_plane"):
        entry["upload_plane"] = site["upload_plane"]
    return entry


def design_pack_index() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for site in NAMED_MESH_SITES:
        label = str(site["label"])
        out[label] = {
            "url": design_pack_url(label),
            "sha256": design_pack_sha256(label),
            "download_open": True,
            "canonical_hub": site["canonical_hub"],
            "plane": "pull-only",
        }
    return out


def named_mesh_sites(*, suffix: str = AZ_TLD) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for site in NAMED_MESH_SITES:
        entry = named_mesh_entry(site, suffix=suffix)
        out[entry["mesh_name"]] = entry
    return out


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
        "preferred_public_pair": list(PREFERRED_PUBLIC_PAIR),
        "cap": CAP_7,
        "az_generator_cite": AZ_GENERATOR_CITE,
        "access": {
            "aznet": True,
            "azbrowser": True,
            "merge": False,
            "naked_public_dns": False,
        },
        "canonical_hubs": [dict(row) for row in CANONICAL_HUBS],
        "design_catalog": [dict(row) for row in CANONICAL_HUBS],
        "named_mesh_sites": [dict(row) for row in NAMED_MESH_SITES],
        "design_packs": design_pack_index(),
        "fifth_product": False,
        "plane_a": [WORKER_HOST + "/"] + [row["canonical_hub"] for row in CANONICAL_HUBS],
        "softwares_tab": False,
        "callable": False,
        "design_of": cap7_design_of_map(),
        "live_worker": WORKER_HOST,
        "dead_named_worker": dead_named_worker(),
        "shelves": CORPUS_SHELVES,
    }


def cap7_design_of_map() -> dict[str, str]:
    """Preferred public pair inherit corpus design. Provenance only."""
    return {label: CORPUS_HUB for label in PREFERRED_PUBLIC_PAIR}


def cap7_designs() -> list[dict[str, Any]]:
    return [
        {
            "label": site["label"],
            "design_of": site["design_of"],
            "canonical_hub": site["canonical_hub"],
            "resolves_to_hub": False,
            "public_icann": False,
            "name_may_change": True,
            "fifth_product": False,
        }
        for site in NAMED_MESH_SITES
    ]


def dead_named_worker() -> dict[str, Any]:
    """miragegrid.vibelock.workers.dev is CF 1042. Do not cite as live."""
    return {
        "url": DEAD_NAMED_WORKER,
        "host": "miragegrid.vibelock.workers.dev",
        "status": "cf-1042",
        "http": 404,
        "cite": False,
        "live": WORKER_HOST,
        "note": "Named worker is not deployed (Cloudflare error 1042). Live cite is miragegrid-download-tracker.vibelock.workers.dev.",
    }


def shelves_cite() -> dict[str, Any]:
    """Honest /shelves pointer. Corpus is canonical. Framagit URL is not invented."""
    return {
        "ok": True,
        "code": "SHELVES-CITE",
        "spec": "COLD-MULTI-SHELF-1.0",
        "kind": "cite-pointer",
        "this_worker_is_not_a_shelf": True,
        "canonical": CORPUS_SHELVES,
        "canonical_hub": CORPUS_HUB,
        "design_of": CORPUS_HUB,
        "resolves_to_hub": False,
        "public_icann": False,
        "framagit": None,
        "framagit_url": None,
        "invented_framagit": False,
        "plane_b_framagit": "awaiting-tip-pack",
        "live_worker": WORKER_HOST,
        "dead_named_worker": dead_named_worker(),
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "note": "Corpus shelves live on azielcorpuslibrary.net. This Worker cites that canonical. Framagit URL is not published — do not invent one.",
    }


def cap7_bridge_cite() -> dict[str, Any]:
    """cite.json Cap-7 bridge section. Law stamps only — not a live ICANN list."""
    return {
        "spec": SEMANTIC_BRIDGE_SPEC,
        "first_flag": FIRST_CLAIM_NAME,
        "suffix_order": [AZ_TLD, AZIEL_TLD, "pivot"],
        "public_host_pair": PUBLIC_HOST_PAIR,
        "preferred_public_pair": list(PREFERRED_PUBLIC_PAIR),
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
        "canonical_hubs": [row["canonical_hub"] for row in CANONICAL_HUBS],
        "named_mesh_sites": list(PREFERRED_PUBLIC_PAIR),
        "design_of": cap7_design_of_map(),
        "designs": cap7_designs(),
        "fifth_product": False,
        "growth": GROWTH,
        "cross_network_survival": CROSS_NETWORK_SURVIVAL,
        "no_lie": True,
        "live_worker": WORKER_HOST,
        "dead_named_worker": dead_named_worker(),
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
        message="mesh names do not resolve, redirect, or CNAME to ICANN hubs; canonical_hub is provenance only",
        extra={
            "name": name,
            "hub": hub,
            "resolves_to_hub": False,
            "public_icann": False,
            "spec": SEMANTIC_BRIDGE_SPEC,
        },
    )


def refuse_fifth_product(*, name: str = "") -> dict[str, Any]:
    return _verdict(
        False,
        "BRIDGE-NO-FIFTH-PRODUCT",
        verdict=REFUSE,
        message="mesh name is a relocatable label of the four online hubs; not a fifth public product",
        extra={
            "name": name,
            "fifth_product": False,
            "canonical_hubs": [row["canonical_hub"] for row in CANONICAL_HUBS],
            "public_icann": False,
            "spec": SEMANTIC_BRIDGE_SPEC,
            "no_lie": True,
        },
    )


def refuse_need_canonical_hub(*, name: str = "") -> dict[str, Any]:
    return _verdict(
        False,
        "BRIDGE-NEED-CANONICAL-HUB",
        verdict=REFUSE,
        message="each mesh entry must cite one of the four hubs as canonical_hub; do not invent a fifth product",
        extra={
            "name": name,
            "canonical_hubs": [row["canonical_hub"] for row in CANONICAL_HUBS],
            "fifth_product": False,
            "public_icann": False,
            "spec": SEMANTIC_BRIDGE_SPEC,
            "no_lie": True,
        },
    )


def refuse_need_tip(*, name: str = "") -> dict[str, Any]:
    return _verdict(
        False,
        "BRIDGE-NEED-TIP",
        verdict=REFUSE,
        message="each mesh entry needs a real tip sha256; do not invent one",
        extra={
            "name": name,
            "public_icann": False,
            "spec": SEMANTIC_BRIDGE_SPEC,
            "no_lie": True,
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
    for row in CANONICAL_HUBS:
        hub = row["canonical_hub"]
        if raw.rstrip("/") + "/" == hub or raw == hub or raw.rstrip("/") == hub.rstrip("/"):
            return hub
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
        return refuse_hub_resolution(name=host, hub=str(claim.get("hub") or claim.get("canonical_hub") or claim.get("design_of") or ""))
    gateway = claim.get("public_gateway_url") or claim.get("gateway_url")
    if gateway and _is_hub_host(gateway):
        return refuse_hub_resolution(name=host, hub=str(gateway))
    if claim.get("icann") is True or claim.get("public_icann") is True:
        return refuse_public_dns_claim(kind="claim-icann")
    if claim.get("fifth_product") is True:
        return refuse_fifth_product(name=host)

    design_of = normalize_design_of(claim.get("design_of") or claim.get("canonical_hub"))
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
    if isinstance(claim.get("design_pack"), Mapping):
        pack = _hex64(claim["design_pack"].get("sha256")) or pack

    entry: dict[str, Any] = {
        "status": status,
        "access": _access_for(claim, hosted_gateway=hosted),
        "icann": False,
        "public_icann": False,
        "resolves_to_hub": False,
        "name_may_change": True,
        "fifth_product": False,
    }
    if tip:
        entry["tip_sha256"] = tip
    if pack:
        entry["design_pack_sha256"] = pack
    if hosted and gateway:
        entry["public_gateway_url"] = str(gateway).strip()
    if design_of:
        entry["design_of"] = design_of
        entry["canonical_hub"] = design_of
    label = preferred_public_pair_label(host)
    if label:
        site = next(s for s in NAMED_MESH_SITES if s["label"] == label)
        entry["label"] = label
        entry["canonical_hub"] = site["canonical_hub"]
        entry["design_of"] = site["design_of"]
        entry["download_open"] = site["download_open"]
        entry["upload_auth"] = site["upload_auth"]
        entry["preferred_public_pair"] = True
        entry["design_pack"] = {
            "url": design_pack_url(label),
            "sha256": design_pack_sha256(label),
            "download_open": True,
            "plane": "pull-only",
        }
        if not tip:
            entry["tip_sha256"] = design_pack_sha256(label)
        if site.get("upload_plane"):
            entry["upload_plane"] = site["upload_plane"]
    if not entry.get("canonical_hub"):
        return refuse_need_canonical_hub(name=host)
    if not entry.get("tip_sha256"):
        return refuse_need_tip(name=host)
    entry["tip"] = entry["tip_sha256"]
    entry["mesh_name"] = host
    entry["person"] = person_id()
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
    suffix: str = AZ_TLD,
    include_named_sites: bool = True,
) -> dict[str, Any]:
    """Named mesh sites always listed. Empty Cap-7 claims stay an empty SLOT list."""
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

    names: dict[str, Any] = named_mesh_sites(suffix=suffix) if include_named_sites else {}
    claimed_names: dict[str, Any] = {}
    for raw in records:
        claim = _as_claim(raw)
        if not claim:
            continue
        row = _entry_from_claim(claim)
        if row.get("ok") is False:
            return row
        claimed_names[claim["name"]] = row
        names[claim["name"]] = row

    if invent_first_flag and FIRST_CLAIM_NAME not in claimed_names:
        return refuse_invent_first_flag_https()

    first = claimed_names.get(FIRST_CLAIM_NAME)
    invented_https = bool(
        first
        and first.get("status") == "https-gateway"
        and not first.get("public_gateway_url")
    )
    if invented_https:
        return refuse_invent_first_flag_https()

    empty_claims = not claimed_names
    honesty = "empty-cap-7" if empty_claims else "claimed"
    return _verdict(
        True,
        "BRIDGE-EMPTY" if empty_claims else "BRIDGE-OK",
        verdict=YES,
        message=(
            "empty Cap-7 SLOT; named mesh sites azcorpus+azlibrary cited as designs, not live ICANN"
            if empty_claims
            else "Cap-7 claims listed honestly; named mesh sites stay designs of the four hubs"
        ),
        extra={
            "spec": SEMANTIC_BRIDGE_SPEC,
            "public_icann": False,
            "resolves_to_hub": False,
            "name_may_change": True,
            "honesty": honesty,
            "names": names,
            "slots": [],
            "claimed": len(claimed_names),
            "cap": CAP_7,
            "public_host_pair": PUBLIC_HOST_PAIR,
            "preferred_public_pair": list(PREFERRED_PUBLIC_PAIR),
            "invented_first_flag_https": False,
            "first_flag": FIRST_CLAIM_NAME,
            "suffix_order": [AZ_TLD, AZIEL_TLD, "pivot"],
            "canonical_hubs": [dict(row) for row in CANONICAL_HUBS],
            "design_catalog": [dict(row) for row in CANONICAL_HUBS],
            "named_mesh_sites": [dict(row) for row in NAMED_MESH_SITES],
            "design_packs": design_pack_index(),
            "fifth_product": False,
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
    """Worker default: named mesh sites listed; Cap-7 claims remain SLOT empty."""
    doc = build_bridge_registry([])
    law = semantic_bridge_dict()
    out = {**law, **doc}
    out["code"] = "BRIDGE-EMPTY"
    out["honesty"] = "empty-cap-7"
    out["slots"] = []
    out["claimed"] = 0
    out["invented_first_flag_https"] = False
    out["names"] = named_mesh_sites()
    return out
