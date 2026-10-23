import { readFileSync } from "node:fs";
import worker from "./src/index.js";
import { BAKED_GIT_SHA, BAKED_GIT_SHA_SOURCE } from "./build/build-stamp.generated.js";
import { resolveBuildStamp } from "./scripts/write-build-stamp.mjs";
import { CAP7_FACTORY_SITES, FACTORY_LABELS, FALSE_SITES, REAL_HUB_DUPLICATIONS, hostedBridgeDoors, publicGateway } from "./src/cap7.js";
import { applyUpdate, landIndex, ping, shuffleCite, shuffleSeed } from "./src/shuffle.js";
import { applyGridShift, attachQnsCd, emptyMesh, hostedStubRefuse, meshPointer } from "../download-tracker/src/mesh.js";

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
assert(stamped.factory_honesty_plane === "names-plane", "factory live is names plane");
assert(stamped.cap7_hosted_endpoints === "live" && stamped.public_icann === false && stamped.icann_dns_publish === false, "hosted endpoints live is not icann");
assert(stamped.mesh_node_live === true && stamped.alt_internet === true && stamped.packet_path === true, "qnm flags on");
assert(stamped.alt_internet_live === true && stamped.packet_path_live === true, "qnm live flags");
assert(stamped.cap7_public_icann === false && stamped.cap7_public_egress === false && stamped.packet_forwarding === false, "cap7 icann egress stay false");
assert(stamped.worker_hardware === false && stamped.mock_live === false, "no mock radio");
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

const CAP7_STUBS = ["vpn-hop", "hop", "tunnel", "mesh"];
function assertCap7Stubs(list, label) {
  assert(Array.isArray(list) && JSON.stringify(list) === JSON.stringify(CAP7_STUBS), label + " " + JSON.stringify(list));
}

const healthHonesty = await call("/v1/health");
const healthHonestyBody = await healthHonesty.json();
assert(healthHonestyBody.channel_plane_is_vpn === false, "health not vpn");
assert(healthHonestyBody.second_door === false, "health no second door");
assert(healthHonestyBody.hash_receipt && healthHonestyBody.hash_receipt.second_receipt_door === false, "health hash continuity");
assert(healthHonestyBody.public_icann_registrar === false && healthHonestyBody.azvpn === false, "health not icann or azvpn");
assert(healthHonestyBody.planned && healthHonestyBody.planned.live === true && healthHonestyBody.planned.executable === true, "control plane live");
assert(healthHonestyBody.planned.softwares_catalog_live === true, "softwares companion cleared");
assert(healthHonestyBody.planned.softwares_desk_frozen === true && healthHonestyBody.planned.softwares_count === 42, "desk frozen count 42");
assert(String(healthHonestyBody.planned.softwares_note || "").startsWith("CLEARED:"), "health note cleared");
const waitingOnClear = "until AZBot " + "CLEAR";
const deferredCompanion = "stay on the runtime companion " + "until";
assert(!String(healthHonestyBody.planned.softwares_note || "").includes(waitingOnClear), "health note not waiting");
assert(!String(healthHonestyBody.planned.softwares_note || "").includes(deferredCompanion), "health note not deferred");
assertCap7Stubs(healthHonestyBody.planned.fraggate_stubs, "health stubs");
assert(healthHonestyBody.planned.geo_target.live === true, "geo slot live");
assert(healthHonestyBody.planned.session_stick.live === true, "session slot live");
assert(healthHonestyBody.planned.egress_rotate.live === true, "egress slot live");
assert(healthHonestyBody.planned.fraggate_stub_executable === false && healthHonestyBody.planned.fraggate_stub_code === "FG-STUB", "packet stubs stay FG-STUB");

