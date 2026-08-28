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
    rc = main(["verify-receipt", str(dest)])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["integrity"] == "PASS"

    forged = json.loads(dest.read_text(encoding="utf-8"))
    forged["mirage_node"] = 99
    dest.write_text(json.dumps(forged), encoding="utf-8")
    rc = main(["verify-receipt", str(dest)])
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
