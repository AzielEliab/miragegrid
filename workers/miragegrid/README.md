# miragegrid app Worker

Named Cloudflare Worker **`miragegrid`**. Host
`https://miragegrid.vibelock.workers.dev`.

This is the **Cap-7 LIVE shuffle** app door (names plane / control plane; `public_icann: false`; not an ICANN DNS publish). It is **not** the
download-tracker. Counted downloads stay on
`miragegrid-download-tracker`.

Historical CF **1042** (Worker name missing / account 10007) is closed
by deploying Worker **name=`miragegrid`**. Not the download-tracker.

```bash
cd workers/miragegrid
npm run deploy
# package.json deploy (CI assert): wrangler deploy --name miragegrid --config wrangler.jsonc
# stamped operator path: bash deploy.sh
```

`wrangler.jsonc` `name` is **`miragegrid`** on account
`ac575a9b822bea2bed97d0ab73aed238` (`workers_dev = true` →
`https://miragegrid.vibelock.workers.dev`). After deploy:

```bash
curl -sS -A 'Mozilla/5.0' https://miragegrid.vibelock.workers.dev/v1/health
# expect worker_name=miragegrid  — CF 1042 is gone
# tip and git_sha: deploy stamp (null until GIT_SHA or WORKERS_CI_COMMIT_SHA is injected)
# version_id: CF_VERSION_METADATA.id at serve time (null when the binding is absent)
# cap7_operator_hold: false
# cap7_live / cap7_factory_live: true (mesh DNS factory and control plane active for operators)
# cap7_registrar_live / paid_registrar / public_icann: false
# cap7_names_only: true (names-only ≠ ICANN). No domain spend. No IP egress.
# Softwares Cap-7 active-use is not vendored. CLEARED pin 6f27394fbcafb640a1ede7017b599a6f66c68769 stays geo-target / session-stick / egress-rotate.
```

`npm run deploy` stays `wrangler deploy --name miragegrid --config wrangler.jsonc`. That string is what `test_app_worker_wrangler_named_miragegrid` asserts. It does not pass `GIT_SHA`. `bash deploy.sh` is the stamped operator path: it sets `GIT_SHA=$(git rev-parse HEAD)` as a wrangler var and bakes the same commit. Workers Builds does not need that flag: `build.command` reads `WORKERS_CI_COMMIT_SHA` during either deploy. Neither path hardcodes a tip.

## LIVE doors (aziel-runtime cite)

| Path | Honesty |
| --- | --- |
| `GET /mcp` | Public cite map on this Worker. **Not** FragGate JSON-RPC exec (catalog stays on AZ runtime `/mcp`). Factory active (`cap7_live`, `cap7_factory_live`). Register **free-only** (no paid ICANN/.az). |
| `GET /land` `POST /land` | Cap-7 shuffle land cite (alias of `/v1/shuffle/land`). Factory active; this path still cites. `public_shuffle_land_exec` false. GET `prev`+`lockset` refuses. Not an ICANN DNS publish. |
| `GET /attest` `POST /attest` | Attest cite + syntactic `prev`/`lockset` check. Factory active. ChainLock / zkattest SLOT (F1). Not an ICANN registrar. |
| `GET /` | App homepage (shuffle + assign) |
| `GET /bridge` `/bridge.json` `/v1/bridge` | Cap-7 shuffle + SEMANTIC-BRIDGE map |
| `GET /v1/shuffle` | Cite CAP7-SHUFFLE-1.0 |
| `POST /v1/shuffle/ping` | Node ping → land |
| `GET /v1/shuffle/land?round_id=` | Cite land for a round (GET never plants) |
| `POST /v1/shuffle/update` | Third hop: update via the landed Cap-7 site (GET 403) |
| `GET /v1/cap7` | Seven factory sites: four hub mirrors, three decoys. Factory active for operators. Not an ICANN registrar. No domain spend. |
| `GET /v1/planned` | geo-target, session-stick, egress-rotate. LIVE control plane. Not a public egress IP. Not a packet hop |
| `POST /v1/egress/geo` `/v1/geo-target` | LIVE region label. `ip_exit: false` |
| `POST /v1/session/sticky` `/v1/session-stick` `/v1/egress/sticky` | LIVE sticky mesh + Cap-7 land. Not a sticky public IP |
| `POST /v1/egress/rotate` `/v1/egress-rotate` | LIVE land rotation among the seven sites. Not packet egress |
| `GET /cap7/{label}` | LIVE factory cite. Not typed on ICANN DNS |
| `GET /aznet/cap7/{label}` | AZnet-plane factory cite (LIVE). Not a public internet door |
| `GET /v1/health` | Liveness plus deploy `tip` / `git_sha` and Cloudflare `version_id`. `cap7_live` and `cap7_factory_live` true. `cap7_registrar_live`, `paid_registrar`, and `public_icann` false. `cap7_names_only` true. |
| `GET /v1/skill` `/v1/nodes` `/v1/doctor` | FragGate LIVE_OPS |
| `POST /v1/assign` `/v1/verify-receipt` | Session assignment |
| `GET /v1/mesh` | PROXY. Node mesh ON (`mesh_node_live`, `alt_internet`, `packet_path`). GET never enables radios. Cap-7 stays names-only. |

AZ Generator is not callable. Cap-7 `public_icann: false` and
`typed_on_icann_dns: false`. AZ domain doors are `public_icann: true`
and `resolves_to_hub: true`. `radio_phy: false`. No hard-coded Cap-7 host.
Factory honesty is LIVE. Live nodes anchor the factory and the AZ doors.
The seven factory names are separate from per-node `.aziel` slots.
Not a VPN. Not an anonymity network. Not AZVPN. `packet_forwarding: false`.
geo-target, session-stick, and egress-rotate are LIVE on the Cap-7 control plane (region label, sticky mesh, land rotate). Not a public egress IP. Not a Cloudflare geo-exit pool.

Author: Aziel Eliab only.
