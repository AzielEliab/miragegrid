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

## Implementation note (package `miragegrid` 0.1.0)

This repository implements the **assignment + receipt engine** specified
below. Nodes are **logical identities** (`node-01` … `node-25`). Optional
`endpoint` strings are labels only. The open core does **not** hop IPs,
open encrypted relay tunnels, speak Tor, or hide origin addresses.
Session mapping drop is in-process forget, not a log wipe.

GodLock already used a 25-node logical grid. This is the standalone spec
with receipts and session lifecycle.

The conceptual paper talks about static endpoints and tunnels as an
architecture story. That story is preserved in sections 1–11. The
Python package does not expand it into a real network.

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

In v0.1.0 the "selected static node" is a logical identity string. No
socket is opened for the assignment.

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

**Open-core mapping:** persistent *logical* host identity (`node-NN`),
ephemeral in-process session binding. This package does not allocate
real IPs or build relay tunnels.

## 5. Session Lifecycle

1. User initiates connection
2. MirageGrid randomization engine selects node
3. Encrypted tunnel established
4. Session operates through node
5. Session ends
6. Mapping destroyed

Next session receives a new node selection.

**Open-core mapping:** step 3 is a no-op (no tunnel). Step 6 sets the
session node to `None` and raises `MappingDestroyedError` on access.
It does not shred operator logs.

## 6. Random Selection Protocol

```
seed = system_entropy + timestamp
rng = cryptographic_random(seed)
node_index = rng % 25
```

### Exact bytes (v0.1.0)

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

v0.1.0 ships the node randomizer and receipt generator. Tunnel manager
and metadata scrubber are out of scope for this open assignment engine.

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
