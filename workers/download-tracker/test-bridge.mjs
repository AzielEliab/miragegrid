import {
  SEMANTIC_BRIDGE_SPEC,
  buildBridgeRegistry,
  cap7BridgeCite,
  hostedBridgeDocument,
  llmsTxt,
  aiTxt,
  robotsTxt,
  sitemapXml,
  refusePublicDnsClaim,
  refuseAzgIcannPublish,
  refuseHubResolution,
  refuseInventFirstFlagHttps,
} from "./src/bridge.js";

function assert(cond, label) {
  if (!cond) throw new Error(label);
}

const empty = hostedBridgeDocument();
assert(empty.spec === SEMANTIC_BRIDGE_SPEC, "spec");
assert(empty.public_icann === false, "public_icann false");
assert(empty.resolves_to_hub === false, "resolves_to_hub false");
assert(empty.code === "BRIDGE-EMPTY", "empty code " + empty.code);
assert(empty.names && Object.keys(empty.names).length === 0, "empty names");
assert(Array.isArray(empty.slots) && empty.slots.length === 0, "empty slots");
assert(empty.invented_first_flag_https === false, "no invented https");
assert(!("www.survivalnetwork.az" in empty.names), "first flag not invented");

const cite = cap7BridgeCite();
assert(cite.public_icann === false, "cite public_icann");
assert(cite.public_host_pair === 2, "pair 2");
assert(cite.suffix_order[0] === ".az", "suffix .az");
assert(cite.person["@id"] === "https://www.azieleliab.com/#aziel", "person @id");
assert(String(cite.cite).includes("/v1/mesh/az-generator"), "az-generator cite");

const tip = "a".repeat(64);
const claimed = buildBridgeRegistry([
  {
    name: "www.survivalnetwork.az",
    public_host: true,
    public_gateway_url: "https://pair.example.workers.dev/a",
    tip_sha256: tip,
    design_of: "https://www.azieleliab.com/",
  },
]);
assert(claimed.code === "BRIDGE-OK", "claimed code " + claimed.code);
assert(claimed.names["www.survivalnetwork.az"].status === "https-gateway", "gateway status");
assert(claimed.names["www.survivalnetwork.az"].resolves_to_hub === false, "claimed no hub resolve");
assert(claimed.names["www.survivalnetwork.az"].design_of === "https://www.azieleliab.com/", "design_of provenance");
assert(claimed.names["www.survivalnetwork.az"].icann === false, "row icann false");

assert(refusePublicDnsClaim().code === "BRIDGE-NO-PUBLIC-DNS", "dns refuse");
assert(refuseAzgIcannPublish().code === "BRIDGE-NO-ICANN-PUBLISH", "icann publish refuse");
assert(refuseHubResolution().code === "BRIDGE-NO-HUB-RESOLVE", "hub resolve refuse");
assert(refuseInventFirstFlagHttps().code === "BRIDGE-NO-INVENT-HTTPS", "invent refuse");
assert(buildBridgeRegistry([], { public_icann: true }).code === "BRIDGE-NO-PUBLIC-DNS", "registry public dns");
assert(buildBridgeRegistry([], { invent_first_flag: true }).code === "BRIDGE-NO-INVENT-HTTPS", "invent empty");
assert(
  buildBridgeRegistry([{ name: "x.az", public_host: true, public_gateway_url: "https://godlock.uk/" }]).code ===
    "BRIDGE-NO-HUB-RESOLVE",
  "gateway must not be a hub",
);

const llms = llmsTxt();
assert(llms.includes("SEMANTIC-BRIDGE-1.0"), "llms law");
assert(llms.includes("public_icann:false"), "llms public_icann");
assert(llms.includes("resolves_to_hub:false"), "llms resolves");
assert(!llms.includes("15:20"), "no 15:20");
const ai = aiTxt();
assert(ai.includes("public_icann:false"), "ai.txt");
const robots = robotsTxt();
assert(robots.includes("Allow: /"), "robots allow");
assert(robots.includes("GPTBot"), "GPTBot");
assert(robots.includes("ClaudeBot") || robots.includes("Claude-User"), "Claude");
assert(robots.includes("PerplexityBot"), "Perplexity");
assert(robots.includes("Google-Extended"), "Google-Extended");
assert(robots.includes("Content-Signal:"), "content-signal");
assert(robots.includes("ai-input=yes"), "ai-input");
assert(robots.includes("ai-train=yes"), "ai-train");
assert(robots.includes("search=yes"), "search");
const sitemap = sitemapXml();
assert(sitemap.includes("/llms.txt"), "sitemap llms");
assert(sitemap.includes("/v1/bridge"), "sitemap bridge");
assert(sitemap.includes("/v1/mesh/az-generator"), "sitemap az-generator");

console.log("bridge JSON empty-vs-claimed honesty ok; llms/ai/robots/sitemap stamped");
console.log("public_icann=false resolves_to_hub=false design_of=provenance-only");
