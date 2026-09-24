/**
 * MirageGrid app Worker (name: miragegrid).
 * Cap-7 LIVE shuffle + FragGate doors. Not the download-tracker.
 * Author: Aziel Eliab only.
 */

import { handleMeshApi, outlastHonesty, refuseCallGenerator, refuseGetEnableOrPlant } from "../../download-tracker/src/mesh.js";
import {
  BANNER,
  MOTTO,
  PRODUCT,
  VERSION,
  assign,
  listNodes,
  receiptFromDict,
  hashOk,
  makePool,
  verifyReceipt,
} from "../../download-tracker/src/runtime.js";
import {
  APP_HOST,
  DOWNLOAD_HOST,
  FACTORY_LABELS,
  IDENTITY,
  aznetCite,
  cap7Roster,
  cap7ShuffleDict,
  hostedBridgeDoors,
  publicGateway,
} from "./cap7.js";
import { applyUpdate, ping, shuffleCite } from "./shuffle.js";
import { citeDocument, renderIndexHtml } from "./homepage.js";

const SKILL = `---
name: MirageGrid
description: Use when assigning a session node or citing Cap-7 LIVE shuffle. Dual surface: named app Worker /v1 + catalog MCP. Author Aziel Eliab.
---

# MirageGrid

Named app Worker: \`https://miragegrid.vibelock.workers.dev\`

Cap-7 LIVE shuffle. Nodes ping this Worker until they land on one factory site. That land is the update endpoint for the round. No single hard-coded Cap-7 host.

Download plane (separate): \`https://miragegrid-download-tracker.vibelock.workers.dev\`

Always send \`User-Agent: Mozilla/5.0\`.

| Method | Path | What |
|--------|------|------|
| GET | \`/bridge\` | LIVE door for aziel-runtime. Cap-7 shuffle + honesty. |
| GET | \`/v1/shuffle\` | CAP7-SHUFFLE-1.0 cite. |
| POST | \`/v1/shuffle/ping\` | Ping until land. |
| POST | \`/v1/shuffle/update\` | Update via the landed Cap-7 site. |
| GET | \`/v1/cap7\` | Seven factory sites. Four real hub duplications, three decoys. LIVE. |
| GET | \`/v1/health\` | Liveness. |
| GET | \`/stats\` / \`/v1/stats\` | Honest app/download-plane stats. |
| GET | \`/v1/skill\` | This markdown. |
| GET | \`/v1/nodes\` | 25 mesh nodes. |
| GET | \`/v1/doctor\` | Law stamp + Worker role. |
| POST | \`/v1/assign\` | Session circuit. |
| POST | \`/v1/verify-receipt\` | Verify receipt. |
| GET | \`/v1/mesh\` | PROXY. Default OFF. GET never enables. |

AZ Generator is not callable. \`radio_phy: false\`. Cap-7 is not typed on ICANN DNS. Internet reaches AZ domains only (AZ.AzielEliab.AZ, AZ.AzielCorpusLibrary.AZ, AZ.Godlock.AZ, AZ.HeDidntJump.AZ) via the four hub websites. Factory honesty is LIVE. Live nodes anchor the factory and those doors. FragGate is THE exec door.
`;

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, HEAD, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept, Authorization, X-Aziel-Runtime-Token, User-Agent",
  };
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "private, no-store", ...corsHeaders() },
  });
}

function normPath(pathname) {
  const path = String(pathname || "/").replace(/\/+$/, "") || "/";
  return path.startsWith("/") ? path : "/" + path;
}

const JSON_BODY_LIMIT = 65536;

