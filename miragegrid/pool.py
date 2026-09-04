"""Static pool of 25 persistent mesh nodes.

Nodes are named mesh members (``node-01`` … ``node-25``). Optional
``endpoint`` strings are listen targets (host:port) for peer links.
The pool itself does not open sockets; ``miragegrid.transport`` and
``miragegrid.vpn`` do.

Author: Aziel Eliab
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Mapping

POOL_SIZE = 25


@dataclass(frozen=True)
class Node:
    """One persistent mesh node.

    ``id`` is ``node-01`` … ``node-25``.
    ``label`` is ``Node01`` … ``Node25``.
    ``index`` is ``0..24``.
    ``number`` is ``1..25`` (receipt field ``mirage_node``).
    ``endpoint`` is an optional listen target (``127.0.0.1:19001``).
    """

    id: str
    label: str
    index: int
    number: int
    endpoint: str | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "label": self.label,
            "index": self.index,
            "number": self.number,
            "endpoint": self.endpoint,
        }


def node_id_for(index: int) -> str:
    return f"node-{index + 1:02d}"


def node_label_for(index: int) -> str:
    return f"Node{index + 1:02d}"


class NodePool:
    """Exactly 25 named mesh nodes. Length is always 25."""

    def __init__(self, endpoints: Mapping[str, str] | None = None) -> None:
        eps = dict(endpoints or {})
        nodes: list[Node] = []
        for index in range(POOL_SIZE):
            nid = node_id_for(index)
            label = node_label_for(index)
            endpoint = eps.get(nid) or eps.get(label)
            if endpoint is not None:
                endpoint = str(endpoint)
            else:
                endpoint = f"127.0.0.1:{19000 + index + 1}"
            nodes.append(
                Node(
                    id=nid,
                    label=label,
                    index=index,
                    number=index + 1,
                    endpoint=endpoint,
                )
            )
        self._nodes: tuple[Node, ...] = tuple(nodes)
        self._by_id: dict[str, Node] = {n.id: n for n in self._nodes}
        self._by_label: dict[str, Node] = {n.label: n for n in self._nodes}
        if len(self._nodes) != POOL_SIZE:
            raise RuntimeError("NodePool must expose exactly 25 mesh nodes")
        if len(self._by_id) != POOL_SIZE:
            raise RuntimeError("NodePool ids must be unique")

    def __len__(self) -> int:
        return POOL_SIZE

    def __iter__(self) -> Iterator[Node]:
        return iter(self._nodes)

    def __getitem__(self, index: int) -> Node:
        return self._nodes[index]

    @property
    def nodes(self) -> tuple[Node, ...]:
        return self._nodes

    def by_id(self, node_id: str) -> Node:
        return self._by_id[node_id]

    def by_index(self, index: int) -> Node:
        if index < 0 or index >= POOL_SIZE:
            raise IndexError(f"node index {index} out of range 0..24")
        return self._nodes[index]

    def by_number(self, number: int) -> Node:
        """Look up by receipt ``mirage_node`` (1–25)."""
        if number < 1 or number > POOL_SIZE:
            raise IndexError(f"mirage_node {number} out of range 1..25")
        return self._nodes[number - 1]

    def contains(self, node_id: str) -> bool:
        return node_id in self._by_id

    def contains_number(self, number: int) -> bool:
        return isinstance(number, int) and 1 <= number <= POOL_SIZE

    @classmethod
    def from_config(cls, path: str | Path) -> "NodePool":
        """Load optional listen endpoints from a JSON file.

        Expected shape::

            {"endpoints": {"node-01": "127.0.0.1:19001"}}
        """
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        endpoints: dict[str, str] = {}
        if isinstance(raw, dict):
            block = raw.get("endpoints", raw)
            if isinstance(block, dict):
                endpoints = {str(k): str(v) for k, v in block.items()}
        return cls(endpoints=endpoints)
