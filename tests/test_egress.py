"""MG-EGRESS-1.0: Cap-7 control plane is live; public egress IP stays refused."""

from __future__ import annotations

from miragegrid.cap7_shuffle import FRAGGATE_CAP7_STUBS
from miragegrid.egress import (
    STICKY_VECTOR,
    egress_cite,
    prepare_sticky,
    refusal_for_assign,
    sticky_mesh_index,
    sticky_node_id,
)


def test_cite_does_not_claim_a_pool() -> None:
    cite = egress_cite()
    assert cite["code"] == "MG-EGRESS-CITE"
    assert cite["residential"] is False
    assert cite["egress_ip"] is None
    assert cite["public_egress_ip"] is False
    assert cite["sticky_public_ip"] is False
    assert cite["cf_geo_exit_pool"] is False
    assert cite["vpn_hosted_live"] is False
    assert cite["azvpn_merged"] is False
    assert cite["anonymity_network"] is False
    assert cite["control_plane"] == "live"
    assert cite["fraggate_stub_ops"] == list(FRAGGATE_CAP7_STUBS)
    assert cite["fraggate_stub_ops"] == ["vpn-hop", "hop", "tunnel", "mesh"]
    assert cite["worker_live_ops"] == ["geo-target", "session-stick", "egress-rotate"]
    assert "geo-target" not in cite["fraggate_stub_ops"]
    assert cite["softwares_catalog_live"] is False


def test_assign_allows_control_plane_and_refuses_ip_exit() -> None:
    assert refusal_for_assign({"country": "US", "city": "Miami"}) is None
    assert refusal_for_assign({"sticky_key": "booth-1", "ttl_seconds": 600}) is None
    assert refusal_for_assign({"rotate": True, "from_label": "azgrid"}) is None

    ip = refusal_for_assign({"country": "US", "egress_ip": "203.0.113.8"})
    assert ip is not None
    assert ip["status"] == 403
    assert ip["body"]["code"] == "MG-NO-IP-EXIT"
    assert ip["body"]["public_ip_applied"] is False
    assert ip["body"]["egress_ip"] is None
    assert "node_id" not in ip["body"]

    residential = refusal_for_assign({"rotate": True, "residential": True})
    assert residential is not None
    assert residential["body"]["code"] == "MG-NO-IP-EXIT"
    assert residential["body"]["ip_rotated"] is False

    paint = refusal_for_assign({"endpoints": {"node-01": "203.0.113.8:443"}})
    assert paint is not None
    assert paint["body"]["code"] == "MG-NO-EGRESS-PAINT"
    assert paint["body"]["endpoints_applied"] is False


def test_assign_allows_a_plain_session_and_rejects_bad_hops() -> None:
    assert refusal_for_assign({}) is None
    assert refusal_for_assign({"hops": 3, "session_id": "booth-a"}) is None
    assert refusal_for_assign({"rotate": False, "sticky": "no"}) is None
    bad = refusal_for_assign({"hops": 0})
    assert bad is not None and bad["body"]["code"] == "MG-BAD-HOPS"
    huge = refusal_for_assign({"hops": 99})
    assert huge is not None and huge["status"] == 400
    sid = refusal_for_assign({"session_id": "x" * 81})
    assert sid is not None and sid["body"]["code"] == "MG-BAD-SESSION-ID"


def test_sticky_mesh_label_is_deterministic_and_not_an_ip() -> None:
    assert sticky_mesh_index(STICKY_VECTOR["sticky_key"]) == STICKY_VECTOR["index"]
    assert sticky_node_id("booth-1") == "node-21"
    assert sticky_node_id("booth-1") == sticky_node_id("booth-1")
    ready = prepare_sticky({"sticky_key": "booth-1"})
    assert ready["sticky"] is True
    assert ready["sticky_key"] == "booth-1"
    assert ready["sticky_public_ip"] is False
    assert ready["ttl_enforced"] is False
    labeled = prepare_sticky({"sticky_key": "booth-1", "country": "DE", "ttl_seconds": 3600})
    assert labeled["sticky"] is True
    assert labeled["ttl_enforced"] is True
    assert labeled["region_label"]["country"] == "DE"
    assert labeled["ip_exit"] is False
    early = sticky_node_id("booth-1", 3600, 1_700_000_000)
    later = sticky_node_id("booth-1", 3600, 1_700_000_000 + 3600)
    assert early.startswith("node-")
    assert later.startswith("node-")
    missing = prepare_sticky({})
    assert missing["body"]["code"] == "MG-STICKY-NEED-KEY"
    address = prepare_sticky({"sticky_key": "booth-1", "sticky_ip": "203.0.113.9"})
    assert address["body"]["code"] == "MG-NO-IP-EXIT"
