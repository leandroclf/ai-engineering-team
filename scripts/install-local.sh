#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
BIN_DIR=${AI_TEAM_BIN_DIR:-"$HOME/.local/bin"}
MODE=${1:-install}
[ "$#" -le 1 ] || { echo 'Too many arguments; use --help.' >&2; exit 2; }
case "$MODE" in
  --help|-h)
    echo 'Usage: bash scripts/install-local.sh [--check|--help]'
    echo 'Linux user install: venv, pinned dependencies, Docker image, then ai-team link.'
    echo 'AI_TEAM_BIN_DIR overrides $HOME/.local/bin. --check performs preflight only.'
    exit 0 ;;
  install|--check) ;;
  *) echo 'Unknown argument; use --help.' >&2; exit 2 ;;
esac
fail() { echo "Bootstrap blocked: $*" >&2; exit 2; }
[ "$(uname -s)" = Linux ] || fail 'Linux is required.'
for tool in python3 git docker readlink; do
  command -v "$tool" >/dev/null || fail "Missing $tool; install it using your Linux distribution."
done
python3 -c 'import sys, venv, ensurepip; sys.exit(0 if sys.version_info >= (3, 10) else 1)' || fail 'Python 3.10+ with venv/ensurepip is required.'
[ ! -e "$BIN_DIR" ] || [ -d "$BIN_DIR" ] || fail 'Command directory is not a directory.'
if [ -e "$BIN_DIR/ai-team" ] || [ -L "$BIN_DIR/ai-team" ]; then
  [ -L "$BIN_DIR/ai-team" ] && [ "$(readlink -f "$BIN_DIR/ai-team" || true)" = "$ROOT/bin/ai-team" ] || fail 'Existing ai-team command found; preserve it and resolve the destination manually.'
fi
docker info >/dev/null 2>&1 || fail 'Docker daemon is unavailable to this user; check service and access.'
if [ "$MODE" = --check ]; then
  echo 'Preflight passed. No files, packages, images or logins changed.'
  exit 0
fi
python3 -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install -r "$ROOT/requirements-validation.txt"
docker build -f "$ROOT/runtimes/Dockerfile" -t ai-eng-provider-cli:local "$ROOT"
chmod +x "$ROOT/bin/ai-team"
mkdir -p "$BIN_DIR"
# Recheck after the build: never replace a destination created during installation.
if [ -e "$BIN_DIR/ai-team" ] || [ -L "$BIN_DIR/ai-team" ]; then
  [ -L "$BIN_DIR/ai-team" ] && [ "$(readlink -f "$BIN_DIR/ai-team" || true)" = "$ROOT/bin/ai-team" ] || fail 'Command destination changed during installation.'
else
  ln -sT "$ROOT/bin/ai-team" "$BIN_DIR/ai-team"
fi
echo "Installed. Add $BIN_DIR to PATH. Login atlas --stage plan, argus, sentinel, and atlas --stage review; then run ai-team doctor."
