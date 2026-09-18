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
8. **Door vs local op.** `/v1/mesh/*` PROXY to aziel-runtime. Local ops are `/v1/{op}` only.
   Suite mesh default OFF; QNM rollup live|locked|isolated; no Node Gate;
   no auto-heal; not anonymity. Product topology stays at `/v1/topology`.
   Mesh law is SPLIT THE WIRES + COLD-COPY SURVIVAL + REHEAL +
   AZ-GENERATOR-1.0 + MIRAGE-GRID-SHIFT-1.0 + AIRGAP-1.0
   (`docs/mesh-law.md`). REDLINE-1.0 (`docs/REDLINE-1.0.md`): GET never
   enables radios or plants claims; AZ Generator is not callable;
   `public_icann:false`; `resolves_to_hub:false`; Cloudflare TLS only;
   FoldLock cite-only.    Cite the named app Worker `miragegrid.vibelock.workers.dev` for
   Cap-7 shuffle / FragGate doors. Cite
   `miragegrid-download-tracker.vibelock.workers.dev` for counted
   downloads. Historical CF 1042 is closed by Worker `miragegrid`.
   `/shelves` cites
   corpus canonical; do not invent a Framagit URL. Assign stays live. Hosted vpn/hop/tunnel stubs
   remain refuse. Do not add neighbor talk-back heal, vote-to-fix
   labeled as auto-heal, live body sync, paper-body fan-out on the 1s
   tip tick, a shared 1s/777s/7m77s socket, a public “call generator”
   door, Softwares-tab products for AZ Generator or Node Gate, unmarked
   hub tunnel hydra, official hubs as airgap Node Gate, fake ICANN
   registration success, more than exactly two public browser hosts of
   Cap-7, mapping mesh names onto hub hostnames as resolution, inventing
   `www.survivalnetwork.az` as live HTTPS when Cap-7 is empty, visible
   15:20 chrome, invented Zenodo DOIs, or
   falsify/ambiguous/misleading verbs (NO-FAN-1.0: No falsification. No
   ambiguity. No misleading.). SEMANTIC-BRIDGE-1.0 is Growth-ON
   discovery (`docs/SEMANTIC-BRIDGE-1.0.md`).
9. New behavior needs a test that fails without the change.
10. Author line stays **Aziel Eliab**.

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
- Isolated counter: `workers/download-tracker/`
- Suite mesh / QNM Live Nodes: `workers/download-tracker/src/mesh.js` (`/v1/mesh/*` PROXY to aziel-runtime). QNS-CD-1.0 photon QNS1 packet transfer is a hub cite / Worker mesh cross-map only (local qnsd in AzielEliab/qnm-node; runtime cites in AzielEliab/aziel-runtime). Not a Softwares-tab product. No public qnsd proxy.

## Reporting downloads from a fork

Point users at GitHub Releases. The worker homepage counts `GET
/download` for this project. See `workers/download-tracker/README.md`.

## License of contributions

By submitting a change you agree it is licensed under Apache-2.0, the
same license as the rest of the tree. Keep the copyright lines honest.
