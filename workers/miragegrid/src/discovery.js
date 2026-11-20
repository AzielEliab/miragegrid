/**
 * First-party discovery for the named app Worker.
 * Growth-ON. Mesh-only. public_icann stays false.
 * Cap-7 is a mesh DNS factory (deep-node → Node Gate), not a public
 * ICANN or Cloudflare registrar and not a public DNS publish.
 * Author: Aziel Eliab only.
 */

import { APP_HOST, FACTORY_LABELS, IDENTITY, PERSON_ID } from "./cap7.js";

/** Revision date of these discovery documents. Not a per-request clock. */
export const DISCOVERY_LASTMOD = "2026-11-20";

/** HTTP and robots.txt content signal. Growth-ON: search, AI input, and AI train are allowed. */
export const CONTENT_SIGNAL = "search=yes, ai-input=yes, ai-train=yes";

/**
 * Public IndexNow ownership key (not a secret).
 * Served as text/plain at /<key>.txt and /.well-known/indexnow-key.txt.
 */
export const INDEXNOW_KEY = "5b98e660dc54bc7778a3fb12c750d035";

/** Machine-only person aliases. JSON-LD alternateName. Not visible HTML chrome. */
export const PERSON_ALIASES = Object.freeze([
  "Aziel Eliab",
  "AzielEliab",
  "azieleliab",
  "Aziel Elroi Eliab",
  "The Revealer of the Sealed",
  "Elias Artista",
]);

/**
 * Ten live public sites and runtimes (verified 2026-11-19).
 * No download-tracker URL. No private repo. MirageGrid stays mesh-only.
 */
export const PUBLIC_DOORS = Object.freeze([
  {
    href: "https://www.azieleliab.com/",
    name: "Aziel Eliab",
    role: "Identity Hub",
    note: "Canonical public site. Person @id https://www.azieleliab.com/#aziel.",
  },
  {
    href: "https://www.azielcorpuslibrary.net/",
    name: "Aziel Corpus Library",
    role: "Corpus library",
    note: "Canonical public library site.",
  },
  {
    href: "https://godlock.uk/",
    name: "GodLock",
    role: "Public site",
    note: "Canonical public site.",
  },
  {
    href: "https://hedidntjump.com/",
    name: "He Didn't Jump",
    role: "Marion Zioncheck Archive",
    note: "Canonical public archive.",
  },
  {
    href: "https://furnaceisntfree.com/",
    name: "Furnace Isn't Free",
    role: "Public site",
    note: "Canonical public site.",
  },
  {
    href: "https://timetounsealthebook.net/",
    name: "Time to Unseal the Book",
    role: "Public site",
    note: "Canonical public site.",
  },
  {
    href: "https://whitestone.vibelock.workers.dev/",
    name: "Whitestone",
    role: "Live pro se web app",
    note: "Public web app on Workers.",
  },
  {
    href: "https://aziel-runtime.vibelock.workers.dev/",
    name: "Aziel Runtime",
    role: "MCP / Softwares",
    note: "Public MCP runtime.",
    catalog: Object.freeze([
      { href: "https://glama.ai/mcp/servers/AzielEliab/aziel-runtime", name: "Glama" },
    ]),
  },
  {
    href: "https://trades-runtime.vibelock.workers.dev/",
    name: "Trades Runtime",
    role: "Public MCP runtime",
    note: "Public MCP runtime.",
    catalog: Object.freeze([
      { href: "https://glama.ai/mcp/servers/AzielEliab/trades-runtime", name: "Glama" },
    ]),
  },
  {
    href: "https://miragegrid.vibelock.workers.dev/",
    name: "MirageGrid",
    role: "Cap-7 mesh DNS factory Worker",
    note: "Mesh-only. public_icann: false. Deep-node → Node Gate. Not an ICANN registrar. Not a Cloudflare registrar. Not a public DNS publish.",
    self: true,
  },
]);

export const SITEMAP_PATHS = Object.freeze([
  "/",
  "/doors",
  "/llms.txt",
  "/ai.txt",
  "/.well-known/ai.txt",
  "/robots.txt",
  "/bridge",
  "/bridge.json",
  "/v1/bridge",
  "/cite.json",
  "/v1/skill",
  "/v1/health",
  "/v1/cap7",
  "/v1/shuffle",
  "/v1/doctor",
  "/v1/aznet",
  "/v1/egress",
  "/v1/nodes",
  "/v1/planned",
  "/openapi.json",
  "/mcp",
  "/land",
  "/attest",
  "/stats",
  ...FACTORY_LABELS.map((label) => "/cap7/" + label),
]);

const SCOPE =
  "MirageGrid is a Cap-7 mesh-only DNS factory. public_icann: false. Deep-node → Node Gate. Not an ICANN registrar, not a Cloudflare registrar, and not a public DNS publish.";

export function personEntity() {
  return {
    "@type": "Person",
    "@id": PERSON_ID,
    name: IDENTITY,
    url: PERSON_ID,
    alternateName: PERSON_ALIASES.slice(),
  };
}

