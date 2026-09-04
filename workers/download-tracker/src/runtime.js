/**
 * MirageGrid hosted runtime (control plane).
 * Node-mesh VPN and anonymity network. Author Aziel Eliab.
 * /v1 never touches DOWNLOADS KV.
 */
const PRODUCT = "miragegrid";
const VERSION = "0.2.0";
const MOTTO = "You enter the booth. The mesh selects a booth and builds a circuit. You leave with no persistent booth identity.";
const BANNER = "MirageGrid is a true node-mesh VPN and anonymity network. Persistent 25-node peer mesh, onion circuits, userspace SOCKS5. Lawful privacy tool. Author Aziel Eliab.";
const HOST = "https://miragegrid-download-tracker.vibelock.workers.dev";
const SKILL = `---
name: MirageGrid
description: Use when assigning a mesh circuit, routing peers, or installing the node-mesh VPN. MirageGrid is a true node-mesh VPN and anonymity network. Author Aziel Eliab.
---

# MirageGrid

You enter the booth. The mesh selects a booth and builds a circuit. You leave with no persistent booth identity.

Author: **Aziel Eliab**.

**THIS IS:** a node-mesh VPN and anonymity network (25 persistent peers, onion circuits, userspace SOCKS5).

**THIS IS NOT:** a crime tool, a log-wipe, or a guarantee against a global adversary. Hosted \`/v1\` does not increment downloads.

Always send \`User-Agent: Mozilla/5.0\`. Cloudflare Workers may 403 an empty agent.

## Endpoints (this Worker)

Host: \`https://miragegrid-download-tracker.vibelock.workers.dev\`

| Method | Path | What |
|--------|------|------|
| GET | \`/v1/health\` | Liveness. Does not increment downloads. |
| GET | \`/v1/skill\` | This markdown. Does not increment downloads. |
| GET | \`/v1/nodes\` | List the 25 mesh nodes. |
| GET | \`/v1/mesh\` | Topology, adjacency, default listen ports. |
| POST | \`/v1/route\` | Shortest peer path between two nodes. |
| POST | \`/v1/assign\` | Assign a session circuit (entry + hops + path). |
| POST | \`/v1/circuit\` | Build circuit hops from entropy/timestamp (or fresh). |
| POST | \`/v1/verify-receipt\` | Verify an internal receipt. |

OpenAPI: \`https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json\`

Catalog OpenAPI: \`https://aziel-runtime.vibelock.workers.dev/openapi.json\`

MCP: \`POST https://aziel-runtime.vibelock.workers.dev/mcp\`

## How to call (Mozilla/5.0)

\`\`\`bash
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://miragegrid-download-tracker.vibelock.workers.dev/v1/assign \\
  -H 'content-type: application/json' -d '{}'
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/mesh
\`\`\`

Grok: import the catalog OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.

## Local (after one-click install)

\`\`\`bash
curl -fsSL https://miragegrid-download-tracker.vibelock.workers.dev/install.sh | bash
miragegrid ui
miragegrid vpn
\`\`\`

Then open http://127.0.0.1:8080 and SOCKS5 at 127.0.0.1:1080.

Apache-2.0 (or the repo LICENSE). Forks are welcome and always allowed.
`;

const POOL_SIZE = 25;
const PEER_OFFSETS = [1, 2, 5, 20, 23, 24];

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...corsHeaders() },
  });
}

function nodeIdFor(index) {
  return `node-${String(index + 1).padStart(2, "0")}`;
}
function nodeLabelFor(index) {
  return `Node${String(index + 1).padStart(2, "0")}`;
}

