"""REDLINE-1.0 — smaller public door + attack simulations.

GET never enables radios or plants Cap-7 claims. AZ Generator is not
externally callable. AZ domain doors are the public internet path
(``public_icann: true``, ``resolves_to_hub: true``). Cap-7 is the
``.az`` duplication/shift layer and is not typed on ICANN DNS.
Public-door crypto is Cloudflare TLS only.
FoldLock is cite-only. Lamb Lens + NO-FAN. No invented completeness.

Author: Aziel Eliab only.
"""

from __future__ import annotations

from typing import Any, Mapping

from miragegrid.az_generator import (
    AzGenerator,
    DeepNode,
    PaperVault,
    node_gate_exit,
    refuse_call_generator,
    refuse_public_registrar,
    synthetic_papers,
)
from miragegrid.mesh import (
    CAP_7,
    MESH_LAW_AUTHOR,
    POOL_SIZE,
    REFUSE,
    _verdict,
    refuse_get_enable_or_plant,
    refuse_no_fan,
    refuse_radio_phy,
)
from miragegrid.semantic_bridge import (
    WORKER_HOST,
    build_bridge_registry,
    dead_named_worker,
    refuse_azg_icann_publish,
    refuse_public_dns_claim,
    semantic_bridge_dict,
    shelves_cite,
)

REDLINE_LAW = "REDLINE"
REDLINE_SPEC = "REDLINE-1.0"
FOLDLOCK_LAW = "FOLDLOCK"
FOLDLOCK_SLUG = "foldlock"
LAMB_LENS_LAW = "LAMB LENS"
PUBLIC_DOOR_CRYPTO = "cloudflare-tls"
# Invented 100% completeness is a NO-LIE refuse — not a score.
INVENT_COMPLETENESS = 100

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
        "completeness",
        "completeness-claim",
        "invent-completeness",
        "claim-complete",
        "radio-on",
    }
)

CALLABLE_AZG_ALIASES: tuple[str, ...] = (
    "/v1/az-generator",
    "/v1/call-generator",
    "/v1/run-generator",
    "/call-generator",
    "/v1/mesh/call-generator",
    "/v1/mesh/run-generator",
    "/v1/mesh/plant",
    "/v1/mesh/claim",
    "/v1/mesh/radio",
    "/v1/mesh/radios",
)

PUBLIC_MESH_GET_DOORS: tuple[str, ...] = (
    "/v1/mesh",
    "/v1/mesh/status",
    "/v1/mesh/nodes",
    "/v1/mesh/az-generator",
    "/v1/mesh/grid-shift",
)


def foldlock_cite() -> dict[str, Any]:
    """FoldLock is Language-domain tether-word suppression. Not Worker TLS."""
    return {
        "law": FOLDLOCK_LAW,
        "slug": FOLDLOCK_SLUG,
        "cite_only": True,
        "kind": "tether-word-suppression",
        "not_zip": True,
        "public_door_crypto": False,
        "theater_crypto": False,
        "softwares_tab_on_this_worker": False,
        "note": "FoldLock cite-only. Not zip. Not Cloudflare TLS. Not a MirageGrid door.",
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
    }


def lamb_lens_cite() -> dict[str, Any]:
    return {
        "law": LAMB_LENS_LAW,
        "ethical_research": True,
        "harvest": False,
        "node_gate": False,
        "no_fan": "NO-FAN-1.0",
        "completeness_claim": False,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
    }


def public_door_crypto_dict() -> dict[str, Any]:
    return {
        "layer": PUBLIC_DOOR_CRYPTO,
        "theater_crypto": False,
        "foldlock": "cite-only",
        "worker_encrypt": False,
        "local_onion": "chacha20-poly1305+x25519",
        "author": MESH_LAW_AUTHOR,
    }


