import worker from "./src/index.js";
import {
  SEMANTIC_BRIDGE_SPEC,
  CORPUS_HUB,
  buildBridgeRegistry,
  cap7BridgeCite,
  canonicalJson,
  designPackBody,
  hostedBridgeDocument,
  llmsTxt,
  aiTxt,
  robotsTxt,
  sitemapXml,
  sha256Hex,
  refusePublicDnsClaim,
  refuseAzgIcannPublish,
  refuseHubResolution,
  refuseInventFirstFlagHttps,
} from "./src/bridge.js";
import { execSync } from "node:child_process";

function assert(cond, label) {
  if (!cond) throw new Error(label);
}

const empty = await hostedBridgeDocument();
assert(empty.spec === SEMANTIC_BRIDGE_SPEC, "spec");
assert(empty.public_icann === false, "public_icann false");
assert(empty.resolves_to_hub === false, "resolves_to_hub false");
assert(empty.code === "BRIDGE-EMPTY", "empty code " + empty.code);
assert(empty.claimed === 0, "empty claims");
assert(Array.isArray(empty.slots) && empty.slots.length === 0, "empty slots");
assert(empty.invented_first_flag_https === false, "no invented https");
assert(!("www.survivalnetwork.az" in empty.names), "first flag not invented");
assert(empty.names["azcorpus.az"], "azcorpus listed");
assert(empty.names["azlibrary.az"], "azlibrary listed");
assert(empty.names["azcorpus.az"].status === "named-mesh-site", "azcorpus named");
assert(empty.names["azcorpus.az"].upload_auth === "none", "azcorpus upload none");
assert(empty.names["azlibrary.az"].upload_auth === "token", "azlibrary upload token");
assert(empty.names["azlibrary.az"].upload_plane === "plane-a", "azlibrary plane-a");
assert(empty.names["azcorpus.az"].download_open === true, "azcorpus download open");
assert(empty.names["azcorpus.az"].canonical_hub === CORPUS_HUB, "azcorpus hub");
assert(empty.names["azcorpus.az"].fifth_product === false, "not fifth product");
assert(empty.names["azcorpus.az"].public_icann === false, "azcorpus not icann");
assert(empty.fifth_product === false, "doc not fifth product");

const cite = cap7BridgeCite();
assert(cite.public_icann === false, "cite public_icann");
assert(cite.public_host_pair === 2, "pair 2");
assert(cite.preferred_public_pair[0] === "azcorpus", "prefer azcorpus");
assert(cite.suffix_order[0] === ".az", "suffix .az");
assert(cite.person["@id"] === "https://www.azieleliab.com/#aziel", "person @id");
assert(String(cite.cite).includes("/v1/mesh/az-generator"), "az-generator cite");

