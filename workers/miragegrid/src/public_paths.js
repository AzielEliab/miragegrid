/**
 * MirageGrid SHIP public paths: /mcp, /land, /attest.
 * Cite/coordination only — FragGate exec stays on aziel-runtime.
 * Cap-7 names-only ≠ ICANN. Author: Aziel Eliab only.
 */

import { APP_HOST, CAP7_SHUFFLE_SPEC, IDENTITY, RUNTIME, appWorker, hostedBridgeDoors } from "./cap7.js";
import { HASH_RECEIPT_CONTINUITY, SOFTWARES_COMPANION_TIP } from "../../download-tracker/src/mesh.js";
import { PRODUCT, VERSION } from "../../download-tracker/src/runtime.js";

const FRAGGATE_MCP = RUNTIME + "/mcp";
const ATTEST_SPEC = "MG-ATTEST-1.0";
const PUBLIC_MCP_SPEC = "MG-PUBLIC-MCP-1.0";

/**
 * Factory hold is off. Mesh DNS factory and control plane are active for operators.
 * Registrar meaning stays names-only ≠ ICANN. No paid registrar. No domain spend.
 * Not an ICANN DNS publish. Not a public egress IP.
 * Softwares Cap-7 active-use is not vendored here; the CLEARED pin stays the geo/stick/rotate companion.
 */
export function cap7OperatorHold() {
  return {
    cap7_operator_hold: false,
    cap7_active_use: true,
    cap7_active_use_means:
      "Mesh DNS factory and control plane are active for operators. Not an ICANN registrar, not a paid registrar, and not a public egress IP.",
    cap7_entity: "TBD",
    cap7_is_mesh_dns_factory: true,
    node_gate_claim_plant: "front-only-not-on-this-worker",
    domain_purchase: "held",
    domain_register: "free-only-if-ever",
    register_policy: "free-only",
    paid_registrar: false,
    icann_az_paid_registrar: false,
    registrar_work: "none",
    spend: "none",
    cap7_registrar_live: false,
    cap7_live: true,
    cap7_factory_live: true,
    cap7_names_only: true,
    cap7_names_are_not_icann: true,
    public_icann: false,
    public_icann_registrar: false,
    icann_dns_publish: false,
    cap7_public_icann: false,
    cap7_public_egress: false,
    public_egress_ip: false,
    packet_forwarding: false,
    ip_exit: false,
    softwares_cap7_active_use_companion:
      "Not vendored. A Softwares Cap-7 active-use PR may land first on aziel-runtime. This Worker does not pin a new tip for it. CLEARED companion pin " +
      SOFTWARES_COMPANION_TIP +
      " stays geo-target, session-stick, and egress-rotate only.",
    note:
      "Cap-7 mesh DNS factory and control plane are active for operators (cap7_operator_hold false). Names-only is not an ICANN or paid .az registrar. No domain spend on this Worker. cap7_registrar_live, paid_registrar, public_icann, and IP egress stay false. GET /v1/mesh never enables radios.",
  };
}

/** Public-path honesty. Factory active-use is on. This route still cites and does not publish ICANN DNS. GET never plants. */
export function publicPathCap7Honesty() {
  return {
    ...cap7OperatorHold(),
    public_icann: false,
    public_icann_registrar: false,
    typed_on_icann_dns: false,
    cap7_typed_on_icann_dns: false,
    factory_honesty: "cite",
    factory_honesty_live: false,
    factory_honesty_plane: "names-plane",
    factory_honesty_means: "public-path cite of Cap-7 names; not a public ICANN or DNS publish",
    cap7_hosted_endpoints: "cite",
    cap7_hosted_endpoints_plane: "names-plane",
    cap7_hosted_endpoints_means: "public-path cite; control-plane names only; not a public ICANN or DNS publish",
    icann_dns_publish: false,
    cap7_public_icann: false,
    cap7_public_egress: false,
    hosted_mcp: "cite",
    hosted_mcp_live: false,
    hosted_update: "cite",
    hosted_update_live: false,
    hosted_endpoints: "cite",
    hosted_endpoints_live: false,
    public_shuffle_land_exec: false,
    public_shuffle_land_exec_live: false,
    anchored_by_live_nodes: false,
    communication_plane: true,
    channel_plane_is_vpn: false,
    packet_forwarding: false,
    is_live_door: false,
    second_door: false,
    fraggate_single_door: true,
    open_proxy: false,
    hosted_vpn: false,
    azvpn: false,
  };
}

