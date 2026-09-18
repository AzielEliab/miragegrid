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
from miragegrid.az_generator import AzGenerator, DeepNode, MeshDnsZone, PaperVault
from miragegrid.cap7_shuffle import cap7_shuffle_dict, hosted_bridge_doors, ping as cap7_ping
from miragegrid.semantic_bridge import build_bridge_registry, hosted_bridge_document, semantic_bridge_dict
from miragegrid.mesh import (
    MeshLawError,
    NodeMesh,
    RoutingError,
    mesh_law_dict,
)
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
    "MeshLawError",
    "NodeMesh",
    "NodePool",
    "POOL_SIZE",
    "Receipt",
    "ReceiptError",
    "RoutingError",
    "MirageSession",
    "AzGenerator",
    "DeepNode",
    "MeshDnsZone",
    "PaperVault",
    "mesh_law_dict",
    "semantic_bridge_dict",
    "build_bridge_registry",
    "hosted_bridge_document",
    "cap7_shuffle_dict",
    "hosted_bridge_doors",
    "cap7_ping",
    "select_index",
    "__version__",
]
