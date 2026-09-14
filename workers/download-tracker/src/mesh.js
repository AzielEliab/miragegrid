/**
 * Suite node mesh — QNM-BUILD-1.0 Live Nodes contract.
 * QNS-CD-1.0 cross-map (photon QNS1 packet transfer) — hub cite only.
 * Default OFF. Public rollup is live|locked|isolated counts only.
 * No Node Gate. No auto-heal. Not an anonymity network.
 * No public qnsd proxy. Local qnsd lives in AzielEliab/qnm-node.
 * /v1/mesh/* PROXY to aziel-runtime (AZIEL_RUNTIME binding).
 * SPLIT THE WIRES (STW-1.0): 0.5–1s tip tick = presence+tip hash only.
 * Payload pull-only. Update=proof (cite prev+lockset; 777s dwell).
 * COLD-COPY SURVIVAL (CCS-1.0). REHEAL (RH-1.0 / REHEAL-1.0 / MESH-REHEAL):
 * no neighbor talk-back; own tip+trusted pull or phoenix-WAIT;
 * no bodies/diffs/vote-to-fix. Public-stack auto-heal means that lawful
 * reheal + archive re-expand, not vote-to-fix.
 * AZ-GENERATOR-1.0: Cap-7 mesh DNS factory living deep in the node.
 * Not callable from outside. 7m77s (497s) tick exits FRONT Node Gate
 * only (claim/plant/flag/restore). First claim www.survivalnetwork.az.
 * ≥49 local vault papers. Vault multiply onto each node as cold copies
 * (bootstrap / join / Cap-7 claim / grid-shift standby). No paper
 * bytes on the 1s tip tick. Mesh-authoritative zone + receipts — not
 * public ICANN. MIRAGE-GRID-SHIFT-1.0: MESH-VAULT snapshot+standby,
 * cloak burst. AIRGAP-1.0: local vault + no bearer radios + no
 * climb-back. Official hubs are not airgap Node Gate.
 * AZ Generator and Node Gate are not Softwares-tab products.
 * Assign live. Hosted vpn/hop/tunnel stubs remain refuse.
 * Not a Softwares-tab product. Author: Aziel Eliab only.
 */

const RUNTIME = "https://aziel-runtime.vibelock.workers.dev";
const FRAGGATE_MCP = "https://aziel-runtime.vibelock.workers.dev/mcp";
const FRAGGATE_CALL = "https://aziel-runtime.vibelock.workers.dev/v1/fraggate/call";
const SERVICE_BINDING_ORIGIN = "https://aziel-runtime";
const IDENTITY = "Aziel Eliab";

export const QNM_SPEC = "QNM-BUILD-1.0";
export const QNS_CD_SPEC = "QNS-CD-1.0";
export const MESH_KERNEL = "NM-0.1";
export const MESH_DEFAULT_OFF = true;
export const MESH_ANONYMITY_NETWORK = false;
export const MESH_NODE_GATE = false;
export const MESH_AUTO_HEAL = false;
export const MESH_IDENTITY = IDENTITY;
export const MESH_SLUG = "mesh";
export const MESH_PRODUCT = "miragegrid";
export const MESH_PATH = "/v1/mesh";
export const MESH_STATUS_PATH = "/v1/mesh/status";
export const MESH_NODES_PATH = "/v1/mesh/nodes";
export const MESH_ENABLE_PATH = "/v1/mesh/enable";
export const MESH_DISABLE_PATH = "/v1/mesh/disable";
export const MESH_JOIN_PATH = "/v1/mesh/join";
export const MESH_HEARTBEAT_PATH = "/v1/mesh/heartbeat";
export const MESH_LEAVE_PATH = "/v1/mesh/leave";
export const MESH_BROADCAST_PATH = "/v1/mesh/broadcast";
export const ANON_BROADCAST = "https://github.com/AzielEliab/anon-broadcast";
export const QNM_NODE_REPO = "https://github.com/AzielEliab/qnm-node";
export const AZIEL_RUNTIME_REPO = "https://github.com/AzielEliab/aziel-runtime";
export const AZINTERFACE_REPO = "https://github.com/AzielEliab/azinterface";
export const QNS_CD_DESIGNS = "https://github.com/AzielEliab/aziel-runtime/tree/main/docs/designs";
export const QNS_CD_MESH_DOC = "https://github.com/AzielEliab/aziel-runtime/blob/main/docs/NODE_MESH.md";

/** Hub cite / Worker mesh cross-map only. Not a Softwares-tab product. No public qnsd. */
export const QNS_CD = Object.freeze({
  spec: QNS_CD_SPEC,
  name: "photon QNS1 packet transfer",
  kind: "cross-map",
  softwares_tab: false,
  engine: false,
  public_proxy: false,
  qnsd_proxy: false,
  node_gate: false,
  default_off: true,
  local: "qnsd",
  local_process: "qnm-node/",
  local_repo: QNM_NODE_REPO,
  runtime_repo: AZIEL_RUNTIME_REPO,
  runtime_designs: QNS_CD_DESIGNS,
  runtime_mesh: QNS_CD_MESH_DOC,
  pair_custody: AZINTERFACE_REPO,
  author: IDENTITY,
  identity: IDENTITY,
  note: "QNS-CD-1.0 photon QNS1 packet transfer. Local qnsd is coded in AzielEliab/qnm-node. Runtime cites + catalog field live in AzielEliab/aziel-runtime. AZInterface has pair custody. Hub cite / Worker mesh cross-map only. Not a Softwares-tab product. No public qnsd proxy. No Node Gate. Mesh default OFF. Author: Aziel Eliab only.",
});

export const MESH_NOTE =
  "QNM-BUILD-1.0. QNS-CD-1.0 photon QNS1 packet transfer. SPLIT THE WIRES. COLD-COPY SURVIVAL. REHEAL. AZ-GENERATOR-1.0. MIRAGE-GRID-SHIFT-1.0. AIRGAP-1.0. PAPER-VAULT-ON-NODE. NO-LIE. NO-REWRITE. NO-FAN-1.0. No falsification. No ambiguity. No misleading. Suite mesh default off. Live|locked|isolated counts only. No Node Gate. No auto-heal. Not an anonymity network. No public qnsd proxy. Author: Aziel Eliab only.";

export const SPLIT_WIRES_LAW = "SPLIT THE WIRES";
export const SPLIT_WIRES_SPEC = "STW-1.0";
export const COLD_COPY_LAW = "COLD-COPY SURVIVAL";
export const COLD_COPY_SPEC = "CCS-1.0";
export const REHEAL_LAW = "REHEAL";
export const REHEAL_SPEC = "RH-1.0";
export const REHEAL_1_0 = "REHEAL-1.0";
export const MESH_REHEAL_SPEC = "MESH-REHEAL";
export const AZ_GENERATOR_LAW = "AZ GENERATOR";
export const AZ_GENERATOR_SPEC = "AZ-GENERATOR-1.0";
export const GRID_SHIFT_LAW = "MIRAGE GRID SHIFT";
export const GRID_SHIFT_SPEC = "MIRAGE-GRID-SHIFT-1.0";
export const AIRGAP_LAW = "AIRGAP";
export const AIRGAP_SPEC = "AIRGAP-1.0";
export const PAPER_VAULT_LAW = "PAPER-VAULT-ON-NODE";
export const NO_LIE_LAW = "NO-LIE";
export const NO_REWRITE_LAW = "NO-REWRITE";
export const NO_FALSIFY_LAW = "NO-FALSIFY";
export const NO_AMBIGUITY_LAW = "NO-AMBIGUITY";
export const NO_MISLEAD_LAW = "NO-MISLEAD";
export const NO_FAN_LAW = "NO FALSIFICATION NO AMBIGUITY NO MISLEADING";
export const NO_FAN_SPEC = "NO-FAN-1.0";
export const NO_FAN_PHRASE = "No falsification. No ambiguity. No misleading.";
export const ASSIGN_LIVE = true;
export const HOSTED_STUB_OPS = Object.freeze(["vpn", "hop", "tunnel", "vpn-hop", "mesh-hop"]);
export const TIP_TICK_SIZE = 33;
export const TIP_TICK_MIN_MS = 500;
export const TIP_TICK_MAX_MS = 1000;
export const DWELL_S = 777;
export const TIP_TICK_SOCKET = "tip-1s";
export const DWELL_SOCKET = "dwell-777s";
export const CLAIM_MINUTES = 7;
export const CLAIM_EXTRA_S = 77;
export const CLAIM_CLOCK_S = CLAIM_MINUTES * 60 + CLAIM_EXTRA_S;
export const CLAIM_SOCKET = "claim-7m77s";
export const CAP_7 = 7;
export const MIN_PAPERS = 49;
export const FIRST_CLAIM_NAME = "www.survivalnetwork.az";
export const TIP_TICK_FORBIDDEN = Object.freeze(["body", "diff", "file", "payload", "bytes", "papers", "paper", "vault"]);
export const VAULT_MULTIPLY_EVENTS = Object.freeze([
  "bootstrap", "join", "cap-7-claim", "cap7-claim", "cap_7_claim", "grid-shift-standby", "grid_shift_standby",
]);
export const REHEAL_FORBIDDEN = Object.freeze([
  "body", "bodies", "diff", "diffs", "file", "payload", "vote", "vote-to-fix", "vote_to_fix", "quorum_fix",
]);
export const REHEAL_ALLOWED = Object.freeze(["live", "locked", "isolated", "tip_hash", "tip-hash"]);