export function publicSurfaceDoors() {
  return {
    mcp: APP_HOST + "/mcp",
    land: APP_HOST + "/land",
    attest: APP_HOST + "/attest",
    bridge: APP_HOST + "/bridge",
    shuffle: APP_HOST + "/v1/shuffle",
    shuffle_land: APP_HOST + "/v1/shuffle/land",
    shuffle_ping: APP_HOST + "/v1/shuffle/ping",
    shuffle_update: APP_HOST + "/v1/shuffle/update",
    cap7: APP_HOST + "/v1/cap7",
    fraggate_catalog_mcp: FRAGGATE_MCP,
  };
}

export function mcpCite() {
  const bridge = hostedBridgeDoors();
  return {
    ok: true,
    code: "MG-PUBLIC-MCP-CITE",
    spec: PUBLIC_MCP_SPEC,
    product: PRODUCT,
    version: VERSION,
    worker_name: "miragegrid",
    role: "cap-7-shuffle-app",
    surface: "public-cite",
    hosted_mcp_means: "cite-json-on-this-worker-not-fraggate-exec",
    ...publicPathCap7Honesty(),
    second_door: false,
    fraggate_single_door: true,
    exec_door: "fraggate_call",
    fraggate_catalog: {
      url: FRAGGATE_MCP,
      method: "POST",
      note: "Full Softwares catalog + FragGate tools/list and fraggate_call live on the AZ runtime Worker. This MirageGrid app path is not that server.",
    },
    public_icann: false,
    typed_on_icann_dns: false,
    cap7_typed_on_icann_dns: false,
    public_icann_registrar: false,
    internet_reaches: "az-domains",
    name_may_change: true,
    doors: publicSurfaceDoors(),
    bridge_code: bridge.code,
    shuffle_spec: CAP7_SHUFFLE_SPEC,
    methods: {
      GET: "Return this cite JSON (application/json).",
      HEAD: "Same headers as GET without a body.",
      POST: "Refuse — cite-only; use the AZ runtime catalog MCP for JSON-RPC exec.",
      OPTIONS: "CORS preflight.",
    },
    note:
      "MirageGrid public /mcp is a hosted cite map for Cap-7 shuffle coordination. It is not a second FragGate door and does not publish Cap-7 factory labels on ICANN DNS. Exec stays POST " +
      FRAGGATE_MCP +
      " (slug miragegrid for in-process shuffle; catalog mesh_* elsewhere).",
    author: IDENTITY,
    identity: IDENTITY,
  };
}

export function mcpPostRefuse() {
  return {
    ok: false,
    code: "MG-MCP-CITE-ONLY",
    spec: PUBLIC_MCP_SPEC,
    verdict: "refuse",
    yes: false,
    message:
      "GET /mcp is the hosted public cite JSON on this app Worker (not FragGate exec). JSON-RPC exec is not hosted here. Use the AZ ecosystem FragGate catalog at " +
      FRAGGATE_MCP +
      ".",
    ...publicPathCap7Honesty(),
    fraggate_catalog_mcp: FRAGGATE_MCP,
    author: IDENTITY,
  };
}

export function attestCite() {
  return {
    ok: true,
    code: "MG-ATTEST-CITE",
    spec: ATTEST_SPEC,
    product: PRODUCT,
    version: VERSION,
    worker_name: "miragegrid",
    role: "cap-7-shuffle-app",
    ...publicPathCap7Honesty(),
    attest: {
      status: "syntactic-only",
      chainlock_verify: "SLOT",
      lockset_verify: "SLOT",
      fraggate_zkattest: "SLOT",
      replay_window: "SLOT",
      syntactic_only: true,
      worker_theater_crypto: false,
      follow_on: "docs/audit/FOLLOW-ON.md#f1",
    },
    update_proof: {
      fields: ["prev", "lockset"],
      meaning: "Non-empty prev and lockset hash to a Cap-7 land label for coordination. Same pair → same land.",
      not_claimed: "ChainLock tip binding, LOCKSET verify, node keying, or FragGate zkattest (not hosted on this Worker).",
    },
    hash_receipt: { ...HASH_RECEIPT_CONTINUITY },
    methods: {
      GET: "This cite.",
      POST: "Syntactic check: JSON {prev, lockset} required; returns land coordination + seed when both non-empty.",
      HEAD: "Headers only.",
    },
    doors: {
      attest: APP_HOST + "/attest",
      land: APP_HOST + "/land",
      update: APP_HOST + "/v1/shuffle/update",
      fraggate_verify: RUNTIME + "/v1/fraggate/call",
    },
    app_worker: appWorker(),
    note:
      "Honest attest on the MirageGrid app Worker: coordination proof only until runtime ChainLock/zkattest lands (F1). Ban-survival hash continuity remains AZNet verify via FragGate, not a second receipt door.",
    author: IDENTITY,
    identity: IDENTITY,
  };
}

