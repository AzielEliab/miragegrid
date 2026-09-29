/**
 * SIDENET-P2 — Cap-7 mesh DNS side-net.
 * L0 public path stays unchanged. This module only serves /v1/sidenet.
 * public_icann false. AZ Generator is not callable. Exactly 2 public
 * browser gateways (azgrid, azbooth). Other mesh names need an AZNet
 * pairing token and an azbrowser flag. This Worker does not verify that
 * token at AZNet and does not host payloads. Softwares stay frozen.
 * Author: Aziel Eliab only.
 */

import { FACTORY_LABELS, IDENTITY } from "./cap7.js";
import { refuseCallGenerator } from "../../download-tracker/src/mesh.js";

export const SIDENET_SPEC = "SIDENET-P2";
export const PUBLIC_BROWSER_GATEWAYS = Object.freeze(["azgrid", "azbooth"]);
const ACCESS = new Set(["aznet", "azbrowser"]);
const BROWSERS = new Set(["browser", "https", "public", "standard-browser", "internet-browser"]);
const BOOL_WORDS = new Set(["true", "false", "1", "0", "yes", "no", "on", "off"]);
const HUBS = new Set([
  "azieleliab.com",
  "www.azieleliab.com",
  "azielcorpuslibrary.net",
  "www.azielcorpuslibrary.net",
  "godlock.uk",
  "www.godlock.uk",
  "hedidntjump.com",
  "www.hedidntjump.com",
]);
const ICANN = [".com", ".net", ".org", ".uk", ".io", ".dev", ".app", ".info", ".co"];

function stamp(out) {
  return {
    ...out,
    layer: "P2",
    spec: SIDENET_SPEC,
    l0_public_path_changed: false,
    public_icann: false,
    softwares_tab: false,
    softwares_frozen: true,
    pairing_is_tunnel: false,
    second_door: false,
    callable: false,
    author: IDENTITY,
    identity: IDENTITY,
  };
}

function verdict(ok, code, verdictName, message, extra) {
  return stamp({
    ok: !!ok,
    code,
    verdict: verdictName,
    yes: verdictName === "yes",
    message,
    ...(extra || {}),
  });
}

export function sidenetDict() {
  return {
    ok: true,
    code: "SIDENET-CITE",
    verdict: "yes",
    yes: true,
    spec: SIDENET_SPEC,
    layer: "P2",
    author: IDENTITY,
    identity: IDENTITY,
    l0_public_path_changed: false,
    l0: {
      changed: false,
      plane: "public-path",
      internet_reaches: "az-domains",
      az_domains_public_icann: true,
      note: "AZ-domain doors and existing public routes stay as they are.",
    },
    p2: {
      plane: "sidenet",
      public_icann: false,
      dns_factory: "cap-7-mesh-authoritative",
      callable: false,
      exit: "node-gate-front",
      public_browser_gateways: PUBLIC_BROWSER_GATEWAYS.slice(),
      public_host_pair: 2,
    },
    public_icann: false,
    dns_factory: "cap-7-mesh-authoritative",
    callable: false,
    lives: "deep-node",
    exit: "node-gate-front",
    public_browser_gateways: PUBLIC_BROWSER_GATEWAYS.slice(),
    public_host_pair: 2,
    cap: 7,
    access: {
      aznet: true,
      azbrowser: true,
      merge: false,
      pairing_only: true,
      pairing_is_tunnel: false,
      pair_token_and_azbrowser_flag: true,
      pair_verified_at_aznet: false,
      this_surface_verifies_aznet_token: false,
      hosts_payloads: false,
    },
    node_gate_actions: ["claim", "flag", "plant", "restore"],
    hosted_node_gate_exec: false,
    softwares_tab: false,
    softwares_frozen: true,
    new_product: false,
    fifth_product: false,
    pairing_is_tunnel: false,
    second_door: false,
    radio_phy: false,
    aznet_payload_host: false,
    note: "P2 side-net. Cap-7 mesh DNS factory, not ICANN. Exactly 2 public browser gateways (azgrid, azbooth). Other mesh names need an AZNet pairing token and an azbrowser flag. This surface does not verify that token at AZNet. L0 public path is unchanged.",
  };
}

function hostOf(name) {
  return String(name || "").trim().toLowerCase().split("/")[0].replace(/\.$/, "");
}

export function factoryLabel(name) {
  let host = hostOf(name);
  if (host.endsWith(".az")) host = host.slice(0, -3);
  return FACTORY_LABELS.includes(host) ? host : null;
}

function pairToken(body) {
  const raw = body.pair_token ?? body.pairing_token ?? body.token;
  const text = String(raw || "").trim();
  if (BOOL_WORDS.has(text.toLowerCase())) return "";
  return text;
}

function azbrowserFlag(body) {
  return ["azbrowser_flag", "flag", "pair_peer"].some((key) => String(body[key] || "").trim().toLowerCase() === "azbrowser");
}

