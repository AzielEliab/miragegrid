# miragegrid app Worker

Named Cloudflare Worker **`miragegrid`**. Host
`https://miragegrid.vibelock.workers.dev`.

This is the **Cap-7 LIVE shuffle** app door. It is **not** the
download-tracker. Counted downloads stay on
`miragegrid-download-tracker`.

Historical CF **1042** (Worker name missing / account 10007) is closed
by deploying Worker **name=`miragegrid`**. Not the download-tracker.

```bash
cd workers/miragegrid
npx wrangler deploy --name miragegrid --config wrangler.jsonc
# or: bash deploy.sh
```

`wrangler.jsonc` `name` is **`miragegrid`** on account
`ac575a9b822bea2bed97d0ab73aed238` (`workers_dev = true` →
`https://miragegrid.vibelock.workers.dev`). After deploy:

```bash
curl -sS -A 'Mozilla/5.0' https://miragegrid.vibelock.workers.dev/v1/health
# expect worker_name=miragegrid  — CF 1042 is gone
```

## LIVE doors (aziel-runtime cite)

| Path | Honesty |
| --- | --- |
| `GET /` | App homepage (shuffle + assign) |
| `GET /bridge` `/bridge.json` `/v1/bridge` | Cap-7 shuffle + SEMANTIC-BRIDGE map |
| `GET /v1/shuffle` | Cite CAP7-SHUFFLE-1.0 |
| `POST /v1/shuffle/ping` | Node ping → land |
| `GET /v1/shuffle/land?round_id=` | Cite land for a round (GET never plants) |
| `POST /v1/shuffle/update` | Third hop: update via the landed Cap-7 site (GET 403) |
| `GET /v1/cap7` | Seven factory sites: four real hub duplications, three false sites, honesty LIVE |
| `GET /cap7/{label}` | LIVE factory cite. Not typed on ICANN DNS |
| `GET /aznet/cap7/{label}` | AZNet-plane factory cite (LIVE). Not a public internet door |
| `GET /v1/health` `/v1/skill` `/v1/nodes` `/v1/doctor` | FragGate LIVE_OPS |
| `POST /v1/assign` `/v1/verify-receipt` | Session assignment |
| `GET /v1/mesh` | PROXY (default OFF). GET never enables. |

AZ Generator is not callable. Cap-7 `public_icann: false` and
`typed_on_icann_dns: false`. AZ domain doors are `public_icann: true`
and `resolves_to_hub: true`. `radio_phy: false`. No hard-coded Cap-7 host.
Factory honesty is LIVE. Live nodes anchor the factory and the AZ doors.

Author: Aziel Eliab only.
