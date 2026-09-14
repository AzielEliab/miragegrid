/**
 * SEMANTIC-BRIDGE-1.0 — AI discovery of Cap-7 names without faking ICANN DNS.
 * Public Plane-A + this Worker are the crawler bridge. Mesh names stay
 * mesh-authoritative (public_icann:false). design_of is hub design
 * provenance only. resolves_to_hub is always false.
 * Author: Aziel Eliab only. Person @id https://www.azieleliab.com/#aziel
 */

export const SEMANTIC_BRIDGE_SPEC = "SEMANTIC-BRIDGE-1.0";
export const CROSS_NETWORK_SURVIVAL = "CROSS-NETWORK-SURVIVAL-1.0";
export const PERSON_ID = "https://www.azieleliab.com/#aziel";
export const IDENTITY = "Aziel Eliab";
export const HOST = "https://miragegrid-download-tracker.vibelock.workers.dev";
export const AZ_GENERATOR_CITE = HOST + "/v1/mesh/az-generator";
export const FIRST_FLAG = "www.survivalnetwork.az";
export const SUFFIX_ORDER = Object.freeze([".az", ".aziel", "pivot"]);
export const PUBLIC_HOST_PAIR = 2;
export const CAP_7 = 7;
export const GROWTH = "Growth-ON";
export const REEXPAND = "archive-not-index";

export const DESIGN_HUBS = Object.freeze([
  {
    design_of: "https://www.azieleliab.com/",
    label: "azieleliab",
    role: "design-provenance",
    resolves_to_hub: false,
  },
  {
    design_of: "https://www.azielcorpuslibrary.net/",
    label: "azielcorpuslibrary",
    designs: ["azcorpus", "azlibrary"],
    role: "design-provenance",
    resolves_to_hub: false,
  },
  {
    design_of: "https://godlock.uk/",
    label: "godlock",
    role: "design-provenance",
    resolves_to_hub: false,
  },
  {
    design_of: "https://hedidntjump.com/",
    label: "hedidntjump",
    role: "design-provenance",
    resolves_to_hub: false,
  },
]);

const HUB_HOSTS = new Set([
  "azieleliab.com",
  "www.azieleliab.com",
  "azielcorpuslibrary.net",
  "www.azielcorpuslibrary.net",
  "godlock.uk",
  "www.godlock.uk",
  "hedidntjump.com",
  "www.hedidntjump.com",
]);

const DESIGN_BY_HOST = {
  "azieleliab.com": "https://www.azieleliab.com/",
  "www.azieleliab.com": "https://www.azieleliab.com/",
  "azielcorpuslibrary.net": "https://www.azielcorpuslibrary.net/",
  "www.azielcorpuslibrary.net": "https://www.azielcorpuslibrary.net/",
  "godlock.uk": "https://godlock.uk/",
  "www.godlock.uk": "https://godlock.uk/",
  "hedidntjump.com": "https://hedidntjump.com/",
  "www.hedidntjump.com": "https://hedidntjump.com/",
};

const ACCESS_VALUES = new Set(["aznet", "azbrowser", "https-gateway"]);

export function personId() {
  return { "@id": PERSON_ID, name: IDENTITY };
}

export function semanticBridgeDict() {
  return {
    law: "SEMANTIC BRIDGE",
    spec: SEMANTIC_BRIDGE_SPEC,
    author: IDENTITY,
    identity: IDENTITY,
    person: personId(),
    growth: GROWTH,
    public_icann: false,
    registrar: false,
    unbounded_public_dns: false,
    cctld_takeover: false,
    resolves_to_hub: false,
    name_may_change: true,
    reexpand: REEXPAND,
    cross_network_survival: CROSS_NETWORK_SURVIVAL,
    no_lie: true,
    no_rewrite: true,
    no_fan: "NO-FAN-1.0",
    first_flag: FIRST_FLAG,
    suffix_order: SUFFIX_ORDER.slice(),
    public_host_pair: PUBLIC_HOST_PAIR,
    cap: CAP_7,
    az_generator_cite: AZ_GENERATOR_CITE,
    access: { aznet: true, azbrowser: true, merge: false, naked_public_dns: false },
    design_catalog: DESIGN_HUBS.map((row) => ({ ...row })),
    plane_a: [HOST + "/"].concat(DESIGN_HUBS.map((row) => row.design_of)),
    softwares_tab: false,
    callable: false,
  };
}

