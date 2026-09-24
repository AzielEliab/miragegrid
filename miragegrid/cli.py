"""Command-line interface for MirageGrid.

Human text is the default. ``--json`` prints the same machine documents
the commands already produced. Author: Aziel Eliab.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence

from miragegrid import __author__, __version__
from miragegrid.errors import MappingDestroyedError, ReceiptError
from miragegrid.mesh import NodeMesh, RoutingError
from miragegrid.pool import NodePool, POOL_SIZE
from miragegrid.receipt import Receipt
from miragegrid.session import MirageSession
from miragegrid.ui import DEFAULT_HOST, DEFAULT_PORT, serve

_LOOPBACK = ("127.0.0.1", "localhost", "::1")


def render_help() -> str:
    return f"""miragegrid — local node-mesh VPN

Open a circuit on this computer and send it through {POOL_SIZE} mesh peers.
Loopback only. Author: {__author__}.

Usage:
  miragegrid
  miragegrid <command> [options]

Common commands:
  ui               Open the local console
  doctor           Check this install
  assign           Open a circuit and print the entry peer
  vpn              Start SOCKS5 on 127.0.0.1:1080
  nodes            List the {POOL_SIZE} mesh peers
  version          Print miragegrid {__version__}

Advanced:
  mesh             Mesh map (--json for the full document)
  route            Path between two peers
  circuit          Build one circuit
  verify-receipt   Check a receipt file
  node             Run one peer listener
  import           Import a JSON document
  export           Export a JSON document
  generator-tick   Local Cap-7 mesh DNS factory tick
  serve            Same as ui
  help             Show this help

Options:
  -h, --help       Show this help
  --version        Print the version
  --json           Print JSON for machines

Examples:
  miragegrid ui
  miragegrid doctor
  miragegrid assign
  miragegrid assign --emit-receipt receipt.json
  miragegrid vpn

