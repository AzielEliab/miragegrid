#!/usr/bin/env bash
# GitBaby / operator: create or replace Cloudflare Worker NAME=miragegrid.
# This is the named app Worker. It is NOT miragegrid-download-tracker.
# Deploying this Worker is what stops CF 1042 on
# https://miragegrid.vibelock.workers.dev
set -euo pipefail
cd "$(dirname "$0")"
# Stamped operator path. Do not hardcode a SHA.
# package.json "deploy" stays the named wrangler command CI asserts:
#   wrangler deploy --name miragegrid --config wrangler.jsonc
# This script is the GIT_SHA stamp: wrangler --var plus the bake.
# Workers Builds sets WORKERS_CI_COMMIT_SHA and wrangler build.command bakes it.
if [[ -z "${GIT_SHA:-}" ]]; then
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    GIT_SHA="$(git rev-parse HEAD)"
    export GIT_SHA
  fi
fi
node scripts/write-build-stamp.mjs --from-git
# wrangler.jsonc already sets name=miragegrid. Pass --name so the
# created Worker cannot silently become another product.
# build.command bakes the stamp again; GIT_SHA stays in the environment.
EXTRA=()
if [[ -n "${GIT_SHA:-}" ]]; then
  EXTRA+=(--var "GIT_SHA:${GIT_SHA}")
fi
npx wrangler deploy --name miragegrid --config wrangler.jsonc "${EXTRA[@]}"
echo "Deployed Worker name=miragegrid. Probe: curl -sS -A 'Mozilla/5.0' https://miragegrid.vibelock.workers.dev/v1/health"
