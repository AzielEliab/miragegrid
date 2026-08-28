/**
 * MirageGrid hosted runtime (port of pool/session/receipt/rng/canon).
 * Logical 25-node labels ONLY. Not a VPN/proxy/Tor. Never hide IPs.
 * /v1 never touches DOWNLOADS KV.
 */
const PRODUCT = "miragegrid";
const VERSION = "0.1.0";
const MOTTO = "You enter the booth. The system selects a booth. The call is attributed to that booth. You leave with no persistent booth identity.";
const BANNER = "Not a VPN, proxy, or Tor. Logical 25-node labels only. Never hide IPs. This API never connects, tunnels, or hops addresses.";
const HOST = "https://miragegrid-download-tracker.vibelock.workers.dev";
const POOL_SIZE = 25;

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
    let endpoint = eps[id] || eps[label] || null;
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
  };
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

function hex32() {
  const b = crypto.getRandomValues(new Uint8Array(16));
  return [...b].map((x) => x.toString(16).padStart(2, "0")).join("");
}

async function assign(body) {
  const pool = makePool(body && body.endpoints);
  const session_id = (body && body.session_id) || hex32();
  const timestamp = (body && body.timestamp) || utcNow();
  const entropy = crypto.getRandomValues(new Uint8Array(32));
  const index = await selectIndex(entropy, timestamp);
  const node = pool.byIndex(index);
  const receipt = await mintReceipt(session_id, node, timestamp, pool, false);
  return {
    product: PRODUCT,
    version: VERSION,
    motto: MOTTO,
    banner: BANNER,
    session_id,
    node_id: node.id,
    node_label: node.label,
    mirage_node: node.number,
    timestamp,
    receipt,
    note: "Mapping is in-request only and is destroyed when the response is sent. Logical labels; no network hop.",
  };
}

function listNodes() {
  const pool = makePool();
  return {
    product: PRODUCT,
    version: VERSION,
    motto: MOTTO,
    banner: BANNER,
    nodes: pool.nodes.map((n) => ({ id: n.id, label: n.label, number: n.number })),
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
      "/v1/health": {
        get: { operationId: "health", summary: "Liveness", responses: { "200": { description: "ok", content: { "application/json": { schema: { type: "object" } } } } } },
      },
      "/v1/nodes": {
        get: { operationId: "nodes", summary: "List 25 logical node labels.", responses: { "200": { description: "nodes", content: { "application/json": { schema: { type: "object" } } } } } },
      },
      "/v1/assign": {
        post: {
          operationId: "assign",
          summary: "Assign one logical node for a session and mint a receipt.",
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
  <p>Custom tool pointing at <code>GET ${HOST}/v1/nodes</code>, <code>POST ${HOST}/v1/assign</code>, <code>POST ${HOST}/v1/verify-receipt</code>.</p>
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
      return json({ ok: true, product: PRODUCT, version: VERSION, banner: BANNER });
    }
    if (path === "/openapi.json" && request.method === "GET") return json(openapiSpec());
    if (path === "/ai" && request.method === "GET") {
      return new Response(aiHtml(), { headers: { "Content-Type": "text/html; charset=utf-8", ...corsHeaders() } });
    }
    if (path === "/v1/nodes" && request.method === "GET") return json(listNodes());
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
