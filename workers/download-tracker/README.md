# miragegrid download tracker

Isolated Worker `miragegrid-download-tracker`. Project `miragegrid`.
KV namespace `MIRAGEGRID_DOWNLOADS` bound as `DOWNLOADS`.
Does **not** 302 to GitHub on `/download`. Serves gzip via `ASSETS.fetch`,
`Cache-Control: private, no-store`.

Hosted `/v1` is the mesh-VPN control plane (assign / mesh / route /
circuit / receipt). Isolated from VibeLock.

GET `/` increments a **page-view** counter (separate from downloads).
GET `/download` increments **downloads**.
`/v1` never increments DOWNLOADS KV.
GET `/install.sh` one-click install (does not increment; script curls `/download`).
GET `/v1/skill` returns skill markdown (`text/markdown`). Does not increment views or downloads.

Host: https://miragegrid-download-tracker.vibelock.workers.dev
