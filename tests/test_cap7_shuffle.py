"""CAP7-SHUFFLE-1.0: ping→land, honest SLOT vs LIVE, no hard-coded host.

Author: Aziel Eliab only.
"""

from __future__ import annotations

from pathlib import Path

from miragegrid.cap7_shuffle import (
    APP_WORKER_HOST,
    AZNET_SIDE_LABELS,
    CAP7_FACTORY_SITES,
    FACTORY_LABELS,
    PUBLIC_PAIR_LABELS,
    apply_update,
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
    assert PUBLIC_PAIR_LABELS == ("azgrid", "azbooth")
    assert set(AZNET_SIDE_LABELS) == {"azcloak", "azvault", "azshift", "azflag", "azstandby"}


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
        assert row["resolves_to_hub"] is False
        assert row["name_may_change"] is True
        assert row["public_icann"] is False
        assert row["radio_phy"] is False
        assert row["fifth_product"] is False
        assert row["mesh_name_icann"] == "SLOT"
        assert row["aznet"] is True


def test_public_pair_live_remainder_slot() -> None:
    by_label = {r["label"]: r for r in cap7_roster()}
    assert by_label["azgrid"]["honesty_public"] == "LIVE"
    assert by_label["azbooth"]["honesty_public"] == "LIVE"
    assert by_label["azgrid"]["browser_reachable"] is True
    for label in AZNET_SIDE_LABELS:
        assert by_label[label]["honesty_public"] == "SLOT"
        assert by_label[label]["browser_reachable"] is False
        assert by_label[label]["reach"] == "aznet"
    gate = public_gateway("azgrid")
    assert gate["ok"] is True
    assert gate["code"] == "CAP7-GATEWAY-LIVE"
    slot = public_gateway("azcloak")
    assert slot["ok"] is False
    assert slot["code"] == "CAP7-SLOT-NOT-LIVE"


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
    assert upd["resolves_to_hub"] is False
    waiting = apply_update(node_id="node-07")
    assert waiting["phase"] == "ping"
    assert waiting["continue"] is True


def test_refuses_icann_hub_resolve_radio_callable() -> None:
    assert ping(public_icann=True)["code"] == "AZG-NOT-PUBLIC-REGISTRAR"
    assert ping(resolves_to_hub=True)["code"] == "BRIDGE-NO-HUB-RESOLVE"
    assert ping(radio_phy=True)["code"] == "AZG-NO-RADIO-PHY"
    assert ping(inbound_call=True)["code"] == "AZG-NOT-CALLABLE"
    assert ping(invent_first_flag=True)["code"] == "BRIDGE-NO-INVENT-HTTPS"
    assert ping(hardcoded_host="azgrid.az")["code"] == "CAP7-NO-HARDCODED-HOST"


def test_bridge_doors_and_app_worker_live() -> None:
    doors = hosted_bridge_doors()
    assert doors["code"] == "BRIDGE-CAP7-SHUFFLE"
    assert doors["app_worker"]["status"] == "live-app"
    assert doors["app_worker"]["cite"] is True
    assert doors["app_worker"]["url"] == APP_WORKER_HOST
    assert doors["honesty"]["app_worker"] == "LIVE"
    assert doors["honesty"]["aznet_side_https"] == "SLOT"
    assert doors["honesty"]["mesh_az_icann"] == "SLOT"
    assert doors["doors"]["bridge"].endswith("/bridge")
    assert doors["doors"]["update"].endswith("/v1/shuffle/update")
    assert doors["radio_phy"] is False
    assert doors["resolves_to_hub"] is False
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
    assert "resolves_to_hub: false" in APP_CAP7
    deploy = (ROOT / "workers/miragegrid/deploy.sh").read_text(encoding="utf-8")
    assert "--name miragegrid" in deploy
    pkg = (ROOT / "workers/miragegrid/package.json").read_text(encoding="utf-8")
    assert '"name": "miragegrid"' in pkg
    assert "wrangler deploy --name miragegrid --config wrangler.jsonc" in pkg
    ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "npx wrangler deploy --name miragegrid --dry-run" in ci
    assert "/v1/shuffle/update" in APP_INDEX
