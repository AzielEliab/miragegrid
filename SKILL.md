---
name: MirageGrid
description: Use when calling MirageGrid hosted /v1 or installing the local package. Not a VPN. Author Aziel Eliab.
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
- `GET /v1/mesh` — persistent topology
- `POST /v1/route` — peer path
- `POST /v1/assign` — session circuit
- Product POSTs listed in OpenAPI

Grok: import OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' -X POST https://miragegrid-download-tracker.vibelock.workers.dev/v1/assign \
  -H 'content-type: application/json' -d '{}'
```

## Local (after one-click install)

```bash
curl -fsSL https://miragegrid-download-tracker.vibelock.workers.dev/install.sh | bash
miragegrid ui
miragegrid doctor
```

Then open http://127.0.0.1:8080 (loopback). Hosted MirageGrid is not a VPN.

Counted download (gzip HTTP 200, no 302): https://miragegrid-download-tracker.vibelock.workers.dev/download?asset=miragegrid-0.2.0.tar.gz
GitHub: https://github.com/AzielEliab/miragegrid
