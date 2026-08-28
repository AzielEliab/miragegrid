"""Session assigns a pool node; mapping gone after close; independence."""

from __future__ import annotations

import threading

import pytest

from miragegrid.errors import MappingDestroyedError
from miragegrid.pool import NodePool
from miragegrid.session import MirageSession


def test_session_assigns_a_node_from_the_pool() -> None:
    pool = NodePool()
    with MirageSession(pool=pool) as session:
        node = session.node
        assert pool.contains(node.id)
        assert node in pool.nodes or node.id in {n.id for n in pool}
        assert session.integrity == "PASS"
        assert session.session_id


def test_after_close_mapping_gone() -> None:
    session = MirageSession()
    _ = session.node
    session.end()
    assert session.closed is True
    assert session._node is None
    with pytest.raises(MappingDestroyedError):
        _ = session.node
    assert session.integrity == "FAIL"


def test_context_manager_destroys_mapping() -> None:
    with MirageSession() as session:
        assert session.node.id.startswith("node-")
    with pytest.raises(MappingDestroyedError):
        _ = session.node


def test_two_sessions_can_differ() -> None:
    ids = []
    nodes = []
    for _ in range(50):
        with MirageSession() as session:
            ids.append(session.session_id)
            nodes.append(session.node.id)
    assert len(set(ids)) == 50
    assert len(set(nodes)) > 1


def test_200_sessions_cover_multiple_nodes() -> None:
    seen = set()
    for _ in range(200):
        with MirageSession() as session:
            seen.add(session.node.id)
    assert len(seen) > 1
    assert seen <= {f"node-{i:02d}" for i in range(1, 26)}


def test_two_concurrent_sessions_independent() -> None:
    results: list[tuple[str, str]] = []

    def worker() -> None:
        with MirageSession() as session:
            results.append((session.session_id, session.node.id))

    t1 = threading.Thread(target=worker)
    t2 = threading.Thread(target=worker)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert len(results) == 2
    assert results[0][0] != results[1][0]
    with MirageSession() as a:
        with MirageSession() as b:
            assert a.session_id != b.session_id
            assert a.node is not b.node
