# Contributing to MirageGrid

**Forks are first-class.** This project is Apache-2.0; you do not need
permission to fork, patch, or redistribute. Pull requests are welcome
if you want a change upstream. Keep a fork forever if you do not.

**Forks are welcome and always allowed.**

## How to run tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q
```

Python 3.10+. Core is stdlib only (`secrets`, `hashlib`, `hmac`,
`socket`, `http.server`). ChaCha20-Poly1305 and X25519 are in-tree.
pytest is the dev extra.

## Ground rules

1. Treat `origin` as one peer among many. Downstream forks are part of
   the download-tracking model (see `workers/download-tracker`): they
   report as `{owner}/{repo}`, not as anonymous noise.
2. **This is a lawful privacy mesh VPN.** Keep default binds on
   loopback (`127.0.0.1`) unless the operator opts into a listen
   address. Do not add crime instructions, log-wipe APIs, source-address
   spoofing, or traffic-analysis evasion cookbooks.
3. **Do not destroy logs to evade inspection.** Session mapping drop is
   in-process forget of the assignment and onion keys. It is documented.
   It is not a wipe API.
4. **Keep `random.choice` out of the protocol path.** Section 6 is
   `SHA-256(entropy || timestamp_utf8) % 25` via `secrets.token_bytes`.
   Extra hops use `SHA-256(entropy || timestamp || b"|hop|" || salt)`.
5. **Receipts stay internal by default.** Do not add a public API that
   always emits receipts. `--emit-receipt` is operator-requested local
   JSON.
6. **Keep the dependency list tiny.** Stdlib only in the core. Dev extra
   is pytest.
7. **Do not invent evaluation numbers.** If you measure something,
   publish the method next to the number.
8. New behavior needs a test that fails without the change.
9. Author line stays **Aziel Eliab**.

## Where to change things

- Node pool: `miragegrid/pool.py`
- Mesh / routing: `miragegrid/mesh.py`
- Onion circuits: `miragegrid/circuit.py`
- Crypto: `miragegrid/crypto.py`
- SOCKS5 VPN: `miragegrid/vpn.py`
- Peer transport: `miragegrid/transport.py`
- Section 6 RNG: `miragegrid/rng.py`
- Session lifecycle: `miragegrid/session.py`
- Receipts / integrity: `miragegrid/receipt.py`, `miragegrid/canon.py`
- CLI: `miragegrid/cli.py`
- Localhost UI: `miragegrid/ui.py`, `miragegrid/templates/ui.html`

## Reporting downloads from a fork

Point users at GitHub Releases. The worker homepage counts `GET
/download` for this project. See `workers/download-tracker/README.md`.

## License of contributions

By submitting a change you agree it is licensed under Apache-2.0, the
same license as the rest of the tree. Keep the copyright lines honest.
