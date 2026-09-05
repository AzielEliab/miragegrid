"""Worker source: live count, product homepage, isolated to miragegrid, no /event CTA."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "workers" / "download-tracker" / "src"
JS = SRC / "index.js"
HOME = SRC / "homepage.js"
RUNTIME = SRC / "runtime.js"
TOML = ROOT / "workers" / "download-tracker" / "wrangler.toml"
SIGIL = ROOT / "workers" / "download-tracker" / "public" / "sigil.png"


def _blob() -> str:
    return "\n".join(
        [
            JS.read_text(encoding="utf-8"),
            HOME.read_text(encoding="utf-8"),
            RUNTIME.read_text(encoding="utf-8"),
        ]
    )


def test_worker_live_count_and_isolation() -> None:
    js = _blob()
    toml = TOML.read_text(encoding="utf-8")
    assert 'PROJECT = "miragegrid"' in js
    assert "await collectStats" in js or "collectStats(env)" in js
    assert "/count" in js
    assert "project" in js and "total" in js
    assert "not VibeLock" in js or "not the VibeLock" in js
    assert "isolated" in js.lower()
    assert 'href="/download?asset=' in js
    assert "live downloads" in js.lower() or "live download" in js.lower()
    homepage = HOME.read_text(encoding="utf-8")
    assert "POST /event" not in homepage
    assert "/event" not in homepage
    assert 'id = "f833961513eb44e3ba061e1d2031fe52"' in toml or 'id = "REPLACE_ME"' in toml
    assert 'name = "miragegrid-download-tracker"' in toml
    assert "ac575a9b822bea2bed97d0ab73aed238" in toml
    assert '"/count"' in toml
    assert "0.2.0" in js or "miragegrid-0.2.0.tar.gz" in js


def test_worker_product_homepage() -> None:
    home = HOME.read_text(encoding="utf-8")
    js = _blob()
    assert "MirageGrid — Aziel Eliab" in home
    assert "application/ld+json" in home
    assert '"@type": "SoftwareApplication"' in home or '"@type":"SoftwareApplication"' in home
    assert "citation_author" in home
    assert "How to cite" in home
    assert "cite.json" in home
    assert "id=\"workspace\"" in home
    assert "/v1/assign" in home
    assert "/v1/mesh" in home
    assert "/v1/route" in home
    assert "/v1/verify-receipt" in home
    assert "Everblooming sigil" in home
    assert "/sigil.png" in home
    assert "Aziel Eliab" in home
    assert "Apache-2.0" in home
    assert "forks welcome" in home.lower()
    assert "not a VPN" in js
    assert "not an anonymity network" in js.lower()
    assert "zenodo.214" not in home.lower()
    assert "10.5281/zenodo" not in home
    assert SIGIL.is_file()
    assert SIGIL.stat().st_size > 1000
    toml = TOML.read_text(encoding="utf-8")
    assert "/cite.json" in toml
    assert "/robots.txt" in toml
    assert "/sitemap.xml" in toml
