"""Protocol path stays choice-free; attack libraries stay out.

Socket is allowed in the mesh VPN modules (vpn, transport). Bind is
allowed there for loopback listeners.
"""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN_IMPORTS = {
    "socks",
    "sockshandler",
    "stem",
    "pysocks",
    "tor",
    "torpy",
    "txtorcon",
    "scapy",
    "pydivert",
    "nfqueue",
}

SOCKET_OK = {"vpn.py", "transport.py"}
BIND_OK = {"vpn.py", "transport.py"}

PKG = Path(__file__).resolve().parents[1] / "miragegrid"


def _py_files() -> list[Path]:
    return [p for p in PKG.rglob("*.py") if p.is_file()]


def test_no_forbidden_imports() -> None:
    found: list[str] = []
    for path in _py_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[0].lower() for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module.split(".")[0].lower()]
            for name in names:
                if name in FORBIDDEN_IMPORTS:
                    found.append(f"{path.name}:{name}")
                if name == "socket" and path.name not in SOCKET_OK:
                    found.append(f"{path.name}:socket")
    assert found == []


def test_no_choice_and_bind_only_in_vpn_modules() -> None:
    for path in _py_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Attribute):
                if func.attr == "bind" and path.name not in BIND_OK:
                    raise AssertionError(f"{path.name} calls .bind(")
                if func.attr == "choice":
                    raise AssertionError(f"{path.name} calls .choice(")
            if isinstance(func, ast.Name) and func.id == "choice":
                raise AssertionError(f"{path.name} calls choice(")
