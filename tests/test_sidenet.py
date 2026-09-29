"""SIDENET-P2: Cap-7 mesh DNS, pairing-only, L0 public path unchanged.

Author: Aziel Eliab only.
"""

from __future__ import annotations

from miragegrid.az_generator import synthetic_papers
from miragegrid.cap7_shuffle import az_domain_rows, cap7_roster
from miragegrid.mesh import mesh_law_dict
from miragegrid.sidenet import (
    PUBLIC_BROWSER_GATEWAYS,
    is_public_browser_gateway,
    sidenet_access,
    sidenet_dict,
    sidenet_node_gate,
)


def test_l0_public_path_stays_az_domains_and_cap7_cite() -> None:
    doors = az_domain_rows()
    assert len(doors) == 4
    assert all(row["public_icann"] is True and row["internet_reachable"] is True for row in doors)
    roster = cap7_roster()
    assert len(roster) == 7
    assert all(row["public_icann"] is False for row in roster)
    assert all(row["browser_reachable"] is False for row in roster)
    assert all(row["internet_reachable"] is False for row in roster)


def test_sidenet_cite_is_not_icann_and_softwares_stay_frozen() -> None:
    law = sidenet_dict()
    assert law["code"] == "SIDENET-CITE"
    assert law["spec"] == "SIDENET-P2"
    assert law["layer"] == "P2"
    assert law["l0_public_path_changed"] is False
    assert law["l0"]["changed"] is False
    assert law["l0"]["az_domains_public_icann"] is True
    assert law["public_icann"] is False
    assert law["callable"] is False
    assert law["public_browser_gateways"] == list(PUBLIC_BROWSER_GATEWAYS)
    assert law["public_browser_gateways"] == ["azgrid", "azbooth"]
    assert len(law["public_browser_gateways"]) == 2
    assert law["softwares_frozen"] is True
    assert law["softwares_tab"] is False
    assert law["new_product"] is False
    assert law["access"]["pairing_only"] is True
    assert law["access"]["pairing_is_tunnel"] is False
    assert law["access"]["pair_verified_at_aznet"] is False
    assert law["hosted_node_gate_exec"] is False
    mesh = mesh_law_dict()
    assert mesh["sidenet"]["public_icann"] is False
    assert mesh["sidenet"]["l0_public_path_changed"] is False


def test_only_two_factory_labels_are_public_browser_gateways() -> None:
    assert is_public_browser_gateway("azgrid") is True
    assert is_public_browser_gateway("azbooth") is True
    assert is_public_browser_gateway("azgrid.az") is True
    for label in ("azcloak", "azvault", "azshift", "azflag", "azstandby"):
        assert is_public_browser_gateway(label) is False
    browser = sidenet_access(name="azgrid", client="browser")
    assert browser["code"] == "AZG-ACCESS-PUBLIC-GATEWAY"
    assert browser["public_icann"] is False
    assert browser["public_browser_gateway"] is True
    assert browser["internet_reachable"] is False
    booth = sidenet_access(name="azbooth", client="https")
    assert booth["ok"] is True
    cloak = sidenet_access(name="azcloak", client="browser")
    assert cloak["code"] == "AZG-PUBLIC-PAIR"
    assert cloak["public_icann"] is False


def test_pairing_requires_token_and_azbrowser_flag() -> None:
    missing = sidenet_access(name="azcloak", client="aznet")
    assert missing["code"] == "SIDENET-NEED-PAIR"
    assert "pair_token" in missing["missing"]
    assert "azbrowser_flag" in missing["missing"]
    word = sidenet_access(name="azcloak", client="aznet", pair_token="true", flag="azbrowser")
    assert word["code"] == "SIDENET-NEED-PAIR"
    one = sidenet_access(name="azvault.az", client="azbrowser", pair_token="pair-token-1")
    assert one["code"] == "SIDENET-NEED-PAIR"
    assert one["missing"] == ["azbrowser_flag"]
    paired = sidenet_access(
        name="azcloak",
        client="azbrowser",
        pair_token="pair-token-1",
        flag="azbrowser",
    )
    assert paired["code"] == "SIDENET-PAIR-OK"
    assert paired["public_icann"] is False
    assert paired["pairing_is_tunnel"] is False
    assert paired["pair_verified_at_aznet"] is False
    assert paired["this_surface_verifies_aznet_token"] is False
    assert paired["hosts_payloads"] is False
    assert paired["merge"] is False
    assert paired["public_browser_gateway"] is False
    mesh_name = sidenet_access(
        name="www.survivalnetwork.az",
        client="aznet",
        pairing_token="pair-token-2",
        pair_peer="azbrowser",
    )
    assert mesh_name["code"] == "SIDENET-PAIR-OK"
    assert mesh_name["public_browser_gateway"] is False


