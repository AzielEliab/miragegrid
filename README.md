# MirageGrid

Node-mesh **VPN** and **anonymity network** for AZ-OS. A persistent
pool of 25 named peers. At session init the system selects an entry
node, builds a multi-hop onion circuit, and routes along the mesh.
An internal receipt is minted. Circuit keys and the session mapping
are destroyed when the session ends.

**Author:** Aziel Eliab
**Version:** 0.2.0 (mesh VPN MVP)
**License:** [Apache-2.0](LICENSE)
**Date:** 2026

> You enter the booth. The mesh selects a booth and builds a circuit.
> The call is attributed to that booth. You leave with no persistent
> booth identity.

See the spec: [docs/whitepaper.md](docs/whitepaper.md).
How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md).

**Forks are welcome and always allowed.**

This is a **lawful privacy tool**. Use it only where you have the right
to do so (personal privacy, journalism, research). It does not authorize
crime, and it does not claim to defeat a global adversary.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
miragegrid ui
```

Local SOCKS5 mesh VPN:

```bash
miragegrid vpn
# socks5://127.0.0.1:1080  — traffic is onion-wrapped through the 25-node mesh
```


## One-click install

```bash
curl -fsSL https://miragegrid-download-tracker.vibelock.workers.dev/install.sh | bash
```

The script curls the **counted** tarball from this project's Worker
(`/download`, User-Agent `Mozilla/5.0`), extracts, makes a venv, and
`pip install -e .`. Then run `miragegrid ui` or `miragegrid vpn`.

Or use the Worker homepage (assign / mesh / route / receipts, plus
**Download** / **One-click install**):
https://miragegrid-download-tracker.vibelock.workers.dev/

## Counted download (Cloudflare Worker)

**This is the counted download.** GitHub releases exist as a mirror.
The Worker serves the gzip itself (HTTP 200, no 302 to GitHub).

- Homepage: [https://miragegrid-download-tracker.vibelock.workers.dev/](https://miragegrid-download-tracker.vibelock.workers.dev/)
- Direct tarball: [miragegrid-0.2.0.tar.gz](https://miragegrid-download-tracker.vibelock.workers.dev/download?asset=miragegrid-0.2.0.tar.gz)
- One-click install: [https://miragegrid-download-tracker.vibelock.workers.dev/install.sh](https://miragegrid-download-tracker.vibelock.workers.dev/install.sh)
- Skill: [https://miragegrid-download-tracker.vibelock.workers.dev/v1/skill](https://miragegrid-download-tracker.vibelock.workers.dev/v1/skill)
- OpenAPI: [https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json](https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json)
- GitHub: [https://github.com/AzielEliab/miragegrid](https://github.com/AzielEliab/miragegrid)

Isolated counter: Worker `miragegrid-download-tracker`, KV `MIRAGEGRID_DOWNLOADS`. `/v1` does not increment downloads.

Open http://127.0.0.1:8080 (loopback only). No CDN, no telemetry. **Node-mesh VPN** — persistent peers, onion circuits, userspace SOCKS5.

Counted download: [https://miragegrid-download-tracker.vibelock.workers.dev/](https://miragegrid-download-tracker.vibelock.workers.dev/)



---

## Architecture (what is real in this tree)

MirageGrid is a **userspace node-mesh VPN** and **anonymity network**:

1. **Persistent mesh** — 25 named peers (`node-01` … `node-25`) with
   X25519 identities and a circulant adjacency (`±1, ±2, ±5`). The
   mesh exists whether or not a session is open.
2. **Peer routing** — shortest-path forwarding on that graph. Optional
   `endpoint` strings are listen targets (`127.0.0.1:19001` by default).
3. **Session circuits** — SHA-256 selection of an entry node, then
   distinct middle/exit hops. Payload is ChaCha20-Poly1305 onion-wrapped
   (exit layer innermost). Link hops use X25519-derived keys.
4. **Userspace VPN** — `miragegrid vpn` binds SOCKS5 on 127.0.0.1:1080.
   CONNECT streams are packed, unwrapped at the exit hop, then opened.
5. **Receipts** — internal: session_id, mirage_node (entry 1–25),
   timestamp, integrity. Mapping drop is in-process forget, not a wipe.

The hosted Worker is the **control plane** (assign / mesh / route /
receipt). Packet forwarding runs in the **local package**.

MirageGrid does **not** guarantee anonymity against global surveillance
or endpoint compromise.

---

## Download

**Hosted (Cloudflare Worker, counted across branches and forks):**

# → [https://miragegrid-download-tracker.vibelock.workers.dev/](https://miragegrid-download-tracker.vibelock.workers.dev/) ←

Direct file: [miragegrid-0.2.0.tar.gz](https://miragegrid-download-tracker.vibelock.workers.dev/download?asset=miragegrid-0.2.0.tar.gz)

- Tracker home: [https://miragegrid-download-tracker.vibelock.workers.dev/](https://miragegrid-download-tracker.vibelock.workers.dev/)
- Stats: [https://miragegrid-download-tracker.vibelock.workers.dev/stats](https://miragegrid-download-tracker.vibelock.workers.dev/stats)
- GitHub releases: [https://github.com/AzielEliab/miragegrid/releases](https://github.com/AzielEliab/miragegrid/releases)

The worker homepage shows a **live download count for this project
only**. The counter is isolated to MirageGrid (its own Worker + KV), not
VibeLock. `GET /download` increments the count. `GET /count` returns
`{project, total}`.

Query params: `owner`, `repo` (`owner/repo` is accepted), `branch`,
`fork` (`1` or `owner/repo`), `tag`, `asset`. See the worker README.

---

## What it does

1. **Static node mesh** — exactly 25 persistent records: id `node-01` …
   `node-25`, X25519 identity, default listen port `19000+N`.
2. **Session randomization** (paper §6) —
   `seed = system_entropy || timestamp_utf8`;
   `node_index = SHA-256(seed) as big-endian int % 25`.
   Further hops use `SHA-256(entropy || timestamp || b"|hop|" || salt)`.
   Uses `secrets.token_bytes` / `hashlib.sha256`. Not `random.choice`.
3. **Lifecycle** — initiate → assign entry + circuit → operate
   (`MirageSession` / SOCKS5) → end → mapping and onion keys destroyed
   (`MappingDestroyedError` on `session.node` after close).
4. **Receipt** — internal: session_id (hex), mirage_node (1–25),
   timestamp UTC ISO, integrity PASS/FAIL. Default: in-memory, not a
   public API. Optional `--emit-receipt FILE.json` for the operator.
5. **Integrity** — PASS if the entry node is in the pool, the circuit
   is open, and the session is not closed; FAIL otherwise.

The next session gets an independent circuit.

Localhost UI: `miragegrid ui` (alias `serve`) binds **127.0.0.1 only**.


## iPhone & Android

Flutter sources: [`mobile/`](mobile/). Application id `com.azieeliab.miragegrid`. Offline. No analytics. Dark matte / gold.

Assign a mesh circuit (entry 1–25 plus hops) and mint a receipt. Companion to the desktop node-mesh VPN.

```bash
cd mobile
flutter create --org com.azieeliab --project-name miragegrid .
flutter pub get
flutter run
```

The `android/` and `ios/` folders in this tree are skeleton READMEs until you run `flutter create .` (this machine has no Flutter SDK on PATH). Then open `android/` in Android Studio or `ios/Runner.xcworkspace` in Xcode. Not a store listing.

## Install

Python 3.10+. Stdlib only in the core (ChaCha20-Poly1305 and X25519 are in-tree).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

From a release artifact:

```bash
python -m pip install miragegrid-0.2.0.tar.gz
```

## CLI

```bash
miragegrid version
miragegrid nodes
miragegrid mesh
miragegrid route --from node-01 --to node-17
miragegrid assign
miragegrid assign --emit-receipt receipt.json
miragegrid circuit
miragegrid verify-receipt receipt.json
miragegrid vpn --host 127.0.0.1 --port 1080
miragegrid node --id node-01 --host 127.0.0.1 --port 19001
miragegrid ui --host 127.0.0.1 --port 8080
miragegrid serve --host 127.0.0.1 --port 8080
```

`assign` prints the entry node, session id, circuit hops, and mesh path.
A receipt file is written only if `--emit-receipt` is passed.

Library:

```python
from miragegrid.session import MirageSession