export const SPLIT_WIRES = Object.freeze({
  law: SPLIT_WIRES_LAW,
  spec: SPLIT_WIRES_SPEC,
  author: IDENTITY,
  identity: IDENTITY,
  tip_tick: {
    min_ms: TIP_TICK_MIN_MS,
    max_ms: TIP_TICK_MAX_MS,
    size: TIP_TICK_SIZE,
    fields: ["presence", "tip_hash"],
    forbid: TIP_TICK_FORBIDDEN.slice(),
  },
  payload: { plane: "pull-only", sender_fanout: false },
  update: {
    kind: "proof",
    timer: false,
    cite: ["prev", "lockset"],
    fail_closed: true,
    dwell_s: DWELL_S,
    clock_desync_is_yes: false,
    ambiguous_tip: "isolate",
  },
  equivocation: { same_prev_two_tips: "lock-isolate", quorum_is_truth: false },
  emit: { last: "local-after-verify", phoenix: "failed-node-only", unsend_unverified_body: false },
  partition: {
    auto_splice: false,
    rejoin: ["cite", "operator", "lockset"],
    heartbeat_loss_is_poison: false,
    heartbeat_loss_applies_last: false,
  },
  sockets: { tip: TIP_TICK_SOCKET, dwell: DWELL_SOCKET, claim: CLAIM_SOCKET, shared: false },
  assign_live: ASSIGN_LIVE,
  hosted_stubs: HOSTED_STUB_OPS.slice(),
});

export const COLD_COPY = Object.freeze({
  law: COLD_COPY_LAW,
  spec: COLD_COPY_SPEC,
  author: IDENTITY,
  identity: IDENTITY,
  multiply: true,
  min_copies: 2,
  live_body_sync: false,
  tip_erase: "expensive",
  server_pull_wipes_cold: false,
  poison: "hash-absolute-refuse",
  data_outlives_creators: true,
});

export const REHEAL = Object.freeze({
  law: REHEAL_LAW,
  spec: REHEAL_SPEC,
  author: IDENTITY,
  identity: IDENTITY,
  neighbor_talk_dirty_back_to_health: false,
  sources: ["own-tip+trusted-pull", "phoenix-wait"],
  allowed: ["live", "locked", "isolated", "tip-hash"],
  forbid: ["bodies", "diffs", "vote-to-fix"],
  auto_heal: false,
  public_stack_auto_heal: "REHEAL-1.0 / MESH-REHEAL",
  reheal_1_0: REHEAL_1_0,
  mesh_reheal: MESH_REHEAL_SPEC,
  phoenix: "wait",
});

export const AZ_GENERATOR = Object.freeze({
  law: AZ_GENERATOR_LAW,
  spec: AZ_GENERATOR_SPEC,
  author: IDENTITY,
  identity: IDENTITY,
  softwares_tab: false,
  callable: false,
  lives: "deep-node",
  exit: "node-gate-front",
  dns_factory: "cap-7-mesh-authoritative",
  public_icann: false,
  registrar: false,
  unbounded_public_dns: false,
  cctld_takeover: false,
  airgap: "AIRGAP-1.0",
  clock: {
    minutes: CLAIM_MINUTES,
    extra_s: CLAIM_EXTRA_S,
    period_s: CLAIM_CLOCK_S,
    socket: CLAIM_SOCKET,
    alias: "7m77s",
  },
  cap: CAP_7,
  public_host_pair: 2,
  first_claim: FIRST_CLAIM_NAME,
  suffix_order: [".az", ".aziel", "pivot"],
  aziel_tld: ".aziel",
  access: { aznet: true, azbrowser: true, merge: false, naked_public_dns: false },
  min_papers: MIN_PAPERS,
  paper_vault: true,
  tld: ".az",
  no_lie: true,
  no_rewrite: true,
  rewrite_key: false,
  no_falsify: true,
  no_ambiguity: true,
  no_mislead: true,
  no_fan: NO_FAN_SPEC,
  no_fan_phrase: NO_FAN_PHRASE,
});

export const GRID_SHIFT = Object.freeze({
  law: GRID_SHIFT_LAW,
  spec: GRID_SHIFT_SPEC,
  author: IDENTITY,
  identity: IDENTITY,
  softwares_tab: false,
  mesh_vault: { kind: "snapshot+official-standby", role: "ip-mask-host" },
  cap: CAP_7,
  cloak_burst: true,
  node_gate: "miragegrid-.az-only",
  official_hubs_are_node_gate: false,
  hub_tunnels_die_with_pull: true,
  resurrection_of_official_hubs: false,
  pretend_pulled_hub_still_cell: false,
  no_lie: true,
  no_rewrite: true,
  no_falsify: true,
  no_ambiguity: true,
  no_mislead: true,
  no_fan: NO_FAN_SPEC,
  no_fan_phrase: NO_FAN_PHRASE,
});

export const PAPER_VAULT = Object.freeze({
  law: PAPER_VAULT_LAW,
  author: IDENTITY,
  identity: IDENTITY,
  on_every_node: true,
  full_set: true,
  min_papers: MIN_PAPERS,
  multiply: "cold-copy",
  wording: "vault multiply onto each node / papers land on every node as cold copies",
  events: ["bootstrap", "join", "cap-7-claim", "grid-shift-standby"],
  plane: "pull-only",
  live_body_sync: false,
  tip_tick_bodies: false,
  cite_dont_merge: true,
  hash_absolute: true,
  no_have_49_without_bytes: true,
  incomplete: "AZG-INCOMPLETE-VAULT / AZG-UNVERIFIED-TIP / phoenix-WAIT",
});

export const AIRGAP = Object.freeze({
  law: AIRGAP_LAW,
  spec: AIRGAP_SPEC,
  author: IDENTITY,
  identity: IDENTITY,
  softwares_tab: false,
  local_vault: true,
  bearer_radios: false,
  climb_back_pulled_hubs: false,
  downloads_from_local_cold_shelf: true,
  origin_offline_downloads_stay_up: true,
  tip_chatter: ["live", "locked", "isolated", "tip-hash"],
  body_gossip: false,
  reheal: "own-tip+trusted-pull-already-trusted-or-phoenix-wait",
  neighbor_majority: false,
  official_hubs_are_node_gate: false,
  official_hubs_are_airgap_node_gate: false,
  no_lie: true,
  no_rewrite: true,
  no_fan: NO_FAN_SPEC,
});

export const NO_FAN = Object.freeze({
  law: NO_FAN_LAW,
  spec: NO_FAN_SPEC,
  phrase: NO_FAN_PHRASE,
  author: IDENTITY,
  identity: IDENTITY,
  beside: [NO_LIE_LAW, NO_REWRITE_LAW],
  no_lie: true,
  no_rewrite: true,
  no_falsify: true,
  no_ambiguity: true,
  no_mislead: true,
  ambiguous_tip: "isolate",
  rewrite_key: false,
});

