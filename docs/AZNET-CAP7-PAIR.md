# AZNet pairing (naming lock)

**Author:** Aziel Eliab only  
**Status:** Locked design law  
**Naming lock:** sidenet = AZNet  
**Softwares:** frozen — AZNet and AZBrowser already exist; this route adds none  
**Cites:** AZ-GENERATOR-1.0 · CAP7-SHUFFLE-1.0 · AZNet AZN-WP-0.1 · NO-LIE · NO-FAN-1.0

Sidenet is not a second product and not a second plane. The name is AZNet.
Cap-7 mesh DNS (MirageGrid) pairs with AZNet and AZBrowser. They stay
separate Softwares. `public_icann` stays false.

A request that uses the old path `/v1/sidenet` refuses `AZN-NAME-LOCK`.

## Layers

| Layer | Plane | What it is |
| --- | --- | --- |
| L0 | public path | AZ-domain doors and the existing public Cap-7 cite. Unchanged. |
| P2 | AZNet | Cap-7 mesh DNS paired with AZNet and AZBrowser. |

This Worker cites the pair. It does not run the AZNet engine (garden,
stamp, memorial). FragGate remains that door. `runs_aznet_engine: false`.

## Factory

MirageGrid is the Cap-7 mesh DNS factory. It is not an ICANN registrar.

- `public_icann: false`
- AZ Generator stays deep in the node. Outside calls refuse `AZG-NOT-CALLABLE`.
- Hosted claim / plant / flag / restore refuse.
- Exactly two public browser gateways: `azgrid` and `azbooth`.
- The other five factory names need an AZNet pairing token and an `azbrowser` flag.

## Pairing

Missing either piece refuses `AZN-NEED-PAIR`. Both present admits
`AZN-PAIR-OK` with `pair_verified_at_aznet: false`. Pairing is not a
tunnel. Pairing does not host payloads. Merging products refuses
`AZG-NO-MERGE-PRODUCTS`. A new Softwares product refuses
`AZN-SOFTWARE-FROZEN`.

## Where it runs

- Local: `miragegrid/sidenet.py` (module file; the public name is AZNet)
- Cite: `GET /v1/aznet`
- Check: `POST /v1/aznet/access`

GET never plants a claim.
