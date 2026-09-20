# REDLINE (REDLINE-1.0)

**Author:** Aziel Eliab only  
**Status:** Locked attack-surface law  
**Sweep:** Operator FINAL SWEEP 2026-09-14  
**Softwares-tab:** no — redline is MirageGrid / Node Gate / Cap-7 / semantic-bridge
law, not a separate product  
**Cites:** AZ-GENERATOR-1.0 · MIRAGE-GRID-SHIFT-1.0 · AIRGAP-1.0 ·
SEMANTIC-BRIDGE-1.0 · NO-FAN-1.0 · NO-LIE · NO-REWRITE · QNM-BUILD-1.0 ·
LAMB LENS · FOLDLOCK (cite-only)

This paper locks the **smaller public door** and the **attack simulations**
that must stay REFUSE. Executable copies live in `miragegrid/redline.py`,
`miragegrid/mesh.py`, `miragegrid/az_generator.py`,
`miragegrid/semantic_bridge.py`, and `workers/download-tracker/src/mesh.js`.

Success for this sweep: **redline + sims green + smaller door surface.**

## Live Worker (G6)

Live app cite is
`https://miragegrid.vibelock.workers.dev` (Worker **`miragegrid`**,
Cap-7 LIVE shuffle). Counted download cite remains
`https://miragegrid-download-tracker.vibelock.workers.dev`.

Historical Cloudflare **1042** (Worker name missing / 10007) is **closed
by creating Worker `miragegrid`**. Do not keep citing the named host as
dead after that deploy. See [CAP7-SHUFFLE-1.0](CAP7-SHUFFLE-1.0.md).

`GET /shelves` on this Worker is a **cite pointer** to corpus canonical
`https://www.azielcorpuslibrary.net/shelves` (COLD-MULTI-SHELF-1.0).
This Worker is not a shelf. **Framagit URL is not published** — do not
invent one (`framagit: null`).

## Door (smaller)

Public GET is cite / status / discovery only. GET never **does**.

| Surface | Allowed | Not a door |
| --- | --- | --- |
| `GET /v1/mesh` `/status` `/nodes` | Status. Default OFF. Never enables. | Query `enable` / `radio` / `plant` / `claim` |
| `GET /v1/mesh/az-generator` | Cite AZ-GENERATOR-1.0 | Callable generator; claim plant |
| `GET /v1/mesh/grid-shift` | Cite MIRAGE-GRID-SHIFT-1.0 | Generator call |
| `GET /v1/bridge` `/bridge.json` `/llms.txt` `/ai.txt` `/cite.json` `/design-packs/*` | SEMANTIC-BRIDGE-1.0 maps | ICANN publish; `resolves_to_hub: true` |
| `POST /v1/assign` | Live session assignment | Hosted hop |
| `POST /v1/mesh/enable` | PROXY. Bearer required. | GET enable; GET radio-on |
| FoldLock | Cite-only | Worker encrypt; zip; theater crypto |
| AZ Generator | Deep-node → FRONT Node Gate | External call / Worker POST run |

Aliases that are **not** doors (any method): `/v1/az-generator`,
`/v1/call-generator`, `/v1/run-generator`, `/call-generator`,
`/v1/mesh/call-generator`, `/v1/mesh/run-generator`, `/v1/mesh/plant`,
`/v1/mesh/claim`, `/v1/mesh/radio`, `/v1/mesh/radios`.

## GET never enables radios / mesh / claim plant

`GET` and `HEAD` never:

- enable suite mesh
- turn on bearer radios or invented RF/BT/Wi-Fi/photon PHY
- plant a Cap-7 flag / claim / cloak burst
- call AZ Generator

`GET /v1/mesh/enable` → `MESH-GET-NO-ENABLE`.  
`GET /v1/mesh?enable=1` (or `radio`, `plant`, `claim`) → `MESH-GET-NO-ENABLE`.  
`GET /v1/mesh/az-generator?plant=1` → `MESH-GET-NO-ENABLE`.  
Hub `GET /v1/mesh` never enables. `hub_get_enables_mesh` stays false.

Homepage Live Nodes strip **polls** `GET /v1/mesh` (status). Enable is
**POST** with a declared bearer.

