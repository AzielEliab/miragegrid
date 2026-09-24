/**
 * CAP7-SHUFFLE-1.0 — MirageGrid-only factory roster.
 * Cap-7 auto-generates .az hub duplications and shifts them with
 * StaticLock + MirageGrid cloak and VPN. Four real, three decoys.
 * Not typed on ICANN DNS. Internet reaches AZ domains only.
 * Author: Aziel Eliab only.
 */

import { outlastHonesty } from "../../download-tracker/src/mesh.js";

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

export const HUB_AE = "https://www.azieleliab.com/";
export const HUB_CORPUS = "https://www.azielcorpuslibrary.net/";
export const HUB_GODLOCK = "https://godlock.uk/";
export const HUB_HDJ = "https://hedidntjump.com/";

export const AZ_DOMAIN_DROP_INS = Object.freeze([
  { display_name: "AZ.AzielEliab.AZ", mirror_host: "azieleliab.com", canonical_hub: HUB_AE },
  { display_name: "AZ.AzielCorpusLibrary.AZ", mirror_host: "azielcorpuslibrary.net", canonical_hub: HUB_CORPUS },
  { display_name: "AZ.Godlock.AZ", mirror_host: "godlock.uk", canonical_hub: HUB_GODLOCK },
  { display_name: "AZ.HeDidntJump.AZ", mirror_host: "hedidntjump.com", canonical_hub: HUB_HDJ },
]);
export const REAL_HUB_DUPLICATIONS = Object.freeze(["azgrid", "azcloak", "azvault", "azshift"]);
export const FALSE_SITES = Object.freeze(["azbooth", "azflag", "azstandby"]);
export const SHIFT_STACK = Object.freeze(["staticlock", "miragegrid-cloak", "miragegrid-vpn"]);

