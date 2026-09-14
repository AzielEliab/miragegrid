"""Persistent mesh is connected; routes are deterministic.

SPLIT THE WIRES, COLD-COPY SURVIVAL, and REHEAL are locked law.
Author: Aziel Eliab only.
"""

from __future__ import annotations

import hashlib
import pytest

from miragegrid.mesh import (
    ASSIGN_LIVE,
    DWELL_S,
    MeshLawError,
    NodeMesh,
    TIP_TICK_SIZE,
    admit_payload,
    cite_update,
    data_outlives_creators,
    encode_tip_tick,
    equivocation_check,
    erase_tip,
    emit_last,
    heartbeat_loss,
    hosted_stub_refuse,
    mesh_law_dict,
    multiply_cold_copies,
    partition_rejoin,
    phoenix,
    poison_refuse,
    refuse_live_body_sync,
    reheal,
    select_circuit_indices,
    server_pull_wipe_cold,
    sockets_share,
)
from miragegrid.pool import POOL_SIZE, node_id_for
from miragegrid.rng import select_index


def test_mesh_connected_degree_and_path() -> None:
    mesh = NodeMesh()
    assert mesh.connected()
    assert len(mesh) == POOL_SIZE
    for i in range(POOL_SIZE):
        assert mesh.degree(i) == 6
    path = mesh.path(0, 12)
    assert path[0] == 0 and path[-1] == 12
    assert 1 <= len(path) <= 5
    ids = mesh.path_ids("node-01", "node-13")
    assert ids[0] == "node-01" and ids[-1] == "node-13"


def test_circuit_indices_use_section6_entry() -> None:
    entropy = b"\x11" * 32
    ts = "2026-03-04T13:02:12Z"
    hops = select_circuit_indices(entropy, ts, hops=3)
    assert hops[0] == select_index(entropy, ts)
    assert len(set(hops)) == 3
    assert all(0 <= h <= 24 for h in hops)
    again = select_circuit_indices(entropy, ts, hops=3)
    assert hops == again


def test_peer_fingerprints_stable() -> None:
    a = NodeMesh()
    b = NodeMesh()
    assert a.peer("node-07").fingerprint == b.peer("node-07").fingerprint
    assert a.peer("node-07").public_key != a.peer("node-08").public_key
    assert node_id_for(6) == "node-07"


def _h(n: int = 1) -> bytes:
    return hashlib.sha256(bytes([n])).digest()


def test_assign_stays_live_and_hosted_stubs_refuse() -> None:
    assert ASSIGN_LIVE is True
    assert hosted_stub_refuse("assign") is None
    for op in ("vpn", "hop", "tunnel", "vpn-hop", "/v1/mesh/tunnel"):
        got = hosted_stub_refuse(op)
        assert got and got["ok"] is False and got["code"] == "MESH-STUB"
        assert got["assign_live"] is True


def test_split_wires_tip_tick_fixed_size_no_body() -> None:
    blob = encode_tip_tick("live", _h(1))
    assert len(blob) == TIP_TICK_SIZE
    with pytest.raises(MeshLawError) as exc:
        encode_tip_tick("live", _h(1), extra={"body": b"nope"})
    assert exc.value.code == "STW-TIP-BODY"
    with pytest.raises(MeshLawError):
        encode_tip_tick("live", _h(1), extra={"diff": "x"})
    with pytest.raises(MeshLawError):
        encode_tip_tick("live", _h(1), extra={"file": "x"})


def test_payload_pull_only_never_fanout() -> None:
    ok = admit_payload(mode="pull", tip_hash=_h(2))
    assert ok["ok"] and ok["yes"]
    fan = admit_payload(mode="fanout", tip_hash=_h(2), fanout=True)
    assert fan["ok"] is False and fan["code"] == "STW-NO-FANOUT"
    push = admit_payload(mode="push", tip_hash=_h(2))
    assert push["code"] == "STW-NO-FANOUT"


def test_update_is_proof_not_timer() -> None:
    closed = cite_update(prev=None, tip=_h(3), lockset=None)
    assert closed["code"] == "STW-UPDATE-FAIL-CLOSED" and closed["yes"] is False
    desync = cite_update(prev=_h(1), tip=_h(2), lockset={"sealed": True}, clock_desync=True)
    assert desync["code"] == "STW-CLOCK-DESYNC" and desync["yes"] is False
    amb = cite_update(prev=_h(1), tip=_h(2), lockset={"sealed": True}, ambiguous=True)
    assert amb["verdict"] == "isolate"
    dwell = cite_update(prev=_h(1), tip=_h(2), lockset={"sealed": True}, dwell_elapsed_s=10)
    assert dwell["verdict"] == "dwell" and dwell["dwell_s"] == DWELL_S
    yes = cite_update(prev=_h(1), tip=_h(2), lockset={"sealed": True}, dwell_elapsed_s=777)
    assert yes["yes"] is True


