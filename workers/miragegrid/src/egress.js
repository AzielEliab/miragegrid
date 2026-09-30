/**
 * MG-EGRESS-1.0 — honest geo / sticky / egress surface.
 * anyIP-style questions land here. No residential pool is live.
 * Sticky mesh-node labels are deterministic. Sticky public IPs are not.
 * AZVPN stays a separate product. Author: Aziel Eliab only.
 */
import { FRAGGATE_CAP7_STUBS } from "../../download-tracker/src/mesh.js";

export const EGRESS_SPEC = "MG-EGRESS-1.0";
export const IDENTITY = "Aziel Eliab";
export const POOL_SIZE = 25;
export const STICKY_PREFIX = "mg-sticky-v1|";
export const STICKY_VECTOR = Object.freeze({
  sticky_key: "booth-1",
  sha256: "97f92cd52d11c560baf28f1e6b93cd6d996a3b2aa5d5a33a0335dfe10af62490",
  index: 20,
  node_id: "node-21",
});

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
const ROTATE_KEYS = Object.freeze([
  "rotate",
  "rotation",
  "egress",
  "egress_ip",
  "exit_ip",
  "proxy",
  "socks",
  "socks5",
  "residential",
  "anyip",
  "new_ip",
]);
const VPN_KEYS = Object.freeze(["vpn", "vpn_hop", "tunnel", "hop", "hosted_vpn"]);
const STICKY_KEYS = Object.freeze([
  "sticky",
  "sticky_session",
  "sticky_key",
  "sticky_ip",
  "session_ttl",
  "ttl",
  "ttl_seconds",
  "duration",
]);
const TTL_KEYS = Object.freeze(["session_ttl", "ttl", "ttl_seconds", "duration"]);
const PAINT_KEYS = Object.freeze(["endpoints", "endpoint"]);
const FALSE_WORDS = new Set(["false", "0", "no", "off"]);
const SESSION_RE = /^[A-Za-z0-9._-]{1,80}$/;

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

export function assignLiveStamps() {
  return {
    geo_applied: false,
    sticky_ip: false,
    sticky_mesh_node: false,
    egress_ip: null,
    residential: false,
    ip_rotated: false,
    vpn_hosted_live: false,
    azvpn_separate: true,
    anonymity_network: false,
    packet_forwarding: false,
  };
}

