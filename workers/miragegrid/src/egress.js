/**
 * MG-EGRESS-1.0 — Cap-7 control plane.
 * geo-target, session-stick, and egress-rotate are LIVE as factory
 * metadata: a region label, a sticky mesh node + Cap-7 land, and a
 * land rotation among the seven sites.
 * Not a public egress IP. Not a Cloudflare geo-exit pool.
 * Not a VPN. Not AZVPN. Not an ICANN registrar.
 * Author: Aziel Eliab only.
 */
import { FRAGGATE_CAP7_STUBS } from "../../download-tracker/src/mesh.js";

import { CAP7_FACTORY_SITES, FACTORY_LABELS, siteRecord } from "./cap7.js";

export const EGRESS_SPEC = "MG-EGRESS-1.0";
export const IDENTITY = "Aziel Eliab";
export const POOL_SIZE = 25;
export const CAP_7 = 7;
export const STICKY_PREFIX = "mg-sticky-v1|";
export const STICKY_VECTOR = Object.freeze({
  sticky_key: "booth-1",
  sha256: "97f92cd52d11c560baf28f1e6b93cd6d996a3b2aa5d5a33a0335dfe10af62490",
  index: 20,
  node_id: "node-21",
});
export const TTL_MIN = 60;
export const TTL_MAX = 86400;
export const FRAGGATE_STUB_OPS = FRAGGATE_CAP7_STUBS;
export const WORKER_LIVE_OPS = Object.freeze(["geo-target", "session-stick", "egress-rotate"]);

const GEO_KEYS = Object.freeze([
  "geo",
  "country",
  "country_code",
  "region",
  "city",
  "state",
  "asn",
  "isp",
  "zip",
  "postal",
]);
const IP_EXIT_KEYS = Object.freeze([
  "egress_ip",
  "exit_ip",
  "new_ip",
  "proxy",
  "socks",
  "socks5",
  "residential",
  "anyip",
  "cf_geo",
  "cf_geo_exit",
  "geo_exit",
  "wireguard",
  "openvpn",
]);
const VPN_KEYS = Object.freeze(["vpn", "vpn_hop", "tunnel", "hop", "hosted_vpn"]);
const TTL_KEYS = Object.freeze(["session_ttl", "ttl", "ttl_seconds", "duration"]);
const PAINT_KEYS = Object.freeze(["endpoints", "endpoint"]);
const FALSE_WORDS = new Set(["false", "0", "no", "off"]);
const SESSION_RE = /^[A-Za-z0-9._-]{1,80}$/;

const IP_EXIT_MESSAGE =
  "MirageGrid does not host a public egress IP, a sticky public address, or a Cloudflare geo-exit pool. Cap-7 geo-target is a region label, session-stick is a mesh node plus a factory land, and egress-rotate moves that land among the seven sites. IP exit stays on AZVPN or a future binding this Worker does not claim.";

function asObject(body) {
  if (!body || typeof body !== "object" || Array.isArray(body)) return {};
  return body;
}

function present(value) {
  if (value == null || value === false || value === "") return false;
  if (typeof value === "string" && FALSE_WORDS.has(value.trim().toLowerCase())) return false;
  if (typeof value === "number" && value === 0) return false;
  if (Array.isArray(value)) return value.length > 0;
  if (typeof value === "object") return Object.keys(value).length > 0;
  return true;
}

function asked(body, keys) {
  return keys.filter((key) => present(body[key]));
}

function requested(body, keys) {
  const out = {};
  for (const key of keys) {
    if (present(body[key])) out[key] = body[key];
  }
  return out;
}

export async function sha256Hex(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(String(text)));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function modHex(hex, n) {
  return Number(BigInt("0x" + hex) % BigInt(n));
}

