# MirageGrid mesh law

**Author:** Aziel Eliab only  
**Locked:** SPLIT THE WIRES (STW-1.0) · COLD-COPY SURVIVAL (CCS-1.0) · REHEAL (RH-1.0)

Hosted `/v1/assign` stays live. Hosted mesh / vpn-hop / tunnel stubs remain refuse.

This is law, not a timer and not a neighbor vote. Executable copies live in
`miragegrid/mesh.py` and `workers/download-tracker/src/mesh.js`.

## SPLIT THE WIRES (STW-1.0)

Two planes. They never share a socket.

**Fast tip tick (0.5–1s).** Presence + tip hash only. Fixed size (33 bytes:
1-byte presence + 32-byte SHA-256). No body. No diff. No file.

**Payload is a second plane.** Pull-only. The sender never fans out a body.

**Update is proof, not a timer.** Cite prev + lockset. Fail-closed if either
is missing. After a valid cite, dwell **777s**. Clock desync is not yes.
An ambiguous tip isolates.

**Equivocation ends the peer.** Same prev, two tips → lock and isolate.
Quorum is not truth.

**Emit last locally after verify.** Phoenix is local to the failed node only.
There is no unsend of an unverified body.

**Partition.** No auto-splice. Rejoin is cite + operator/lockset. Heartbeat
loss is not poison and does not apply the last packet.

**Sockets.** The 1s tip tick and the 777s dwell never share a socket.

## COLD-COPY SURVIVAL (CCS-1.0)

- Multiply cold copies (minimum two).
- Refuse live body sync. Payload stays pull-only.
- The tip is expensive to erase. Cheap erase is refused.
- A server pull cannot wipe cold replicas.
- Poison is hash-absolute refuse.
- Data outlives creators.

## REHEAL (RH-1.0)

A neighbor cannot talk a node dirty-back-to-health.

Legal sources only:

1. Own tip + trusted pull
2. phoenix-WAIT

Allowed fields: `live`, `locked`, `isolated`, `tip-hash`.

Forbidden: bodies, diffs, vote-to-fix.

This is not auto-heal. `MESH_AUTO_HEAL` stays false. Phoenix-WAIT is local
wait, not a controller hunt and not neighbor gossip.

## Surface

| Surface | What it does |
| --- | --- |
| `miragegrid/mesh.py` | Topology stays live. Law functions refuse illegal planes. |
| Worker `mesh.js` | `/v1/mesh/*` PROXY. Stamps STW/CCS/RH. `/v1/mesh/vpn|hop|tunnel` refuse `MESH-STUB`. `/v1/mesh/reheal` is local law (not neighbor heal). |
| `POST /v1/assign` | Live session assignment. |

Identity: **Aziel Eliab** only.
