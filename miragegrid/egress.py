"""MG-EGRESS-1.0 — honest geo / sticky / egress contract.

anyIP-style questions land here. No residential pool is live.
Sticky mesh-node labels are deterministic. Sticky public IPs are not.
AZVPN stays a separate product. Author: Aziel Eliab only.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any

from miragegrid.cap7_shuffle import FRAGGATE_CAP7_STUBS

EGRESS_SPEC = "MG-EGRESS-1.0"
IDENTITY = "Aziel Eliab"
POOL_SIZE = 25
STICKY_PREFIX = "mg-sticky-v1|"
STICKY_VECTOR = {
    "sticky_key": "booth-1",
    "sha256": "97f92cd52d11c560baf28f1e6b93cd6d996a3b2aa5d5a33a0335dfe10af62490",
    "index": 20,
    "node_id": "node-21",
}
SESSION_RE = re.compile(r"[A-Za-z0-9._-]{1,80}")
FALSE_WORDS = {"false", "0", "no", "off"}

GEO_KEYS = (
    "geo",
    "country",
    "country_code",
    "region",
    "city",
    "state",
    "asn",
    "isp",
    "zip",
    "postal",
)
ROTATE_KEYS = (
    "rotate",
    "rotation",
    "egress",
    "egress_ip",
    "exit_ip",
    "proxy",
    "socks",
    "socks5",
    "residential",
    "anyip",
    "new_ip",
)
VPN_KEYS = ("vpn", "vpn_hop", "tunnel", "hop", "hosted_vpn")
STICKY_KEYS = (
    "sticky",
    "sticky_session",
    "sticky_key",
    "sticky_ip",
    "session_ttl",
    "ttl",
    "ttl_seconds",
    "duration",
)
TTL_KEYS = ("session_ttl", "ttl", "ttl_seconds", "duration")
PAINT_KEYS = ("endpoints", "endpoint")


def _present(value: Any) -> bool:
    if value is None or value is False or value == "":
        return False
    if isinstance(value, str) and value.strip().lower() in FALSE_WORDS:
        return False
    if isinstance(value, (int, float)) and value == 0:
        return False
    if isinstance(value, (list, tuple, dict)) and len(value) == 0:
        return False
    return True


def _asked(body: dict[str, Any], keys: tuple[str, ...]) -> list[str]:
    return [key for key in keys if _present(body.get(key))]


def _requested(body: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    return {key: body.get(key) for key in keys if _present(body.get(key))}


def honesty_stamps() -> dict[str, Any]:
    return {
        "spec": EGRESS_SPEC,
        "author": IDENTITY,
        "identity": IDENTITY,
        "residential": False,
        "egress_ip": None,
        "geo_applied": False,
        "sticky_ip": False,
        "ip_rotated": False,
        "vpn_hosted_live": False,
        "packet_forwarding": False,
        "anonymity_network": False,
        "azvpn_separate": True,
        "azvpn_merged": False,
        "fraggate_stub_ops": list(FRAGGATE_CAP7_STUBS),
        "fulfilled": False,
    }


def _verdict(ok: bool, code: str, status: int, message: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    body = {
        "ok": bool(ok),
        "code": code,
        "verdict": "yes" if ok else "refuse",
        "yes": bool(ok),
        "message": message,
        **honesty_stamps(),
    }
    if extra:
        body.update(extra)
    return {"status": status, "body": body}


def _fields(body: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(body, dict):
        return {}
    return body


def egress_cite() -> dict[str, Any]:
    return {
        "ok": True,
        "code": "MG-EGRESS-CITE",
        "verdict": "yes",
        "yes": True,
        "message": "Cite only. Geo targeting, sticky public IPs, and egress IP rotation are not live. Mesh-node stickiness is a separate deterministic label, not an IP.",
        **honesty_stamps(),
        "fulfilled": False,
        "cite": True,
        "live": {
            "assign": "POST /v1/assign — short-lived mesh node label (node-01..node-25) and a receipt. Not an egress IP.",
            "sticky_mesh_node": "POST /v1/session/sticky — same sticky_key, same mesh node label. Not a sticky IP. No TTL store.",
            "cap7": "Cap-7 factory cite/shuffle. Not ICANN .az publish.",
        },
        "refuse_until_ready": {
            "geo": "POST /v1/egress/geo — MG-GEO-NOT-READY. No country, city, or ASN pool.",
            "sticky_ip": "POST /v1/egress/sticky — MG-STICKY-IP-NOT-READY. No sticky public address.",
            "ip_rotation": "POST /v1/egress/rotate — MG-EGRESS-IP-NOT-READY. No egress address to rotate.",
            "ttl": "MG-STICKY-TTL-NOT-READY. No durable session store, so a TTL would be theater.",
            "painted_endpoints": "MG-NO-EGRESS-PAINT. Callers cannot write listen addresses onto the pool.",
        },
        "not": [
            "residential IP network",
            "anonymity network",
            "hosted packet VPN",
            "AZVPN (separate Softwares product)",
        ],
        "azvpn": {
            "slug": "azvpn",
            "merged": False,
            "note": "AZVPN is the HTTPS/WS concentrator. MirageGrid does not open it.",
        },
        "vector": dict(STICKY_VECTOR),
    }


def geo_refuse(body: dict[str, Any] | None = None) -> dict[str, Any]:
    fields = _fields(body)
    return _verdict(
        False,
        "MG-GEO-NOT-READY",
        403,
        "No geo pool is live. Country, city, region, and ASN are not applied. No exit address is selected.",
        {"requested": _requested(fields, GEO_KEYS), "pool": None},
    )


def rotate_refuse(body: dict[str, Any] | None = None) -> dict[str, Any]:
    fields = _fields(body)
    return _verdict(
        False,
        "MG-EGRESS-IP-NOT-READY",
        403,
        "No egress IP pool is live. Nothing rotated. A new mesh label is POST /v1/assign, and that label is not an IP.",
        {
            "requested": _requested(fields, ROTATE_KEYS),
            "mesh_label_rotation": "POST /v1/assign",
            "mesh_label_is_ip": False,
        },
    )


def sticky_ip_refuse(body: dict[str, Any] | None = None) -> dict[str, Any]:
    fields = _fields(body)
    return _verdict(
        False,
        "MG-STICKY-IP-NOT-READY",
        403,
        "No sticky public IP is live. Mesh-node stickiness is POST /v1/session/sticky and is not an address.",
        {"requested": _requested(fields, STICKY_KEYS), "mesh_node_stick": "POST /v1/session/sticky"},
    )


def sticky_ttl_refuse(body: dict[str, Any] | None = None) -> dict[str, Any]:
    fields = _fields(body)
    return _verdict(
        False,
        "MG-STICKY-TTL-NOT-READY",
        403,
        "No session store is live, so a TTL cannot be enforced. Refusing rather than ignoring the expiry.",
        {"requested": _requested(fields, TTL_KEYS), "ttl_enforced": False},
    )


def vpn_refuse(body: dict[str, Any] | None = None) -> dict[str, Any]:
    fields = _fields(body)
    return _verdict(
        False,
        "MG-NOT-VPN",
        403,
        "Hosted MirageGrid is not a VPN, not a tunnel, and not an anonymity network. FragGate vpn-hop, hop, tunnel, mesh, geo-target, session-stick, and egress-rotate stay stub. AZVPN is separate.",
        {"requested": _requested(fields, VPN_KEYS)},
    )


def paint_refuse(body: dict[str, Any] | None = None) -> dict[str, Any]:
    fields = _fields(body)
    return _verdict(
        False,
        "MG-NO-EGRESS-PAINT",
        403,
        "Listen addresses stay loopback defaults. A caller-supplied endpoint is not an egress IP.",
        {"requested": _requested(fields, PAINT_KEYS), "listen_targets": "loopback-defaults", "endpoints_applied": False},
    )


def refusal_for_assign(body: dict[str, Any] | None) -> dict[str, Any] | None:
    fields = _fields(body)
    if _asked(fields, VPN_KEYS):
        return vpn_refuse(fields)
    if _asked(fields, GEO_KEYS):
        return geo_refuse(fields)
    if _asked(fields, ROTATE_KEYS):
        return rotate_refuse(fields)
    if _asked(fields, STICKY_KEYS):
        return sticky_ip_refuse(fields)
    if _asked(fields, PAINT_KEYS):
        return paint_refuse(fields)
    if "hops" in fields and fields.get("hops") is not None:
        hops = fields.get("hops")
        if not isinstance(hops, int) or isinstance(hops, bool) or hops < 1 or hops > POOL_SIZE:
            return _verdict(False, "MG-BAD-HOPS", 400, "hops must be an integer 1..25", {"hops": hops})
    session_id = fields.get("session_id")
    if session_id not in (None, ""):
        if not isinstance(session_id, str) or SESSION_RE.fullmatch(session_id) is None:
            return _verdict(False, "MG-BAD-SESSION-ID", 400, "session_id must be 1–80 [A-Za-z0-9._-]", {})
    return None


def sticky_mesh_index(sticky_key: str) -> int:
    digest = hashlib.sha256(f"{STICKY_PREFIX}{sticky_key}".encode("utf-8")).digest()
    return int.from_bytes(digest, "big") % POOL_SIZE


def sticky_node_id(sticky_key: str) -> str:
    return f"node-{sticky_mesh_index(sticky_key) + 1:02d}"


def prepare_sticky(body: dict[str, Any] | None) -> dict[str, Any]:
    fields = _fields(body)
    if _asked(fields, VPN_KEYS):
        return vpn_refuse(fields)
    if _asked(fields, GEO_KEYS):
        return geo_refuse(fields)
    if _asked(fields, ROTATE_KEYS):
        return rotate_refuse(fields)
    if _present(fields.get("sticky_ip")):
        return sticky_ip_refuse(fields)
    if _asked(fields, TTL_KEYS):
        return sticky_ttl_refuse(fields)
    if _asked(fields, PAINT_KEYS):
        return paint_refuse(fields)
    key = str(fields.get("sticky_key") or fields.get("session_key") or "").strip()
    if not key:
        return _verdict(False, "MG-STICKY-NEED-KEY", 400, "sticky_key is required. It selects a mesh node label, not an IP.", {})
    if SESSION_RE.fullmatch(key) is None:
        return _verdict(False, "MG-BAD-SESSION-ID", 400, "sticky_key must be 1–80 [A-Za-z0-9._-]", {})
    return {"sticky": True, "sticky_key": key}