Local console: miragegrid ui  →  http://127.0.0.1:8080
"""


def render_error(message: str) -> str:
    text = " ".join(message.split())
    choice = re.search(r"invalid choice: '([^']*)'", text)
    if choice:
        name = choice.group(1) or ""
        return (
            f'Unknown command "{name}".\n'
            "Try: miragegrid ui    or    miragegrid --help"
        )
    if "arguments are required" in text and "file" in text:
        return (
            "A receipt file is required.\n"
            "Next: miragegrid verify-receipt receipt.json"
        )
    if "arguments are required" in text and "path" in text:
        return (
            "A JSON file path is required.\n"
            "Next: miragegrid import file.json"
        )
    if text.startswith("unrecognized arguments"):
        return f"{text}.\nTry: miragegrid --help"
    if "invalid int value" in text:
        return f"That number is not valid. {text}\nNext: miragegrid --help"
    return f"{text}\nTry: miragegrid --help"


class MirageParser(argparse.ArgumentParser):
    def __init__(self, *args: Any, root: bool = False, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.root = root

    def format_help(self) -> str:
        if self.root:
            return render_help()
        return super().format_help()

    def error(self, message: str) -> None:
        sys.stderr.write(render_error(message) + "\n")
        self.exit(2)


def _build_parser() -> MirageParser:
    parser = MirageParser(
        prog="miragegrid",
        root=True,
        add_help=True,
    )
    parser.add_argument("--version", action="store_true", dest="version_flag")
    sub = parser.add_subparsers(dest="cmd", required=False, parser_class=MirageParser)

    sub.add_parser("version", help="Print the package version.")
    sub.add_parser("help", help="Show help.")
    sub.add_parser("nodes", help="List the 25 mesh peers.")

    sub.add_parser("mesh", help="Print a short mesh summary. Use --json for the full map.")

    p_route = sub.add_parser("route", help="Show the path between two peers.")
    p_route.add_argument("--from", dest="src", default="node-01", help="Source peer id.")
    p_route.add_argument("--to", dest="dst", default="node-13", help="Destination peer id.")

    p_as = sub.add_parser("assign", help="Open a circuit and print the entry peer.")
    p_as.add_argument(
        "--emit-receipt",
        default=None,
        metavar="FILE.json",
        help="Write the internal receipt JSON.",
    )
    p_as.add_argument(
        "--config",
        default=None,
        help="Optional JSON with listen endpoints (host:port).",
    )
    p_as.add_argument("--hops", type=int, default=3, help="Onion hops (default 3, range 1–25).")

    p_circ = sub.add_parser("circuit", help="Build one circuit and print its hops.")
    p_circ.add_argument("--hops", type=int, default=3, help="Onion hops (default 3, range 1–25).")

    p_ver = sub.add_parser("verify-receipt", help="Check a local receipt JSON file.")
    p_ver.add_argument("file", help="Receipt JSON path.")

    p_vpn = sub.add_parser("vpn", help="Start the local SOCKS5 proxy (loopback).")
    p_vpn.add_argument("--host", default="127.0.0.1", help="Bind host (loopback only).")
    p_vpn.add_argument("--port", type=int, default=1080, help="Bind port (default 1080).")

    p_node = sub.add_parser("node", help="Run one mesh peer listener (loopback).")
    p_node.add_argument("--id", dest="node_id", default="node-01", help="Peer id.")
    p_node.add_argument("--host", default="127.0.0.1", help="Bind host (loopback only).")
    p_node.add_argument("--port", type=int, default=0, help="Bind port (0 picks a free port).")

    p_ui = sub.add_parser("ui", help="Open the local console (loopback only).")
    p_ui.add_argument("--host", default=DEFAULT_HOST, help="Bind host (default 127.0.0.1).")
    p_ui.add_argument("--port", type=int, default=DEFAULT_PORT, help="Bind port (default 8080).")

    p_serve = sub.add_parser("serve", help="Same as ui.")
    p_serve.add_argument("--host", default=DEFAULT_HOST, help="Bind host (default 127.0.0.1).")
    p_serve.add_argument("--port", type=int, default=DEFAULT_PORT, help="Bind port (default 8080).")

    sub.add_parser("doctor", help="Check this install. No telemetry.")

    p_imp = sub.add_parser("import", help="Import a JSON document.")
    p_imp.add_argument("path", help="JSON file to import.")

    p_exp = sub.add_parser("export", help="Export a JSON document.")
    p_exp.add_argument("path", help="Where to write the JSON file.")

    p_tick = sub.add_parser(
        "generator-tick",
        help="Local Cap-7 mesh DNS factory tick (on this computer).",
    )
    p_tick.add_argument("--id", dest="node_id", default="node-01", help="Origin peer id.")
    p_tick.add_argument("--now", dest="now_s", type=float, default=0, help="Clock seconds for the tick.")
    p_tick.add_argument(
        "--papers",
        type=int,
        default=0,
        help="Synthetic local vault size for this operator loop.",
    )
    p_tick.add_argument("--name", default=None, help="Optional claim name.")

    return parser


def _extract_json(argv: Sequence[str]) -> tuple[bool, list[str]]:
    as_json = False
    cleaned: list[str] = []
    for arg in argv:
        if arg == "--json":
            as_json = True
        else:
            cleaned.append(arg)
    return as_json, cleaned


def _write_json(payload: Any) -> None:
    sys.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n")


def _die(reason: str, nxt: str) -> int:
    sys.stderr.write(f"{reason}\n{nxt}\n")
    return 2


def _welcome(as_json: bool) -> int:
    if as_json:
        _write_json(
            {
                "product": "miragegrid",
                "version": __version__,
                "author": __author__,
                "next": ["miragegrid ui", "miragegrid doctor", "miragegrid --help"],
            }
        )
        return 0
    sys.stdout.write(
        "MirageGrid opens a local circuit through "
        f"{POOL_SIZE} mesh peers on this computer.\n"
        "\n"
        "Next: open the console.\n"
        "\n"
        "  miragegrid ui\n"
        "\n"
        "The page is at http://127.0.0.1:8080 (this computer only).\n"
        "Check the install with miragegrid doctor, or see miragegrid --help.\n"
        "\n"
        f"Author: {__author__}\n"
    )
    return 0


def _version(as_json: bool) -> int:
    if as_json:
        _write_json({"product": "miragegrid", "version": __version__, "author": __author__})
    else:
        sys.stdout.write(f"miragegrid {__version__}\n")
    return 0


def _loopback(host: str | None) -> str:
    chosen = host or "127.0.0.1"
    if chosen not in _LOOPBACK:
        sys.stderr.write(
            "That host is outside this computer's loopback. Using 127.0.0.1.\n"
            "Next: miragegrid ui\n"
        )
        return "127.0.0.1"
    return chosen


def _check_hops(hops: int) -> str | None:
    if hops < 1 or hops > POOL_SIZE:
        return f"Hops must be from 1 to {POOL_SIZE}."
    return None


def _load_pool(config: str | None) -> NodePool | str:
    if not config:
        return NodePool()
    path = Path(config)
    if not path.is_file():
        return f"Config file not found: {path}"
    try:
        return NodePool.from_config(path)
    except json.JSONDecodeError:
        return "That config file is not JSON."
    except OSError as exc:
        return f"Could not read the config file: {exc}"


def main(argv: Sequence[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    as_json, cleaned = _extract_json(raw)
    parser = _build_parser()
    try:
        args = parser.parse_args(cleaned)
    except SystemExit as exc:
        code = exc.code
        if code in (None, 0):
            return 0
        if isinstance(code, int):
            return code
        return 2

    if getattr(args, "version_flag", False) and not args.cmd:
        return _version(as_json)

    if not args.cmd:
        return _welcome(as_json)

    if args.cmd in ("version", "help"):
        if args.cmd == "help":
            sys.stdout.write(render_help())
            return 0
        return _version(as_json)

    if args.cmd == "nodes":
        pool = NodePool()
        if as_json:
            _write_json({"nodes": [node.to_dict() for node in pool]})
            return 0
        for node in pool:
            extra = f"  endpoint={node.endpoint}" if node.endpoint else ""
            sys.stdout.write(f"{node.id}  {node.label}{extra}\n")
        return 0

    if args.cmd == "mesh":
        mesh = NodeMesh()
        payload = mesh.to_dict()
        if as_json:
            _write_json(payload)
            return 0
        connected = "yes" if payload.get("connected") else "no"
        factory = (payload.get("az_generator") or {}).get("dns_factory") or ""
        sys.stdout.write(
            "Mesh\n"
            f"Peers: {payload.get('pool_size')}\n"
            f"Topology: {payload.get('topology')}\n"
            f"Connected: {connected}\n"
            f"Factory: {factory}\n"
            "\n"
            "Full map: miragegrid mesh --json\n"
        )
        return 0

    if args.cmd == "route":
        mesh = NodeMesh()
        try:
            path = mesh.path_ids(args.src, args.dst)
        except KeyError:
            return _die(
                f'Unknown peer "{args.src}" or "{args.dst}".',
                "Next: miragegrid nodes",
            )
        except RoutingError as exc:
            return _die(f"No path: {exc}", "Next: miragegrid nodes")
        payload = {"from": args.src, "to": args.dst, "path": path}
        if as_json:
            _write_json(payload)
            return 0
        sys.stdout.write(" → ".join(path) + "\n")
        return 0

    if args.cmd == "assign":
        loaded = _load_pool(args.config)
        if isinstance(loaded, str):
            return _die(loaded, "Next: miragegrid assign")
        hops = int(getattr(args, "hops", 3) or 3)
        hop_err = _check_hops(hops)
        if hop_err:
            return _die(hop_err, "Next: miragegrid assign --hops 3")
        try:
            with MirageSession(pool=loaded, hops=hops) as session:
                node = session.node
                hop_ids = list(session.circuit.hop_ids)
                path_ids = list(session.circuit.path_ids)
                session_id = session.session_id
                if args.emit_receipt:
                    session.receipt.write_json(args.emit_receipt)
                    sys.stderr.write(f"wrote receipt {args.emit_receipt}\n")
        except MappingDestroyedError as exc:
            return _die(str(exc), "Next: miragegrid assign")
        except ValueError as exc:
            return _die(str(exc), "Next: miragegrid assign --hops 3")
        if as_json:
            _write_json(
                {
                    "node_id": node.id,
                    "session_id": session_id,
                    "circuit": hop_ids,
                    "path": path_ids,
                }
            )
            return 0
        sys.stdout.write(f"{node.id}\n")
        sys.stdout.write(f"session_id={session_id}\n")
        sys.stdout.write(f"circuit={' '.join(hop_ids)}\n")
        sys.stdout.write(f"path={' '.join(path_ids)}\n")
        return 0

    if args.cmd == "circuit":
        hops = int(getattr(args, "hops", 3) or 3)
        hop_err = _check_hops(hops)
        if hop_err:
            return _die(hop_err, "Next: miragegrid circuit --hops 3")
        try:
            with MirageSession(hops=hops) as session:
                payload = session.circuit.to_dict()
        except ValueError as exc:
            return _die(str(exc), "Next: miragegrid circuit --hops 3")
        if as_json:
            _write_json(payload)
            return 0
        hops_out = payload.get("hops") or []
        names = [str(item.get("node_id")) for item in hops_out if isinstance(item, dict)]
        path = payload.get("path") or []
        entry = names[0] if names else "—"
        sys.stdout.write(
            "Circuit\n"
            f"Entry: {entry}\n"
            f"Hops: {' '.join(names) if names else '—'}\n"
            f"Path: {' → '.join(path) if path else '—'}\n"
            "\n"
            "Full record: miragegrid circuit --json\n"
        )
        return 0

    if args.cmd == "verify-receipt":
        path = Path(args.file)
        if not path.is_file():
            return _die(
                f"Receipt file not found: {path}",
                "Next: miragegrid assign --emit-receipt receipt.json",
            )
        try:
            rec = Receipt.load(path)
        except (ReceiptError, OSError, json.JSONDecodeError) as exc:
            return _die(
                f"Could not read that receipt: {exc}",
                "Next: miragegrid assign --emit-receipt receipt.json",
            )
        status = rec.verify(NodePool())
        payload = {
            "integrity": status,
            "session_id": rec.session_id,
            "mirage_node": rec.mirage_node,
            "timestamp": rec.timestamp,
            "hash_ok": rec.hash_ok(),
        }
        if as_json:
            _write_json(payload)
            return 0 if status == "PASS" else 1
        word = "passed" if status == "PASS" else "failed"
        hash_word = "yes" if payload["hash_ok"] else "no"
        sys.stdout.write(
            f"Receipt {word}.\n"
            f"Session: {payload['session_id']}\n"
            f"Entry node: {payload['mirage_node']}\n"
            f"Time: {payload['timestamp']}\n"
            f"Hash ok: {hash_word}\n"
        )
        if status != "PASS":
            sys.stderr.write("Next: miragegrid assign --emit-receipt receipt.json\n")
        return 0 if status == "PASS" else 1

    if args.cmd == "vpn":
        host = _loopback(args.host)
        from miragegrid.vpn import serve_vpn

        if not as_json:
            sys.stdout.write(f"SOCKS5 proxy on {host}:{int(args.port)}\n")
        serve_vpn(host=host, port=int(args.port))
        return 0

    if args.cmd == "node":
        host = _loopback(args.host)
        from miragegrid.transport import MeshListener

        mesh = NodeMesh()
        try:
            listener = MeshListener(mesh, args.node_id, host=host, port=int(args.port) or None)
        except KeyError:
            return _die(
                f'Unknown peer "{args.node_id}".',
                "Next: miragegrid nodes",
            )
        h, p = listener.start()
        sys.stdout.write(f"Peer {args.node_id} is listening on {h}:{p}\n")
        try:
            import threading

            while True:
                threading.Event().wait(3600)
        except KeyboardInterrupt:
            sys.stdout.write("\nPeer stopped.\n")
        finally:
            listener.stop()
        return 0

    if args.cmd in ("ui", "serve"):
        host = _loopback(args.host or DEFAULT_HOST)
        serve(host=host, port=int(args.port))
        return 0

    if args.cmd == "doctor":
        from miragegrid.doctor import run_doctor

        return run_doctor(as_json=as_json)

    if args.cmd == "import":
        from miragegrid.jsonio import import_json

        try:
            rec = import_json(args.path)
        except FileNotFoundError:
            return _die(
                f"File not found: {args.path}",
                "Next: miragegrid import path/to/file.json",
            )
        except json.JSONDecodeError:
            return _die(
                "That file is not JSON.",
                "Next: miragegrid import path/to/file.json",
            )
        except (OSError, ValueError) as exc:
            return _die(str(exc), "Next: miragegrid import path/to/file.json")
        if as_json:
            _write_json(rec)
            return 0
        keys = ", ".join(rec.get("keys") or []) or "—"
        sys.stdout.write(
            f"Imported {rec.get('imported')}\n"
            f"Stored {rec.get('stored')}\n"
            f"Keys: {keys}\n"
        )
        return 0

    if args.cmd == "export":
        from miragegrid.jsonio import export_json

        try:
            rec = export_json(args.path)
        except OSError as exc:
            return _die(str(exc), "Next: miragegrid export path/to/file.json")
        if as_json:
            _write_json(rec)
            return 0
        sys.stdout.write(f"Exported {rec.get('exported')}\nAuthor: {rec.get('author')}\n")
        return 0

    if args.cmd == "generator-tick":
        from miragegrid.az_generator import DeepNode, PaperVault, synthetic_papers

        vault = PaperVault(synthetic_papers(int(args.papers)))
        node = DeepNode(args.node_id, vault=vault)
        out = node.tick(now_s=float(args.now_s), name=args.name)
        if as_json:
            _write_json(out)
            return 0 if out.get("ok") else 1
        code = out.get("code") or ("ok" if out.get("ok") else "refused")
        message = out.get("message") or ""
        sys.stdout.write(f"Factory tick: {code}\n")
        if message:
            sys.stdout.write(f"{message}\n")
        sys.stdout.write("\nFull record: miragegrid generator-tick --json\n")
        return 0 if out.get("ok") else 1

    return _die(f'Unknown command "{args.cmd}".', "Try: miragegrid ui    or    miragegrid --help")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
