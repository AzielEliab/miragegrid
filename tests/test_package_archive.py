"""Counted tarball matches package 0.3.0. Packet-hop locks stay in the archive."""

from __future__ import annotations

import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "workers" / "download-tracker" / "public" / "miragegrid-0.3.0.tar.gz"
PREFIX = "miragegrid-0.3.0/"


def _text(tar: tarfile.TarFile, name: str) -> str:
    extracted = tar.extractfile(PREFIX + name)
    assert extracted is not None, name
    return extracted.read().decode("utf-8")


def test_counted_archive_version_and_metadata() -> None:
    assert ARCHIVE.is_file()
    with tarfile.open(ARCHIVE, "r:gz") as tar:
        names = set(tar.getnames())
        assert PREFIX + "PKG-INFO" in names
        assert PREFIX + "VERSION" in names
        assert PREFIX + "pyproject.toml" in names
        pkg = _text(tar, "PKG-INFO")
        assert "Metadata-Version:" in pkg
        assert "Name: miragegrid\n" in pkg
        assert "Version: 0.3.0\n" in pkg
        assert _text(tar, "VERSION").strip() == "0.3.0"
        assert 'version = "0.3.0"' in _text(tar, "pyproject.toml")
        assert '__version__ = "0.3.0"' in _text(tar, "miragegrid/__init__.py")
        planned = _text(tar, "miragegrid/cap7_shuffle.py")
        assert '"softwares_catalog_live": True' in planned
        assert "softwares_note" not in planned
        assert "AZBot CLEAR" not in planned
        assert '"vpn-hop"' in planned
        assert "public_egress_ip" in planned


def test_download_sources_name_the_030_archive() -> None:
    index = (ROOT / "workers/download-tracker/src/index.js").read_text(encoding="utf-8")
    home = (ROOT / "workers/download-tracker/src/homepage.js").read_text(encoding="utf-8")
    install = (ROOT / "install.sh").read_text(encoding="utf-8")
    assert 'const DEFAULT_ASSET = "miragegrid-0.3.0.tar.gz"' in index
    assert 'const DEFAULT_ASSET = "miragegrid-0.3.0.tar.gz"' in home
    assert "miragegrid-0.3.0.tar.gz" in install
    assert 'Content-Disposition", \'attachment; filename="\' + asset' in index
    assert "miragegrid-0.2.0.tar.gz" not in index
    assert "miragegrid-0.2.0.tar.gz" not in home
    assert "miragegrid-0.2.0.tar.gz" not in install
