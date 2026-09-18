import worker from "./src/index.js";
import { CAP7_FACTORY_SITES, FACTORY_LABELS, PUBLIC_PAIR, hostedBridgeDoors, publicGateway } from "./src/cap7.js";
import { landIndex, ping, shuffleCite, shuffleSeed } from "./src/shuffle.js";

function assert(cond, label) {
  if (!cond) throw new Error(label);
}

const env = { AZIEL_RUNTIME_ORIGIN: "https://aziel-runtime.vibelock.workers.dev" };

async function call(path, init = {}) {
  const req = new Request("https://miragegrid.vibelock.workers.dev" + path, {
    ...init,
    headers: { "user-agent": "Mozilla/5.0", accept: "application/json", ...(init.headers || {}) },
  });
  return worker.fetch(req, env);
}

assert(CAP7_FACTORY_SITES.length === 7, "cap 7");
assert(new Set(FACTORY_LABELS).size === 7, "distinct labels");
assert(PUBLIC_PAIR[0] === "azgrid" && PUBLIC_PAIR[1] === "azbooth", "public pair");

const bridge = hostedBridgeDoors();
assert(bridge.code === "BRIDGE-CAP7-SHUFFLE", "bridge code");
assert(bridge.app_worker.status === "live-app", "app live");
assert(bridge.honesty.aznet_side_https === "SLOT", "aznet slot");
assert(bridge.public_icann === false, "no icann");
assert(bridge.resolves_to_hub === false, "no hub resolve");
assert(bridge.radio_phy === false, "no radio");
assert(publicGateway("azgrid").ok === true, "azgrid live");
assert(publicGateway("azcloak").ok === false, "azcloak slot");

const seed = await shuffleSeed({ round_id: "r1" });
assert(seed && seed.length === 64, "seed");
assert(landIndex(seed) >= 0 && landIndex(seed) < 7, "land index");

const pingOpen = await ping({ node_id: "node-01" });
assert(pingOpen.code === "CAP7-PING" && pingOpen.continue === true, "open ping");
const landA = await ping({ node_id: "node-01", round_id: "r1" });
const landB = await ping({ node_id: "node-25", round_id: "r1" });
assert(landA.code === "CAP7-LAND", "land");
assert(landA.land.label === landB.land.label, "same seed same land");
assert(landA.hardcoded_host === false, "no hardcoded host");
const update = await ping({ node_id: "node-07", prev: "p", lockset: "l" });
assert(update.update === true && update.update_endpoint, "update land");
assert(shuffleCite().code === "CAP7-SHUFFLE-CITE", "cite");

const home = await call("/");
assert(home.status === 200, "home " + home.status);
const html = await home.text();
assert(html.includes("Cap-7"), "home cap7");
assert(html.includes("azgrid"), "home azgrid");

const health = await call("/v1/health");
assert(health.status === 200, "health");
const healthBody = await health.json();
assert(healthBody.ok === true && healthBody.worker_name === "miragegrid", "health body");

const br = await call("/bridge");
assert(br.status === 200, "bridge http");
const brBody = await br.json();
assert(brBody.code === "BRIDGE-CAP7-SHUFFLE", "bridge live");
assert(brBody.doors.shuffle.includes("/v1/shuffle"), "shuffle door");

const pingRes = await call("/v1/shuffle/ping", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ node_id: "node-01", round_id: "worker-round" }),
});
const pingBody = await pingRes.json();
assert(pingBody.code === "CAP7-LAND", "worker ping land " + pingBody.code);

const slot = await call("/cap7/azcloak");
assert(slot.status === 403, "slot not live https");
const livePair = await call("/cap7/azgrid");
assert(livePair.status === 200, "public pair live");

const azg = await call("/v1/az-generator");
assert(azg.status === 403, "azg not callable");
const azgBody = await azg.json();
assert(azgBody.code === "AZG-NOT-CALLABLE", "azg code");

const enableGet = await call("/v1/mesh/enable");
const enableBody = await enableGet.json();
assert(enableBody.code === "MESH-GET-NO-ENABLE", "get never enables " + enableBody.code);

const assign = await call("/v1/assign", { method: "POST", headers: { "content-type": "application/json" }, body: "{}" });
assert(assign.status === 200, "assign");
const assignBody = await assign.json();
assert(assignBody.receipt && assignBody.node_id, "assign receipt");

console.log("cap7 shuffle worker smoke ok land=" + pingBody.land.label);
