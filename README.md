# MirageGrid

Distributed identity *abstraction* for AZ-OS: a static pool of 25 named
logical nodes. At session init, one is selected cryptographically as the
outward identity. An internal receipt is minted. The mapping is destroyed
when the session ends.

**Author:** Aziel Eliab
**Version:** 1.0 conceptual architecture (package `miragegrid` 0.1.0)
**License:** [Apache-2.0](LICENSE)
**Date:** 2026

> You enter the booth. The system selects a booth. The call is attributed
> to that booth. You leave with no persistent booth identity.

See the spec: [docs/whitepaper.md](docs/whitepaper.md).
How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md).

**Forks are welcome and always allowed.**

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
miragegrid ui
```

Open http://127.0.0.1:8080 (loopback only). No CDN, no telemetry. **Not a VPN, proxy mesh, Zoom tether, or Tor hop.** Logical node ids only.

Counted download: [https://miragegrid-download-tracker.vibelock.workers.dev/](https://miragegrid-download-tracker.vibelock.workers.dev/)



---

## This repo is not an anonymity network

This tree is an open, auditable **assignment + receipt engine**. Nodes
are logical identities (`node-01` … `node-25`). Optional `endpoint`
strings in a config file are **labels only** — this package never
connects, never tunnels, never hops IPs, never speaks Tor or SOCKS, and
never hides an origin address.

GodLock already used a 25-node logical grid. This is the standalone spec
with receipts and session lifecycle.

**MirageGrid does not guarantee anonymity against global surveillance or
endpoint compromise.** Session mapping drop is *in-process forget*,
documented, not a log wipe.

Do not treat this repository as a VPN, proxy mesh, or traffic-analysis
breaker.

---

## Download

**Hosted (Cloudflare Worker, counted across branches and forks):**

# → [https://miragegrid-download-tracker.vibelock.workers.dev/](https://miragegrid-download-tracker.vibelock.workers.dev/) ←

Direct file: [miragegrid-0.1.0.tar.gz](https://miragegrid-download-tracker.vibelock.workers.dev/miragegrid-0.1.0.tar.gz)

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

1. **Static node pool** — exactly 25 persistent records: id `node-01` …
   `node-25`, label `Node01` … `Node25`, optional endpoint label.
2. **Session randomization** (paper §6) —
   `seed = system_entropy || timestamp_utf8`;
   `node_index = SHA-256(seed) as big-endian int % 25`.
   Uses `secrets.token_bytes` / `hashlib.sha256`. Not `random.choice`.
3. **Lifecycle** — initiate → assign node → operate (`MirageSession`
   handle) → end → mapping destroyed (`MappingDestroyedError` on
   `session.node` after close).
4. **Receipt** — internal: session_id (hex), mirage_node (1–25),
   timestamp UTC ISO, integrity PASS/FAIL. Default: in-memory, not a
   public API. Optional `--emit-receipt FILE.json` for the operator.
5. **Integrity** — PASS if the node id is in the pool and the session is
   not closed; FAIL otherwise. Optional canonical SHA-256 of those
   fields (TemporalLock-style, copied in-tree).

The next session gets an independent selection.

Localhost UI: `miragegrid ui` (alias `serve`) binds **127.0.0.1 only**.


## iPhone & Android

Flutter sources: [`mobile/`](mobile/). Application id `com.azieeliab.miragegrid`. Offline. No analytics. Dark matte / gold.

Assign a logical node 1–25 and mint a receipt. Labels only. Never a VPN, proxy, or Tor.

```bash
cd mobile
flutter create --org com.azieeliab --project-name miragegrid .
flutter pub get
flutter run
```

The `android/` and `ios/` folders in this tree are skeleton READMEs until you run `flutter create .` (this machine has no Flutter SDK on PATH). Then open `android/` in Android Studio or `ios/Runner.xcworkspace` in Xcode. Not a store listing.

## Install

Python 3.10+. Stdlib only in the core.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

From a release artifact:

```bash
python -m pip install miragegrid-0.1.0.tar.gz
```

## CLI

```bash
miragegrid version
miragegrid nodes
miragegrid assign
miragegrid assign --emit-receipt receipt.json
miragegrid verify-receipt receipt.json
miragegrid ui --host 127.0.0.1 --port 8080
miragegrid serve --host 127.0.0.1 --port 8080
```

`assign` prints the node id and session id. A receipt file is written
only if `--emit-receipt` is passed.

Library:

```python
from miragegrid.session import MirageSession

with MirageSession() as session:
    print(session.node.id, session.session_id)
    # receipt is internal; operator may emit:
    # session.emit_receipt()
# mapping destroyed
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

Offline. Stdlib runtime. No network dependencies.

## Layout

```
miragegrid/            library (pool, rng, session, receipt, canon, cli, ui)
tests/                 pytest, offline
docs/whitepaper.md     1.0 conceptual architecture (sections 1–11)
examples/              assign a session
workers/download-tracker/   Cloudflare Worker + wrangler.toml (undeployed)
CONTRIBUTING.md        forks first-class; no real tunnels/IP hiding PRs
mobile/              Flutter iPhone + Android (`flutter create .`)
```

## License

Apache-2.0. See [LICENSE](LICENSE).

Forks are welcome and always allowed.