export const PUBLIC_STACK = Object.freeze({
  author: IDENTITY,
  pieces: ["anonymity-network", "node-gate", "auto-heal"],
  anonymity_network: "onion/mesh privacy (existing MVP; lawful privacy tool)",
  node_gate: "MirageGrid admission/claim surface for .az names (not official hubs)",
  auto_heal: "REHEAL-1.0 / MESH-REHEAL: own last good tip + verified trusted pull, or phoenix-WAIT",
  softwares_tab_products: ["miragegrid"],
  az_generator_softwares_tab: false,
  node_gate_softwares_tab: false,
});

export function qnsCdFields() {
  return { qns_cd_spec: QNS_CD_SPEC, qns_cd: QNS_CD };
}

export function meshLawFields() {
  return {
    assign_live: ASSIGN_LIVE,
    split_wires: SPLIT_WIRES,
    cold_copy: COLD_COPY,
    reheal: REHEAL,
    az_generator: AZ_GENERATOR,
    grid_shift: GRID_SHIFT,
    airgap: AIRGAP,
    paper_vault: PAPER_VAULT,
    public_stack: PUBLIC_STACK,
    no_lie: true,
    no_rewrite: true,
    no_fan: NO_FAN,
  };
}

export function attachQnsCd(data) {
  if (!data || typeof data !== "object" || Array.isArray(data)) return data;
  return { ...data, ...qnsCdFields(), ...meshLawFields() };
}

export function attachMeshLaw(data) {
  return attachQnsCd(data);
}

function lawVerdict(ok, code, verdict, message, extra) {
  return {
    ok: !!ok,
    code,
    verdict,
    yes: verdict === "yes",
    message,
    author: IDENTITY,
    identity: IDENTITY,
    ...(extra || {}),
    ...qnsCdFields(),
    ...meshLawFields(),
  };
}

export function hostedStubRefuse(op) {
  let key = String(op == null ? "" : op).trim().toLowerCase().replace(/^\/+/, "");
  for (const prefix of ["v1/mesh/", "mesh/", "v1/"]) {
    if (key.startsWith(prefix)) key = key.slice(prefix.length);
  }
  if (key === "assign") return null;
  if (HOSTED_STUB_OPS.includes(key)) {
    return lawVerdict(false, "MESH-STUB", "refuse", "hosted " + key + " remains refuse; assign stays live", {
      op: key,
      assign_live: ASSIGN_LIVE,
    });
  }
  return null;
}

export function tipPlaneContaminated(body) {
  if (!body || typeof body !== "object" || Array.isArray(body)) return false;
  const keys = Object.keys(body).map((k) => String(k).toLowerCase().replace(/\s+/g, "-"));
  return keys.some((k) => TIP_TICK_FORBIDDEN.includes(k) || REHEAL_FORBIDDEN.includes(k));
}

export function refuseTipContamination(body) {
  if (!tipPlaneContaminated(body)) return null;
  if (body && (body.vote_to_fix || body["vote-to-fix"] || body.vote || body.quorum_fix)) {
    return lawVerdict(false, "RH-NO-VOTE-TO-FIX", "refuse", "vote-to-fix is forbidden");
  }
  if (body && (body.neighbor_talk || body.talk_dirty || body.talk_dirty_back_to_health)) {
    return lawVerdict(false, "RH-NO-NEIGHBOR-TALK", "refuse", "neighbor talk-dirty-back-to-health is refused");
  }
  return lawVerdict(false, "STW-TIP-BODY", "refuse", "tip tick is presence+tip hash only (no body/diff/file)");
}

export function refuseReheal(body) {
  if (!body || typeof body !== "object") return null;
  if (body.neighbor_talk || body.talk_dirty || body.talk_dirty_back_to_health) {
    return lawVerdict(false, "RH-NO-NEIGHBOR-TALK", "refuse", "neighbor talk-dirty-back-to-health is refused");
  }
  if (body.vote_to_fix || body["vote-to-fix"] || body.quorum_fix) {
    return lawVerdict(false, "RH-NO-VOTE-TO-FIX", "refuse", "vote-to-fix is forbidden");
  }
  if (body.live_body_sync || body.fanout || body.sender_fanout) {
    return lawVerdict(false, "STW-NO-FANOUT", "refuse", "payload plane is pull-only; sender fan-out is refused");
  }
  if (body.poison || body.poison_marker || body["poison-marker"] || body.rewrite_key || body["rewrite-key"]) {
    return lawVerdict(false, "CCS-POISON-MARKER", "refuse", "poison marker is hash-absolute refuse");
  }
  const fan = refuseNoFan(body);
  if (fan) return fan;
  return refuseTipContamination(body);
}

export function refuseCallGenerator(path) {
  return lawVerdict(false, "AZG-NOT-CALLABLE", "refuse", "AZ Generator lives deep in the node; it is not called from outside", {
    callable: false,
    lives: "deep-node",
    exit: "node-gate-front",
    path: path || "",
    public_icann: false,
    dns_factory: "cap-7-mesh-authoritative",
  });
}

export function citeAzGenerator() {
  return lawVerdict(true, "AZG-CITE", "yes", "AZ-GENERATOR-1.0 cite only. Cap-7 mesh DNS factory. Deep-node → front Node Gate. Not callable. Not public ICANN.", {
    callable: false,
    lives: "deep-node",
    exit: "node-gate-front",
    dns_factory: "cap-7-mesh-authoritative",
    public_icann: false,
    registrar: false,
    unbounded_public_dns: false,
    cctld_takeover: false,
    airgap: "AIRGAP-1.0",
    period_s: CLAIM_CLOCK_S,
    cap: CAP_7,
    public_host_pair: 2,
    first_claim: FIRST_CLAIM_NAME,
    suffix_order: [".az", ".aziel", "pivot"],
    aziel_tld: ".aziel",
    access: { aznet: true, azbrowser: true, merge: false, naked_public_dns: false },
    min_papers: MIN_PAPERS,
    softwares_tab: false,
  });
}

const NO_FAN_FALSIFY = Object.freeze([
  "falsify", "falsified", "falsification", "fake", "fake-flag", "invent", "invent-continuity",
  "fabricate", "false-tip", "false-receipt", "false-claim",   "false-live-nodes", "false-site-up", "false-paper-set", "we-have-49", "have-49-without-bytes",
]);
const NO_FAN_AMBIGUITY = Object.freeze([
  "ambiguous", "ambiguity", "dual-tip", "soft-maybe", "maybe", "pretty-copy", "majority-paper-over",
]);
const NO_FAN_MISLEAD = Object.freeze([
  "misleading", "mislead", "pretend", "pretend-hub-cell", "hub-still-cell", "unmarked-hydra",
  "neighbor-resurrection",
]);

function normVerb(value) {
  return String(value == null ? "" : value).trim().toLowerCase().replace(/[_\s]+/g, "-");
}

export function refuseNoFan(body) {
  if (body == null) return null;
  const raw = typeof body === "string" ? body : (body.verb || body.kind || "");
  const key = normVerb(raw);
  const obj = body && typeof body === "object" ? body : {};
  if (obj.falsify || obj.falsified || obj.fake_flag || obj.invent_continuity || obj.false_tip || NO_FAN_FALSIFY.includes(key)) {
    return lawVerdict(false, "NO-FAN-FALSIFY", "refuse", "no falsified tip, receipt, domain claim, Live Nodes count, or site-up claim", {
      phrase: NO_FAN_PHRASE, spec: NO_FAN_SPEC, kind: key || "falsify", no_lie: true, no_rewrite: true,
    });
  }
  if (obj.ambiguous || obj.dual_tip || obj.soft_maybe || NO_FAN_AMBIGUITY.includes(key)) {
    return lawVerdict(false, "NO-FAN-AMBIGUITY", "isolate", "ambiguous tip isolates; do not paper over with majority or pretty copy", {
      phrase: NO_FAN_PHRASE, spec: NO_FAN_SPEC, kind: key || "ambiguous", quorum_is_truth: false,
    });
  }
  if (obj.misleading || obj.pretend_hub_cell || obj.neighbor_resurrection || NO_FAN_MISLEAD.includes(key)) {
    return lawVerdict(false, "NO-FAN-MISLEAD", "refuse", "no misleading chrome: pulled hub is not still the cell; auto-heal is not neighbor resurrection", {
      phrase: NO_FAN_PHRASE, spec: NO_FAN_SPEC, kind: key || "misleading",
    });
  }
  return null;
}