export function honestyStamps() {
  return {
    spec: EGRESS_SPEC,
    author: IDENTITY,
    identity: IDENTITY,
    residential: false,
    egress_ip: null,
    public_egress_ip: false,
    sticky_public_ip: false,
    sticky_ip: false,
    cf_geo_exit_pool: false,
    geo_pool: false,
    ip_exit: false,
    ip_rotated: false,
    vpn_hosted_live: false,
    packet_forwarding: false,
    hosted_vpn: false,
    anonymity_network: false,
    azvpn_separate: true,
    azvpn_merged: false,
    wireguard: false,
    openvpn: false,
    l3_exit: false,
    public_icann: false,
    public_icann_registrar: false,
    typed_on_icann_dns: false,
    fraggate_stub_ops: FRAGGATE_STUB_OPS.slice(),
    worker_live_ops: WORKER_LIVE_OPS.slice(),
    softwares_catalog_live: true,
  };
}

export function noIpFlags() {
  return {
    ip_exit: false,
    public_egress_ip: false,
    sticky_public_ip: false,
    sticky_ip: false,
    cf_geo_exit_pool: false,
    geo_pool: false,
    egress_ip: null,
    residential: false,
    ip_rotated: false,
    packet_forwarding: false,
    hosted_vpn: false,
    vpn_hosted_live: false,
    anonymity_network: false,
    azvpn: false,
    wireguard: false,
    openvpn: false,
    l3_exit: false,
    public_icann: false,
    public_icann_registrar: false,
  };
}

function verdict(ok, code, status, message, extra) {
  return {
    status,
    body: {
      ok: !!ok,
      code,
      verdict: ok ? "yes" : "refuse",
      yes: !!ok,
      message,
      ...honestyStamps(),
      ...(extra || {}),
    },
  };
}

export function regionLabel(body) {
  const fields = asObject(body);
  const label = {};
  for (const key of GEO_KEYS) {
    const value = fields[key];
    if (!present(value) || typeof value === "object") continue;
    label[key] = String(value).trim().slice(0, 80);
  }
  return Object.keys(label).length ? label : null;
}

export function regionStamp(body) {
  const region = regionLabel(body);
  if (!region) {
    return {
      geo_applied: false,
      geo_means: null,
      region_label: null,
      ...noIpFlags(),
    };
  }
  return {
    geo_applied: true,
    geo_means: "region-label",
    region_label: region,
    ...noIpFlags(),
    note_geo: "Region label is Cap-7 metadata on this land. It does not select an IP exit or a Cloudflare colo.",
  };
}

function firstTtl(fields) {
  for (const key of TTL_KEYS) {
    if (fields[key] != null && fields[key] !== "" && fields[key] !== false) return fields[key];
  }
  return null;
}

export function normalizeTtl(body) {
  const raw = firstTtl(asObject(body));
  if (raw == null) return { ttl_seconds: null };
  const n = typeof raw === "number" ? raw : Number(String(raw).trim());
  if (!Number.isInteger(n) || n < TTL_MIN || n > TTL_MAX) {
    return {
      error: verdict(
        false,
        "MG-BAD-TTL",
        400,
        "ttl_seconds must be an integer 60..86400. The stick is a time-bucket hash of the key, not a stored public IP.",
        { ttl_enforced: false, durable_store: false },
      ),
    };
  }
  return { ttl_seconds: n };
}

function ipExitRefuse(fields) {
  const hits = asked(fields, IP_EXIT_KEYS);
  const stickyAddr = typeof fields.sticky_ip === "string" || typeof fields.sticky_ip === "number";
  if (!hits.length && !stickyAddr) return null;
  return verdict(false, "MG-NO-IP-EXIT", 403, IP_EXIT_MESSAGE, {
    requested: { ...requested(fields, IP_EXIT_KEYS), ...(stickyAddr ? { sticky_ip: fields.sticky_ip } : {}) },
    public_ip_applied: false,
    control_plane: "cap7",
  });
}

export function assignLiveStamps() {
  return {
    geo_applied: false,
    sticky_ip: false,
    sticky_public_ip: false,
    sticky_mesh_node: false,
    egress_ip: null,
    public_egress_ip: false,
    residential: false,
    ip_rotated: false,
    ip_exit: false,
    cf_geo_exit_pool: false,
    geo_pool: false,
    vpn_hosted_live: false,
    azvpn_separate: true,
    anonymity_network: false,
    packet_forwarding: false,
    hosted_vpn: false,
    wireguard: false,
    openvpn: false,
    l3_exit: false,
    public_icann: false,
  };
}

