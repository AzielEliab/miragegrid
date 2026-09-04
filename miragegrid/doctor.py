"""Self-check for MirageGrid. Crypto and mesh are in-process. No telemetry.

    miragegrid doctor
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Callable

from miragegrid import __version__

AUTHOR = "Aziel Eliab"
Check = tuple[str, bool, str]


def _ok(name: str, detail: str = "") -> Check:
    return name, True, detail


def _fail(name: str, detail: str) -> Check:
    return name, False, detail


def _check_version() -> Check:
    if __version__:
        return _ok("version", str(__version__))
    return _fail("version", "missing")


def _check_identity() -> Check:
    try:
        mod = __import__(__name__.split(".")[0])
        author = str(getattr(mod, "__author__", AUTHOR))
    except Exception as exc:  # noqa: BLE001
        return _fail("identity", str(exc))
    blob = author + " " + AUTHOR
    forbidden = ("Col" + "lin H" + "orton", "Ja" + "ck Al" + "tman", "GodLock" + ".AZ", "Reve" + "aler")
    if any(x in blob for x in forbidden):
        return _fail("identity", "forbidden identity label")
    if "Aziel Eliab" not in blob:
        return _fail("identity", author)
    return _ok("identity", AUTHOR)



def _check_json_roundtrip() -> Check:
    from miragegrid.jsonio import export_json, import_json

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "in.json"
        out = Path(tmp) / "out.json"
        src.write_text(json.dumps({"product": "miragegrid", "author": AUTHOR, "ok": True}, indent=2), encoding="utf-8")
        rec = import_json(src)
        if not rec.get("ok"):
            return _fail("import", str(rec))
        rec2 = export_json(out)
        if not rec2.get("ok") or not out.exists():
            return _fail("export", str(rec2))
        doc = json.loads(out.read_text(encoding="utf-8"))
        if doc.get("author") != AUTHOR:
            return _fail("export author", str(doc.get("author")))
        return _ok("json import/export", "roundtrip")


def _check_mesh() -> Check:
    from miragegrid.mesh import NodeMesh

    mesh = NodeMesh()
    if not mesh.connected():
        return _fail("mesh", "not connected")
    path = mesh.path(0, 12)
    if path[0] != 0 or path[-1] != 12:
        return _fail("mesh path", str(path))
    return _ok("mesh", f"circulant-25 connected path={len(path)}")


def _check_circuit() -> Check:
    from miragegrid.circuit import Circuit
    from miragegrid.mesh import NodeMesh

    mesh = NodeMesh()
    circ = Circuit.build(
        mesh,
        entropy=b"\x11" * 32,
        timestamp="2026-03-04T13:02:12Z",
        hops=3,
    )
    msg = b"miragegrid-circuit-selfcheck"
    back = circ.unwrap(circ.wrap(msg))
    if back != msg:
        return _fail("circuit", "unwrap mismatch")
    if circ.entry.node_id == circ.exit.node_id:
        return _fail("circuit", "entry equals exit")
    circ.close()
    try:
        circ.wrap(b"x")
    except Exception:
        return _ok("circuit", "3-hop onion + key drop")
    return _fail("circuit", "wrap after close")


def _check_crypto() -> Check:
    from miragegrid.crypto import aead_decrypt, aead_encrypt, x25519, x25519_keypair

    secret, pub = x25519_keypair(b"\x01" + b"\x00" * 31)
    shared = x25519(secret, pub)
    if len(shared) != 32:
        return _fail("crypto", "x25519 length")
    blob = aead_encrypt(b"k" * 32, b"n" * 12, b"hello", b"aad")
    if aead_decrypt(b"k" * 32, b"n" * 12, blob, b"aad") != b"hello":
        return _fail("crypto", "aead")
    return _ok("crypto", "x25519+chacha20-poly1305")


CHECKS: tuple[Callable[[], Check], ...] = (
    _check_version,
    _check_identity,
    _check_json_roundtrip,
    _check_mesh,
    _check_circuit,
    _check_crypto,
)


def run_doctor(*, as_json: bool = False) -> int:
    results = []
    failed = 0
    for fn in CHECKS:
        name, ok, detail = fn()
        results.append({"name": name, "ok": ok, "detail": detail})
        if not ok:
            failed += 1
        mark = "ok" if ok else "FAIL"
        if not as_json:
            print(f"[{mark}] {name}" + (f" — {detail}" if detail else ""))
    payload = {
        "ok": failed == 0,
        "failed": failed,
        "checks": results,
        "version": __version__,
        "author": AUTHOR,
        "network": False,
        "telemetry": False,
    }
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print("doctor", "passed" if failed == 0 else "failed")
    return 0 if failed == 0 else 1
