# AZ GENERATOR (AZ-GENERATOR-1.0)

**Author:** Aziel Eliab only  
**Status:** Locked design law  
**Softwares-tab:** no — AZ Generator is a MirageGrid subsystem / law, not a separate product  
**Cites:** SPLIT THE WIRES (STW-1.0) · COLD-COPY SURVIVAL (CCS-1.0) · REHEAL (RH-1.0) / REHEAL-1.0 / MESH-REHEAL · MIRAGE-GRID-SHIFT-1.0 · AIRGAP-1.0 · NO-LIE · NO-REWRITE · NO-FALSIFY · NO-AMBIGUITY · NO-MISLEAD (NO-FAN-1.0)

This paper is law for the next MirageGrid generation. It does not invent a
Softwares-tab product. MirageGrid remains the Softwares product. Node Gate
and AZ Generator stay inside MirageGrid.

**AZ Generator is a Cap-7 mesh DNS factory.** It lives **deep in the
node**. It does **not** get called from outside (no POST `/call-generator`,
no Worker-invoked back door, no hosted cron into the node). Flow:

    deep node → 7m77s (497s) claim tick → FRONT Node Gate
    (claim / plant / flag / restore)

Hosted `/v1/assign` stays live. Hosted mesh / vpn-hop / tunnel stubs remain
refuse. Hosted `GET /v1/mesh/az-generator` **cites** this law. `POST`
`/v1/mesh/az-generator` **refuses** (`AZG-NOT-CALLABLE`). Executable copies
live in `miragegrid/mesh.py`, `miragegrid/az_generator.py`, and
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
clock. It is not GodLock, not AZBot, and not a hub. It is not a
Softwares-tab product. AZNet and AZBrowser are **separate** Softwares
products; they pair for access only and are never merged into the
generator.

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

Domain claimed → authored into a **mesh-authoritative** zone hosted by
the **origin node**. Cap: **7 names per node**. This is **not** a public
ICANN registrar write and **not** takeover of the public `.az` ccTLD.

## Three clocks, strangers

Tip/presence plane ≠ payload/download plane. The **1s** tip tick, the
**777s** dwell, and the **7m77s** claim clock never share a socket.
Three clocks. Strangers. STW-1.0 is not rewritten; the claim clock is
the third stranger.

## Cap-7 mesh DNS factory

At most **7** spare/claimed names per covered node. An eighth claim is
refuse. Not “7 doors × 7 domains.” Cloak burst (see
MIRAGE-GRID-SHIFT-1.0) may plant up to the same Cap-7 with a cloak on
top; it cannot exceed Cap-7.

The factory authors zone records + claim receipts + tip/hash
continuity. Mesh tip remains authoritative. Hosted Worker stamps are
cite-only.

### Honest suffix order (never fake ICANN)

1. Prefer **`.az`**.
2. If `.az` cannot be honestly claimed/resolved → **`.aziel`**.
3. If neither is honest → **pivot** to a mesh-authoritative suffix the
   node can actually register in its Cap-7 zone. Stamp the active
   suffix. Do **not** pretend `.az` or `.aziel` succeeded.

### Exactly 2 public browser hosts

Of the Cap-7 set, **exactly 2** names become hosted public HTTPS
gateways/mirrors reachable by a standard internet browser. Those two
are **mirrors of mesh names** — not ICANN registrations. The other
Cap-7 slots stay mesh/AZNet-side.

### Access (AZNet + AZBrowser)

All generated names, including the public pair, are resolved/browsed
through **AZNet** and **AZBrowser** (functional pairing only). This is
not a naked public DNS story. Standard browsers reach only the public
pair. Do not merge AZNet, AZBrowser, and MirageGrid into one product.

## Flag / repost / restore

The generator constantly **plants a flag** and **reposts current known
sites** using node data.

If a chain is broken, restore at its **most active guaranteed point**.

Restore requires **at least 49 Aziel Eliab papers** established from
the node’s **local vault** (hash-absolute; cite don’t merge; bytes↔hash).
Fewer than 49, or a node that lacks the full verified set → do not
claim a false tip; **AZG-UNVERIFIED-TIP / incomplete vault**;
phoenix-WAIT / hold. Do not invent.

Obey **NO-LIE / NO-REWRITE**: no rewrite key; the network never lies to
stay alive; receipts still hash; copies are not all on one tunnel.