export function contentSignalHeaders(contentType) {
  const type = String(contentType || "").toLowerCase();
  if (type.startsWith("text/") || type.startsWith("application/xml") || type.startsWith("application/xhtml")) {
    return { "Content-Signal": CONTENT_SIGNAL };
  }
  return {};
}

function escapeHtml(value) {
  return String(value == null ? "" : value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function escapeXml(value) {
  return escapeHtml(value).replace(/'/g, "&apos;");
}

function canonical(path) {
  if (path === "/") return APP_HOST + "/";
  return APP_HOST + path;
}

function doorLinks(door) {
  const catalog = (door.catalog || [])
    .map((row) => ` (<a href="${escapeHtml(row.href)}">${escapeHtml(row.name)} catalog</a>)`)
    .join("");
  return `<a href="${escapeHtml(door.href)}">${escapeHtml(door.name)}</a> — ${escapeHtml(door.role)}${catalog}`;
}

export function doorsFooterHtml() {
  const items = PUBLIC_DOORS.map((door) => `<li>${doorLinks(door)}</li>`).join("");
  return `<footer class="card" id="ecosystem-doors">
  <h2>Ecosystem / Doors</h2>
  <p class="kid">Ten live public sites and runtimes. <a href="/doors">Open /doors</a>. This host is mesh-only (<code>public_icann: false</code>): a Cap-7 mesh DNS factory (deep-node → Node Gate), not a public ICANN or Cloudflare registrar, and not a public DNS publish.</p>
  <ul>
    ${items}
  </ul>
</footer>`;
}

export function renderDoorsHtml() {
  const items = PUBLIC_DOORS.map((door, index) => {
    return `<li id="door-${index + 1}"><p>${doorLinks(door)}</p><p class="kid">${escapeHtml(door.note)}</p></li>`;
  }).join("");
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: "MirageGrid ecosystem doors",
    url: canonical("/doors"),
    description: SCOPE,
    isPartOf: { "@type": "WebSite", name: "MirageGrid", url: canonical("/") },
    author: personEntity(),
    mainEntity: {
      "@type": "ItemList",
      numberOfItems: PUBLIC_DOORS.length,
      itemListElement: PUBLIC_DOORS.map((door, index) => ({
        "@type": "ListItem",
        position: index + 1,
        name: door.name,
        url: door.href,
        description: door.role + ". " + door.note,
      })),
    },
  };
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ecosystem / Doors — MirageGrid (mesh-only, not an ICANN registrar)</title>
<meta name="description" content="${escapeHtml(SCOPE)}">
<meta name="author" content="${IDENTITY}">
<link rel="canonical" href="${canonical("/doors")}">
<script type="application/ld+json">${JSON.stringify(jsonLd)}</script>
<style>
  :root { color-scheme: dark; --bg:#0e1014; --panel:#151922; --ink:#e8eaef; --muted:#9aa3b2; --line:#2a3140; --gold:#c9a227; }
  * { box-sizing: border-box; }
  body { font: 16px/1.45 system-ui, sans-serif; max-width: 56rem; margin: 2.25rem auto; padding: 0 1.25rem 4rem; background: var(--bg); color: var(--ink); }
  h1 { font-size: 1.85rem; margin: 0 0 .2rem; }
  h2 { font-size: 1.15rem; margin: 0 0 .55rem; }
  a { color: #c9d4ff; }
  .banner { border: 1px solid #5c4a1a; background: #241c0d; color: #f0d78c; padding: .85rem 1rem; border-radius: 8px; margin: 0 0 1.2rem; font-size: .92rem; }
  .card { border: 1px solid var(--line); border-radius: 12px; padding: 1.15rem 1.25rem; background: var(--panel); margin: 0 0 1rem; }
  .kid { color: var(--muted); font-size: .92rem; }
  ol { padding-left: 1.2rem; }
  li { margin: 0 0 .85rem; }
</style>
</head>
<body>
  <h1>Ecosystem / Doors</h1>
  <p class="banner">${escapeHtml(SCOPE)} Author ${IDENTITY}.</p>
  <p class="kid"><a href="/">MirageGrid home</a> · <a href="/llms.txt">llms.txt</a> · <a href="/ai.txt">ai.txt</a> · <a href="/sitemap.xml">sitemap.xml</a></p>
  <section class="card">
    <h2>Ten live public sites</h2>
    <p class="kid">These are the public doors. MirageGrid is one of them and stays mesh-only. Cap-7 names are coordination labels on the names plane. They are not live ICANN hosts and this Worker does not publish them to public DNS.</p>
    <ol>
      ${items}
    </ol>
  </section>
</body>
</html>`;
}

export function robotsTxt() {
  const agents = ["GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-User", "anthropic-ai", "PerplexityBot", "Google-Extended"];
  const lines = [
    "# SEMANTIC-BRIDGE-1.0 — Growth-ON.",
    "# Cap-7 is mesh-only (public_icann: false). Not public ICANN DNS.",
    "# Not an ICANN registrar. Not a Cloudflare registrar. Not a public DNS publish.",
    "User-agent: *",
    "Allow: /",
    "Content-Signal: " + CONTENT_SIGNAL,
    "Sitemap: " + canonical("/sitemap.xml"),
    "",
  ];
  for (const agent of agents) {
    lines.push("User-agent: " + agent, "Allow: /", "");
  }
  return lines.join("\n");
}

export function sitemapXml() {
  const body = SITEMAP_PATHS.map((path) => {
    return "  <url><loc>" + escapeXml(canonical(path)) + "</loc><lastmod>" + DISCOVERY_LASTMOD + "</lastmod></url>";
  }).join("\n");
  return (
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    body +
    "\n</urlset>\n"
  );
}

export function llmsTxt() {
  const doorLines = PUBLIC_DOORS.map((door) => {
    const catalog = (door.catalog || []).map((row) => ` Catalog: [${row.name}](${row.href}).`).join("");
    return `- [${door.name}](${door.href}): ${door.role}. ${door.note}${catalog}`;
  });
  return [
    "# MirageGrid",
    "> " + SCOPE,
    "",
    "Author: " + IDENTITY + " only",
    "Person @id: " + PERSON_ID,
    "",
    "This file describes the named app Worker at " + canonical("/") + ".",
    "Cap-7 is a mesh DNS factory: four hub mirrors and three decoys, separate from per-node .aziel slots.",
    "Shift stack: StaticLock + MirageGrid cloak + cap7-egress.",
    "Factory honesty is LIVE on the names plane (control-plane coordination). That LIVE is mesh-only. It is not an ICANN DNS publish and not a public DNS publish.",
    "public_icann: false",
    "public_icann_registrar: false",
    "typed_on_icann_dns: false",
    "resolves_to_hub: false",
    "internet_reaches: az-domains (via the hub websites, not via Cap-7 names)",
    "AZ Generator is not callable here (AZG-NOT-CALLABLE). The exit is deep-node → FRONT Node Gate.",
    "Not a VPN. Not an anonymity network. Not AZVPN. packet_forwarding: false.",
    "Growth-ON.",
    "",
    "## Ecosystem doors",
    "Ten live public sites and runtimes. This list is a cross-reference, not a DNS publish.",
    ...doorLines,
    "",
    "## Machine maps on this host",
    "- [llms.txt](" + canonical("/llms.txt") + ")",
    "- [ai.txt](" + canonical("/ai.txt") + ")",
    "- [ai.txt well-known](" + canonical("/.well-known/ai.txt") + ")",
    "- [sitemap.xml](" + canonical("/sitemap.xml") + ")",
    "- [robots.txt](" + canonical("/robots.txt") + ")",
    "- [doors](" + canonical("/doors") + ")",
    "- [bridge](" + canonical("/bridge") + ")",
    "- [cite.json](" + canonical("/cite.json") + ")",
    "- [health](" + canonical("/v1/health") + ")",
    "- [cap7 roster](" + canonical("/v1/cap7") + ")",
    "- [skill](" + canonical("/v1/skill") + ")",
    "",
    "Sitemap lastmod: " + DISCOVERY_LASTMOD,
    "License: Apache-2.0",
    "",
  ].join("\n");
}

export function aiTxt() {
  const lines = [
    "SEMANTIC-BRIDGE-1.0",
    "product:MirageGrid",
    "host:" + canonical("/"),
    "growth:Growth-ON",
    "public_icann:false",
    "public_icann_registrar:false",
    "typed_on_icann_dns:false",
    "resolves_to_hub:false",
    "mesh_only:true",
    "cap7:mesh-dns-factory",
    "deep_node_to_node_gate:true",
    "not_icann_registrar:true",
    "not_cloudflare_registrar:true",
    "not_public_dns_publish:true",
    "icann_dns_publish:false",
    "packet_forwarding:false",
    "hosted_vpn:false",
    "azvpn:false",
    "az_generator_callable:false",
    "person:" + PERSON_ID,
    "author:" + IDENTITY,
    "llms:" + canonical("/llms.txt"),
    "ai:" + canonical("/ai.txt"),
    "ai_well_known:" + canonical("/.well-known/ai.txt"),
    "sitemap:" + canonical("/sitemap.xml"),
    "robots:" + canonical("/robots.txt"),
    "doors:" + canonical("/doors"),
    "bridge:" + canonical("/bridge"),
    "cite:" + canonical("/cite.json"),
    "lastmod:" + DISCOVERY_LASTMOD,
    "content_signal:" + CONTENT_SIGNAL,
    "door_count:" + PUBLIC_DOORS.length,
  ];
  PUBLIC_DOORS.forEach((door, index) => {
    lines.push("door_" + (index + 1) + ":" + door.href);
    lines.push("door_" + (index + 1) + "_name:" + door.name);
  });
  lines.push("do_not_treat_cap7_names_as_icann:true", "");
  return lines.join("\n");
}
