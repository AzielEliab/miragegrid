---
name: MirageGrid
description: Use when calling MirageGrid hosted /v1 or installing the local package. Dual surface: Worker /v1 + catalog MCP. This Worker /v1/mesh/* PROXY to aziel-runtime via AZIEL_RUNTIME. Suite mesh default OFF. QNM-BUILD-1.0 live|locked|isolated. QNS-CD-1.0 photon QNS1 packet transfer is a hub cite / Worker mesh cross-map only (qnm-node qnsd + aziel-runtime catalog). No Node Gate. No public qnsd proxy. No auto-heal. Not anonymity. Hosted MirageGrid is not a VPN. Author Aziel Eliab.
---

# MirageGrid

Ephemeral session node assignment. 25 named peers. Receipts. Author: **Aziel Eliab**.

**THIS IS:** a session assignment engine (mesh maps, circuit hops, internal receipts).

**THIS IS NOT:** a VPN, an anonymity network, a hosted hop, a crime tool, a log-wipe, or a guarantee against global surveillance. Hosted `/v1` does not increment downloads or views.

Always send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.

## Call these URLs

- Worker OpenAPI: https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- Live skill (this markdown): `GET https://miragegrid-download-tracker.vibelock.workers.dev/v1/skill`

Ops (do **not** increment downloads or views):

- `GET /v1/health` — liveness
- `GET /v1/skill` — this file
- `GET /v1/topology` — persistent 25-node circulant topology (local op)
- `GET /v1/mesh` — PROXY suite mesh status. Default OFF. QNM live|locked|isolated. QNS-CD-1.0 cross-map (photon QNS1 packet transfer) is stamped for peers. Never enables. No public qnsd proxy.
- `GET /v1/mesh/nodes` — PROXY Live Nodes roster (5-minute presence). Same QNS-CD-1.0 cross-map.
- `POST /v1/mesh/{enable,disable,join,heartbeat,leave,broadcast}` — PROXY. Bearer required to enable. No auto-heal. Anon-broadcast is not a publish path.
- `POST /v1/route` — peer path
- `POST /v1/assign` — session circuit
- Product POSTs listed in OpenAPI

Works with any OpenAPI- or MCP-capable assistant: ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants.

Import notes: ChatGPT — GPT Actions (OpenAPI URL). Grok — custom tool from OpenAPI. Venice — HTTP tools. Cursor / Glama — MCP catalog. Claude and other OpenAPI/MCP clients — same OpenAPI document or MCP catalog.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/mesh
curl -s -A 'Mozilla/5.0' -X POST https://miragegrid-download-tracker.vibelock.workers.dev/v1/assign \
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
