# CAP-7 LIVE SHUFFLE (CAP7-SHUFFLE-1.0)

**Author:** Aziel Eliab only  
**Status:** Locked design law  
**Softwares-tab:** no — Cap-7 shuffle is a MirageGrid subsystem / law, not a
separate product  
**Cites:** AZ-GENERATOR-1.0 · MIRAGE-GRID-SHIFT-1.0 · SEMANTIC-BRIDGE-1.0 ·
AIRGAP-1.0 · REDLINE-1.0 · NO-LIE · NO-REWRITE · NO-FAN-1.0

This paper locks the **named app Worker** and the **ping → land → update**
shuffle. It does not invent a Softwares-tab product beyond MirageGrid.
Cap-7 is not publicly typed on ICANN DNS. Internet reaches **AZ domains
only**, through the four hub websites.

## Two hosted Workers (honest)

| Worker name | Host | Plane | Honesty |
| --- | --- | --- | --- |
| `miragegrid` | `https://miragegrid.vibelock.workers.dev` | App / Cap-7 shuffle / FragGate doors | **LIVE** after this deploy |
| `miragegrid-download-tracker` | `https://miragegrid-download-tracker.vibelock.workers.dev` | Counted download | **LIVE** |

Historical Cloudflare **1042** (Worker `miragegrid` missing, account
error 10007) is **closed by creating Worker `miragegrid`**. Do not keep
citing the named host as dead once this Worker exists. Do not pretend
the download-tracker *is* the app Worker.

## Cap-7 sites (auto `.az` duplication / shift)

Exactly **7** factory sites. Cap-7 **auto-generates `.az` mirrors
of all 4 hubs** and **shifts** them with **StaticLock** + **MirageGrid
cloak** + **planned-egress**. planned-egress is not a hosted packet VPN
and not AZVPN.

**Exactly 4** are hub mirrors (one per hub). **Exactly 3**
are decoys. Those seven names are separate from per-node `.aziel` slots.

Factory honesty is **LIVE**. There is no SLOT hedge on hosted update,
hosted MCP, shuffle land, or the factory itself. Live nodes anchor
the factory. Cap-7 names are **not** publicly typed on ICANN DNS and
are **not** the public internet door.

| Label | Hub duplicated | Kind |
| --- | --- | --- |
| `azgrid` | https://www.azieleliab.com/ | real hub duplication |
| `azcloak` | https://godlock.uk/ | real hub duplication |
| `azvault` | https://www.azielcorpuslibrary.net/ | real hub duplication |
| `azshift` | https://hedidntjump.com/ | real hub duplication |
| `azbooth` | cloak shape of azieleliab | **false site** (decoy) |
| `azflag` | cloak shape of corpus | **false site** (decoy) |
| `azstandby` | cloak shape of godlock | **false site** (decoy) |

Stamps on every factory site:

- `factory_honesty: LIVE`
- `typed_on_icann_dns: false`
- `internet_reachable: false`
- `hosted_update` / `hosted_mcp` / `public_shuffle_land_exec`: **LIVE**
- `anchored_by_live_nodes: true`
- `shift_stack`: `staticlock`, `miragegrid-cloak`, `planned-egress`
- `planned_egress.status`: `planned` (`hosted: false`, `packet_forwarding: false`, `live: false`)
- `public_icann_registrar: false`
- `separate_from_per_node_aziel_slots: true`
- `radio_phy: false`
- AZ Generator exit: **FRONT Node Gate only** (`callable: false`)
- Real four: `hub_duplication: true`, `resolves_to_hub: true` (the `.az` duplicate pairs to that hub)
- Decoy three: `false_site: true`, `resolves_to_hub: false`

## AZ domains (the public internet doors)

Internet reaches these names **only**, via the hub HTTPS links.
They are not Cap-7. Shuffle **once** to 1 of 4. Mirror the hub while
it is up. Stand alone without that site. Become **immutable** after
the hub goes down. Anchored by live nodes. Not a Softwares-tab product.
Not an ICANN registrar purchase of a ccTLD.

