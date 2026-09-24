# MirageGrid

**Distributed Static Masking Layer for AZ-OS**

Conceptual Whitepaper — Formal Architecture Draft

**Version:** 1.0
**Status:** Conceptual Architecture Specification
**Layer:** Network Obfuscation / Identity Separation
**Author:** Aziel Eliab
**License:** Apache-2.0
**Date:** 2026

---

## Implementation note (package `miragegrid` 0.2.0)

This repository implements a **userspace node-mesh VPN and anonymity
network**: persistent 25-node mesh, X25519 identities, circulant peer
routing, ChaCha20-Poly1305 onion circuits, and a loopback SOCKS5
gateway. Optional `endpoint` strings are listen targets.

Session mapping drop is in-process forget of the assignment and onion
keys, not a log wipe. Hosted `/v1` is the control plane (assign / mesh
/ route / receipt). Packet forwarding runs in the local package.

GodLock already used a 25-node grid. This is the standalone mesh VPN
with receipts and session lifecycle.

The conceptual paper (sections 1–11) is the architecture story.
Section 12 records what 0.2.0 actually ships.

---

## 1. Abstract

MirageGrid is a distributed identity abstraction layer designed for
AZ-OS.

Instead of using a single network address that can be correlated to an
origin device, MirageGrid operates a static pool of 25 persistent IP
endpoints.

At session initialization the system randomly selects one endpoint,
presenting that address as the system's outward identity.

Each session therefore appears to originate from one of many legitimate
static nodes, rather than a single traceable machine.

The system behaves similarly to a digital phone booth:

- The user enters the system
- The system selects a booth
- The call originates from the booth
- The user leaves with no persistent booth identity

## 2. Design Goals

**Identity Dispersion**
Prevent correlation between sessions by distributing outbound identity.

**Static Legitimacy**
Each node appears as a normal persistent network endpoint, avoiding the
volatility signature of rotating proxies.

**Randomized Assignment**
Session identity is randomly selected, preventing deterministic tracking.

**AZ-OS Integration**
All assignments generate receipts and integrity verification under the
AZE / DIF-E system, ensuring deterministic execution and immutable event
history.

## 3. System Architecture

MirageGrid consists of four components:

### 3.1 Static Node Pool

A distributed pool of 25 static IP nodes acting as outward gateways.

Example:

- Node01
- Node02
- Node03
- …
- Node25

In this implementation the records are `node-01` … `node-25` with labels
`Node01` … `Node25`.

### 3.2 Session Randomization Engine

Conceptual sketch:

```
selected_node = random.choice(node_pool)
```

The protocol actually implemented is section 6. `random.choice` is not
used on the protocol path.

### 3.3 Identity Separation

```
User Device
   ↓
AZ-OS Network Layer
   ↓
MirageGrid Session Assignment
   ↓
Selected Static Node
   ↓
External Network
```

In v0.2.0 the selected node is the circuit **entry**. The session also
builds middle/exit hops and a mesh walk. SOCKS5 (`miragegrid vpn`)
opens sockets on loopback.

### 3.4 Receipt Layer

```
Session ID: 78A4F1
Mirage Node: 14
Timestamp: 2026-03-04T13:02:12Z
Integrity: PASS
```

The receipt exists internally and is not externally accessible. An
operator may emit a local JSON file on request (`--emit-receipt`).

## 4. MirageGrid Node Model

Each node functions as a stable endpoint rather than a rotating proxy.

Characteristics:

- Static IP
- Persistent host identity
- Encrypted relay tunnel
- Ephemeral session binding

**Open-core mapping:** persistent mesh identity (`node-NN` + X25519
key), ephemeral onion circuit, default listen `127.0.0.1:19000+N`.

## 5. Session Lifecycle

1. User initiates connection
2. MirageGrid randomization engine selects node
3. Encrypted tunnel established
4. Session operates through node
5. Session ends
6. Mapping destroyed

Next session receives a new node selection.

