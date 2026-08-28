"""Pool has 25 unique logical nodes."""

from __future__ import annotations

from miragegrid.pool import POOL_SIZE, NodePool, node_id_for, node_label_for


def test_pool_has_25_unique_nodes() -> None:
    pool = NodePool()
    assert len(pool) == 25
    assert POOL_SIZE == 25
    ids = [n.id for n in pool]
    labels = [n.label for n in pool]
    assert len(set(ids)) == 25
    assert len(set(labels)) == 25
    assert ids[0] == "node-01"
    assert ids[-1] == "node-25"
    assert labels[0] == "Node01"
    assert labels[-1] == "Node25"
    assert pool[0].number == 1
    assert pool[24].number == 25
    assert node_id_for(0) == "node-01"
    assert node_label_for(13) == "Node14"


def test_optional_endpoint_is_label_only() -> None:
    pool = NodePool(endpoints={"node-01": "booth-alpha"})
    assert pool.by_id("node-01").endpoint == "booth-alpha"
    assert pool.by_id("node-02").endpoint is None
    assert not hasattr(pool, "connect")
    assert not hasattr(pool.by_id("node-01"), "connect")