| Display name | Hub HTTPS |
| --- | --- |
| `AZ.AzielEliab.AZ` | https://www.azieleliab.com/ |
| `AZ.AzielCorpusLibrary.AZ` | https://www.azielcorpuslibrary.net/ |
| `AZ.Godlock.AZ` | https://godlock.uk/ |
| `AZ.HeDidntJump.AZ` | https://hedidntjump.com/ |

Each door: `public_icann: true`, `resolves_to_hub: true`,
`internet_reachable: true`, `honesty: LIVE`.

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
- The update **URL** is always this app Worker (`POST /v1/shuffle/update`). `update_endpoint_varies_by_land` is **false**. The land **label** is which factory name the round cites. Do not describe that label as a distinct public host.

## AZnet survival surface

Cap-7 is the duplication/shift/cloak layer. AZnet and AZ Browser stay
**separate Softwares** (pairing only; never merge). The hosted HTTP
channel is not a packet VPN and not AZVPN. The third shift-stack name
is `planned-egress`.

## Planned adaptation (not LIVE)

These are design intent only. No LIVE flag. No ICANN publish. No packet hop.

| Name | Meaning | Honesty |
| --- | --- | --- |
| `geo-target` | Optional region label on assign or shuffle land | metadata only; `ip_exit: false`. Worker door `MG-GEO-NOT-READY`. |
| `session-stick` | Bind a session or land for a TTL | `status: planned`. A TTL refuses `MG-STICKY-TTL-NOT-READY`. |
| `egress-rotate` | Rotate the hosted update land among the Cap-7 roster | not ICANN DNS; not a packet hop. Worker door `MG-EGRESS-IP-NOT-READY`. |

`POST /v1/session/sticky` is a separate live mesh-node label (`SHA-256` of the key). It is not an IP and not the planned TTL stick. Sticky public IPs refuse `MG-STICKY-IP-NOT-READY`. See [MG-EGRESS-1.0.md](MG-EGRESS-1.0.md).

FragGate ops `vpn-hop`, `hop`, `tunnel`, and `mesh` stay non-executable
(runtime `FG-STUB`). The FragGate `mesh` op is not QNM suite `mesh_*`
and it is not `GET /v1/mesh` status.

Worker `/cap7/{label}` cites the LIVE factory site. It does not publish
that name on ICANN DNS.

## Bridge cite (aziel-runtime LIVE doors)

Runtime cites the app Worker:

- `GET /bridge` (also `/bridge.json`, `/v1/bridge`)
- `GET /v1/shuffle` · `POST /v1/shuffle/ping` · `GET /v1/shuffle/land`
- `GET /v1/cap7`

FragGate LIVE_OPS stay `health`, `assign`, `verify-receipt`, `bridge`,
`nodes`, `doctor`, `skill`. Hosted vpn/hop/tunnel/mesh stay stub.

## Refuse

- Claiming Cap-7 is publicly typed on ICANN DNS (`CAP7-NOT-ICANN-DNS`)
- Claiming an ICANN registrar purchase of a ccTLD (`AZG-NOT-PUBLIC-REGISTRAR`)
- Hard-coding one Cap-7 host as the only update door
- Inventing `www.survivalnetwork.az` as live HTTPS
- Calling AZ Generator from the Worker
- GET enable / GET radio-on / GET claim plant / GET `prev`+`lockset` update plant
- Hosted cloak-burst name plant (`MGS-NO-HOSTED-PLANT`)
- Invented radio PHY
- Merging AZnet / AZ Browser / AZVPN / MirageGrid into one product
- Treating geo, sticky public IP, or egress rotation as live ([MG-EGRESS-1.0.md](MG-EGRESS-1.0.md))
- SLOT hedges on factory honesty, hosted update, hosted MCP, or shuffle land
- Citing the named Worker as CF 1042 dead after this deploy

Designed AZ-domain `resolves_to_hub: true` + `public_icann: true` is the
public internet path. It is not a refuse.

Identity: **Aziel Eliab** only.