**Open-core mapping:** step 3 builds a ChaCha20-Poly1305 onion circuit
and may start the local SOCKS5 gateway. Step 6 drops circuit keys and
sets the session node to `None` (`MappingDestroyedError` on access).
It does not shred operator logs.

## 6. Random Selection Protocol

```
seed = system_entropy + timestamp
rng = cryptographic_random(seed)
node_index = rng % 25
```

### Exact bytes (v0.2.0, unchanged from v0.1.0 for hop 0)

| Piece | Encoding |
|-------|----------|
| `system_entropy` | 32 bytes from `secrets.token_bytes(32)` (or caller-supplied) |
| `timestamp` | UTC ISO-8601 with trailing `Z`, second precision, UTF-8 |
| concatenated seed | `entropy \|\| timestamp.encode("utf-8")` |
| `cryptographic_random` | `SHA-256(seed)` (32-byte digest) |
| `node_index` | `int.from_bytes(digest, "big") % 25` (range `0..24`) |

Index `0` is `node-01` / `Node01` / mirage_node `1`. Index `24` is
`node-25`.

## 7. Virtual Phone Booth Model

MirageGrid follows the phone booth principle:

- You enter
- You make a call
- The call originates from the booth
- You leave

Each session originates from a different booth node.

## 8. AZ-OS Integration

MirageGrid sits between:

- AZ Browser
- AZ Mail
- AZ Network Core

Integration modules:

- metadata scrubber
- tunnel manager
- node randomizer
- receipt generator

v0.2.0 ships the node randomizer, receipt generator, mesh router,
onion circuit manager, and userspace SOCKS5 gateway. A full metadata
scrubber remains a later layer.

## 9. Security Model

MirageGrid protects against:

- basic IP correlation
- pattern tracking
- infrastructure inference

It does **not** guarantee anonymity against global surveillance or
endpoint compromise.

## 10. Future Extensions

- MirageGrid-100
- Dynamic Node Geography
- Temporal Node Cycling
- Adaptive Trust Scoring

## 11. Formal Definition

MirageGrid is a distributed static identity abstraction system in which
outbound network identity is randomly selected from a fixed pool of
persistent nodes, preventing correlation between sessions while
maintaining deterministic internal auditability.

## 12. Mesh VPN MVP (package 0.2.0)

The open-core package is a lawful privacy **node-mesh VPN**:

- Topology: circulant graph C_25(1,2,5), diameter 3, always connected.
- Identities: X25519 per node, derived from a mesh seed (RFC 7748).
- Circuits: 3 hops by default (entry / middle / exit). Hop 0 uses
  section 6. Further hops use
  `SHA-256(entropy || timestamp_utf8 || "|hop|" || salt_u32be)`.
- Payload: ChaCha20-Poly1305 onion (RFC 8439). Link keys: X25519 DH.
- Local VPN: SOCKS5 CONNECT on 127.0.0.1:1080 (`miragegrid vpn`).
- Peer listener: `miragegrid node` (loopback by default).

It does not guarantee anonymity against a global adversary. It is not
a crime tool.

The Worker homepage shows a suite Live Nodes strip. `/v1/mesh/*` PROXY
to aziel-runtime. Suite mesh default OFF. QNM rollup is
live|locked|isolated counts only. QNS-CD-1.0 (photon QNS1 packet
transfer) is a hub cite / Worker mesh cross-map only — local qnsd is
qnm-node; runtime cites live in aziel-runtime. No Node Gate. No public
qnsd proxy. No auto-heal. Not an anonymity network. Anon-broadcast is
not a publish path. Hosted MirageGrid remains session assignment;
packet forwarding stays local. Assign stays live. Hosted mesh /
vpn-hop / tunnel stubs remain refuse.

## 13. Locked mesh law (STW-1.0 · CCS-1.0 · RH-1.0)

Author: Aziel Eliab only. Full text: [mesh-law.md](mesh-law.md).

