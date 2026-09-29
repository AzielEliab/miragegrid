"""AZNet pairing for Cap-7 mesh DNS.

Naming lock: sidenet = AZNet. Sidenet is not a second product and not a
second plane. Cap-7 mesh DNS pairs with AZNet and AZBrowser. Softwares
stay frozen. ``public_icann`` stays false.

L0, the public path, stays as it is: AZ-domain doors, hub HTTPS, and the
existing Cap-7 shuffle cite. This module does not rewrite those responses
and it does not run the AZNet engine (garden, stamp, memorial). FragGate
remains that door.

MirageGrid remains the Cap-7 mesh DNS factory. It is not an ICANN
registrar. AZ Generator is not callable from outside
(``AZG-NOT-CALLABLE``). Exactly two Cap-7 factory labels are public
browser gateways (``azgrid``, ``azbooth``). Every other mesh name needs
an AZNet pairing token and an ``azbrowser`` flag. Pairing is order/token.
It is not a tunnel and it does not host payloads. This surface does not
verify the token at AZNet.

Author: Aziel Eliab only.
"""

from __future__ import annotations

from typing import Any, Mapping

from miragegrid.az_generator import (
    ACCESS_CLIENTS,
    PUBLIC_BROWSER_CLIENTS,
    PUBLIC_HOST_PAIR,
    PaperVault,
    attempt_claim,
    refuse_call_generator,
    refuse_icann_tld,
    refuse_naked_dns,
    refuse_product_merge,
    refuse_public_registrar,
)
from miragegrid.cap7_shuffle import FACTORY_LABELS
from miragegrid.mesh import (
    MESH_LAW_AUTHOR,
    REFUSE,
    YES,
    _verdict,
    plant_flag_and_repost,
    refuse_falsify,
    restore_chain,
)

