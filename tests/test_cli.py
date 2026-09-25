"""CLI version, nodes, assign, emit-receipt, verify-receipt."""

from __future__ import annotations

import json
from pathlib import Path

from miragegrid import __version__
from miragegrid.cli import main


def test_cli_version(capsys) -> None:
    assert main(["version"]) == 0
    assert capsys.readouterr().out.strip() == f"miragegrid {__version__}"


def test_cli_nodes(capsys) -> None:
    assert main(["nodes"]) == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 25
    assert out[0].startswith("node-01")
    assert out[-1].startswith("node-25")
    assert "Node01" in out[0]
    assert "Node25" in out[-1]


def test_cli_assign(capsys) -> None:
    assert main(["assign"]) == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert lines[0].startswith("node-")
    assert lines[1].startswith("session_id=")
    assert "receipt" not in "\n".join(lines).lower()


def test_cli_assign_emit_receipt(tmp_path: Path, capsys) -> None:
    dest = tmp_path / "receipt.json"
    assert main(["assign", "--emit-receipt", str(dest)]) == 0
    out = capsys.readouterr().out
    assert "node-" in out
    data = json.loads(dest.read_text(encoding="utf-8"))
    assert "session_id" in data
    assert "mirage_node" in data
    assert "timestamp" in data
    assert data["integrity"] in ("PASS", "FAIL")
    assert 1 <= int(data["mirage_node"]) <= 25


def test_cli_verify_receipt(tmp_path: Path, capsys) -> None:
    dest = tmp_path / "receipt.json"
    assert main(["assign", "--emit-receipt", str(dest)]) == 0
    capsys.readouterr()
    rc = main(["verify-receipt", "--json", str(dest)])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["integrity"] == "PASS"
    assert "session_id" in payload
    assert "mirage_node" in payload
    assert "timestamp" in payload
    assert "hash_ok" in payload

    capsys.readouterr()
    rc = main(["verify-receipt", str(dest)])
    assert rc == 0
    human = capsys.readouterr().out
    assert "Receipt passed." in human
    assert not human.strip().startswith("{")

    forged = json.loads(dest.read_text(encoding="utf-8"))
    forged["mirage_node"] = 99
    dest.write_text(json.dumps(forged), encoding="utf-8")
    rc = main(["verify-receipt", "--json", str(dest)])
    assert rc == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["integrity"] == "FAIL"


def test_help_lists_ui_and_version() -> None:
    from miragegrid.cli import _build_parser

    text = _build_parser().format_help()
    assert "ui" in text
    assert "version" in text
    assert "127.0.0.1:8080" in text or "miragegrid ui" in text
    assert "VPN" in text or "anonymity" in text.lower() or "loopback" in text.lower()
    assert "vpn" in text.lower() or "mesh" in text.lower()
    assert "CHANGELOG" not in text
    assert "Advanced" in text


def test_bare_command_is_a_welcome(capsys) -> None:
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "miragegrid ui" in out
    assert "Aziel Eliab" in out
    assert "arguments are required" not in out
    assert "Cap-7" not in out or "mesh DNS" in out


def test_unknown_command_has_a_next_step(capsys) -> None:
    rc = main(["bogus"])
    assert rc == 2
    err = capsys.readouterr().err
    assert 'Unknown command "bogus".' in err
    assert "miragegrid --help" in err
    assert "Traceback" not in err


def test_mesh_json_matches_library(capsys) -> None:
    from miragegrid.mesh import NodeMesh

    assert main(["mesh", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == NodeMesh().to_dict()


def test_route_json_shape(capsys) -> None:
    assert main(["--json", "route", "--from", "node-01", "--to", "node-17"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["from"] == "node-01"
    assert payload["to"] == "node-17"
    assert payload["path"][0] == "node-01"
    assert payload["path"][-1] == "node-17"


def test_missing_receipt_explains_next_step(capsys) -> None:
    rc = main(["verify-receipt", "missing-receipt.json"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "not found" in err.lower() or "Receipt file not found" in err
    assert "miragegrid assign --emit-receipt" in err
