/**
 * MirageGrid human homepage. Complete product UI — not a downloads shell.
 * Author: Aziel Eliab only. Apache-2.0. Forks welcome.
 * Hosted surface is session assignment. MirageGrid is not a VPN.
 */

const HOST = "https://miragegrid-download-tracker.vibelock.workers.dev";
const GITHUB_REPO = "https://github.com/AzielEliab/miragegrid";
const GITHUB_LATEST = "https://github.com/AzielEliab/miragegrid/releases/latest";
const CATALOG = "https://aziel-runtime.vibelock.workers.dev/";
const DEFAULT_ASSET = "miragegrid-0.2.0.tar.gz";
const INSTALL_LINE = "curl -fsSL https://miragegrid-download-tracker.vibelock.workers.dev/install.sh | bash";
const TITLE = "MirageGrid — Aziel Eliab";
const ONE_LINE =
  "Ephemeral session node assignment. Not a VPN and not an anonymity network.";
const MOTTO =
  "You enter the booth. The mesh selects a booth and builds a circuit. You leave with no persistent booth identity.";
const BANNER =
  "THIS IS: a 25-node session assignment engine for AZ-OS — logical identities, circuit maps, and receipts. Hosted /v1 assigns and verifies; it does not forward packets. THIS IS NOT: a VPN, an anonymity network, a hosted hop, a crime tool, a log-wipe, or a guarantee against a global adversary. Isolated counter: not VibeLock. Author Aziel Eliab.";
const DESC =
  "MirageGrid by Aziel Eliab — ephemeral session node assignment with receipts. Not a VPN and not an anonymity network. Apache-2.0. Forks welcome.";

export function citeDocument() {
  return {
    author: "Aziel Eliab",
    title: "MirageGrid",
    version: "0.2.0",
    one_line: ONE_LINE,
    github: GITHUB_REPO,
    homepage: HOST + "/",
    download: HOST + "/download",
    license: "Apache-2.0",
    catalog: CATALOG,
    doi: null,
    note: "Zenodo software deposit needed (no DOI invented).",
  };
}