function makePool(endpoints) {
  const eps = endpoints && typeof endpoints === "object" ? endpoints : {};
  const nodes = [];
  for (let index = 0; index < POOL_SIZE; index++) {
    const id = nodeIdFor(index);
    const label = nodeLabelFor(index);
    let endpoint = eps[id] || eps[label] || `127.0.0.1:${19000 + index + 1}`;
    if (endpoint != null) endpoint = String(endpoint);
    nodes.push({ id, label, index, number: index + 1, endpoint });
  }
  const byId = Object.fromEntries(nodes.map((n) => [n.id, n]));
  return {
    nodes,
    byId,
    contains(id) { return Boolean(byId[id]); },
    containsNumber(n) { return Number.isInteger(n) && n >= 1 && n <= POOL_SIZE; },
    byIndex(i) {
      if (i < 0 || i >= POOL_SIZE) throw new Error(`node index ${i} out of range 0..24`);
      return nodes[i];
    },
    byNumber(n) {
      if (n < 1 || n > POOL_SIZE) throw new Error(`mirage_node ${n} out of range 1..25`);
      return nodes[n - 1];
    },
    byId(id) {
      if (!byId[id]) throw new Error(`unknown node ${id}`);
      return byId[id];
    },
  };
}

function neighbors(index) {
  const seen = [];
  for (const off of PEER_OFFSETS) {
    const n = (index + off) % POOL_SIZE;
    if (n !== index && !seen.includes(n)) seen.push(n);
  }
  seen.sort((a, b) => a - b);
  return seen;
}

function shortestNextHop(src) {
  const parent = Array(POOL_SIZE).fill(-1);
  parent[src] = src;
  const q = [src];
  while (q.length) {
    const cur = q.shift();
    for (const n of neighbors(cur)) {
      if (parent[n] === -1 && n !== src) {
        parent[n] = cur;
        q.push(n);
      }
    }
  }
  const nxt = Array(POOL_SIZE).fill(-1);
  for (let dst = 0; dst < POOL_SIZE; dst++) {
    if (dst === src) {
      nxt[dst] = src;
      continue;
    }
    if (parent[dst] === -1) {
      nxt[dst] = -1;
      continue;
    }
    let walk = dst;
    while (parent[walk] !== src) walk = parent[walk];
    nxt[dst] = walk;
  }
  return nxt;
}

function pathIndices(src, dst) {
  if (src === dst) return [src];
    const hops = [src];
    let cur = src;
    let guard = 0;
    while (cur !== dst) {
      const hop = shortestNextHop(cur)[dst];
    if (hop < 0 || hop === cur) throw new Error("no mesh path");
    hops.push(hop);
    cur = hop;
    guard += 1;
    if (guard > POOL_SIZE + 2) throw new Error("path too long");
  }
  return hops;
}