export function cap7BridgeCite() {
  return {
    spec: SEMANTIC_BRIDGE_SPEC,
    first_flag: FIRST_FLAG,
    suffix_order: SUFFIX_ORDER.slice(),
    public_host_pair: PUBLIC_HOST_PAIR,
    public_icann: false,
    access: { aznet: true, azbrowser: true, merge: false, naked_public_dns: false },
    aznet: true,
    azbrowser: true,
    cite: AZ_GENERATOR_CITE,
    person: personId(),
    resolves_to_hub: false,
    name_may_change: true,
    growth: GROWTH,
    cross_network_survival: CROSS_NETWORK_SURVIVAL,
    no_lie: true,
  };
}

function verdict(ok, code, v, message, extra) {
  return {
    ok: !!ok,
    code,
    verdict: v,
    yes: v === "yes",
    message,
    author: IDENTITY,
    identity: IDENTITY,
    ...(extra || {}),
  };
}

export function refusePublicDnsClaim(kind) {
  return verdict(false, "BRIDGE-NO-PUBLIC-DNS", "refuse", "mesh .az is not public ICANN DNS; do not claim public resolution", {
    kind: kind || "az-public-dns",
    public_icann: false,
    spec: SEMANTIC_BRIDGE_SPEC,
    no_lie: true,
  });
}

export function refuseAzgIcannPublish(kind) {
  return verdict(false, "BRIDGE-NO-ICANN-PUBLISH", "refuse", "AZ Generator does not live-publish to ICANN; Worker cites only", {
    kind: kind || "azg-icann-publish",
    public_icann: false,
    callable: false,
    spec: SEMANTIC_BRIDGE_SPEC,
  });
}

export function refuseHubResolution(name, hub) {
  return verdict(false, "BRIDGE-NO-HUB-RESOLVE", "refuse", "mesh names do not resolve, redirect, or CNAME to ICANN hubs; design_of is provenance only", {
    name: name || "",
    hub: hub || "",
    resolves_to_hub: false,
    public_icann: false,
    spec: SEMANTIC_BRIDGE_SPEC,
  });
}

export function refuseInventFirstFlagHttps(name) {
  return verdict(false, "BRIDGE-NO-INVENT-HTTPS", "refuse", "empty Cap-7: do not invent www.survivalnetwork.az as live HTTPS", {
    name: name || FIRST_FLAG,
    invented_first_flag_https: false,
    honesty: "empty-cap-7",
    spec: SEMANTIC_BRIDGE_SPEC,
    no_lie: true,
  });
}

function hostOf(value) {
  let text = String(value == null ? "" : value).trim().toLowerCase();
  if (text.startsWith("https://")) text = text.slice(8);
  else if (text.startsWith("http://")) text = text.slice(7);
  return text.split("/")[0].split(":")[0].replace(/\.+$/, "");
}

function isHubHost(value) {
  return HUB_HOSTS.has(hostOf(value));
}

export function normalizeDesignOf(value) {
  if (value == null || value === false) return null;
  const raw = String(value).trim();
  if (!raw) return null;
  const host = hostOf(raw);
  if (DESIGN_BY_HOST[host]) return DESIGN_BY_HOST[host];
  const withSlash = raw.endsWith("/") ? raw : raw + "/";
  for (const row of DESIGN_HUBS) {
    if (withSlash === row.design_of || raw === row.design_of || raw.replace(/\/+$/, "") === row.design_of.replace(/\/+$/, "")) {
      return row.design_of;
    }
  }
  return null;
}

function hex64(value) {
  const text = String(value == null ? "" : value).trim().toLowerCase();
  return /^[0-9a-f]{64}$/.test(text) ? text : null;
}

function asClaim(raw) {
  if (raw == null) return null;
  if (typeof raw === "string") {
    const host = hostOf(raw);
    return host ? { name: host } : null;
  }
  if (typeof raw !== "object") return null;
  const name = raw.name || raw.host || raw.mesh_name || raw.url;
  const host = hostOf(name);
  if (!host) return null;
  return { ...raw, name: host };
}

function accessFor(claim, hostedGateway) {
  const requested = String(claim.access || "").trim().toLowerCase().replace(/_/g, "-");
  if (hostedGateway) return "https-gateway";
  if (ACCESS_VALUES.has(requested) && requested !== "https-gateway") return requested;
  return "aznet";
}

