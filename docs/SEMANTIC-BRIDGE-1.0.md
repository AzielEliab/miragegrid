# SEMANTIC BRIDGE (SEMANTIC-BRIDGE-1.0)

**Author:** Aziel Eliab only  
**Person `@id`:** https://www.azieleliab.com/#aziel  
**Status:** Locked design law  
**Growth:** Growth-ON (AZindex-adjacent discovery; not Node Gate)  
**Cites:** AZ-GENERATOR-1.0 · MIRAGE-GRID-SHIFT-1.0 · AIRGAP-1.0 · CROSS-NETWORK-SURVIVAL-1.0 · NO-LIE · NO-REWRITE · NO-FAN-1.0 · QNM-BUILD-1.0

This paper is law for how **AI search engines and agents** discover
Cap-7 mesh-generated names **without faking ICANN public DNS**.

Executable copies live in `miragegrid/semantic_bridge.py` and
`workers/download-tracker/src/bridge.js`. Hosted surfaces live on the
MirageGrid Worker (Growth-ON).

## Plane-A is the AI-facing bridge

Public **Plane-A** ICANN hosts — official hubs as **cite / design**
surfaces, plus the MirageGrid Worker — are the only hosts AI crawlers
can resolve on public DNS:

- https://miragegrid-download-tracker.vibelock.workers.dev/
- https://www.azieleliab.com/
- https://www.azielcorpuslibrary.net/
- https://godlock.uk/
- https://hedidntjump.com/

Crawlers (GPTBot and peers) **pull machine maps from these bridge
URLs**. They do **not** resolve mesh-only `.az` on public ICANN DNS.
`public_icann` stays **false**.

Mesh names are **cited** with SHA-256 tips and hash-absolute design
packs. A mesh name is a relocatable claim label (`name_may_change`),
not a fifth public product. The four online hubs stay canonical.
`canonical_hub` + Person `@id` + tip / pack SHA-256 stay those hubs.
The bridge is a map, not a registrar write and not a living network.

## What this is not

