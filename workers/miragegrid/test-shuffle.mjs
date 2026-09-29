import worker from "./src/index.js";
import { CAP7_FACTORY_SITES, FACTORY_LABELS, FALSE_SITES, REAL_HUB_DUPLICATIONS, hostedBridgeDoors, publicGateway } from "./src/cap7.js";
import { applyUpdate, landIndex, ping, shuffleCite, shuffleSeed } from "./src/shuffle.js";
import { applyGridShift, attachQnsCd } from "../download-tracker/src/mesh.js";

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
assert(REAL_HUB_DUPLICATIONS.length === 4 && FALSE_SITES.length === 3, "four real three decoy");
assert(REAL_HUB_DUPLICATIONS.includes("azgrid") && FALSE_SITES.includes("azbooth"), "azgrid real azbooth decoy");

const bridge = hostedBridgeDoors();
assert(bridge.code === "BRIDGE-CAP7-SHUFFLE", "bridge code");
assert(bridge.app_worker.status === "live-app", "app live");
assert(bridge.honesty.factory === "LIVE", "factory live");
assert(bridge.honesty.az_domains === "LIVE", "az domains live");
assert(bridge.public_icann === false, "cap7 not icann dns");
assert(bridge.internet_reaches === "az-domains", "internet is az domains");
assert(bridge.false_site_count === 3, "three decoys");
assert(bridge.real_duplication_count === 4, "four real");
assert(bridge.radio_phy === false, "no radio");
assert(bridge.az_domains.length === 4, "four az doors");
assert(bridge.az_domains.every((row) => row.public_icann === true && row.internet_reachable === true), "az doors public");
assert(publicGateway("azgrid").ok === true && publicGateway("azgrid").hub_duplication === true, "azgrid real");
assert(publicGateway("azbooth").ok === true && publicGateway("azbooth").false_site === true, "azbooth decoy");
assert(publicGateway("azcloak").internet_reachable === false, "cap7 not internet");

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
assert(landA.internet_reachable === false, "land not internet");
assert(landA.factory_honesty === "LIVE", "land factory live");
assert(typeof landA.resolves_to_hub === "boolean", "land resolve stamp");
const seen = new Set();
for (let i = 0; i < 32; i++) {
  const s = await shuffleSeed({ round_id: "round-" + i });
  seen.add(FACTORY_LABELS[landIndex(s)]);
}
assert(seen.size >= 2, "distinct Cap-7 names across seeds");
const update = await ping({ node_id: "node-07", prev: "p", lockset: "l" });
assert(update.update === true && update.update_endpoint, "update land");
assert(shuffleCite().code === "CAP7-SHUFFLE-CITE", "cite");
const upd = await applyUpdate({ node_id: "node-07", prev: "p", lockset: "l" });
assert(upd.code === "CAP7-UPDATE" && upd.phase === "update", "update hop");
assert(upd.update_endpoint === update.update_endpoint, "same land update");
assert(upd.internet_reachable === false, "update not internet");
assert(upd.hosted_update === "LIVE", "update hosted live");
const wait = await applyUpdate({ node_id: "node-07" });
assert(wait.continue === true && wait.phase === "ping", "update waits on land");

const home = await call("/");
assert(home.status === 200, "home " + home.status);
const html = await home.text();
assert(html.includes("Cap-7"), "home cap7");
assert(html.includes("azgrid"), "home azgrid");
assert(html.includes("/v1/shuffle/update"), "home update hop");
assert(html.includes("resolves_to_hub"), "home no hub resolve");
assert(html.includes("Communication/cite plane") || html.includes("Communication plane"), "home communication plane");
assert(html.includes("FragGate is THE"), "home single door");

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
assert(slot.status === 200, "factory cite live");
const slotBody = await slot.json();
assert(slotBody.internet_reachable === false && slotBody.factory_honesty === "LIVE", "cloak factory live not icann");
const livePair = await call("/cap7/azgrid");
assert(livePair.status === 200, "azgrid factory live");

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

const updRes = await call("/v1/shuffle/update", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ node_id: "node-01", prev: "p", lockset: "l" }),
});
const updBody = await updRes.json();
assert(updRes.status === 200 && updBody.code === "CAP7-UPDATE", "worker update " + updBody.code);
assert(updBody.internet_reachable === false, "worker update not internet");
assert(updBody.hosted_update === "LIVE", "worker update live");
const getUpd = await call("/v1/shuffle/update");
const getUpdBody = await getUpd.json();
assert(getUpd.status === 403 && getUpdBody.code === "MESH-GET-NO-ENABLE", "GET update refuses");

