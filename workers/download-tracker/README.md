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
GET `/cite.json` citation record plus Cap-7 SEMANTIC-BRIDGE-1.0 section (`design_of` + `resolves_to_hub:false`). No invented Zenodo DOI.
GET `/llms.txt` and `/ai.txt` Growth-ON agent maps (HTTP 200). `public_icann:false`.
GET `/bridge.json` and `/v1/bridge` honest Cap-7 JSON map. Mesh name ≠ new product: relocatable labels of the four online hubs. Each entry has `canonical_hub`, `tip`, `public_icann:false`, `name_may_change:true`, `design_of`. Named mesh sites azcorpus + azlibrary listed as designs (hash-absolute `GET /design-packs/{label}.json`). Empty Cap-7 claims → SLOT. `canonical_hub` / `design_of` is hub design provenance only; `resolves_to_hub` is false. Mesh names do not CNAME/redirect to azieleliab.com / corpus / godlock / HDJ.
GET `/shelves` cites https://www.azielcorpuslibrary.net/shelves (COLD-MULTI-SHELF-1.0). Framagit URL is null — not invented.
Live host only: `https://miragegrid-download-tracker.vibelock.workers.dev`. Named `https://miragegrid.vibelock.workers.dev` is Cloudflare 1042 (not deployed) — do not cite.
REDLINE-1.0: GET never enables radios or plants Cap-7 claims. AZ Generator is not callable. Fake ICANN publish refuses. `resolves_to_hub: true` refuses.
`/v1/mesh/*` PROXY to aziel-runtime suite mesh (`AZIEL_RUNTIME` / `https://aziel-runtime.vibelock.workers.dev`). Default OFF. QNM-BUILD-1.0 live|locked|isolated. QNS-CD-1.0 (photon QNS1 packet transfer) is a hub cite / Worker mesh cross-map only — local qnsd in [qnm-node](https://github.com/AzielEliab/qnm-node), runtime cites in [aziel-runtime](https://github.com/AzielEliab/aziel-runtime). No Node Gate. No public qnsd proxy. No auto-heal. Not anonymity. Locked law: **SPLIT THE WIRES** (tip tick = presence+hash; payload pull-only; 777s dwell on a separate socket), **COLD-COPY SURVIVAL**, **REHEAL** (own tip+trusted pull or phoenix-WAIT; no neighbor talk-dirty-back-to-health; no bodies/diffs/vote-to-fix), **AZ-GENERATOR-1.0** (Cap-7 mesh DNS factory; deep-node → FRONT Node Gate; not callable; `.az` → `.aziel` → pivot; exactly 2 public gateways; AZNet+AZBrowser; ≥49 vault; vault multiply as cold copies; not ICANN), **MIRAGE-GRID-SHIFT-1.0** (MESH-VAULT snapshot+standby; cloak burst; Node Gate is MirageGrid `.az` only), **AIRGAP-1.0** (local vault; no bearer radios; no climb-back; official hubs are not airgap Node Gate). Public-stack auto-heal means lawful REHEAL-1.0 / MESH-REHEAL, not vote-to-fix. **NO-FAN-1.0:** No falsification. No ambiguity. No misleading. Beside NO-LIE / NO-REWRITE. AZ Generator and Node Gate are not Softwares-tab products. Hosted `/v1/mesh/vpn`, `/hop`, `/tunnel` refuse `MESH-STUB`. Assign stays live. Human UI Live Nodes strip polls `GET /v1/mesh`. Product topology is `GET /v1/topology`.

Verify: `curl -sS -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/mesh/status` returns MESH-OK style JSON with `enabled: false` by default.

Host: https://miragegrid-download-tracker.vibelock.workers.dev
