# CAP-7 LIVE SHUFFLE (CAP7-SHUFFLE-1.0)

**Author:** Aziel Eliab only  
**Status:** Locked design law  
**Softwares-tab:** no — Cap-7 shuffle is a MirageGrid subsystem / law, not a
separate product  
**Cites:** AZ-GENERATOR-1.0 · MIRAGE-GRID-SHIFT-1.0 · SEMANTIC-BRIDGE-1.0 ·
AIRGAP-1.0 · REDLINE-1.0 · NO-LIE · NO-REWRITE · NO-FAN-1.0

This paper locks the **named app Worker** and the **ping → land → update**
shuffle. It does not invent a Softwares-tab product beyond MirageGrid.
It does not invent public ICANN `.az` DNS.

## Two hosted Workers (honest)

| Worker name | Host | Plane | Honesty |
| --- | --- | --- | --- |
| `miragegrid` | `https://miragegrid.vibelock.workers.dev` | App / Cap-7 shuffle / FragGate doors | **LIVE** after this deploy |
| `miragegrid-download-tracker` | `https://miragegrid-download-tracker.vibelock.workers.dev` | Counted download | **LIVE** |

Historical Cloudflare **1042** (Worker `miragegrid` missing, account
error 10007) is **closed by creating Worker `miragegrid`**. Do not keep
citing the named host as dead once this Worker exists. Do not pretend
the download-tracker *is* the app Worker.

## Cap-7 sites (MirageGrid-only factory)

Exactly **7** factory sites. **Different names** from each other and
from the four official hubs. They inherit **hub design DNA only**.

Locked stamps on every site:

- `resolves_to_hub: false`
- `name_may_change: true`
- `public_icann: false`
- `fifth_product: false`
- `radio_phy: false`
- AZ Generator exit: **FRONT Node Gate only** (`callable: false`)

| Label | Design DNA (`design_of` / `canonical_hub`) | Public HTTPS | AZNet |
| --- | --- | --- | --- |
| `azgrid` | https://www.azieleliab.com/ | **LIVE** Worker path `/cap7/azgrid` | yes |
| `azbooth` | https://www.azieleliab.com/ | **LIVE** Worker path `/cap7/azbooth` | yes |
| `azcloak` | https://godlock.uk/ | **SLOT** (not browser-reachable) | mesh-side |
| `azvault` | https://www.azielcorpuslibrary.net/ | **SLOT** | mesh-side |
| `azshift` | https://hedidntjump.com/ | **SLOT** | mesh-side |
| `azflag` | https://www.azielcorpuslibrary.net/ | **SLOT** | mesh-side |
| `azstandby` | https://godlock.uk/ | **SLOT** | mesh-side |

Exactly **2** of Cap-7 are browser-reachable HTTPS mirrors on the app
Worker (the public pair: `azgrid` + `azbooth`). The other **5** are
**AZNet-hosted survival endpoints** — mesh/AZNet-side, not public
HTTPS. Mesh names (`azgrid.az`, …) stay **SLOT** on ICANN. Do not
invent `www.survivalnetwork.az` as live HTTPS.

`azcorpus` + `azlibrary` remain **named mesh-site designs** inside
azielcorpuslibrary.net (SEMANTIC-BRIDGE-1.0). They are not the Cap-7
factory site names.

## Update shuffle (no hard-coded host)

All nodes **ping MirageGrid** (the app Worker) until they **land on
one Cap-7 site in the shuffle**. That land is the **update endpoint
for that round**.

- No single hard-coded Cap-7 host.
- Land is `SHA-256(seed) mod 7` over the locked 7-label roster.
- **Update is proof, not a timer** (STW-1.0). An update-round seed is
  `prev|lockset`. A coordination-round seed is an explicit `round_id`.
- Ping without a seed stays `phase: ping`, `continue: true` — do not
  invent a land.
- Same seed → same land for every node. GET never plants a claim.

## AZNet survival surface

Cap-7 **establishes AZNet-hosted endpoints** as the survival surface.
AZNet and AZBrowser stay **separate Softwares** (pairing only; never
merge). Naked public DNS is refuse.

- Public pair: browser-reachable Worker HTTPS **and** AZNet.
- Remainder: AZNet-side only. Public HTTPS honesty is **SLOT**.
- Worker `/aznet/cap7/{label}` **cites** the mesh-side endpoint. It
  does not pretend the name resolves on ICANN.

## Bridge cite (aziel-runtime LIVE doors)

Runtime cites the app Worker:

- `GET /bridge` (also `/bridge.json`, `/v1/bridge`)
- `GET /v1/shuffle` · `POST /v1/shuffle/ping` · `GET /v1/shuffle/land`
- `GET /v1/cap7`

FragGate LIVE_OPS stay `health`, `assign`, `verify-receipt`, `bridge`,
`nodes`, `doctor`, `skill`. Hosted vpn/hop/tunnel/mesh stay stub.

## Refuse

- Fake ICANN / Cloudflare registrar / `.az` ccTLD takeover
- `resolves_to_hub: true` / hub CNAME / redirect
- Hard-coding one Cap-7 host as the only update door
- Inventing live HTTPS for AZNet-side slots or `www.survivalnetwork.az`
- Calling AZ Generator from the Worker
- GET enable / GET radio-on / GET claim plant
- Invented radio PHY
- Merging AZNet / AZBrowser / MirageGrid into one product
- Citing the named Worker as CF 1042 dead after this deploy

Identity: **Aziel Eliab** only.