export function egressCite() {
  return {
    ok: true,
    code: "MG-EGRESS-CITE",
    verdict: "yes",
    yes: true,
    message:
      "Cap-7 control plane is LIVE. geo-target records a region label. session-stick binds a mesh node and a factory land for a TTL. egress-rotate moves that land among the seven sites. None of these allocate a public egress IP or a Cloudflare geo-exit pool.",
    ...honestyStamps(),
    cite: true,
    control_plane: "live",
    live: {
      geo_target: "POST /v1/egress/geo or POST /v1/geo-target — region label on a mesh node and a Cap-7 land. ip_exit false.",
      session_stick: "POST /v1/session/sticky or POST /v1/session-stick or POST /v1/egress/sticky — same sticky_key, same node id and Cap-7 site. TTL is a time-bucket hash. Not a public IP.",
      egress_rotate: "POST /v1/egress/rotate or POST /v1/egress-rotate — next Cap-7 factory land. Not packet egress.",
      assign: "POST /v1/assign — session circuit. A region label, sticky_key, or land rotate stamps the Cap-7 plane. Not an egress IP.",
    },
    not_hosted: {
      public_egress_ip: "MG-NO-IP-EXIT. No sticky public address and no Cloudflare geo-exit pool.",
      packet_hop: "FragGate vpn-hop, hop, tunnel, and mesh stay FG-STUB. They are not Cap-7 land hops.",
      painted_endpoints: "MG-NO-EGRESS-PAINT. Callers cannot write listen addresses onto the pool.",
    },
    not: [
      "residential IP network",
      "anonymity network",
      "hosted packet VPN",
      "Cloudflare geo-exit pool",
      "sticky public IP",
      "AZVPN (separate Softwares product)",
      "public ICANN registrar",
    ],
    azvpn: {
      slug: "azvpn",
      merged: false,
      note: "AZVPN is the HTTPS/WS concentrator. MirageGrid does not open it and does not claim its exit pool.",
    },
    sticky_ip_means:
      "On MirageGrid, the sticky path is a Cap-7 session/land stick: one mesh node id and one factory site for the key (and for a TTL window when ttl_seconds is set). sticky_public_ip stays false. A public egress address is not allocated.",
    vector: STICKY_VECTOR,
  };
}

export function vpnRefuse(body) {
  const fields = asObject(body);
  return verdict(
    false,
    "MG-NOT-VPN",
    403,
    "Hosted MirageGrid is not a VPN, not a tunnel, and not an anonymity network. FragGate vpn-hop, hop, tunnel, and mesh stay stub. AZVPN is separate. Cap-7 land hop is egress-rotate, not a packet hop.",
    { requested: requested(fields, VPN_KEYS) },
  );
}

export function paintRefuse(body) {
  const fields = asObject(body);
  return verdict(false, "MG-NO-EGRESS-PAINT", 403, "Listen addresses stay loopback defaults. A caller-supplied endpoint is not an egress IP.", {
    requested: requested(fields, PAINT_KEYS),
    listen_targets: "loopback-defaults",
    endpoints_applied: false,
  });
}

export function refusalForAssign(body) {
  const fields = asObject(body);
  if (asked(fields, VPN_KEYS).length) return vpnRefuse(fields);
  const ip = ipExitRefuse(fields);
  if (ip) return ip;
  if (asked(fields, PAINT_KEYS).length) return paintRefuse(fields);
  if (fields.hops != null && (!Number.isInteger(fields.hops) || fields.hops < 1 || fields.hops > POOL_SIZE)) {
    return verdict(false, "MG-BAD-HOPS", 400, "hops must be an integer 1..25", { hops: fields.hops });
  }
  if (fields.session_id != null && fields.session_id !== "") {
    if (typeof fields.session_id !== "string" || !SESSION_RE.test(fields.session_id)) {
      return verdict(false, "MG-BAD-SESSION-ID", 400, "session_id must be 1–80 [A-Za-z0-9._-]", {});
    }
  }
  const key = String(fields.sticky_key || fields.session_key || "").trim();
  if (key && !SESSION_RE.test(key)) {
    return verdict(false, "MG-BAD-SESSION-ID", 400, "sticky_key must be 1–80 [A-Za-z0-9._-]", {});
  }
  const ttl = normalizeTtl(fields);
  if (ttl.error) return ttl.error;
  if (ttl.ttl_seconds != null && !key) {
    return verdict(false, "MG-STICKY-NEED-KEY", 400, "ttl_seconds needs sticky_key. The TTL binds a mesh node and a Cap-7 land, not a public IP.", {});
  }
  return null;
}

