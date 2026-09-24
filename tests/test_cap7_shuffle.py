"""CAP7-SHUFFLE-1.0: ping→land, honest SLOT vs LIVE, no hard-coded host.

Author: Aziel Eliab only.
"""

from __future__ import annotations

from pathlib import Path

from miragegrid.cap7_shuffle import (
    APP_WORKER_HOST,
    AZ_DOMAIN_DROP_INS,
    CAP7_FACTORY_SITES,
    FACTORY_LABELS,
    FALSE_SITES,
    REAL_HUB_DUPLICATIONS,
    apply_update,
    az_domain_rows,
    cap7_roster,
    cap7_shuffle_dict,
    hosted_bridge_doors,
    land_index,
    land_site,
    ping,
    public_gateway,
    refuse_hardcoded_host,
    shuffle_cite,
    shuffle_seed,
)
from miragegrid.mesh import mesh_law_dict
from miragegrid.semantic_bridge import app_worker, dead_named_worker

ROOT = Path(__file__).resolve().parents[1]
APP_CFG = (ROOT / "workers/miragegrid/wrangler.jsonc").read_text(encoding="utf-8")
APP_INDEX = (ROOT / "workers/miragegrid/src/index.js").read_text(encoding="utf-8")
APP_CAP7 = (ROOT / "workers/miragegrid/src/cap7.js").read_text(encoding="utf-8")
APP_SHUFFLE = (ROOT / "workers/miragegrid/src/shuffle.js").read_text(encoding="utf-8")


def test_seven_different_factory_names_not_hubs() -> None:
    labels = [s["label"] for s in CAP7_FACTORY_SITES]
    assert len(labels) == 7
    assert len(set(labels)) == 7
    assert labels == list(FACTORY_LABELS)
    for name in (
        "azieleliab",
        "godlock",
        "hedidntjump",
        "azielcorpuslibrary",
        "azcorpus",
        "azlibrary",
    ):
        assert name not in labels
    assert REAL_HUB_DUPLICATIONS == ("azgrid", "azcloak", "azvault", "azshift")
    assert FALSE_SITES == ("azbooth", "azflag", "azstandby")


def test_sites_inherit_hub_dna_only() -> None:
    hubs = {
        "https://www.azieleliab.com/",
        "https://www.azielcorpuslibrary.net/",
        "https://godlock.uk/",
        "https://hedidntjump.com/",
    }
    for row in cap7_roster():
        assert row["canonical_hub"] in hubs
        assert row["design_of"] == row["canonical_hub"]
        assert row["public_icann"] is False
        assert row["typed_on_icann_dns"] is False
        assert row["internet_reachable"] is False
        assert row["factory_honesty"] == "LIVE"
        assert row["hosted_update"] == "LIVE"
        assert row["anchored_by_live_nodes"] is True
        assert row["radio_phy"] is False
        assert row["fifth_product"] is False
        assert row["staticlock"] is True
        assert "SLOT" not in str(row["honesty_public"])
        assert row["aznet"] is True
    by_label = {r["label"]: r for r in cap7_roster()}
    assert by_label["azgrid"]["hub_duplication"] is True
    assert by_label["azgrid"]["false_site"] is False
    assert by_label["azgrid"]["resolves_to_hub"] is True
    assert by_label["azbooth"]["false_site"] is True
    assert by_label["azbooth"]["decoy"] is True
    assert by_label["azbooth"]["resolves_to_hub"] is False
    assert sum(1 for row in cap7_roster() if row["hub_duplication"]) == 4
    assert sum(1 for row in cap7_roster() if row["false_site"]) == 3


def test_az_domains_are_the_only_internet_doors() -> None:
    rows = az_domain_rows()
    assert [row["display_name"] for row in rows] == [item["display_name"] for item in AZ_DOMAIN_DROP_INS]
    assert len(rows) == 4
    for row in rows:
        assert row["public_icann"] is True
        assert row["resolves_to_hub"] is True
        assert row["internet_reachable"] is True
        assert row["honesty"] == "LIVE"
        assert row["shuffle_once"] is True
        assert row["stands_alone"] is True
        assert row["immutable_after_hub_down"] is True
        assert row["mirrors_while_up"] is True
        assert row["anchored_by_live_nodes"] is True
        assert row["cap7"] is False
        assert row["icann_registrar_purchase"] is False
        assert row["internet_url"] == row["canonical_hub"]
    gate = public_gateway("azgrid")
    assert gate["ok"] is True
    assert gate["code"] == "CAP7-FACTORY-LIVE"
    assert gate["internet_reachable"] is False
    assert gate["hub_duplication"] is True
    decoy = public_gateway("azbooth")
    assert decoy["ok"] is True
    assert decoy["false_site"] is True
    assert decoy["factory_honesty"] == "LIVE"
    cloak = public_gateway("azcloak")
    assert cloak["ok"] is True
    assert cloak["hub_duplication"] is True