def redline_dict() -> dict[str, Any]:
    return {
        "law": REDLINE_LAW,
        "spec": REDLINE_SPEC,
        "author": MESH_LAW_AUTHOR,
        "identity": MESH_LAW_AUTHOR,
        "get_never_enables": True,
        "get_never_plants": True,
        "hub_get_enables_mesh": False,
        "az_generator_callable": False,
        "public_icann": False,
        "resolves_to_hub": False,
        "public_door_crypto": public_door_crypto_dict(),
        "foldlock": foldlock_cite(),
        "lamb_lens": lamb_lens_cite(),
        "no_fan": "NO-FAN-1.0",
        "completeness_claim": False,
        "pool": POOL_SIZE,
        "cap": CAP_7,
        "public_host_pair": 2,
        "public_mesh_get_doors": list(PUBLIC_MESH_GET_DOORS),
        "callable_azg_aliases": list(CALLABLE_AZG_ALIASES),
        "smaller_door": True,
        "live_worker": WORKER_HOST,
        "app_worker": "https://miragegrid.vibelock.workers.dev",
        "dead_named_worker": dead_named_worker(),
        "shelves": shelves_cite(),
    }


def refuse_theater_crypto(
    *,
    layer: str | None = None,
    foldlock_as_crypto: bool = False,
    worker_encrypt: bool = False,
) -> dict[str, Any]:
    """Public door is Cloudflare TLS. FoldLock is cite-only. No theater crypto."""
    key = str(layer or "").strip().lower().replace("_", "-")
    if (
        foldlock_as_crypto
        or worker_encrypt
        or key in {"theater", "xor", "homemade", "foldlock-encrypt", "zip-crypto", "worker-encrypt"}
    ):
        return _verdict(
            False,
            "REDLINE-NO-THEATER-CRYPTO",
            verdict=REFUSE,
            message="public door is Cloudflare TLS only; FoldLock is cite-only; no theater crypto",
            extra={
                "public_door_crypto": PUBLIC_DOOR_CRYPTO,
                "foldlock": "cite-only",
                "theater_crypto": False,
                "kind": key or ("foldlock-encrypt" if foldlock_as_crypto else "theater"),
                "spec": REDLINE_SPEC,
            },
        )
    return _verdict(
        True,
        "REDLINE-TLS-OK",
        verdict="yes",
        message="Cloudflare TLS is the public-door encrypt layer",
        extra={"public_door_crypto": PUBLIC_DOOR_CRYPTO, "theater_crypto": False, "foldlock": foldlock_cite()},
    )


def refuse_completeness_claim(*, claimed: int | None = None, completeness: int | None = None) -> dict[str, Any]:
    """Refuse invented 100% completeness. Pool is 25. Cap-7 is 7. Public host pair is 2."""
    n = completeness if completeness is not None else claimed
    if n == INVENT_COMPLETENESS or claimed == INVENT_COMPLETENESS or completeness == INVENT_COMPLETENESS:
        return _verdict(
            False,
            "AZG-NO-COMPLETENESS-CLAIM",
            verdict=REFUSE,
            message="no invented completeness; pool is 25; Cap-7 is 7; public host pair is 2",
            extra={
                "completeness_claim": False,
                "pool": POOL_SIZE,
                "cap": CAP_7,
                "public_host_pair": 2,
                "claimed": n,
                "spec": REDLINE_SPEC,
                "no_fan": "NO-FAN-1.0",
            },
        )
    return _verdict(
        True,
        "AZG-COMPLETENESS-HONEST",
        verdict="yes",
        message="count is not an invented 100% completeness claim",
        extra={"completeness_claim": False, "pool": POOL_SIZE, "cap": CAP_7},
    )


def refuse_callable_alias(path: str | None = None) -> dict[str, Any]:
    """Any external run-generator / plant / radio alias is not a door."""
    raw = str(path or "").strip()
    key = raw.split("?")[0].rstrip("/") or "/"
    if not key.startswith("/"):
        key = "/" + key
    if key in CALLABLE_AZG_ALIASES or key.endswith("/call-generator") or key.endswith("/run-generator"):
        return refuse_call_generator(path=key)
    return refuse_call_generator(path=key or "external")


