# MirageGrid mesh law

**Author:** Aziel Eliab only  
**Locked:** SPLIT THE WIRES (STW-1.0) · COLD-COPY SURVIVAL (CCS-1.0) · REHEAL (RH-1.0 / REHEAL-1.0 / MESH-REHEAL) · AZ-GENERATOR-1.0 · MIRAGE-GRID-SHIFT-1.0

Hosted `/v1/assign` stays live. Hosted mesh / vpn-hop / tunnel stubs remain refuse.

This is law, not a timer and not a neighbor vote. Executable copies live in
`miragegrid/mesh.py` and `workers/download-tracker/src/mesh.js`.

Next-generation papers: [AZ-GENERATOR-1.0.md](AZ-GENERATOR-1.0.md) ·
[MIRAGE-GRID-SHIFT-1.0.md](MIRAGE-GRID-SHIFT-1.0.md).

## Public stack (locked wording)

MirageGrid’s public stack is now three named pieces:

1. **Anonymity network** — onion/mesh privacy (existing MVP stays a lawful
   privacy tool).
2. **Node Gate** — the MirageGrid admission/claim surface for `.az` names
   (NOT azieleliab.com, NOT godlock.uk, NOT corpus — those hubs are not
   Node Gate).
3. **Auto-heal** — MUST obey REHEAL-1.0 / MESH-REHEAL: heal from own last
   good tip + verified trusted pull, or phoenix-WAIT. NEVER neighbor
   vote-to-fix / majority fanfic. “Auto-heal” in copy means that lawful
   reheal + archive re-expand, not peer talk-back-to-health.

AZ Generator and Node Gate are MirageGrid subsystems / law. They are not
Softwares-tab products. MirageGrid remains the Softwares product.

Suite mesh `/v1/mesh` (QNM-BUILD-1.0) stays default OFF. That strip is
not Node Gate, not auto-heal, and not the anonymity network.

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

**Sockets.** The 1s tip tick and the 777s dwell never share a socket
**with each other or with the 7m77s claim clock**. Three clocks.
Strangers.

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

Public-stack **auto-heal** means this lawful reheal + archive re-expand.
`MESH_AUTO_HEAL` on the suite QNM strip stays false. Phoenix-WAIT is
local wait, not a controller hunt and not neighbor gossip. Neighbor
vote-to-fix labeled as auto-heal is refuse.

## AZ GENERATOR (AZ-GENERATOR-1.0)

Every **7 minutes and 77 seconds** (period **497s**) the generator
attempts to claim a new `.az` domain. Origin node hosts the site +
server. Cap **7** domains per node. First claim is
`www.survivalnetwork.az` when no known site contains that name; if that
cannot be claimed, resume the 7m77s clock under Cap-7.

Constantly plant a flag and repost current known sites. Broken chain →
restore at the most active guaranteed point. Restore needs **at least
49 Aziel Eliab papers** from the node’s data (hash-absolute; cite don’t
merge; bytes↔hash). Fewer than 49 → no false tip; phoenix-WAIT / hold.

NO-LIE / NO-REWRITE: no rewrite key; the network never lies to stay
alive; receipts still hash; copies are not all on one tunnel.

Offline origin: sites stay up for downloads (cold-copy / standby /
MESH-VAULT). Tip plane may show isolated/locked; download plane stays
pull-only.

Full text: [AZ-GENERATOR-1.0.md](AZ-GENERATOR-1.0.md).

## MIRAGE GRID SHIFT (MIRAGE-GRID-SHIFT-1.0)

MESH-VAULT is **snapshot plus official standby** — an **IP-mask host**.
A **grid shift** keeps the `.az` (or standby) name answerable for
downloads while the node itself is cloaked/hidden after a domain pull.
Official-hub Cloudflare tunnels still die with the pull (TUN-WP /
NODE-OPS). Not resurrection of godlock.uk / corpus hostnames.

When lawful auto-heal fires, a cloak burst may plant up to Cap-7 spare
`.az` names with a cloak on top (hide originating node IP behind the
grid / Node Gate plane).

Full text: [MIRAGE-GRID-SHIFT-1.0.md](MIRAGE-GRID-SHIFT-1.0.md).

## Scope restatements

**GodLock** on godlock.uk is a dark stress-test engine for
intelligent-design challenges (one challenge box; Yes/No/Let’s
review/Interesting; hash-chained receipts). It is not a forum, not
Node Gate, not the AZ Generator, not an anonymity network. Softwares on
godlock.uk stay GodLock-first / Runtime-pointer only. GodLock challenge
receipts ≠ ACT-RECEIPT public action receipts.

**AZBot / AZindex** gates hub ingest / first-screen PRs (corpus, ae,
godlock, HDJ, runtime ingest) with AZindex-OK — Growth-ON crawlers,
identity locks, CROSS-NETWORK-SURVIVAL + NO-LIE cites, no visible 15:20
chrome. AZBot does not operate Node Gate, does not claim `.az` domains,
and is not the AZ Generator.

Official hubs (azieleliab.com, azielcorpuslibrary.net, godlock.uk,
hedidntjump.com) remain named public hosts. They are not Node Gate.
azieleliab.com hosts software/runtime but is not login-recovery or
Node Gate (QNM-BUILD).

## Refuse

- Unmarked Cloudflare tunnel hydra on official hubs
- Neighbor vote-to-fix labeled as auto-heal
- Softwares-tab listing for AZ Generator / Node Gate as separate products
- Visible 15:20 identity-lock HTML
- Invented Zenodo DOIs

## Surface

| Surface | What it does |
| --- | --- |
| `miragegrid/mesh.py` | Topology stays live. Law functions refuse illegal planes. |
| Worker `mesh.js` | `/v1/mesh/*` PROXY. Stamps STW/CCS/RH/AZG/MGS. `/v1/mesh/vpn|hop|tunnel` refuse `MESH-STUB`. `/v1/mesh/reheal` is local law (not neighbor heal). `/v1/mesh/az-generator` and `/v1/mesh/grid-shift` cite local law. |
| `POST /v1/assign` | Live session assignment. |

Identity: **Aziel Eliab** only.
