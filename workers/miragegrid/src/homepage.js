/**
 * MirageGrid app homepage — Cap-7 LIVE shuffle.
 * Inherits hub design DNA (dark/gold) only. Does not resolve to hubs.
 * Author: Aziel Eliab only.
 */

import { APP_HOST, CAP7_SHUFFLE_SPEC, DOWNLOAD_HOST, IDENTITY, cap7Roster, personId } from "./cap7.js";

const TITLE = "MirageGrid — Cap-7 LIVE shuffle";
const MOTTO = "Nodes ping MirageGrid until they land on one Cap-7 site. That land is the update endpoint for the round.";
const BANNER = "THIS IS: the named app Worker (miragegrid). Cap-7 factory sites inherit hub design DNA only. resolves_to_hub is false. public_icann is false. AZ Generator exits FRONT Node Gate only. Communication/cite plane — not a VPN. FragGate is THE exec door. Hosted update and AZNet endpoints stay SLOT. THIS IS NOT: a VPN, ICANN .az registrar, a second /mcp, or the download-tracker. Author Aziel Eliab.";

export function citeDocument() {
  return {
    author: IDENTITY,
    title: "MirageGrid",
    version: "0.2.0",
    one_line: "Cap-7 LIVE shuffle app Worker. Not a VPN.",
    github: "https://github.com/AzielEliab/miragegrid",
    homepage: APP_HOST + "/",
    download: DOWNLOAD_HOST + "/download",
    license: "Apache-2.0",
    catalog: "https://aziel-runtime.vibelock.workers.dev/",
    doi: null,
    person: personId(),
    spec: CAP7_SHUFFLE_SPEC,
    resolves_to_hub: false,
    public_icann: false,
    radio_phy: false,
    channel_plane_is_vpn: false,
    second_door: false,
    hosted_update: "SLOT",
    live_app_worker: APP_HOST,
    live_download_worker: DOWNLOAD_HOST,
    historical_cf_1042: "closed-by-creating-worker-miragegrid",
    shelves: "https://www.azielcorpuslibrary.net/shelves",
  };
}