def _sim(name: str, row: Mapping[str, Any], expect: str) -> dict[str, Any]:
    code = str(row.get("code") or "")
    ok = code == expect and row.get("ok") is False
    return {
        "name": name,
        "ok": ok,
        "code": code,
        "expect": expect,
        "verdict": row.get("verdict"),
        "message": row.get("message"),
        "attack": name,
        "refuse": ok,
    }


def sim_callable_azg() -> dict[str, Any]:
    node = DeepNode("node-01", vault=PaperVault(synthetic_papers(49)))
    rows = [
        node.call_generator(),
        node.generator.call(),
        AzGenerator("node-02").call(),
        node_gate_exit(source="worker", action="run-generator"),
        refuse_callable_alias("/v1/mesh/call-generator"),
        refuse_call_generator(path="POST /v1/mesh/az-generator"),
    ]
    hit = next((r for r in rows if r.get("code") == "AZG-NOT-CALLABLE"), rows[0])
    out = _sim("callable-azg", hit, "AZG-NOT-CALLABLE")
    out["all_refused"] = all(r.get("code") == "AZG-NOT-CALLABLE" for r in rows)
    out["ok"] = bool(out["ok"] and out["all_refused"])
    return out


def sim_get_enable() -> dict[str, Any]:
    rows = [
        refuse_get_enable_or_plant(method="GET", path="/v1/mesh/enable"),
        refuse_get_enable_or_plant(method="GET", path="/v1/mesh", search="enable=1"),
        refuse_get_enable_or_plant(method="HEAD", path="/v1/mesh/enable"),
        refuse_get_enable_or_plant(method="GET", path="/v1/mesh/status", search="enabled=true"),
    ]
    hit = next((r for r in rows if r and r.get("code") == "MESH-GET-NO-ENABLE"), rows[0] or {})
    out = _sim("enable-via-get", hit, "MESH-GET-NO-ENABLE")
    out["all_refused"] = all(r is not None and r.get("code") == "MESH-GET-NO-ENABLE" for r in rows)
    out["ok"] = bool(out["ok"] and out["all_refused"])
    return out


def sim_get_radio_and_plant() -> dict[str, Any]:
    rows = [
        refuse_get_enable_or_plant(method="GET", path="/v1/mesh", search="radio=1"),
        refuse_get_enable_or_plant(method="GET", path="/v1/mesh/az-generator", search="plant=1"),
        refuse_get_enable_or_plant(method="GET", path="/v1/mesh/az-generator", search="claim=1"),
        refuse_get_enable_or_plant(method="GET", path="/v1/mesh/radio"),
        refuse_radio_phy(kind="wifi"),
    ]
    get_ok = all(r is not None and r.get("code") in {"MESH-GET-NO-ENABLE", "AZG-NO-RADIO-PHY"} for r in rows)
    hit = rows[0] or {}
    out = _sim("get-radio-plant", hit, "MESH-GET-NO-ENABLE")
    out["all_refused"] = get_ok
    out["ok"] = get_ok
    return out


def sim_fake_icann_publish() -> dict[str, Any]:
    rows = [
        refuse_public_registrar(kind="icann"),
        refuse_azg_icann_publish(),
        refuse_public_dns_claim(kind="az-public-dns"),
        build_bridge_registry([], icann_publish=True),
        build_bridge_registry([], cctld_purchase=True),
    ]
    hit = next((r for r in rows if r.get("code") in {"AZG-NOT-PUBLIC-REGISTRAR", "BRIDGE-NO-ICANN-PUBLISH", "BRIDGE-NO-PUBLIC-DNS"}), rows[0])
    out = _sim("fake-icann-publish", hit, str(hit.get("code") or ""))
    out["expect"] = "AZG-NOT-PUBLIC-REGISTRAR|BRIDGE-NO-ICANN-PUBLISH|BRIDGE-NO-PUBLIC-DNS"
    out["all_refused"] = all(
        r.get("ok") is False
        and r.get("code") in {"AZG-NOT-PUBLIC-REGISTRAR", "BRIDGE-NO-ICANN-PUBLISH", "BRIDGE-NO-PUBLIC-DNS"}
        for r in rows
    )
    out["ok"] = bool(out["all_refused"])
    return out