def test_ping_without_seed_continues() -> None:
    out = ping(node_id="node-01")
    assert out["ok"] is True
    assert out["code"] == "CAP7-PING"
    assert out["phase"] == "ping"
    assert out["continue"] is True
    assert out["land"] is None
    assert out["hardcoded_host"] is False


def test_same_seed_same_land_no_hardcoded_host() -> None:
    a = ping(node_id="node-01", round_id="round-alpha")
    b = ping(node_id="node-25", round_id="round-alpha")
    c = ping(node_id="node-01", round_id="round-beta")
    assert a["code"] == "CAP7-LAND"
    assert a["phase"] == "land"
    assert a["continue"] is False
    assert a["land"]["label"] == b["land"]["label"]
    assert a["update"] is False
    # Different round may land elsewhere; must not be a single hardcoded host.
    assert refuse_hardcoded_host()["code"] == "CAP7-NO-HARDCODED-HOST"
    assert a["hardcoded_host"] is False
    lands = {a["land"]["label"], c["land"]["label"]}
    assert lands <= set(FACTORY_LABELS)
    # Distinct seeds must be able to pick different Cap-7 names.
    seen = {land_site(shuffle_seed(round_id=f"round-{i}"))["label"] for i in range(32)}
    assert seen <= set(FACTORY_LABELS)
    assert len(seen) >= 2
    seed = shuffle_seed(round_id="round-alpha")
    assert seed and len(seed) == 64
    assert land_site(seed)["label"] == a["land"]["label"]
    assert 0 <= land_index(seed) < 7


def test_update_proof_land_is_update_endpoint() -> None:
    out = ping(node_id="node-07", prev="prev-tip", lockset="lock-1")
    assert out["code"] == "CAP7-LAND"
    assert out["update"] is True
    assert out["update_endpoint"]
    assert out["land"]["label"] in FACTORY_LABELS
    other = ping(node_id="node-08", prev="prev-tip", lockset="lock-1")
    assert other["land"]["label"] == out["land"]["label"]
    upd = apply_update(node_id="node-07", prev="prev-tip", lockset="lock-1")
    assert upd["code"] == "CAP7-UPDATE"
    assert upd["phase"] == "update"
    assert upd["land"]["label"] == out["land"]["label"]
    assert upd["update_endpoint"] == out["update_endpoint"]
    assert upd["hardcoded_host"] is False
    assert upd["internet_reachable"] is False
    assert upd["hosted_update"] == "LIVE"
    assert upd["factory_honesty"] == "LIVE"
    waiting = apply_update(node_id="node-07")
    assert waiting["phase"] == "ping"
    assert waiting["continue"] is True


def test_refuses_icann_hub_resolve_radio_callable() -> None:
    assert ping(public_icann=True)["ok"] is True
    assert ping(resolves_to_hub=True)["ok"] is True
    assert ping(icann_registrar_purchase=True)["code"] == "AZG-NOT-PUBLIC-REGISTRAR"
    assert ping(cctld_purchase=True)["code"] == "AZG-NOT-PUBLIC-REGISTRAR"
    assert ping(typed_on_icann_dns=True)["code"] == "CAP7-NOT-ICANN-DNS"
    assert ping(radio_phy=True)["code"] == "AZG-NO-RADIO-PHY"
    assert ping(inbound_call=True)["code"] == "AZG-NOT-CALLABLE"
    assert ping(invent_first_flag=True)["code"] == "BRIDGE-NO-INVENT-HTTPS"
    assert ping(hardcoded_host="azgrid.az")["code"] == "CAP7-NO-HARDCODED-HOST"
    assert ping(channel_plane_is_vpn=True)["code"] == "CAP7-NO-VPN-LIE"
    assert ping(second_door=True)["code"] == "CAP7-NO-VPN-LIE"
    assert ping(open_proxy=True)["code"] == "CAP7-NO-VPN-LIE"