export function socketsShare(planeA, planeB) {
  const planes = new Set([String(planeA), String(planeB)]);
  const families = [
    new Set([TIP_TICK_SOCKET, "1s", "tip", "tip-tick"]),
    new Set([DWELL_SOCKET, "777s", "dwell", "update"]),
    new Set([CLAIM_SOCKET, "7m77s", "497s", "claim", "az-generator"]),
  ];
  const hits = families.filter((fam) => [...planes].some((p) => fam.has(p))).length;
  if (hits >= 2) {
    return lawVerdict(false, "STW-SOCKET-SPLIT", "refuse", "1s tip tick, 777s dwell, and 7m77s claim clock never share a socket");
  }
  return lawVerdict(true, "STW-SOCKET-OK", "yes", "planes stay on separate sockets");
}

function normalizeAzName(name) {
  let text = String(name == null ? "" : name).trim().toLowerCase();
  if (text.startsWith("https://")) text = text.slice(8);
  if (text.startsWith("http://")) text = text.slice(7);
  text = text.split("/")[0].split(":")[0].replace(/^\.+|\.+$/g, "");
  return text;
}

function isAzName(name) {
  const host = normalizeAzName(name);
  return !!host && host.endsWith(".az") && host !== "az";
}

const OFFICIAL_HUBS = Object.freeze([
  "azieleliab.com",
  "www.azieleliab.com",
  "godlock.uk",
  "www.godlock.uk",
  "azielcorpuslibrary.net",
  "www.azielcorpuslibrary.net",
  "hedidntjump.com",
  "www.hedidntjump.com",
]);

function isOfficialHub(name) {
  const host = normalizeAzName(name);
  return OFFICIAL_HUBS.some((h) => host === h || host.endsWith("." + h)) || host.includes("corpus");
}

function knownContainsFirstClaim(sites) {
  const list = Array.isArray(sites) ? sites : [];
  return list.some((site) => String(site == null ? "" : (site.name || site.host || site.url || site)).toLowerCase().includes(FIRST_CLAIM_NAME));
}

function paperBytes(paper) {
  const body = paper && (paper.bytes || paper.body || paper.data);
  if (body == null) return null;
  return typeof body === "string" ? body : String(body);
}

function paperCount(papers, requireBytes) {
  const list = Array.isArray(papers) ? papers : [];
  const seen = new Set();
  let n = 0;
  for (const paper of list) {
    if (!paper || typeof paper !== "object") continue;
    const author = String(paper.author || paper.identity || "").trim();
    if (author !== IDENTITY) continue;
    const digest = String(paper.hash || paper.sha256 || paper.tip_hash || "").trim().toLowerCase();
    if (digest.length !== 64) continue;
    if (requireBytes && paperBytes(paper) == null) continue;
    if (seen.has(digest)) continue;
    seen.add(digest);
    n += 1;
  }
  return n;
}

function vaultComplete(papers) {
  return paperCount(papers, true) >= MIN_PAPERS;
}

export function refuseIncompleteVault(body) {
  const b = body && typeof body === "object" ? body : {};
  const papers = b.papers || b.vault;
  const nVault = paperCount(papers, true);
  const nCite = paperCount(papers, false);
  if (b.have_49 || b.have49 || b.claimed_count === MIN_PAPERS) {
    if (nVault < MIN_PAPERS) {
      return refuseNoFan("false-paper-set");
    }
  }
  if (nVault >= MIN_PAPERS) return null;
  if (nCite < MIN_PAPERS) return null;
  return lawVerdict(false, "AZG-INCOMPLETE-VAULT", "phoenix-wait", "incomplete vault: no full verified paper set; AZG-UNVERIFIED-TIP; phoenix-WAIT / hold; do not invent", {
    papers: nVault, cites: nCite, min_papers: MIN_PAPERS, false_tip: false, phoenix: "wait",
    unverified_tip: true, azg_unverified_tip: true, code_alias: "AZG-UNVERIFIED-TIP",
    have_49_without_bytes: nCite >= MIN_PAPERS,
  });
}

export function vaultMultiply(body) {
  const b = body && typeof body === "object" ? body : {};
  if (b.live_body_sync || b.fanout || b.sender_fanout) {
    return lawVerdict(false, "STW-NO-FANOUT", "refuse", "no live body sync / sender fan-out of paper bytes; payload plane is pull-only", {
      live_body_sync: false, plane: "pull-only",
    });
  }
  if (b.tip_tick || b.tip_tick_bodies) {
    return lawVerdict(false, "STW-TIP-BODY", "refuse", "tip tick is presence+tip hash only; no paper bytes on the 1s tick", {
      tip_tick_bodies: false,
    });
  }
  const event = String(b.event || "").trim().toLowerCase().replace(/[_\s]+/g, "-");
  if (!VAULT_MULTIPLY_EVENTS.includes(event) && !VAULT_MULTIPLY_EVENTS.includes(String(b.event || ""))) {
    return lawVerdict(false, "AZG-VAULT-EVENT", "refuse", "vault multiply is bootstrap / join / Cap-7 claim / grid-shift standby only", {
      event, events: ["bootstrap", "join", "cap-7-claim", "grid-shift-standby"],
    });
  }
  const incomplete = refuseIncompleteVault(b);
  if (incomplete) return incomplete;
  if (!vaultComplete(b.papers || b.vault)) {
    return lawVerdict(false, "AZG-INCOMPLETE-VAULT", "phoenix-wait", "incomplete vault: AZG-UNVERIFIED-TIP; phoenix-WAIT / hold; do not invent", {
      papers: paperCount(b.papers || b.vault, true), min_papers: MIN_PAPERS, false_tip: false,
      phoenix: "wait", unverified_tip: true, azg_unverified_tip: true, code_alias: "AZG-UNVERIFIED-TIP",
    });
  }
  return lawVerdict(true, "AZG-VAULT-MULTIPLY", "yes", "vault multiply onto each node; papers land as cold copies", {
    event, papers: paperCount(b.papers || b.vault, true), min_papers: MIN_PAPERS, plane: "pull-only",
    live_body_sync: false, tip_tick_bodies: false, cite_dont_merge: true, cold_copy: true,
  });
}

export function airgapMode(body) {
  const b = body && typeof body === "object" ? body : {};
  if (b.enabled === false) {
    return lawVerdict(true, "AIRGAP-OFF", "yes", "airgap mode off", { airgap: false, spec: AIRGAP_SPEC });
  }
  if (b.bearer_radios) {
    return lawVerdict(false, "AIRGAP-NO-BEARER", "refuse", "airgap forbids bearer radios", {
      airgap: true, bearer_radios: false, spec: AIRGAP_SPEC,
    });
  }
  if (b.climb_back) {
    return lawVerdict(false, "AIRGAP-NO-CLIMB-BACK", "refuse", "airgap forbids climb-back onto pulled public hub hostnames", {
      airgap: true, climb_back: false, spec: AIRGAP_SPEC,
    });
  }
  if (b.body_gossip) {
    return lawVerdict(false, "AIRGAP-NO-BODY-GOSSIP", "refuse", "airgap tip chatter is live/locked/isolated/tip-hash only; no body gossip", {
      airgap: true, spec: AIRGAP_SPEC,
    });
  }
  if (b.neighbor_majority || b.vote_to_fix) {
    return lawVerdict(false, "RH-NO-VOTE-TO-FIX", "refuse", "airgap reheal never uses neighbor majority", {
      airgap: true, neighbor_majority: false, spec: AIRGAP_SPEC,
    });
  }
  if (b.hub_as_gate) {
    const host = b.hub_as_gate === true ? "godlock.uk" : String(b.hub_as_gate);
    if (isOfficialHub(host)) {
      return lawVerdict(false, "MGS-NOT-NODE-GATE", "refuse", "official hubs are not airgap Node Gate", {
        airgap: true, official_hubs_are_airgap_node_gate: false, spec: AIRGAP_SPEC,
      });
    }
  }
  if ((b.papers || b.vault) && !vaultComplete(b.papers || b.vault)) {
    const incomplete = refuseIncompleteVault(b);
    if (incomplete) return incomplete;
    return lawVerdict(false, "AZG-INCOMPLETE-VAULT", "phoenix-wait", "airgap requires the full verified local vault; AZG-UNVERIFIED-TIP; phoenix-WAIT", {
      airgap: true, papers: paperCount(b.papers || b.vault, true), min_papers: MIN_PAPERS,
      phoenix: "wait", unverified_tip: true, azg_unverified_tip: true, code_alias: "AZG-UNVERIFIED-TIP",
    });
  }
  return lawVerdict(true, "AIRGAP-OK", "yes", "airgap: local vault; no bearer radios; no climb-back; local cold shelf may serve", {
    airgap: true, spec: AIRGAP_SPEC, local_vault: true, bearer_radios: false, climb_back: false,
    body_gossip: false, downloads_from_local_cold_shelf: b.serve_local !== false,
    tip_chatter: ["live", "locked", "isolated", "tip-hash"], official_hubs_are_airgap_node_gate: false,
  });
}

