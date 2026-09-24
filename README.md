# MirageGrid

Open a local circuit through 25 mesh peers on this computer.

**Author:** Aziel Eliab

## Start

1. Install.

   ```bash
   python -m venv .venv && source .venv/bin/activate && pip install -e .
   ```

2. Open the console.

   ```bash
   miragegrid ui
   ```

3. Choose **Open a circuit**.

The console is at http://127.0.0.1:8080 (this computer only).
`miragegrid doctor` checks the install. `miragegrid --help` lists commands.
People get short text. Machines use `--json`.

Cap-7 is the mesh DNS factory: four hub mirrors and three decoys. It keeps those names on the mesh. It does not register names at a public ICANN registrar.

A local SOCKS5 proxy, when you want it:

```bash
miragegrid vpn
```

It listens at `127.0.0.1:1080`.

See [RUN.txt](RUN.txt), the spec [docs/whitepaper.md](docs/whitepaper.md), and [CONTRIBUTING.md](CONTRIBUTING.md). License: [Apache-2.0](LICENSE). Version 0.2.0.

## Notes

This is a lawful privacy tool for personal privacy, journalism, and research where you have the right to use it.

The public stack is three pieces: the anonymity network (this local mesh VPN), Node Gate (the admission surface for mesh `.az` names; the hub websites stay the hub websites), and auto-heal (REHEAL-1.0 / MESH-REHEAL: own last good tip plus a verified trusted pull, or phoenix-WAIT). AZ Generator and Node Gate are MirageGrid subsystems. AZ Generator is the Cap-7 mesh DNS factory. It lives deep in the node and exits through the front Node Gate. A node may publish two hosted HTTPS mirrors of the mesh tip; the other Cap-7 names stay on the mesh. Access for mesh names is AZNet and AZBrowser, which stay separate products. See [docs/AZ-GENERATOR-1.0.md](docs/AZ-GENERATOR-1.0.md), [docs/MIRAGE-GRID-SHIFT-1.0.md](docs/MIRAGE-GRID-SHIFT-1.0.md), and [docs/AIRGAP-1.0.md](docs/AIRGAP-1.0.md).


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
- Suite mesh proxy: [https://miragegrid-download-tracker.vibelock.workers.dev/v1/mesh](https://miragegrid-download-tracker.vibelock.workers.dev/v1/mesh) — default OFF; QNM live / locked / isolated; QNS-CD-1.0 photon QNS1 cross-map (no public qnsd). Locked law: **SPLIT THE WIRES**, **COLD-COPY SURVIVAL**, **REHEAL**, **AZ-GENERATOR-1.0**, **MIRAGE-GRID-SHIFT-1.0**, **AIRGAP-1.0** ([docs/mesh-law.md](docs/mesh-law.md))
- OpenAPI: [https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json](https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json)
- Named app Worker (Cap-7 LIVE shuffle): [https://miragegrid.vibelock.workers.dev/](https://miragegrid.vibelock.workers.dev/) — `GET /bridge` · `GET /v1/shuffle` · `POST /v1/shuffle/ping` · `GET /v1/cap7`. Nodes ping until they land on one factory site. That land is the update endpoint for the round. No hard-coded Cap-7 host. Historical CF 1042 is closed by Worker `miragegrid`.
- Semantic bridge (Growth-ON): [app /bridge](https://miragegrid.vibelock.workers.dev/bridge) · [download llms.txt](https://miragegrid-download-tracker.vibelock.workers.dev/llms.txt) · [download bridge.json](https://miragegrid-download-tracker.vibelock.workers.dev/v1/bridge) · [cite.json](https://miragegrid-download-tracker.vibelock.workers.dev/cite.json) · [azcorpus pack](https://miragegrid-download-tracker.vibelock.workers.dev/design-packs/azcorpus.json) · [azlibrary pack](https://miragegrid-download-tracker.vibelock.workers.dev/design-packs/azlibrary.json) · [shelves cite](https://miragegrid-download-tracker.vibelock.workers.dev/shelves) — Internet reaches AZ domains only (AZ.AzielEliab.AZ, AZ.AzielCorpusLibrary.AZ, AZ.Godlock.AZ, AZ.HeDidntJump.AZ) via the four hub websites. Cap-7 auto-generates `.az` duplications of those hubs and shifts them with StaticLock + MirageGrid cloak and VPN: four real hub duplications, three false sites, factory honesty LIVE, not typed on ICANN DNS. Named mesh sites azcorpus + azlibrary remain designs inside azielcorpuslibrary.net. REDLINE-1.0: GET never enables radios or plants claims.
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
receipt). Packet forwarding runs in the **local package**. Assign stays
live. Hosted mesh / vpn-hop / tunnel stubs remain refuse.

**SPLIT THE WIRES** — the 0.5–1s tip tick is presence + tip hash only
(fixed-size; no body/diff/file). Payload is pull-only (never sender
fan-out). Update is proof, not a timer (cite prev + lockset, fail-closed;
777s dwell after a valid cite; clock desync is not yes; ambiguous tip
isolates). Equivocation ends the peer. Emit last locally after verify.
Phoenix is local to the failed node. Partition does not auto-splice.
The 1s tip socket, the 777s dwell socket, and the 7m77s claim socket
never share.

**COLD-COPY SURVIVAL** — multiply cold copies; refuse live body sync;
the tip is expensive to erase; a server pull cannot wipe cold replicas;
poison is hash-absolute refuse; data outlives creators.

**REHEAL** — a neighbor cannot talk a node dirty-back-to-health. Heal
from own tip + trusted pull, or phoenix-WAIT. Allowed: live / locked /
isolated / tip-hash. Forbidden: bodies, diffs, vote-to-fix.
Public-stack auto-heal means this lawful reheal (REHEAL-1.0 /
MESH-REHEAL), not neighbor vote-to-fix.

**AZ GENERATOR** — Cap-7 mesh DNS factory living deep in the node:
four hub mirrors and three decoys. It does not register names at a
public ICANN registrar. 7m77s (497s) local tick exits the front Node
Gate only (the generator is not called from outside). Honest suffix
order `.az` → `.aziel` → pivot. First flag
`www.survivalnetwork.<active-suffix>`. Two of a node's Cap-7 names
may be hosted HTTPS mirrors of the mesh tip; the rest stay mesh/AZNet.
Access via AZNet + AZBrowser. Restore needs ≥49 local vault papers
(vault multiply onto each node as cold copies; no paper-body fan-out
on the 1s tip tick). Incomplete vault refuses (AZG-UNVERIFIED-TIP /
AZG-INCOMPLETE-VAULT). Radio PHY stays in local qnm-node. Hub
`GET /v1/mesh` never enables.

**MIRAGE GRID SHIFT** — MESH-VAULT is snapshot + official standby
(IP-mask host). Grid shift keeps the `.az` answerable and cloaks the
node after a domain pull. Official-hub tunnels die with the pull.
Grid-shift standby is a vault-multiply event.

**AIRGAP** — local vault + no bearer radios + no climb-back onto pulled
public hub hostnames. Downloads from the local cold shelf stay allowed.
Tip chatter: live / locked / isolated / tip-hash only; no body gossip.
Official hubs are not airgap Node Gate.

**NO-LIE / NO-REWRITE / NO-FAN-1.0** — no rewrite key; the network
never lies to stay alive; receipts still hash. **No falsification. No
ambiguity. No misleading.** Ambiguous tip isolates. Do not fake the
flag. Do not invent continuity. Cloak must not pretend a pulled hub
is still the cell.

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

With no arguments, `miragegrid` prints a short welcome and the next command.

```bash
miragegrid
miragegrid --help
miragegrid ui
miragegrid doctor
miragegrid assign
miragegrid vpn
```

Advanced commands stay available: `mesh`, `route`, `circuit`, `verify-receipt`, `node`, `import`, `export`, `generator-tick`, and `serve` (same as `ui`). Add `--json` for the machine document. `assign` still prints the entry peer, session id, circuit hops, and mesh path. A receipt file is written only if `--emit-receipt` is passed.

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
docs/whitepaper.md     architecture (sections 1–19)
docs/mesh-law.md       SPLIT THE WIRES · COLD-COPY · REHEAL · AZ-GENERATOR · GRID-SHIFT · AIRGAP
docs/AZ-GENERATOR-1.0.md  Cap-7 mesh DNS factory · deep-node → Node Gate · paper vault on node
docs/MIRAGE-GRID-SHIFT-1.0.md  Node Gate · cloak burst · MESH-VAULT grid shift
docs/AIRGAP-1.0.md     local vault · no bearer radios · no climb-back
docs/SEMANTIC-BRIDGE-1.0.md  AI discovery of Cap-7 names · not ICANN · design_of only
docs/REDLINE-1.0.md        attack-surface law · GET never enables · sims REFUSE
docs/audit/                Cap-7 LIVE Worker security findings + follow-on
examples/              assign a circuit
workers/download-tracker/   Cloudflare Worker + wrangler.toml (undeployed)
CONTRIBUTING.md        forks first-class; lawful privacy mesh VPN
mobile/              Flutter iPhone + Android (`flutter create .`)
```

## Use with AI assistants

Live HTTPS control plane on the existing download-tracker Worker. **Mesh assignment, peer routes, circuit hops.** Packet forwarding is the local package.

Any MCP- or OpenAPI-capable assistant can import this API, including:

- ChatGPT (GPT Actions / OpenAI)
- Grok (xAI)
- Venice
- Claude (Anthropic)
- Cursor (MCP)
- Glama (MCP)
- Perplexity
- Microsoft Copilot / Bing
- Google Gemini / Vertex
- Mistral
- Meta AI
- Apple Intelligence surfaces
- Amazon Q tooling
- DuckAssist
- You.com
- Cohere
- other MCP/OpenAPI-capable assistants

OpenAPI:

```
https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json
```

Practical import notes: ChatGPT — paste the OpenAPI URL into GPT Actions. Grok — import OpenAPI as a custom tool. Venice — custom HTTP tools from the same URL. Cursor / Glama — connect the MCP catalog. Claude, Perplexity, Copilot / Bing, Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q, DuckAssist, You.com, Cohere, and other OpenAPI/MCP clients — import the OpenAPI document or attach the MCP catalog where the client supports it.

Setup notes: [https://miragegrid-download-tracker.vibelock.workers.dev/ai](https://miragegrid-download-tracker.vibelock.workers.dev/ai)

MCP catalog (ships separately): `https://aziel-runtime.vibelock.workers.dev/mcp`. Suite mesh `/v1/mesh/*` PROXY via `AZIEL_RUNTIME` (default OFF; QNM-BUILD-1.0 live|locked|isolated; QNS-CD-1.0 photon QNS1 packet transfer is a hub cite / Worker mesh cross-map only — [qnm-node](https://github.com/AzielEliab/qnm-node) qnsd + [aziel-runtime](https://github.com/AzielEliab/aziel-runtime) catalog; no Node Gate; no public qnsd proxy). Catalog MCP `mesh_*` + FragGate `slug=mesh`.

```bash
curl -sS -X POST https://miragegrid-download-tracker.vibelock.workers.dev/v1/assign \
  -H "content-type: application/json" \
  -d '{}'
```

## License

Apache-2.0. See [LICENSE](LICENSE).

Forks are welcome and always allowed.