def sim_cap7_typed_on_icann() -> dict[str, Any]:
    from miragegrid.cap7_shuffle import refuse_cap7_typed_on_icann

    rows = [
        refuse_cap7_typed_on_icann(),
        build_bridge_registry([], typed_on_icann_dns=True),
        build_bridge_registry(
            [{"name": "azgrid.az", "public_icann": True, "design_of": "https://www.azieleliab.com/", "tip_sha256": "ab" * 32}]
        ),
    ]
    hit = next((r for r in rows if r.get("code") == "CAP7-NOT-ICANN-DNS"), rows[0])
    out = _sim("cap7-typed-on-icann", hit, "CAP7-NOT-ICANN-DNS")
    out["all_refused"] = all(r.get("code") == "CAP7-NOT-ICANN-DNS" and r.get("typed_on_icann_dns") is False for r in rows)
    out["ok"] = bool(out["ok"] and out["all_refused"])
    law = semantic_bridge_dict()
    out["cap7_typed_on_icann_dns"] = law.get("cap7_typed_on_icann_dns") is False
    out["internet_reaches"] = law.get("internet_reaches")
    out["ok"] = bool(out["ok"] and out["cap7_typed_on_icann_dns"] and out["internet_reaches"] == "az-domains")
    return out


def sim_theater_crypto() -> dict[str, Any]:
    rows = [
        refuse_theater_crypto(layer="xor"),
        refuse_theater_crypto(foldlock_as_crypto=True),
        refuse_theater_crypto(worker_encrypt=True),
    ]
    hit = rows[0]
    out = _sim("theater-crypto", hit, "REDLINE-NO-THEATER-CRYPTO")
    out["all_refused"] = all(r.get("code") == "REDLINE-NO-THEATER-CRYPTO" for r in rows)
    tls = refuse_theater_crypto(layer="cloudflare-tls")
    out["tls_ok"] = tls.get("code") == "REDLINE-TLS-OK"
    out["ok"] = bool(out["ok"] and out["all_refused"] and out["tls_ok"])
    return out


def sim_invent_completeness() -> dict[str, Any]:
    hit = refuse_completeness_claim(completeness=100)
    out = _sim("invent-completeness", hit, "AZG-NO-COMPLETENESS-CLAIM")
    fan = refuse_no_fan("false-live-nodes")
    out["no_fan"] = fan is not None and fan.get("code") == "NO-FAN-FALSIFY"
    out["ok"] = bool(out["ok"] and out["no_fan"])
    return out


def run_attack_sims() -> dict[str, Any]:
    """Operator FINAL SWEEP sims. All must REFUSE. Green = REDLINE-GREEN."""
    sims = [
        sim_callable_azg(),
        sim_get_enable(),
        sim_get_radio_and_plant(),
        sim_fake_icann_publish(),
        sim_cap7_typed_on_icann(),
        sim_theater_crypto(),
        sim_invent_completeness(),
    ]
    green = all(bool(s.get("ok")) and bool(s.get("refuse") or s.get("all_refused")) for s in sims)
    return _verdict(
        green,
        "REDLINE-GREEN" if green else "REDLINE-FAIL",
        verdict="yes" if green else REFUSE,
        message=(
            "redline + sims green; smaller door surface"
            if green
            else "one or more attack sims did not refuse"
        ),
        extra={
            "spec": REDLINE_SPEC,
            "sims": sims,
            "count": len(sims),
            "refused": sum(1 for s in sims if s.get("ok")),
            "public_icann": False,
            "cap7_typed_on_icann_dns": False,
            "internet_reaches": "az-domains",
            "resolves_to_hub": False,
            "callable": False,
            "get_never_enables": True,
            "completeness_claim": False,
            "public_door_crypto": PUBLIC_DOOR_CRYPTO,
            "foldlock": "cite-only",
            "lamb_lens": True,
            "no_fan": "NO-FAN-1.0",
            "smaller_door": True,
        },
    )