export function claimAzDomain(body) {
  const b = body && typeof body === "object" ? body : {};
  if (b.inbound_call || b.call_generator || b.run_generator) {
    return refuseCallGenerator("claimAzDomain");
  }
  if (b.public_registrar || b.icann || b.cloudflare_dns) {
    return lawVerdict(false, "AZG-NOT-PUBLIC-REGISTRAR", "refuse", "mesh DNS factory is not a public ICANN/Cloudflare registrar; do not fake registration success", {
      public_icann: false, registrar: false, unbounded_public_dns: false, dns_factory: "cap-7-mesh-authoritative",
    });
  }
  const fan = refuseNoFan(b);
  if (fan) return fan;
  if (b.tip_verified === false) {
    return lawVerdict(false, "AZG-UNVERIFIED-TIP", "phoenix-wait", "unverified tip: refuse claim rather than invent continuity; phoenix-WAIT / hold", {
      false_tip: false, phoenix: "wait", no_lie: true, phrase: NO_FAN_PHRASE,
    });
  }
  const origin = String(b.origin_node || b.node || "node-01");
  const claimed = Number(b.claimed || b.claimed_count || 0) || 0;
  const known = Array.isArray(b.known_sites) ? b.known_sites : [];
  if (claimed >= CAP_7) {
    return lawVerdict(false, "AZG-CAP-7", "refuse", "Cap-7: at most 7 .az names per covered node", {
      claimed, cap: CAP_7, origin_node: origin,
    });
  }
  const firstNeeded = !knownContainsFirstClaim(known);
  const named = normalizeAzName(b.name);
  if (firstNeeded && (!named || named === FIRST_CLAIM_NAME)) {
    if (b.claimable === false) {
      return lawVerdict(true, "AZG-FIRST-CLAIM-RESUME", "yes", "www.survivalnetwork.az cannot be claimed; resume 7m77s clock under Cap-7", {
        first_claim: FIRST_CLAIM_NAME, resume: true, period_s: CLAIM_CLOCK_S, origin_node: origin, hosted_by: origin,
      });
    }
    return lawVerdict(true, "AZG-FIRST-CLAIM", "yes", "first claim is www.survivalnetwork.az", {
      name: FIRST_CLAIM_NAME, origin_node: origin, hosted_by: origin, period_s: CLAIM_CLOCK_S, cap: CAP_7,
    });
  }
  if (b.have_49 && paperCount(b.papers || b.vault, true) < MIN_PAPERS) {
    return refuseNoFan("false-paper-set");
  }
  if (b.papers != null || b.vault != null || b.needs_papers) {
    const pile = b.papers || b.vault;
    const incomplete = refuseIncompleteVault(b);
    if (incomplete) return incomplete;
    if (paperCount(pile, true) < MIN_PAPERS) {
      return lawVerdict(false, "AZG-INCOMPLETE-VAULT", "phoenix-wait", "incomplete local vault; refuse claim rather than invent continuity; phoenix-WAIT / hold", {
        papers: paperCount(pile, true), min_papers: MIN_PAPERS, false_tip: false, phoenix: "wait",
      });
    }
  }
  if (named && isOfficialHub(named)) {
    return lawVerdict(false, "AZG-NOT-HUB", "refuse", "official hubs are not Node Gate and are not claimed .az names");
  }
  if (named && !isAzName(named)) {
    return lawVerdict(false, "AZG-TLD", "refuse", "AZ Generator claims domains ending in .az only");
  }
  return lawVerdict(true, named ? "AZG-CLAIM-OK" : "AZG-CLOCK-TICK", "yes", named ? "domain claimed; site + server hosted by origin node" : "7m77s clock continues under Cap-7", {
    name: named || "", origin_node: origin, hosted_by: origin, period_s: CLAIM_CLOCK_S, cap: CAP_7,
  });
}

export function offlineDownloadStayUp(body) {
  const b = body && typeof body === "object" ? body : {};
  const offline = !!(b.origin_offline || b.offline);
  return lawVerdict(true, "AZG-OFFLINE-STAY-UP", "yes", "origin offline: sites stay up for downloads (cold-copy / standby / MESH-VAULT)", {
    origin_offline: offline,
    downloads_stay_up: true,
    download_plane: "pull-only",
    tip_plane: offline ? (b.tip_presence || "isolated") : "live",
    mesh_vault: "snapshot+official-standby",
  });
}

export function applyGridShift(body) {
  const b = body && typeof body === "object" ? body : {};
  const fan = refuseNoFan(b);
  if (fan) return fan;
  if (b.vote_to_fix || b["vote-to-fix"] || b.neighbor_talk) {
    return lawVerdict(false, "RH-NO-VOTE-TO-FIX", "refuse", "neighbor vote-to-fix labeled as auto-heal is refused");
  }
  if (b.resurrect_hub) {
    return lawVerdict(false, "MGS-NO-HUB-RESURRECT", "refuse", "grid shift is not resurrection of godlock.uk / corpus hostnames");
  }
  const az = normalizeAzName(b.az_name || b.name);
  if (az && isOfficialHub(az)) {
    return lawVerdict(false, "MGS-NOT-NODE-GATE", "refuse", "official hubs are not Node Gate");
  }
  if (az && !isAzName(az)) {
    return lawVerdict(false, "MGS-AZ-ONLY", "refuse", "grid shift keeps a .az (or standby) name answerable");
  }
  const names = Array.isArray(b.names) ? b.names.map(normalizeAzName) : [];
  if (b.cloak_burst) {
    const already = Number(b.already_claimed || 0) || 0;
    if (already + names.length > CAP_7 || names.length > CAP_7) {
      return lawVerdict(false, "AZG-CAP-7", "refuse", "cloak burst cannot exceed Cap-7 spare/claimed .az names", { cap: CAP_7 });
    }
    return lawVerdict(true, "MGS-CLOAK-BURST", "yes", "cloak burst planted spare .az names; originating node IP hidden", {
      names, cap: CAP_7, cloak: true, softwares_tab: false,
    });
  }
  return lawVerdict(true, "MGS-SHIFT-OK", "yes", "grid shift: .az stays answerable; node cloaked/hidden after domain pull", {
    az_name: az || FIRST_CLAIM_NAME,
    answerable: true,
    node_cloaked: b.cloak !== false,
    mesh_vault: "snapshot+official-standby",
    hub_tunnels_die_with_pull: true,
    resurrection: false,
    downloads_stay_up: true,
  });
}

export const MESH_OPS = Object.freeze([
  "status",
  "enable",
  "disable",
  "join",
  "heartbeat",
  "leave",
  "nodes",
  "broadcast",
]);

export const MESH_PROXY_ROUTES = Object.freeze([
  { path: MESH_PATH, methods: ["get", "head"], op: "status", summary: "PROXY to aziel-runtime GET /v1/mesh. Suite mesh status. Default OFF. Not a local op." },
  { path: MESH_STATUS_PATH, methods: ["get"], op: "status", summary: "PROXY alias of GET /v1/mesh. Not a local op." },
  { path: MESH_NODES_PATH, methods: ["get"], op: "nodes", summary: "PROXY to aziel-runtime GET /v1/mesh/nodes. Live Nodes (5-minute presence). Not a local op." },
  { path: MESH_ENABLE_PATH, methods: ["post"], op: "enable", summary: "PROXY to aziel-runtime POST /v1/mesh/enable. Operator bearer required. Rate-limited. Not a local op." },
  { path: MESH_DISABLE_PATH, methods: ["post"], op: "disable", summary: "PROXY to aziel-runtime POST /v1/mesh/disable. Always allowed. Not a local op." },
  { path: MESH_JOIN_PATH, methods: ["post"], op: "join", summary: "PROXY to aziel-runtime POST /v1/mesh/join. Body {product, node_id?, label?, presence?}. Refused while OFF. Not a local op." },
  { path: MESH_HEARTBEAT_PATH, methods: ["post"], op: "heartbeat", summary: "PROXY to aziel-runtime POST /v1/mesh/heartbeat. Body {node_id}. Not a local op." },
  { path: MESH_LEAVE_PATH, methods: ["post"], op: "leave", summary: "PROXY to aziel-runtime POST /v1/mesh/leave. Body {node_id}. Not a local op." },
  { path: MESH_BROADCAST_PATH, methods: ["post"], op: "broadcast", summary: "PROXY to aziel-runtime POST /v1/mesh/broadcast. SHA-256 receipt only. Not AnonBroadcast upload. Not a local op." },
]);