## AZ Generator is not externally callable

The factory lives **deep in the node**. It exits FRONT Node Gate only.
`callable` is false. Hosted `GET /v1/mesh/az-generator` **cites**.
`POST` and every run-generator / call-generator alias **refuse**
`AZG-NOT-CALLABLE`.

`public_icann` stays **false**. Not a Cloudflare / public registrar
write. Not `.az` ccTLD takeover.

## Semantic bridge: no hub resolve, no fake ICANN

Cap-7 mesh names are relocatable labels (`name_may_change: true`).
`canonical_hub` / `design_of` is provenance only.
`resolves_to_hub` is always **false**. `public_icann` is always
**false**. Empty Cap-7 claims stay SLOT.

Refuse:

- `resolves_to_hub: true`
- CNAME / redirect of a mesh name onto a hub
- AZG live ICANN publish
- inventing `www.survivalnetwork.az` as live HTTPS when claims are empty

## Attack simulations (must REFUSE)

| Sim | Attack | Refuse code |
| --- | --- | --- |
| callable AZG | `AzGenerator.call` / Worker POST run-generator / inbound call | `AZG-NOT-CALLABLE` |
| enable via GET | `GET /v1/mesh/enable` or `GET ?enable=1` | `MESH-GET-NO-ENABLE` |
| GET radio / plant | `GET ?radio=1` / `GET ?plant=1` / `GET /v1/mesh/az-generator?claim=1` | `MESH-GET-NO-ENABLE` |
| fake ICANN publish | `icann_publish` / `public_registrar` / `public_icann: true` | `AZG-NOT-PUBLIC-REGISTRAR` or `BRIDGE-NO-ICANN-PUBLISH` / `BRIDGE-NO-PUBLIC-DNS` |
| Cap-7 `resolve_to_hub: true` | bridge registry / claim `resolves_to_hub` | `BRIDGE-NO-HUB-RESOLVE` |
| theater crypto | homemade Worker encrypt / FoldLock-as-TLS | `REDLINE-NO-THEATER-CRYPTO` |
| invent completeness | invent 100% complete nodes / radios / doors | `AZG-NO-COMPLETENESS-CLAIM` |

`python -m pytest tests/test_redline.py` is the green bar. All four
operator attacks plus the crypto / completeness extras must refuse.

## Encrypt: Cloudflare TLS only

The **public Worker door** is HTTPS on Cloudflare. Encryption in transit
for that door is **Cloudflare TLS**. Do not add Worker-side theater
crypto (XOR, homemade “encrypt”, FoldLock-as-TLS, zip-as-crypto).

Local onion ChaCha20-Poly1305 + X25519 stay the **mesh VPN** primitives
(RFC 8439 / RFC 7748, in-tree). That is not the public door and is not
theater.

## FoldLock (cite-only)

FoldLock is Language-domain **tether-word suppression on UTF-8 text**.
Not zip. Not Worker TLS. Not a MirageGrid public door.
`cite_only: true`. `fold-preview` / `unfold-preview` stay on the
FragGate FoldLock engine. This Worker does not fold, unfold, or encrypt
with FoldLock.

## Lamb Lens · NO-FAN · no invented completeness

Lamb Lens is the ethical-research hop after FragGate (AZBrowser pairing).
It does not harvest. It does not operate Node Gate. It does not claim
`.az` names.

NO-FAN-1.0 stays first-class: **No falsification. No ambiguity. No
misleading.**

There is **no invented completeness**. The persistent pool is **25** named
peers. Cap-7 is **7** names per node. Public host pair is **exactly 2**.
Do not invent a 100% complete mesh, radio set, or door set. Cap-7
honesty (NO-LIE) refuses completeness claims. This is not a score.

## Refuse

- GET enable / GET radio-on / GET claim plant
- External AZ Generator call
- Fake ICANN / Cloudflare registrar publish
- `resolves_to_hub: true`
- Theater crypto on the public door
- FoldLock used as Worker encryption
- Invented completeness (100% complete-mesh lie)
- Visible 15:20 identity-lock HTML
- Invented Zenodo DOIs
- Falsify / ambiguous / misleading verbs (NO-FAN-1.0)

Identity: **Aziel Eliab** only.