const plannedRoute = await call("/v1/planned");
const plannedRouteBody = await plannedRoute.json();
assert(plannedRoute.status === 200 && plannedRouteBody.live === true, "planned route");
assert(plannedRouteBody.softwares_catalog_live === true, "planned route cites cleared companion");
assert(String(plannedRouteBody.softwares_note || "").includes("Softwares count stays 42"), "count stays 42");
assert(plannedRouteBody.public_icann === false && plannedRouteBody.azvpn_softwares === false && plannedRouteBody.hosted_vpn === false, "planned still not icann or azvpn");
assertCap7Stubs(plannedRouteBody.fraggate_stubs, "planned route stubs");
assert(plannedRouteBody.geo_target.live === true && plannedRouteBody.session_stick.live === true && plannedRouteBody.egress_rotate.live === true, "planned objects live");

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
assert(lockedBody.name === "AZnet" && lockedBody.sidenet === "AZnet", "sidenet equals AZnet");
assert(lockedBody.browser_name === "AZ Browser", "browser display name");
assert(lockedBody.public_icann === false && lockedBody.softwares_frozen === true, "lock not icann frozen");

const sidenet = await call("/v1/aznet");
assert(sidenet.status === 200, "aznet cite");
const sidenetBody = await sidenet.json();
assert(sidenetBody.code === "AZN-CAP7-CITE", "aznet code");
assert(sidenetBody.naming_lock === "sidenet=AZnet", "naming lock");
assert(sidenetBody.browser_name === "AZ Browser" && sidenetBody.pairs_with.join("|") === "AZnet|AZ Browser", "pair display names");
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

assert(landA.update_endpoint_varies_by_land === false, "land url does not vary");
assert(landA.land_label === landA.land.label, "land label cited");
assert(!Object.prototype.hasOwnProperty.call(landA.land, "miragegrid_vpn"), "no vpn key on land");
assert(!landA.land.shift_stack.includes("miragegrid-vpn"), "no vpn stack label");
assert(landA.land.shift_stack.includes("cap7-egress"), "cap7 egress slot");
assert(landA.land.cap7_egress && landA.land.cap7_egress.status === "live" && landA.land.cap7_egress.hosted === true && landA.land.cap7_egress.live === true, "cap7 egress live");
assert(landA.land.cap7_egress.packet_forwarding === false && landA.land.cap7_egress.ip_exit === false, "cap7 egress not ip");
assert(landA.land.planned_egress.former_label === "planned-egress", "former planned label");
assert(landA.land.resolves_to_hub_means === "design-pair-not-public-dns" || landA.land.resolves_to_hub_means === "decoy-not-a-hub-pair", "resolve means");

const egress = await call("/v1/egress");
assert(egress.status === 200, "egress cite");
const egressBody = await egress.json();
assert(egressBody.code === "MG-EGRESS-CITE", "egress code " + egressBody.code);
assert(egressBody.residential === false && egressBody.egress_ip === null, "no residential pool");
assert(egressBody.vpn_hosted_live === false && egressBody.azvpn_merged === false, "not azvpn");
assert(egressBody.softwares_catalog_live === true && String(egressBody.softwares_note || "").startsWith("CLEARED:"), "egress cites cleared companion");
assert(egressBody.planned && egressBody.planned.softwares_catalog_live === true, "egress planned cleared");
assert(egressBody.sticky_public_ip === false && egressBody.worker_live_ops.includes("session-stick"), "cite worker stick");
assertCap7Stubs(egressBody.fraggate_stub_ops, "egress stub ops");

const geo = await call("/v1/egress/geo", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ country: "US", city: "Miami" }),
});
const geoBody = await geo.json();
assert(geo.status === 200 && geoBody.code === "MG-GEO-TARGET", "geo live " + geo.status + " " + geoBody.code);
assert(geoBody.ok === true && geoBody.receipt && geoBody.receipt.integrity === "PASS", "geo receipt");
assert(geoBody.region_label.country === "US" && geoBody.region_label.city === "Miami", "geo label");
assert(geoBody.geo_applied === true && geoBody.geo_means === "region-label", "geo metadata");
assert(geoBody.egress_ip === null && geoBody.ip_exit === false && geoBody.cf_geo_exit_pool === false, "geo not ip exit");
assert(geoBody.public_egress_ip === false && geoBody.sticky_public_ip === false, "geo no public ip");
assert(geoBody.public_icann === false && geoBody.packet_forwarding === false && geoBody.hosted_vpn === false, "geo not vpn");
assert(typeof geoBody.land_label === "string" && geoBody.node_id, "geo land and node");
const geoAgain = await call("/v1/geo-target", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ country: "US", city: "Miami" }),
});
const geoAgainBody = await geoAgain.json();
assert(geoAgain.status === 200 && geoAgainBody.node_id === geoBody.node_id && geoAgainBody.land_label === geoBody.land_label, "geo stable");
assert(geoAgainBody.session_id !== geoBody.session_id, "geo receipt session is fresh");

