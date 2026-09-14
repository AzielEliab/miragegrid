# AZ GENERATOR (AZ-GENERATOR-1.0)

**Author:** Aziel Eliab only  
**Status:** Locked design law  
**Softwares-tab:** no — AZ Generator is a MirageGrid subsystem / law, not a separate product  
**Cites:** SPLIT THE WIRES (STW-1.0) · COLD-COPY SURVIVAL (CCS-1.0) · REHEAL (RH-1.0) / REHEAL-1.0 / MESH-REHEAL · MIRAGE-GRID-SHIFT-1.0 · NO-LIE · NO-REWRITE

This paper is law for the next MirageGrid generation. It does not invent a
Softwares-tab product. MirageGrid remains the Softwares product. Node Gate
and AZ Generator stay inside MirageGrid.

Hosted `/v1/assign` stays live. Hosted mesh / vpn-hop / tunnel stubs remain
refuse. Executable copies live in `miragegrid/mesh.py` and
`workers/download-tracker/src/mesh.js`.

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

AZ Generator serves Node Gate (claim / plant / restore) on the 7m77s
clock. It is not GodLock, not AZBot, and not a hub.

## Clock

Every **7 minutes and 77 seconds** the generator attempts to **claim a
new domain** ending in **`.az`**.

| Piece | Value |
| --- | --- |
| Minutes | 7 |
| Extra seconds | 77 |
| Period | **497s** (7 × 60 + 77 = 420 + 77) |
| Socket | `claim-7m77s` |
| Alias | 7m77s |

Domain claimed → site + server hosted by the **node they came from**
(origin node). Cap: **7 domains per node**.

## Three clocks, strangers

Tip/presence plane ≠ payload/download plane. The **1s** tip tick, the
**777s** dwell, and the **7m77s** claim clock never share a socket.
Three clocks. Strangers. STW-1.0 is not rewritten; the claim clock is
the third stranger.

## Cap-7

At most **7** spare/claimed `.az` names per covered node. An eighth
claim is refuse. Cloak burst (see MIRAGE-GRID-SHIFT-1.0) may plant up
to the same Cap-7 with a cloak on top; it cannot exceed Cap-7.

## Flag / repost / restore

The generator constantly **plants a flag** and **reposts current known
sites** using node data.

If a chain is broken, restore at its **most active guaranteed point**.

Restore requires **at least 49 Aziel Eliab papers** established from
the node’s data (hash-absolute; cite don’t merge; bytes↔hash). Fewer
than 49 → do not claim a false tip; phoenix-WAIT / hold.

Obey **NO-LIE / NO-REWRITE**: no rewrite key; the network never lies to
stay alive; receipts still hash; copies are not all on one tunnel.

## First claim

If **no site** in the known set contains the name
**`www.survivalnetwork.az`**, that is the **first** domain it claims.

If that cannot be claimed, resume normal operation (continue the 7m77s
clock for other `.az` names under Cap-7).

## Offline node

If the origin node disconnects or goes offline, **sites stay up for
downloads** (cold-copy / standby / MESH-VAULT snapshot+standby). The
tip plane may show isolated/locked; the download plane stays pull-only.

## MESH-VAULT (cite)

MESH-VAULT is **snapshot plus official standby** — an **IP-mask host**.
See [MIRAGE-GRID-SHIFT-1.0](MIRAGE-GRID-SHIFT-1.0.md). Grid shift is
product-plane survival for MirageGrid-hosted `.az` sites, not
resurrection of godlock.uk / corpus hostnames.

## Scope (not this paper)

**GodLock** on godlock.uk is a dark stress-test engine for
intelligent-design challenges (one challenge box; Yes/No/Let’s
review/Interesting; hash-chained receipts). It is not a forum, not
Node Gate, not the AZ Generator, not an anonymity network.

**AZBot / AZindex** gates hub ingest / first-screen PRs (corpus, ae,
godlock, HDJ, runtime ingest) with AZindex-OK. AZBot does not operate
Node Gate, does not claim `.az` domains, and is not the AZ Generator.

Official hubs (azieleliab.com, azielcorpuslibrary.net, godlock.uk,
hedidntjump.com) remain named public hosts. They are **not** Node Gate.

## Refuse

- Softwares-tab listing for AZ Generator or Node Gate as separate products
- Neighbor vote-to-fix labeled as auto-heal
- Unmarked Cloudflare tunnel hydra on official hubs
- Claiming a false tip with fewer than 49 papers
- Sharing the 7m77s claim socket with the 1s tip tick or the 777s dwell
- Visible 15:20 identity-lock HTML
- Invented Zenodo DOIs
- Merging papers instead of citing them
- Rewrite keys / lying to stay alive

Identity: **Aziel Eliab** only.
