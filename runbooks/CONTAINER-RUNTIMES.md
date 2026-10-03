# Containerized Provider CLI Runtimes

## Choose the entry point

For productive local work, install and operate `ai-team` through the [Linux guide](../docs/LOCAL-LINUX-WORKFLOW.md). It uses Docker Engine directly, fixed non-root UID 1001 and separate `ai-team-<role>-home` login volumes. Compose is not required for this path. Its host checks run offline without account volumes; Git metadata is read-only for agents and commits are host-owned.

The commands below describe the historical scenario/PR transport harness. Compose volumes are project-prefixed and are distinct from `ai-team` volumes. Do not interchange their logins, recovery instructions or delivery behavior.

## Why
Each provider CLI runs in its own container with its own account home volume. The container is the sandbox: host-level sandboxes such as Codex's bwrap are not required, and accounts cannot read each other's credentials.

| Environment | Agent | Service | Account | Home volume |
|---|---|---|---|---|
| OPENAI-CLI-A | Atlas | `atlas-cli` | primary OpenAI account | `atlas-home` |
| OPENAI-CLI-B | Sentinel | `sentinel-cli` | secondary OpenAI account | `sentinel-home` |
| CLAUDE-CLI | Argus | `argus-cli` | configured Claude subscription | `argus-home` |

Image: `runtimes/Dockerfile` (pinned CLI versions, non-root `agent` user with the host UID, read-only rootfs, all capabilities dropped, `no-new-privileges`).

## Build
```
docker compose -f runtimes/compose.yaml build
```
If the host UID is not 1001, export `HOST_UID=$(id -u)` first.

## Sign in (HUMAN, once per account)
Run each command in an interactive terminal and sign in with the **matching** account:
```
docker compose -f runtimes/compose.yaml run --rm atlas-cli    codex login --device-auth   # OpenAI account 1
docker compose -f runtimes/compose.yaml run --rm sentinel-cli codex login --device-auth   # OpenAI account 2
docker compose -f runtimes/compose.yaml run --rm argus-cli    claude auth login           # Claude subscription
```
Verify the result without printing secrets:
```
docker compose -f runtimes/compose.yaml run --rm -T atlas-cli    codex login status
docker compose -f runtimes/compose.yaml run --rm -T sentinel-cli codex login status
docker compose -f runtimes/compose.yaml run --rm -T argus-cli    claude auth status
```
`codex login status` does not show which account is signed in. Device auth reuses whatever ChatGPT session the browser already has, so sign in to each OpenAI account in a separate private/incognito window, signing out first. Then confirm that the two containers hold **different** users by comparing a hash of the id_token `sub` claim. Atlas and Sentinel on the same user breaks the independence model.

Credentials live in the named Docker volumes. Never copy them into the repository, prompts or evidence. Revoke access through provider controls and the intended service's logout. Removing a volume destroys local login data and does not prove remote revocation/cancellation; inspect the exact volume and effects before any deliberate removal.

## Run a scenario
```
python3 scripts/provider_run.py --container --env OPENAI-CLI-A --run-id <id> --scenario S01 --prompt-file <prompt.md> [--check "<cmd>"]
```
The harness clones HEAD into the gitignored `.runs/` directory. On Docker Desktop, its location must be shared with Docker; the original validation host used `/home` because `/tmp` was not shared. This is not a universal Linux path requirement. Only that clone (`/work`) and the run's evidence directory (`/evidence`) are mounted. The image also installs pinned validation dependencies in `/opt/validation`. Inside the container, Codex runs with `--sandbox danger-full-access`, so the container is the boundary.

## Limits
- An agent can read its **own** account credentials inside its container. Scan evidence for tokens before committing it.
- Outbound network is open, because the CLIs need their provider APIs. Do not mount host secrets, SSH agents or the Docker socket.
- OPENAI-CLI-B is Sentinel's repository-execution plane. It does not replace the live Sentinel Dot (OPENAI-DOT-B).

## GitHub PR/CI transport
```
scripts/pr_chain.sh <tag> <atlas-prompt> <sentinel-prompt> <argus-prompt>
```
The historical transport runs on the host with operator Git/gh authority (the original host used SSH alias `github-hotmail` and user `leandroclf`; configure your own authorized identity explicitly). Provider child environment removes GitHub token/SSH-agent variables; this is not a guarantee against credentials embedded in files or images. Flow: Atlas commits in its clone → branch `validation/<tag>` → draft PR → wait for CI on the head SHA → Sentinel and Argus review `refs/pull/<n>/head` fetched over public HTTPS, and the run fails if the SHA differs → verdicts published as commit statuses `sentinel/review` and `argus/assurance` plus PR comments → PR closed unmerged and branch deleted. Statuses are per-SHA, so a new push to the PR never inherits earlier verdicts. Evidence: `validation/runs/<tag>-transport/transport.yaml`.

## Updated provider review contract

The PR chain requires structured JSON reviews. Codex receives `--output-schema`; Claude receives `--json-schema`, restricted mode and unattended permission denial. Rebuild the image after changing validation dependencies. `--max-turns 30` bounds the Claude invocation; it is not a subscription spending limit.

Before a controlled run, execute `python3 scripts/preflight.py --provider codex` or `--provider claude` in the intended runtime/checkout and preserve the sanitized JSON. Probe commands do not install software, log in or prove account independence. Pin updates require official release review and canary execution; never update a running task implicitly.

Read-only mounts protect checkout writes; running Python tests still executes arbitrary code. The historical credential-bearing harness container is not a safe executor for hostile repository tests. Local `ai-team` implements separate offline checks without credentials; the legacy harness does not gain this isolation automatically. The policy forbidding checkout-code execution inside authenticated agents is not enforced per tool call. Provider children do not inherit GitHub token/SSH-agent environment variables, but their own credentials on disk remain accessible within their container.

## Stop and revoke

1. Stop the specific run and verify local child processes. POSIX harness timeout now terminates the process group.
2. Inspect Docker/remote task state independently; killing a CLI client is not evidence the container or remote task stopped.
3. For a Dot, inspect delegated tasks in Activity and stop them separately. Inspect recurring schedules independently from pausing the main Dot task.
4. Revoke the relevant access using provider controls, then reconcile in-flight and completed effects. Admin revocation of Dot local access may allow already authorized work to finish.
5. Re-read authorization revision and external state before allowing another operation. Preserve unresolved cancellation as INCONCLUSIVE.

See the dated official sources in `docs/PROVIDER-GUIDANCE-REVIEW.md`. These are operational instructions; this review did not stop tasks, revoke accounts or remove volumes.