function clientOf(body) {
  return String(body.client || "").trim().toLowerCase().replace(/_/g, "-");
}

export function sidenetAccess(body) {
  const fields = body && typeof body === "object" ? body : {};
  if (fields.softwares_tab || fields.new_product || fields.fifth_product) {
    return verdict(false, "SIDENET-SOFTWARE-FROZEN", "refuse", "Softwares stay frozen; sidenet is a MirageGrid subsystem, not a new product", {
      new_product: false,
      fifth_product: false,
      merge: false,
    });
  }
  if (fields.public_icann || fields.cctld_takeover || fields.registrar) {
    return verdict(false, "AZG-NOT-PUBLIC-REGISTRAR", "refuse", "mesh DNS factory is not a public ICANN registrar", {
      registrar: false,
      cctld_takeover: false,
      dns_factory: "cap-7-mesh-authoritative",
    });
  }
  if (fields.merge || fields.merge_products) {
    return verdict(false, "AZG-NO-MERGE-PRODUCTS", "refuse", "AZNet and AZBrowser stay separate Softwares products; functional pairing only", {
      merge: false,
      aznet: "aznet",
      azbrowser: "azbrowser",
    });
  }
  if (fields.hosts_payloads || fields.aznet_payload_host || fields.payload_host) {
    return verdict(false, "SIDENET-NO-PAYLOAD-HOST", "refuse", "AZNet pairing does not host payloads", {
      hosts_payloads: false,
      aznet_payload_host: false,
    });
  }
  if (fields.pairing_is_tunnel || fields.channel_plane_is_vpn || fields.hosted_vpn || fields.second_door || fields.open_proxy) {
    return verdict(false, "CAP7-NO-VPN-LIE", "refuse", "pairing is not a tunnel; the channel plane is not a VPN; FragGate stays the only door", {
      channel_plane_is_vpn: false,
      hosted_vpn: false,
      open_proxy: false,
      hosts_payloads: false,
    });
  }
  if (fields.pair_verified_at_aznet || fields.aznet_verified) {
    return verdict(false, "SIDENET-NO-VERIFIED-LIE", "refuse", "this surface does not verify pairing tokens at AZNet; do not stamp verification", {
      pair_verified_at_aznet: false,
      this_surface_verifies_aznet_token: false,
      pair_check: "refused-unverified-claim",
    });
  }
  if (fields.naked_dns) {
    return verdict(false, "AZG-NO-NAKED-DNS", "refuse", "resolution/browsing goes through AZNet + AZBrowser; not a naked public DNS story", {
      naked_public_dns: false,
    });
  }

  const host = hostOf(fields.name || fields.label);
  if (HUBS.has(host)) {
    return verdict(false, "MGS-NOT-NODE-GATE", "refuse", "official hubs stay on the L0 public path; they are not sidenet Node Gate", {
      name: host,
    });
  }
  const label = factoryLabel(host);
  if (!label) {
    if (!host) {
      return verdict(false, "CAP7-UNKNOWN", "refuse", "unknown Cap-7 name; mesh DNS is not a public resolver", {
        name: host,
        dns_factory: "cap-7-mesh-authoritative",
      });
    }
    const tld = ICANN.find((suffix) => host.endsWith(suffix));
    if (tld) {
      return verdict(false, "AZG-TLD", "refuse", "AZ Generator claims the active honest suffix (.az → .aziel → pivot) — not ICANN TLDs", {
        name: host,
        tld,
      });
    }
    if (!host.endsWith(".az") && !host.endsWith(".aziel")) {
      return verdict(false, "CAP7-UNKNOWN", "refuse", "unknown Cap-7 name; mesh DNS is not a public resolver", {
        name: host,
        dns_factory: "cap-7-mesh-authoritative",
      });
    }
  }

  const client = clientOf(fields);
  const gateway = PUBLIC_BROWSER_GATEWAYS.includes(label);
  if (BROWSERS.has(client)) {
    if (gateway) {
      return verdict(true, "AZG-ACCESS-PUBLIC-GATEWAY", "yes", "one of exactly 2 Cap-7 public browser gateways; not an ICANN name", {
        name: host,
        label,
        client,
        public_browser_gateway: true,
        public_browser_gateways: PUBLIC_BROWSER_GATEWAYS.slice(),
        public_host_pair: 2,
        pair_required: false,
        internet_reachable: false,
        typed_on_icann_dns: false,
        registrar: false,
      });
    }
    return verdict(false, "AZG-PUBLIC-PAIR", "refuse", "standard browsers reach exactly 2 Cap-7 public browser gateways; this name stays on the sidenet", {
      name: host,
      label,
      client,
      public_browser_gateway: false,
      public_browser_gateways: PUBLIC_BROWSER_GATEWAYS.slice(),
      public_host_pair: 2,
      access: ["azbrowser", "aznet"],
    });
  }
  if (!ACCESS.has(client)) {
    return verdict(false, "AZG-NO-NAKED-DNS", "refuse", "resolution/browsing goes through AZNet + AZBrowser; not a naked public DNS story", {
      naked_public_dns: false,
      client,
    });
  }
  const token = pairToken(fields);
  const flag = azbrowserFlag(fields);
  const missing = [];
  if (!token) missing.push("pair_token");
  if (!flag) missing.push("azbrowser_flag");
  if (missing.length) {
    return verdict(false, "SIDENET-NEED-PAIR", "refuse", "AZNet and AZBrowser pairing requires a pairing token and an azbrowser flag; both are required", {
      name: host,
      label,
      client,
      missing,
      merge: false,
      pair_verified_at_aznet: false,
      this_surface_verifies_aznet_token: false,
      hosts_payloads: false,
      aznet_payload_host: false,
    });
  }
  return verdict(true, "SIDENET-PAIR-OK", "yes", "pairing token and azbrowser flag are both present; this surface did not verify the token at AZNet", {
    name: host,
    label,
    client,
    public_browser_gateway: gateway,
    merge: false,
    pair_check: "token-and-flag-present",
    pair_verified_at_aznet: false,
    this_surface_verifies_aznet_token: false,
    hosts_payloads: false,
    aznet_payload_host: false,
    access: ["azbrowser", "aznet"],
    door: "fraggate",
  });
}

