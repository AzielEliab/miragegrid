/**
 * SEMANTIC-BRIDGE-1.0 — AI discovery of Cap-7 names without faking ICANN DNS.
 * Mesh names are relocatable labels (name_may_change). Not a fifth product.
 * azcorpus + azlibrary are designs inside azielcorpuslibrary.net.
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
export const PREFERRED_PUBLIC_PAIR = Object.freeze(["azcorpus", "azlibrary"]);
export const CORPUS_HUB = "https://www.azielcorpuslibrary.net/";

export const CANONICAL_HUBS = Object.freeze([
  { canonical_hub: "https://www.azieleliab.com/", label: "azieleliab", role: "canonical-hub", fifth_product: false },
  {
    canonical_hub: CORPUS_HUB,
    label: "azielcorpuslibrary",
    designs: ["azcorpus", "azlibrary"],
    role: "canonical-hub",
    fifth_product: false,
  },
  { canonical_hub: "https://godlock.uk/", label: "godlock", role: "canonical-hub", fifth_product: false },
  { canonical_hub: "https://hedidntjump.com/", label: "hedidntjump", role: "canonical-hub", fifth_product: false },
]);

export const DESIGN_HUBS = CANONICAL_HUBS;

export const NAMED_MESH_SITES = Object.freeze([
  {
    label: "azcorpus",
    role: "public-corpus-shelf",
    design: "public Corpus shelf site design",
    canonical_hub: CORPUS_HUB,
    design_of: CORPUS_HUB,
    download_open: true,
    upload_auth: "none",
    preferred_public_pair: true,
    fifth_product: false,
  },
  {
    label: "azlibrary",
    role: "aziel-library",
    design: "Aziel Library site design",
    canonical_hub: CORPUS_HUB,
    design_of: CORPUS_HUB,
    download_open: true,
    upload_auth: "token",
    upload_plane: "plane-a",
    preferred_public_pair: true,
    fifth_product: false,
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
  "azielcorpuslibrary.net": CORPUS_HUB,
  "www.azielcorpuslibrary.net": CORPUS_HUB,
  "godlock.uk": "https://godlock.uk/",
  "www.godlock.uk": "https://godlock.uk/",
  "hedidntjump.com": "https://hedidntjump.com/",
  "www.hedidntjump.com": "https://hedidntjump.com/",
};

const ACCESS_VALUES = new Set(["aznet", "azbrowser", "https-gateway"]);

export function personId() {
  return { "@id": PERSON_ID, name: IDENTITY };
}

export function honestMeshName(label, suffix) {
  const host = String(label || "").trim().toLowerCase().split(".")[0];
  let suf = String(suffix == null ? ".az" : suffix).trim().toLowerCase();
  if (!suf.startsWith(".")) suf = "." + suf;
  return host + suf;
}

export function preferredPublicPairLabel(name) {
  const host = String(name || "").trim().toLowerCase().split("/")[0];
  for (const label of PREFERRED_PUBLIC_PAIR) {
    if (host === label || host.startsWith(label + ".")) return label;
  }
  return null;
}

export function canonicalJson(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return "[" + value.map(canonicalJson).join(",") + "]";
  const keys = Object.keys(value).sort();
  return "{" + keys.map((k) => JSON.stringify(k) + ":" + canonicalJson(value[k])).join(",") + "}";
}

export function designPackBody(label) {
  const site = NAMED_MESH_SITES.find((s) => s.label === label);
  if (!site) return null;
  const pack = {
    author: IDENTITY,
    canonical_hub: site.canonical_hub,
    design: site.design,
    design_of: site.design_of,
    download_open: site.download_open,
    fifth_product: false,
    kind: "azg-design-pack",
    label: site.label,
    plane: "pull-only",
    public_icann: false,
    role: site.role,
    spec: SEMANTIC_BRIDGE_SPEC,
    upload_auth: site.upload_auth,
  };
  if (site.upload_plane) pack.upload_plane = site.upload_plane;
  return pack;
}

export async function sha256Hex(text) {
  const bytes = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export function designPackSha256Sync(label) {
  // Node test helper — not used on the Worker fetch path (async sha used there).
  return null;
}

function designPackUrl(label) {
  return HOST + "/design-packs/" + label + ".json";
}

export function namedMeshEntry(site, suffix, digest) {
  const label = site.label;
  const meshName = honestMeshName(label, suffix || ".az");
  const entry = {
    status: "named-mesh-site",
    label,
    role: site.role,
    design: site.design,
    mesh_name: meshName,
    suffix: String(suffix || ".az").startsWith(".") ? String(suffix || ".az") : "." + String(suffix || ".az"),
    suffix_order: SUFFIX_ORDER.slice(),
    name_may_change: true,
    canonical_hub: site.canonical_hub,
    design_of: site.design_of,
    resolves_to_hub: false,
    public_icann: false,
    icann: false,
    download_open: !!site.download_open,
    upload_auth: site.upload_auth,
    preferred_public_pair: true,
    fifth_product: false,
    access: { aznet: true, azbrowser: true, merge: false, naked_public_dns: false },
    design_pack: {
      url: designPackUrl(label),
      sha256: digest || "",
      download_open: true,
      plane: "pull-only",
    },
    tip_sha256: digest || "",
    person: personId(),
  };
  if (site.upload_plane) entry.upload_plane = site.upload_plane;
  return entry;
}

export async function designPackIndex() {
  const out = {};
  for (const site of NAMED_MESH_SITES) {
    const body = designPackBody(site.label);
    const digest = await sha256Hex(canonicalJson(body));
    out[site.label] = {
      url: designPackUrl(site.label),
      sha256: digest,
      download_open: true,
      canonical_hub: site.canonical_hub,
      plane: "pull-only",
    };
  }
  return out;
}

export async function namedMeshSites(suffix) {
  const out = {};
  for (const site of NAMED_MESH_SITES) {
    const body = designPackBody(site.label);
    const digest = await sha256Hex(canonicalJson(body));
    const entry = namedMeshEntry(site, suffix || ".az", digest);
    out[entry.mesh_name] = entry;
  }
  return out;
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
    preferred_public_pair: PREFERRED_PUBLIC_PAIR.slice(),
    cap: CAP_7,
    az_generator_cite: AZ_GENERATOR_CITE,
    access: { aznet: true, azbrowser: true, merge: false, naked_public_dns: false },
    canonical_hubs: CANONICAL_HUBS.map((row) => ({ ...row })),
    design_catalog: CANONICAL_HUBS.map((row) => ({ ...row })),
    named_mesh_sites: NAMED_MESH_SITES.map((row) => ({ ...row })),
    fifth_product: false,
    plane_a: [HOST + "/"].concat(CANONICAL_HUBS.map((row) => row.canonical_hub)),
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
    preferred_public_pair: PREFERRED_PUBLIC_PAIR.slice(),
    public_icann: false,
    access: { aznet: true, azbrowser: true, merge: false, naked_public_dns: false },
    aznet: true,
    azbrowser: true,
    cite: AZ_GENERATOR_CITE,
    person: personId(),
    resolves_to_hub: false,
    name_may_change: true,
    canonical_hubs: CANONICAL_HUBS.map((row) => row.canonical_hub),
    named_mesh_sites: PREFERRED_PUBLIC_PAIR.slice(),
    fifth_product: false,
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
  return verdict(false, "BRIDGE-NO-HUB-RESOLVE", "refuse", "mesh names do not resolve, redirect, or CNAME to ICANN hubs; canonical_hub is provenance only", {
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
  for (const row of CANONICAL_HUBS) {
    if (withSlash === row.canonical_hub || raw === row.canonical_hub || raw.replace(/\/+$/, "") === row.canonical_hub.replace(/\/+$/, "")) {
      return row.canonical_hub;
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

async function entryFromClaim(claim) {
  const host = String(claim.name || "");
  if (isHubHost(host)) return refuseHubResolution(host, host);
  if (claim.resolves_to_hub === true || claim.cname_to_hub || claim.redirect_to_hub) {
    return refuseHubResolution(host, String(claim.hub || claim.canonical_hub || claim.design_of || ""));
  }
  const gateway = claim.public_gateway_url || claim.gateway_url || "";
  if (gateway && isHubHost(gateway)) return refuseHubResolution(host, String(gateway));
  if (claim.icann === true || claim.public_icann === true) return refusePublicDnsClaim("claim-icann");

  const designOf = normalizeDesignOf(claim.design_of || claim.canonical_hub);
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
  const packObj = claim.design_pack && typeof claim.design_pack === "object" ? claim.design_pack : {};
  const tip = hex64(claim.tip_sha256 || claim.tip_hash || claim.sha256 || receipt.hash);
  const pack = hex64(claim.design_pack_sha256 || packObj.sha256 || claim.pack_sha256);
  const entry = {
    status,
    access: accessFor(claim, hosted),
    icann: false,
    public_icann: false,
    resolves_to_hub: false,
    name_may_change: true,
    fifth_product: false,
  };
  if (tip) entry.tip_sha256 = tip;
  if (pack) entry.design_pack_sha256 = pack;
  if (publicGatewayUrl) entry.public_gateway_url = publicGatewayUrl;
  if (designOf) {
    entry.design_of = designOf;
    entry.canonical_hub = designOf;
  }
  const label = preferredPublicPairLabel(host);
  if (label) {
    const site = NAMED_MESH_SITES.find((s) => s.label === label);
    const body = designPackBody(label);
    const digest = await sha256Hex(canonicalJson(body));
    entry.label = label;
    entry.canonical_hub = site.canonical_hub;
    entry.design_of = site.design_of;
    entry.download_open = site.download_open;
    entry.upload_auth = site.upload_auth;
    entry.preferred_public_pair = true;
    entry.design_pack = { url: designPackUrl(label), sha256: digest, download_open: true, plane: "pull-only" };
    if (!entry.tip_sha256) entry.tip_sha256 = digest;
    if (site.upload_plane) entry.upload_plane = site.upload_plane;
  }
  return entry;
}

export async function buildBridgeRegistry(claims, opts) {
  const options = opts && typeof opts === "object" ? opts : {};
  if (options.public_icann || options.public_dns) return refusePublicDnsClaim("registry-public-dns");
  if (options.icann_publish) return refuseAzgIcannPublish();
  if (options.resolve_to_hub) return refuseHubResolution();

  const records = Array.isArray(claims) ? claims.slice() : [];
  if (options.zone && Array.isArray(options.zone.records)) records.push(...options.zone.records);
  else if (options.zone && typeof options.zone.names === "function") {
    records.push(...options.zone.names().map((n) => ({ name: n })));
  }

  const includeNamed = options.include_named_sites !== false;
  const names = includeNamed ? await namedMeshSites(options.suffix || ".az") : {};
  const claimedNames = {};
  for (const raw of records) {
    const claim = asClaim(raw);
    if (!claim) continue;
    const row = await entryFromClaim(claim);
    if (row && row.ok === false) return row;
    claimedNames[claim.name] = row;
    names[claim.name] = row;
  }

  if (options.invent_first_flag && !claimedNames[FIRST_FLAG]) return refuseInventFirstFlagHttps();

  const first = claimedNames[FIRST_FLAG];
  if (first && first.status === "https-gateway" && !first.public_gateway_url) {
    return refuseInventFirstFlagHttps();
  }

  const empty = Object.keys(claimedNames).length === 0;
  return verdict(
    true,
    empty ? "BRIDGE-EMPTY" : "BRIDGE-OK",
    "yes",
    empty
      ? "empty Cap-7 SLOT; named mesh sites azcorpus+azlibrary cited as designs, not live ICANN"
      : "Cap-7 claims listed honestly; named mesh sites stay designs of the four hubs",
    {
      spec: SEMANTIC_BRIDGE_SPEC,
      public_icann: false,
      resolves_to_hub: false,
      name_may_change: true,
      honesty: empty ? "empty-cap-7" : "claimed",
      names,
      slots: [],
      claimed: Object.keys(claimedNames).length,
      cap: CAP_7,
      public_host_pair: PUBLIC_HOST_PAIR,
      preferred_public_pair: PREFERRED_PUBLIC_PAIR.slice(),
      invented_first_flag_https: false,
      first_flag: FIRST_FLAG,
      suffix_order: SUFFIX_ORDER.slice(),
      canonical_hubs: CANONICAL_HUBS.map((row) => ({ ...row })),
      design_catalog: CANONICAL_HUBS.map((row) => ({ ...row })),
      named_mesh_sites: NAMED_MESH_SITES.map((row) => ({ ...row })),
      design_packs: await designPackIndex(),
      fifth_product: false,
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

export async function hostedBridgeDocument() {
  const named = await namedMeshSites(".az");
  const packs = await designPackIndex();
  return {
    ...semanticBridgeDict(),
    ...(await buildBridgeRegistry([])),
    code: "BRIDGE-EMPTY",
    honesty: "empty-cap-7",
    names: named,
    slots: [],
    claimed: 0,
    invented_first_flag_https: false,
    design_packs: packs,
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
    HOST + "/design-packs/azcorpus.json",
    HOST + "/design-packs/azlibrary.json",
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
    "Cap-7 mesh names are relocatable labels. public_icann:false. name_may_change:true.",
    "Not a fifth public product. The four online hubs stay canonical.",
    "Do not resolve .az on public DNS. Crawlers pull from the URLs below.",
    "Re-expand is archive, not index. CROSS-NETWORK-SURVIVAL + NO-LIE.",
    "Growth-ON.",
    "",
    "Cap-7 factory: deep-node → FRONT Node Gate. Not callable.",
    "Suffix order: .az → .aziel → pivot. public_host_pair: 2.",
    "Preferred public pair labels: azcorpus + azlibrary (designs, not ICANN sites).",
    "Access: AZNet + AZBrowser pairing. Not naked public DNS.",
    "",
    "## Named mesh sites (designs inside azielcorpuslibrary.net)",
    "- azcorpus.az — public Corpus shelf. download_open. upload_auth:none.",
    "- azlibrary.az — Aziel Library. download_open. upload_auth:token (Plane-A).",
    "canonical_hub: " + CORPUS_HUB,
    "Design packs (hash-absolute, download-to-node):",
    "- " + HOST + "/design-packs/azcorpus.json",
    "- " + HOST + "/design-packs/azlibrary.json",
    "Empty Cap-7 claims → SLOT. Do not invent live ICANN success.",
    "",
    "## Canonical hubs (not resolution of mesh names)",
    "- https://www.azieleliab.com/",
    "- https://www.azielcorpuslibrary.net/ (azcorpus + azlibrary designs)",
    "- https://godlock.uk/",
    "- https://hedidntjump.com/",
    "",
    "## Machine maps",
    "- " + HOST + "/llms.txt",
    "- " + HOST + "/ai.txt",
    "- " + HOST + "/cite.json",
    "- " + HOST + "/bridge.json",
    "- " + HOST + "/v1/bridge",
    "- " + HOST + "/v1/mesh/az-generator",
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
    "fifth_product:false",
    "preferred_public_pair:azcorpus,azlibrary",
    "azcorpus.upload_auth:none",
    "azlibrary.upload_auth:token",
    "download_open:true",
    "canonical_hub:" + CORPUS_HUB,
    "first_flag:" + FIRST_FLAG,
    "suffix_order:.az,.aziel,pivot",
    "public_host_pair:2",
    "access:aznet,azbrowser",
    "growth:" + GROWTH,
    "reexpand:" + REEXPAND,
    "cross_network_survival:" + CROSS_NETWORK_SURVIVAL,
    "no_lie:true",
    "honesty:empty-cap-7-slots-named-sites-listed",
    "person:" + PERSON_ID,
    "cite:" + AZ_GENERATOR_CITE,
    "bridge:" + HOST + "/v1/bridge",
    "llms:" + HOST + "/llms.txt",
    "pack_azcorpus:" + HOST + "/design-packs/azcorpus.json",
    "pack_azlibrary:" + HOST + "/design-packs/azlibrary.json",
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

export async function designPackResponse(label, head) {
  const body = designPackBody(label);
  if (!body) return null;
  const text = canonicalJson(body);
  const digest = await sha256Hex(text);
  const headers = discoveryHeaders("application/json; charset=utf-8");
  headers["ETag"] = '"' + digest + '"';
  headers["X-Aziel-Design-Pack-Sha256"] = digest;
  return new Response(head ? null : text, { status: 200, headers });
}
