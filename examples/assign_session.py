#!/usr/bin/env python3
"""Assign a MirageGrid mesh circuit, print hops, destroy the mapping.

Author: Aziel Eliab
"""

from __future__ import annotations

from miragegrid.session import MirageSession
from miragegrid.errors import MappingDestroyedError


def main() -> None:
    with MirageSession() as session:
        node = session.node
        print(f"entry {node.id}  ({node.label})")
        print(f"session_id={session.session_id}")
        print(f"circuit hops={session.circuit.hop_ids}")
        print(f"mesh path={session.circuit.path_ids}")
        print(f"live integrity={session.integrity}")
        print(f"str(session)={session}")
        dump = session.to_dict()
        print(f"default dump keys={sorted(dump)}")
        assert "receipt" not in dump
        rec = session.emit_receipt()
        print(
            "internal receipt snapshot: "
            f"mirage_node={rec['mirage_node']} integrity={rec['integrity']}"
        )
        back = session.unwrap(session.wrap(b"booth-payload"))
        print(f"onion roundtrip={back!r}")
    print("mapping destroyed")
    try:
        _ = session.node
    except MappingDestroyedError as exc:
        print(f"after close: {exc}")


if __name__ == "__main__":
    main()