export function honestyStamps() {
  return {
    spec: EGRESS_SPEC,
    author: IDENTITY,
    identity: IDENTITY,
    residential: false,
    egress_ip: null,
    geo_applied: false,
    sticky_ip: false,
    ip_rotated: false,
    vpn_hosted_live: false,
    packet_forwarding: false,
    anonymity_network: false,
    azvpn_separate: true,
    azvpn_merged: false,
    fraggate_stub_ops: FRAGGATE_CAP7_STUBS.slice(),
    fulfilled: false,
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

export function egressCite() {
  return {
    ok: true,
    code: "MG-EGRESS-CITE",
    verdict: "yes",
    yes: true,
    message: "Cite only. Geo targeting, sticky public IPs, and egress IP rotation are not live. Mesh-node stickiness is a separate deterministic label, not an IP.",
    ...honestyStamps(),
    fulfilled: false,
    cite: true,
    live: {
      assign: "POST /v1/assign — short-lived mesh node label (node-01..node-25) and a receipt. Not an egress IP.",
      sticky_mesh_node: "POST /v1/session/sticky — same sticky_key, same mesh node label. Not a sticky IP. No TTL store.",
      cap7: "Cap-7 factory cite/shuffle. Not ICANN .az publish.",
    },
    refuse_until_ready: {
      geo: "POST /v1/egress/geo — MG-GEO-NOT-READY. No country, city, or ASN pool.",
      sticky_ip: "POST /v1/egress/sticky — MG-STICKY-IP-NOT-READY. No sticky public address.",
      ip_rotation: "POST /v1/egress/rotate — MG-EGRESS-IP-NOT-READY. No egress address to rotate.",
      ttl: "MG-STICKY-TTL-NOT-READY. No durable session store, so a TTL would be theater.",
      painted_endpoints: "MG-NO-EGRESS-PAINT. Callers cannot write listen addresses onto the pool.",
    },
    not: [
      "residential IP network",
      "anonymity network",
      "hosted packet VPN",
      "AZVPN (separate Softwares product)",
    ],
    azvpn: { slug: "azvpn", merged: false, note: "AZVPN is the HTTPS/WS concentrator. MirageGrid does not open it." },
    vector: STICKY_VECTOR,
  };
}

export function geoRefuse(body) {
  const fields = asObject(body);
  return verdict(false, "MG-GEO-NOT-READY", 403, "No geo pool is live. Country, city, region, and ASN are not applied. No exit address is selected.", {
    requested: requested(fields, GEO_KEYS),
    pool: null,
  });
}

export function rotateRefuse(body) {
  const fields = asObject(body);
  return verdict(false, "MG-EGRESS-IP-NOT-READY", 403, "No egress IP pool is live. Nothing rotated. A new mesh label is POST /v1/assign, and that label is not an IP.", {
    requested: requested(fields, ROTATE_KEYS),
    mesh_label_rotation: "POST /v1/assign",
    mesh_label_is_ip: false,
  });
}

export function stickyIpRefuse(body) {
  const fields = asObject(body);
  return verdict(false, "MG-STICKY-IP-NOT-READY", 403, "No sticky public IP is live. Mesh-node stickiness is POST /v1/session/sticky and is not an address.", {
    requested: requested(fields, STICKY_KEYS),
    mesh_node_stick: "POST /v1/session/sticky",
  });
}

export function stickyTtlRefuse(body) {
  const fields = asObject(body);
  return verdict(false, "MG-STICKY-TTL-NOT-READY", 403, "No session store is live, so a TTL cannot be enforced. Refusing rather than ignoring the expiry.", {
    requested: requested(fields, TTL_KEYS),
    ttl_enforced: false,
  });
}

export function vpnRefuse(body) {
  const fields = asObject(body);
  return verdict(false, "MG-NOT-VPN", 403, "Hosted MirageGrid is not a VPN, not a tunnel, and not an anonymity network. FragGate vpn-hop, hop, tunnel, mesh, geo-target, session-stick, and egress-rotate stay stub. AZVPN is separate.", {
    requested: requested(fields, VPN_KEYS),
  });
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
  const vpn = asked(fields, VPN_KEYS);
  if (vpn.length) return vpnRefuse(fields);
  const geo = asked(fields, GEO_KEYS);
  if (geo.length) return geoRefuse(fields);
  const rotate = asked(fields, ROTATE_KEYS);
  if (rotate.length) return rotateRefuse(fields);
  const sticky = asked(fields, STICKY_KEYS);
  if (sticky.length) return stickyIpRefuse(fields);
  const paint = asked(fields, PAINT_KEYS);
  if (paint.length) return paintRefuse(fields);
  if (fields.hops != null && (!Number.isInteger(fields.hops) || fields.hops < 1 || fields.hops > POOL_SIZE)) {
    return verdict(false, "MG-BAD-HOPS", 400, "hops must be an integer 1..25", { hops: fields.hops });
  }
  if (fields.session_id != null && fields.session_id !== "") {
    if (typeof fields.session_id !== "string" || !SESSION_RE.test(fields.session_id)) {
      return verdict(false, "MG-BAD-SESSION-ID", 400, "session_id must be 1–80 [A-Za-z0-9._-]", {});
    }
  }
  return null;
}

export function prepareSticky(body) {
  const fields = asObject(body);
  const vpn = asked(fields, VPN_KEYS);
  if (vpn.length) return vpnRefuse(fields);
  const geo = asked(fields, GEO_KEYS);
  if (geo.length) return geoRefuse(fields);
  const rotate = asked(fields, ROTATE_KEYS);
  if (rotate.length) return rotateRefuse(fields);
  if (present(fields.sticky_ip)) return stickyIpRefuse(fields);
  const ttl = asked(fields, TTL_KEYS);
  if (ttl.length) return stickyTtlRefuse(fields);
  const paint = asked(fields, PAINT_KEYS);
  if (paint.length) return paintRefuse(fields);
  const key = String(fields.sticky_key || fields.session_key || "").trim();
  if (!key) {
    return verdict(false, "MG-STICKY-NEED-KEY", 400, "sticky_key is required. It selects a mesh node label, not an IP.", {});
  }
  if (!SESSION_RE.test(key)) {
    return verdict(false, "MG-BAD-SESSION-ID", 400, "sticky_key must be 1–80 [A-Za-z0-9._-]", {});
  }
  return { sticky: true, sticky_key: key };
}

export function routeEgress(method, path, body) {
  const m = String(method || "GET").toUpperCase();
  const p = String(path || "");
  if (p === "/v1/egress") {
    if (m === "GET" || m === "HEAD") return { status: 200, body: egressCite() };
    return verdict(false, "MG-EGRESS-CITE", 405, "GET cites the egress surface. POST a specific refuse door or /v1/session/sticky.", {});
  }
  if (p === "/v1/egress/geo") return geoRefuse(body);
  if (p === "/v1/egress/rotate") return rotateRefuse(body);
  if (p === "/v1/egress/sticky") return stickyIpRefuse(body);
  if (p === "/v1/session") {
    if (m === "GET" || m === "HEAD") {
      return {
        status: 200,
        body: {
          ...egressCite(),
          code: "MG-SESSION-CITE",
          message: "Session cite. Assign is a fresh mesh label. Sticky mesh labels are POST /v1/session/sticky. Sticky IPs refuse.",
        },
      };
    }
    return verdict(false, "MG-SESSION-CITE", 405, "GET cites sessions. POST /v1/assign or POST /v1/session/sticky.", {});
  }
  if (p === "/v1/session/sticky") {
    if (m !== "POST") {
      return verdict(false, "MG-STICKY-NEED-KEY", 403, "GET does not stick a session. POST sticky_key. No TTL and no IP.", {});
    }
    return prepareSticky(body);
  }
  return null;
}
