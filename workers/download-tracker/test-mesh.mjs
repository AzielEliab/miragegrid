import { handleMeshApi } from "./src/mesh.js";

function assert(cond, label) {
  if (!cond) throw new Error(label);
}

const env = { AZIEL_RUNTIME_ORIGIN: "https://aziel-runtime.vibelock.workers.dev" };

async function call(path, init = {}) {
  const req = new Request("https://example.test" + path, {
    ...init,
    headers: { "user-agent": "Mozilla/5.0", accept: "application/json", ...(init.headers || {}) },
  });
  return handleMeshApi(req, new URL(req.url), env);
}

const status = await call("/v1/mesh/status");
assert(status && status.status === 200, "GET /v1/mesh/status HTTP " + (status && status.status));
const body = await status.json();
assert(body.code === "MESH-OK", "expected MESH-OK, got " + JSON.stringify(body.code));
assert(body.enabled === false, "expected enabled:false, got " + JSON.stringify(body.enabled));
assert(body.qns_cd_spec === "QNS-CD-1.0", "expected qns_cd_spec QNS-CD-1.0, got " + JSON.stringify(body.qns_cd_spec));
assert(body.qns_cd && body.qns_cd.spec === "QNS-CD-1.0", "expected qns_cd.spec QNS-CD-1.0");
assert(body.qns_cd.name === "photon QNS1 packet transfer", "expected photon QNS1 name");
assert(body.qns_cd.public_proxy === false && body.qns_cd.qnsd_proxy === false, "qnsd must not be a public proxy");
assert(body.qns_cd.softwares_tab === false, "QNS-CD is not a Softwares-tab product");
assert(body.qns_cd.node_gate === false, "no Node Gate");
assert(String(body.qns_cd.local_repo || "").includes("qnm-node"), "qns_cd must cite qnm-node");
assert(String(body.qns_cd.runtime_repo || "").includes("aziel-runtime"), "qns_cd must cite aziel-runtime");

const enable = await call("/v1/mesh/enable", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: "{}",
});
const enableBody = await enable.json();
assert(
  enableBody.code === "MESH-NEED-BEARER" || enableBody.enabled === false,
  "empty enable should stay off / MESH-NEED-BEARER, got " + JSON.stringify(enableBody),
);

const unknown = await call("/v1/mesh/not-a-door");
assert(unknown.status === 404, "unknown path HTTP " + unknown.status);
const unknownBody = await unknown.json();
assert(unknownBody.code === "MESH-UNKNOWN", "expected MESH-UNKNOWN, got " + JSON.stringify(unknownBody.code));

const join = await call("/v1/mesh/join", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ product: "miragegrid", label: "MirageGrid Worker" }),
});
const joinBody = await join.json();
assert(joinBody.code === "MESH-OFF" || joinBody.enabled === false, "join while OFF should be MESH-OFF, got " + JSON.stringify(joinBody));

console.log("GET /v1/mesh/status MESH-OK enabled:false qns_cd_spec=" + body.qns_cd_spec);
console.log("POST /v1/mesh/enable {} →", enableBody.code);
console.log("GET /v1/mesh/not-a-door →", unknownBody.code);
console.log("POST /v1/mesh/join while OFF →", joinBody.code);
console.log("mesh proxy smoke ok");