AZN_SPEC = "AZN-CAP7-PAIR"
AZN_NAME = "AZNet"
AZN_SLUG = "aznet"
NAMING_LOCK = "sidenet=AZNet"
AZN_LAYER = "P2"
L0_PLANE = "public-path"
PUBLIC_BROWSER_GATEWAYS: tuple[str, ...] = ("azgrid", "azbooth")
NODE_GATE_ACTIONS: frozenset[str] = frozenset({"claim", "plant", "flag", "restore"})
_BOOL_WORDS: frozenset[str] = frozenset({"true", "false", "1", "0", "yes", "no", "on", "off"})
_HUB_HOSTS: frozenset[str] = frozenset(
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


def _stamp(out: dict[str, Any]) -> dict[str, Any]:
    out["layer"] = AZN_LAYER
    out["spec"] = AZN_SPEC
    out["aznet_name"] = AZN_NAME
    out["slug"] = AZN_SLUG
    out["naming_lock"] = NAMING_LOCK
    out["sidenet"] = AZN_NAME
    out["pairs_with"] = [AZN_NAME, "AZBrowser"]
    if not out.get("name"):
        out["name"] = AZN_NAME
    if "plane" not in out:
        out["plane"] = AZN_SLUG
    out["l0_public_path_changed"] = False
    out["public_icann"] = False
    out["softwares_frozen"] = True
    out["new_product"] = False
    out["this_route_adds_software"] = False
    out["merge"] = False
    out["pairing_is_tunnel"] = False
    out["second_door"] = False
    out["callable"] = False
    return out


def sidenet_dict() -> dict[str, Any]:
    """Cite AZNet pairing. L0 AZ-domain doors stay public_icann true."""
    return _stamp(
        {
            "ok": True,
            "code": "AZN-CAP7-CITE",
            "verdict": YES,
            "yes": True,
            "author": MESH_LAW_AUTHOR,
            "identity": MESH_LAW_AUTHOR,
            "l0": {
                "changed": False,
                "plane": L0_PLANE,
                "internet_reaches": "az-domains",
                "az_domains_public_icann": True,
                "note": "AZ-domain doors and existing public routes stay as they are.",
            },
            "p2": {
                "name": AZN_NAME,
                "plane": AZN_SLUG,
                "naming_lock": NAMING_LOCK,
                "public_icann": False,
                "dns_factory": "cap-7-mesh-authoritative",
                "callable": False,
                "exit": "node-gate-front",
                "public_browser_gateways": list(PUBLIC_BROWSER_GATEWAYS),
                "public_host_pair": PUBLIC_HOST_PAIR,
                "runs_aznet_engine": False,
            },
            "dns_factory": "cap-7-mesh-authoritative",
            "lives": "deep-node",
            "exit": "node-gate-front",
            "public_browser_gateways": list(PUBLIC_BROWSER_GATEWAYS),
            "public_host_pair": PUBLIC_HOST_PAIR,
            "cap": 7,
            "access": {
                "aznet": True,
                "azbrowser": True,
                "merge": False,
                "pairing_only": True,
                "pairing_is_tunnel": False,
                "pair_token_and_azbrowser_flag": True,
                "pair_verified_at_aznet": False,
                "this_surface_verifies_aznet_token": False,
                "hosts_payloads": False,
            },
            "node_gate_actions": sorted(NODE_GATE_ACTIONS),
            "hosted_node_gate_exec": False,
            "fifth_product": False,
            "radio_phy": False,
            "aznet_payload_host": False,
            "runs_aznet_engine": False,
            "note": (
                "Naming lock: sidenet = AZNet. Cap-7 mesh DNS pairs with AZNet and AZBrowser. "
                "Not ICANN. Exactly 2 public browser gateways (azgrid, azbooth). "
                "Other mesh names need an AZNet pairing token and an azbrowser flag. "
                "This surface does not verify that token and does not run the AZNet engine. "
                "Softwares stay frozen. L0 public path is unchanged."
            ),
        }
    )


def _host(name: str | None) -> str:
    return str(name or "").strip().lower().split("/")[0].rstrip(".")


def factory_label(name: str | None) -> str | None:
    host = _host(name)
    if host.endswith(".az"):
        host = host[: -len(".az")]
    if host in FACTORY_LABELS:
        return host
    return None


def is_public_browser_gateway(name: str | None) -> bool:
    label = factory_label(name)
    return label in PUBLIC_BROWSER_GATEWAYS


def _pair_token(body: Mapping[str, Any]) -> str:
    raw = body.get("pair_token", body.get("pairing_token", body.get("token")))
    text = str(raw or "").strip()
    if text.lower() in _BOOL_WORDS:
        return ""
    return text


def _azbrowser_flag(body: Mapping[str, Any]) -> bool:
    for key in ("azbrowser_flag", "flag", "pair_peer"):
        if str(body.get(key) or "").strip().lower() == "azbrowser":
            return True
    return False


def _client(body: Mapping[str, Any]) -> str:
    return str(body.get("client") or "").strip().lower().replace("_", "-")


def sidenet_access(body: Mapping[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
    """Admit a mesh name on P2, or refuse with an honest stamp.

    Standard browsers reach only the two public browser gateways.
    AZNet and AZBrowser reach mesh names only when a pairing token and an
    azbrowser flag are both present. Presence is not AZNet verification.
    """
    fields: dict[str, Any] = dict(body or {})
    fields.update(kwargs)
    if fields.get("softwares_tab") or fields.get("new_product") or fields.get("fifth_product"):
        return _stamp(
            _verdict(
                False,
                "AZN-SOFTWARE-FROZEN",
                verdict=REFUSE,
                message="Softwares stay frozen. sidenet is the name AZNet. This route does not add a product.",
                extra={"new_product": False, "fifth_product": False, "merge": False},
            )
        )
    if fields.get("public_icann") or fields.get("cctld_takeover") or fields.get("registrar"):
        return _stamp(refuse_public_registrar(kind="aznet"))
    if fields.get("merge") or fields.get("merge_products"):
        return _stamp(refuse_product_merge())
    if fields.get("hosts_payloads") or fields.get("aznet_payload_host") or fields.get("payload_host"):
        return _stamp(
            _verdict(
                False,
                "AZN-NO-PAYLOAD-HOST",
                verdict=REFUSE,
                message="AZNet pairing does not host payloads",
                extra={"hosts_payloads": False, "aznet_payload_host": False},
            )
        )
    if (
        fields.get("pairing_is_tunnel")
        or fields.get("channel_plane_is_vpn")
        or fields.get("hosted_vpn")
        or fields.get("second_door")
        or fields.get("open_proxy")
    ):
        return _stamp(
            _verdict(
                False,
                "CAP7-NO-VPN-LIE",
                verdict=REFUSE,
                message="pairing is not a tunnel; the channel plane is not a VPN; FragGate stays the only door",
                extra={
                    "channel_plane_is_vpn": False,
                    "hosted_vpn": False,
                    "open_proxy": False,
                    "hosts_payloads": False,
                },
            )
        )
    if fields.get("pair_verified_at_aznet") or fields.get("aznet_verified"):
        return _stamp(
            _verdict(
                False,
                "AZN-NO-VERIFIED-LIE",
                verdict=REFUSE,
                message="this surface does not verify pairing tokens at AZNet; do not stamp verification",
                extra={
                    "pair_verified_at_aznet": False,
                    "this_surface_verifies_aznet_token": False,
                    "pair_check": "refused-unverified-claim",
                },
            )
        )
    if fields.get("naked_dns"):
        return _stamp(refuse_naked_dns())

    host = _host(fields.get("name") or fields.get("label"))
    if host in _HUB_HOSTS:
        return _stamp(
            _verdict(
                False,
                "MGS-NOT-NODE-GATE",
                verdict=REFUSE,
                message="official hubs stay on the L0 public path; they are not AZNet Node Gate",
                extra={"name": host, "l0_public_path_changed": False},
            )
        )
    label = factory_label(host)
    if label is None:
        tld = refuse_icann_tld(host)
        if tld:
            return _stamp(tld)
        if not (host.endswith(".az") or host.endswith(".aziel")):
            return _stamp(
                _verdict(
                    False,
                    "CAP7-UNKNOWN",
                    verdict=REFUSE,
                    message="unknown Cap-7 name; mesh DNS is not a public resolver",
                    extra={"name": host, "dns_factory": "cap-7-mesh-authoritative"},
                )
            )

    client = _client(fields)
    gateway = label in PUBLIC_BROWSER_GATEWAYS
    if client in PUBLIC_BROWSER_CLIENTS:
        if gateway:
            return _stamp(
                _verdict(
                    True,
                    "AZG-ACCESS-PUBLIC-GATEWAY",
                    verdict=YES,
                    message="one of exactly 2 Cap-7 public browser gateways; not an ICANN name",
                    extra={
                        "name": host,
                        "label": label,
                        "client": client,
                        "public_browser_gateway": True,
                        "public_browser_gateways": list(PUBLIC_BROWSER_GATEWAYS),
                        "public_host_pair": PUBLIC_HOST_PAIR,
                        "pair_required": False,
                        "internet_reachable": False,
                        "typed_on_icann_dns": False,
                        "registrar": False,
                    },
                )
            )
        return _stamp(
            _verdict(
                False,
                "AZG-PUBLIC-PAIR",
                verdict=REFUSE,
                message="standard browsers reach exactly 2 Cap-7 public browser gateways; this name stays on AZNet",
                extra={
                    "name": host,
                    "label": label,
                    "client": client,
                    "public_browser_gateway": False,
                    "public_browser_gateways": list(PUBLIC_BROWSER_GATEWAYS),
                    "public_host_pair": PUBLIC_HOST_PAIR,
                    "access": sorted(ACCESS_CLIENTS),
                },
            )
        )

    if client not in ACCESS_CLIENTS:
        return _stamp(refuse_naked_dns())

    token = _pair_token(fields)
    flag = _azbrowser_flag(fields)
    missing = []
    if not token:
        missing.append("pair_token")
    if not flag:
        missing.append("azbrowser_flag")
    if missing:
        return _stamp(
            _verdict(
                False,
                "AZN-NEED-PAIR",
                verdict=REFUSE,
                message="AZNet and AZBrowser pairing requires a pairing token and an azbrowser flag; both are required",
                extra={
                    "name": host,
                    "label": label,
                    "client": client,
                    "missing": missing,
                    "merge": False,
                    "pair_verified_at_aznet": False,
                    "this_surface_verifies_aznet_token": False,
                    "hosts_payloads": False,
                    "aznet_payload_host": False,
                },
            )
        )
    return _stamp(
        _verdict(
            True,
            "AZN-PAIR-OK",
            verdict=YES,
            message="pairing token and azbrowser flag are both present; this surface did not verify the token at AZNet",
            extra={
                "name": host,
                "label": label,
                "client": client,
                "public_browser_gateway": gateway,
                "merge": False,
                "pair_check": "token-and-flag-present",
                "pair_verified_at_aznet": False,
                "this_surface_verifies_aznet_token": False,
                "hosts_payloads": False,
                "aznet_payload_host": False,
                "access": sorted(ACCESS_CLIENTS),
                "door": "fraggate",
            },
        )
    )


def sidenet_node_gate(
    *,
    action: str,
    hosted: bool = False,
    name: str | None = None,
    fake_flag: bool = False,
    public_icann: bool = False,
    papers: list[Any] | None = None,
    origin_node: str = "node-01",
    most_active_point: str | None = None,
    broken: bool = True,
    have_49: bool = False,
    zone_names: list[str] | None = None,
    now_s: float | None = None,
    last_tick_s: float | None = None,
) -> dict[str, Any]:
    """Node Gate claim / plant / flag / restore.

    ``hosted=True`` is the Worker: cite and refuse. Local execution stays
    on the node and still refuses ICANN, a fake flag, and an incomplete vault.
    """
    act = str(action or "").strip().lower().replace("_", "-")
    if public_icann:
        return _stamp(refuse_public_registrar(kind="aznet-node-gate"))
    if act not in NODE_GATE_ACTIONS:
        return _stamp(
            _verdict(
                False,
                "AZN-NODE-GATE",
                verdict=REFUSE,
                message="Node Gate actions are claim, plant, flag, and restore",
                extra={"action": act, "actions": sorted(NODE_GATE_ACTIONS), "hosted_exec": False},
            )
        )
    if hosted:
        if fake_flag:
            return _stamp(refuse_falsify(kind="fake-flag"))
        if act in {"claim", "restore"}:
            refused = refuse_call_generator(path=f"aznet/{act}")
            refused["action"] = act
            refused["hosted_exec"] = False
            return _stamp(refused)
        return _stamp(
            _verdict(
                False,
                "MGS-NO-HOSTED-PLANT",
                verdict=REFUSE,
                message="flag and plant stay on the local Node Gate; the hosted Worker does not plant a name",
                extra={
                    "action": act,
                    "hosted_plant": False,
                    "hosted_exec": False,
                    "this_worker_is_node_gate": False,
                    "exit": "node-gate-front",
                },
            )
        )

    if act == "claim":
        vault = PaperVault(papers or [])
        out = attempt_claim(
            origin_node=origin_node,
            vault=vault,
            name=name,
            now_s=now_s,
            last_tick_s=last_tick_s,
        )
        out["action"] = "claim"
        out["hosted_exec"] = False
        return _stamp(out)

    if act == "restore":
        out = restore_chain(
            papers=papers,
            broken=broken,
            most_active_point=most_active_point,
            have_49=have_49,
        )
        out["action"] = "restore"
        out["hosted_exec"] = False
        return _stamp(out)

    if fake_flag:
        return _stamp(refuse_falsify(kind="fake-flag"))

    known = list(zone_names or [])
    if act == "plant":
        host = _host(name)
        if not host and not known:
            return _stamp(
                _verdict(
                    False,
                    "AZN-PLANT-NEEDS-CLAIM",
                    verdict=REFUSE,
                    message="plant does not invent a Cap-7 name; claim it on the local 7m77s clock first",
                    extra={"name": "", "zone_names": known, "hosted_exec": False},
                )
            )
        if host and host not in known and f"{host}.az" not in known:
            return _stamp(
                _verdict(
                    False,
                    "AZN-PLANT-NEEDS-CLAIM",
                    verdict=REFUSE,
                    message="plant does not invent a Cap-7 name; claim it on the local 7m77s clock first",
                    extra={"name": host, "zone_names": known, "hosted_exec": False},
                )
            )
    out = plant_flag_and_repost(sites=known or ([name] if name else []), fake_flag=False)
    out["action"] = act
    out["hosted_exec"] = False
    return _stamp(out)