function expandCircuitPath(hopIndices) {
  if (!hopIndices.length) return [];
  const walk = [hopIndices[0]];
  for (let i = 0; i < hopIndices.length - 1; i++) {
    const seg = pathIndices(hopIndices[i], hopIndices[i + 1]);
    walk.push(...seg.slice(1));
  }
  return walk;
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function sortedJson(obj) {
  const keys = Object.keys(obj).sort();
  return "{" + keys.map((k) => JSON.stringify(k) + ":" + JSON.stringify(obj[k])).join(",") + "}";
}

async function sha256Hex(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function digestReceipt(session_id, mirage_node, timestamp, integrity) {
  const payload = {
    integrity,
    mirage_node: Number(mirage_node),
    session_id,
    timestamp,
  };
  return sha256Hex(sortedJson(payload));
}

function evaluateIntegrity(nodeId, pool, closed) {
  if (closed || nodeId == null) return "FAIL";
  if (!pool.contains(nodeId)) return "FAIL";
  return "PASS";
}

function integrityForNumber(mirageNode, pool) {
  if (!Number.isInteger(mirageNode) || !pool.containsNumber(mirageNode)) return "FAIL";
  try {
    const node = pool.byNumber(mirageNode);
    if (!pool.contains(node.id)) return "FAIL";
  } catch {
    return "FAIL";
  }
  return "PASS";
}

async function mintReceipt(sessionId, node, timestamp, pool, closed = false) {
  const integrity = evaluateIntegrity(node.id, pool, closed);
  const hash = await digestReceipt(sessionId, node.number, timestamp, integrity);
  return { session_id: sessionId, mirage_node: node.number, timestamp, integrity, hash };
}

async function receiptFromDict(data) {
  const required = ["session_id", "mirage_node", "timestamp", "integrity"];
  const missing = required.filter((k) => !(k in data));
  if (missing.length) throw new Error(`receipt missing fields: ${missing}`);
  const mirage_node = Number(data.mirage_node);
  if (!Number.isInteger(mirage_node)) throw new Error("mirage_node must be an integer 1–25");
  const session_id = String(data.session_id);
  const timestamp = String(data.timestamp);
  const integrity = String(data.integrity);
  let stored = data.hash;
  if (stored == null) stored = await digestReceipt(session_id, mirage_node, timestamp, integrity);
  return { session_id, mirage_node, timestamp, integrity, hash: String(stored) };
}

async function hashOk(rec) {
  return (await digestReceipt(rec.session_id, rec.mirage_node, rec.timestamp, rec.integrity)) === rec.hash;
}

async function verifyReceipt(rec, pool) {
  if (!(await hashOk(rec))) return "FAIL";
  const live = integrityForNumber(rec.mirage_node, pool);
  if (live === "FAIL") return "FAIL";
  if (rec.integrity !== "PASS") return "FAIL";
  return "PASS";
}

async function selectIndex(entropy, timestamp) {
  const tsBytes = new TextEncoder().encode(timestamp);
  const seed = new Uint8Array(entropy.length + tsBytes.length);
  seed.set(entropy, 0);
  seed.set(tsBytes, entropy.length);
  const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", seed));
  let n = 0n;
  for (const b of digest) n = (n << 8n) + BigInt(b);
  return Number(n % BigInt(POOL_SIZE));
}

async function selectCircuitIndices(entropy, timestamp, hops = 3) {
  const chosen = [await selectIndex(entropy, timestamp)];
  const used = new Set(chosen);
  let salt = 0;
  const enc = new TextEncoder();
  while (chosen.length < hops) {
    const extra = enc.encode("|hop|");
    const saltB = new Uint8Array(4);
    new DataView(saltB.buffer).setUint32(0, salt);
    const seed = new Uint8Array(entropy.length + enc.encode(timestamp).length + extra.length + 4);
    let o = 0;
    seed.set(entropy, o); o += entropy.length;
    seed.set(enc.encode(timestamp), o); o += enc.encode(timestamp).length;
    seed.set(extra, o); o += extra.length;
    seed.set(saltB, o);
    const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", seed));
    let n = 0n;
    for (const b of digest) n = (n << 8n) + BigInt(b);
    const idx = Number(n % BigInt(POOL_SIZE));
    if (!used.has(idx)) {
      chosen.push(idx);
      used.add(idx);
    }
    salt += 1;
    if (salt > 10000) throw new Error("unable to select distinct circuit hops");
  }
  return chosen;
}

function hex32() {
  const b = crypto.getRandomValues(new Uint8Array(16));
  return [...b].map((x) => x.toString(16).padStart(2, "0")).join("");
}

async function buildCircuit(entropy, timestamp, hops = 3) {
  const indices = await selectCircuitIndices(entropy, timestamp, hops);
  const path = expandCircuitPath(indices);
  const roles = indices.length === 1
    ? ["entry-exit"]
    : ["entry", ...Array(Math.max(0, indices.length - 2)).fill("middle"), "exit"];
  return {
    hops: indices.map((idx, i) => ({
      index: idx,
      node_id: nodeIdFor(idx),
      role: roles[i],
    })),
    path: path.map(nodeIdFor),
    entry: nodeIdFor(indices[0]),
    exit: nodeIdFor(indices[indices.length - 1]),
  };
}

async function assign(body) {
  const pool = makePool(body && body.endpoints);
  const session_id = (body && body.session_id) || hex32();
  const timestamp = (body && body.timestamp) || utcNow();
  const entropy = crypto.getRandomValues(new Uint8Array(32));
  const hops = Number.isInteger(body && body.hops) ? body.hops : 3;
  const index = await selectIndex(entropy, timestamp);
  const node = pool.byIndex(index);
  const receipt = await mintReceipt(session_id, node, timestamp, pool, false);
  const circuit = await buildCircuit(entropy, timestamp, hops);
  return {
    product: PRODUCT,
    version: VERSION,
    motto: MOTTO,
    banner: BANNER,
    kind: "mesh-vpn-circuit",
    session_id,
    node_id: node.id,
    node_label: node.label,
    mirage_node: node.number,
    timestamp,
    circuit,
    receipt,
    note: "Control-plane assignment. Circuit mapping is in-request only. Packet forwarding runs in the local package (miragegrid vpn).",
  };
}

function listNodes() {
  const pool = makePool();
  return {
    product: PRODUCT,
    version: VERSION,
    motto: MOTTO,
    banner: BANNER,
    nodes: pool.nodes.map((n) => ({ id: n.id, label: n.label, number: n.number, endpoint: n.endpoint })),
  };
}

function meshView() {
  const pool = makePool();
  const adjacency = {};
  for (let i = 0; i < POOL_SIZE; i++) {
    adjacency[nodeIdFor(i)] = neighbors(i).map(nodeIdFor);
  }
  return {
    product: PRODUCT,
    version: VERSION,
    banner: BANNER,
    pool_size: POOL_SIZE,
    topology: "circulant-25-1-2-5",
    connected: true,
    peers: pool.nodes.map((n) => ({
      id: n.id,
      label: n.label,
      index: n.index,
      number: n.number,
      endpoint: n.endpoint,
    })),
    adjacency,
  };
}

function routeView(srcId, dstId) {
  const pool = makePool();
  const src = pool.byId(srcId).index;
  const dst = pool.byId(dstId).index;
  const path = pathIndices(src, dst).map(nodeIdFor);
  return {
    product: PRODUCT,
    version: VERSION,
    banner: BANNER,
    from: srcId,
    to: dstId,
    path,
  };
}

function openapiSpec() {
  return {
    openapi: "3.1.0",
    info: {
      title: "MirageGrid runtime",
      version: VERSION,
      description: BANNER + " " + MOTTO,
    },
    servers: [{ url: HOST }],
    paths: {
      "/v1/skill": {
        get: {
          operationId: "miragegrid_skill",
          summary: "Return skill markdown. Does not increment download KV.",
          responses: { "200": { description: "markdown" } },
        },
      },
      "/v1/health": {
        get: { operationId: "health", summary: "Liveness", responses: { "200": { description: "ok", content: { "application/json": { schema: { type: "object" } } } } } },
      },
      "/v1/nodes": {
        get: { operationId: "nodes", summary: "List 25 mesh nodes.", responses: { "200": { description: "nodes", content: { "application/json": { schema: { type: "object" } } } } } },
      },
      "/v1/mesh": {
        get: { operationId: "mesh", summary: "Persistent 25-node mesh topology.", responses: { "200": { description: "mesh", content: { "application/json": { schema: { type: "object" } } } } } },
      },
      "/v1/route": {
        post: {
          operationId: "route",
          summary: "Shortest peer path on the mesh.",
          requestBody: { required: false, content: { "application/json": { schema: { type: "object" } } } },
          responses: { "200": { description: "route", content: { "application/json": { schema: { type: "object" } } } } },
        },
      },
      "/v1/circuit": {
        post: {
          operationId: "circuit",
          summary: "Build onion-circuit hops (entry/middle/exit).",
          requestBody: { required: false, content: { "application/json": { schema: { type: "object" } } } },
          responses: { "200": { description: "circuit", content: { "application/json": { schema: { type: "object" } } } } },
        },
      },
      "/v1/assign": {
        post: {
          operationId: "assign",
          summary: "Assign a mesh circuit for a session and mint a receipt.",
          requestBody: { required: false, content: { "application/json": { schema: { type: "object" } } } },
          responses: { "200": { description: "assignment", content: { "application/json": { schema: { type: "object" } } } } },
        },
      },
      "/v1/verify-receipt": {
        post: {
          operationId: "verifyReceipt",
          summary: "Verify a receipt JSON (hash + pool membership).",
          requestBody: { required: true, content: { "application/json": { schema: { type: "object" } } } },
          responses: { "200": { description: "verify", content: { "application/json": { schema: { type: "object" } } } } },
        },
      },
    },
  };
}

function aiHtml() {
  return `<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MirageGrid — use with Grok, ChatGPT, Venice</title>
<style>
  :root { color-scheme: dark; }
  body { font: 16px/1.45 system-ui, sans-serif; max-width: 42rem; margin: 3rem auto; padding: 0 1.25rem; background: #0e1014; color: #e8eaef; }
  code { background: #151922; padding: .15rem .4rem; border-radius: 4px; }
  a { color: #c9d4ff; }
  .motto { color: #9aa3b2; font-style: italic; }
  .banner { border: 1px solid #2a3140; padding: .8rem 1rem; border-radius: 8px; }
</style>
<body>
  <h1>MirageGrid live API</h1>
  <p class="motto">${MOTTO}</p>
  <p class="banner">${BANNER}</p>
  <h2>ChatGPT (GPT Actions)</h2>
  <p>Paste this OpenAPI URL into GPT Actions:</p>
  <p><code>${HOST}/openapi.json</code></p>
  <h2>Grok / xAI</h2>
  <p>Custom tool pointing at <code>GET ${HOST}/v1/mesh</code>, <code>POST ${HOST}/v1/assign</code>, <code>POST ${HOST}/v1/route</code>.</p>
  <h2>Venice</h2>
  <p>Custom HTTP tool from the same OpenAPI URL.</p>
  <h2>MCP catalog</h2>
  <p>The shared catalog (ships separately) is <code>https://aziel-runtime.vibelock.workers.dev/mcp</code>.</p>
  <p><a href="/openapi.json">openapi.json</a> · <a href="/v1/health">health</a> · <a href="/">downloads</a></p>
</body>
</html>`;
}

export async function handleRuntimeApi(request, url) {
  const path = url.pathname;
  const isApi = path === "/v1" || path.startsWith("/v1/") || path === "/openapi.json" || path === "/ai";
  if (!isApi) return null;
  try {
    if (path === "/v1/health" && request.method === "GET") {
      return json({ ok: true, product: PRODUCT, version: VERSION, banner: BANNER, kind: "node-mesh-vpn" });
    }
    if (path === "/v1/skill" && request.method === "GET") {
      return new Response(SKILL, {
      status: 200,
      headers: { "Content-Type": "text/markdown; charset=utf-8", "Cache-Control": "private, no-store", ...corsHeaders() },
      });
  }
    if (path === "/openapi.json" && request.method === "GET") return json(openapiSpec());
    if (path === "/ai" && request.method === "GET") {
      return new Response(aiHtml(), { headers: { "Content-Type": "text/html; charset=utf-8", ...corsHeaders() } });
    }
    if (path === "/v1/nodes" && request.method === "GET") return json(listNodes());
    if (path === "/v1/mesh" && request.method === "GET") return json(meshView());
    if (path === "/v1/route" && request.method === "POST") {
      let body = {};
      try { body = await request.json(); } catch { body = {}; }
      const src = (body && (body.from || body.src)) || "node-01";
      const dst = (body && (body.to || body.dst)) || "node-13";
      return json(routeView(src, dst));
    }
    if (path === "/v1/circuit" && request.method === "POST") {
      let body = {};
      try { body = await request.json(); } catch { body = {}; }
      const timestamp = (body && body.timestamp) || utcNow();
      const entropy = crypto.getRandomValues(new Uint8Array(32));
      const hops = Number.isInteger(body && body.hops) ? body.hops : 3;
      const circuit = await buildCircuit(entropy, timestamp, hops);
      return json({ product: PRODUCT, version: VERSION, banner: BANNER, timestamp, circuit });
    }
    if (path === "/v1/assign" && request.method === "POST") {
      let body = {};
      try { body = await request.json(); } catch { body = {}; }
      return json(await assign(body && typeof body === "object" ? body : {}));
    }
    if (path === "/v1/verify-receipt" && request.method === "POST") {
      let body;
      try { body = await request.json(); } catch { return json({ error: "JSON body required" }, 400); }
      const recBody = body.receipt && typeof body.receipt === "object" ? body.receipt : body;
      const rec = await receiptFromDict(recBody);
      const pool = makePool();
      const status = await verifyReceipt(rec, pool);
      return json({
        product: PRODUCT,
        version: VERSION,
        banner: BANNER,
        integrity: status,
        session_id: rec.session_id,
        mirage_node: rec.mirage_node,
        timestamp: rec.timestamp,
        hash_ok: await hashOk(rec),
      });
    }
    return json({ error: "not found" }, 404);
  } catch (err) {
    return json({ error: String(err.message || err), banner: BANNER }, 400);
  }
}