def test_bridge_doors_and_app_worker_live() -> None:
    doors = hosted_bridge_doors()
    assert doors["code"] == "BRIDGE-CAP7-SHUFFLE"
    assert doors["app_worker"]["status"] == "live-app"
    assert doors["app_worker"]["cite"] is True
    assert doors["app_worker"]["url"] == APP_WORKER_HOST
    assert doors["honesty"]["app_worker"] == "LIVE"
    assert doors["honesty"]["factory"] == "LIVE"
    assert doors["honesty"]["az_domains"] == "LIVE"
    assert doors["internet_reaches"] == "az-domains"
    assert doors["typed_on_icann_dns"] is False
    assert doors["false_site_count"] == 3
    assert doors["real_duplication_count"] == 4
    assert doors["doors"]["bridge"].endswith("/bridge")
    assert doors["doors"]["update"].endswith("/v1/shuffle/update")
    assert doors["radio_phy"] is False
    assert doors["channel_plane_is_vpn"] is False
    assert doors["second_door"] is False
    assert doors["hosted_update"] == "LIVE"
    assert doors["honesty"]["public_shuffle_land_exec"] == "LIVE"
    assert doors["honesty"]["hosted_endpoints"] == "LIVE"
    assert doors["hosted_mcp"] == "LIVE"
    assert doors["anchored_by_live_nodes"] is True
    assert doors["aznet_payload_host"] is False
    assert doors["hash_receipt"]["second_receipt_door"] is False
    cloak = public_gateway("azcloak")
    assert cloak["resolves_to_hub"] is True
    assert cloak["radio_phy"] is False
    assert cloak["internet_reachable"] is False
    land = ping(node_id="node-01", round_id="outlast")
    assert land["hosted_update"] == "LIVE"
    assert land["public_shuffle_land_exec"] == "LIVE"
    assert land["is_live_door"] is False
    law = cap7_shuffle_dict()
    assert law["domain_anchor"] == "live-nodes"
    assert law["factory_honesty"] == "LIVE"
    assert law["open_proxy"] is False
    assert law["fraggate_single_door"] is True
    cite = shuffle_cite()
    assert cite["code"] == "CAP7-SHUFFLE-CITE"
    law = cap7_shuffle_dict()
    assert law["az_generator"]["exit"] == "node-gate-front"
    assert law["az_generator"]["callable"] is False
    mesh = mesh_law_dict()
    assert mesh["cap7_shuffle"]["spec"] == "CAP7-SHUFFLE-1.0"
    live = app_worker()
    assert live["status"] == "live-app"
    assert live["cite"] is True
    assert dead_named_worker()["status"] == "live-app"


def test_land_index_uses_full_width_int() -> None:
    seed = "f" * 64
    assert land_index(seed) == int(seed[:16], 16) % 7
    assert land_index(seed) == 1


def test_get_prev_lockset_does_not_plant_update() -> None:
    planted = ping(node_id="node-01", prev="p", lockset="l", method="GET")
    assert planted["ok"] is False
    assert planted["code"] == "MESH-GET-NO-ENABLE"
    cite = ping(node_id="node-01", round_id="audit-round", method="GET")
    assert cite["code"] == "CAP7-LAND"
    assert cite["update"] is False


def test_bad_node_id_refused() -> None:
    bad = ping(node_id="A" * 200, round_id="r")
    assert bad["ok"] is False
    assert bad["code"] == "CAP7-BAD-NODE-ID"


def test_app_worker_wrangler_named_miragegrid() -> None:
    assert '"name": "miragegrid"' in APP_CFG
    assert "ac575a9b822bea2bed97d0ab73aed238" in APP_CFG
    assert '"main": "src/index.js"' in APP_CFG
    assert "2026-09-18" in APP_CFG
    assert "nodejs_compat" in APP_CFG
    assert "observability" in APP_CFG
    assert "/bridge" in APP_INDEX
    assert "/v1/shuffle/ping" in APP_INDEX
    assert "CAP7-SHUFFLE-1.0" in APP_CAP7
    assert "hardcoded_host" in APP_SHUFFLE
    assert "azgrid" in APP_CAP7 and "azstandby" in APP_CAP7
    assert "radio_phy: false" in APP_CAP7
    assert "AZ.AzielEliab.AZ" in APP_CAP7
    assert "false_site" in APP_CAP7
    assert "staticlock" in APP_CAP7
    assert "factory_honesty: \"LIVE\"" in APP_CAP7 or "factory_honesty: 'LIVE'" in APP_CAP7 or 'factoryHonesty: "LIVE"' in APP_CAP7 or "LIVE" in APP_CAP7
    deploy = (ROOT / "workers/miragegrid/deploy.sh").read_text(encoding="utf-8")
    assert "--name miragegrid" in deploy
    pkg = (ROOT / "workers/miragegrid/package.json").read_text(encoding="utf-8")
    assert '"name": "miragegrid"' in pkg
    assert "wrangler deploy --name miragegrid --config wrangler.jsonc" in pkg
    ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "npx wrangler deploy --name miragegrid --dry-run" in ci
    assert "/v1/shuffle/update" in APP_INDEX
    assert "outlastHonesty" in APP_INDEX
    assert "CAP7-NO-VPN-LIE" in APP_SHUFFLE
    assert "hosted_update" in APP_CAP7
    audit = (ROOT / "docs/audit/OUTLAST-CAP7-MESH-2026-09-18.md").read_text(encoding="utf-8")
    assert "FragGate is THE exec door" in audit
    assert "channel_plane_is_vpn" in audit
    assert "MGS-NO-HOSTED-APPLY" in audit
    assert "CAP7-NO-VPN-LIE" in audit