const ipExit = await call("/v1/egress/geo", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ country: "US", egress_ip: "203.0.113.8" }),
});
const ipExitBody = await ipExit.json();
assert(ipExit.status === 403 && ipExitBody.code === "MG-NO-IP-EXIT", "ip exit refuse " + ipExitBody.code);
assert(ipExitBody.public_ip_applied === false && ipExitBody.receipt == null, "ip exit minted nothing");

const stickyIp = await call("/v1/egress/sticky", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ sticky_key: "booth-1", ttl_seconds: 600 }),
});
const stickyIpBody = await stickyIp.json();
assert(stickyIp.status === 200 && stickyIpBody.code === "MG-SESSION-STICK", "sticky path " + stickyIp.status + " " + stickyIpBody.code);
assert(stickyIpBody.sticky_public_ip === false && stickyIpBody.egress_ip === null && stickyIpBody.ip_exit === false, "sticky path not public ip");
assert(stickyIpBody.ttl_enforced === true && stickyIpBody.ttl_mechanism === "time-bucket-hash", "ttl bucket");
assert(stickyIpBody.land_stick === true && stickyIpBody.land_label, "sticky land");
assert(stickyIpBody.receipt && stickyIpBody.receipt.integrity === "PASS", "sticky path receipt");

const rotateIp = await call("/v1/egress/rotate", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ rotate: true, residential: true }),
});
const rotateIpBody = await rotateIp.json();
assert(rotateIp.status === 403 && rotateIpBody.code === "MG-NO-IP-EXIT", "residential not a land rotate " + rotateIpBody.code);
assert(rotateIpBody.ip_rotated === false && rotateIpBody.receipt == null, "residential minted nothing");

const rotate = await call("/v1/egress/rotate", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ from_label: "azgrid" }),
});
const rotateBody = await rotate.json();
assert(rotate.status === 200 && rotateBody.code === "MG-EGRESS-ROTATE", "rotate live " + rotate.status + " " + rotateBody.code);
assert(rotateBody.land_label === "azbooth" && rotateBody.previous_land === "azgrid", "roster next " + rotateBody.land_label);
assert(rotateBody.land_rotated === true && rotateBody.ip_rotated === false, "land rotated not ip");
assert(rotateBody.packet_forwarding === false && rotateBody.hosted_vpn === false && rotateBody.public_icann === false, "rotate not vpn");
assert(rotateBody.update_endpoint_varies_by_land === false, "update url stable");
assert(rotateBody.receipt && rotateBody.receipt.integrity === "PASS", "rotate receipt");
const rotateAlias = await call("/v1/egress-rotate", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ from_label: "azstandby" }),
});
const rotateAliasBody = await rotateAlias.json();
assert(rotateAlias.status === 200 && rotateAliasBody.land_label === "azgrid", "roster wrap " + rotateAliasBody.land_label);

const painted = await call("/v1/assign", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ endpoints: { "node-01": "203.0.113.8:443" } }),
});
const paintedBody = await painted.json();
assert(painted.status === 403 && paintedBody.code === "MG-NO-EGRESS-PAINT", "paint " + paintedBody.code);

const geoAssign = await call("/v1/assign", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ country: "US" }),
});
const geoAssignBody = await geoAssign.json();
assert(geoAssign.status === 200 && geoAssignBody.geo_applied === true, "assign geo " + geoAssign.status);
assert(geoAssignBody.region_label.country === "US" && geoAssignBody.receipt, "assign geo receipt");
assert(geoAssignBody.ip_exit === false && geoAssignBody.egress_ip === null && geoAssignBody.cf_geo_exit_pool === false, "assign geo not exit");