export async function attestSyntactic(body, pingFn) {
  const prev = String(body?.prev || "").trim();
  const lock = String(body?.lockset || "").trim();
  if (!prev || !lock) {
    return {
      ok: false,
      code: "MG-ATTEST-NEED-PROOF",
      spec: ATTEST_SPEC,
      verdict: "refuse",
      yes: false,
      message: "POST /attest requires non-empty prev and lockset strings for syntactic coordination check",
      attest: attestCite().attest,
      author: IDENTITY,
    };
  }
  const landed = await pingFn({ node_id: body?.node_id, prev, lockset: lock }, { method: "POST" });
  return {
    ok: landed.ok !== false,
    code: landed.ok === false ? landed.code || "MG-ATTEST-REFUSE" : "MG-ATTEST-SYNTACTIC",
    spec: ATTEST_SPEC,
    verdict: landed.ok === false ? "refuse" : "yes",
    yes: landed.ok !== false,
    message:
      landed.ok === false
        ? landed.message || "attest refused"
        : "Syntactic prev|lockset accepted for Cap-7 land coordination. Not ChainLock or zkattest verified.",
    attest: {
      ...attestCite().attest,
      syntactic_ok: landed.ok !== false,
      chainlock_verify: "SLOT",
      fraggate_zkattest: "SLOT",
    },
    prev_present: true,
    lockset_present: true,
    land: citeCap7PublicRow(landed.land) || null,
    round_seed: landed.round_seed || null,
    land_label: landed.land_label || (landed.land && landed.land.label) || null,
    phase: landed.phase,
    update: !!landed.update,
    ...publicPathCap7Honesty(),
    ping: landed.ok === false ? landed : undefined,
    author: IDENTITY,
  };
}

export function landPathNote() {
  return {
    alias_of: APP_HOST + "/v1/shuffle/land",
    public_shuffle_land_exec_means: "coordination-cite-not-icann-publish",
    get_never_plants: true,
    ...publicPathCap7Honesty(),
    message:
      "GET /land cites Cap-7 factory land label for round_id (or POST body). Mesh DNS factory names only — not paid ICANN/.az register. GET with prev+lockset refuses.",
  };
}

/** Names-plane cite for one Cap-7 site row on a public path. Not an ICANN publish. */
export function citeCap7PublicRow(row) {
  if (!row || typeof row !== "object" || Array.isArray(row)) return row;
  return {
    ...row,
    public_icann: false,
    public_icann_registrar: false,
    cap7_public_icann: false,
    cap7_public_egress: false,
    typed_on_icann_dns: false,
    icann_dns_publish: false,
    names_plane: "cap7-names",
    hosted_mcp: "cite",
    hosted_update: "cite",
    hosted_endpoints: "cite",
    cap7_hosted_endpoints: "cite",
    cap7_hosted_endpoints_plane: "names-plane",
    cap7_hosted_endpoints_means: "public-path cite; control-plane names only; not a public ICANN or DNS publish",
    factory_honesty: "cite",
    factory_honesty_plane: "names-plane",
    factory_honesty_means: "public-path cite of Cap-7 names; not a public ICANN or DNS publish",
    honesty_public: "cite",
    hosted_status: "cite",
    public_shuffle_land_exec: false,
    cap7_operator_hold: false,
    cap7_active_use: true,
    cap7_live: true,
    cap7_factory_live: true,
    cap7_registrar_live: false,
    cap7_names_only: true,
    cap7_names_are_not_icann: true,
    paid_registrar: false,
    public_egress_ip: false,
  };
}

/** Public /land overlay. Factory active-use stays on. Nested rows cite names and do not publish ICANN DNS. */
export function overlayPublicLandHonesty(landed) {
  if (!landed || typeof landed !== "object") return landed;
  const overlay = publicPathCap7Honesty();
  const out = { ...landed, public_path: "/land", ...overlay };
  if (out.land && typeof out.land === "object") out.land = citeCap7PublicRow(out.land);
  if (Array.isArray(out.sites)) out.sites = out.sites.map(citeCap7PublicRow);
  if (Array.isArray(out.cap7)) out.cap7 = out.cap7.map(citeCap7PublicRow);
  return out;
}
