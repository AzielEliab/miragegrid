"""No socks/tor/proxy-mesh imports; no socket.bind tricks; no stdlib random protocol."""

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
    "socket",
}

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
    assert found == []


def test_no_socket_bind_or_choice_calls() -> None:
    for path in _py_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Attribute):
                if func.attr == "bind":
                    raise AssertionError(f"{path.name} calls .bind(")
                if func.attr == "choice":
                    raise AssertionError(f"{path.name} calls .choice(")
            if isinstance(func, ast.Name) and func.id == "choice":
                raise AssertionError(f"{path.name} calls choice(")
