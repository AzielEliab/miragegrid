---
name: MirageGrid
description: Use when calling MirageGrid hosted /v1 or installing the local package. Dual surface: Worker /v1 + catalog MCP. This Worker /v1/mesh/* PROXY to aziel-runtime via AZIEL_RUNTIME. Suite mesh default OFF. QNM-BUILD-1.0 live|locked|isolated. QNS-CD-1.0 photon QNS1 packet transfer is a hub cite / Worker mesh cross-map only (qnm-node qnsd + aziel-runtime catalog). SPLIT THE WIRES. COLD-COPY SURVIVAL. REHEAL. AZ-GENERATOR-1.0. MIRAGE-GRID-SHIFT-1.0. AIRGAP-1.0. SEMANTIC-BRIDGE-1.0. REDLINE-1.0. NO-FAN-1.0. No Node Gate. No public qnsd proxy. No auto-heal. Not anonymity. Hosted MirageGrid is not a VPN. Author Aziel Eliab.
---

# MirageGrid

Ephemeral session node assignment. 25 named peers. Receipts. Author: **Aziel Eliab**.

**THIS IS:** a session assignment engine (mesh maps, circuit hops, internal receipts). Assign stays live. Mesh law is SPLIT THE WIRES + COLD-COPY SURVIVAL + REHEAL + AZ-GENERATOR-1.0 + MIRAGE-GRID-SHIFT-1.0 + AIRGAP-1.0 + NO-LIE + NO-REWRITE + NO-FAN-1.0 (**No falsification. No ambiguity. No misleading.**). Paper vault multiplies onto each node as cold copies (no paper-body fan-out on the 1s tip tick). Public-stack auto-heal means lawful REHEAL-1.0 / MESH-REHEAL, not neighbor vote-to-fix. AZ Generator and Node Gate are MirageGrid subsystems — not Softwares-tab products.

**THIS IS NOT:** a VPN, an anonymity network, a hosted hop, a crime tool, a log-wipe, or a guarantee against global surveillance. Hosted `/v1` does not increment downloads or views.

Always send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.

## Call these URLs

- App Worker (Cap-7 shuffle): https://miragegrid.vibelock.workers.dev/
- App OpenAPI: https://miragegrid.vibelock.workers.dev/openapi.json
- Worker OpenAPI (download plane): https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- Live skill (app Worker): `GET https://miragegrid.vibelock.workers.dev/v1/skill`
- Live skill (download plane): `GET https://miragegrid-download-tracker.vibelock.workers.dev/v1/skill`

Ops (do **not** increment downloads or views):

- `GET /v1/health` — liveness
- `GET /v1/skill` — this file
- `GET /v1/topology` — persistent 25-node circulant topology (local op)
- `GET /v1/mesh` — PROXY suite mesh status. Default OFF. QNM live|locked|isolated. QNS-CD-1.0 cross-map (photon QNS1 packet transfer) is stamped for peers. Never enables. No public qnsd proxy. Stamps **SPLIT THE WIRES**, **COLD-COPY SURVIVAL**, **REHEAL**, **AZ-GENERATOR-1.0**, **MIRAGE-GRID-SHIFT-1.0**, **AIRGAP-1.0**, paper-vault-on-node.
- `POST /v1/mesh/reheal` — local REHEAL law. Own tip+trusted pull or phoenix-WAIT. Neighbor talk-dirty-back-to-health, bodies, diffs, and vote-to-fix refuse. Public-stack auto-heal means this lawful reheal, not vote-to-fix. Suite strip stays No auto-heal.
- `GET /v1/mesh/az-generator` — cite-only AZ-GENERATOR-1.0 stamps (Cap-7 mesh DNS factory; deep-node → FRONT Node Gate; not callable; `.az` → `.aziel` → pivot; four real hub duplications and three false sites; AZnet+AZ Browser; ≥49 vault; not typed on ICANN DNS). `POST` refuses `AZG-NOT-CALLABLE`.
- `GET /v1/aznet` on the app Worker — AZnet pairing cite. Naming lock: sidenet = AZnet (not a second product). L0 public path unchanged. `public_icann: false`. Cap-7 mesh DNS pairs with AZnet and AZ Browser. Exactly 2 public browser gateways (`azgrid`, `azbooth`). `POST /v1/aznet/access` needs an AZnet pairing token and an `azbrowser` flag for every other mesh name. This Worker does not verify that token and does not run the AZnet engine. `GET /v1/sidenet` refuses `AZN-NAME-LOCK`. Hosted claim/plant/flag/restore refuse. Softwares stay frozen.
- `GET /bridge` `/v1/shuffle` `POST /v1/shuffle/ping` `GET /v1/cap7` on the named app Worker `miragegrid.vibelock.workers.dev` — CAP7-SHUFFLE-1.0. Ping until land. No hard-coded Cap-7 host. GET never plants `prev`+`lockset`. Historical CF 1042 is closed. Security audit: `docs/audit/`.
- `GET /llms.txt` `/ai.txt` `/cite.json` `/bridge.json` `/v1/bridge` `/design-packs/azcorpus.json` `/design-packs/azlibrary.json` `/shelves` — SEMANTIC-BRIDGE-1.0 Growth-ON maps. Cap-7 is a mesh DNS factory (StaticLock + MirageGrid cloak + cap7-egress): four hub mirrors, three decoys, separate from per-node `.aziel` slots. Factory honesty LIVE. Not a public ICANN registrar. Not typed on ICANN DNS. Not a VPN. Not AZVPN. `packet_forwarding: false`. Internet reaches AZ domains only — AZ.AzielEliab.AZ, AZ.AzielCorpusLibrary.AZ, AZ.Godlock.AZ, AZ.HeDidntJump.AZ — via the four hub websites (`public_icann:true`, `resolves_to_hub:true`). Live nodes anchor both. Named mesh sites azcorpus and azlibrary stay designs inside azielcorpuslibrary.net. App Worker is `miragegrid.vibelock.workers.dev`. Download plane is `miragegrid-download-tracker.vibelock.workers.dev`. `/shelves` cites https://www.azielcorpuslibrary.net/shelves (Framagit URL null — not invented). REDLINE-1.0: GET never enables. AZG not callable.
- LIVE on this Worker’s Cap-7 control plane: `geo-target` (region label only; `ip_exit: false`; no Cloudflare geo-exit pool), `session-stick` (bind a mesh node and a Cap-7 land for a TTL; `sticky_public_ip: false`), `egress-rotate` (rotate the update land among Cap-7 sites; not packet egress). Still not ICANN publish. Worker health may show these three `live: true`. Softwares companion on aziel-runtime is CLEARED (tip `be1c7990452094536b122645103d41f595c03c76`, version_id `1c2de0ef-f315-4444-86aa-aec03f730a58`): `public_door_ops` lists `geo-target`, `session-stick`, and `egress-rotate` (MirageGrid 0.3.0). Cap-7 control-plane LIVE only — not a public egress IP, not residential, not AZVPN. Softwares desk layout unchanged; Softwares count stays 42. FragGate ops `vpn-hop`, `hop`, `tunnel`, and `mesh` stay non-executable (`FG-STUB`). FragGate `mesh` is not QNM suite `mesh_*` and is not `GET /v1/mesh`. A Cap-7 land hop is `egress-rotate`, not `vpn-hop`. Cap-7 is not an ICANN registrar. AZVPN is not MirageGrid.
- `GET /v1/mesh/grid-shift` — cite-only MIRAGE-GRID-SHIFT-1.0. `POST` remains local law apply (not a generator call).
- `POST /v1/mesh/airgap` — local AIRGAP-1.0 law (local vault; no bearer radios; no climb-back; no body gossip). Official hubs are not airgap Node Gate.
- `POST /v1/mesh/vault` — paper-vault-on-node multiply (cold copies on bootstrap / join / Cap-7 claim / grid-shift standby; pull-only; no tip-tick bodies).
- `GET /v1/mesh/nodes` — PROXY Live Nodes roster (5-minute presence). Same QNS-CD-1.0 cross-map.
- `POST /v1/mesh/{enable,disable,join,heartbeat,leave,broadcast}` — PROXY. Bearer required to enable. No auto-heal. Anon-broadcast is not a publish path.
- `POST /v1/route` — peer path
- `POST /v1/assign` — session circuit. A region label, `sticky_key`, or Cap-7 land rotate stamps the control plane. Public egress IPs and painted endpoints refuse (`MG-NO-IP-EXIT`, `MG-NO-EGRESS-PAINT`).
- `GET /v1/egress` — MG-EGRESS-1.0 cite. Region label, sticky mesh, and land rotate are LIVE on this Worker. No residential pool. No Cloudflare geo-exit pool. AZVPN stays separate. FragGate `vpn-hop` / `hop` / `tunnel` / `mesh` stay stub.
- `POST /v1/egress/geo` and `POST /v1/geo-target` — LIVE `MG-GEO-TARGET`. Region label plus a receipt. `ip_exit: false`.
- `POST /v1/session/sticky`, `POST /v1/session-stick`, and `POST /v1/egress/sticky` — same `sticky_key`, same mesh node and Cap-7 land. Not a public IP. Optional `ttl_seconds` is a time-bucket hash (`MG-SESSION-STICK`).
- `POST /v1/egress/rotate` and `POST /v1/egress-rotate` — LIVE `MG-EGRESS-ROTATE`. Next factory land. `ip_rotated: false`.
- Product POSTs listed in OpenAPI

Works with any OpenAPI- or MCP-capable assistant: ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants.

Import notes: ChatGPT — GPT Actions (OpenAPI URL). Grok — custom tool from OpenAPI. Venice — HTTP tools. Cursor / Glama — MCP catalog. Claude and other OpenAPI/MCP clients — same OpenAPI document or MCP catalog.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://miragegrid.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://miragegrid.vibelock.workers.dev/bridge
curl -s -A 'Mozilla/5.0' -X POST https://miragegrid.vibelock.workers.dev/v1/shuffle/ping \
  -H 'content-type: application/json' -d '{"node_id":"node-01","round_id":"r1"}'
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/mesh
curl -s -A 'Mozilla/5.0' -X POST https://miragegrid.vibelock.workers.dev/v1/assign \
  -H 'content-type: application/json' -d '{}'
```

## Local (after one-click install)

```bash
curl -fsSL https://miragegrid-download-tracker.vibelock.workers.dev/install.sh | bash
miragegrid ui
miragegrid doctor
```

Then open http://127.0.0.1:8080 (loopback). Hosted MirageGrid is not a VPN. Worker homepage Live Nodes strip polls `GET /v1/mesh` (default OFF). QNS-CD-1.0 is a hub cite / mesh cross-map only — local qnsd is [qnm-node](https://github.com/AzielEliab/qnm-node); runtime cites live in [aziel-runtime](https://github.com/AzielEliab/aziel-runtime). Not a Softwares-tab product.

Counted download (gzip HTTP 200, no 302): https://miragegrid-download-tracker.vibelock.workers.dev/download?asset=miragegrid-0.2.0.tar.gz
GitHub: https://github.com/AzielEliab/miragegrid
