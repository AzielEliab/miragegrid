---
name: MirageGrid
description: Use when calling MirageGrid hosted /v1 or installing the local package. Author Aziel Eliab.
---

# MirageGrid

Distributed identity abstraction. 25 logical nodes. Not a VPN. Author: **Aziel Eliab**.

**THIS IS:** a distributed identity abstraction (25 logical nodes, cryptographic sessions).

**THIS IS NOT:** a VPN, Tor, anonymous relay, or untraceable-origin system. Hosted `/v1` does not increment downloads or views.

Always send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.

## Call these URLs

- Worker OpenAPI: https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- Live skill (this markdown): `GET https://miragegrid-download-tracker.vibelock.workers.dev/v1/skill`

Ops (do **not** increment downloads or views):

- `GET /v1/health` — liveness
- `GET /v1/skill` — this file
- Product POSTs listed in OpenAPI

Grok: import OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/skill
```

## Local (after one-click install)

```bash
curl -fsSL https://miragegrid-download-tracker.vibelock.workers.dev/install.sh | bash
miragegrid ui
miragegrid doctor
```

Then open http://127.0.0.1:8080 (loopback only).

Counted download (gzip HTTP 200, no 302): https://miragegrid-download-tracker.vibelock.workers.dev/download?asset=miragegrid-0.1.0.tar.gz
GitHub: https://github.com/AzielEliab/miragegrid

## Catalog + local UI

Author: **Aziel Eliab**. Honest scope: Ephemeral session node assignment. Not a VPN and not an anonymity network.

- Catalog product: https://aziel-runtime.vibelock.workers.dev/p/miragegrid/
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- This Worker skill: `GET https://miragegrid-download-tracker.vibelock.workers.dev/v1/skill`
- This Worker OpenAPI: https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json
- Sample payload: `GET https://miragegrid-download-tracker.vibelock.workers.dev/v1/example`

Local UI: **Import JSON file** (`type=file`) and **Export JSON**. Then `miragegrid doctor`.

Grok: import catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.
