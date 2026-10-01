# MG-EGRESS-1.0 — Cap-7 geo, sticky mesh, land rotate

**Author:** Aziel Eliab only  
**Status:** Control plane LIVE (package 0.3.0). Not a public egress IP.  
**Not a Softwares-tab product of its own.** It is a MirageGrid surface.

anyIP-style questions (geo target, sticky session, IP rotation) map to
MirageGrid. This paper says what that mapping is allowed to claim.

## LIVE on the Cap-7 plane

| Surface | What it does |
| --- | --- |
| `POST /v1/egress/geo` and `POST /v1/geo-target` | Records a region label. Stable hash picks a mesh node and a Cap-7 land. Receipt over that node. `ip_exit: false`. Code `MG-GEO-TARGET`. |
| `POST /v1/session/sticky`, `POST /v1/session-stick`, `POST /v1/egress/sticky` | Same `sticky_key` selects the same mesh node and the same Cap-7 site. Vector without a TTL: `booth-1` → `node-21`. A `ttl_seconds` value (60..86400) folds `floor(unix/ttl)` into the digest. Code `MG-SESSION-STICK`. |
| `POST /v1/egress/rotate` and `POST /v1/egress-rotate` | Moves the factory land to the next roster label (`from_label`) or a seed hash. Update URL stays this Worker. Code `MG-EGRESS-ROTATE`. `ip_rotated: false`. |
| `POST /v1/assign` | Fresh circuit, unless `sticky_key` binds the node. A region label is stamped when present. |
| FragGate names | `geo-target`, `session-stick`, `egress-rotate` are LIVE on the Cap-7 control plane and on runtime Softwares `public_door_ops`. This Worker executes the HTTP doors. |

The Cap-7 shift stack is `staticlock`, `miragegrid-cloak`, `cap7-egress`
(former label `planned-egress`). `cap7-egress` is `status: live` and
`hosted: true`. It rotates a land label. AZVPN (`slug: azvpn`) is a
different product.

## What “sticky IP” means here

The path `POST /v1/egress/sticky` is the session/land stick. It does
**not** allocate a public address. `sticky_public_ip` stays false.
`egress_ip` stays null. A caller-supplied address, `residential`,
`socks`, or a Cloudflare geo-exit flag refuses `MG-NO-IP-EXIT`.

IP exit and a geo-exit pool stay on AZVPN, or on a future Cloudflare
egress binding this Worker does not claim. MirageGrid does not host a
VPN exit.

## Still refuse

| Ask | Code | Why |
| --- | --- | --- |
| Public egress IP, sticky address, residential, SOCKS, CF geo pool | `MG-NO-IP-EXIT` | Not hosted. The control plane does not invent one. |
| `vpn` / `hop` / `tunnel` on assign | `MG-NOT-VPN` | Hosted MirageGrid is not a VPN. Cap-7 land hop is `egress-rotate`. |
| Caller `endpoints` | `MG-NO-EGRESS-PAINT` | Listen addresses stay loopback defaults. |
| `hops` outside 1..25 | `MG-BAD-HOPS` | Matches the selector. |
| TTL outside 60..86400 | `MG-BAD-TTL` | A bad window is not silently ignored. |
| Missing `sticky_key` when sticking | `MG-STICKY-NEED-KEY` | A stick needs a key. |
| Malformed JSON | `MG-BAD-JSON` | A bad body is not an empty success. |

`MG-GEO-NOT-READY`, `MG-STICKY-IP-NOT-READY`, `MG-EGRESS-IP-NOT-READY`,
and `MG-STICKY-TTL-NOT-READY` are retired. Those doors return 200 for
the control-plane ask.

FragGate stub ops stay stub: `vpn-hop`, `hop`, `tunnel`, `mesh`.
WireGuard, OpenVPN, and L3 exit stay false. `planned.softwares_catalog_live` is true because runtime Softwares already lists geo-target, session-stick, and egress-rotate. Packet-hop stubs stay stubs. Cap-7 is not an ICANN registrar. AZVPN is not MirageGrid.

## TTL without a session store

The TTL is a time-bucket hash, not a Workers KV session. Same key inside
one window returns the same node id, the same Cap-7 land, and the same
`stick_id`. The next window is a different digest. `durable_store` is
false. That is enforcement, not an ignored expiry.

## GitBaby / AZBot

Runtime Softwares already lists `geo-target`, `session-stick`, and `egress-rotate` on `public_door_ops`. This repo’s health shows the same three ops `live: true` and `planned.softwares_catalog_live: true`. Do not unstub `vpn-hop`, `hop`, `tunnel`, or `mesh`. Do not merge MirageGrid into AZVPN. Do not enable `GET /v1/mesh` radios. Do not invent a Zenodo DOI. Do not claim ICANN publish. Do not claim a public egress IP.

Identity: **Aziel Eliab** only.
