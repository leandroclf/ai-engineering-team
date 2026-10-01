#!/usr/bin/env bash
# Atlas -> GitHub PR/CI -> Sentinel -> Argus over real GitHub transport.
# Agents hold no GitHub credentials: this orchestrator (operator identity) pushes, opens the PR,
# waits for CI and publishes each reviewer verdict as a commit status + PR comment bound to the head SHA.
# The PR is closed unmerged so validation fixtures on main stay intact.
#
# Usage: scripts/pr_chain.sh <tag> <atlas-prompt> <sentinel-prompt> <argus-prompt>
set -euo pipefail
TAG=$1; ATLAS_PROMPT=$2; SENTINEL_PROMPT=$3; ARGUS_PROMPT=$4
ROOT=$(cd "$(dirname "$0")/.." && pwd); cd "$ROOT"
REPO=leandroclf/ai-engineering-team
PUSH_URL=${PUSH_URL:-git@github-hotmail:$REPO.git}     # operator's SSH identity with push access
FETCH_URL=https://github.com/$REPO.git                  # reviewers read from GitHub, not the local repo
export GH_TOKEN=${GH_TOKEN:-$(gh auth token --user "${GH_USER:-leandroclf}")}
BRANCH=validation/$TAG
OUT=validation/runs/$TAG-transport; mkdir -p "$OUT"
log(){ echo "$1: $2" >> "$OUT/transport.yaml"; }

python3 scripts/provider_run.py --container --env OPENAI-CLI-A --run-id "$TAG-atlas" --scenario AS01 --risk R2 \
  --prompt-file "$ATLAS_PROMPT" --check "git log --oneline -3"
CLONE=.runs/clone-$TAG-atlas
git -C "$CLONE" diff --cached --quiet HEAD || git -C "$CLONE" commit -qm "harness: snapshot of uncommitted Atlas changes"
HEAD_SHA=$(git -C "$CLONE" rev-parse HEAD)
git -C "$CLONE" push -q "$PUSH_URL" "HEAD:refs/heads/$BRANCH"
PR_URL=$(gh pr create -R "$REPO" --draft -B main -H "$BRANCH" -t "validation($TAG): Atlas remediation under independent review" \
  -b "Validation-only PR from \`scripts/pr_chain.sh\`. Head \`$HEAD_SHA\`. Never merged; closed after Sentinel/Argus evidence is recorded.")
PR=${PR_URL##*/}
log pr_url "$PR_URL"; log head_sha "$HEAD_SHA"; log branch "$BRANCH"

# CI on the exact head SHA.
until RUN=$(gh run list -R "$REPO" --commit "$HEAD_SHA" --event pull_request --json databaseId,status,conclusion \
        -q '.[0] | select(.status=="completed") | "\(.databaseId) \(.conclusion)"') && [ -n "$RUN" ]; do sleep 10; done
log ci_run "${RUN% *}"; log ci_conclusion "${RUN#* }"

# Reviewers start from the PR head fetched from GitHub and refuse a SHA mismatch.
PRE="git fetch -q $FETCH_URL refs/pull/$PR/head && git reset -q --hard FETCH_HEAD && test \$(git rev-parse HEAD) = $HEAD_SHA"
python3 scripts/provider_run.py --container --env OPENAI-CLI-B --run-id "$TAG-sentinel" --scenario AS03 --risk R2 \
  --prompt-file "$SENTINEL_PROMPT" --pre "$PRE" --check "git rev-parse HEAD" &
python3 scripts/provider_run.py --container --env CLAUDE-CLI --run-id "$TAG-argus" --scenario XH-ATLAS-ARGUS --risk R2 \
  --prompt-file "$ARGUS_PROMPT" --pre "$PRE" --check "git rev-parse HEAD" &
wait

publish(){ # context run-id
  local msg=validation/runs/$2/last-message.md verdict state
  verdict=$(grep -m1 -oE '^verdict: *[A-Z_]+' "$msg" | awk '{print $2}' || true)
  case $verdict in PASS|PASS_WITH_FINDINGS) state=success;; BLOCKED) state=failure;; *) state=pending;; esac
  [ "$(sed -n 3p "validation/runs/$2/check.txt")" = "$HEAD_SHA" ] || { state=error; verdict="SHA_MISMATCH"; }
  gh api -X POST "repos/$REPO/statuses/$HEAD_SHA" -f state=$state -f context="$1" \
    -f description="${verdict:-NO_VERDICT} (validation/runs/$2)" >/dev/null
  { echo "### \`$1\` — ${verdict:-NO_VERDICT} @ \`$HEAD_SHA\`"; echo; echo '```yaml'; sed -n '/^schema_version/,/^reviewed_at/p' "$msg"; echo '```'; } \
    | gh pr comment "$PR" -R "$REPO" -F - >/dev/null
  log "status_$1" "$state ${verdict:-NO_VERDICT}"
}
publish sentinel/review "$TAG-sentinel"
publish argus/assurance "$TAG-argus"

gh pr close "$PR" -R "$REPO" -d -c "Validation complete; closed unmerged by design." >/dev/null
log closed_unmerged true
cat "$OUT/transport.yaml"
