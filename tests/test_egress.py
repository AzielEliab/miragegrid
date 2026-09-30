"""MG-EGRESS-1.0: refuse geo / sticky IP / rotation; sticky mesh label is real."""

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
    assert cite["vpn_hosted_live"] is False
    assert cite["azvpn_merged"] is False
    assert cite["anonymity_network"] is False
    assert cite["fraggate_stub_ops"] == list(FRAGGATE_CAP7_STUBS)
    assert cite["fraggate_stub_ops"] == [
        "vpn-hop",
        "hop",
        "tunnel",
        "mesh",
        "geo-target",
        "session-stick",
        "egress-rotate",
    ]
    assert cite["vpn_hosted_live"] is False
    assert cite["fulfilled"] is False


def test_assign_refuses_geo_sticky_and_rotation_without_a_node() -> None:
    geo = refusal_for_assign({"country": "US", "city": "Miami"})
    assert geo is not None
    assert geo["status"] == 403
    assert geo["body"]["code"] == "MG-GEO-NOT-READY"
    assert geo["body"]["geo_applied"] is False
    assert geo["body"]["egress_ip"] is None
    assert "node_id" not in geo["body"]

    sticky = refusal_for_assign({"sticky": True, "ttl_seconds": 600})
    assert sticky is not None
    assert sticky["body"]["code"] == "MG-STICKY-IP-NOT-READY"

    rotate = refusal_for_assign({"rotate": True, "residential": True})
    assert rotate is not None
    assert rotate["body"]["code"] == "MG-EGRESS-IP-NOT-READY"
    assert rotate["body"]["ip_rotated"] is False

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
    blocked = prepare_sticky({"sticky_key": "booth-1", "country": "DE"})
    assert blocked["body"]["code"] == "MG-GEO-NOT-READY"
    ttl = prepare_sticky({"sticky_key": "booth-1", "ttl_seconds": 120})
    assert ttl["body"]["code"] == "MG-STICKY-TTL-NOT-READY"
    assert ttl["body"].get("node_id") is None
    missing = prepare_sticky({})
    assert missing["body"]["code"] == "MG-STICKY-NEED-KEY"