def test_equivocation_ends_peer_quorum_not_truth() -> None:
    ev = equivocation_check(peer="node-03", prev=_h(1), tips=[_h(2), _h(3)], quorum_votes=99)
    assert ev["verdict"] == "lock" and ev["isolate"] is True
    assert ev["quorum_is_truth"] is False


def test_emit_phoenix_partition_and_sockets() -> None:
    assert emit_last(verified=False)["code"] == "STW-UNVERIFIED-BODY"
    assert emit_last(verified=True, unsend=True)["code"] == "STW-NO-UNSEND"
    assert emit_last(verified=True, local=True)["yes"] is True
    assert phoenix(failed_node="node-04", target="node-09")["code"] == "STW-PHOENIX-LOCAL"
    assert phoenix(failed_node="node-04")["verdict"] == "phoenix-wait"
    assert partition_rejoin(cite=None, operator=True, lockset={}, auto_splice=True)["code"] == "STW-NO-AUTO-SPLICE"
    assert partition_rejoin(cite=_h(4), operator=True, lockset={"sealed": True})["yes"] is True
    assert heartbeat_loss(mark_poison=True)["code"] == "STW-HB-NOT-POISON"
    assert heartbeat_loss(apply_last=True)["code"] == "STW-HB-NOT-APPLY"
    split = sockets_share("1s", "777s")
    assert split["ok"] is False and split["code"] == "STW-SOCKET-SPLIT"


def test_cold_copy_survival() -> None:
    assert multiply_cold_copies(1)["code"] == "CCS-MULTIPLY"
    assert multiply_cold_copies(2)["yes"] is True
    assert refuse_live_body_sync(live_body_sync=True)["code"] == "CCS-NO-LIVE-BODY-SYNC"
    assert erase_tip()["code"] == "CCS-TIP-EXPENSIVE"
    assert server_pull_wipe_cold()["code"] == "CCS-SERVER-PULL-NO-WIPE"
    poison = poison_refuse(claimed=_h(1), actual=_h(2))
    assert poison["code"] == "CCS-POISON-HASH"
    keep = data_outlives_creators(creator_gone=True)
    assert keep["kept"] is True and keep["yes"] is True


def test_reheal_own_tip_or_phoenix_wait_no_neighbor_talk() -> None:
    talk = reheal(source="neighbor", neighbor_talk=True)
    assert talk["ok"] is False and talk["code"] == "RH-NO-NEIGHBOR-TALK"
    vote = reheal(source="own-tip+trusted-pull", own_tip=_h(5), trusted_pull=True, vote_to_fix=True)
    assert vote["code"] == "RH-NO-VOTE-TO-FIX"
    body = reheal(source="own-tip+trusted-pull", own_tip=_h(5), fields={"diff": "x"})
    assert body["code"] == "RH-NO-BODY"
    wait = reheal(source="phoenix-wait", phoenix_wait=True)
    assert wait["verdict"] == "phoenix-wait" and wait["auto_heal"] is False
    own = reheal(source="own-tip+trusted-pull", own_tip=_h(5), trusted_pull=True, fields={"isolated": True, "tip_hash": _h(5).hex()})
    assert own["yes"] is True and own["auto_heal"] is False
    closed = reheal(source="gossip")
    assert closed["code"] == "RH-FAIL-CLOSED"


def test_mesh_dict_cites_locked_law() -> None:
    mesh = NodeMesh()
    doc = mesh.to_dict()
    law = mesh_law_dict()
    assert doc["assign_live"] is True
    assert doc["split_wires"]["law"] == "SPLIT THE WIRES"
    assert doc["cold_copy"]["law"] == "COLD-COPY SURVIVAL"
    assert doc["reheal"]["law"] == "REHEAL"
    assert law["reheal"]["neighbor_talk_dirty_back_to_health"] is False
    assert "Aziel Eliab" in law["author"]
    assert doc["az_generator"]["spec"] == "AZ-GENERATOR-1.0"
    assert doc["grid_shift"]["spec"] == "MIRAGE-GRID-SHIFT-1.0"
    assert doc["public_stack"]["pieces"] == ["anonymity-network", "node-gate", "auto-heal"]
    assert law["az_generator"]["clock"]["period_s"] == 497
    assert law["az_generator"]["softwares_tab"] is False
    assert law["grid_shift"]["softwares_tab"] is False
