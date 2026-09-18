# OUTLAST companion — Cap-7 / MirageGrid mesh (2026-09-18)

**Author:** Aziel Eliab only  
**Kind:** outlast / communication-preservation companion  
**Worker LIVE:** `https://miragegrid.vibelock.workers.dev` (`worker_name=miragegrid`, `role=cap-7-shuffle-app`, post #15/#16)  
**Download plane:** `https://miragegrid-download-tracker.vibelock.workers.dev`  
**Door:** FragGate is THE exec door. Catalog slug `miragegrid` digest `d7e85c3ed924ed68076aa40ce9bbc9247ff3b8076f0cdd4be7fcda40506c8d07` (verify matched 2026-09-18; registry digest `1906551cd1d3cadd5a322c03d4ceaf94c9aa0f473392f1761bd4c5caa8de82e8`). LIVE_OPS: `health`, `assign`, `verify-receipt`, `bridge`, `shuffle`, `nodes`, `doctor`, `skill`. Stub: `vpn-hop`, `hop`, `tunnel`, `mesh`.  
**Aligns with:** live aziel-runtime `GET /survival` `cap7_aznet` + [BAN-SURVIVAL-1.0](https://github.com/AzielEliab/aziel-runtime/blob/main/docs/designs/BAN-SURVIVAL-1.0.md) §6 / §6b / §6c. Security sibling: [SECURITY-FINDINGS-2026-09-18.md](SECURITY-FINDINGS-2026-09-18.md).

Goal: the Cap-7 / mesh path **outlasts bans and hostname death** without inventing ICANN `.az` or a second FragGate door. One banned workers.dev host is not last tip gone. Landing on another factory name is not a new `/mcp`.

Live probe (User-Agent `Mozilla/5.0`, 2026-09-18):

| Check | Result |
| --- | --- |
| `GET /v1/health` | `ok:true`, `resolves_to_hub:false`, `radio_phy:false`, `channel_plane_is_vpn:false`, `second_door:false`, `hosted_endpoints:SLOT` |
| `GET /bridge` | `BRIDGE-CAP7-SHUFFLE`; public-pair HTTPS LIVE; AZNet-side HTTPS SLOT; mesh `.az` SLOT; first-flag HTTPS SLOT; `hosted_update:SLOT` |
| `GET /v1/shuffle` | `CAP7-SHUFFLE-CITE`, `hardcoded_host:false`, `public_shuffle_land_exec:SLOT` |
| `POST /v1/shuffle/ping` `{}` | `CAP7-PING` `continue:true` (no invented land) |
| `POST /v1/shuffle/ping` `{round_id}` | `CAP7-LAND` (coordination cite). Land exec stays SLOT. |
| `POST /v1/shuffle/update` `{prev,lockset}` | `CAP7-UPDATE`. `hosted_update:SLOT`. Same seed → same land. |
| `GET /v1/shuffle/ping?prev=p&lockset=l` | `403 MESH-GET-NO-ENABLE` |
| `GET /cap7/azgrid` | `CAP7-GATEWAY-LIVE` (Worker path cite, not ICANN, `is_live_door:false`) |
| `GET /cap7/azcloak` | `403 CAP7-SLOT-NOT-LIVE`, `resolves_to_hub:false`, `radio_phy:false` |
| `GET /aznet/cap7/azcloak` | `CAP7-AZNET-SLOT` (cite only; `aznet_payload_host:false`) |
| `GET /v1/mesh` | allowlisted PROXY. `node_gate:false`, `this_worker_is_node_gate:false`, `fraggate_single_door:true`, `open_proxy:false` |
| `POST /v1/mesh/grid-shift` `{name:foo.az}` | `403 MGS-NO-HOSTED-APPLY` (hosted Worker does not apply a shift) |
| `POST /v1/mesh/grid-shift` cloak_burst | `403 MGS-NO-HOSTED-PLANT` |
| `GET /v1/mesh/vpn` `/hop` `/tunnel` | `403 MESH-STUB` |
| FragGate `fraggate_verify { slug: miragegrid }` | matched. Stub ops stay stub. |

No fake ICANN `.az` publish. No open node proxy. No second `/mcp`.

---

## Verdict

**The Cap-7/mesh path can outlast a banned hostname** because:

1. **Seven relocatable factory names** (`name_may_change:true`) — a dead `workers.dev` path is not the only land.
2. **Ping → land → update is proof, not a hard-coded host.** Same `prev|lockset` or `round_id` lands every node on the same label.
3. **AZNet-side remainder stays SLOT on public HTTPS.** Survival names are mesh/AZNet cites (`aznet://cap7/{label}`), not invented ICANN.
4. **Hash/receipt continuity is FragGate + AZNet verify** (`stamp`, `verify_hash`, `receipt_verify`) — the Worker session hash is not a second receipt door.
5. **Cold shelves + runtime `/survival` stay the death-by-ban backup.** This Worker is not `/mcp`.

**It must not outlast by lying.** Hosted assign is a communication/control plane. Local `miragegrid vpn` is the mesh VPN. AZNet pairing is not a tunnel. Channel plane is not a VPN (`channel_plane_is_vpn:false`).

---

## CRITICAL

None on the public packet path. Hosted MirageGrid still does not forward packets, does not open an arbitrary-origin HTTP proxy, and does not host AZNet payloads.

---

## HIGH

### H1 — Hosted `POST /v1/mesh/grid-shift` claimed a live apply (`MGS-SHIFT-OK`)

**Surface:** `POST /v1/mesh/grid-shift` `{"name":"foo.az"}` on the LIVE Worker returned `200 MGS-SHIFT-OK` / `answerable:true`.  
**Law:** MIRAGE-GRID-SHIFT-1.0 apply + cloak is FRONT Node Gate / local node only. Hosted Worker is cite. `#16` already refused hosted cloak-burst plant (`MGS-NO-HOSTED-PLANT`) but left the generic apply path claiming the `.az` stayed answerable. That is a NO-LIE / OUTLAST fail: hostname death is not survived by a Worker pretending a grid-shift happened.

**Fix in this PR:** hosted `applyGridShift` success → `403 MGS-NO-HOSTED-APPLY`. GET `/v1/mesh/grid-shift` stays `MGS-CITE`. Local Python `miragegrid.mesh.grid_shift` stays node-local `MGS-SHIFT-OK` (tests unchanged).

### H2 — Communication plane vs VPN lie (`kind: mesh-vpn-circuit` on hosted assign)

**Surface:** `POST /v1/assign` on the app Worker returned `kind: "mesh-vpn-circuit"` next to banner “MirageGrid is not a VPN”. Runtime `/survival` `cap7_aznet.channel_plane_is_vpn` is **false**; `pairing_is_tunnel` is **false**. FragGate stub ops `vpn-hop` / `hop` / `tunnel` / `mesh` stay stub.  
**Risk:** a banned-host client (or an LLM) reads hosted assign as a VPN hop / second concealment door.

**Fix in this PR:** hosted assign/health/bridge/shuffle/mesh overlay `channel_plane_is_vpn:false`, `hosted_vpn:false`, `packet_forwarding:false`, `communication_plane:true`, `hosted_kind:"session-assignment"`. Ping bodies that set `channel_plane_is_vpn` / `hosted_vpn` / `second_door` / `open_proxy` refuse `CAP7-NO-VPN-LIE`. Historical `kind: mesh-vpn-circuit` stays on the shared assign payload (local package *is* a mesh VPN) so clients do not break.

---

## MEDIUM

### M1 — Public land/update looked like hosted exec (runtime SLOT)

Runtime BAN-SURVIVAL §6c / `/survival` shuffle:

- `public_worker_bridge`: LIVE cite
- `public_worker_shuffle`: SLOT exec
- `hosted_update`: SLOT
- factory `honesty_public` LIVE on azgrid/azbooth = **path cite**, `is_live_door:false`

Product #15 made `POST /v1/shuffle/ping` → `CAP7-LAND` on public HTTPS. That land is **coordination** (which name is this round’s update endpoint). `POST /cap7/azgrid/update` still returns `CAP7-NO-HARDCODED-HOST`. AZNet-side land cites `aznet://cap7/{label}/update`.

**This PR:** stamp `public_shuffle_land_exec:SLOT`, `hosted_update:SLOT`, `is_live_door:false` on land/update/bridge/roster. Do **not** take down ping→land cite — that is how the path outlasts a dead hostname. Do **not** invent a working hosted update `/mcp`.

### M2 — Hash/receipt continuity was Worker-local only

`POST /v1/verify-receipt` checks SHA-256 of `{integrity, mirage_node, session_id, timestamp}`. That is a session-assignment hash. Ban-survival continuity when a public door dies is AZNet via FragGate (`stamp` / `verify_hash` / `receipt_verify`) plus catalog `verify-receipt`. A Worker-only hash is not a second ForgeReceipts door.

**This PR:** `hash_receipt` stamp on health/doctor/assign/verify-receipt/bridge (`second_receipt_door:false`, `door:fraggate_call`, `aznet_verify:[stamp,verify_hash,receipt_verify]`). Cap JSON body on verify-receipt (64 KiB). No Worker theater crypto.

### M3 — AZNet hosted-endpoint honesty was incomplete on SLOT refuse

`GET /cap7/azcloak` omitted `resolves_to_hub` / `radio_phy`. Runtime hosted_endpoints stay SLOT (`BAN-CAP7-HOST-NOT-ATTESTED`, `payload_host:stub`).

**This PR:** SLOT refuse and `/aznet/cap7/*` cites carry `resolves_to_hub:false`, `radio_phy:false`, `hosted_endpoints:SLOT`, `aznet_payload_host:false`.

---

## LOW

### L1 — Dual public mesh PROXY (download-tracker still a control plane)

Same as security F2. Allowlist only (`/v1/mesh`, `/status`, `/nodes`, POST enable/disable/join/heartbeat/leave/broadcast`). Not `BAN-NO-OPEN-NODE-PROXY`. `live_node_api:SLOT`.

### L2 — Update proof still syntactic

Same as security M1 / F1. `prev`+`lockset` are non-empty strings. Follow-on: ChainLock / FragGate `zkattest`. Do not invent Worker theater crypto to “survive.”

---

## Alignment with runtime OUTLAST / BAN-SURVIVAL

| Runtime `/survival` `cap7_aznet` | This Worker after this PR |
| --- | --- |
| `radio_phy: false` | stamped on health/bridge/shuffle/cap7/mesh |
| `resolves_to_hub: false` | stamped; ping `resolves_to_hub:true` → `BRIDGE-NO-HUB-RESOLVE` |
| `public_icann: false` / `live_registrar: false` | stamped; ping ICANN → `AZG-NOT-PUBLIC-REGISTRAR` |
| `channel_plane_is_vpn: false` | stamped; ping VPN-lie → `CAP7-NO-VPN-LIE` |
| `pairing_is_tunnel: false` | stamped |
| `cite` LIVE (`/bridge` + FragGate `op:bridge`) | LIVE cite |
| `aznet_verify` LIVE via `fraggate_call` | `hash_receipt` points at those ops; Worker is not a second door |
| `hosted_endpoints` SLOT / `payload_host: stub` | `hosted_endpoints:SLOT`, `aznet_payload_host:false` |
| shuffle `layout` LIVE, `public_worker_shuffle` SLOT, `hosted_update` SLOT | ping→land cite LIVE; land exec + hosted update SLOT |
| `live_node_api` SLOT / `BAN-NO-OPEN-NODE-PROXY` | allowlisted PROXY only; unknown mesh path 404 |
| `fraggate_is_the_door` / `backdoor_exec: false` | `second_door:false`, `fraggate_single_door:true` |
| Node Gate = FRONT exit only | `az_generator.exit: node-gate-front`, `this_worker_is_node_gate:false`, `callable:false` |

In-process land remains `fraggate_call { slug: "miragegrid", op: "shuffle" }`. App-Worker `/bridge` is the LIVE cite surface runtime already names. This repo does not invent a Cap-7 `/mcp`.

---

## What stayed honest (no change)

- AZ Generator `callable:false`, exit FRONT Node Gate only.
- Public pair = `azgrid` + `azbooth` only. Other five = AZNet-side SLOT on public HTTPS.
- Mesh PROXY allowlist only. `POST /v1/mesh/disable` → `MESH-DISABLE-REFUSED`. Empty enable → `MESH-NEED-BEARER`.
- GET never plants (`MESH-GET-NO-ENABLE`).
- FragGate stub ops stay stub. Digest continuity is `fraggate_verify`, not a Worker-invented digest.
- Local Python `grid_shift` / `cloak_burst` stay node-local law.
- Download-tracker has no `/v1/shuffle`. App Worker has no `/download` increment.

---

## Safe fixes shipped here

| Code | Change |
| --- | --- |
| `OUTLAST_HONESTY` / `hash_receipt` | Stamps on Worker mesh overlay, health, doctor, assign, verify-receipt, bridge, roster, land, update |
| `MGS-NO-HOSTED-APPLY` | Hosted grid-shift apply refused |
| `CAP7-NO-VPN-LIE` | Refuse VPN / second-door / open-proxy claims on ping |
| SLOT refuse fields | `resolves_to_hub` + `radio_phy` + `aznet_payload_host` on azcloak-class paths |
| `hosted_kind: session-assignment` | Honesty overlay on hosted assign (kind string preserved) |

Identity: **Aziel Eliab** only.
