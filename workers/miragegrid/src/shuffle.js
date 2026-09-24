/**
 * CAP7-SHUFFLE-1.0 — ping MirageGrid until land.
 * Land is SHA-256(seed) mod 7. No hard-coded Cap-7 host.
 * Update seed is prev|lockset (proof, not a timer).
 * Author: Aziel Eliab only.
 */

import {
  APP_HOST,
  CAP7_FACTORY_SITES,
  CAP7_SHUFFLE_SPEC,
  CAP_7,
  IDENTITY,
  appWorker,
  cap7Roster,
  cap7ShuffleDict,
  siteRecord,
} from "./cap7.js";
import { outlastHonesty, refuseCallGenerator, refuseGetEnableOrPlant } from "../../download-tracker/src/mesh.js";

function verdict(ok, code, v, message, extra) {
  return {
    ok: !!ok,
    code,
    verdict: v,
    yes: v === "yes",
    message,
    author: IDENTITY,
    identity: IDENTITY,
    spec: CAP7_SHUFFLE_SPEC,
    ...(extra || {}),
  };
}

export async function sha256Hex(text) {
  const bytes = new TextEncoder().encode(String(text));
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export async function shuffleSeed({ prev, lockset, round_id } = {}) {
  const p = String(prev || "").trim();
  const lock = String(lockset || "").trim();
  const rid = String(round_id || "").trim();
  if (p && lock) return sha256Hex(p + "|" + lock);
  if (rid) return sha256Hex("round|" + rid);
  return null;
}

export function landIndex(seedHex) {
  const hex = String(seedHex || "").replace(/[^0-9a-f]/gi, "").toLowerCase();
  const slice = (hex || "0").padStart(1, "0").slice(0, 16);
  // 16 hex digits are 64 bits — Number.parseInt loses precision above 2^53-1.
  try {
    return Number(BigInt("0x" + slice) % BigInt(CAP_7));
  } catch {
    return 0;
  }
}

const NODE_ID_RE = /^[A-Za-z0-9._-]{1,80}$/;

export function sanitizeNodeId(raw) {
  const node = String(raw || "").trim();
  if (!node) return { ok: true, node_id: "anonymous" };
  if (!NODE_ID_RE.test(node)) {
    return {
      ok: false,
      code: "CAP7-BAD-NODE-ID",
      verdict: "refuse",
      yes: false,
      message: "node_id must be 1–80 [A-Za-z0-9._-]",
      spec: CAP7_SHUFFLE_SPEC,
      author: IDENTITY,
    };
  }
  return { ok: true, node_id: node };
}

export function landSite(seedHex) {
  return siteRecord(CAP7_FACTORY_SITES[landIndex(seedHex)]);
}

export async function applyUpdate(body, { method } = {}) {
  const m = String(method || "POST").toUpperCase();
  if (m !== "POST") {
    return {
      ok: false,
      code: "MESH-GET-NO-ENABLE",
      verdict: "refuse",
      yes: false,
      message: "GET never plants an update; POST /v1/shuffle/update after ping→land",
      get_never_plants: true,
      spec: CAP7_SHUFFLE_SPEC,
      author: IDENTITY,
    };
  }
  const landed = await ping(body, { method: "POST" });
  if (!landed.ok) return landed;
  if (landed.phase !== "land" || !landed.land) {
    return {
      ...landed,
      code: "CAP7-PING",
      phase: "ping",
      continue: true,
      update: false,
      message: "update waits on land; ping MirageGrid with prev+lockset or round_id",
    };
  }
  return {
    ok: true,
    code: "CAP7-UPDATE",
    verdict: "yes",
    yes: true,
    message: "update endpoint is the landed Cap-7 site for this round; no hard-coded host",
    phase: "update",
    continue: false,
    land: landed.land,
    update: true,
    update_endpoint: landed.land.update_path,
    round_seed: landed.round_seed,
    node_id: landed.node_id,
    hardcoded_host: false,
    resolves_to_hub: !!landed.land.resolves_to_hub,
    false_site: !!landed.land.false_site,
    hub_duplication: !!landed.land.hub_duplication,
    public_icann: false,
    typed_on_icann_dns: false,
    internet_reachable: false,
    internet_reaches: "az-domains",
    radio_phy: false,
    hosted_update: "LIVE",
    hosted_mcp: "LIVE",
    public_shuffle_land_exec: "LIVE",
    factory_honesty: "LIVE",
    anchored_by_live_nodes: true,
    is_live_door: false,
    channel_plane_is_vpn: false,
    second_door: false,
    spec: CAP7_SHUFFLE_SPEC,
    author: IDENTITY,
    identity: IDENTITY,
    app_worker: appWorker(),
  };
}

export function shuffleCite() {
  const law = cap7ShuffleDict();
  return verdict(true, "CAP7-SHUFFLE-CITE", "yes", "CAP7-SHUFFLE-1.0 cite. Four real .az hub duplications, three false sites. Internet reaches AZ domains only.", {
    ...law,
    doors: {
      bridge: APP_HOST + "/bridge",
      bridge_json: APP_HOST + "/bridge.json",
      v1_bridge: APP_HOST + "/v1/bridge",
      shuffle: APP_HOST + "/v1/shuffle",
      ping: APP_HOST + "/v1/shuffle/ping",
      land: APP_HOST + "/v1/shuffle/land",
      update: APP_HOST + "/v1/shuffle/update",
      cap7: APP_HOST + "/v1/cap7",
    },
    phase: "cite",
    continue: false,
    land: null,
  });
}

export async function ping(body, { method } = {}) {
  const b = body && typeof body === "object" ? body : {};
  const m = String(method || "POST").toUpperCase();
  const path = "/v1/shuffle/ping";
  const getRefuse = refuseGetEnableOrPlant(m, path, "");
  if (getRefuse) return getRefuse;
  if (b.inbound_call || b.call_generator || b.run_generator) return refuseCallGenerator("cap7-shuffle-ping");
  if (b.radio_phy || b.rf || b.bluetooth || b.wifi || b.photon_phy) {
    return verdict(false, "AZG-NO-RADIO-PHY", "refuse", "MirageGrid is not RF/BT/Wi-Fi/photon radio PHY", {
      radio_phy: false, hub_get_enables_mesh: false,
    });
  }
  if (b.icann_registrar_purchase || b.cctld_purchase || b.public_registrar) {
    return verdict(false, "AZG-NOT-PUBLIC-REGISTRAR", "refuse", "mesh DNS factory is not an ICANN registrar purchase of a ccTLD", {
      icann_registrar_purchase: false, registrar: false, cctld_purchase: false,
    });
  }
  if (b.typed_on_icann_dns || b.cap7_on_icann) {
    return verdict(false, "CAP7-NOT-ICANN-DNS", "refuse", "Cap-7 is not publicly typed on ICANN DNS. Internet reaches AZ domains via the four hub websites.", {
      typed_on_icann_dns: false, internet_reaches: "az-domains", factory_honesty: "LIVE",
    });
  }
  if (b.invent_first_flag) {
    return verdict(false, "BRIDGE-NO-INVENT-HTTPS", "refuse", "empty Cap-7: do not invent www.survivalnetwork.az as live HTTPS", {
      invented_first_flag_https: false,
    });
  }
  if (b.hardcoded_host) {
    return verdict(false, "CAP7-NO-HARDCODED-HOST", "refuse", "update shuffle has no single hard-coded Cap-7 host; land comes from the ping seed", {
      hardcoded_host: false,
    });
  }
  if (b.channel_plane_is_vpn || b.hosted_vpn || b.pairing_is_tunnel || b.second_door || b.open_proxy) {
    return verdict(false, "CAP7-NO-VPN-LIE", "refuse", "hosted Cap-7 is a communication/cite plane; not a VPN, tunnel, second FragGate door, or open proxy", {
      ...outlastHonesty(),
    });
  }

  const prev = String(b.prev || "").trim();
  const lock = String(b.lockset || "").trim();
  if ((m === "GET" || m === "HEAD") && prev && lock) {
    return {
      ok: false,
      code: "MESH-GET-NO-ENABLE",
      verdict: "refuse",
      yes: false,
      message: "GET never plants an update; POST /v1/shuffle/update after ping→land",
      get_never_plants: true,
      spec: CAP7_SHUFFLE_SPEC,
      author: IDENTITY,
    };
  }

  const seed = await shuffleSeed({
    prev: b.prev,
    lockset: b.lockset,
    round_id: b.round_id || b.round,
  });
  const nodeRow = sanitizeNodeId(b.node_id || b.node);
  if (!nodeRow.ok) return nodeRow;
  const node = nodeRow.node_id;
  if (!seed) {
    return verdict(true, "CAP7-PING", "yes", "ping accepted; supply prev+lockset (update proof) or round_id to land", {
      phase: "ping",
      continue: true,
      land: null,
      update: false,
      node_id: node,
      hardcoded_host: false,
      sites: cap7Roster(),
      app_worker: appWorker(),
    });
  }

  const site = landSite(seed);
  const update = m !== "GET" && m !== "HEAD" && !!(prev && lock);
  return verdict(
    true,
    "CAP7-LAND",
    "yes",
    update
      ? "landed on one Cap-7 site; that land is the update endpoint for this round"
      : "landed on one Cap-7 site for this shuffle round",
    {
      phase: "land",
      continue: false,
      land: site,
      update,
      update_endpoint: site.update_path,
      round_seed: seed,
      node_id: node,
      hardcoded_host: false,
      radio_phy: false,
      public_icann: false,
      typed_on_icann_dns: false,
      internet_reachable: false,
      internet_reaches: "az-domains",
      resolves_to_hub: !!site.resolves_to_hub,
      false_site: !!site.false_site,
      hub_duplication: !!site.hub_duplication,
      hosted_update: "LIVE",
      hosted_mcp: "LIVE",
      public_shuffle_land_exec: "LIVE",
      factory_honesty: "LIVE",
      anchored_by_live_nodes: true,
      is_live_door: false,
      channel_plane_is_vpn: false,
      second_door: false,
      app_worker: appWorker(),
    },
  );
}
