"""Softwares Cap-7 companion is CLEARED. Waiting copy must not return.

Author: Aziel Eliab only.
"""

from __future__ import annotations

from pathlib import Path

from miragegrid.cap7_shuffle import SOFTWARES_COMPANION_NOTE, planned_adaptation
from miragegrid.egress import egress_cite

ROOT = Path(__file__).resolve().parents[1]

# Split so this file does not store the forbidden sentences as one string.
FORBIDDEN = (
    "until AZBot " + "CLEAR",
    "stay on the runtime companion " + "until",
    "CLEAR waits on the runtime " + "companion",
    "AZBot " + "CLEAR after deploy",
    "AZBot " + "CLEAR follows deploy",
)

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache", ".venv", "dist"}
SUFFIXES = {".py", ".js", ".mjs", ".md", ".json", ".jsonc", ".yml", ".yaml", ".toml", ".html", ".txt"}


def test_planned_and_egress_cite_the_cleared_companion() -> None:
    planned = planned_adaptation()
    note = planned["softwares_note"]
    assert note == SOFTWARES_COMPANION_NOTE
    assert note.startswith("CLEARED:")
    assert planned["softwares_companion_tip"] == "6f27394fbcafb640a1ede7017b599a6f66c68769"
    assert "6f27394fbcafb640a1ede7017b599a6f66c68769" in note
    assert "be1c7990452094536b122645103d41f595c03c76" not in note
    assert "1c2de0ef-f315-4444-86aa-aec03f730a58" in note
    assert "git lockstep pin" in note
    assert "not a deploy stamp of this tip" in note
    assert "public_door_ops" in note
    assert "MirageGrid 0.3.0" in note
    assert "not a public egress IP" in note
    assert "not residential" in note
    assert "not AZVPN" in note
    assert "Softwares desk layout unchanged" in note
    assert "Softwares count stays 42" in note
    assert planned["softwares_catalog_live"] is True
    assert planned["softwares_desk_frozen"] is True
    assert planned["softwares_count"] == 42
    assert planned["worker_live_ops"] == ["geo-target", "session-stick", "egress-rotate"]
    assert planned["fraggate_stubs"] == ["vpn-hop", "hop", "tunnel", "mesh"]
    assert planned["public_icann"] is False
    assert planned["hosted_vpn"] is False
    assert planned["public_egress_ip"] is False
    assert planned["sticky_public_ip"] is False
    assert planned["azvpn_softwares"] is False
    assert "geo-target" not in planned["fraggate_stubs"]

    cite = egress_cite()
    assert cite["softwares_catalog_live"] is True
    assert cite["softwares_note"] == note
    assert cite["azvpn_merged"] is False
    assert cite["residential"] is False
    assert cite["public_egress_ip"] is False

    mesh = (ROOT / "workers/download-tracker/src/mesh.js").read_text(encoding="utf-8")
    egress_js = (ROOT / "workers/miragegrid/src/egress.js").read_text(encoding="utf-8")
    assert note in mesh
    assert "softwares_note: SOFTWARES_COMPANION_NOTE" in egress_js
    assert "SOFTWARES_COMPANION_NOTE" in egress_js
    assert "softwares_catalog_live: true" in mesh
    assert "softwares_catalog_live: true" in egress_js
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    paper = (ROOT / "docs/MG-EGRESS-1.0.md").read_text(encoding="utf-8")
    assert "CLEARED" in skill and "6f27394fbcafb640a1ede7017b599a6f66c68769" in skill
    assert "be1c7990452094536b122645103d41f595c03c76" not in skill
    assert "AZBot CLEAR is received" in paper
    assert "Softwares count stays 42" in paper
    assert "6f27394fbcafb640a1ede7017b599a6f66c68769" in paper

    old_tip = "be1c7990452094536b122645103d41f595c03c76"
    stale: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in SUFFIXES:
            continue
        if path.name == "test_softwares_companion_clear.py":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if old_tip in text:
            stale.append(str(path.relative_to(ROOT)))
    assert stale == []


def test_waiting_on_azbot_clear_does_not_return() -> None:
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in FORBIDDEN:
            if needle in text:
                hits.append(f"{path.relative_to(ROOT)} contains {needle!r}")
    assert hits == []