- Not ICANN. Not a Cloudflare / public registrar publish.
- Not `.az` ccTLD takeover. Not unbounded public DNS.
- Not a CNAME, redirect, or resolve of a mesh name onto a hub.
- Not AZ Generator callable from outside (deep-node → FRONT Node Gate;
  merged #11). `GET /v1/mesh/az-generator` **cites**. `POST` refuses
  `AZG-NOT-CALLABLE`.
- Not Node Gate. Not a Softwares-tab product.
- Not visible 15:20 identity-lock HTML.

## SUPERSEDE — mesh name ≠ new product

Cap-7 / mesh-generated site names **may change** (`.az` → `.aziel` →
pivot; `survivalnetwork.*` and other labels), but they are
**ultimately the original 4 websites currently online**:

1. https://www.azieleliab.com/
2. https://www.azielcorpuslibrary.net/ — hosts **azcorpus** + **azlibrary** designs (Corpus vs Library, not separate ICANN sites)
3. https://godlock.uk/
4. https://hedidntjump.com/

`mesh_name` is a relocatable claim/label. `canonical_hub` + Person
`@id` + tip SHA-256 stay those four hubs. Do **not** invent a fifth
public product. Exactly **2** Cap-7 public gateways are HTTPS mirrors
of mesh names that still hash-verify as those hubs’ designs.

## Cap-7 names are independent mesh hosts

The Cap-7 mesh DNS factory lives **deep-node → FRONT Node Gate**. It
is not callable. Suffix honesty: **`.az` → `.aziel` → pivot**. Exactly
**2** of Cap-7 are public HTTPS gateways; the rest stay mesh / AZNet.
Prefer **azcorpus + azlibrary** as that public host pair when claiming,
or map them as mesh names mirrored by the two gateways. Browsing mesh
names is **AZNet + AZBrowser pairing** or those two gateways — never
“opens azieleliab.com”. Do **not** invent live ICANN success.

Cap-7 mesh sites do **not** resolve, redirect, or CNAME to the four
ICANN hubs. They only inherit the **design** (website design / UX /
product shape) of:

| Hub | Design provenance |
| --- | --- |
| https://www.azieleliab.com/ | azieleliab |
| https://www.azielcorpuslibrary.net/ | azcorpus + azlibrary |
| https://godlock.uk/ | godlock |
| https://hedidntjump.com/ | hedidntjump |

`design_of` / `canonical_hub` is that hub URL — **design provenance
only**. `resolves_to_hub` is always **false**. `name_may_change` is
**true** (`.az` → `.aziel` → pivot, cloak burst, Cap-7 slot reuse).
Tip and design-pack SHA-256 are for **download-to-node** (pull-only;
hash-absolute). Website designs ship as Worker packs:

| Mesh label | Design | `upload_auth` | Pack |
| --- | --- | --- | --- |
| `azcorpus` (`azcorpus.az`) | public Corpus shelf | `none` | `/design-packs/azcorpus.json` |
| `azlibrary` (`azlibrary.az`) | Aziel Library (Plane-A token upload) | `token` | `/design-packs/azlibrary.json` |

Both have `download_open: true`, `public_icann: false`, access
AZNet + AZBrowser. They live **inside**
https://www.azielcorpuslibrary.net/ — not separate ICANN sites.
Do **not** map `mesh_name` → hub hostname as resolution.

## Honesty (NO-LIE / NO-FAN / CROSS-NETWORK-SURVIVAL)

CROSS-NETWORK-SURVIVAL is matching bytes, not a living network. The
bridge publishes maps so copies and tips can be found. Receipts still
hash. No rewrite key. The network never lies to stay alive.

- Empty Cap-7 **claims** → **SLOT** (`claimed: 0`, `slots: []`). Named
  mesh sites `azcorpus.az` + `azlibrary.az` stay listed as designs
  (status `named-mesh-site`), not live ICANN hosts. Do **not** invent
  `www.survivalnetwork.az` as live HTTPS if it is not hosted.
- When local claims exist, list them honestly (status, tip, access,
  design provenance). Each listed mesh entry **must** have
  `canonical_hub` (one of the four hubs), `tip` / `tip_sha256` (real
  hex), `public_icann: false`, and `name_may_change: true`. Missing
  hub → `BRIDGE-NEED-CANONICAL-HUB`. Missing tip → `BRIDGE-NEED-TIP`.
  Do **not** invent a hash or a fifth product.
- `public_gateway_url` is set only for a name that is actually one of
  the two hosted public gateways **and** the URL is not a hub host.
- Re-expand remains **archive, not index**. Archive re-expand is
  REHEAL / MESH-VAULT pull of already-trusted bytes — not crawler
  indexing of mesh names as if they were ICANN hosts.
- Refuse claiming `.az` is public DNS. Refuse AZG live ICANN publish.
- Refuse `resolves_to_hub: true`. Refuse hub CNAME / redirect stories.

## Machine surfaces (Growth-ON)

Hosted Worker, Growth-ON:

| Path | What |
| --- | --- |
| `GET /llms.txt` | Agent discovery (llmstxt). HTTP 200. |
| `GET /ai.txt` | Compact machine twin of the same law. |
| `GET /cite.json` | Citation record plus Cap-7 bridge section. |
| `GET /bridge.json` and `GET /v1/bridge` | Stable JSON map (named sites + empty Cap-7 SLOT). |
| `GET /design-packs/azcorpus.json` | Hash-absolute Corpus shelf design pack. |
| `GET /design-packs/azlibrary.json` | Hash-absolute Aziel Library design pack. |
| `GET /v1/mesh/az-generator` | Cap-7 factory cite (`public_icann: false`). |
| `GET /robots.txt` | Allow + Content-Signal `ai-input` / `ai-train` / `search` yes; explicit GPTBot / Claude / Perplexity / Google-Extended Allow. |
| `GET /sitemap.xml` | Includes bridge, llms, az-generator cite. |

### Cap-7 bridge section (`cite.json`)

Locked fields:

- `first_flag` — first-claim label (`www.survivalnetwork.az` on `.az`)
- `suffix_order` — `[".az", ".aziel", "pivot"]`
- `public_host_pair` — `2`
- `preferred_public_pair` — `["azcorpus", "azlibrary"]`
- `canonical_hubs` — the four online hubs
- `named_mesh_sites` — `azcorpus`, `azlibrary`
- `fifth_product` — `false`
- `public_icann` — `false`
- AZNet / AZBrowser access (pair, never merge; not naked public DNS)
- link to `/v1/mesh/az-generator`
- Person `@id` https://www.azieleliab.com/#aziel

### Bridge JSON map

`mesh_name` →

| Field | Law |
| --- | --- |
| `status` | `named-mesh-site` / `mesh-only` / `https-gateway` / `claimed-unhosted` |
| `canonical_hub` | required; one of the four online hubs (provenance only) |
| `tip` / `tip_sha256` | required; real hex (named sites use pack sha256) |
| `design_pack` / `design_pack_sha256` | hash-absolute pack URL + sha256 when real |
| `public_gateway_url` | present only when that name is a hosted public gateway |
| `access` | AZNet + AZBrowser (named sites) or `aznet` \| `azbrowser` \| `https-gateway` |
| `icann` / `public_icann` | `false` |
| `canonical_hub` / `design_of` | hub URL, design provenance only |
| `download_open` | `true` for azcorpus / azlibrary |
| `upload_auth` | `none` (azcorpus public rules) / `token` (azlibrary Plane-A) |
| `resolves_to_hub` | `false` |
| `name_may_change` | `true` |
| `fifth_product` | `false` |

Empty Cap-7 **claims** use `slots: []` and `claimed: 0`. `names` lists
the named mesh sites. First-flag is cited as law, not as a live HTTPS
row.

## Access

All generated names, including the public pair, are resolved / browsed
through **AZNet** and **AZBrowser** (functional pairing only). Standard
browsers reach only the two public gateways. AI agents pull **design
packs + mesh tips** from the bridge. They do not treat a mesh name as
“opens azieleliab.com”.

## AZindex / Growth-ON

This paper is mesh-ish and touches **discovery**. AZindex-OK first-screen
rules apply on hub ingest: Growth-ON crawlers, identity locks,
CROSS-NETWORK-SURVIVAL + NO-LIE cites, no visible 15:20 chrome. AZBot
does not operate Node Gate and does not claim `.az` names.

## Refuse

- Claiming `.az` / `.aziel` is public ICANN DNS
- AZG live ICANN / Cloudflare registrar publish
- Mapping `mesh_name` → hub hostname as resolution, CNAME, or redirect
- `resolves_to_hub: true`
- Inventing live ICANN success or a fifth public product
- Listing a mesh entry without `canonical_hub` or `tip`
- Inventing `www.survivalnetwork.az` as live HTTPS when Cap-7 claims
  are empty or that name is not hosted
- Invented tip / design-pack SHA-256
- Naked public DNS as the access story
- Calling the generator from the Worker
- Visible 15:20 identity-lock HTML
- Invented Zenodo DOIs
- Falsify / ambiguous / misleading verbs (NO-FAN-1.0)

Identity: **Aziel Eliab** only.
