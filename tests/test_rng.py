"""select_index is deterministic, in range, and not stdlib random."""

from __future__ import annotations

import ast
from pathlib import Path

from miragegrid.rng import POOL_SIZE, seed_bytes, select_index


TS = "2026-03-04T13:02:12Z"
RNG = Path(__file__).resolve().parents[1] / "miragegrid" / "rng.py"


def test_select_index_deterministic_and_range() -> None:
    entropy = b"\x11" * 32
    a = select_index(entropy, TS)
    b = select_index(entropy, TS)
    assert a == b
    assert 0 <= a <= 24
    assert POOL_SIZE == 25
    # Documented concatenation:
    assert seed_bytes(entropy, TS) == entropy + TS.encode("utf-8")


def test_different_entropy_often_different_index() -> None:
    ts = TS
    seen = {select_index(bytes([i]) * 32, ts) for i in range(50)}
    assert len(seen) > 1


def test_protocol_does_not_import_or_call_stdlib_random() -> None:
    src = RNG.read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(a.name.split(".")[0] != "random" for a in node.names)
        if isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] != "random"
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr == "choice":
                raise AssertionError("protocol path must not call choice()")
    assert "import random" not in src