**SPLIT THE WIRES.** Fast 0.5–1s tip tick = presence + tip hash only,
fixed-size (no body/diff/file). Payload is a pull-only second plane
(never sender fan-out). Update is proof, not a timer (cite prev +
lockset, fail-closed; 777s dwell after a valid cite; clock desync is
not yes; ambiguous tip isolates). Equivocation ends the peer (same prev,
two tips → lock/isolate; quorum is not truth). Emit last locally after
verify. Phoenix is local to the failed node only. No unsend of an
unverified body. Partition does not auto-splice; rejoin is cite +
operator/lockset. Heartbeat loss is not poison and does not apply the
last packet. The 1s tip socket and the 777s dwell socket never share.

**COLD-COPY SURVIVAL.** Multiply cold copies. Refuse live body sync.
The tip is expensive to erase. A server pull cannot wipe cold replicas.
Poison is hash-absolute refuse. Data outlives creators.

**REHEAL.** No neighbor talk-dirty-back-to-health. Heal from own tip +
trusted pull, or phoenix-WAIT. Allowed fields: live / locked / isolated
/ tip-hash. Forbidden: bodies, diffs, vote-to-fix. Public-stack
**auto-heal** means this lawful reheal + archive re-expand
(REHEAL-1.0 / MESH-REHEAL). Suite `MESH_AUTO_HEAL` stays false.

## 14. Public stack (locked wording)

MirageGrid’s public stack is now three named pieces:

1. **Anonymity network** — onion/mesh privacy (existing MVP stays a
   lawful privacy tool).
2. **Node Gate** — the MirageGrid admission/claim surface for `.az`
   names (NOT azieleliab.com, NOT godlock.uk, NOT corpus — those hubs
   are not Node Gate).
3. **Auto-heal** — MUST obey REHEAL-1.0 / MESH-REHEAL: heal from own
   last good tip + verified trusted pull, or phoenix-WAIT. NEVER
   neighbor vote-to-fix / majority fanfic. “Auto-heal” in copy means
   that lawful reheal + archive re-expand, not peer talk-back-to-health.

AZ Generator and Node Gate are MirageGrid subsystems / law — not
Softwares-tab products. MirageGrid remains the Softwares product.

## 15. AZ Generator (AZ-GENERATOR-1.0)

Full text: [AZ-GENERATOR-1.0.md](AZ-GENERATOR-1.0.md).

The generator lives deep in the node and is not called from outside.
Every **7 minutes and 77 seconds** (period **497s**) the local tick
attempts a claim and exits the FRONT Node Gate. Cap-7 mesh DNS
factory (not ICANN). Suffix order `.az` → `.aziel` → honest pivot.
First flag `www.survivalnetwork.<active-suffix>`. Exactly 2 of Cap-7
are public browser gateways; access is AZNet + AZBrowser.

Restore a broken chain at its most active guaranteed point. Restore
requires **at least 49 Aziel Eliab papers** from the node’s **local
vault** (hash-absolute; cite don’t merge; bytes↔hash). Every node MUST
carry the full Aziel Eliab paper set as a **cold vault copy** — **vault
multiply onto each node** / **papers land on every node as cold
copies** on bootstrap / join / Cap-7 claim / grid-shift standby
(pull-only; no live body sync of paper bytes on the 1s tip tick).
Incomplete vault or “we have 49” without bytes →
AZG-UNVERIFIED-TIP / incomplete vault; phoenix-WAIT; do not invent.
Fewer than 49 → phoenix-WAIT / hold; no false tip.

NO-LIE / NO-REWRITE · **No falsification. No ambiguity. No
misleading.** (NO-FAN-1.0). `<49` papers or unverified tip → refuse
the claim; do not invent continuity. If `www.survivalnetwork.az`
cannot be claimed, resume normal — do not fake the flag. Offline
origin: downloads stay up (MESH-VAULT snapshot+standby). The 7m77s
claim clock never shares a socket with the 1s tip tick or the 777s
dwell.