function entryFromClaim(claim) {
  const host = String(claim.name || "");
  if (isHubHost(host)) return refuseHubResolution(host, host);
  if (claim.resolves_to_hub === true || claim.cname_to_hub || claim.redirect_to_hub) {
    return refuseHubResolution(host, String(claim.hub || claim.design_of || ""));
  }
  const gateway = claim.public_gateway_url || claim.gateway_url || "";
  if (gateway && isHubHost(gateway)) return refuseHubResolution(host, String(gateway));
  if (claim.icann === true || claim.public_icann === true) return refusePublicDnsClaim("claim-icann");

  const designOf = normalizeDesignOf(claim.design_of);
  const publicHost = !!(claim.public_host || claim.plane === "public-gateway");
  const hosted = !!gateway && !isHubHost(gateway) && publicHost;
  let status = "mesh-only";
  let publicGatewayUrl = null;
  if (publicHost && hosted) {
    status = "https-gateway";
    publicGatewayUrl = String(gateway).trim();
  } else if (publicHost) {
    status = "claimed-unhosted";
  }

  const receipt = claim.receipt && typeof claim.receipt === "object" ? claim.receipt : {};
  const tip = hex64(claim.tip_sha256 || claim.tip_hash || claim.sha256 || receipt.hash);
  const pack = hex64(claim.design_pack_sha256 || claim.design_pack || claim.pack_sha256);
  const entry = {
    status,
    access: accessFor(claim, hosted),
    icann: false,
    resolves_to_hub: false,
    name_may_change: true,
  };
  if (tip) entry.tip_sha256 = tip;
  if (pack) entry.design_pack_sha256 = pack;
  if (publicGatewayUrl) entry.public_gateway_url = publicGatewayUrl;
  if (designOf) entry.design_of = designOf;
  return entry;
}

export function buildBridgeRegistry(claims, opts) {
  const options = opts && typeof opts === "object" ? opts : {};
  if (options.public_icann || options.public_dns) return refusePublicDnsClaim("registry-public-dns");
  if (options.icann_publish) return refuseAzgIcannPublish();
  if (options.resolve_to_hub) return refuseHubResolution();

  const records = Array.isArray(claims) ? claims : [];
  if (options.zone && Array.isArray(options.zone.records)) records.push(...options.zone.records);
  else if (options.zone && typeof options.zone.names === "function") {
    records.push(...options.zone.names().map((n) => ({ name: n })));
  }

  const names = {};
  for (const raw of records) {
    const claim = asClaim(raw);
    if (!claim) continue;
    const row = entryFromClaim(claim);
    if (row && row.ok === false) return row;
    names[claim.name] = row;
  }

  if (options.invent_first_flag && !names[FIRST_FLAG]) return refuseInventFirstFlagHttps();

  const first = names[FIRST_FLAG];
  if (first && first.status === "https-gateway" && !first.public_gateway_url) {
    return refuseInventFirstFlagHttps();
  }

  const empty = Object.keys(names).length === 0;
  return verdict(
    true,
    empty ? "BRIDGE-EMPTY" : "BRIDGE-OK",
    "yes",
    empty
      ? "empty Cap-7: SLOT empty list; first-flag is cited, not hosted HTTPS"
      : "Cap-7 claims listed honestly; mesh-authoritative; not ICANN; design_of is provenance only",
    {
      spec: SEMANTIC_BRIDGE_SPEC,
      public_icann: false,
      resolves_to_hub: false,
      name_may_change: true,
      honesty: empty ? "empty-cap-7" : "claimed",
      names,
      slots: [],
      claimed: Object.keys(names).length,
      cap: CAP_7,
      public_host_pair: PUBLIC_HOST_PAIR,
      invented_first_flag_https: false,
      first_flag: FIRST_FLAG,
      suffix_order: SUFFIX_ORDER.slice(),
      design_catalog: DESIGN_HUBS.map((row) => ({ ...row })),
      person: personId(),
      cite: AZ_GENERATOR_CITE,
      access: { aznet: true, azbrowser: true, merge: false, naked_public_dns: false },
      reexpand: REEXPAND,
      growth: GROWTH,
      cross_network_survival: CROSS_NETWORK_SURVIVAL,
      no_lie: true,
      no_rewrite: true,
    },
  );
}

export function hostedBridgeDocument() {
  return {
    ...semanticBridgeDict(),
    ...buildBridgeRegistry([]),
    code: "BRIDGE-EMPTY",
    honesty: "empty-cap-7",
    names: {},
    slots: [],
    claimed: 0,
    invented_first_flag_https: false,
  };
}

export function contentSignal() {
  return "ai-input=yes, ai-train=yes, search=yes";
}