function escapeHtml(value) {
  return String(value == null ? "" : value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export function renderIndexHtml(stats) {
  const views = Number(stats.views) || 0;
  const downloads = Number(stats.downloads != null ? stats.downloads : stats.total) || 0;
  const v = views.toLocaleString("en-US");
  const n = downloads.toLocaleString("en-US");
  const gh = stats.github || {};
  const breakdown =
    (stats.breakdown || [])
      .map(
        (b) =>
          `<li><code>${escapeHtml(b.owner)}/${escapeHtml(b.repo)}</code> branch <code>${escapeHtml(b.branch)}</code> fork=${escapeHtml(b.fork)} → ${escapeHtml(b.count)}</li>`,
      )
      .join("") || "<li>none yet</li>";
  const cite = citeDocument();
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: "MirageGrid",
    softwareVersion: "0.2.0",
    applicationCategory: "DeveloperApplication",
    operatingSystem: "Linux, macOS, Windows",
    author: { "@type": "Person", name: "Aziel Eliab", url: "https://github.com/AzielEliab" },
    creator: { "@type": "Person", name: "Aziel Eliab" },
    codeRepository: GITHUB_REPO,
    downloadUrl: HOST + "/download",
    license: "https://www.apache.org/licenses/LICENSE-2.0",
    url: HOST + "/",
    description: DESC,
    offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
  };

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${TITLE}</title>
<meta name="description" content="${escapeHtml(DESC)}">
<meta name="author" content="Aziel Eliab">
<meta name="citation_title" content="MirageGrid">
<meta name="citation_author" content="Aziel Eliab">
<meta name="citation_publication_date" content="2026">
<link rel="canonical" href="${HOST}/">
<link rel="icon" href="/sigil.png" type="image/png">
<meta property="og:title" content="${TITLE}">
<meta property="og:description" content="${escapeHtml(DESC)}">
<meta property="og:url" content="${HOST}/">
<meta property="og:type" content="website">
<meta property="og:image" content="${HOST}/sigil.png">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="${TITLE}">
<meta name="twitter:description" content="${escapeHtml(DESC)}">
<meta name="twitter:image" content="${HOST}/sigil.png">
<script type="application/ld+json">
${JSON.stringify(jsonLd, null, 2)}
</script>
<style>
  :root {
    color-scheme: dark;
    --bg: #0e1014;
    --panel: #151922;
    --ink: #e8eaef;
    --muted: #9aa3b2;
    --line: #2a3140;
    --gold: #c9a227;
    --gold-soft: #d4af37;
    --pass: #7dcf9a;
    --fail: #ff8a8a;
  }
  * { box-sizing: border-box; }
  body {
    font: 16px/1.45 system-ui, sans-serif;
    max-width: 56rem;
    margin: 2.25rem auto;
    padding: 0 1.25rem 4rem;
    background: var(--bg);
    color: var(--ink);
  }
  h1 { font-size: 1.85rem; margin: 0 0 .2rem; letter-spacing: .01em; }
  h2 { font-size: 1.15rem; margin: 0 0 .55rem; }
  a { color: #c9d4ff; }
  .brandrow { display: flex; align-items: center; gap: 12px; margin: 0 0 10px; }
  .brandmark {
    width: 48px; height: 48px; border-radius: 12px; object-fit: cover; flex: 0 0 auto;
    box-shadow: 0 0 0 1px #d4af3733, 0 0 18px #c9a22733;
    animation: everbloom 4.8s ease-in-out infinite;
  }
  @keyframes everbloom {
    0%, 100% { box-shadow: 0 0 0 1px #d4af3733, 0 0 10px #c9a22722; filter: saturate(1); }
    50% { box-shadow: 0 0 0 1px #d4af3766, 0 0 28px #c9a22766; filter: saturate(1.25); }
  }
  .stamp { margin: 0; color: var(--gold-soft); font-size: .88rem; letter-spacing: .02em; }
  .motto { color: var(--muted); margin: 0 0 1rem; }
  .banner {
    border: 1px solid #5c4a1a; background: #241c0d; color: #f0d78c;
    padding: .85rem 1rem; border-radius: 8px; margin: 0 0 1.2rem; font-size: .92rem;
  }
  .grid { display: grid; grid-template-columns: 1.15fr .85fr; gap: 1rem; }
  @media (max-width: 800px) { .grid { grid-template-columns: 1fr; } }
  .card {
    border: 1px solid var(--line); border-radius: 12px;
    padding: 1.15rem 1.25rem; background: var(--panel); margin: 0 0 1rem;
  }
  .nums { display: grid; grid-template-columns: 1fr 1fr; gap: .8rem; margin: 0 0 1rem; }
  .count { font-size: 2.1rem; font-variant-numeric: tabular-nums; font-weight: 700; margin: 0; }
  .count span { display: block; font-size: .95rem; font-weight: 500; color: var(--muted); }
  .btns { display: grid; grid-template-columns: 1fr 1fr; gap: .75rem; margin: 0 0 .85rem; }
  @media (max-width: 520px) { .btns { grid-template-columns: 1fr; } }
  a.btn, button.btn {
    display: block; width: 100%; box-sizing: border-box; text-align: center;
    font: inherit; font-size: 1.05rem; font-weight: 750; padding: .85rem 1rem;
    border-radius: 10px; border: 0; cursor: pointer; text-decoration: none;
  }
  a.btn.primary, button.btn.primary { background: #e8eaef; color: #0e1014; }
  button.btn.install, button.btn.gold { background: var(--gold); color: #14110a; }
  button.btn.install.copied { background: var(--pass); color: #0e1014; }
  button.btn.secondary { background: #2a3340; color: var(--ink); }
  button.btn:disabled { opacity: .45; cursor: not-allowed; }
  .ops { display: flex; flex-wrap: wrap; gap: .5rem; margin: 0 0 .75rem; }
  .ops button { width: auto; padding: .55rem .85rem; font-size: .95rem; }
  label.field { display: block; color: var(--muted); font-size: .8rem; text-transform: uppercase; letter-spacing: .06em; margin: .45rem 0 .2rem; }
  input, select, textarea {
    width: 100%; background: #0e1014; color: var(--ink); border: 1px solid var(--line);
    border-radius: 8px; padding: .5rem .65rem; font: inherit;
  }
  textarea { min-height: 7rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .82rem; }
  .route { display: grid; grid-template-columns: 1fr 1fr auto; gap: .5rem; align-items: end; margin: 0 0 .75rem; }
  @media (max-width: 640px) { .route { grid-template-columns: 1fr; } }
  .k { color: var(--muted); font-size: .78rem; text-transform: uppercase; letter-spacing: .06em; }
  .v { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 1.02rem; margin: .1rem 0 .65rem; word-break: break-word; }
  .pass { color: var(--pass); }
  .fail { color: var(--fail); }
  .hops { display: flex; flex-wrap: wrap; gap: .4rem; margin: .25rem 0 .7rem; }
  .hop {
    border: 1px solid var(--line); border-radius: 999px; padding: .2rem .65rem;
    font-family: ui-monospace, monospace; font-size: .85rem;
  }
  .hop.entry { border-color: var(--gold); color: var(--gold); }
  .hop.exit { border-color: #7eb8ff; color: #7eb8ff; }
  .status { min-height: 1.3rem; color: var(--muted); margin: 0 0 .6rem; }
  .kid { font-size: 1.02rem; margin: 0 0 1rem; }
  .meta { margin-top: 1.1rem; color: var(--muted); font-size: .92rem; }
  .iso { margin-top: .85rem; font-size: .85rem; color: #7d8696; }
  pre { background: #0e1014; padding: .75rem .9rem; overflow: auto; border-radius: 8px; font-size: .82rem; }
  code { font-size: .88rem; }
  .cite { margin-top: .4rem; }
  .cite p { color: #c5ccd8; }
  footer { color: var(--muted); font-size: .88rem; margin-top: 1.5rem; }
  nav.jump { display: flex; flex-wrap: wrap; gap: .75rem; margin: 0 0 1.1rem; font-size: .92rem; }
</style>
</head>
<body>
  <div class="brandrow">
    <img class="brandmark" src="/sigil.png" width="48" height="48" alt="Everblooming sigil — Aziel Eliab" decoding="async">
    <p class="stamp">Everblooming sigil · Aziel Eliab</p>
  </div>
  <h1>MirageGrid</h1>
  <p class="motto">${escapeHtml(MOTTO)} Author Aziel Eliab.</p>
  <p class="banner">${escapeHtml(BANNER)}</p>
  <nav class="jump">
    <a href="#workspace">Workspace</a>
    <a href="#download">Download</a>
    <a href="#cite">Cite</a>
    <a href="/v1/skill">Skill</a>
    <a href="/openapi.json">OpenAPI</a>
    <a href="${GITHUB_REPO}">GitHub</a>
  </nav>

  <div class="grid">
    <section class="card" id="workspace">
      <h2>Workspace</h2>
      <p class="kid">Assign a session node, inspect the 25-node mesh, route two peers, or verify a receipt. Results stay on this page. Hosted ops do not increment downloads.</p>
      <div class="ops">
        <button type="button" class="btn gold" id="op-assign">Assign</button>
        <button type="button" class="btn secondary" id="op-mesh">Mesh</button>
        <button type="button" class="btn secondary" id="op-circuit">Circuit</button>
        <button type="button" class="btn secondary" id="op-health">Health</button>
        <button type="button" class="btn secondary" id="op-nodes">Nodes</button>
      </div>
      <div class="route">
        <div>
          <label class="field" for="route-from">From</label>
          <select id="route-from"></select>
        </div>
        <div>
          <label class="field" for="route-to">To</label>
          <select id="route-to"></select>
        </div>
        <button type="button" class="btn secondary" id="op-route">Route</button>
      </div>
      <label class="field" for="receipt-in">Receipt JSON</label>
      <textarea id="receipt-in" spellcheck="false" placeholder='Paste a receipt from Assign, or {}'></textarea>
      <div class="ops">
        <button type="button" class="btn secondary" id="op-verify">Verify receipt</button>
        <button type="button" class="btn secondary" id="op-export" disabled>Export last result</button>
      </div>
      <p class="status" id="ws-status">Ready. Assign a node to begin.</p>
      <div id="ws-fields">
        <div class="k">Status</div>
        <div class="v" id="ws-summary">No assignment yet.</div>
        <div class="k">Entry node</div>
        <div class="v" id="ws-node">—</div>
        <div class="k">Circuit hops</div>
        <div class="hops" id="ws-hops"><span class="hop">—</span></div>
        <div class="k">Mesh path</div>
        <div class="v" id="ws-path">—</div>
        <div class="k">Session ID</div>
        <div class="v" id="ws-sid">—</div>
        <div class="k">Integrity</div>
        <div class="v" id="ws-integrity">—</div>
      </div>
      <label class="field">Raw result</label>
      <pre id="ws-raw">{}</pre>
    </section>

    <section class="card" id="download">
      <div class="nums">
        <p class="count">${v}<span>Views</span></p>
        <p class="count">${n}<span>Downloads</span></p>
      </div>
      <p class="kid"><strong>Two big buttons.</strong> Download saves the gzip (the Downloads number goes up — live downloads). One-click install copies a Terminal command. After it finishes, type <code>miragegrid ui</code>.</p>
      <div class="btns">
        <a class="btn primary dl" href="/download?asset=${DEFAULT_ASSET}">Download</a>
        <button type="button" class="btn install" id="install-btn">One-click install</button>
      </div>
      <pre id="install-cmd">${INSTALL_LINE}</pre>
      <p class="kid">Then run: <code>miragegrid ui</code>. Local console is http://127.0.0.1:8080. Hosted MirageGrid is not a VPN.</p>
      <p class="meta">Live download count ticks on the Download click. The Worker serves the gzip (HTTP 200). No 302 to GitHub. Forks using this same link are counted automatically. ${DEFAULT_ASSET} — ${n} counted.</p>
      <p class="iso">Isolated counter: Worker <code>miragegrid-download-tracker</code>, project <code>miragegrid</code>, KV <code>MIRAGEGRID_DOWNLOADS</code>. Not mixed with any other product. /v1 does not increment downloads.</p>
      <p class="meta">GitHub: stars ${escapeHtml(gh.stars || 0)} · forks ${escapeHtml(gh.forks || 0)} · watchers ${escapeHtml(gh.watchers || 0)} · release assets ${escapeHtml(gh.release_download_count || 0)}</p>
      <p class="meta"><a href="/stats">JSON stats</a> · <a href="/openapi.json">OpenAPI</a> · <a href="/v1/skill">Skill</a> · <a href="/ai">AI runtime</a> · <a href="${GITHUB_REPO}">GitHub</a> · <a href="${GITHUB_LATEST}">releases</a></p>
      <h2>Per repo / branch / fork</h2>
      <ul>${breakdown}</ul>
    </section>
  </div>

  <section class="card">
    <h2>What you can do here</h2>
    <p>This page is the software. <strong>Assign</strong> picks an entry node (1–25), builds a circuit map, and mints an internal receipt. <strong>Mesh</strong> shows the persistent circulant topology. <strong>Route</strong> walks the shortest peer path. <strong>Verify</strong> checks a receipt hash and pool membership.</p>
    <p>Packet forwarding is not hosted. If you install the local package, <code>miragegrid ui</code> is a loopback console. That still does not make MirageGrid a VPN or an anonymity network.</p>
    <p class="iso">Always send <code>User-Agent: Mozilla/5.0</code> to the API. Cloudflare Workers may 403 an empty agent.</p>
  </section>

  <section class="card cite" id="cite">
    <h2>How to cite</h2>
    <p>Aziel Eliab. MirageGrid. ${GITHUB_REPO}. ${HOST}. Zenodo software deposit needed (no DOI invented).</p>
    <p>Author: <strong>Aziel Eliab</strong> only · License: Apache-2.0 · Forks are welcome and always allowed.</p>
    <p><a href="${CATALOG}">Catalog</a> · <a href="${GITHUB_REPO}">GitHub</a> · <a href="${HOST}/download">Download</a> · <a href="${HOST}/cite.json">cite.json</a></p>
    <pre>${escapeHtml(JSON.stringify(cite, null, 2))}</pre>
  </section>

  <footer>
    Apache-2.0 · Aziel Eliab · 2026 · forks welcome and always allowed.
    Lawful use only. MirageGrid is not a VPN.
  </footer>

  <script>
    (function () {
      var cmd = "curl -fsSL https://miragegrid-download-tracker.vibelock.workers.dev/install.sh | bash";
      var btn = document.getElementById("install-btn");
      var pre = document.getElementById("install-cmd");
      if (btn) {
        btn.addEventListener("click", function () {
          function done(ok) {
            btn.textContent = ok ? "Copied! Paste in Terminal, then run miragegrid ui" : "Select the command, copy it, then run miragegrid ui";
            btn.classList.add("copied");
          }
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(cmd).then(function () { done(true); }).catch(function () { done(false); });
          } else {
            done(false);
            if (pre && window.getSelection) {
              var r = document.createRange();
              r.selectNodeContents(pre);
              var sel = window.getSelection();
              sel.removeAllRanges();
              sel.addRange(r);
            }
          }
        });
      }

      var lastResult = null;
      var $ = function (id) { return document.getElementById(id); };
      function setStatus(text) { $("ws-status").textContent = text; }
      function showRaw(obj) { $("ws-raw").textContent = JSON.stringify(obj, null, 2); }
      function text(el, value) { el.textContent = value == null || value === "" ? "—" : String(value); }
      function renderHops(hops) {
        var box = $("ws-hops");
        box.innerHTML = "";
        if (!hops || !hops.length) {
          box.innerHTML = '<span class="hop">—</span>';
          return;
        }
        hops.forEach(function (hop, i) {
          var el = document.createElement("span");
          var id = typeof hop === "string" ? hop : (hop.node_id || hop.id || "?");
          var role = typeof hop === "object" && hop.role ? hop.role : (i === 0 ? "entry" : (i === hops.length - 1 ? "exit" : "middle"));
          el.className = "hop" + (role === "entry" || role === "entry-exit" ? " entry" : "") + (role === "exit" || role === "entry-exit" ? " exit" : "");
          el.textContent = id + (role ? " · " + role : "");
          box.appendChild(el);
        });
      }
      function clearFields() {
        text($("ws-node"), "—");
        renderHops([]);
        text($("ws-path"), "—");
        text($("ws-sid"), "—");
        $("ws-integrity").textContent = "—";
        $("ws-integrity").className = "v";
      }
      function applyResult(data, label) {
        lastResult = data;
        $("op-export").disabled = !data;
        showRaw(data || {});
        var circuit = (data && data.circuit) || data || {};
        var hops = circuit.hops || [];
        var path = circuit.path || data.path || [];
        var node = data && (data.node_id || data.node_label || (data.mirage_node != null ? "node-" + String(data.mirage_node).padStart(2, "0") : null));
        var sid = data && (data.session_id || (data.receipt && data.receipt.session_id));
        var integrity = data && (data.integrity || (data.receipt && data.receipt.integrity) || data.live_integrity);
        text($("ws-summary"), (data && (data.note || data.limitation || data.banner || label)) || label || "Result");
        text($("ws-node"), node);
        renderHops(hops.length ? hops : (Array.isArray(data && data.nodes) ? data.nodes.slice(0, 8).map(function (n) { return n.id; }) : []));
        text($("ws-path"), Array.isArray(path) && path.length ? path.join(" → ") : (data && data.topology ? data.topology + " · " + (data.pool_size || 25) + " peers" : "—"));
        text($("ws-sid"), sid);
        if (integrity) {
          $("ws-integrity").textContent = integrity;
          $("ws-integrity").className = "v " + (integrity === "PASS" ? "pass" : "fail");
        } else if (data && data.ok === true) {
          $("ws-integrity").textContent = "ok";
          $("ws-integrity").className = "v pass";
        } else if (data && data.hash_ok === false) {
          $("ws-integrity").textContent = "FAIL";
          $("ws-integrity").className = "v fail";
        } else {
          $("ws-integrity").textContent = "—";
          $("ws-integrity").className = "v";
        }
        if (data && data.receipt) {
          $("receipt-in").value = JSON.stringify(data.receipt, null, 2);
        }
      }
      function api(method, path, body) {
        setStatus("Calling " + method + " " + path + "…");
        var opts = {
          method: method,
          headers: { "Accept": "application/json", "Content-Type": "application/json" },
        };
        if (body !== undefined) opts.body = JSON.stringify(body);
        return fetch(path, opts).then(function (r) {
          return r.text().then(function (t) {
            var data;
            try { data = JSON.parse(t); } catch (e) { data = { error: t || ("HTTP " + r.status) }; }
            if (!r.ok) {
              setStatus("Error " + r.status + " from " + path);
              applyResult(data, "Error");
              throw new Error((data && data.error) || ("HTTP " + r.status));
            }
            setStatus(method + " " + path + " — " + r.status);
            applyResult(data, path);
            return data;
          });
        }).catch(function (err) {
          setStatus(String(err.message || err));
        });
      }
      function fillNodeSelects(nodes) {
        var from = $("route-from");
        var to = $("route-to");
        from.innerHTML = "";
        to.innerHTML = "";
        (nodes || []).forEach(function (n, i) {
          var id = n.id || n;
          var a = document.createElement("option");
          a.value = id; a.textContent = id;
          var b = a.cloneNode(true);
          from.appendChild(a);
          to.appendChild(b);
          if (i === 0) from.value = id;
          if (id === "node-13" || i === 12) to.value = id;
        });
      }
      $("op-assign").addEventListener("click", function () { api("POST", "/v1/assign", {}); });
      $("op-mesh").addEventListener("click", function () { api("GET", "/v1/mesh"); });
      $("op-circuit").addEventListener("click", function () { api("POST", "/v1/circuit", {}); });
      $("op-health").addEventListener("click", function () { api("GET", "/v1/health"); });
      $("op-nodes").addEventListener("click", function () {
        api("GET", "/v1/nodes").then(function (data) {
          if (data && data.nodes) fillNodeSelects(data.nodes);
        });
      });
      $("op-route").addEventListener("click", function () {
        api("POST", "/v1/route", { from: $("route-from").value || "node-01", to: $("route-to").value || "node-13" });
      });
      $("op-verify").addEventListener("click", function () {
        var raw = $("receipt-in").value.trim();
        var body;
        try { body = raw ? JSON.parse(raw) : {}; } catch (e) {
          setStatus("Receipt JSON is not valid.");
          return;
        }
        api("POST", "/v1/verify-receipt", body);
      });
      $("op-export").addEventListener("click", function () {
        if (!lastResult) return;
        var blob = new Blob([JSON.stringify(lastResult, null, 2)], { type: "application/json" });
        var a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "miragegrid-result.json";
        a.click();
        URL.revokeObjectURL(a.href);
      });
      var defaults = [];
      for (var i = 1; i <= 25; i++) defaults.push({ id: "node-" + String(i).padStart(2, "0") });
      fillNodeSelects(defaults);
      fetch("/v1/nodes", { headers: { "Accept": "application/json" } }).then(function (r) { return r.json(); }).then(function (data) {
        if (data && data.nodes) fillNodeSelects(data.nodes);
      }).catch(function () { /* dropdowns already filled */ });
    })();
  </script>
</body>
</html>`;
}
