#!/usr/bin/env bash
# MirageGrid one-click install. Counted download via this project's Worker.
# Usage: curl -fsSL https://miragegrid-download-tracker.vibelock.workers.dev/install.sh | bash
set -euo pipefail

HOST="${MIRAGEGRID_HOME_HOST:-https://miragegrid-download-tracker.vibelock.workers.dev}"
ASSET="${MIRAGEGRID_HOME_ASSET:-miragegrid-0.2.0.tar.gz}"
WORKDIR="${MIRAGEGRID_HOME:-$HOME/miragegrid}"

mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "Downloading counted tarball from ${HOST}/download (User-Agent Mozilla/5.0)…"
curl -fsSL -A 'Mozilla/5.0' "${HOST}/download?asset=${ASSET}" -o "${ASSET}"

tar -xzf "${ASSET}"
DIR="$(find . -maxdepth 1 -type d -name 'miragegrid-*' | head -n 1)"
if [ -n "${DIR}" ]; then
  cd "${DIR}"
fi

python3 -m venv .venv
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .

echo
echo "MirageGrid is installed."
echo "Open the console:"
echo "  miragegrid ui"
echo "Then choose Open a circuit at http://127.0.0.1:8080/"
echo "Author: Aziel Eliab."
