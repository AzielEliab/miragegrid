#!/usr/bin/env bash
# GitBaby / operator: create or replace Cloudflare Worker NAME=miragegrid.
# This is the named app Worker. It is NOT miragegrid-download-tracker.
# Deploying this Worker is what stops CF 1042 on
# https://miragegrid.vibelock.workers.dev
set -euo pipefail
cd "$(dirname "$0")"
# wrangler.jsonc already sets name=miragegrid. Pass --name so the
# created Worker cannot silently become another product.
npx wrangler deploy --name miragegrid --config wrangler.jsonc
echo "Deployed Worker name=miragegrid. Probe: curl -sS -A 'Mozilla/5.0' https://miragegrid.vibelock.workers.dev/v1/health"
