"""AZ-GENERATOR-1.0 and MIRAGE-GRID-SHIFT-1.0 locked law.

Clock: 7m + 77s = 497s. Cap-7. First claim www.survivalnetwork.az.
Restore needs ≥49 Aziel Eliab papers. Offline downloads stay up.
Author: Aziel Eliab only.
"""

from __future__ import annotations

import hashlib

from miragegrid.mesh import (
    CAP_7,
    CLAIM_CLOCK_S,
    CLAIM_EXTRA_S,
    CLAIM_MINUTES,
    FIRST_CLAIM_NAME,
    MIN_PAPERS,
    auto_heal,
    az_generator_dict,
    claim_az_domain,
    claim_clock_period_s,
    cloak_burst,
    count_aziel_papers,
    grid_shift,
    grid_shift_dict,
    known_contains_first_claim,
    mesh_law_dict,
    node_gate_admit,
    offline_download_stay_up,
    plant_flag_and_repost,
    public_stack_dict,
    refuse_hub_tunnel_hydra,
    restore_chain,
    sockets_share,
)


def _h(n: int) -> bytes:
    return hashlib.sha256(bytes([n])).digest()


def _papers(n: int) -> list[dict]:
    out = []
    for i in range(n):
        body = f"aziel-eliab-paper-{i}".encode("utf-8")
        out.append(
            {
                "author": "Aziel Eliab",
                "hash": hashlib.sha256(body).hexdigest(),
                "bytes": body,
            }
        )
    return out


def test_claim_clock_is_7m77s_equals_497s() -> None:
    assert CLAIM_MINUTES == 7
    assert CLAIM_EXTRA_S == 77
    assert CLAIM_CLOCK_S == 420 + 77 == 497
    assert claim_clock_period_s() == 497
    law = az_generator_dict()
    assert law["clock"]["period_s"] == 497
    assert law["clock"]["minutes"] == 7
    assert law["clock"]["extra_s"] == 77
    assert law["clock"]["alias"] == "7m77s"
    assert law["softwares_tab"] is False


def test_three_clocks_are_strangers() -> None:
    assert sockets_share("1s", "777s")["code"] == "STW-SOCKET-SPLIT"
    assert sockets_share("1s", "7m77s")["code"] == "STW-SOCKET-SPLIT"
    assert sockets_share("777s", "497s")["code"] == "STW-SOCKET-SPLIT"
    assert sockets_share("tip-1s", "claim-7m77s")["code"] == "STW-SOCKET-SPLIT"
    assert sockets_share("1s", "1s")["yes"] is True


def test_cap_7_refuses_eighth_name() -> None:
    assert CAP_7 == 7
    ok = claim_az_domain(
        origin_node="node-03",
        known_sites=["https://www.survivalnetwork.az/"],
        claimed=6,
        name="spare-seven.az",
    )
    assert ok["yes"] is True
    assert ok["hosted_by"] == "node-03"
    eighth = claim_az_domain(
        origin_node="node-03",
        known_sites=["https://www.survivalnetwork.az/"],
        claimed=7,
        name="spare-eight.az",
    )
    assert eighth["ok"] is False
    assert eighth["code"] == "AZG-CAP-7"


def test_first_claim_is_survivalnetwork_az() -> None:
    assert FIRST_CLAIM_NAME == "www.survivalnetwork.az"
    assert known_contains_first_claim([]) is False
    assert known_contains_first_claim(["https://other.az/"]) is False
    assert known_contains_first_claim(["https://www.survivalnetwork.az/home"]) is True
    first = claim_az_domain(origin_node="node-01", known_sites=[])
    assert first["code"] == "AZG-FIRST-CLAIM"
    assert first["name"] == "www.survivalnetwork.az"
    assert first["hosted_by"] == "node-01"
    resume = claim_az_domain(origin_node="node-01", known_sites=[], claimable=False)
    assert resume["code"] == "AZG-FIRST-CLAIM-RESUME"
    assert resume["resume"] is True


