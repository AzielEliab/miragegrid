"""Persistent mesh is connected; routes are deterministic."""

from __future__ import annotations

from miragegrid.mesh import NodeMesh, select_circuit_indices
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