async function readJsonBody(request, { required = false } = {}) {
  const len = Number(request.headers.get("Content-Length") || "0");
  if (Number.isFinite(len) && len > JSON_BODY_LIMIT) {
    return { error: { ok: false, code: "CAP7-BODY-TOO-LARGE", message: "JSON body exceeds 64 KiB", spec: "CAP7-SHUFFLE-1.0" }, status: 413 };
  }
  let text = "";
  try {
    text = await request.text();
  } catch {
    text = "";
  }
  if (text.length > JSON_BODY_LIMIT) {
    return { error: { ok: false, code: "CAP7-BODY-TOO-LARGE", message: "JSON body exceeds 64 KiB", spec: "CAP7-SHUFFLE-1.0" }, status: 413 };
  }
  if (!String(text || "").trim()) {
    if (required) return { error: { error: "JSON body required" }, status: 400 };
    return { body: {} };
  }
  try {
    const body = JSON.parse(text);
    return { body: body && typeof body === "object" ? body : {} };
  } catch {
    if (required) return { error: { error: "JSON body required" }, status: 400 };
    return { body: {} };
  }
}

function openapiSpec() {
  return {
    openapi: "3.1.0",
    info: {
      title: "MirageGrid app Worker",
      version: VERSION,
      description: BANNER + " Cap-7 LIVE shuffle. Author Aziel Eliab.",
    },
    servers: [{ url: APP_HOST }],
    paths: {
      "/bridge": { get: { operationId: "miragegrid_bridge", summary: "Cap-7 shuffle + SEMANTIC-BRIDGE doors." } },
      "/v1/shuffle": { get: { operationId: "miragegrid_shuffle_cite", summary: "CAP7-SHUFFLE-1.0 cite." } },
      "/v1/shuffle/ping": { post: { operationId: "miragegrid_shuffle_ping", summary: "Ping until land." } },
      "/v1/shuffle/update": { post: { operationId: "miragegrid_shuffle_update", summary: "Update via the landed Cap-7 site. No hard-coded host." } },
      "/v1/cap7": { get: { operationId: "miragegrid_cap7", summary: "Factory roster. Four real hub duplications, three false sites. LIVE. Not ICANN DNS." } },
      "/v1/health": { get: { operationId: "health", summary: "Liveness." } },
      "/stats": { get: { operationId: "stats", summary: "Honest app/download-plane stats." } },
      "/v1/stats": { get: { operationId: "v1Stats", summary: "Honest app/download-plane stats alias." } },
      "/v1/skill": { get: { operationId: "skill", summary: "Skill markdown." } },
      "/v1/nodes": { get: { operationId: "nodes", summary: "25 mesh nodes." } },
      "/v1/doctor": { get: { operationId: "doctor", summary: "Law stamp." } },
      "/v1/assign": { post: { operationId: "assign", summary: "Assign a session circuit." } },
      "/v1/verify-receipt": { post: { operationId: "verifyReceipt", summary: "Verify a receipt." } },
    },
  };
}

function doctor() {
  return {
    ok: true,
    code: "MG-DOCTOR",
    product: PRODUCT,
    version: VERSION,
    worker_name: "miragegrid",
    role: "cap-7-shuffle-app",
    banner: BANNER,
    motto: MOTTO,
    app_worker: APP_HOST,
    download_worker: DOWNLOAD_HOST,
    radio_phy: false,
    public_icann: false,
    resolves_to_hub: false,
    hardcoded_host: false,
    az_generator: { callable: false, exit: "node-gate-front" },
    cap7: cap7ShuffleDict(),
    ...outlastHonesty(),
    author: IDENTITY,
    identity: IDENTITY,
  };
}

function minimalStats() {
  return {
    ok: true,
    product: PRODUCT,
    note: `The named app Worker does not own counters. Honest views/downloads, when available, are maintained by ${DOWNLOAD_HOST}/stats.`,
  };
}