def test_fewer_than_49_papers_refuses_false_tip() -> None:
    assert MIN_PAPERS == 49
    assert count_aziel_papers(_papers(48)) == 48
    held = restore_chain(papers=_papers(48), broken=True)
    assert held["ok"] is False
    assert held["code"] == "AZG-PAPERS"
    assert held["verdict"] == "phoenix-wait"
    assert held["false_tip"] is False
    ok = restore_chain(papers=_papers(49), broken=True, most_active_point="tip-7")
    assert ok["yes"] is True
    assert ok["code"] == "AZG-RESTORE-OK"
    assert ok["cite_dont_merge"] is True
    merged = _papers(49) + _papers(49)[:3]
    assert count_aziel_papers(merged) == 49


def test_offline_origin_downloads_stay_up() -> None:
    stay = offline_download_stay_up(origin_offline=True)
    assert stay["yes"] is True
    assert stay["downloads_stay_up"] is True
    assert stay["download_plane"] == "pull-only"
    assert stay["tip_plane"] in {"isolated", "locked"}
    refuse = offline_download_stay_up(origin_offline=True, download_plane="fanout")
    assert refuse["ok"] is False


def test_auto_heal_is_lawful_reheal_not_vote() -> None:
    vote = auto_heal(vote_to_fix=True, labeled_auto_heal=True)
    assert vote["ok"] is False
    assert vote["code"] == "RH-NO-VOTE-TO-FIX"
    own = auto_heal(source="own-tip+trusted-pull", own_tip=_h(9), trusted_pull=True)
    assert own["yes"] is True
    assert own["suite_mesh_auto_heal"] is False
    assert own["auto_heal"] is False
    wait = auto_heal(source="phoenix-wait", phoenix_wait=True)
    assert wait["verdict"] == "phoenix-wait"


def test_node_gate_is_az_only_not_official_hubs() -> None:
    assert node_gate_admit(name="godlock.uk")["code"] == "MGS-NOT-NODE-GATE"
    assert node_gate_admit(name="azieleliab.com")["code"] == "MGS-NOT-NODE-GATE"
    assert node_gate_admit(name="www.azielcorpuslibrary.net")["code"] == "MGS-NOT-NODE-GATE"
    assert node_gate_admit(name="hedidntjump.com")["code"] == "MGS-NOT-NODE-GATE"
    assert node_gate_admit(name="example.com")["code"] == "MGS-AZ-ONLY"
    ok = node_gate_admit(name="www.survivalnetwork.az")
    assert ok["yes"] is True
    assert ok["softwares_tab"] is False
    assert ok["product"] == "miragegrid"


def test_grid_shift_and_cloak_burst() -> None:
    shift = grid_shift(domain_pulled="example.net", az_name="standby.az", cloak=True)
    assert shift["yes"] is True
    assert shift["answerable"] is True
    assert shift["node_cloaked"] is True
    assert shift["resurrection"] is False
    no = grid_shift(domain_pulled="godlock.uk", az_name="godlock.uk", resurrect_hub=True)
    assert no["code"] == "MGS-NO-HUB-RESURRECT"
    burst = cloak_burst(
        origin_node="node-02",
        names=["a.az", "b.az"],
        heal_fired=True,
        already_claimed=0,
    )
    assert burst["yes"] is True
    assert burst["cloak"] is True
    over = cloak_burst(
        origin_node="node-02",
        names=["n1.az", "n2.az", "n3.az", "n4.az", "n5.az", "n6.az", "n7.az", "n8.az"],
        heal_fired=True,
    )
    assert over["code"] == "AZG-CAP-7"
    hydra = refuse_hub_tunnel_hydra(host="godlock.uk", unmarked=True)
    assert hydra["code"] == "MGS-HUB-TUNNEL-HYDRA"


def test_flag_repost_and_public_stack() -> None:
    flag = plant_flag_and_repost(sites=["www.survivalnetwork.az"], node_data={"sites": ["other.az"]})
    assert flag["yes"] is True
    assert flag["flag"] is True
    stack = public_stack_dict()
    assert stack["pieces"] == ["anonymity-network", "node-gate", "auto-heal"]
    assert stack["az_generator_softwares_tab"] is False
    assert stack["node_gate_softwares_tab"] is False
    law = mesh_law_dict()
    assert law["az_generator"]["spec"] == "AZ-GENERATOR-1.0"
    assert law["grid_shift"]["spec"] == "MIRAGE-GRID-SHIFT-1.0"
    assert law["reheal"]["mesh_reheal"] == "MESH-REHEAL"
    assert grid_shift_dict()["mesh_vault"]["role"] == "ip-mask-host"
    assert "Aziel Eliab" in law["author"]
