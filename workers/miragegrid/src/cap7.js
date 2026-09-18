/**
 * CAP7-SHUFFLE-1.0 — MirageGrid-only factory roster.
 * Different names. Hub design DNA only. resolves_to_hub false.
 * name_may_change true. public_icann false. radio_phy false.
 * Author: Aziel Eliab only.
 */

export const CAP7_SHUFFLE_SPEC = "CAP7-SHUFFLE-1.0";
export const SEMANTIC_BRIDGE_SPEC = "SEMANTIC-BRIDGE-1.0";
export const IDENTITY = "Aziel Eliab";
export const PERSON_ID = "https://www.azieleliab.com/#aziel";
export const APP_HOST = "https://miragegrid.vibelock.workers.dev";
export const DOWNLOAD_HOST = "https://miragegrid-download-tracker.vibelock.workers.dev";
export const RUNTIME = "https://aziel-runtime.vibelock.workers.dev";
export const CAP_7 = 7;
export const PUBLIC_HOST_PAIR = 2;
export const FIRST_FLAG = "www.survivalnetwork.az";
export const PUBLIC_PAIR = Object.freeze(["azgrid", "azbooth"]);
export const AZNET_SIDE = Object.freeze(["azcloak", "azvault", "azshift", "azflag", "azstandby"]);

export const HUB_AE = "https://www.azieleliab.com/";
export const HUB_CORPUS = "https://www.azielcorpuslibrary.net/";
export const HUB_GODLOCK = "https://godlock.uk/";
export const HUB_HDJ = "https://hedidntjump.com/";

export const CAP7_FACTORY_SITES = Object.freeze([
  {
    label: "azgrid",
    role: "factory-grid",
    design: "azieleliab software/runtime hub design DNA",
    canonical_hub: HUB_AE,
    design_of: HUB_AE,
    reach: "https-gateway",
    browser_reachable: true,
  },
  {
    label: "azbooth",
    role: "factory-booth",
    design: "azieleliab session-booth design DNA",
    canonical_hub: HUB_AE,
    design_of: HUB_AE,
    reach: "https-gateway",
    browser_reachable: true,
  },
  {
    label: "azcloak",
    role: "factory-cloak",
    design: "godlock cloak/dark design DNA",
    canonical_hub: HUB_GODLOCK,
    design_of: HUB_GODLOCK,
    reach: "aznet",
    browser_reachable: false,
  },
  {
    label: "azvault",
    role: "factory-vault",
    design: "corpus vault/shelf design DNA",
    canonical_hub: HUB_CORPUS,
    design_of: HUB_CORPUS,
    reach: "aznet",
    browser_reachable: false,
  },
  {
    label: "azshift",
    role: "factory-shift",
    design: "hedidntjump shift/standby design DNA",
    canonical_hub: HUB_HDJ,
    design_of: HUB_HDJ,
    reach: "aznet",
    browser_reachable: false,
  },
  {
    label: "azflag",
    role: "factory-flag",
    design: "corpus cite/flag design DNA",
    canonical_hub: HUB_CORPUS,
    design_of: HUB_CORPUS,
    reach: "aznet",
    browser_reachable: false,
  },
  {
    label: "azstandby",
    role: "factory-standby",
    design: "godlock standby/mask design DNA",
    canonical_hub: HUB_GODLOCK,
    design_of: HUB_GODLOCK,
    reach: "aznet",
    browser_reachable: false,
  },
]);

export const FACTORY_LABELS = Object.freeze(CAP7_FACTORY_SITES.map((s) => s.label));

export function personId() {
  return { "@id": PERSON_ID, name: IDENTITY };
}

export function appWorker() {
  return {
    url: APP_HOST,
    host: "miragegrid.vibelock.workers.dev",
    worker_name: "miragegrid",
    status: "live-app",
    http: 200,
    cite: true,
    role: "cap-7-shuffle-app",
    download_plane: DOWNLOAD_HOST,
    historical_cf_1042: "closed-by-creating-worker-miragegrid",
    note: "Named app Worker (Cap-7 LIVE shuffle + FragGate doors). Download-tracker stays the counted download plane. Historical CF 1042 (Worker missing / 10007) is closed by this Worker.",
    author: IDENTITY,
    identity: IDENTITY,
  };
}

export function downloadWorker() {
  return {
    url: DOWNLOAD_HOST,
    host: "miragegrid-download-tracker.vibelock.workers.dev",
    worker_name: "miragegrid-download-tracker",
    status: "live-download",
    cite: true,
    role: "counted-download",
    app_plane: APP_HOST,
    note: "Counted download plane. Isolated from the named app Worker.",
    author: IDENTITY,
    identity: IDENTITY,
  };
}

export function siteRecord(site) {
  const label = site.label;
  const publicPair = !!site.browser_reachable;
  const path = publicPair ? "/cap7/" + label : "/aznet/cap7/" + label;
  return {
    label,
    mesh_name: label + ".az",
    role: site.role,
    design: site.design,
    canonical_hub: site.canonical_hub,
    design_of: site.design_of,
    resolves_to_hub: false,
    name_may_change: true,
    public_icann: false,
    icann: false,
    fifth_product: false,
    radio_phy: false,
    reach: site.reach,
    honesty_public: publicPair ? "LIVE" : "SLOT",
    browser_reachable: publicPair,
    aznet: true,
    azbrowser: true,
    merge: false,
    mesh_name_icann: "SLOT",
    worker_path: APP_HOST + path,
    aznet_endpoint: "aznet://cap7/" + label,
    update_path: publicPair ? APP_HOST + path + "/update" : "aznet://cap7/" + label + "/update",
    person: personId(),
    author: IDENTITY,
  };
}