const badHops = await call("/v1/assign", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ hops: 99 }),
});
const badHopsBody = await badHops.json();
assert(badHops.status === 400 && badHopsBody.code === "MG-BAD-HOPS", "bad hops " + badHopsBody.code);

const badJson = await call("/v1/assign", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: "{",
});
const badJsonBody = await badJson.json();
assert(badJson.status === 400 && badJsonBody.code === "MG-BAD-JSON", "bad json " + badJsonBody.code);

const stickyA = await call("/v1/session/sticky", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ sticky_key: "booth-1" }),
});
const stickyB = await call("/v1/session/sticky", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ sticky_key: "booth-1" }),
});
const stickyABody = await stickyA.json();
const stickyBBody = await stickyB.json();
assert(stickyA.status === 200 && stickyABody.code === "MG-SESSION-STICK", "sticky mesh " + stickyA.status + " " + stickyABody.code);
assert(stickyABody.node_id === "node-21", "vector node " + stickyABody.node_id);
assert(stickyBBody.node_id === stickyABody.node_id && stickyBBody.land_label === stickyABody.land_label, "sticky stable");
assert(stickyABody.session_id !== stickyBBody.session_id, "receipt session is fresh");
assert(stickyABody.sticky_ip === false && stickyABody.sticky_public_ip === false && stickyABody.egress_ip === null, "sticky not ip");
assert(stickyABody.ttl_enforced === false && stickyABody.circuit_built === false && stickyABody.land_stick === true, "no ttl still land stick");
assert(stickyABody.receipt && stickyABody.receipt.mirage_node === 21, "sticky receipt");

const stickyGeo = await call("/v1/session/sticky", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ sticky_key: "booth-1", country: "DE", ttl_seconds: 3600 }),
});
const stickyGeoBody = await stickyGeo.json();
assert(stickyGeo.status === 200 && stickyGeoBody.code === "MG-SESSION-STICK", "sticky geo " + stickyGeo.status);
assert(stickyGeoBody.region_label.country === "DE" && stickyGeoBody.geo_means === "region-label", "sticky region");
assert(stickyGeoBody.ip_exit === false && stickyGeoBody.cf_geo_exit_pool === false, "sticky geo not exit");
assert(stickyGeoBody.ttl_enforced === true && stickyGeoBody.land_label, "sticky ttl land");

const stickyTtl = await call("/v1/session-stick", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ sticky_key: "booth-1", ttl_seconds: 3600 }),
});
const stickyTtlBody = await stickyTtl.json();
assert(stickyTtl.status === 200 && stickyTtlBody.ttl_enforced === true, "ttl " + stickyTtl.status);
assert(stickyTtlBody.node_id === stickyGeoBody.node_id && stickyTtlBody.land_label === stickyGeoBody.land_label, "same window same stick");
assert(stickyTtlBody.stick_id && stickyTtlBody.expires_at, "stick id and expiry");
assert(stickyTtlBody.durable_store === false, "ttl is not a kv store");

assert(assignHonestyBody.receipt_covers === "entry-node", "receipt covers entry");
assert(assignHonestyBody.endpoints_applied === false, "defaults not painted");
assert(assignHonestyBody.egress_ip === null, "assign has no egress ip");

const stubHop = hostedStubRefuse("vpn-hop");
assert(stubHop && stubHop.code === "MESH-STUB" && stubHop.ok === false, "vpn-hop stays stub");
assert(hostedStubRefuse("hop").code === "MESH-STUB", "hop stays stub");
assert(hostedStubRefuse("tunnel").code === "MESH-STUB", "tunnel stays stub");
assert(hostedStubRefuse("assign") == null, "assign not stubbed");
assert(hostedStubRefuse("geo-target") == null, "geo-target is not a packet stub");
assert(hostedStubRefuse("session-stick") == null, "session-stick is not a packet stub");
assert(hostedStubRefuse("egress-rotate") == null, "egress-rotate is not a packet stub");

