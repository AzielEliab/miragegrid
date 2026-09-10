# miragegrid download tracker

Isolated Worker `miragegrid-download-tracker`. Project `miragegrid`.
KV namespace `MIRAGEGRID_DOWNLOADS` bound as `DOWNLOADS`.
Does **not** 302 to GitHub on `/download`. Serves gzip via `ASSETS.fetch`,
`Cache-Control: private, no-store`.

`GET /` is the **product homepage** (workspace + download/install + cite).
Hosted `/v1` is session assignment (assign / mesh / route / circuit /
receipt). MirageGrid is **not** a VPN and not an anonymity network.

GET `/` increments a **page-view** counter (separate from downloads).
GET `/download` increments **downloads**.
`/v1` never increments DOWNLOADS KV.
GET `/install.sh` one-click install (does not increment; script curls `/download`).
GET `/v1/skill` returns skill markdown (`text/markdown`). Does not increment views or downloads.
GET `/cite.json` citation record. No invented Zenodo DOI.
`/v1/mesh/*` PROXY to aziel-runtime suite mesh (`AZIEL_RUNTIME` / `https://aziel-runtime.vibelock.workers.dev`). Default OFF. QNM-BUILD-1.0 live|locked|isolated. No Node Gate. No auto-heal. Not anonymity. Human UI Live Nodes strip polls `GET /v1/mesh`. Product topology is `GET /v1/topology`.

Verify: `curl -sS -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/mesh/status` returns MESH-OK style JSON with `enabled: false` by default.

Host: https://miragegrid-download-tracker.vibelock.workers.dev