export function prepareGeo(body) {
  const fields = asObject(body);
  if (asked(fields, VPN_KEYS).length) return vpnRefuse(fields);
  const ip = ipExitRefuse(fields);
  if (ip) return ip;
  if (asked(fields, PAINT_KEYS).length) return paintRefuse(fields);
  const region = regionLabel(fields);
  if (!region) {
    return verdict(
      false,
      "MG-GEO-NEED-LABEL",
      400,
      "A region label (country, region, or city) is required. It is metadata on the Cap-7 land, not an IP exit.",
      { geo_applied: false },
    );
  }
  return { geo: true, region_label: region };
}

export function prepareSticky(body) {
  const fields = asObject(body);
  if (asked(fields, VPN_KEYS).length) return vpnRefuse(fields);
  const ip = ipExitRefuse(fields);
  if (ip) return ip;
  if (asked(fields, PAINT_KEYS).length) return paintRefuse(fields);
  const ttl = normalizeTtl(fields);
  if (ttl.error) return ttl.error;
  const key = String(fields.sticky_key || fields.session_key || "").trim();
  if (!key) {
    return verdict(
      false,
      "MG-STICKY-NEED-KEY",
      400,
      "sticky_key is required. It binds a mesh node and a Cap-7 land. It does not allocate a public IP.",
      {},
    );
  }
  if (!SESSION_RE.test(key)) {
    return verdict(false, "MG-BAD-SESSION-ID", 400, "sticky_key must be 1–80 [A-Za-z0-9._-]", {});
  }
  return {
    sticky: true,
    sticky_key: key,
    ttl_seconds: ttl.ttl_seconds,
    region_label: regionLabel(fields),
    sticky_public_ip_requested: fields.sticky_ip === true,
  };
}

export async function stickBinding(stickyKey, ttlSeconds, nowMs = Date.now()) {
  let window = null;
  let expires_at = null;
  let material = STICKY_PREFIX + stickyKey;
  if (ttlSeconds != null) {
    window = Math.floor(nowMs / 1000 / ttlSeconds);
    expires_at = new Date((window + 1) * ttlSeconds * 1000).toISOString().replace(/\.\d{3}Z$/, "Z");
    material = STICKY_PREFIX + stickyKey + "|w" + window;
  }
  const digestHex = await sha256Hex(material);
  const node_index = modHex(digestHex, POOL_SIZE);
  const siteMaterial = "mg-cap7-stick-v1|" + stickyKey + (window == null ? "" : "|w" + window);
  const siteDigest = await sha256Hex(siteMaterial);
  const site_index = modHex(siteDigest, CAP_7);
  const site = siteRecord(CAP7_FACTORY_SITES[site_index]);
  return {
    node_index,
    node_id: "node-" + String(node_index + 1).padStart(2, "0"),
    land_label: site.label,
    site,
    ttl_seconds: ttlSeconds,
    window,
    expires_at,
    ttl_enforced: ttlSeconds != null,
    ttl_mechanism: ttlSeconds != null ? "time-bucket-hash" : "deterministic-hash",
    durable_store: false,
    stick_id: digestHex.slice(0, 32),
  };
}

export async function geoBinding(regionLabelValue) {
  const canonical = Object.keys(regionLabelValue).sort().map((key) => key + "=" + regionLabelValue[key]).join("|");
  const digestHex = await sha256Hex("mg-geo-label-v1|" + canonical);
  const node_index = modHex(digestHex, POOL_SIZE);
  const siteDigest = await sha256Hex("mg-geo-land-v1|" + canonical);
  const site_index = modHex(siteDigest, CAP_7);
  const site = siteRecord(CAP7_FACTORY_SITES[site_index]);
  return {
    node_index,
    node_id: "node-" + String(node_index + 1).padStart(2, "0"),
    land_label: site.label,
    site,
    canonical,
  };
}