export function robotsTxt() {
  const sitemap = "Sitemap: " + HOST + "/sitemap.xml";
  const signal = "Content-Signal: " + contentSignal();
  const agents = ["GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-User", "anthropic-ai", "PerplexityBot", "Google-Extended"];
  const lines = [
    "# SEMANTIC-BRIDGE-1.0 — Growth-ON. Mesh .az is not public ICANN DNS.",
    "User-agent: *",
    "Allow: /",
    signal,
    sitemap,
    "",
  ];
  for (const agent of agents) {
    lines.push("User-agent: " + agent, "Allow: /", "");
  }
  return lines.join("\n");
}

export function sitemapXml() {
  const locs = [
    HOST + "/",
    HOST + "/download",
    HOST + "/install.sh",
    HOST + "/v1/skill",
    HOST + "/v1/mesh",
    HOST + "/v1/mesh/az-generator",
    HOST + "/v1/bridge",
    HOST + "/openapi.json",
    HOST + "/cite.json",
    HOST + "/llms.txt",
    HOST + "/ai.txt",
    HOST + "/bridge.json",
    "https://github.com/AzielEliab/miragegrid",
  ];
  return (
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    locs.map((u) => "  <url><loc>" + u + "</loc></url>").join("\n") +
    "\n</urlset>\n"
  );
}

export function llmsTxt() {
  return [
    "# MirageGrid",
    "> Ephemeral session node assignment. Not a VPN and not an anonymity network.",
    "",
    "Author: Aziel Eliab only",
    "Person @id: " + PERSON_ID,
    "",
    "## SEMANTIC-BRIDGE-1.0",
    "Public Plane-A ICANN hosts + this Worker are the AI-facing bridge.",
    "Cap-7 mesh names are mesh-authoritative. public_icann:false.",
    "Do not resolve .az on public DNS. Crawlers pull from the URLs below.",
    "Re-expand is archive, not index. CROSS-NETWORK-SURVIVAL + NO-LIE.",
    "Growth-ON.",
    "",
    "Cap-7 factory: deep-node → FRONT Node Gate. Not callable.",
    "Suffix order: .az → .aziel → pivot. public_host_pair: 2.",
    "Access: AZNet + AZBrowser pairing. Not naked public DNS.",
    "",
    "Mesh sites inherit hub *design* only. They do not resolve/CNAME/redirect",
    "to azieleliab.com, azielcorpuslibrary.net, godlock.uk, or hedidntjump.com.",
    "design_of = design provenance. resolves_to_hub:false. name_may_change:true.",
    "Empty Cap-7 → SLOT empty list. Do not invent www.survivalnetwork.az as live HTTPS.",
    "",
    "## Machine maps",
    "- " + HOST + "/llms.txt",
    "- " + HOST + "/ai.txt",
    "- " + HOST + "/cite.json",
    "- " + HOST + "/bridge.json",
    "- " + HOST + "/v1/bridge",
    "- " + HOST + "/v1/mesh/az-generator",
    "- " + HOST + "/sitemap.xml",
    "- " + HOST + "/robots.txt",
    "",
    "## Design catalog (provenance only — not resolution)",
    "- https://www.azieleliab.com/",
    "- https://www.azielcorpuslibrary.net/ (azcorpus + azlibrary)",
    "- https://godlock.uk/",
    "- https://hedidntjump.com/",
    "",
    "License: Apache-2.0",
    "",
  ].join("\n");
}

export function aiTxt() {
  return [
    "SEMANTIC-BRIDGE-1.0",
    "public_icann:false",
    "resolves_to_hub:false",
    "name_may_change:true",
    "first_flag:" + FIRST_FLAG,
    "suffix_order:.az,.aziel,pivot",
    "public_host_pair:2",
    "access:aznet,azbrowser",
    "growth:" + GROWTH,
    "reexpand:" + REEXPAND,
    "cross_network_survival:" + CROSS_NETWORK_SURVIVAL,
    "no_lie:true",
    "honesty:empty-cap-7-unless-local-claims",
    "person:" + PERSON_ID,
    "cite:" + AZ_GENERATOR_CITE,
    "bridge:" + HOST + "/v1/bridge",
    "llms:" + HOST + "/llms.txt",
    "do_not_invent_survivalnetwork_https:true",
    "do_not_resolve_mesh_to_hub:true",
    "",
  ].join("\n");
}

export function discoveryHeaders(contentType) {
  return {
    "Content-Type": contentType,
    "Cache-Control": "public, max-age=300",
    "Content-Signal": contentSignal(),
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept, User-Agent",
  };
}