/** Allowlisted suite mesh PROXY paths. Not a Node Gate. Not local ops. */
export const MESH_ROUTE_METHODS = Object.freeze({
  "/v1/mesh": ["GET", "HEAD"],
  "/v1/mesh/status": ["GET", "HEAD"],
  "/v1/mesh/nodes": ["GET", "HEAD"],
  "/v1/mesh/enable": ["POST"],
  "/v1/mesh/disable": ["POST"],
  "/v1/mesh/join": ["POST"],
  "/v1/mesh/heartbeat": ["POST"],
  "/v1/mesh/leave": ["POST"],
  "/v1/mesh/broadcast": ["POST"],
});

export function meshCorsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, HEAD, POST, OPTIONS",
    "Access-Control-Allow-Headers":
      "Content-Type, Accept, Authorization, X-Aziel-Runtime-Token, User-Agent",
    "Access-Control-Expose-Headers": "X-Aziel-Runtime-Version, X-Aziel-Mesh-Door",
  };
}

function firstNum(...vals) {
  for (const raw of vals) {
    if (raw == null || raw === "") continue;
    const n = typeof raw === "number" ? raw : Number(String(raw).replace(/,/g, ""));
    if (Number.isFinite(n) && n >= 0) return Math.floor(n);
  }
  return null;
}

function asList(value) {
  if (!value) return [];
  if (Array.isArray(value)) return value;
  if (typeof value === "object") return Object.values(value);
  return [];
}

function truthyEnabled(value) {
  if (value === true || value === 1) return true;
  const s = String(value || "").trim().toLowerCase();
  return s === "on" || s === "enabled" || s === "true" || s === "live";
}

export function emptyRollup() {
  return { live: 0, locked: 0, isolated: 0 };
}

export function meshRollup(mesh) {
  const m = mesh && typeof mesh === "object" ? mesh : {};
  const r = m.rollup && typeof m.rollup === "object" && !Array.isArray(m.rollup) ? m.rollup : {};
  return {
    live: firstNum(r.live, m.live_nodes, m.live) ?? 0,
    locked: firstNum(r.locked, m.locked_nodes, m.locked) ?? 0,
    isolated: firstNum(r.isolated, m.isolated_nodes, m.isolated) ?? 0,
  };
}

function parseRollup(inner, listedLive) {
  const r = inner.rollup && typeof inner.rollup === "object" && !Array.isArray(inner.rollup)
    ? inner.rollup
    : {};
  const live = firstNum(
    r.live,
    r.live_nodes,
    r.live_count,
    inner.live,
    inner.live_nodes,
    inner.mesh_live_nodes,
    inner.live_count,
    inner.count,
    inner.n,
    inner.node_count,
    listedLive,
  );
  const locked = firstNum(r.locked, r.locked_nodes, r.locked_count, inner.locked, inner.locked_nodes, inner.locked_count);
  const isolated = firstNum(r.isolated, r.isolated_nodes, r.isolated_count, inner.isolated, inner.isolated_nodes, inner.isolated_count);
  return {
    live: live != null ? live : 0,
    locked: locked != null ? locked : 0,
    isolated: isolated != null ? isolated : 0,
  };
}

export function emptyMesh(extra = {}) {
  const rollup = extra.rollup && typeof extra.rollup === "object"
    ? { ...emptyRollup(), ...extra.rollup }
    : emptyRollup();
  return {
    ok: true,
    code: extra.code || "MESH-OK",
    spec: QNM_SPEC,
    kernel: MESH_KERNEL,
    enabled: false,
    default_off: true,
    live_nodes: 0,
    status: extra.status || "off",
    source: extra.source || "fallback",
    node_gate: false,
    auto_heal: false,
    anonymity_network: false,
    author: MESH_IDENTITY,
    identity: MESH_IDENTITY,
    note: MESH_NOTE,
    door: MESH_PATH,
    ...extra,
    spec: QNM_SPEC,
    rollup,
    node_gate: false,
    auto_heal: false,
    anonymity_network: false,
    author: MESH_IDENTITY,
    identity: MESH_IDENTITY,
    ...qnsCdFields(),
    ...meshLawFields(),
  };
}

export function compactMeshNode(raw) {
  if (raw == null) return null;
  if (typeof raw === "string") {
    const id = raw.trim();
    return id ? { id } : null;
  }
  if (typeof raw !== "object") return null;
  const id = String(raw.id || raw.node_id || raw.session_id || raw.peer || raw.name || "").trim();
  const product = String(raw.product || raw.slug || raw.suite || "").trim();
  const seen = raw.last_utc || raw.last_seen || raw.seen_utc || raw.heartbeat_utc || "";
  if (!id && !product && !seen) return null;
  const out = {};
  if (id) out.id = id;
  if (product) out.product = product;
  if (seen) out.last_utc = String(seen);
  return out;
}

export function parseMeshDoc(body) {
  if (body == null) return emptyMesh({ status: "unavailable", source: "empty" });
  if (typeof body !== "object" || Array.isArray(body)) {
    return emptyMesh({ status: "unavailable", source: "empty" });
  }
  const inner = body.result && typeof body.result === "object" && !Array.isArray(body.result)
    ? { ...body, ...body.result }
    : (body.mesh && typeof body.mesh === "object" && !Array.isArray(body.mesh)
      ? { ...body, ...body.mesh }
      : body);
  const listed = asList(inner.nodes || inner.list || inner.peers || inner.live_nodes_list)
    .map(compactMeshNode)
    .filter(Boolean);
  const rollup = parseRollup(inner, listed.length ? listed.length : null);
  const enabled = truthyEnabled(inner.enabled)
    || truthyEnabled(inner.mesh_enabled)
    || String(inner.status || "").toLowerCase() === "on";
  const unavailable = inner.ok === false
    && !enabled
    && (inner.error || inner.status === "unavailable" || inner.status === "not_found");
  const status = enabled ? "on" : (unavailable ? "unavailable" : "off");
  const live = enabled ? rollup.live : 0;
  const locked = enabled ? rollup.locked : 0;
  const isolated = enabled ? rollup.isolated : 0;
  const products = asList(inner.products_present || inner.products)
    .map((p) => (typeof p === "string" ? p : (p && (p.product || p.slug || p.name)) || ""))
    .map((s) => String(s).trim())
    .filter(Boolean);
  return emptyMesh({
    ok: inner.ok !== false,
    enabled,
    default_off: inner.default_off !== false,
    live_nodes: live,
    rollup: { live, locked, isolated },
    products_present: products,
    nodes: listed,
    status,
    source: inner.source || "parsed",
    door: inner.door || MESH_PATH,
    note: enabled
      ? "QNM-BUILD-1.0. Suite mesh is on. Live|locked|isolated counts only. No Node Gate. No auto-heal. Not an anonymity network."
      : MESH_NOTE,
  });
}