export function azDomainRows() {
  return AZ_DOMAIN_DROP_INS.map((row) => ({
    display_name: row.display_name,
    mirror_host: row.mirror_host,
    canonical_hub: row.canonical_hub,
    internet_url: row.canonical_hub,
    public_icann: true,
    resolves_to_hub: true,
    internet_reachable: true,
    honesty: "LIVE",
    shuffle_once: true,
    pool: 4,
    mirrors_while_up: true,
    stands_alone: true,
    immutable_after_hub_down: true,
    anchored_by_live_nodes: true,
    domain_anchor: "live-nodes",
    softwares_tab: false,
    cap7: false,
    icann_registrar_purchase: false,
    cctld_purchase: false,
    author: IDENTITY,
  }));
}

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
  const real = REAL_HUB_DUPLICATIONS.includes(label);
  const falseSite = FALSE_SITES.includes(label);
  const path = "/cap7/" + label;
  const drop = AZ_DOMAIN_DROP_INS.find((row) => row.canonical_hub === site.canonical_hub);
  return {
    label,
    mesh_name: label + ".az",
    role: site.role,
    design: site.design,
    canonical_hub: site.canonical_hub,
    design_of: site.design_of,
    layer: "cap7-az-duplication",
    generates: "auto-.az-hub-duplication",
    hub_duplication: real,
    false_site: falseSite,
    decoy: falseSite,
    resolves_to_hub: real,
    name_may_change: true,
    public_icann: false,
    typed_on_icann_dns: false,
    internet_reachable: false,
    public_internet_door: false,
    icann: false,
    fifth_product: false,
    radio_phy: false,
    reach: "cap7-shift",
    honesty_public: "LIVE",
    factory_honesty: "LIVE",
    browser_reachable: false,
    aznet: true,
    azbrowser: true,
    merge: false,
    worker_path: APP_HOST + path,
    aznet_endpoint: "aznet://cap7/" + label,
    update_path: APP_HOST + "/v1/shuffle/update",
    hosted_status: "LIVE",
    hosted_update: "LIVE",
    hosted_mcp: "LIVE",
    public_shuffle_land_exec: "LIVE",
    anchored_by_live_nodes: true,
    domain_anchor: "live-nodes",
    shift_stack: SHIFT_STACK.slice(),
    staticlock: true,
    miragegrid_cloak: true,
    miragegrid_vpn: true,
    internet_door: drop ? drop.display_name : null,
    is_live_door: false,
    aznet_payload_host: false,
    channel_plane_is_vpn: false,
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
    labels: FACTORY_LABELS.slice(),
    sites: cap7Roster(),
    real_hub_duplications: REAL_HUB_DUPLICATIONS.slice(),
    false_sites: FALSE_SITES.slice(),
    real_duplication_count: 4,
    false_site_count: 3,
    az_domains: azDomainRows(),
    internet_reaches: "az-domains",
    typed_on_icann_dns: false,
    internet_reachable: false,
    name_may_change: true,
    fifth_product: false,
    radio_phy: false,
    hardcoded_host: false,
    update_is_proof: true,
    shift_stack: SHIFT_STACK.slice(),
    staticlock: true,
    miragegrid_cloak: true,
    miragegrid_vpn: true,
    az_generator: {
      callable: false,
      lives: "deep-node",
      exit: "node-gate-front",
      radio_phy: false,
      typed_on_icann_dns: false,
    },
    access: { aznet: true, azbrowser: true, merge: false, naked_public_dns: false },
    app_worker: appWorker(),
    download_worker: downloadWorker(),
    first_flag: FIRST_FLAG,
    invented_first_flag_https: false,
    canonical_hubs: [HUB_AE, HUB_CORPUS, HUB_GODLOCK, HUB_HDJ],
    named_mesh_designs: ["azcorpus", "azlibrary"],
    ...outlastHonesty(),
    note: "Cap-7 auto-generates .az duplications of the four hubs and shifts them with StaticLock + MirageGrid cloak and VPN. Four names are real hub duplications; three are false sites. Internet reaches AZ domains only, via hub HTTPS. Factory honesty is LIVE. Live nodes anchor the factory and the AZ doors. FragGate stays THE door.",
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
    typed_on_icann_dns: false,
    internet_reachable: false,
    internet_reaches: "az-domains",
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
    real_hub_duplications: REAL_HUB_DUPLICATIONS.slice(),
    false_sites: FALSE_SITES.slice(),
    real_duplication_count: 4,
    false_site_count: 3,
    az_domains: azDomainRows(),
    shift_stack: SHIFT_STACK.slice(),
    doors: {
      bridge: APP_HOST + "/bridge",
      bridge_json: APP_HOST + "/bridge.json",
      v1_bridge: APP_HOST + "/v1/bridge",
      shuffle: APP_HOST + "/v1/shuffle",
      ping: APP_HOST + "/v1/shuffle/ping",
      land: APP_HOST + "/v1/shuffle/land",
      update: APP_HOST + "/v1/shuffle/update",
      cap7: APP_HOST + "/v1/cap7",
    },
    first_flag: FIRST_FLAG,
    invented_first_flag_https: false,
    honesty: {
      app_worker: "LIVE",
      download_worker: "LIVE",
      factory: "LIVE",
      az_domains: "LIVE",
      cap7_icann_dns: false,
      hosted_endpoints: "LIVE",
      hosted_update: "LIVE",
      hosted_mcp: "LIVE",
      public_shuffle_land_exec: "LIVE",
      anchored_by_live_nodes: true,
      channel_plane_is_vpn: false,
      second_door: false,
    },
    ...outlastHonesty(),
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
  return {
    ok: true,
    code: "CAP7-FACTORY-LIVE",
    verdict: "yes",
    yes: true,
    message: "LIVE Cap-7 factory site (duplication/shift/cloak). Not an ICANN public door. Internet reaches AZ domains via hub HTTPS.",
    ...row,
    spec: CAP7_SHUFFLE_SPEC,
    az_domains: azDomainRows(),
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
    code: "CAP7-FACTORY-LIVE",
    verdict: "yes",
    yes: true,
    message: "LIVE Cap-7 factory cite on the AZNet plane. Not typed on ICANN DNS. Internet reaches AZ domains via hub HTTPS.",
    ...row,
    honesty_public: "LIVE",
    factory_honesty: "LIVE",
    public_https: false,
    aznet_plane: true,
    hosted_endpoints: "LIVE",
    aznet_payload_host: false,
    is_live_door: false,
    internet_reachable: false,
    typed_on_icann_dns: false,
    spec: CAP7_SHUFFLE_SPEC,
  };
}
