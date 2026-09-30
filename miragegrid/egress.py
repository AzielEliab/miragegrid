"""MG-EGRESS-1.0 — Cap-7 control plane.

geo-target, session-stick, and egress-rotate are LIVE as factory metadata:
a region label, a sticky mesh node plus Cap-7 land, and a land rotation.
Not a public egress IP. Not a Cloudflare geo-exit pool.
Not a VPN. Not AZVPN. Not an ICANN registrar. Author: Aziel Eliab only.
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
TTL_MIN = 60
TTL_MAX = 86400
FRAGGATE_STUB_OPS = list(FRAGGATE_CAP7_STUBS)
WORKER_LIVE_OPS = ["geo-target", "session-stick", "egress-rotate"]
IP_EXIT_MESSAGE = (
    "MirageGrid does not host a public egress IP, a sticky public address, or a "
    "Cloudflare geo-exit pool. Cap-7 geo-target is a region label, session-stick "
    "is a mesh node plus a factory land, and egress-rotate moves that land among "
    "the seven sites. IP exit stays on AZVPN or a future binding this package does not claim."
)
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
ROTATE_KEYS = ("rotate", "rotation", "from_label", "land_label", "prev_land")
IP_EXIT_KEYS = (
    "egress_ip",
    "exit_ip",
    "new_ip",
    "proxy",
    "socks",
    "socks5",
    "residential",
    "anyip",
    "cf_geo",
    "cf_geo_exit",
    "geo_exit",
    "wireguard",
    "openvpn",
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
        "public_egress_ip": False,
        "sticky_public_ip": False,
        "sticky_ip": False,
        "cf_geo_exit_pool": False,
        "geo_pool": False,
        "ip_exit": False,
        "ip_rotated": False,
        "vpn_hosted_live": False,
        "packet_forwarding": False,
        "hosted_vpn": False,
        "anonymity_network": False,
        "azvpn_separate": True,
        "azvpn_merged": False,
        "wireguard": False,
        "openvpn": False,
        "l3_exit": False,
        "public_icann": False,
        "public_icann_registrar": False,
        "fraggate_stub_ops": list(FRAGGATE_STUB_OPS),
        "worker_live_ops": list(WORKER_LIVE_OPS),
        "softwares_catalog_live": False,
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


def region_label(body: dict[str, Any] | None) -> dict[str, str] | None:
    fields = _fields(body)
    label: dict[str, str] = {}
    for key in GEO_KEYS:
        value = fields.get(key)
        if not _present(value) or isinstance(value, (dict, list)):
            continue
        label[key] = str(value).strip()[:80]
    return label or None


def _first_ttl(fields: dict[str, Any]) -> Any:
    for key in TTL_KEYS:
        value = fields.get(key)
        if value not in (None, "", False):
            return value
    return None


def normalize_ttl(body: dict[str, Any] | None) -> dict[str, Any]:
    raw = _first_ttl(_fields(body))
    if raw is None:
        return {"ttl_seconds": None}
    if isinstance(raw, bool) or not isinstance(raw, int):
        try:
            if isinstance(raw, str) and raw.strip().lstrip("-").isdigit():
                raw = int(raw.strip())
            else:
                raise ValueError
        except ValueError:
            raw = None
    if not isinstance(raw, int) or isinstance(raw, bool) or raw < TTL_MIN or raw > TTL_MAX:
        return {
            "error": _verdict(
                False,
                "MG-BAD-TTL",
                400,
                "ttl_seconds must be an integer 60..86400. The stick is a time-bucket hash of the key, not a stored public IP.",
                {"ttl_enforced": False, "durable_store": False},
            )
        }
    return {"ttl_seconds": raw}


def ip_exit_refuse(body: dict[str, Any] | None = None) -> dict[str, Any] | None:
    fields = _fields(body)
    hits = _asked(fields, IP_EXIT_KEYS)
    sticky_addr = isinstance(fields.get("sticky_ip"), (str, int)) and not isinstance(fields.get("sticky_ip"), bool)
    if not hits and not sticky_addr:
        return None
    requested = _requested(fields, IP_EXIT_KEYS)
    if sticky_addr:
        requested["sticky_ip"] = fields.get("sticky_ip")
    return _verdict(
        False,
        "MG-NO-IP-EXIT",
        403,
        IP_EXIT_MESSAGE,
        {"requested": requested, "public_ip_applied": False, "control_plane": "cap7"},
    )


def egress_cite() -> dict[str, Any]:
    return {
        "ok": True,
        "code": "MG-EGRESS-CITE",
        "verdict": "yes",
        "yes": True,
        "message": (
            "Cap-7 control plane is LIVE. geo-target records a region label. "
            "session-stick binds a mesh node and a factory land for a TTL. "
            "egress-rotate moves that land among the seven sites. "
            "None of these allocate a public egress IP or a Cloudflare geo-exit pool."
        ),
        **honesty_stamps(),
        "cite": True,
        "control_plane": "live",
        "live": {
            "geo_target": "POST /v1/egress/geo — region label on a mesh node and a Cap-7 land. ip_exit false.",
            "session_stick": "POST /v1/session/sticky — same sticky_key, same node id and Cap-7 site. Not a public IP.",
            "egress_rotate": "POST /v1/egress/rotate — next Cap-7 factory land. Not packet egress.",
            "assign": "POST /v1/assign — session circuit. Not an egress IP.",
        },
        "not_hosted": {
            "public_egress_ip": "MG-NO-IP-EXIT. No sticky public address and no Cloudflare geo-exit pool.",
            "packet_hop": "FragGate vpn-hop, hop, tunnel, and mesh stay FG-STUB.",
            "painted_endpoints": "MG-NO-EGRESS-PAINT.",
        },
        "not": [
            "residential IP network",
            "anonymity network",
            "hosted packet VPN",
            "Cloudflare geo-exit pool",
            "sticky public IP",
            "AZVPN (separate Softwares product)",
            "public ICANN registrar",
        ],
        "azvpn": {
            "slug": "azvpn",
            "merged": False,
            "note": "AZVPN is the HTTPS/WS concentrator. MirageGrid does not open it and does not claim its exit pool.",
        },
        "sticky_ip_means": (
            "On MirageGrid, the sticky path is a Cap-7 session/land stick: one mesh node id and one "
            "factory site for the key. sticky_public_ip stays false."
        ),
        "vector": dict(STICKY_VECTOR),
    }


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
    blocked = ip_exit_refuse(fields)
    if blocked:
        return blocked
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
    key = str(fields.get("sticky_key") or fields.get("session_key") or "").strip()
    if key and SESSION_RE.fullmatch(key) is None:
        return _verdict(False, "MG-BAD-SESSION-ID", 400, "sticky_key must be 1–80 [A-Za-z0-9._-]", {})
    ttl = normalize_ttl(fields)
    if ttl.get("error"):
        return ttl["error"]
    if ttl.get("ttl_seconds") is not None and not key:
        return _verdict(
            False,
            "MG-STICKY-NEED-KEY",
            400,
            "ttl_seconds needs sticky_key. The TTL binds a mesh node and a Cap-7 land, not a public IP.",
            {},
        )
    return None


def sticky_mesh_index(sticky_key: str, ttl_seconds: int | None = None, now_s: int | None = None) -> int:
    material = f"{STICKY_PREFIX}{sticky_key}"
    if ttl_seconds is not None:
        if now_s is None:
            raise ValueError("now_s is required when ttl_seconds is set")
        window = now_s // ttl_seconds
        material = f"{material}|w{window}"
    digest = hashlib.sha256(material.encode("utf-8")).digest()
    return int.from_bytes(digest, "big") % POOL_SIZE


def sticky_node_id(sticky_key: str, ttl_seconds: int | None = None, now_s: int | None = None) -> str:
    return f"node-{sticky_mesh_index(sticky_key, ttl_seconds, now_s) + 1:02d}"


def prepare_sticky(body: dict[str, Any] | None) -> dict[str, Any]:
    fields = _fields(body)
    if _asked(fields, VPN_KEYS):
        return vpn_refuse(fields)
    blocked = ip_exit_refuse(fields)
    if blocked:
        return blocked
    if _asked(fields, PAINT_KEYS):
        return paint_refuse(fields)
    ttl = normalize_ttl(fields)
    if ttl.get("error"):
        return ttl["error"]
    key = str(fields.get("sticky_key") or fields.get("session_key") or "").strip()
    if not key:
        return _verdict(
            False,
            "MG-STICKY-NEED-KEY",
            400,
            "sticky_key is required. It binds a mesh node and a Cap-7 land. It does not allocate a public IP.",
            {},
        )
    if SESSION_RE.fullmatch(key) is None:
        return _verdict(False, "MG-BAD-SESSION-ID", 400, "sticky_key must be 1–80 [A-Za-z0-9._-]", {})
    return {
        "sticky": True,
        "sticky_key": key,
        "ttl_seconds": ttl.get("ttl_seconds"),
        "ttl_enforced": ttl.get("ttl_seconds") is not None,
        "region_label": region_label(fields),
        "sticky_public_ip": False,
        "public_egress_ip": False,
        "ip_exit": False,
        "cf_geo_exit_pool": False,
    }