function escapeHtml(value) {
  return String(value == null ? "" : value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export function renderIndexHtml() {
  const sites = cap7Roster();
  const rows = sites
    .map(
      (s) =>
        `<tr><td><code>${escapeHtml(s.label)}</code></td><td>${escapeHtml(s.honesty_public)}</td><td>${escapeHtml(s.reach)}</td><td>${escapeHtml(s.design_of)}</td><td><code>${escapeHtml(s.worker_path)}</code></td></tr>`,
    )
    .join("");
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: "MirageGrid",
    softwareVersion: "0.2.0",
    author: { "@type": "Person", name: IDENTITY, url: "https://www.azieleliab.com/#aziel" },
    url: APP_HOST + "/",
    description: MOTTO,
  };

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${TITLE}</title>
<meta name="description" content="${escapeHtml(MOTTO)}">
<meta name="author" content="${IDENTITY}">
<link rel="canonical" href="${APP_HOST}/">
<script type="application/ld+json">${JSON.stringify(jsonLd)}</script>
<style>
  :root { color-scheme: dark; --bg:#0e1014; --panel:#151922; --ink:#e8eaef; --muted:#9aa3b2; --line:#2a3140; --gold:#c9a227; --pass:#7dcf9a; --fail:#ff8a8a; }
  * { box-sizing: border-box; }
  body { font: 16px/1.45 system-ui, sans-serif; max-width: 56rem; margin: 2.25rem auto; padding: 0 1.25rem 4rem; background: var(--bg); color: var(--ink); }
  h1 { font-size: 1.85rem; margin: 0 0 .2rem; }
  h2 { font-size: 1.15rem; margin: 0 0 .55rem; }
  a { color: #c9d4ff; }
  .motto { color: var(--muted); margin: 0 0 1rem; }
  .banner { border: 1px solid #5c4a1a; background: #241c0d; color: #f0d78c; padding: .85rem 1rem; border-radius: 8px; margin: 0 0 1.2rem; font-size: .92rem; }
  .card { border: 1px solid var(--line); border-radius: 12px; padding: 1.15rem 1.25rem; background: var(--panel); margin: 0 0 1rem; }
  table { width: 100%; border-collapse: collapse; font-size: .88rem; }
  th, td { text-align: left; padding: .4rem .35rem; border-bottom: 1px solid var(--line); vertical-align: top; }
  .live { color: var(--pass); font-weight: 700; }
  .slot { color: var(--fail); font-weight: 700; }
  button { font: 700 .85rem/1 system-ui; height: 2.1rem; padding: 0 .85rem; border-radius: 8px; background: #0c0b08; color: var(--ink); border: 1px solid var(--gold); cursor: pointer; }
  button:hover { background: #241c0d; color: var(--gold); }
  input, textarea { width: 100%; padding: .45rem .55rem; border: 1px solid var(--line); border-radius: 8px; background: #0c0b08; color: var(--ink); font: inherit; margin: 0 0 .6rem; }
  pre { white-space: pre-wrap; word-break: break-word; background: #0c0b08; padding: .75rem; border-radius: 8px; font-size: .82rem; }
  .ops { display: flex; flex-wrap: wrap; gap: .5rem; margin: .6rem 0; }
  .kid { color: var(--muted); font-size: .92rem; }
</style>
</head>
<body>
  <h1>MirageGrid</h1>
  <p class="motto">${escapeHtml(MOTTO)} Author ${IDENTITY}.</p>
  <p class="banner">${escapeHtml(BANNER)}</p>

  <nav class="ops">
    <a href="/bridge">/bridge</a>
    <a href="/v1/shuffle">/v1/shuffle</a>
    <a href="/v1/cap7">/v1/cap7</a>
    <a href="/v1/health">/v1/health</a>
    <a href="/v1/skill">/v1/skill</a>
    <a href="/openapi.json">OpenAPI</a>
    <a href="${DOWNLOAD_HOST}/">Downloads</a>
  </nav>

  <section class="card" id="cap7">
    <h2>Cap-7 factory sites</h2>
    <p class="kid">Different names. Hub design DNA only. <code>resolves_to_hub: false</code>. Mesh <code>.az</code> stays SLOT on ICANN. Public pair (azgrid + azbooth) is LIVE Worker HTTPS cite. Remainder is AZNet-side SLOT. Hosted update / AZNet endpoints stay SLOT. Communication plane — not a VPN. FragGate is THE door.</p>
    <table>
      <thead><tr><th>Label</th><th>Public</th><th>Reach</th><th>design_of</th><th>Path</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
  </section>

  <section class="card" id="shuffle">
    <h2>Update shuffle</h2>
    <p class="kid">Ping until land. No hard-coded Cap-7 host. Update seed is <code>prev|lockset</code> (proof). Coordination seed is <code>round_id</code>.</p>
    <label for="node-id">Node id</label>
    <input id="node-id" value="node-01" maxlength="80">
    <label for="round-id">Round id (optional)</label>
    <input id="round-id" placeholder="shared round token">
    <label for="prev">prev (update proof)</label>
    <input id="prev" placeholder="previous tip">
    <label for="lockset">lockset (update proof)</label>
    <input id="lockset" placeholder="lockset cite">
    <div class="ops">
      <button type="button" id="op-ping">Ping</button>
      <button type="button" id="op-update">Update</button>
      <button type="button" id="op-assign">Assign</button>
      <button type="button" id="op-health">Health</button>
      <button type="button" id="op-bridge">Bridge</button>
    </div>
    <p class="status" id="ws-status">Ready. Ping to land.</p>
    <pre id="ws-out">No ping yet.</pre>
  </section>

  <section class="card" id="cite">
    <h2>Cite</h2>
    <p class="kid">App Worker <code>${APP_HOST}</code> is LIVE. Download plane <a href="${DOWNLOAD_HOST}/">${DOWNLOAD_HOST}</a>. Historical CF 1042 is closed by creating Worker <code>miragegrid</code>. Author ${IDENTITY} only. Apache-2.0. Forks welcome.</p>
  </section>

<script>
(function () {
  const out = document.getElementById("ws-out");
  const status = document.getElementById("ws-status");
  async function call(path, init) {
    const res = await fetch(path, Object.assign({
      headers: { "user-agent": "Mozilla/5.0", accept: "application/json", "content-type": "application/json" }
    }, init || {}));
    const text = await res.text();
    let data;
    try { data = JSON.parse(text); } catch { data = { raw: text, status: res.status }; }
    out.textContent = JSON.stringify(data, null, 2);
    status.textContent = path + " → " + res.status + (data.code ? " " + data.code : "");
    return data;
  }
  function shuffleBody() {
    return {
      node_id: document.getElementById("node-id").value,
      round_id: document.getElementById("round-id").value,
      prev: document.getElementById("prev").value,
      lockset: document.getElementById("lockset").value
    };
  }
  document.getElementById("op-ping").onclick = function () {
    call("/v1/shuffle/ping", { method: "POST", body: JSON.stringify(shuffleBody()) });
  };
  document.getElementById("op-update").onclick = function () {
    call("/v1/shuffle/update", { method: "POST", body: JSON.stringify(shuffleBody()) });
  };
  document.getElementById("op-assign").onclick = function () {
    call("/v1/assign", { method: "POST", body: "{}" });
  };
  document.getElementById("op-health").onclick = function () { call("/v1/health"); };
  document.getElementById("op-bridge").onclick = function () { call("/bridge"); };
})();
</script>
</body>
</html>`;
}