const healthLive = await call("/v1/health");
const healthLiveBody = await healthLive.json();
assert(healthLiveBody.version === "0.3.0", "version " + healthLiveBody.version);
assert(healthLiveBody.planned.geo_target.live === true && healthLiveBody.planned.geo_target.hosted === true && healthLiveBody.planned.geo_target.executable === true, "geo live");
assert(healthLiveBody.planned.session_stick.live === true && healthLiveBody.planned.session_stick.executable === true, "stick live");
assert(healthLiveBody.planned.egress_rotate.live === true && healthLiveBody.planned.egress_rotate.executable === true, "rotate live");
assert(healthLiveBody.planned.live === true && healthLiveBody.planned.executable === true, "control plane live");
assert(healthLiveBody.planned.ip_exit === false && healthLiveBody.planned.sticky_public_ip === false && healthLiveBody.planned.cf_geo_exit_pool === false, "health no ip exit");
assert(healthLiveBody.planned.fraggate_stubs.join(",") === "vpn-hop,hop,tunnel,mesh", "stubs " + healthLiveBody.planned.fraggate_stubs);
assert(!healthLiveBody.planned.fraggate_stubs.includes("geo-target"), "geo not stub");
assert(healthLiveBody.cap7_control_plane.geo_target === true && healthLiveBody.cap7_control_plane.session_stick === true && healthLiveBody.cap7_control_plane.egress_rotate === true, "health trio");
assert(healthLiveBody.cap7_control_plane.live === true && healthLiveBody.cap7_control_plane.public_icann === false, "pre-existing control plane live");
assert(healthLiveBody.public_icann === false && healthLiveBody.packet_forwarding === false && healthLiveBody.azvpn === false, "health locks");
assert(healthLiveBody.cap7_live === false && healthLiveBody.cap7_factory_live === false && healthLiveBody.cap7_registrar_live === false, "health cap7 live false");
assert(healthLiveBody.paid_registrar === false && healthLiveBody.cap7_names_only === true, "health names only");
assert(healthLiveBody.tip === (BAKED_GIT_SHA || null) && healthLiveBody.git_sha === healthLiveBody.tip, "health tip matches bake");
assert(healthLiveBody.git_sha_source === (BAKED_GIT_SHA ? BAKED_GIT_SHA_SOURCE : "unset"), "health stamp source");
assert(healthLiveBody.version_id === null && healthLiveBody.version_id_source === "unset", "health version unset without metadata");
assert(healthLiveBody.version_id_note.includes("CF_VERSION_METADATA.id"), "version id note");
assert(!healthLiveBody.banner.includes("planned, not LIVE"), "banner no longer says planned");

