"""MirageGrid: node-mesh VPN and anonymity network for AZ-OS.

Version 0.2.0 — persistent 25-node mesh, onion circuits, userspace
SOCKS5 VPN. Author: Aziel Eliab (2026).

A static pool of 25 named mesh nodes. At session init the system
selects an entry node and builds a multi-hop circuit. Traffic is
onion-wrapped and forwarded along the mesh. The mapping and circuit
keys are destroyed when the session ends.

This is a lawful privacy tool. It does not authorize crime.
"""

from __future__ import annotations

from miragegrid.circuit import Circuit, CircuitClosedError
from miragegrid.errors import (
    IntegrityError,
    MappingDestroyedError,
    MirageGridError,
    ReceiptError,
)
from miragegrid.mesh import NodeMesh, RoutingError
from miragegrid.pool import Node, NodePool, POOL_SIZE
from miragegrid.receipt import Receipt
from miragegrid.rng import select_index
from miragegrid.session import MirageSession

__version__ = "0.2.0"
__author__ = "Aziel Eliab"
__all__ = [
    "Circuit",
    "CircuitClosedError",
    "IntegrityError",
    "MappingDestroyedError",
    "MirageGridError",
    "Node",
    "NodeMesh",
    "NodePool",
    "POOL_SIZE",
    "Receipt",
    "ReceiptError",
    "RoutingError",
    "MirageSession",
    "select_index",
    "__version__",
]
