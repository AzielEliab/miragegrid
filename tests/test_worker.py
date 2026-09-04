"""Worker source: live count, GET /count, isolated to miragegrid, no /event CTA."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "workers" / "download-tracker" / "src" / "index.js"
TOML = ROOT / "workers" / "download-tracker" / "wrangler.toml"


def test_worker_live_count_and_isolation() -> None:
    js = JS.read_text(encoding="utf-8")
    toml = TOML.read_text(encoding="utf-8")
    assert 'PROJECT = "miragegrid"' in js
    assert "await collectStats" in js or "collectStats(env)" in js
    assert "/count" in js
    assert "project" in js and "total" in js
    assert "not VibeLock" in js or "not the VibeLock" in js
    assert "isolated" in js.lower()
    assert 'href="/download?asset=' in js
    assert "live downloads" in js.lower() or "live download" in js.lower()
    # Homepage must not tell users to POST /event
    homepage = js.split("function indexHtml")[1].split("export default")[0]
    assert "POST /event" not in homepage
    assert "/event" not in homepage
    assert 'id = "f833961513eb44e3ba061e1d2031fe52"' in toml or 'id = "REPLACE_ME"' in toml
    assert 'name = "miragegrid-download-tracker"' in toml
    assert "ac575a9b822bea2bed97d0ab73aed238" in toml
    assert '"/count"' in toml
    assert "0.2.0" in js or "miragegrid-0.2.0.tar.gz" in js
    assert "node-mesh VPN" in js or "node-mesh vpn" in js.lower()
