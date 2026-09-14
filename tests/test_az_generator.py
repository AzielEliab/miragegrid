"""AZ-GENERATOR-1.0 and MIRAGE-GRID-SHIFT-1.0 locked law.

Clock: 7m + 77s = 497s. Cap-7. First claim www.survivalnetwork.az.
Restore needs ≥49 Aziel Eliab papers. Offline downloads stay up.
Author: Aziel Eliab only.
"""

from __future__ import annotations

import hashlib

import pytest

from miragegrid.mesh import (
    AIRGAP_SPEC,
    CAP_7,
    CLAIM_CLOCK_S,
    CLAIM_EXTRA_S,
    CLAIM_MINUTES,
    FIRST_CLAIM_NAME,
    MIN_PAPERS,
    TIP_TICK_FORBIDDEN,
    airgap_dict,
    airgap_mode,
    airgap_reheal,
    auto_heal,
    az_generator_dict,
    claim_az_domain,
    claim_clock_period_s,
    cloak_burst,
    count_aziel_papers,
    count_vault_papers,
    encode_tip_tick,
    grid_shift,
    grid_shift_dict,
    known_contains_first_claim,
    mesh_law_dict,
    node_gate_admit,
    offline_download_stay_up,
    paper_vault_dict,
    plant_flag_and_repost,
    public_stack_dict,
    refuse_ambiguity,
    refuse_falsify,
    refuse_hub_tunnel_hydra,
    refuse_incomplete_vault,
    refuse_misleading,
    refuse_no_fan,
    refuse_paper_body_on_tip,
    restore_chain,
    sockets_share,
    vault_complete,
    vault_multiply,
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


def _hash_only(n: int) -> list[dict]:
    out = []
    for i in range(n):
        body = f"aziel-eliab-paper-{i}".encode("utf-8")
        out.append(
            {
                "author": "Aziel Eliab",
                "hash": hashlib.sha256(body).hexdigest(),
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
    assert law["no_fan"]["spec"] == "NO-FAN-1.0"
    assert law["no_fan"]["phrase"] == "No falsification. No ambiguity. No misleading."
    assert law["no_lie"] is True
    assert law["no_rewrite"] is True


def test_no_fan_refuses_falsify_ambiguous_misleading_verbs() -> None:
    fake = refuse_no_fan("falsify")
    assert fake and fake["code"] == "NO-FAN-FALSIFY" and fake["ok"] is False
    assert fake["phrase"] == "No falsification. No ambiguity. No misleading."
    assert refuse_falsify(kind="false-tip")["code"] == "NO-FAN-FALSIFY"
    assert refuse_no_fan("false-receipt")["code"] == "NO-FAN-FALSIFY"
    assert refuse_no_fan("false-live-nodes")["code"] == "NO-FAN-FALSIFY"
    assert refuse_no_fan("false-site-up")["code"] == "NO-FAN-FALSIFY"
    amb = refuse_no_fan("ambiguous")
    assert amb and amb["code"] == "NO-FAN-AMBIGUITY" and amb["verdict"] == "isolate"
    assert refuse_ambiguity()["quorum_is_truth"] is False
    assert refuse_no_fan("dual-tip")["code"] == "NO-FAN-AMBIGUITY"
    assert refuse_no_fan("pretty-copy")["code"] == "NO-FAN-AMBIGUITY"
    mis = refuse_misleading(kind="pretend-hub-cell")
    assert mis["code"] == "NO-FAN-MISLEAD"
    assert refuse_no_fan("neighbor-resurrection")["code"] == "NO-FAN-MISLEAD"
    assert refuse_no_fan("clear") is None


def test_unverified_tip_and_fake_flag_refuse_continuity() -> None:
    unverified = claim_az_domain(origin_node="node-01", tip_verified=False)
    assert unverified["code"] == "AZG-UNVERIFIED-TIP"
    assert unverified["false_tip"] is False
    invent = claim_az_domain(origin_node="node-01", invent_continuity=True)
    assert invent["code"] == "NO-FAN-FALSIFY"
    resume = claim_az_domain(origin_node="node-01", claimable=False)
    assert resume["code"] == "AZG-FIRST-CLAIM-RESUME"
    assert resume["fake_flag"] is False
    fake = plant_flag_and_repost(sites=["www.survivalnetwork.az"], fake_flag=True)
    assert fake["code"] == "NO-FAN-FALSIFY"
    hub = grid_shift(domain_pulled="godlock.uk", az_name="standby.az", pretend_hub_cell=True)
    assert hub["code"] == "NO-FAN-MISLEAD"
    risen = grid_shift(domain_pulled="godlock.uk", az_name="standby.az", neighbor_resurrection=True)
    assert risen["code"] == "NO-FAN-MISLEAD"


def test_incomplete_vault_refuses_restore_and_claim() -> None:
    hashes = _hash_only(49)
    assert count_aziel_papers(hashes) == 49
    assert count_vault_papers(hashes) == 0
    assert vault_complete(hashes) is False
    held = restore_chain(papers=hashes, broken=True)
    assert held["ok"] is False
    assert held["code"] == "AZG-INCOMPLETE-VAULT"
    assert held["verdict"] == "phoenix-wait"
    assert held["unverified_tip"] is True
    assert held["code_alias"] == "AZG-UNVERIFIED-TIP"
    fake = restore_chain(papers=hashes, broken=True, have_49=True)
    assert fake["code"] == "NO-FAN-FALSIFY"
    claim = claim_az_domain(
        origin_node="node-04",
        known_sites=["https://www.survivalnetwork.az/"],
        name="spare.az",
        papers=hashes,
        needs_papers=True,
    )
    assert claim["ok"] is False
    assert claim["code"] in {"AZG-INCOMPLETE-VAULT", "AZG-UNVERIFIED-TIP", "NO-FAN-FALSIFY", "AZG-PAPERS"}
    lied = claim_az_domain(
        origin_node="node-04",
        known_sites=["https://www.survivalnetwork.az/"],
        name="spare.az",
        papers=hashes,
        have_49=True,
        needs_papers=True,
    )
    assert lied["code"] == "NO-FAN-FALSIFY"
    empty = refuse_incomplete_vault(papers=_hash_only(49))
    assert empty and empty["code"] == "AZG-INCOMPLETE-VAULT"
    ok = restore_chain(papers=_papers(49), broken=True, most_active_point="tip-9")
    assert ok["yes"] is True
    assert ok["vault_complete"] is True


def test_vault_multiply_cold_copies_not_tip_tick() -> None:
    papers = _papers(49)
    for event in ("bootstrap", "join", "cap-7-claim", "grid-shift-standby"):
        landed = vault_multiply(event=event, papers=papers)
        assert landed["yes"] is True
        assert landed["code"] == "AZG-VAULT-MULTIPLY"
        assert landed["live_body_sync"] is False
        assert landed["tip_tick_bodies"] is False
        assert landed["plane"] == "pull-only"
        assert landed["cold_copy"] is True
    fan = vault_multiply(event="join", papers=papers, live_body_sync=True)
    assert fan["code"] == "STW-NO-FANOUT"
    tick = vault_multiply(event="bootstrap", papers=papers, tip_tick=True)
    assert tick["code"] == "STW-TIP-BODY"
    short = vault_multiply(event="join", papers=_papers(12))
    assert short["code"] == "AZG-INCOMPLETE-VAULT"
    assert short["verdict"] == "phoenix-wait"
    body = refuse_paper_body_on_tip(extra={"papers": papers})
    assert body and body["code"] == "STW-TIP-BODY"
    assert "papers" in TIP_TICK_FORBIDDEN
    with pytest.raises(Exception) as exc:
        encode_tip_tick("live", hashlib.sha256(b"t").digest(), extra={"papers": papers})
    assert exc.value.code == "STW-TIP-BODY"


def test_airgap_mode_constants_and_refuses() -> None:
    law = airgap_dict()
    assert law["spec"] == AIRGAP_SPEC
    assert law["local_vault"] is True
    assert law["bearer_radios"] is False
    assert law["climb_back_pulled_hubs"] is False
    assert law["downloads_from_local_cold_shelf"] is True
    assert law["body_gossip"] is False
    assert law["official_hubs_are_airgap_node_gate"] is False
    assert law["neighbor_majority"] is False
    ok = airgap_mode(enabled=True, vault_papers=_papers(49))
    assert ok["yes"] is True
    assert ok["code"] == "AIRGAP-OK"
    assert ok["downloads_from_local_cold_shelf"] is True
    assert airgap_mode(bearer_radios=True)["code"] == "AIRGAP-NO-BEARER"
    assert airgap_mode(climb_back=True)["code"] == "AIRGAP-NO-CLIMB-BACK"
    assert airgap_mode(body_gossip=True)["code"] == "AIRGAP-NO-BODY-GOSSIP"
    assert airgap_mode(neighbor_majority=True)["code"] == "RH-NO-VOTE-TO-FIX"
    assert airgap_mode(hub_as_gate="godlock.uk")["code"] == "MGS-NOT-NODE-GATE"
    assert airgap_mode(hub_as_gate="azieleliab.com")["code"] == "MGS-NOT-NODE-GATE"
    assert airgap_mode(hub_as_gate="azielcorpuslibrary.net")["code"] == "MGS-NOT-NODE-GATE"
    assert airgap_mode(hub_as_gate="hedidntjump.com")["code"] == "MGS-NOT-NODE-GATE"
    incomplete = airgap_mode(vault_papers=_hash_only(49))
    assert incomplete["code"] == "AZG-INCOMPLETE-VAULT"
    wait = airgap_reheal(phoenix_wait=True)
    assert wait["verdict"] == "phoenix-wait"
    own = airgap_reheal(own_tip=hashlib.sha256(b"own").digest(), trusted_pull=True, already_trusted=True)
    assert own["yes"] is True
    untrusted = airgap_reheal(own_tip=hashlib.sha256(b"own").digest(), trusted_pull=True, already_trusted=False)
    assert untrusted["ok"] is False
    mesh = mesh_law_dict()
    assert mesh["airgap"]["spec"] == "AIRGAP-1.0"
    assert mesh["paper_vault"]["on_every_node"] is True
    assert mesh["paper_vault"]["no_have_49_without_bytes"] is True
    assert paper_vault_dict()["multiply"] == "cold-copy"
    assert az_generator_dict()["paper_vault"]["on_every_node"] is True
    assert grid_shift_dict()["official_hubs_are_node_gate"] is False


def test_incomplete_vault_cap8_first_claim_clocks_no_fan_and_factory() -> None:
    from miragegrid.az_generator import (
        PUBLIC_HOST_PAIR,
        AzGenerator,
        DeepNode,
        MeshDnsZone,
        PaperVault,
        access_name,
        attempt_claim,
        claim_clock_ready,
        refuse_call_generator,
        refuse_icann_tld,
        refuse_naked_dns,
        refuse_product_merge,
        refuse_public_registrar,
        synthetic_papers,
        vault_live_sync_on_tip,
        vault_multiply,
    )
    from miragegrid.mesh import first_claim_for_suffix, select_claim_suffix

    vault48 = PaperVault(synthetic_papers(48))
    assert vault48.complete() is False
    held = attempt_claim(origin_node="node-01", vault=vault48)
    assert held["code"] == "AZG-INCOMPLETE-VAULT"
    assert held["verdict"] == "phoenix-wait"
    assert held["false_tip"] is False
    papers = claim_az_domain(origin_node="node-01", papers=_papers(48), known_sites=["https://www.survivalnetwork.az/"])
    assert papers["code"] == "AZG-INCOMPLETE-VAULT"

    vault = PaperVault()
    boot = vault.bootstrap(synthetic_papers(49))
    assert boot["yes"] is True
    assert vault.complete() is True
    assert vault_multiply(reason="tip-tick")["code"] == "AZG-VAULT-MULTIPLY"
    assert vault_live_sync_on_tip(live_body_sync=True)["code"] == "AZG-AIRGAP"

    node = DeepNode("node-03", vault=vault)
    assert node.call_generator()["code"] == "AZG-NOT-CALLABLE"
    assert node.generator.call()["code"] == "AZG-NOT-CALLABLE"
    assert refuse_call_generator()["lives"] == "deep-node"

    first = node.tick(now_s=0)
    assert first["code"] == "AZG-FIRST-CLAIM"
    assert first["name"] == "www.survivalnetwork.az"
    assert first["exit"] == "node-gate-front"
    assert first["public_icann"] is False
    assert first["receipt"]["hash"]
    hold = node.tick(now_s=100)
    assert hold["code"] == "AZG-CLOCK-HOLD"
    second = node.tick(now_s=497, name="spare-two.az")
    assert second["ok"] is True
    assert len(node.generator.zone.public_hosts()) == PUBLIC_HOST_PAIR
    third = node.tick(now_s=994, name="mesh-only-three.az")
    assert third["ok"] is True
    assert third["public_host"] is False
    assert "mesh-only-three.az" in node.generator.zone.mesh_only()
    assert access_name(name="www.survivalnetwork.az", client="aznet", zone=node.generator.zone)["code"] == "AZG-ACCESS-MESH"
    assert access_name(name="www.survivalnetwork.az", client="browser", zone=node.generator.zone)["code"] == "AZG-ACCESS-PUBLIC-GATEWAY"
    assert access_name(name="mesh-only-three.az", client="browser", zone=node.generator.zone)["code"] == "AZG-PUBLIC-PAIR"
    assert access_name(name="www.survivalnetwork.az", client="aznet", zone=node.generator.zone, merge_products=True)["code"] == "AZG-NO-MERGE-PRODUCTS"
    assert refuse_naked_dns()["code"] == "AZG-NO-NAKED-DNS"
    assert refuse_product_merge()["merge"] is False

    for i, extra in enumerate(("d.az", "e.az", "f.az", "g.az")):
        filled = node.tick(now_s=497 * (3 + i), name=extra)
        assert filled["ok"] is True
    eighth = node.tick(now_s=497 * 8, name="spare-eight.az")
    assert eighth["code"] == "AZG-CAP-7"

    assert refuse_icann_tld("spare.com")["code"] == "AZG-TLD"
    assert refuse_public_registrar()["cctld_takeover"] is False
    assert claim_az_domain(origin_node="node-01", public_registrar=True)["code"] == "AZG-NOT-PUBLIC-REGISTRAR"
    assert claim_az_domain(origin_node="node-01", inbound_call=True)["code"] == "AZG-NOT-CALLABLE"

    az = select_claim_suffix(az_usable=True)
    assert az["suffix"] == ".az" and first_claim_for_suffix(".az") == "www.survivalnetwork.az"
    aziel = select_claim_suffix(az_usable=False, aziel_usable=True)
    assert aziel["suffix"] == ".aziel" and aziel["first_claim"] == "www.survivalnetwork.aziel"
    assert aziel["pretended_az"] is False
    pivot = select_claim_suffix(az_usable=False, aziel_usable=False, pivot_suffix=".mesh")
    assert pivot["code"] == "AZG-SUFFIX-PIVOT"
    assert pivot["first_claim"] == "www.survivalnetwork.mesh"
    assert pivot["pretended_aziel"] is False
    none = select_claim_suffix(az_usable=False, aziel_usable=False)
    assert none["code"] == "AZG-SUFFIX-NONE"
    icann_pivot = select_claim_suffix(az_usable=False, aziel_usable=False, pivot_suffix=".com")
    assert icann_pivot["code"] == "AZG-SUFFIX-NONE"

    gen = AzGenerator("node-04", vault=PaperVault(synthetic_papers(49)))
    gen.set_suffix_availability(az_usable=False, aziel_usable=True)
    flag = gen.tick(now_s=0)
    assert flag["name"] == "www.survivalnetwork.aziel"
    assert flag["suffix"] == ".aziel"
    dead = claim_az_domain(origin_node="node-04", az_usable=False, aziel_usable=True, claimable=False)
    assert dead["code"] == "AZG-FIRST-CLAIM-RESUME"
    assert dead["fake_flag"] is False
    assert dead["first_claim"] == "www.survivalnetwork.aziel"

    zone = MeshDnsZone("node-05")
    zone.publish(name="a.az")
    zone.publish(name="b.az")
    zone.publish(name="c.az")
    assert zone.designate_public_pair(["a.az"])["code"] == "AZG-PUBLIC-PAIR"
    assert zone.designate_public_pair(["a.az", "b.az", "c.az"])["code"] == "AZG-PUBLIC-PAIR"
    ok_pair = zone.designate_public_pair(["a.az", "b.az"])
    assert ok_pair["yes"] is True
    assert zone.public_hosts() == ["a.az", "b.az"]
    assert "NOT ICANN" in zone.zone_file()
    assert claim_clock_ready(now_s=10, last_tick_s=0)["code"] == "AZG-CLOCK-HOLD"
    law = az_generator_dict()
    assert law["callable"] is False
    assert law["dns_factory"] == "cap-7-mesh-authoritative"
    assert law["public_host_pair"] == 2
    assert law["suffix_order"][0] == ".az"