export function sidenetNodeGate(action, body) {
  const fields = body && typeof body === "object" ? body : {};
  const act = String(action || "").trim().toLowerCase().replace(/_/g, "-");
  if (fields.public_icann || fields.registrar || fields.cctld_takeover) {
    return verdict(false, "AZG-NOT-PUBLIC-REGISTRAR", "refuse", "mesh DNS factory is not a public ICANN registrar", {
      action: act,
      registrar: false,
      hosted_exec: false,
    });
  }
  if (!["claim", "plant", "flag", "restore"].includes(act)) {
    return verdict(false, "SIDENET-NODE-GATE", "refuse", "Node Gate actions are claim, plant, flag, and restore", {
      action: act,
      hosted_exec: false,
    });
  }
  if (fields.fake_flag || fields.fakeFlag) {
    return verdict(false, "NO-FAN-FALSIFY", "refuse", "do not fake the flag", {
      action: act,
      phrase: "No falsification. No ambiguity. No misleading.",
      hosted_exec: false,
    });
  }
  if (act === "claim" || act === "restore") {
    const refused = refuseCallGenerator("sidenet/" + act);
    return stamp({ ...refused, action: act, hosted_exec: false, public_icann: false });
  }
  return verdict(false, "MGS-NO-HOSTED-PLANT", "refuse", "flag and plant stay on the local Node Gate; the hosted Worker does not plant a name", {
    action: act,
    hosted_plant: false,
    hosted_exec: false,
    this_worker_is_node_gate: false,
    exit: "node-gate-front",
  });
}

export function handleSidenet(method, path, body) {
  const m = String(method || "GET").toUpperCase();
  if (path === "/v1/sidenet") {
    if (m === "GET" || m === "HEAD") return { status: 200, body: sidenetDict() };
    return { status: 405, body: verdict(false, "SIDENET-METHOD", "refuse", "GET cites sidenet; POST does not run the generator", { hosted_exec: false }) };
  }
  if (path === "/v1/sidenet/access") {
    if (m === "GET" || m === "HEAD") {
      return {
        status: 403,
        body: verdict(false, "MESH-GET-NO-ENABLE", "refuse", "GET never enables radios or plants mesh claims", {
          enabled: false,
          claim_plant: false,
          path,
        }),
      };
    }
    if (m !== "POST") return { status: 405, body: verdict(false, "SIDENET-METHOD", "refuse", "POST the pairing check", {}) };
    const out = sidenetAccess(body);
    return { status: out.ok ? 200 : 403, body: out };
  }
  const gate = path.match(/^\/v1\/sidenet\/(claim|plant|flag|restore)$/);
  if (gate) {
    if (m === "GET" || m === "HEAD") {
      return {
        status: 403,
        body: verdict(false, "MESH-GET-NO-ENABLE", "refuse", "GET never enables radios or plants mesh claims", {
          enabled: false,
          claim_plant: false,
          action: gate[1],
          path,
        }),
      };
    }
    if (m !== "POST") return { status: 405, body: verdict(false, "SIDENET-METHOD", "refuse", "hosted Node Gate does not execute", { action: gate[1] }) };
    const out = sidenetNodeGate(gate[1], body);
    return { status: 403, body: out };
  }
  if (path === "/v1/sidenet/call-generator" || path === "/v1/sidenet/run-generator") {
    const refused = refuseCallGenerator(path);
    return { status: 403, body: stamp({ ...refused, hosted_exec: false, public_icann: false }) };
  }
  return null;
}
