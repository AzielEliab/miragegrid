# MIRAGE GRID SHIFT (MIRAGE-GRID-SHIFT-1.0)

**Author:** Aziel Eliab only  
**Status:** Locked design law  
**Softwares-tab:** no — Node Gate, cloak burst, and grid shift are MirageGrid
subsystems / law, not separate products  
**Cites:** AZ-GENERATOR-1.0 · AIRGAP-1.0 · SPLIT THE WIRES (STW-1.0) ·
COLD-COPY SURVIVAL (CCS-1.0) · REHEAL (RH-1.0) / REHEAL-1.0 / MESH-REHEAL ·
TUN-WP · NODE-OPS · MESH-VAULT · NO-LIE · NO-REWRITE · NO-FALSIFY ·
NO-AMBIGUITY · NO-MISLEAD (NO-FAN-1.0)

This paper locks Cap-7, cloak burst, grid shift, Node Gate, and the
public-stack wording for **auto-heal**. It does not invent a
Softwares-tab product beyond MirageGrid.

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

Suite mesh `/v1/mesh` (QNM-BUILD-1.0) stays default OFF. That strip is
**not** Node Gate, **not** auto-heal, and **not** the anonymity network.
`MESH_NODE_GATE` and `MESH_AUTO_HEAL` stay false on the suite rollup.
Product-plane Node Gate and lawful auto-heal live inside MirageGrid, not
on official hubs and not on the QNM Live Nodes strip.

## Node Gate

Node Gate is the MirageGrid admission/claim surface for **`.az` names**.

It is **not**:

- azieleliab.com
- godlock.uk
- azielcorpuslibrary.net / corpus
- hedidntjump.com
- the suite QNM `/v1/mesh` rollup
- GodLock
- AZBot / AZindex
- a Softwares-tab product

azieleliab.com hosts software/runtime but is **not** login-recovery or
Node Gate (QNM-BUILD).

## MESH-VAULT restated

MESH-VAULT is **snapshot plus official standby** — an **IP-mask host**.

The operator-facing name for the move when a public domain is pulled is
a **grid shift**: the `.az` (or standby) name stays answerable for
downloads while the **node itself is cloaked/hidden** after the domain
pull.

Public Cloudflare tunnels on official hubs still **die with the pull**
(TUN-WP / NODE-OPS) — MirageGrid grid-shift is product-plane survival
for MirageGrid-hosted `.az` sites, not resurrection of godlock.uk /
corpus hostnames.

Unmarked Cloudflare tunnel hydra on official hubs is refuse.

## Cap-7 + cloak burst

Cap **7** spare/claimed `.az` names per covered node.

When auto-heal fires (lawful REHEAL-1.0 / MESH-REHEAL only), the same
burst may plant up to Cap-7 spare names **with a cloak on top** (hide
originating node IP behind the grid / Node Gate plane).

Use MirageGrid + AZ Generator on a clock of **7 minutes + 77 seconds**
(7m77s = **497s**) for each domain to be claimed, duplicated, and
hosted. See [AZ-GENERATOR-1.0](AZ-GENERATOR-1.0.md).

An eighth name is refuse. Cloak is not a rewrite key. Cloak does not
lie about the tip.

## No falsification. No ambiguity. No misleading.

First-class refuse law beside NO-LIE / NO-REWRITE (NO-FAN-1.0). Locked
wording: **No falsification. No ambiguity. No misleading.**

- No falsified tip, receipt, domain claim, Live Nodes count, or
  “site up” claim.
- No ambiguous tip / dual tip / soft maybe — ambiguous tip = isolate
  (already STW-1.0). Do not paper over with majority or pretty copy.
- No misleading chrome: cloak/grid-shift must not pretend a pulled
  official hub hostname is still the cell; `.az` names are named
  MirageGrid hosts, not unmarked hydra; auto-heal must not be worded
  as neighbor resurrection.
