/**
 * Deploy tip for GET /v1/health.
 * git_sha prefers the runtime GIT_SHA var (wrangler deploy --var), same as
 * aziel-runtime. Otherwise the bundle bake from Workers Builds / CI.
 * version_id is env.CF_VERSION_METADATA.id at serve time. Never a constant.
 */

import { BAKED_GIT_SHA, BAKED_GIT_SHA_SOURCE } from "../build/build-stamp.generated.js";

const SHA_RE = /^[0-9a-f]{40}$/;
const VERSION_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
const TRACKS = new Set(["deploy_var", "workers_ci", "cf_pages", "github_sha", "git_head", "build_inject"]);

export function cleanSha(value) {
  const s = String(value ?? "").trim().toLowerCase();
  return SHA_RE.test(s) ? s : "";
}

export function cleanVersionId(value) {
  const s = String(value ?? "").trim().toLowerCase();
  return VERSION_RE.test(s) ? s : "";
}

export function deployStamp(env) {
  const e = env && typeof env === "object" ? env : {};
  const fromVar = cleanSha(e.GIT_SHA);
  const baked = cleanSha(BAKED_GIT_SHA);
  let git_sha = "";
  let git_sha_source = "unset";
  if (fromVar) {
    git_sha = fromVar;
    git_sha_source = "deploy_var";
  } else if (baked) {
    git_sha = baked;
    const src = String(BAKED_GIT_SHA_SOURCE || "").trim();
    git_sha_source = TRACKS.has(src) ? src : "build_inject";
  }
  const meta = e.CF_VERSION_METADATA;
  const version_id = cleanVersionId(meta && typeof meta === "object" ? meta.id : "");
  const tracks = Boolean(git_sha) && TRACKS.has(git_sha_source);
  return {
    tip: git_sha || null,
    git_sha: git_sha || null,
    git_sha_source,
    git_sha_tracks_deployed_tip: tracks,
    git_sha_note: git_sha
      ? "Deployed tip. GIT_SHA was set when this Worker was deployed, or the commit was baked at bundle time (Workers Builds WORKERS_CI_COMMIT_SHA / CI sha). That sha is the deploy stamp. It is not a claim that a newer git commit is already running."
      : "No deploy stamp on this bundle. Set GIT_SHA via wrangler deploy --var GIT_SHA:<40-hex> or bake WORKERS_CI_COMMIT_SHA at bundle time. Not a hardcoded tip.",
    version_id: version_id || null,
    version_id_source: version_id ? "cf_version_metadata" : "unset",
    version_id_note: "version_id is env.CF_VERSION_METADATA.id, read at serve time. It is not a baked constant.",
  };
}