Obey **NO-FALSIFY / NO-AMBIGUITY / NO-MISLEAD** (NO-FAN-1.0), first-class
beside NO-LIE / NO-REWRITE: **No falsification. No ambiguity. No
misleading.** If fewer than 49 papers or the tip is unverified, **refuse
the claim** rather than invent continuity. Do not claim a false tip. Do
not fake the flag.

## First claim

The first-flag name follows the **ACTIVE** honest suffix:

- active `.az` → `www.survivalnetwork.az`
- active `.aziel` → `www.survivalnetwork.aziel`
- pivoted → `www.survivalnetwork.<active-honest-suffix>`

If that name cannot be claimed, resume the 7m77s clock under Cap-7.
**Do not fake the flag on a dead suffix.**

## AIRGAP-1.0 (local vault)

The paper vault is air-gapped from the 1s tip plane. Paper bodies never
ride a tip tick. Vault multiply is allowed only on bootstrap, join,
Cap-7 claim, and grid-shift standby. Restore / claim requires **≥49**
hash-absolute Aziel Eliab papers from the **LOCAL** vault. Incomplete
vault → `AZG-INCOMPLETE-VAULT` / phoenix-WAIT.

## No falsification. No ambiguity. No misleading.

First-class refuse law beside NO-LIE / NO-REWRITE (NO-FAN-1.0).

- No falsified tip, receipt, domain claim, Live Nodes count, or
  “site up” claim.
- No ambiguous tip / dual tip / soft maybe — ambiguous tip = isolate
  (STW-1.0). Do not paper over with majority or pretty copy.
- No misleading chrome: do not invent continuity to stay alive.
- `<49` papers, incomplete vault, or unverified tip → refuse claim;
  AZG-UNVERIFIED-TIP / incomplete vault; phoenix-WAIT / hold.
- No “we have 49” without bytes (NO-FAN).
- `www.survivalnetwork.az` cannot be claimed → resume normal; do not
  fake the flag.
- Pair with NO-LIE: the network never lies to stay alive; no rewrite
  key; receipts still hash.

## Paper vault on every node

Every MirageGrid / AZ Generator node **MUST** carry the **full set of
Aziel Eliab papers** in its local vault (enough for the ≥49 restore
rule and for offline / airgap operation).

This is reconciled with SPLIT THE WIRES + COLD-COPY:

- The tip plane stays presence + tip-hash only. **No live body sync /
  sender fan-out of paper bytes on the 1s tick.**
- “Pushed to each node” means: on node **bootstrap / join / Cap-7
  claim / grid-shift standby**, the node **obtains a cold vault copy**
  of the Aziel paper set (pull-only payload plane, or vault-on-transfer
  multiply). Locked wording: **vault multiply onto each node** /
  **papers land on every node as cold copies.**
- Hash-absolute: each paper verifies by published tip/hash. Cite,
  don’t merge. NO-FAN: no falsified paper set, no “we have 49”
  without bytes.
- If a node lacks the full verified set, AZ Generator restore / claim
  that needs ≥49 papers **refuses** (AZG-UNVERIFIED-TIP / incomplete
  vault) — phoenix-WAIT, do not invent.

See [AIRGAP-1.0](AIRGAP-1.0.md) for airgapped operation of that vault.

## Offline node

If the origin node disconnects or goes offline, **sites stay up for
downloads** (cold-copy / standby / MESH-VAULT snapshot+standby). The
tip plane may show isolated/locked; the download plane stays pull-only.
Airgap still allows serve from the local cold shelf.

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
- Incomplete vault / “we have 49” without bytes
- Live body sync of paper bytes on the 1s tip tick
- Unverified tip used to invent continuity
- Faking the flag when `www.survivalnetwork.az` cannot be claimed
- Falsify / ambiguous / misleading verbs (NO-FAN-1.0)
- Sharing the 7m77s claim socket with the 1s tip tick or the 777s dwell
- Calling the generator from outside / Worker POST run-generator
- Faking ICANN / Cloudflare registrar success or `.az` ccTLD takeover
- Hosting more or fewer than exactly 2 public browser gateways of Cap-7
- Merging AZNet / AZBrowser / generator into one product
- Naked public DNS as the access story
- Claiming `.com` / `.net` / other ICANN TLDs
- Pretending `.az` or `.aziel` succeeded after an honest pivot
- Invented radio PHY / turning MirageGrid into a qnm RF/BT/Wi-Fi/photon mesh (local qnm radios are not this product; hub `GET /v1/mesh` never enables)
- Visible 15:20 identity-lock HTML
- Invented Zenodo DOIs
- Merging papers instead of citing them
- Rewrite keys / lying to stay alive

Identity: **Aziel Eliab** only.
