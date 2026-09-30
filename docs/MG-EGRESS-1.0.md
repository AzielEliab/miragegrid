# MG-EGRESS-1.0 — geo, sticky session, egress (honest slice)

**Author:** Aziel Eliab only  
**Status:** First adaptation slice. Refuse-until-ready except one real label.  
**Not a Softwares-tab product of its own.** It is a MirageGrid surface.

anyIP-style questions (geo target, sticky session, IP rotation) map to
MirageGrid. This paper says what that mapping is allowed to claim.

## Live today

| Surface | What it does |
| --- | --- |
| `POST /v1/assign` | Fresh mesh node label `node-01` … `node-25`, circuit cite, receipt over the **entry node** only. Listen targets stay `127.0.0.1`. |
| `POST /v1/session/sticky` | `SHA-256("mg-sticky-v1\|" + sticky_key) mod 25`. Same key, same label. Vector: `booth-1` → `node-21`. Receipt session id is fresh. No circuit. |
| Cap-7 shuffle | Factory cite/land. Not ICANN `.az`. Update URL does not change per land label. |
| FragGate `assign` | Still the catalog live op. |

The Cap-7 shift stack is `staticlock`, `miragegrid-cloak`, `planned-egress`.
`planned-egress` is `status: planned` and `hosted: false`. AZVPN (`slug: azvpn`)
is a different product. Cap-7 JSON does not carry a VPN shift-stack label.

## Refuse until a real pool exists

| Ask | Code | Why |
| --- | --- | --- |
| Country, city, region, ASN | `MG-GEO-NOT-READY` | No geo pool. No exit address is chosen. |
| Sticky public IP | `MG-STICKY-IP-NOT-READY` | A mesh label is not an address. |
| Rotate / residential / proxy / SOCKS egress | `MG-EGRESS-IP-NOT-READY` | Nothing to rotate. |
| TTL on a sticky key | `MG-STICKY-TTL-NOT-READY` | No session store. Ignoring the expiry would be a lie. |
| Caller `endpoints` | `MG-NO-EGRESS-PAINT` | Callers cannot write listen addresses onto the pool. |
| `vpn` / `hop` / `tunnel` on assign | `MG-NOT-VPN` | Hosted MirageGrid is not a VPN. |
| `hops` outside 1..25 | `MG-BAD-HOPS` | Matches the local selector. Stops a 500. |
| Malformed JSON | `MG-BAD-JSON` | A bad body is not an empty success. |

These doors do not mint a receipt and do not return `node_id`.

FragGate stub ops stay stub: `vpn-hop`, `hop`, `tunnel`, `mesh`.
This slice does not add catalog LIVE_OPS.

## Still planned

- A real egress pool (addresses that exist, with a geo attribute that was measured).
- Durable sticky sessions with an enforced TTL (needs a store; not an in-memory isolate map).
- Per-land update hosts. Today every land cites the same app Worker URL.
- Attested `prev|lockset` (ChainLock / zkattest). Syntactic proof only today.

## GitBaby / AZBot

No runtime catalog PR is required for this slice. Leave the Softwares
`one_line` as: assign a short-lived session node and cite mesh-name
metadata. Do not rewrite it to claim residential geo, sticky IPs, or
egress rotation. Do not unstub `vpn-hop`, `hop`, `tunnel`, or `mesh`.
Do not merge MirageGrid into AZVPN. Do not enable `GET /v1/mesh` radios.
Do not invent a Zenodo DOI.

Identity: **Aziel Eliab** only.