assert(landIndex("f".repeat(64)) === Number(BigInt("0x" + "f".repeat(16)) % 7n), "bigint land");
assert(landIndex("f".repeat(64)) === 1, "land f*64 is 1");

const getPlant = await call("/v1/shuffle/ping?prev=p&lockset=l&node_id=node-01");
const getPlantBody = await getPlant.json();
assert(getPlant.status === 403 && getPlantBody.code === "MESH-GET-NO-ENABLE", "GET ping prev+lockset plants not");

const getCapUpd = await call("/cap7/azgrid/update");
const getCapUpdBody = await getCapUpd.json();
assert(getCapUpd.status === 403 && getCapUpdBody.code === "MESH-GET-NO-ENABLE", "GET cap7 update refuses");

const burst = applyGridShift({ cloak_burst: true, names: ["evil.az", "takeover.az"] });
assert(burst.ok === false && burst.code === "MGS-NO-HOSTED-PLANT", "hosted cloak burst refuses " + burst.code);

const stamped = attachQnsCd({ ok: true, node_gate: true, auto_heal: true, anonymity_network: true, enabled: true });
assert(stamped.node_gate === false, "overlay node_gate");
assert(stamped.auto_heal === false, "overlay auto_heal");
assert(stamped.anonymity_network === false, "overlay anonymity");
assert(stamped.this_worker_is_node_gate === false, "overlay this worker");
assert(stamped.enabled === true, "enabled status preserved");
assert(stamped.channel_plane_is_vpn === false, "overlay not vpn");
assert(stamped.second_door === false, "overlay no second door");
assert(stamped.open_proxy === false, "overlay no open proxy");
assert(stamped.hosted_endpoints === "LIVE", "overlay hosted endpoints live");
assert(stamped.factory_honesty === "LIVE", "overlay factory live");
assert(stamped.anchored_by_live_nodes === true, "overlay live-node anchor");
assert(stamped.internet_reaches === "az-domains", "overlay internet az domains");
assert(stamped.aznet_payload_host === false, "overlay no aznet payload host");

const applyShift = applyGridShift({ name: "foo.az" });
assert(applyShift.ok === false && applyShift.code === "MGS-NO-HOSTED-APPLY", "hosted grid-shift apply refuses " + applyShift.code);

assert(updBody.hosted_update === "LIVE", "update hosted LIVE");
assert(updBody.channel_plane_is_vpn === false, "update not vpn");
assert(updBody.second_door === false, "update no second door");
assert(landA.public_shuffle_land_exec === "LIVE", "land exec LIVE");
assert(bridge.honesty.hosted_update === "LIVE", "bridge hosted update live");
assert(bridge.channel_plane_is_vpn === false, "bridge not vpn");

const vpnLie = await ping({ node_id: "node-01", round_id: "r1", channel_plane_is_vpn: true });
assert(vpnLie.code === "CAP7-NO-VPN-LIE", "vpn lie refuse " + vpnLie.code);

const slotHonesty = await call("/cap7/azcloak");
const slotHonestyBody = await slotHonesty.json();
assert(slotHonestyBody.internet_reachable === false, "slot not internet");
assert(slotHonestyBody.hub_duplication === true, "azcloak real duplication");
assert(slotHonestyBody.radio_phy === false, "slot radio");

const healthHonesty = await call("/v1/health");
const healthHonestyBody = await healthHonesty.json();
assert(healthHonestyBody.channel_plane_is_vpn === false, "health not vpn");
assert(healthHonestyBody.second_door === false, "health no second door");
assert(healthHonestyBody.hash_receipt && healthHonestyBody.hash_receipt.second_receipt_door === false, "health hash continuity");

const assignHonesty = await call("/v1/assign", { method: "POST", headers: { "content-type": "application/json" }, body: "{}" });
const assignHonestyBody = await assignHonesty.json();
assert(assignHonestyBody.hosted_kind === "session-assignment", "hosted assign kind");
assert(assignHonestyBody.channel_plane_is_vpn === false, "assign not vpn");
assert(assignHonestyBody.packet_forwarding === false, "assign no packets");

const badNode = await call("/v1/shuffle/ping", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ node_id: "A".repeat(200), round_id: "r" }),
});
const badNodeBody = await badNode.json();
assert(badNodeBody.code === "CAP7-BAD-NODE-ID", "bad node id " + badNodeBody.code);

const locked = await call("/v1/sidenet");
assert(locked.status === 403, "old sidenet name refuses");
const lockedBody = await locked.json();
assert(lockedBody.code === "AZN-NAME-LOCK", "name lock " + lockedBody.code);
assert(lockedBody.name === "AZNet" && lockedBody.sidenet === "AZNet", "sidenet equals AZNet");
assert(lockedBody.public_icann === false && lockedBody.softwares_frozen === true, "lock not icann frozen");