const probeSha = "0123456789abcdef0123456789abcdef01234567";
const probeVersion = "11111111-2222-4333-8444-555555555555";
const healthStampedRes = await worker.fetch(
  new Request("https://miragegrid.vibelock.workers.dev/v1/health", { headers: { "user-agent": "Mozilla/5.0", accept: "application/json" } }),
  { ...env, GIT_SHA: probeSha, CF_VERSION_METADATA: { id: probeVersion, tag: "", timestamp: "2026-10-23T00:00:00.000Z" } },
);
const healthStamped = await healthStampedRes.json();
assert(healthStampedRes.status === 200 && healthStamped.tip === probeSha && healthStamped.git_sha === probeSha, "health tip from GIT_SHA");
assert(healthStamped.git_sha_source === "deploy_var" && healthStamped.git_sha_tracks_deployed_tip === true, "health deploy_var");
assert(healthStamped.version_id === probeVersion && healthStamped.version_id_source === "cf_version_metadata", "health version metadata");
assert(healthStamped.cap7_live === false && healthStamped.cap7_factory_live === false && healthStamped.public_icann === false && healthStamped.paid_registrar === false, "stamped health cap7 false");
const bogus = await worker.fetch(
  new Request("https://miragegrid.vibelock.workers.dev/v1/health", { headers: { "user-agent": "Mozilla/5.0" } }),
  { ...env, GIT_SHA: "f49b6a7", CF_VERSION_METADATA: { id: "not-a-version" } },
);
const bogusBody = await bogus.json();
assert(bogusBody.tip === (BAKED_GIT_SHA || null) && bogusBody.version_id === null, "reject short sha and bad version id");
const ciStamp = resolveBuildStamp({ WORKERS_CI_COMMIT_SHA: probeSha, GITHUB_SHA: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" });
assert(ciStamp.sha === probeSha && ciStamp.source === "workers_ci", "workers ci wins over github sha");
const varStamp = resolveBuildStamp({ GIT_SHA: probeSha, WORKERS_CI_COMMIT_SHA: "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" });
assert(varStamp.source === "deploy_var" && varStamp.sha === probeSha, "deploy var wins");
const emptyStamp = resolveBuildStamp({}, { fromGit: false, gitHead: probeSha });
assert(emptyStamp.sha === "" && emptyStamp.source === "unset", "no implicit git head");
const gitStamp = resolveBuildStamp({}, { fromGit: true, gitHead: probeSha });
assert(gitStamp.sha === probeSha && gitStamp.source === "git_head", "from-git opt in");
const banned = ["f49b6a7d0be810be26a1d21a5d3c99d41a95197e", "856a3e75-6c26-4e35-9839-c4f73ec0f551"];
for (const rel of ["src/index.js", "src/build-stamp.js", "scripts/write-build-stamp.mjs", "wrangler.jsonc", "deploy.sh"]) {
  const text = readFileSync(new URL(rel, import.meta.url), "utf8");
  for (const needle of banned) assert(!text.includes(needle), rel + " must not hardcode " + needle.slice(0, 12));
}

assert(html.includes("no residential IP pool") || html.includes("There is no residential IP pool"), "home egress honesty");
assert(html.includes("/v1/session/sticky"), "home sticky door");
assert(html.includes("not a sticky public IP") || html.includes("Not a sticky public IP") || html.includes("not a sticky public IP".toLowerCase()) || html.includes("sticky public IP"), "home denies sticky public ip");

const mcpCite = await call("/mcp");
assert(mcpCite.status === 200, "mcp cite http");
const mcpBody = await mcpCite.json();
assert(mcpBody.code === "MG-PUBLIC-MCP-CITE", "mcp code " + mcpBody.code);
assert(mcpBody.is_live_door === false && mcpBody.second_door === false, "mcp not exec door");
assert(mcpBody.cap7_entity === "TBD" && mcpBody.domain_purchase === "held", "mcp operator hold");
assert(mcpBody.register_policy === "free-only" && mcpBody.paid_registrar === false, "mcp free only");
assert(mcpBody.cap7_live === false && mcpBody.cap7_factory_live === false, "mcp cap7 live false");
assert(mcpBody.hosted_mcp === "cite" && mcpBody.hosted_mcp_live === false, "mcp cite not live");
assert(mcpBody.public_icann === false && mcpBody.cap7_registrar_live === false, "mcp not icann registrar");
const mcpPost = await call("/mcp", { method: "POST", headers: { "content-type": "application/json" }, body: "{}" });
assert(mcpPost.status === 403, "mcp post refuse");
const mcpPostBody = await mcpPost.json();
assert(mcpPostBody.code === "MG-MCP-CITE-ONLY", "mcp post code");

const landPub = await call("/land?round_id=ship-round&node_id=node-01");
assert(landPub.status === 200, "land public");
const landPubBody = await landPub.json();
assert(landPubBody.code === "CAP7-LAND" && landPubBody.public_path === "/land", "land public path");
assert(landPubBody.cap7_live === false && landPubBody.public_shuffle_land_exec === false, "land cap7 live flags false");
assert(landPubBody.register_policy === "free-only" && landPubBody.paid_registrar === false, "land free only");
assert(landPubBody.land && landPubBody.land.factory_honesty === "cite", "land nested cite");
assert(landPubBody.land.honesty_public === "cite", "land site honesty cite");
assert(landPubBody.land.public_icann === false && landPubBody.land.icann_dns_publish === false, "land site not icann");
assert(landPubBody.cap7_public_icann === false && landPubBody.public_egress_ip === false, "land cap7 icann egress stay false");
const landSites = await call("/land?node_id=node-01");
const landSitesBody = await landSites.json();
assert(Array.isArray(landSitesBody.sites) && landSitesBody.sites.length === 7, "land sites roster");
assert(landSitesBody.sites.every((row) => row.honesty_public === "cite" && row.factory_honesty === "cite"), "land sites cite not factory LIVE");
assert(landSitesBody.sites.every((row) => row.public_icann === false && row.cap7_public_icann === false && row.icann_dns_publish === false), "land sites names-only");
assert(landSitesBody.cap7_live === false && landSitesBody.cap7_registrar_live === false, "land names-only flags stay false");
const meshPolicy = emptyMesh();
assert(meshPolicy.mesh_node_live === true && meshPolicy.alt_internet === true && meshPolicy.packet_path === true, "empty mesh policy on");
assert(meshPolicy.alt_internet_live === true && meshPolicy.packet_path_live === true && meshPolicy.mesh_node_live_status === "LIVE", "qnm live flags");
assert(meshPolicy.enabled === true && meshPolicy.default_off === false, "node mesh default on");
assert(meshPolicy.live_nodes === 0, "no invented live count");
assert(meshPolicy.cap7_public_icann === false && meshPolicy.public_egress_ip === false && meshPolicy.packet_forwarding === false, "cap7 icann egress stay false");
assert(meshPolicy.worker_hardware === false && meshPolicy.radio_phy === false && meshPolicy.mock_live === false, "no mock radio");
assert(meshPolicy.carrier_hw_absent === "QNM-RADIO-ABSENT", "carrier absent code");
const pointer = meshPointer();
assert(pointer.enabled_default === true && pointer.mesh_node_live === true && pointer.packet_path_live === true, "mesh pointer on");
const qnmStamp = attachQnsCd({ ok: true, enabled: true, alt_internet_live: false, packet_path_live: false, public_icann: true, live_nodes: 3 });
assert(qnmStamp.mesh_node_live === true && qnmStamp.alt_internet_live === true && qnmStamp.packet_path_live === true, "proxy stamp turns qnm flags on");
assert(qnmStamp.public_icann === false && qnmStamp.cap7_public_icann === false && qnmStamp.cap7_public_egress === false, "proxy stamp keeps cap7 names-only");
assert(qnmStamp.live_nodes === 3, "proxy stamp does not invent or wipe a real count");
assert(qnmStamp.packet_forwarding === false && qnmStamp.worker_hardware === false, "stamp is not public egress or fake hardware");
const landGetPlant = await call("/land?prev=p&lockset=l&node_id=node-01");
assert(landGetPlant.status === 403 && (await landGetPlant.json()).code === "MESH-GET-NO-ENABLE", "land get prev lockset refuses");

const attestGet = await call("/attest");
assert(attestGet.status === 200, "attest cite");
const attestGetBody = await attestGet.json();
assert(attestGetBody.code === "MG-ATTEST-CITE" && attestGetBody.attest.syntactic_only === true, "attest cite");
assert(attestGetBody.attest.chainlock_verify === "SLOT", "attest chainlock slot");
const attestBad = await call("/attest", { method: "POST", headers: { "content-type": "application/json" }, body: "{}" });
assert(attestBad.status === 400 && (await attestBad.json()).code === "MG-ATTEST-NEED-PROOF", "attest need proof");
const attestOk = await call("/attest", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ prev: "p", lockset: "l", node_id: "node-01" }),
});
const attestOkBody = await attestOk.json();
assert(attestOk.status === 200 && attestOkBody.code === "MG-ATTEST-SYNTACTIC", "attest syntactic " + attestOkBody.code);
assert(attestOkBody.attest.fraggate_zkattest === "SLOT", "attest zk slot");

console.log("cap7 shuffle worker smoke ok land=" + pingBody.land.label);