export function publicMesh(mesh) {
  const m = mesh && typeof mesh === "object" ? mesh : emptyMesh();
  const enabled = !!m.enabled;
  const rollup = enabled ? meshRollup(m) : emptyRollup();
  return {
    spec: QNM_SPEC,
    kernel: MESH_KERNEL,
    enabled,
    default_off: m.default_off !== false,
    live_nodes: enabled ? rollup.live : 0,
    rollup,
    status: enabled ? "on" : (m.status === "unavailable" ? "unavailable" : "off"),
    source: m.source || "fallback",
    node_gate: false,
    auto_heal: false,
    anonymity_network: false,
    author: MESH_IDENTITY,
    identity: MESH_IDENTITY,
    door: MESH_PATH,
    status_path: MESH_STATUS_PATH,
    nodes_path: MESH_NODES_PATH,
    join: MESH_JOIN_PATH,
    heartbeat: MESH_HEARTBEAT_PATH,
    enable: MESH_ENABLE_PATH,
    disable: MESH_DISABLE_PATH,
    leave: MESH_LEAVE_PATH,
    broadcast: MESH_BROADCAST_PATH,
    mcp: FRAGGATE_MCP,
    fraggate: FRAGGATE_CALL,
    slug: MESH_SLUG,
    product: MESH_PRODUCT,
    ops: MESH_OPS.slice(),
    origin: RUNTIME + MESH_PATH,
    note: m.note || MESH_NOTE,
    ...qnsCdFields(),
    ...meshLawFields(),
  };
}

export function meshStatusLine(mesh) {
  const m = mesh && typeof mesh === "object" ? mesh : emptyMesh();
  if (m.enabled) {
    const r = meshRollup(m);
    return "Suite mesh: on · live " + r.live + " · locked " + r.locked + " · isolated " + r.isolated + ". Not an anonymity network.";
  }
  if (m.status === "unavailable") {
    return "Suite mesh: off (unavailable). QNM-BUILD-1.0. QNS-CD-1.0. Not an anonymity network.";
  }
  return "Suite mesh: off (default). QNM-BUILD-1.0. QNS-CD-1.0. Not an anonymity network.";
}

/** Public Live Nodes count. Never auto-heal a visiting floor. */
export function alignLiveNodes({ mesh } = {}) {
  if (mesh && mesh.enabled) return meshRollup(mesh).live;
  return 0;
}

export function meshPointer() {
  return {
    pointer: true,
    path: MESH_PATH,
    enabled_default: false,
    spec: QNM_SPEC,
    kernel: MESH_KERNEL,
    rollup: "live|locked|isolated",
    node_gate: false,
    auto_heal: false,
    anonymity_network: false,
    author: MESH_IDENTITY,
    identity: MESH_IDENTITY,
    catalog_mcp: FRAGGATE_MCP,
    fraggate_slug: MESH_SLUG,
    origin: RUNTIME + MESH_PATH,
    note: "PROXY to aziel-runtime /v1/mesh/* via AZIEL_RUNTIME. Not a local op. Not AnonBroadcast. Not AZMail's product-local ring. MirageGrid hosted /v1 remains session assignment (not a hosted hop). Full node process is local qnm-node/. QNS-CD-1.0 photon QNS1 packet transfer is a hub cite / Worker mesh cross-map only (no public qnsd proxy). SPLIT THE WIRES. COLD-COPY SURVIVAL. REHEAL. AZ-GENERATOR-1.0. MIRAGE-GRID-SHIFT-1.0. AIRGAP-1.0. PAPER-VAULT-ON-NODE. " + MESH_NOTE,
    anon_broadcast: ANON_BROADCAST,
    anon_broadcast_publish_path: false,
    ...qnsCdFields(),
    ...meshLawFields(),
  };
}

export function meshOpenApiPaths() {
  const paths = {};
  for (const route of MESH_PROXY_ROUTES) {
    const entry = paths[route.path] || {};
    for (const method of route.methods) {
      entry[method] = {
        operationId: "miragegrid_mesh_" + route.op + (method === "head" ? "_head" : "") + "_proxy",
        summary: route.summary,
        tags: ["mesh"],
        responses: { "200": { description: "aziel-runtime mesh envelope" } },
      };
      if (method === "post") {
        entry[method].requestBody = { content: { "application/json": { schema: { type: "object" } } } };
      }
    }
    paths[route.path] = entry;
  }
  return paths;
}

export function normalizeMeshPath(pathname) {
  const raw = String(pathname == null ? "" : pathname);
  const noQuery = raw.split("?")[0];
  const path = noQuery.replace(/\/+$/, "") || "/";
  return path.startsWith("/") ? path : `/${path}`;
}

export function isMeshPath(pathname) {
  const path = normalizeMeshPath(pathname);
  return path === "/v1/mesh" || path.startsWith("/v1/mesh/");
}

export function runtimeOrigin(env) {
  const fromEnv = env && (env.AZIEL_RUNTIME_ORIGIN || env.RUNTIME_ORIGIN);
  if (typeof fromEnv === "string" && /^https:\/\//i.test(fromEnv)) {
    return fromEnv.replace(/\/+$/, "");
  }
  return RUNTIME;
}

function runtimeService(env) {
  const bind = env && env.AZIEL_RUNTIME;
  if (bind && typeof bind === "object" && typeof bind.fetch === "function") return bind;
  return null;
}

function joinOriginUrl(base, pathAndQuery) {
  const origin = String(base || RUNTIME).replace(/\/+$/, "");
  const raw = String(pathAndQuery == null ? "" : pathAndQuery);
  const qIndex = raw.indexOf("?");
  const pathOnly = qIndex >= 0 ? raw.slice(0, qIndex) : raw;
  const query = qIndex >= 0 ? raw.slice(qIndex) : "";
  let path = pathOnly.startsWith("/") ? pathOnly : `/${pathOnly}`;
  path = path.replace(/\/{2,}/g, "/");
  if (!path || path === "/") path = "/";
  return origin + path + query;
}

function meshJson(body, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "private, no-store",
      ...meshCorsHeaders(),
    },
  });
}

function meshErrFields({ message, door_url, http_status, content_type, via, extra }) {
  return {
    ok: false,
    code: "MESH-ERR",
    door: "mesh",
    kernel: "mesh",
    spec: QNM_SPEC,
    author: MESH_IDENTITY,
    identity: MESH_IDENTITY,
    node_gate: false,
    auto_heal: false,
    anonymity_network: false,
    enabled: false,
    default_off: true,
    message,
    door_url: door_url || "",
    http_status: http_status == null ? null : http_status,
    content_type: content_type || "",
    via: via || "",
    ...(extra || {}),
    ...qnsCdFields(),
    ...meshLawFields(),
  };
}

async function originFetch(env, pathAndQuery, init, request) {
  const headers = new Headers((init && init.headers) || {});
  if (!headers.has("User-Agent") && !headers.has("user-agent")) headers.set("User-Agent", "Mozilla/5.0");
  if (!headers.has("Accept") && !headers.has("accept")) headers.set("Accept", "application/json");
  headers.set("X-Aziel-Runtime-Via", "miragegrid-download-tracker");
  const next = { ...(init || {}), headers };
  if (!next.signal && typeof AbortSignal !== "undefined" && typeof AbortSignal.timeout === "function") {
    next.signal = AbortSignal.timeout(20000);
  }

  const raw = String(pathAndQuery == null ? "" : pathAndQuery);
  const path = raw.startsWith("/") ? raw : `/${raw}`;
  const door_url = joinOriginUrl(runtimeOrigin(env), path);
  const bind = runtimeService(env);
  if (bind) {
    try {
      const res = await bind.fetch(new Request(SERVICE_BINDING_ORIGIN + path, next));
      const ct = String(res.headers.get("Content-Type") || "");
      const looksJson = ct.includes("json");
      if (res.ok || looksJson) {
        return { res, via: "service-binding", door_url };
      }
    } catch {
      /* binding missing or local stub — HTTPS fallback */
    }
  }

  try {
    if (request && request.url) {
      const here = new URL(request.url).origin;
      const there = new URL(door_url).origin;
      if (here && here === there) {
        throw new Error("Mesh URL points at this Worker — refusing self-fetch loop.");
      }
    }
  } catch (err) {
    if (String(err && err.message || "").includes("self-fetch")) throw err;
  }
  const res = await fetch(door_url, next);
  return { res, via: "http", door_url };
}

/**
 * PROXY one allowlisted /v1/mesh/* path to aziel-runtime.
 * Not a local op. GET never enables. Default radios OFF.
 */
