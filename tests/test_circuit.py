"""Onion wrap/unwrap and key drop."""

from __future__ import annotations

import pytest

from miragegrid.circuit import Circuit, CircuitClosedError
from miragegrid.errors import MappingDestroyedError
from miragegrid.mesh import NodeMesh
from miragegrid.session import MirageSession


def test_onion_roundtrip_and_roles() -> None:
    mesh = NodeMesh()
    circ = Circuit.build(
        mesh,
        entropy=b"\x22" * 32,
        timestamp="2026-03-04T13:02:12Z",
        hops=3,
    )
    assert circ.entry.role == "entry"
    assert circ.exit.role == "exit"
    assert circ.entry.node_id != circ.exit.node_id
    msg = b"anonymity-payload"
    assert circ.unwrap(circ.wrap(msg)) == msg
    assert circ.path[0] == circ.entry.index
    assert circ.path[-1] == circ.exit.index


def test_session_circuit_destroyed() -> None:
    session = MirageSession(entropy=b"\x33" * 32, timestamp="2026-03-04T13:02:12Z")
    hops = session.circuit.hop_ids
    assert session.node.id == hops[0]
    assert session.integrity == "PASS"
    wrapped = session.wrap(b"x")
    assert session.unwrap(wrapped) == b"x"
    session.end()
    with pytest.raises(MappingDestroyedError):
        _ = session.circuit
    with pytest.raises(MappingDestroyedError):
        _ = session.node


def test_wrap_after_circuit_close() -> None:
    mesh = NodeMesh()
    circ = Circuit.build(
        mesh,
        entropy=b"\x44" * 32,
        timestamp="2026-03-04T13:02:12Z",
    )
    circ.close()
    with pytest.raises(CircuitClosedError):
        circ.wrap(b"nope")
