# miragegrid app Worker

Named Cloudflare Worker **`miragegrid`**. Host
`https://miragegrid.vibelock.workers.dev`.

This is the **Cap-7 LIVE shuffle** app door. It is **not** the
download-tracker. Counted downloads stay on
`miragegrid-download-tracker`.

Historical CF **1042** (Worker name missing / account 10007) is closed
by deploying this Worker:

```bash
cd workers/miragegrid
npx wrangler deploy
```

`wrangler.jsonc` `name` is `miragegrid` on account
`ac575a9b822bea2bed97d0ab73aed238` (`workers_dev = true` →
`miragegrid.vibelock.workers.dev`).

## LIVE doors (aziel-runtime cite)

| Path | Honesty |
| --- | --- |
| `GET /` | App homepage (shuffle + assign) |
| `GET /bridge` `/bridge.json` `/v1/bridge` | Cap-7 shuffle + SEMANTIC-BRIDGE map |
| `GET /v1/shuffle` | Cite CAP7-SHUFFLE-1.0 |
| `POST /v1/shuffle/ping` | Node ping → land |
| `GET /v1/shuffle/land?round_id=` | Cite land for a round (GET never plants) |
| `GET /v1/cap7` | Seven factory sites, SLOT vs LIVE |
| `GET /cap7/azgrid` `/cap7/azbooth` | Public pair **LIVE** HTTPS mirrors |
| `GET /aznet/cap7/{label}` | AZNet-side cite (**SLOT** on public HTTPS) |
| `GET /v1/health` `/v1/skill` `/v1/nodes` `/v1/doctor` | FragGate LIVE_OPS |
| `POST /v1/assign` `/v1/verify-receipt` | Session assignment |
| `GET /v1/mesh` | PROXY (default OFF). GET never enables. |

AZ Generator is not callable. `public_icann: false`.
`resolves_to_hub: false`. `radio_phy: false`. No hard-coded Cap-7 host.

Author: Aziel Eliab only.