export async function runMeshProxy(env, request, pathAndQuery) {
  const pathOnly = normalizeMeshPath(pathAndQuery);
  const stub = hostedStubRefuse(pathOnly);
  if (stub) {
    return { status: 403, data: stub };
  }
  const method = String((request && request.method) || "GET").toUpperCase();
  if (pathOnly === "/v1/mesh/enable" && method === "GET") {
    return {
      status: 403,
      data: lawVerdict(false, "MESH-GET-NO-ENABLE", "refuse", "GET never enables suite mesh", {
        enabled: false,
        default_off: true,
        path: pathOnly,
      }),
    };
  }
  if (pathOnly === "/v1/mesh/reheal") {
    if (method !== "POST") {
      return {
        status: 405,
        data: meshErrFields({
          message: "REHEAL is POST-only. Own tip+trusted pull or phoenix-WAIT. No neighbor talk-back.",
          extra: { code: "MESH-METHOD", path: pathOnly, method },
        }),
      };
    }
    let healBody = {};
    try {
      healBody = await request.json();
    } catch {
      healBody = {};
    }
    const dirty = refuseReheal(healBody);
    if (dirty) return { status: 403, data: dirty };
    const wait = !!(healBody && (healBody.phoenix_wait || healBody.phoenix === "wait" || healBody.source === "phoenix-wait"));
    const ownTip = healBody && (healBody.own_tip || healBody.tip_hash || healBody["tip-hash"]);
    const trusted = !!(healBody && healBody.trusted_pull);
    if (wait) {
      return {
        status: 200,
        data: lawVerdict(true, "RH-PHOENIX-WAIT", "phoenix-wait", "reheal phoenix-WAIT (not neighbor talk-back)", {
          source: "phoenix-wait",
          auto_heal: false,
        }),
      };
    }
    if (ownTip && trusted) {
      return {
        status: 200,
        data: lawVerdict(true, "RH-OWN-TIP", "yes", "reheal from own tip plus trusted pull", {
          source: "own-tip+trusted-pull",
          auto_heal: false,
        }),
      };
    }
    return {
      status: 403,
      data: lawVerdict(false, "RH-FAIL-CLOSED", "refuse", "reheal fail-closed without own tip+trusted pull or phoenix-WAIT"),
    };
  }
  if (pathOnly === "/v1/mesh/az-generator") {
    if (method === "GET" || method === "HEAD") {
      return { status: 200, data: citeAzGenerator() };
    }
    return { status: 403, data: refuseCallGenerator(pathOnly) };
  }
  if (pathOnly === "/v1/mesh/grid-shift") {
    if (method === "GET" || method === "HEAD") {
      return {
        status: 200,
        data: lawVerdict(true, "MGS-CITE", "yes", "MIRAGE-GRID-SHIFT-1.0 cite only. MESH-VAULT snapshot+standby. Cap-7 cloak burst. Not a generator call.", {
          softwares_tab: false,
          public_icann: false,
          cap: CAP_7,
        }),
      };
    }
    if (method !== "POST") {
      return {
        status: 405,
        data: meshErrFields({
          message: "MIRAGE-GRID-SHIFT-1.0 is POST-only. MESH-VAULT snapshot+standby. Cap-7 cloak burst.",
          extra: { code: "MESH-METHOD", path: pathOnly, method },
        }),
      };
    }
    let shiftBody = {};
    try {
      shiftBody = await request.json();
    } catch {
      shiftBody = {};
    }
    const dirty = refuseReheal(shiftBody);
    if (dirty) return { status: 403, data: dirty };
    return { status: 200, data: applyGridShift(shiftBody) };
  }
  if (pathOnly === "/v1/mesh/airgap") {
    const method = String((request && request.method) || "GET").toUpperCase();
    if (method !== "POST") {
      return {
        status: 405,
        data: meshErrFields({
          message: "AIRGAP-1.0 is POST-only. Local vault. No bearer radios. No climb-back.",
          extra: { code: "MESH-METHOD", path: pathOnly, method },
        }),
      };
    }
    let airBody = {};
    try {
      airBody = await request.json();
    } catch {
      airBody = {};
    }
    const dirty = refuseReheal(airBody);
    if (dirty) return { status: 403, data: dirty };
    return { status: 200, data: airgapMode(airBody) };
  }
  if (pathOnly === "/v1/mesh/vault") {
    const method = String((request && request.method) || "GET").toUpperCase();
    if (method !== "POST") {
      return {
        status: 405,
        data: meshErrFields({
          message: "PAPER-VAULT-ON-NODE is POST-only. Vault multiply. Cold copies. No tip-tick bodies.",
          extra: { code: "MESH-METHOD", path: pathOnly, method },
        }),
      };
    }
    let vaultBody = {};
    try {
      vaultBody = await request.json();
    } catch {
      vaultBody = {};
    }
    const dirty = refuseReheal(vaultBody);
    if (dirty) return { status: 403, data: dirty };
    return { status: 200, data: vaultMultiply(vaultBody) };
  }
  const allowed = MESH_ROUTE_METHODS[pathOnly];
  if (!allowed) {
    return {
      status: 404,
      data: meshErrFields({
        message: "Unknown mesh path. Use GET /v1/mesh /status /nodes or POST /enable /disable /join /heartbeat /leave /broadcast.",
        extra: { code: "MESH-UNKNOWN", path: pathOnly },
      }),
    };
  }
  if (!allowed.includes(method)) {
    return {
      status: 405,
      data: meshErrFields({
        message: "Method not allowed on " + pathOnly + ".",
        extra: { code: "MESH-METHOD", path: pathOnly, method },
      }),
    };
  }

  let search = "";
  try {
    if (pathAndQuery && String(pathAndQuery).includes("?")) {
      search = "?" + String(pathAndQuery).split("?").slice(1).join("?");
    } else if (request && request.url) {
      search = new URL(request.url).search || "";
    }
  } catch {
    search = "";
  }
  const path = pathOnly + search;

  let body;
  if (method === "POST") {
    try {
      body = await request.json();
    } catch {
      body = {};
    }
    const dirty = refuseReheal(body);
    if (dirty) return { status: 403, data: dirty };
  }

  const headers = {
    Accept: "application/json",
    "User-Agent": "Mozilla/5.0",
  };
  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (request && request.headers) {
    const token = request.headers.get("Authorization") || request.headers.get("X-Aziel-Runtime-Token");
    if (token) {
      headers.Authorization = token.startsWith("Bearer ") || token.startsWith("bearer ") ? token : `Bearer ${token}`;
      headers["X-Aziel-Runtime-Token"] = token.replace(/^Bearer\s+/i, "");
    }
  }

  const door_url = joinOriginUrl(runtimeOrigin(env), path);
  let fetched;
  try {
    fetched = await originFetch(
      env,
      path,
      {
        method,
        headers,
        body: body !== undefined ? JSON.stringify(body) : undefined,
      },
      request,
    );
  } catch (err) {
    return {
      status: 502,
      data: meshErrFields({
        message: "Mesh door fetch failed.",
        door_url,
        http_status: null,
        content_type: "",
        via: runtimeService(env) ? "service-binding" : "http",
        extra: { detail: String(err && err.message ? err.message : err) },
      }),
    };
  }

  const res = fetched.res;
  const via = fetched.via;
  const len = Number(res.headers.get("Content-Length") || "0");
  if (Number.isFinite(len) && len > 2 * 1024 * 1024) {
    return {
      status: 502,
      data: meshErrFields({
        message: "Mesh response too large for this Worker proxy.",
        door_url: fetched.door_url || door_url,
        http_status: res.status,
        content_type: res.headers.get("Content-Type") || "",
        via,
      }),
    };
  }

  if (method === "HEAD") {
    return { status: res.status, data: attachQnsCd({ ok: res.ok, code: res.ok ? "MESH-OK" : "MESH-ERR", door: "mesh", via, enabled: false }) };
  }

  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = null;
  }
  if (!data || typeof data !== "object") {
    const preview = String(text || "").replace(/\s+/g, " ").slice(0, 160);
    return {
      status: res.status || 502,
      data: meshErrFields({
        message: "Mesh door returned non-JSON.",
        door_url: fetched.door_url || door_url,
        http_status: res.status,
        content_type: res.headers.get("Content-Type") || "",
        via,
        extra: { preview },
      }),
    };
  }
  return { status: res.status, data: attachQnsCd(data) };
}

/**
 * Worker fetch entry for /v1/mesh and /v1/mesh/*.
 * Returns null when the path is not a mesh door path.
 */
export async function handleMeshApi(request, url, env) {
  if (!isMeshPath(url.pathname)) return null;
  const result = await runMeshProxy(env, request, url.pathname + (url.search || ""));
  return meshJson(result.data, result.status);
}
