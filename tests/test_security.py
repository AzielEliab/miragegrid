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


def test_attack_surface_refuses_call_generator_vpn_and_neighbor_heal() -> None:
    root = Path(__file__).resolve().parents[1]
    mesh_py = (root / "miragegrid" / "mesh.py").read_text(encoding="utf-8")
    gen = (root / "miragegrid" / "az_generator.py").read_text(encoding="utf-8")
    js = (root / "workers/download-tracker/src/mesh.js").read_text(encoding="utf-8")
    assert "AZG-NOT-CALLABLE" in gen and "AZG-NOT-CALLABLE" in js
    assert "MESH-GET-NO-ENABLE" in js
    assert "GET never enables" in js
    assert "MESH-STUB" in mesh_py and '"vpn"' in js and '"tunnel"' in js
    assert "RH-NO-VOTE-TO-FIX" in mesh_py and "RH-NO-NEIGHBOR-TALK" in js
    assert "CCS-POISON-MARKER" in gen and "CCS-POISON-MARKER" in js
    assert "public_icann" in gen and "cctld_takeover" in js
    assert "AZG-PUBLIC-PAIR" in gen
    assert "cap-7-mesh-authoritative" in gen
    assert "AZG-NO-RADIO-PHY" in mesh_py
    assert "radio_phy" in gen or "RADIO_PHY" in mesh_py
    assert "refuse_get_enable_or_plant" in mesh_py
    assert "GET never enables radios or plants mesh claims" in js
    from miragegrid.mesh import hosted_stub_refuse, reheal

    assert hosted_stub_refuse("vpn")["code"] == "MESH-STUB"
    assert hosted_stub_refuse("hop")["code"] == "MESH-STUB"
    assert hosted_stub_refuse("tunnel")["code"] == "MESH-STUB"
    assert reheal(source="own-tip+trusted-pull", vote_to_fix=True)["code"] == "RH-NO-VOTE-TO-FIX"