export async function rotateNodeIndex(landLabel) {
  const digestHex = await sha256Hex("mg-cap7-rotate-node-v1|" + landLabel);
  return modHex(digestHex, POOL_SIZE);
}

export async function prepareRotate(body) {
  const fields = asObject(body);
  if (asked(fields, VPN_KEYS).length) return vpnRefuse(fields);
  const ip = ipExitRefuse(fields);
  if (ip) return ip;
  if (asked(fields, PAINT_KEYS).length) return paintRefuse(fields);
  const from = String(fields.from_label || fields.land_label || fields.prev_land || "").trim().toLowerCase();
  if (from && !FACTORY_LABELS.includes(from)) {
    return verdict(false, "CAP7-UNKNOWN", 400, "from_label is not one of the seven Cap-7 factory sites. Not an ICANN name.", {
      public_icann: false,
    });
  }
  let land_label;
  let mechanism;
  let previous = null;
  if (from) {
    land_label = FACTORY_LABELS[(FACTORY_LABELS.indexOf(from) + 1) % FACTORY_LABELS.length];
    mechanism = "roster-next";
    previous = from;
  } else {
    const seed = String(fields.round_id || fields.session_id || "cap7-rotate").trim();
    if (!seed || seed.length > 80) {
      return verdict(false, "MG-BAD-SESSION-ID", 400, "round_id or session_id must be 1–80 characters when used as a rotate seed.", {});
    }
    const digest = await sha256Hex("mg-cap7-rotate-v1|" + seed);
    land_label = FACTORY_LABELS[modHex(digest, CAP_7)];
    mechanism = "seed-hash";
  }
  const site = siteRecord(CAP7_FACTORY_SITES.find((row) => row.label === land_label));
  return {
    rotate: true,
    land_label,
    previous_land: previous,
    mechanism,
    site,
    region_label: regionLabel(fields),
  };
}

export async function routeEgress(method, path, body) {
  const m = String(method || "GET").toUpperCase();
  const p = String(path || "");
  if (p === "/v1/egress") {
    if (m === "GET" || m === "HEAD") return { status: 200, body: egressCite() };
    return verdict(false, "MG-EGRESS-CITE", 405, "GET cites the Cap-7 control plane. POST /v1/egress/geo, /v1/egress/sticky, or /v1/egress/rotate.", {});
  }
  if (p === "/v1/egress/geo" || p === "/v1/geo-target") {
    if (m !== "POST") return verdict(false, "MG-GEO-NEED-LABEL", 405, "POST a region label. GET does not target.", {});
    return prepareGeo(body);
  }
  if (p === "/v1/egress/rotate" || p === "/v1/egress-rotate") {
    if (m !== "POST") return verdict(false, "MG-EGRESS-ROTATE", 405, "POST rotates the Cap-7 land. GET does not rotate.", {});
    return prepareRotate(body);
  }
  if (p === "/v1/egress/sticky" || p === "/v1/session/sticky" || p === "/v1/session-stick") {
    if (m !== "POST") {
      return verdict(false, "MG-STICKY-NEED-KEY", 405, "POST sticky_key. The stick is a mesh node and a Cap-7 land, not a public IP.", {});
    }
    return prepareSticky(body);
  }
  if (p === "/v1/session") {
    if (m === "GET" || m === "HEAD") {
      return {
        status: 200,
        body: {
          ...egressCite(),
          code: "MG-SESSION-CITE",
          message: "Session cite. Assign is a fresh mesh label. POST /v1/session/sticky binds a node and a Cap-7 land. sticky_public_ip is false.",
        },
      };
    }
    return verdict(false, "MG-SESSION-CITE", 405, "GET cites sessions. POST /v1/assign or POST /v1/session/sticky.", {});
  }
  return null;
}
