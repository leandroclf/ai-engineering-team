#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
command -v python3 >/dev/null
command -v git >/dev/null
command -v docker >/dev/null
docker compose version >/dev/null
python3 -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install -r "$ROOT/requirements-validation.txt"
chmod +x "$ROOT/bin/ai-team"
mkdir -p "$HOME/.local/bin"
if [ -e "$HOME/.local/bin/ai-team" ] && [ "$(readlink -f "$HOME/.local/bin/ai-team")" != "$ROOT/bin/ai-team" ]; then
  echo 'Existing ai-team command found; preserve it and resolve the destination manually.' >&2
  exit 2
fi
ln -sfn "$ROOT/bin/ai-team" "$HOME/.local/bin/ai-team"
docker build -f "$ROOT/runtimes/Dockerfile" -t ai-eng-provider-cli:local "$ROOT"
echo 'Installed. Add $HOME/.local/bin to PATH, then run ai-team doctor.'