- Pair with NO-LIE: the network never lies to stay alive; no rewrite
  key; receipts still hash.

## Auto-heal wording (locked)

| Phrase | Means |
| --- | --- |
| Auto-heal (public stack) | Lawful reheal + archive re-expand: own last good tip + verified trusted pull, or phoenix-WAIT |
| MESH-REHEAL / REHEAL-1.0 / RH-1.0 | Same law. Neighbor cannot talk a node dirty-back-to-health |
| Suite `MESH_AUTO_HEAL` | Stays **false**. The QNM strip never vote-heals a visiting floor |
| Neighbor vote-to-fix labeled “auto-heal” | **Refuse** |

Allowed reheal fields remain `live`, `locked`, `isolated`, `tip-hash`.
Forbidden: bodies, diffs, vote-to-fix, majority fanfic.

Grid-shift **standby** is a vault-multiply event: the standby node
**obtains a cold vault copy** of the Aziel paper set (pull-only payload
plane, or vault-on-transfer). Papers land as cold copies. No paper
bytes on the 1s tip tick.

## Split the wires (three strangers)

The 1s tip tick and the 777s dwell never share a socket **with** the
7m77s claim clock. Three clocks. Strangers. Payload/download stays
pull-only.

## Offline / download plane

If the origin node disconnects or goes offline, **sites stay up for
downloads** (cold-copy / standby / MESH-VAULT snapshot+standby). Tip
plane may show isolated/locked; download plane stays pull-only.
Airgap still allows downloads / serve from the local cold shelf.

## AIRGAP (AIRGAP-1.0)

Airgap = local vault + no bearer radios + no climb-back onto pulled
public hub hostnames. Official hubs (ae / corpus / godlock / HDJ) are
**not** airgap Node Gate. Tip chatter when airgapped: live / locked /
isolated / tip-hash only if any; no body gossip. Re-expand / reheal
still: own tip + trusted pull of bytes already trusted, or
phoenix-WAIT — never neighbor majority.

Full text: [AIRGAP-1.0.md](AIRGAP-1.0.md).

## Hub sites vs MirageGrid

Official hubs (azieleliab.com, azielcorpuslibrary.net, godlock.uk,
hedidntjump.com) remain named public hosts. They are **not** Node Gate.

## GodLock scope (not MirageGrid)

GodLock on godlock.uk is a **dark stress-test engine** for
intelligent-design challenges (one challenge box; Yes/No/Let’s
review/Interesting; hash-chained receipts). It is **not** a forum,
**not** Node Gate, **not** the AZ Generator, **not** an anonymity
network. Softwares on godlock.uk stay GodLock-first / Runtime-pointer
only. GodLock challenge receipts ≠ ACT-RECEIPT public action receipts.

## AZBot / AZindex scope (not MirageGrid)

AZBot gates **hub ingest / first-screen** PRs (corpus, ae, godlock,
HDJ, runtime ingest) with AZindex-OK — Growth-ON crawlers, identity
locks, CROSS-NETWORK-SURVIVAL + NO-LIE cites, no visible 15:20 chrome.
AZBot does **not** operate Node Gate, does not claim `.az` domains, and
is not the AZ Generator.

## Refuse

- Unmarked Cloudflare tunnel hydra on official hubs
- Neighbor vote-to-fix labeled as auto-heal
- Softwares-tab listing for AZ Generator / Node Gate as separate products
- Visible 15:20 identity-lock HTML
- Invented Zenodo DOIs
- Resurrection of godlock.uk / corpus hostnames via grid shift
- Pretending a pulled official hub hostname is still the cell
- Auto-heal worded as neighbor resurrection
- Falsify / ambiguous / misleading verbs (NO-FAN-1.0)
- Merging GodLock, AZBot, or official hubs into Node Gate
- Official hubs as airgap Node Gate
- Bearer radios / climb-back / body gossip while airgapped
- Paper-body fan-out on the 1s tip tick

Identity: **Aziel Eliab** only.
