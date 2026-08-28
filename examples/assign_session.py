#!/usr/bin/env python3
"""Assign a logical MirageGrid node, print it, destroy the mapping.

No sockets. No tunnels. No network.
"""

from __future__ import annotations

from miragegrid.session import MirageSession
from miragegrid.errors import MappingDestroyedError


def main() -> None:
    with MirageSession() as session:
        node = session.node
        print(f"booth {node.id}  ({node.label})")
        print(f"session_id={session.session_id}")
        print(f"live integrity={session.integrity}")
        print(f"str(session)={session}")
        # Receipt is internal; not in default dump:
        dump = session.to_dict()
        print(f"default dump keys={sorted(dump)}")
        assert "receipt" not in dump
        # Operator may emit a snapshot without making it the public API:
        rec = session.emit_receipt()
        print(
            "internal receipt snapshot: "
            f"mirage_node={rec['mirage_node']} integrity={rec['integrity']}"
        )
    print("mapping destroyed")
    try:
        _ = session.node
    except MappingDestroyedError as exc:
        print(f"after close: {exc}")


if __name__ == "__main__":
    main()