with MirageSession() as session:
    print(session.node.id, session.circuit.hop_ids)
    print(session.wrap(b"hello"))
# mapping and circuit keys destroyed
```

## Example

```bash
python examples/assign_session.py
```

## Tests

```bash
pip install -e ".[dev]"
python -m pytest -q
```

Offline. Stdlib runtime. Mesh/VPN tests use loopback only.

## Layout

```
miragegrid/            library (pool, mesh, circuit, crypto, vpn, session, cli, ui)
tests/                 pytest
docs/whitepaper.md     architecture (sections 1–12)
examples/              assign a circuit
workers/download-tracker/   Cloudflare Worker + wrangler.toml (undeployed)
CONTRIBUTING.md        forks first-class; lawful privacy mesh VPN
mobile/              Flutter iPhone + Android (`flutter create .`)
```

## Use with Grok, ChatGPT, Venice

Live HTTPS control plane on the existing download-tracker Worker. **Mesh assignment, peer routes, circuit hops.** Packet forwarding is the local package.

OpenAPI (ChatGPT GPT Actions / Venice custom HTTP / Grok custom tool):

```
https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json
```

Setup notes: [https://miragegrid-download-tracker.vibelock.workers.dev/ai](https://miragegrid-download-tracker.vibelock.workers.dev/ai)

MCP catalog (ships separately): `https://aziel-runtime.vibelock.workers.dev/mcp`

```bash
curl -sS -X POST https://miragegrid-download-tracker.vibelock.workers.dev/v1/assign \
  -H "content-type: application/json" \
  -d '{}'
```

## License

Apache-2.0. See [LICENSE](LICENSE).

Forks are welcome and always allowed.