## 16. Grid shift · Cap-7 · cloak burst (MIRAGE-GRID-SHIFT-1.0)

Full text: [MIRAGE-GRID-SHIFT-1.0.md](MIRAGE-GRID-SHIFT-1.0.md).

MESH-VAULT is snapshot plus official standby — an IP-mask host. A
**grid shift** keeps the `.az` (or standby) name answerable for
downloads while the node is cloaked/hidden after a domain pull.
Official-hub Cloudflare tunnels die with the pull (TUN-WP / NODE-OPS).
Not resurrection of godlock.uk / corpus hostnames.

When lawful auto-heal fires, a cloak burst may plant up to Cap-7 spare
`.az` names with a cloak on top. Cloak/grid-shift must not pretend a
pulled official hub hostname is still the cell. `.az` names are named
MirageGrid hosts, not unmarked hydra. Auto-heal must not be worded as
neighbor resurrection.

## 17. Scope restatements (not MirageGrid)

**GodLock** on godlock.uk is a dark stress-test engine for
intelligent-design challenges (one challenge box; Yes/No/Let’s
review/Interesting; hash-chained receipts). It is not a forum, not
Node Gate, not the AZ Generator, not an anonymity network. Softwares
on godlock.uk stay GodLock-first / Runtime-pointer only. GodLock
challenge receipts ≠ ACT-RECEIPT public action receipts.

**AZBot / AZindex** gates hub ingest / first-screen PRs (corpus, ae,
godlock, HDJ, runtime ingest) with AZindex-OK. AZBot does not operate
Node Gate, does not claim `.az` domains, and is not the AZ Generator.

Official hubs (azieleliab.com, azielcorpuslibrary.net, godlock.uk,
hedidntjump.com) remain named public hosts. They are not Node Gate
and are **not** airgap Node Gate. azieleliab.com hosts software/runtime
but is not login-recovery or Node Gate (QNM-BUILD).

## 18. Airgap (AIRGAP-1.0)

Full text: [AIRGAP-1.0.md](AIRGAP-1.0.md).

Airgap = local vault + no bearer radios + no climb-back onto pulled
public hub hostnames. Downloads / serve from the local cold shelf stay
allowed while airgapped (sites stay up for downloads when origin is
offline). Tip chatter: live / locked / isolated / tip-hash only if
any; no body gossip. Re-expand / reheal: own tip + trusted pull of
bytes already trusted, or phoenix-WAIT — never neighbor majority.

## 19. Semantic bridge (SEMANTIC-BRIDGE-1.0)

Full text: [SEMANTIC-BRIDGE-1.0.md](SEMANTIC-BRIDGE-1.0.md).

Public Plane-A hosts + the MirageGrid Worker are the AI-facing
bridge. Internet reaches AZ domains only
(AZ.AzielEliab.AZ, AZ.AzielCorpusLibrary.AZ, AZ.Godlock.AZ,
AZ.HeDidntJump.AZ) via the four hub websites
(`public_icann: true`, `resolves_to_hub: true`). Cap-7 auto-generates
`.az` duplications of those hubs and shifts them with StaticLock +
MirageGrid cloak and VPN. Four factory names are real hub duplications.
Three are false sites. Factory honesty is LIVE. Cap-7 is not typed on
ICANN DNS. Named sites azcorpus + azlibrary are designs inside
azielcorpuslibrary.net (hash-absolute `/design-packs/*`) and stay
`public_icann: false`. Growth-ON. CROSS-NETWORK-SURVIVAL + NO-LIE.
Re-expand is archive, not index. Named app Worker is
`miragegrid.vibelock.workers.dev` (Cap-7 LIVE shuffle). Download plane
is `miragegrid-download-tracker.vibelock.workers.dev`. Historical CF
1042 is closed by creating Worker `miragegrid`.
`GET /shelves` points at corpus canonical. See [REDLINE-1.0.md](REDLINE-1.0.md).
