# MirageGrid download tracker (Cloudflare Worker)

Counts GitHub-release downloads for MirageGrid across the canonical
repository, other branches, and forks. Forks are identified by GitHub
`owner/repo`.

**This worker must be deployed** before
`https://miragegrid-download-tracker.vibelock.workers.dev` resolves.
Until then, send people to
[GitHub Releases](https://github.com/AzielEliab/miragegrid/releases).

No secrets belong in this directory. The KV namespace id in
`wrangler.toml` is the placeholder `REPLACE_ME` until you create a
namespace.

This tree is shipped **undeployed**. Do not treat the workers.dev URL
as live until someone with the Cloudflare account runs the steps below.
Do not deploy from this tree until KV is a real id.

The homepage shows a **live download count for MirageGrid only**. The
counter is isolated to this project (its own Worker + KV), not VibeLock.
`GET /download` increments. `GET /count` returns `{project, total}`.

MirageGrid is an assignment + receipt engine. It is not a VPN, proxy
mesh, or anonymity network.

## Bindings

| Binding     | Type | Purpose |
|-------------|------|---------|
| `DOWNLOADS` | KV   | Counters keyed `project|owner|repo|branch|fork` |

## Deploy

```bash
cd workers/download-tracker

# 1. Log in once (opens a browser; token stays in wrangler, not in git)
npx wrangler login

# 2. Create the KV namespace. Paste the id into wrangler.toml
#    replacing REPLACE_ME. Binding name MUST stay DOWNLOADS.
npx wrangler kv namespace create DOWNLOADS

# 3. Deploy
npx wrangler deploy
```

The `workers.dev` subdomain wrangler prints
(`miragegrid-download-tracker.<account>.workers.dev`) is enough until
custom DNS is ready. This tree documents the intended public URL
`https://miragegrid-download-tracker.vibelock.workers.dev`.

## Routes

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/` | Index page with live count and the download link |
| GET | `/download?repo=&tag=&asset=` | Increment KV, 302 to the hosted asset (default: `miragegrid-0.1.0.tar.gz`) |
| GET | `/count` | JSON `{project, total}` for this project only |
| GET | `/stats` | JSON totals plus per-repo and per-branch breakdown |
| GET | `/go` | Increment KV, 302 to GitHub |

Query params on `/download`: `owner`, `repo` (`AzielEliab/miragegrid` is
accepted), `branch`, `fork` (`1` or `owner/repo`), `tag`, `asset`.

Default GitHub releases URL:

```
https://github.com/AzielEliab/miragegrid/releases
```

Tracked asset URL (after deploy):

```
https://miragegrid-download-tracker.vibelock.workers.dev/download?asset=miragegrid-0.1.0.tar.gz
```

## Stats

`GET /stats` returns `total`, `by_repo`, `by_branch`, `by_fork`, and a
`breakdown` array. `GET /count` is the short form `{project, total}`.

## CORS

All responses include `Access-Control-Allow-Origin: *`.

## Use with Grok, ChatGPT, Venice

This Worker now also hosts the product runtime API. `/v1` calls never increment DOWNLOADS KV.

- OpenAPI: `https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json`
- Health: `GET /v1/health` → `{ok, product, version:"0.1.0"}`
- Setup HTML: `GET /ai` (ChatGPT Actions, Grok/xAI custom tool, Venice custom HTTP; MCP catalog `https://aziel-runtime.vibelock.workers.dev/mcp`)

CORS `*` on API routes.