async function appStats() {
  try {
    const upstream = await fetch(`${DOWNLOAD_HOST}/stats`, {
      headers: { Accept: "application/json", "User-Agent": "Mozilla/5.0 MirageGrid-app" },
    });
    if (upstream.ok) {
      const body = await upstream.json();
      if (body && typeof body === "object" && !Array.isArray(body)) {
        return {
          ...body,
          ok: true,
          product: PRODUCT,
          source: `${DOWNLOAD_HOST}/stats`,
          note: "Views/downloads are reported by the separate counted download-tracker; the named app Worker owns no counters.",
        };
      }
    }
  } catch {
    // Keep the app stats route honest if the separate counter plane is unavailable.
  }
  return minimalStats();
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = normPath(url.pathname);
    const method = String(request.method || "GET").toUpperCase();

    if (method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    const getRefuse = refuseGetEnableOrPlant(method, path, url.search || "");
    if (getRefuse) return json(getRefuse, 403);

    if (
      path === "/call-generator" ||
      path === "/run-generator" ||
      path === "/v1/call-generator" ||
      path === "/v1/run-generator" ||
      path === "/v1/az-generator"
    ) {
      return json(refuseCallGenerator(path), 403);
    }

    const mesh = await handleMeshApi(request, url, env);
    if (mesh) return mesh;

    if ((path === "/" || path === "/index.html") && (method === "GET" || method === "HEAD")) {
      return new Response(method === "HEAD" ? null : renderIndexHtml(), {
        status: 200,
        headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "private, no-store", ...corsHeaders() },
      });
    }

    if ((path === "/bridge" || path === "/bridge.json" || path === "/v1/bridge") && (method === "GET" || method === "HEAD")) {
      const doc = hostedBridgeDoors();
      return method === "HEAD" ? new Response(null, { status: 200, headers: corsHeaders() }) : json(doc);
    }

    if ((path === "/cite.json" || path === "/cite.json/") && method === "GET") {
      return json(citeDocument());
    }

    if (path === "/v1/shuffle" && (method === "GET" || method === "HEAD")) {
      const body = shuffleCite();
      const landRound = url.searchParams.get("round_id") || url.searchParams.get("round");
      if (landRound) {
        const landed = await ping({ round_id: landRound, node_id: url.searchParams.get("node_id") }, { method });
        return json({ ...body, land: landed.land || null, ping: landed });
      }
      return json(body);
    }

    if (path === "/v1/shuffle/ping") {
      if (method === "GET" || method === "HEAD") {
        const landed = await ping(
          {
            node_id: url.searchParams.get("node_id"),
            round_id: url.searchParams.get("round_id") || url.searchParams.get("round"),
            prev: url.searchParams.get("prev"),
            lockset: url.searchParams.get("lockset"),
          },
          { method },
        );
        return json(landed);
      }
      if (method !== "POST") return json({ error: "method not allowed", path }, 405);
      const parsed = await readJsonBody(request);
      if (parsed.error) return json(parsed.error, parsed.status);
      return json(await ping(parsed.body, { method }));
    }

    if (path === "/v1/shuffle/land" && (method === "GET" || method === "HEAD")) {
      const landed = await ping(
        {
          node_id: url.searchParams.get("node_id"),
          round_id: url.searchParams.get("round_id") || url.searchParams.get("round"),
          prev: url.searchParams.get("prev"),
          lockset: url.searchParams.get("lockset"),
        },
        { method },
      );
      return json(landed);
    }

    if (path === "/v1/shuffle/update") {
      if (method !== "POST") {
        return json(await applyUpdate({}, { method }), method === "GET" || method === "HEAD" ? 403 : 405);
      }
      const parsed = await readJsonBody(request);
      if (parsed.error) return json(parsed.error, parsed.status);
      const out = await applyUpdate(parsed.body, { method });
      return json(out, out.ok ? 200 : 403);
    }

    if (path === "/v1/cap7" && (method === "GET" || method === "HEAD")) {
      return json({
        ok: true,
        code: "CAP7-ROSTER",
        spec: "CAP7-SHUFFLE-1.0",
        cap: 7,
        public_host_pair: 2,
        sites: cap7Roster(),
        labels: FACTORY_LABELS.slice(),
        real_hub_duplications: ["azgrid", "azcloak", "azvault", "azshift"],
        false_sites: ["azbooth", "azflag", "azstandby"],
        false_site_count: 3,
        real_duplication_count: 4,
        internet_reaches: "az-domains",
        typed_on_icann_dns: false,
        factory_honesty: "LIVE",
        anchored_by_live_nodes: true,
        public_icann: false,
        name_may_change: true,
        radio_phy: false,
        hardcoded_host: false,
        app_worker: APP_HOST,
        author: IDENTITY,
      });
    }

    const cap7Match = path.match(/^\/cap7\/([a-z0-9-]+)(\/update)?$/);
    if (cap7Match) {
      if (cap7Match[2] === "/update") {
        if (method === "GET" || method === "HEAD") {
          return json(await applyUpdate({}, { method }), 403);
        }
        if (method === "POST") {
          return json({
            ok: false,
            code: "CAP7-NO-HARDCODED-HOST",
            message: "update via POST /v1/shuffle/update after ping→land; no hard-coded Cap-7 host",
            hardcoded_host: false,
          }, 403);
        }
      }
      if (method === "GET" || method === "HEAD") {
        const gate = publicGateway(cap7Match[1]);
        return json(gate, gate.ok ? 200 : 403);
      }
    }

    const aznetMatch = path.match(/^\/aznet\/cap7\/([a-z0-9-]+)(\/update)?$/);
    if (aznetMatch) {
      if (aznetMatch[2] === "/update" && (method === "GET" || method === "HEAD")) {
        return json(await applyUpdate({}, { method }), 403);
      }
      if (method === "GET" || method === "HEAD") {
        return json(aznetCite(aznetMatch[1]));
      }
    }

    if (path === "/v1/health" && (method === "GET" || method === "HEAD")) {
      return json({
        ok: true,
        product: PRODUCT,
        version: VERSION,
        worker_name: "miragegrid",
        role: "cap-7-shuffle-app",
        banner: BANNER,
        kind: "cap-7-shuffle-app",
        radio_phy: false,
        public_icann: false,
        resolves_to_hub: false,
        app_worker: APP_HOST,
        download_worker: DOWNLOAD_HOST,
        ...outlastHonesty(),
      });
    }

    if ((path === "/stats" || path === "/v1/stats") && (method === "GET" || method === "HEAD")) {
      const body = await appStats();
      if (method === "HEAD") {
        return new Response(null, {
          status: 200,
          headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "private, no-store", ...corsHeaders() },
        });
      }
      return json(body);
    }

    if (path === "/v1/skill" && method === "GET") {
      return new Response(SKILL, {
        status: 200,
        headers: { "Content-Type": "text/markdown; charset=utf-8", "Cache-Control": "private, no-store", ...corsHeaders() },
      });
    }

    if (path === "/v1/doctor" && (method === "GET" || method === "HEAD")) {
      return json(doctor());
    }

    if (path === "/v1/nodes" && method === "GET") return json(listNodes());

    if (path === "/openapi.json" && method === "GET") return json(openapiSpec());

    if (path === "/v1/assign" && method === "POST") {
      const parsed = await readJsonBody(request);
      if (parsed.error) return json(parsed.error, parsed.status);
      const assigned = await assign(parsed.body && typeof parsed.body === "object" ? parsed.body : {});
      return json({
        ...assigned,
        hosted_kind: "session-assignment",
        ...outlastHonesty(),
      });
    }

    if (path === "/v1/verify-receipt" && method === "POST") {
      const parsed = await readJsonBody(request, { required: true });
      if (parsed.error) return json(parsed.error, parsed.status);
      const body = parsed.body;
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
        ...outlastHonesty(),
      });
    }

    if (path === "/v1" || path.startsWith("/v1/")) {
      return json({ error: "not found", hint: "GET /v1/health /v1/shuffle /bridge POST /v1/shuffle/ping POST /v1/assign" }, 404);
    }

    return json({ error: "not found", worker: "miragegrid", hint: "GET / GET /bridge GET /v1/shuffle" }, 404);
  },
};