def test_honest_refuses_for_icann_merge_tunnel_and_fake_verification() -> None:
    icann = sidenet_access(name="azgrid", client="aznet", public_icann=True, pair_token="t", flag="azbrowser")
    assert icann["code"] == "AZG-NOT-PUBLIC-REGISTRAR"
    assert icann["public_icann"] is False
    merge = sidenet_access(name="azgrid", client="aznet", merge=True, pair_token="t", flag="azbrowser")
    assert merge["code"] == "AZG-NO-MERGE-PRODUCTS"
    tunnel = sidenet_access(name="azcloak", client="aznet", pairing_is_tunnel=True, pair_token="t", flag="azbrowser")
    assert tunnel["code"] == "CAP7-NO-VPN-LIE"
    assert tunnel["pairing_is_tunnel"] is False
    lie = sidenet_access(
        name="azcloak",
        client="aznet",
        pair_token="t",
        flag="azbrowser",
        pair_verified_at_aznet=True,
    )
    assert lie["code"] == "SIDENET-NO-VERIFIED-LIE"
    assert lie["pair_verified_at_aznet"] is False
    payload = sidenet_access(name="azcloak", client="aznet", hosts_payloads=True, pair_token="t", flag="azbrowser")
    assert payload["code"] == "SIDENET-NO-PAYLOAD-HOST"
    frozen = sidenet_access(name="azgrid", client="browser", new_product=True)
    assert frozen["code"] == "SIDENET-SOFTWARE-FROZEN"
    hub = sidenet_access(name="godlock.uk", client="aznet", pair_token="t", flag="azbrowser")
    assert hub["code"] == "MGS-NOT-NODE-GATE"
    tld = sidenet_access(name="spare.com", client="aznet", pair_token="t", flag="azbrowser")
    assert tld["code"] == "AZG-TLD"
    naked = sidenet_access(name="azcloak", client="curl", pair_token="t", flag="azbrowser")
    assert naked["code"] == "AZG-NO-NAKED-DNS"


def test_hosted_node_gate_refuses_and_local_claim_plant_flag_restore() -> None:
    claim = sidenet_node_gate(action="claim", hosted=True)
    assert claim["code"] == "AZG-NOT-CALLABLE"
    assert claim["public_icann"] is False
    assert claim["callable"] is False
    assert claim["lives"] == "deep-node"
    plant = sidenet_node_gate(action="plant", hosted=True, name="spare.az")
    assert plant["code"] == "MGS-NO-HOSTED-PLANT"
    assert plant["hosted_plant"] is False
    flag = sidenet_node_gate(action="flag", hosted=True, fake_flag=True)
    assert flag["code"] == "NO-FAN-FALSIFY"
    restore = sidenet_node_gate(action="restore", hosted=True)
    assert restore["code"] == "AZG-NOT-CALLABLE"
    icann = sidenet_node_gate(action="claim", hosted=False, public_icann=True)
    assert icann["code"] == "AZG-NOT-PUBLIC-REGISTRAR"

    papers = synthetic_papers(49)
    local = sidenet_node_gate(action="claim", hosted=False, papers=papers, origin_node="node-01", now_s=0)
    assert local["code"] == "AZG-FIRST-CLAIM"
    assert local["name"] == "www.survivalnetwork.az"
    assert local["public_icann"] is False
    assert local["exit"] == "node-gate-front"
    short = sidenet_node_gate(action="restore", hosted=False, papers=synthetic_papers(48), broken=True)
    assert short["ok"] is False
    assert short["code"] in {"AZG-PAPERS", "AZG-INCOMPLETE-VAULT"}
    restored = sidenet_node_gate(
        action="restore",
        hosted=False,
        papers=papers,
        broken=True,
        most_active_point="tip-3",
    )
    assert restored["code"] == "AZG-RESTORE-OK"
    assert restored["vault_complete"] is True
    invented = sidenet_node_gate(
        action="plant",
        hosted=False,
        name="not-yet.az",
        zone_names=["www.survivalnetwork.az"],
    )
    assert invented["code"] == "SIDENET-PLANT-NEEDS-CLAIM"
    planted = sidenet_node_gate(
        action="plant",
        hosted=False,
        name="www.survivalnetwork.az",
        zone_names=["www.survivalnetwork.az"],
    )
    assert planted["code"] == "AZG-FLAG-REPOST"
    assert planted["flag"] is True
    repost = sidenet_node_gate(action="flag", hosted=False, zone_names=["www.survivalnetwork.az"])
    assert repost["code"] == "AZG-FLAG-REPOST"
    assert repost["rewrite"] is False
