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

Host: https://miragegrid-download-tracker.vibelock.workers.dev
