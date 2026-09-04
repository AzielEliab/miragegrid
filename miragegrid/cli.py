"""Command-line interface for MirageGrid.

    miragegrid version
    miragegrid nodes
    miragegrid mesh
    miragegrid route --from node-01 --to node-17
    miragegrid assign [--emit-receipt FILE.json]
    miragegrid circuit
    miragegrid verify-receipt FILE.json
    miragegrid vpn [--host 127.0.0.1] [--port 1080]
    miragegrid node [--id node-01] [--host 127.0.0.1] [--port 19001]
    miragegrid ui [--host 127.0.0.1] [--port 8080]
    miragegrid serve [--host 127.0.0.1] [--port 8080]

Node-mesh VPN and anonymity network. Author: Aziel Eliab.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from miragegrid import __version__
from miragegrid.errors import MappingDestroyedError, ReceiptError
from miragegrid.mesh import NodeMesh
from miragegrid.pool import NodePool
from miragegrid.receipt import Receipt
from miragegrid.session import MirageSession
from miragegrid.ui import DEFAULT_HOST, DEFAULT_PORT, serve


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="miragegrid",
        description=(
            "MirageGrid — node-mesh VPN and anonymity network for AZ-OS "
            "(Aziel Eliab, 2026). Persistent 25-node mesh, onion circuits, "
            "userspace SOCKS5. Lawful privacy tool. "
            "Local UI: `miragegrid ui` at http://127.0.0.1:8080 (loopback). "
            "Local VPN: `miragegrid vpn` SOCKS5 at 127.0.0.1:1080."
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("version", help="Print package version.")
    sub.add_parser("nodes", help="List the 25 mesh nodes.")
    sub.add_parser("mesh", help="Print mesh topology, fingerprints, and adjacency.")

    p_route = sub.add_parser("route", help="Peer-route between two mesh nodes.")
    p_route.add_argument("--from", dest="src", default="node-01", help="Source node id.")
    p_route.add_argument("--to", dest="dst", default="node-13", help="Destination node id.")

    p_as = sub.add_parser(
        "assign",
        help="Assign a mesh circuit (entry + hops); print node id, session id, path.",
    )
    p_as.add_argument(
        "--emit-receipt",
        default=None,
        metavar="FILE.json",
        help="Write the internal receipt JSON the operator asked for.",
    )
    p_as.add_argument(
        "--config",
        default=None,
        help="Optional JSON with listen endpoints (host:port).",
    )
    p_as.add_argument("--hops", type=int, default=3, help="Onion hops (default 3).")

    p_circ = sub.add_parser("circuit", help="Build one anonymity circuit and print hops.")
    p_circ.add_argument("--hops", type=int, default=3)

    p_ver = sub.add_parser("verify-receipt", help="Verify a local receipt JSON file.")
    p_ver.add_argument("file", help="Receipt JSON path.")

    p_vpn = sub.add_parser("vpn", help="Start the local SOCKS5 mesh VPN (loopback).")
    p_vpn.add_argument("--host", default="127.0.0.1")
    p_vpn.add_argument("--port", type=int, default=1080)

    p_node = sub.add_parser("node", help="Run one mesh peer listener (loopback).")
    p_node.add_argument("--id", dest="node_id", default="node-01")
    p_node.add_argument("--host", default="127.0.0.1")
    p_node.add_argument("--port", type=int, default=0)

    p_ui = sub.add_parser("ui", help="Localhost HTML UI (127.0.0.1 only).")
    p_ui.add_argument("--host", default=DEFAULT_HOST, help="Bind host (default 127.0.0.1).")
    p_ui.add_argument("--port", type=int, default=DEFAULT_PORT, help="Bind port (default 8080).")

    p_serve = sub.add_parser("serve", help="Alias for ui. Localhost only.")
    p_serve.add_argument("--host", default=DEFAULT_HOST, help="Bind host (default 127.0.0.1).")
    p_serve.add_argument("--port", type=int, default=DEFAULT_PORT, help="Bind port (default 8080).")

    p_doc = sub.add_parser("doctor", help="Self-check. No telemetry.")
    p_doc.add_argument("--json", action="store_true", dest="as_json", help="Print doctor results as JSON.")

    p_imp = sub.add_parser("import", help="Import a JSON document.")
    p_imp.add_argument("path")

    p_exp = sub.add_parser("export", help="Export a JSON document.")
    p_exp.add_argument("path")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.cmd == "version":
        sys.stdout.write(f"miragegrid {__version__}\n")
        return 0

    if args.cmd == "nodes":
        pool = NodePool()
        for node in pool:
            extra = f"  endpoint={node.endpoint}" if node.endpoint else ""
            sys.stdout.write(f"{node.id}  {node.label}{extra}\n")
        return 0

    if args.cmd == "mesh":
        mesh = NodeMesh()
        sys.stdout.write(json.dumps(mesh.to_dict(), indent=2) + "\n")
        return 0

    if args.cmd == "route":
        mesh = NodeMesh()
        try:
            path = mesh.path_ids(args.src, args.dst)
        except (KeyError, Exception) as exc:
            sys.stderr.write(f"miragegrid: {exc}\n")
            return 2
        sys.stdout.write(json.dumps({"from": args.src, "to": args.dst, "path": path}, indent=2) + "\n")
        return 0

    if args.cmd == "assign":
        pool = NodePool.from_config(args.config) if args.config else NodePool()
        hops = int(getattr(args, "hops", 3) or 3)
        try:
            with MirageSession(pool=pool, hops=hops) as session:
                node = session.node
                sys.stdout.write(f"{node.id}\n")
                sys.stdout.write(f"session_id={session.session_id}\n")
                sys.stdout.write(f"circuit={' '.join(session.circuit.hop_ids)}\n")
                sys.stdout.write(f"path={' '.join(session.circuit.path_ids)}\n")
                if args.emit_receipt:
                    session.receipt.write_json(args.emit_receipt)
                    sys.stderr.write(f"wrote receipt {args.emit_receipt}\n")
        except MappingDestroyedError as exc:
            sys.stderr.write(f"miragegrid: {exc}\n")
            return 2
        return 0

    if args.cmd == "circuit":
        hops = int(getattr(args, "hops", 3) or 3)
        with MirageSession(hops=hops) as session:
            sys.stdout.write(json.dumps(session.circuit.to_dict(), indent=2) + "\n")
        return 0

    if args.cmd == "verify-receipt":
        path = Path(args.file)
        if not path.is_file():
            sys.stderr.write(f"miragegrid: not found: {path}\n")
            return 2
        try:
            rec = Receipt.load(path)
        except (ReceiptError, OSError, json.JSONDecodeError) as exc:
            sys.stderr.write(f"miragegrid: {exc}\n")
            return 2
        status = rec.verify(NodePool())
        payload = {
            "integrity": status,
            "session_id": rec.session_id,
            "mirage_node": rec.mirage_node,
            "timestamp": rec.timestamp,
            "hash_ok": rec.hash_ok(),
        }
        sys.stdout.write(json.dumps(payload, indent=2) + "\n")
        return 0 if status == "PASS" else 1

    if args.cmd == "vpn":
        host = args.host or "127.0.0.1"
        if host not in ("127.0.0.1", "localhost", "::1"):
            sys.stderr.write("miragegrid: refusing non-loopback bind; using 127.0.0.1\n")
            host = "127.0.0.1"
        from miragegrid.vpn import serve_vpn

        serve_vpn(host=host, port=int(args.port))
        return 0

    if args.cmd == "node":
        host = args.host or "127.0.0.1"
        if host not in ("127.0.0.1", "localhost", "::1"):
            sys.stderr.write("miragegrid: refusing non-loopback bind; using 127.0.0.1\n")
            host = "127.0.0.1"
        from miragegrid.transport import MeshListener

        mesh = NodeMesh()
        listener = MeshListener(mesh, args.node_id, host=host, port=int(args.port) or None)
        h, p = listener.start()
        sys.stdout.write(f"miragegrid node {args.node_id}  {h}:{p}\n")
        try:
            import threading

            while True:
                threading.Event().wait(3600)
        except KeyboardInterrupt:
            sys.stdout.write("\nmiragegrid node stopped\n")
        finally:
            listener.stop()
        return 0

    if args.cmd in ("ui", "serve"):
        host = args.host or DEFAULT_HOST
        if host not in ("127.0.0.1", "localhost", "::1"):
            sys.stderr.write("miragegrid: refusing non-loopback bind; using 127.0.0.1\n")
            host = DEFAULT_HOST
        serve(host=host, port=int(args.port))
        return 0

    if args.cmd == "doctor":
        from miragegrid.doctor import run_doctor

        return run_doctor(as_json=getattr(args, "as_json", False))

    if args.cmd == "import":
        from miragegrid.jsonio import import_json

        rec = import_json(args.path)
        sys.stdout.write(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
        return 0

    if args.cmd == "export":
        from miragegrid.jsonio import export_json

        rec = export_json(args.path)
        sys.stdout.write(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
        return 0

    parser.error(f"unknown command {args.cmd}")
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