const tip = "a".repeat(64);
const claimed = await buildBridgeRegistry([
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
assert(claimed.names["azcorpus.az"].status === "named-mesh-site", "named site stays");

assert(refusePublicDnsClaim().code === "BRIDGE-NO-PUBLIC-DNS", "dns refuse");
assert(refuseAzgIcannPublish().code === "BRIDGE-NO-ICANN-PUBLISH", "icann publish refuse");
assert(refuseHubResolution().code === "BRIDGE-NO-HUB-RESOLVE", "hub resolve refuse");
assert(refuseInventFirstFlagHttps().code === "BRIDGE-NO-INVENT-HTTPS", "invent refuse");
assert((await buildBridgeRegistry([], { public_icann: true })).code === "BRIDGE-NO-PUBLIC-DNS", "registry public dns");
assert((await buildBridgeRegistry([], { invent_first_flag: true })).code === "BRIDGE-NO-INVENT-HTTPS", "invent empty");
assert(
  (await buildBridgeRegistry([{ name: "x.az", public_host: true, public_gateway_url: "https://godlock.uk/" }])).code ===
    "BRIDGE-NO-HUB-RESOLVE",
  "gateway must not be a hub",
);

const llms = llmsTxt();
assert(llms.includes("SEMANTIC-BRIDGE-1.0"), "llms law");
assert(llms.includes("public_icann:false"), "llms public_icann");
assert(llms.includes("azcorpus.az"), "llms azcorpus");
assert(llms.includes("azlibrary.az"), "llms azlibrary");
assert(llms.includes("/design-packs/azcorpus.json"), "llms pack");
assert(!llms.includes("15:20"), "no 15:20");
const ai = aiTxt();
assert(ai.includes("public_icann:false"), "ai.txt");
assert(ai.includes("azcorpus.upload_auth:none"), "ai corpus auth");
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
assert(sitemap.includes("/design-packs/azcorpus.json"), "sitemap pack");

const repoRoot = new URL("../../..", import.meta.url).pathname;
const py = execSync(
  "python3 -c \"from miragegrid.semantic_bridge import design_pack_sha256; print(design_pack_sha256('azcorpus')); print(design_pack_sha256('azlibrary'))\"",
  { cwd: repoRoot, env: { ...process.env, PYTHONPATH: repoRoot } },
)
  .toString()
  .trim()
  .split("\n");
const jsCorpus = await sha256Hex(canonicalJson(designPackBody("azcorpus")));
const jsLibrary = await sha256Hex(canonicalJson(designPackBody("azlibrary")));
assert(py[0] === jsCorpus, "azcorpus pack hash python==js");
assert(py[1] === jsLibrary, "azlibrary pack hash python==js");
assert(empty.names["azcorpus.az"].design_pack.sha256 === jsCorpus, "hosted pack sha");

async function hit(path) {
  const req = new Request("https://miragegrid-download-tracker.vibelock.workers.dev" + path, {
    method: "GET",
    headers: { "user-agent": "Mozilla/5.0", accept: "*/*" },
  });
  return worker.fetch(req, {});
}

const llmsRes = await hit("/llms.txt");
assert(llmsRes.status === 200, "llms HTTP " + llmsRes.status);
assert(String(llmsRes.headers.get("Content-Signal") || "").includes("ai-input=yes"), "llms Content-Signal");
const llmsBody = await llmsRes.text();
assert(llmsBody.includes("SEMANTIC-BRIDGE-1.0"), "llms body");
assert(llmsBody.includes("azcorpus.az"), "llms named sites");
assert(!llmsBody.includes("15:20"), "llms no 15:20 chrome");

const aiRes = await hit("/ai.txt");
assert(aiRes.status === 200, "ai.txt HTTP " + aiRes.status);

const bridgeRes = await hit("/v1/bridge");
assert(bridgeRes.status === 200, "bridge HTTP " + bridgeRes.status);
const bridgeDoc = await bridgeRes.json();
assert(bridgeDoc.public_icann === false, "live public_icann");
assert(bridgeDoc.resolves_to_hub === false, "live resolves_to_hub");
assert(bridgeDoc.claimed === 0, "live empty claims");
assert(Array.isArray(bridgeDoc.slots) && bridgeDoc.slots.length === 0, "live empty slots");
assert(!("www.survivalnetwork.az" in (bridgeDoc.names || {})), "live no invented first-flag https");
assert(bridgeDoc.names["azcorpus.az"].status === "named-mesh-site", "live azcorpus");
assert(bridgeDoc.names["azlibrary.az"].upload_auth === "token", "live azlibrary token");

const packRes = await hit("/design-packs/azcorpus.json");
assert(packRes.status === 200, "pack HTTP " + packRes.status);
assert(packRes.headers.get("X-Aziel-Design-Pack-Sha256") === jsCorpus, "pack sha header");
const packBody = await packRes.text();
assert((await sha256Hex(packBody)) === jsCorpus, "pack body hash-absolute");
assert(packBody.includes("azg-design-pack"), "pack kind");
assert(packBody.includes(CORPUS_HUB), "pack hub");

const libRes = await hit("/design-packs/azlibrary.json");
assert(libRes.status === 200, "library pack HTTP " + libRes.status);

const miss = await hit("/design-packs/unknown.json");
assert(miss.status === 404, "unknown pack SLOT");

const citeRes = await hit("/cite.json");
assert(citeRes.status === 200, "cite HTTP " + citeRes.status);
const citeDoc = await citeRes.json();
assert(citeDoc.cap7_bridge && citeDoc.cap7_bridge.public_icann === false, "cite cap7 public_icann");
assert(citeDoc.person && citeDoc.person["@id"] === "https://www.azieleliab.com/#aziel", "cite person");
assert(citeDoc.cap7_bridge.resolves_to_hub === false, "cite no hub resolve");
assert(citeDoc.cap7_bridge.named_mesh_sites.includes("azcorpus"), "cite named");

const robotsRes = await hit("/robots.txt");
assert(robotsRes.status === 200, "robots HTTP " + robotsRes.status);
const robotsBody = await robotsRes.text();
assert(robotsBody.includes("GPTBot"), "robots GPTBot");
assert(robotsBody.includes("Content-Signal:"), "robots signal");

const mapRes = await hit("/sitemap.xml");
assert(mapRes.status === 200, "sitemap HTTP " + mapRes.status);
const mapBody = await mapRes.text();
assert(mapBody.includes("/llms.txt"), "sitemap llms");
assert(mapBody.includes("/v1/mesh/az-generator"), "sitemap az-generator");
assert(mapBody.includes("/v1/bridge"), "sitemap bridge");
assert(mapBody.includes("/design-packs/azlibrary.json"), "sitemap library pack");

const azg = await hit("/v1/mesh/az-generator");
assert(azg.status === 200, "az-generator HTTP " + azg.status);
const azgDoc = await azg.json();
assert(azgDoc.public_icann === false, "azg cite public_icann");
assert(azgDoc.callable === false, "azg not callable");

console.log("bridge JSON empty-claims SLOT + named azcorpus/azlibrary designs");
console.log("public_icann=false resolves_to_hub=false fifth_product=false hash-absolute packs");
console.log("Worker fetch: llms/ai/bridge/cite/packs/robots/sitemap/az-generator all 200");