const sidenet = await call("/v1/aznet");
assert(sidenet.status === 200, "aznet cite");
const sidenetBody = await sidenet.json();
assert(sidenetBody.code === "AZN-CAP7-CITE", "aznet code");
assert(sidenetBody.naming_lock === "sidenet=AZNet", "naming lock");
assert(sidenetBody.l0_public_path_changed === false, "l0 unchanged");
assert(sidenetBody.l0.az_domains_public_icann === true, "l0 az domains stay public");
assert(sidenetBody.public_icann === false, "aznet pair not icann");
assert(sidenetBody.callable === false, "generator not callable");
assert(sidenetBody.runs_aznet_engine === false, "does not run aznet engine");
assert(sidenetBody.softwares_frozen === true && sidenetBody.this_route_adds_software === false, "softwares frozen");
assert(sidenetBody.public_browser_gateways.length === 2, "two gateways");
assert(sidenetBody.public_browser_gateways[0] === "azgrid" && sidenetBody.public_browser_gateways[1] === "azbooth", "azgrid azbooth");
assert(sidenetBody.access.pair_verified_at_aznet === false, "no fake aznet verify");

const l0grid = await call("/cap7/azgrid");
assert(l0grid.status === 200, "l0 azgrid cite still live");
const l0cloak = await call("/cap7/azcloak");
assert(l0cloak.status === 200, "l0 azcloak cite still live");

const needPair = await call("/v1/aznet/access", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ name: "azcloak", client: "aznet" }),
});
const needPairBody = await needPair.json();
assert(needPair.status === 403 && needPairBody.code === "AZN-NEED-PAIR", "need pair " + needPairBody.code);

const paired = await call("/v1/aznet/access", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ name: "azcloak", client: "azbrowser", pair_token: "pair-token-1", flag: "azbrowser" }),
});
const pairedBody = await paired.json();
assert(paired.status === 200 && pairedBody.code === "AZN-PAIR-OK", "pair ok " + pairedBody.code);
assert(pairedBody.public_icann === false && pairedBody.pairing_is_tunnel === false, "pair not icann not tunnel");
assert(pairedBody.pair_verified_at_aznet === false && pairedBody.hosts_payloads === false, "pair not verified not payload");

const gateway = await call("/v1/aznet/access", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ name: "azgrid", client: "browser" }),
});
const gatewayBody = await gateway.json();
assert(gateway.status === 200 && gatewayBody.code === "AZG-ACCESS-PUBLIC-GATEWAY", "gateway " + gatewayBody.code);
assert(gatewayBody.public_icann === false && gatewayBody.public_browser_gateway === true, "gateway not icann");

const browserCloak = await call("/v1/aznet/access", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ name: "azcloak", client: "browser" }),
});
const browserCloakBody = await browserCloak.json();
assert(browserCloak.status === 403 && browserCloakBody.code === "AZG-PUBLIC-PAIR", "browser cloak " + browserCloakBody.code);

const icann = await call("/v1/aznet/access", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ name: "azgrid", client: "aznet", public_icann: true, pair_token: "t", flag: "azbrowser" }),
});
const icannBody = await icann.json();
assert(icann.status === 403 && icannBody.code === "AZG-NOT-PUBLIC-REGISTRAR", "icann " + icannBody.code);
assert(icannBody.public_icann === false, "icann stamp stays false");

const hostedClaim = await call("/v1/aznet/claim", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ name: "spare.az" }),
});
const hostedClaimBody = await hostedClaim.json();
assert(hostedClaim.status === 403 && hostedClaimBody.code === "AZG-NOT-CALLABLE", "hosted claim " + hostedClaimBody.code);

const hostedPlant = await call("/v1/aznet/plant", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ name: "spare.az" }),
});
const hostedPlantBody = await hostedPlant.json();
assert(hostedPlant.status === 403 && hostedPlantBody.code === "MGS-NO-HOSTED-PLANT", "hosted plant " + hostedPlantBody.code);

const getPlantSidenet = await call("/v1/aznet/flag");
const getPlantSidenetBody = await getPlantSidenet.json();
assert(getPlantSidenet.status === 403 && getPlantSidenetBody.code === "MESH-GET-NO-ENABLE", "get flag " + getPlantSidenetBody.code);

const hostedRestore = await call("/v1/aznet/restore", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: "{}",
});
const hostedRestoreBody = await hostedRestore.json();
assert(hostedRestore.status === 403 && hostedRestoreBody.code === "AZG-NOT-CALLABLE", "hosted restore " + hostedRestoreBody.code);

console.log("cap7 shuffle worker smoke ok land=" + pingBody.land.label);
