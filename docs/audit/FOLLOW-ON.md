# Cap-7 / MirageGrid security follow-on

**Author:** Aziel Eliab only  
**Not this PR.** Large or cross-repo work after the 2026-09-18 audit.

FragGate stays THE door. Do not add a second exec path, an unmarked hydra, or a fake Cap-7 `/mcp`.

| ID | Work | Why later |
| --- | --- | --- |
| F1 | Attest update proof: `lockset` must verify against ChainLock / LOCKSET / FragGate `zkattest`. Replay window. | Needs runtime attest + node keying. No Worker theater crypto. |
| F2 | Shrink `miragegrid-download-tracker` to counted `/download` + semantic-bridge cite. Move assign/mesh PROXY solely to Worker `miragegrid`. | Cross-cutting OpenAPI / homepage / SKILL. |
| F3 | aziel-runtime BAN-SURVIVAL-1.0 §6c: name the **named** app Worker as LIVE **cite/land** (not `/mcp`). Keep AZNet-side hosted update SLOT. Keep `BAN-NO-FAKE-CAP7-HOST`. | Runtime paper is stale vs product #15. |
| F4 | AZNet `stamp` binds a Cap-7 **factory label** (design DNA only) to an attested named FragGate origin before any hosted-endpoint flip. | BAN-SURVIVAL `BAN-CAP7-HOST-NOT-ATTESTED`. Security audit first (this PR). |
| F5 | Rate-limit `POST /v1/shuffle/ping` and `/update` (and remaining `/event`) at the Worker. | Needs CF rate-limit / Durable Object; not an obvious one-file fix. |
| F6 | Shared Python/JS land helper published as one golden vector file (all 7 labels hit). | Nice-to-have after BigInt fix. |
| F7 | CORS allowlist for mesh enable if a browser credential flow is added. | None today. |
| F8 | Live-node API remains SLOT until a node publishes named origin + FragGate-only exec + digest + same hop strip (`BAN-NO-OPEN-NODE-PROXY`). | Runtime follow-on, not this repo. |

Identity: **Aziel Eliab** only.