export function cap7Roster() {
  return CAP7_FACTORY_SITES.map(siteRecord);
}

export function findSite(label) {
  const key = String(label || "").trim().toLowerCase();
  return CAP7_FACTORY_SITES.find((s) => s.label === key) || null;
}

export function cap7ShuffleDict() {
  return {
    law: "CAP-7 LIVE SHUFFLE",
    spec: CAP7_SHUFFLE_SPEC,
    author: IDENTITY,
    identity: IDENTITY,
    person: personId(),
    cap: CAP_7,
    public_host_pair: PUBLIC_HOST_PAIR,
    public_pair: PUBLIC_PAIR.slice(),
    aznet_side: AZNET_SIDE.slice(),
    labels: FACTORY_LABELS.slice(),
    sites: cap7Roster(),
    resolves_to_hub: false,
    name_may_change: true,
    public_icann: false,
    fifth_product: false,
    radio_phy: false,
    hardcoded_host: false,
    update_is_proof: true,
    az_generator: {
      callable: false,
      lives: "deep-node",
      exit: "node-gate-front",
      radio_phy: false,
      public_icann: false,
    },
    access: { aznet: true, azbrowser: true, merge: false, naked_public_dns: false },
    app_worker: appWorker(),
    download_worker: downloadWorker(),
    first_flag: FIRST_FLAG,
    invented_first_flag_https: false,
    canonical_hubs: [HUB_AE, HUB_CORPUS, HUB_GODLOCK, HUB_HDJ],
    named_mesh_designs: ["azcorpus", "azlibrary"],
    note: "Nodes ping the app Worker until they land on one Cap-7 site. That land is the update endpoint for the round. No single hard-coded Cap-7 host.",
  };
}

export function hostedBridgeDoors() {
  const law = cap7ShuffleDict();
  return {
    ok: true,
    code: "BRIDGE-CAP7-SHUFFLE",
    spec: SEMANTIC_BRIDGE_SPEC,
    shuffle_spec: CAP7_SHUFFLE_SPEC,
    author: IDENTITY,
    identity: IDENTITY,
    person: personId(),
    public_icann: false,
    resolves_to_hub: false,
    name_may_change: true,
    fifth_product: false,
    radio_phy: false,
    hardcoded_host: false,
    app_worker: appWorker(),
    download_worker: downloadWorker(),
    runtime: RUNTIME,
    aznet: "aznet",
    azbrowser: "azbrowser",
    merge: false,
    cap7: law.sites,
    public_pair: PUBLIC_PAIR.slice(),
    aznet_side: AZNET_SIDE.slice(),
    doors: {
      bridge: APP_HOST + "/bridge",
      bridge_json: APP_HOST + "/bridge.json",
      v1_bridge: APP_HOST + "/v1/bridge",
      shuffle: APP_HOST + "/v1/shuffle",
      ping: APP_HOST + "/v1/shuffle/ping",
      land: APP_HOST + "/v1/shuffle/land",
      cap7: APP_HOST + "/v1/cap7",
    },
    first_flag: FIRST_FLAG,
    invented_first_flag_https: false,
    honesty: {
      app_worker: "LIVE",
      download_worker: "LIVE",
      public_pair_https: "LIVE",
      aznet_side_https: "SLOT",
      mesh_az_icann: "SLOT",
      first_flag_https: "SLOT",
    },
    az_generator: law.az_generator,
    note: law.note,
  };
}

export function publicGateway(label) {
  const site = findSite(label);
  if (!site) {
    return {
      ok: false,
      code: "BRIDGE-NO-PUBLIC-DNS",
      verdict: "refuse",
      yes: false,
      message: "unknown Cap-7 factory label; mesh .az is not public ICANN DNS",
      public_icann: false,
      author: IDENTITY,
    };
  }
  const row = siteRecord(site);
  if (!row.browser_reachable) {
    return {
      ok: false,
      code: "CAP7-SLOT-NOT-LIVE",
      verdict: "refuse",
      yes: false,
      message: "this Cap-7 slot is AZNet-side; do not invent public HTTPS LIVE",
      label: row.label,
      honesty_public: "SLOT",
      browser_reachable: false,
      aznet: true,
      aznet_endpoint: row.aznet_endpoint,
      public_icann: false,
      spec: CAP7_SHUFFLE_SPEC,
      author: IDENTITY,
    };
  }
  return {
    ok: true,
    code: "CAP7-GATEWAY-LIVE",
    verdict: "yes",
    yes: true,
    message: "browser-reachable Cap-7 public pair mirror on the app Worker (not ICANN .az)",
    ...row,
    spec: CAP7_SHUFFLE_SPEC,
    public_icann: false,
  };
}

export function aznetCite(label) {
  const site = findSite(label);
  if (!site) {
    return {
      ok: false,
      code: "CAP7-UNKNOWN",
      verdict: "refuse",
      yes: false,
      message: "unknown Cap-7 factory label",
      public_icann: false,
      author: IDENTITY,
    };
  }
  const row = siteRecord(site);
  return {
    ok: true,
    code: row.browser_reachable ? "CAP7-AZNET-AND-HTTPS" : "CAP7-AZNET-SLOT",
    verdict: "yes",
    yes: true,
    message: row.browser_reachable
      ? "public pair is Worker HTTPS + AZNet; mesh .az stays SLOT on ICANN"
      : "AZNet-hosted survival endpoint; public HTTPS is SLOT; not browser-reachable",
    ...row,
    honesty_public: row.honesty_public,
    public_https: row.browser_reachable,
    aznet_plane: true,
    spec: CAP7_SHUFFLE_SPEC,
  };
}
