# SIDENET P2

**Author:** Aziel Eliab only  
**Status:** Locked design law  
**Softwares-tab:** no — sidenet is a MirageGrid subsystem, not a new product  
**Cites:** AZ-GENERATOR-1.0 · CAP7-SHUFFLE-1.0 · AZNet AZN-WP-0.1 · NO-LIE · NO-FAN-1.0

Two layers. They do not replace each other.

| Layer | Plane | What it is |
| --- | --- | --- |
| L0 | public path | AZ-domain doors and the existing public Cap-7 cite. Unchanged. |
| P2 | sidenet | Cap-7 mesh DNS plus AZNet + AZBrowser pairing. |

## Factory

MirageGrid is the Cap-7 mesh DNS factory. It is not an ICANN registrar.

- `public_icann: false`
- `typed_on_icann_dns: false`
- AZ Generator stays deep in the node. Outside calls refuse `AZG-NOT-CALLABLE`.
- Exit is the front Node Gate: claim, plant, flag, restore.
- Hosted Worker cites those actions and does not execute them.
- Incomplete vault and a fake flag still refuse. Do not invent a tip.

## Two public browser gateways

Exactly two Cap-7 factory labels are public browser gateways:

- `azgrid`
- `azbooth`

A standard browser may cite those two. They are still not ICANN names
(`public_icann: false`, `internet_reachable: false` on the mesh name).
The other five factory names stay on the sidenet. A browser that asks
for one of them refuses `AZG-PUBLIC-PAIR`.

## Pairing

AZNet and AZBrowser stay separate Softwares. Access to a mesh name on
P2 needs both:

1. a pairing token (a boolean word is not a token)
2. an `azbrowser` flag

Missing either refuses `SIDENET-NEED-PAIR`. Present both admits
`SIDENET-PAIR-OK` with `pair_verified_at_aznet: false`. This surface
does not verify the token at AZNet. Pairing is not a tunnel
(`CAP7-NO-VPN-LIE`). Pairing does not host payloads
(`SIDENET-NO-PAYLOAD-HOST`). Merging the products refuses
`AZG-NO-MERGE-PRODUCTS`. Asking for a new Softwares product refuses
`SIDENET-SOFTWARE-FROZEN`.

Official hub hostnames stay on L0. They are not Node Gate.

## Where it runs

- Local: `miragegrid/sidenet.py`
- App Worker cite: `GET /v1/sidenet` on `miragegrid.vibelock.workers.dev`
- App Worker check: `POST /v1/sidenet/access`

GET never plants a claim.
