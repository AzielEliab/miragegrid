"""Receipt fields, default dump omits receipt, forged node FAIL."""

from __future__ import annotations

import json

from miragegrid.canon import digest
from miragegrid.pool import NodePool
from miragegrid.receipt import Receipt
from miragegrid.session import MirageSession


def test_receipt_has_required_fields() -> None:
    with MirageSession() as session:
        rec = session.receipt
        assert rec.session_id == session.session_id
        assert 1 <= rec.mirage_node <= 25
        assert rec.timestamp.endswith("Z")
        assert rec.integrity == "PASS"
        assert rec.hash == rec.recomputed_hash()
        assert rec.hash_ok()


def test_default_dump_and_str_omit_receipt() -> None:
    with MirageSession() as session:
        text = str(session)
        dump = session.to_dict()
        payload = session.to_json()
        assert "receipt" not in dump
        assert "integrity" not in dump
        assert "receipt" not in payload
        assert "receipt" not in text.lower()
        assert "mirage_node" not in payload
        emitted = session.to_dict(include_receipt=True)
        assert "receipt" in emitted
        assert emitted["receipt"]["integrity"] == "PASS"


def test_integrity_fail_if_node_id_forged() -> None:
    pool = NodePool()
    with MirageSession(pool=pool) as session:
        good = session.receipt
    forged = Receipt(
        session_id=good.session_id,
        mirage_node=99,
        timestamp=good.timestamp,
        integrity="PASS",
        hash=digest(good.session_id, 99, good.timestamp, "PASS"),
    )
    assert forged.evaluate(pool) == "FAIL"
    # Tamper number but keep original hash:
    broken = Receipt(
        session_id=good.session_id,
        mirage_node=99,
        timestamp=good.timestamp,
        integrity="PASS",
        hash=good.hash,
    )
    assert broken.evaluate(pool) == "FAIL"
    assert good.evaluate(pool) == "PASS"


def test_receipt_json_roundtrip() -> None:
    with MirageSession() as session:
        rec = session.receipt
        loaded = Receipt.from_dict(json.loads(rec.to_json()))
        assert loaded == rec
