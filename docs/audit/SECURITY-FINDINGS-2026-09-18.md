# Cap-7 / MirageGrid SECURITY AUDIT (2026-09-18)

**Author:** Aziel Eliab only  
**Kind:** design / function / protocol  
**Worker LIVE:** `https://miragegrid.vibelock.workers.dev` (`worker_name=miragegrid`, `role=cap-7-shuffle-app`)  
**Download plane:** `https://miragegrid-download-tracker.vibelock.workers.dev` (counted downloads only — still also hosts `/v1` assign + mesh PROXY)  
**Door:** FragGate is THE exec door. Catalog slug `miragegrid` LIVE_OPS: `health`, `assign`, `verify-receipt`, `bridge`, `shuffle`, `nodes`, `doctor`, `skill`. Stub: `vpn-hop`, `hop`, `tunnel`, `mesh`.  
**Companion:** aziel-runtime [BAN-SURVIVAL-1.0](https://github.com/AzielEliab/aziel-runtime/blob/main/docs/designs/BAN-SURVIVAL-1.0.md) (mutual backup; no second door; no open node proxy; Cap-7 hosted `/mcp` stays SLOT).

Live probe (User-Agent `Mozilla/5.0`, 2026-09-18):

| Check | Result |
| --- | --- |
| `GET /v1/health` | `ok:true`, `resolves_to_hub:false`, `radio_phy:false`, `public_icann:false` |
| `GET /bridge` | `BRIDGE-CAP7-SHUFFLE`; public-pair HTTPS LIVE; AZNet-side HTTPS SLOT; mesh `.az` SLOT; first-flag HTTPS SLOT |
| `GET /v1/shuffle` | `CAP7-SHUFFLE-CITE`, `hardcoded_host:false` |
| `GET /cap7/azgrid` | `CAP7-GATEWAY-LIVE` (Worker path, not ICANN) |
| `GET /cap7/azcloak` | `403 CAP7-SLOT-NOT-LIVE` |
| `GET /aznet/cap7/azcloak` | `CAP7-AZNET-SLOT` (cite only) |
| `GET /v1/az-generator` | `403 AZG-NOT-CALLABLE` |
| `GET /v1/mesh/enable` | `403 MESH-GET-NO-ENABLE` |
| `GET /v1/shuffle/update` | `403 MESH-GET-NO-ENABLE` |
| `POST /v1/mesh/disable` | `400 MESH-DISABLE-REFUSED` (suite-presence stays ON — honest) |
| `POST /v1/mesh/enable` `{}` | `400 MESH-NEED-BEARER` |

No fake ICANN `.az` publish was observed. FragGate describe (`slug=miragegrid`, digest `d7e85c3ed9…`) stays the catalog door.

---

## CRITICAL

None on the public packet path. Hosted MirageGrid does not forward packets, does not open an arbitrary-origin HTTP proxy, and does not call AZ Generator. `/v1/mesh/*` is allowlisted to `aziel-runtime` only (`AZIEL_RUNTIME` binding + fixed HTTPS origin). That is **not** `BAN-NO-OPEN-NODE-PROXY`.

---

## HIGH

### H1 — JS land index loses 64-bit precision (`SHA-256(seed) mod 7` can disagree)

**Surface:** `workers/miragegrid/src/shuffle.js` `landIndex` used `Number.parseInt(hex.slice(0, 16), 16)`.  
**Protocol:** CAP7-SHUFFLE-1.0: same seed → same land. Python `int(digest[:16], 16) % 7` is exact. JS IEEE-754 cannot hold 64-bit integers (`0xffffffffffffffff` is not a safe integer).

Live check: `parseInt("ffffffffffffffff", 16) % 7 === 2` vs Python / `BigInt` `% 7 === 1`.

**Fix in this PR:** `BigInt("0x" + slice) % 7n`. Tests pin `f*64` and several `round_id` seeds against Python.

### H2 — GET ping/land with `prev`+`lockset` returned `update:true` (GET planted an update-shaped land)

**Surface:** `GET /v1/shuffle/ping?prev=p&lockset=l` on the LIVE Worker returned `CAP7-LAND` / `update:true` (200).  
**Law:** REDLINE-1.0 / CAP7-SHUFFLE-1.0 — GET never plants. `POST /v1/shuffle/update` is the third hop.

`refuseGetEnableOrPlant` did not treat `prev`/`lockset` as plant intent, and `ping()` called it with an empty search string.

**Fix in this PR:** GET/HEAD + `prev`+`lockset` (or path `…/update`) → `403 MESH-GET-NO-ENABLE`. GET land/cite with `round_id` stays cite-only (`update:false`).

### H3 — Mesh PROXY passed through runtime `node_gate` / `auto_heal` / `anonymity_network` = true

**Surface:** `GET /v1/mesh` on **both** Workers returned `node_gate:true`, `auto_heal:true`, `anonymity_network:true` (copied from the suite mesh envelope).  
**Law:** hosted MirageGrid is not Node Gate, not auto-heal, not an anonymity network. `attachQnsCd` spread runtime data first and never overwrote those three stamps.

`enabled:true` on that GET is **suite-presence status** (BAN-SURVIVAL / QNM read-only presence ON by default). This PR does **not** rewrite `enabled` — GET is status, not enable.

**Fix in this PR:** `attachQnsCd` locks Worker honesty stamps last: `node_gate:false`, `auto_heal:false`, `anonymity_network:false`, `radio_phy:false`, `public_icann:false`, `resolves_to_hub:false`, `this_worker_is_node_gate:false`, `fraggate_single_door:true`.

### H4 — Hosted `POST /v1/mesh/grid-shift` cloak_burst accepted invented `.az` names

**Surface:** `POST /v1/mesh/grid-shift` `{"cloak_burst":true,"names":["evil.az","takeover.az"]}` → `200 MGS-CLOAK-BURST` “planted spare .az names”.  
**Law:** name factory is the locked Cap-7 roster; plant/claim exits FRONT Node Gate only; hosted Worker is not a registrar.

Local `miragegrid.mesh.cloak_burst` stays the **node-local** law (tests unchanged). The **hosted** Worker path now refuses.

**Fix in this PR:** hosted `applyGridShift` cloak_burst → `403 MGS-NO-HOSTED-PLANT`.

---

## MEDIUM

### M1 — Update “proof” is syntactic, not attested

`prev`+`lockset` may be any non-empty strings (`"p"`+`"l"` lands). Same pair → same land (good). There is no ChainLock / LOCKSET verify, no node attest, no replay window. Anyone can POST a land/update cite.

**This PR:** cap JSON body (64 KiB) and `node_id` (`[A-Za-z0-9._-]{1,80}`).  
**Follow-on:** bind `lockset` to a verified tip (ChainLock / FragGate `zkattest`). Do not invent Worker theater crypto.

### M2 — Dual public mesh / assign doors (download-tracker still a control plane)

#15 isolated the **named** Worker. The download-tracker still serves `/v1/assign`, `/v1/mesh/*` PROXY, and OpenAPI. Two public surfaces accept mesh bearer headers (CORS `*`).

**This PR:** Via header uses `WORKER_ROLE` when set (`cap-7-shuffle-app` vs download-tracker).  
**Follow-on:** shrink download-tracker to counted download + cite; keep shuffle/assign on `miragegrid` only.

### M3 — `POST /event` increments KV with no auth and any asset

Live: `{"owner":"evil","repo":"x","asset":"nope"}` → `200` and `count` incremented (already 47 on that key). Homepage has no `/event` CTA (good). Path traversal `/download/..%2Fwrangler.toml` → 404 (good).

**Fix in this PR:** increment only for `AzielEliab/miragegrid` + allowlisted `miragegrid-*.tar.gz` asset; reject `..` / slashes / control chars in asset names.

### M4 — BAN-SURVIVAL paper still marks public workers.dev shuffle SLOT

Runtime BAN-SURVIVAL-1.0 §6c: “Public MirageGrid workers.dev shuffle stays SLOT” and `/bridge` “not a LIVE shuffle door from this runtime”. Product #15 made `GET /bridge` + ping→land **LIVE cite** on `miragegrid.vibelock.workers.dev`.

This is a **coordination gap**, not a product lie: the Worker is live; the runtime paper is stale. Hosted Cap-7 `/mcp` and ICANN `.az` stay SLOT (`BAN-NO-FAKE-CAP7-HOST`). This Worker is **not** a FragGate exec origin.

**Follow-on (aziel-runtime):** update BAN-SURVIVAL cite: public shuffle on the **named** app Worker is LIVE **cite/land** (not `/mcp`); hosted update URL for AZNet-side names stays SLOT; do not invent a second door.

### M5 — Unbounded mesh PROXY `res.text()` when `Content-Length` is missing

Allowlist + 2 MiB `Content-Length` cap exist. Missing/wrong `Content-Length` still buffered the full body.

**Fix in this PR:** read as `arrayBuffer`, refuse > 2 MiB regardless of header. Refuse `..` in proxied paths.

---

## LOW

### L1 — CORS `*` on cite/assign/shuffle

Expected for a public cite API. Bearer on mesh enable is still runtime-gated (`MESH-NEED-BEARER`). Follow-on: tighten CORS on `POST /v1/mesh/enable` if a browser credential flow is ever added (none today).

### L2 — `GET /cap7/{label}/update` cited the gateway (looked like an update hop)

**Fix in this PR:** GET `…/update` → `MESH-GET-NO-ENABLE`. POST `…/update` on a public-pair label points callers at `POST /v1/shuffle/update` (no hard-coded host).

### L3 — `X-Aziel-Runtime-Via` always said `miragegrid-download-tracker`

**Fix in this PR:** app Worker sends `cap-7-shuffle-app`.

### L4 — OpenAPI on the app Worker omitted mesh / land honesty notes

Documentation only. Follow-on: generate from one spec.

---

## What stayed honest (no change)

- AZ Generator `callable:false`, exit `node-gate-front`; aliases `403 AZG-NOT-CALLABLE`.
- Public pair = `azgrid` + `azbooth` only. Other five = AZNet-side SLOT on public HTTPS.
- `resolves_to_hub:false`, `public_icann:false`, `radio_phy:false` on health/bridge/cap7.
- Mesh PROXY allowlist only (`/v1/mesh`, `/status`, `/nodes`, POST enable/disable/join/heartbeat/leave/broadcast`). Not an open proxy.
- `POST /v1/mesh/disable` refused by runtime (`MESH-DISABLE-REFUSED`).
- Download-tracker has no `/v1/shuffle` (404). App Worker has no `/download` increment.
- FragGate stub ops (`vpn-hop` / `hop` / `tunnel` / `mesh`) stay stub. FragGate is THE door.

Identity: **Aziel Eliab** only.
