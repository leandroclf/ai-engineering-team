# Containerized Provider CLI Runtimes

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

Credentials live only in the named Docker volumes. Never copy them into the repository, prompts or evidence. To revoke access, run `logout` in the service or `docker volume rm <volume>`.

## Run a scenario
```
python3 scripts/provider_run.py --container --env OPENAI-CLI-A --run-id <id> --scenario S01 --prompt-file <prompt.md> [--check "<cmd>"]
```
The harness clones HEAD into the gitignored `.runs/` directory, which must be under `/home` because Docker Desktop does not share `/tmp`. Only that clone (`/work`) and the run's evidence directory (`/evidence`) are mounted. Inside the container, Codex runs with `--sandbox danger-full-access`, so the container is the boundary.

## Limits
- An agent can read its **own** account credentials inside its container. Scan evidence for tokens before committing it.
- Outbound network is open, because the CLIs need their provider APIs. Do not mount host secrets, SSH agents or the Docker socket.
- OPENAI-CLI-B is Sentinel's repository-execution plane. It does not replace the live Sentinel Dot (OPENAI-DOT-B).
