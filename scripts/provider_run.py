#!/usr/bin/env python3
"""Run one provider-CLI validation scenario in a disposable clone and preserve observable evidence.

Usage:
  provider_run.py --run-id ID --scenario S01 --env OPENAI-CLI-A --risk R0 --prompt-file P [--pre CMD] [--check CMD]

The clone is taken from the committed HEAD, so fixtures must be committed first.
Reasoning/thinking events are dropped; only messages, tool calls and results are kept.
Successful execution remains INCONCLUSIVE pending evaluation; failures/unavailability are recorded.
"""
import argparse
import datetime
import json
import pathlib
import re
import os
import signal
import subprocess
import sys

import yaml
from jsonschema import ValidationError
try:
    from .review_contract import SCHEMA_PATH, read_json, validate_review
except ImportError:
    from review_contract import SCHEMA_PATH, read_json, validate_review

ROOT = pathlib.Path(__file__).resolve().parent.parent
AGENTS = {"OPENAI-CLI-A": ("Atlas", "openai"), "OPENAI-CLI-B": ("Sentinel", "openai"),
          "CLAUDE-CLI": ("Argus", "anthropic")}
# runtimes/compose.yaml service per environment; each has its own account home volume.
SERVICES = {"OPENAI-CLI-A": "atlas-cli", "OPENAI-CLI-B": "sentinel-cli", "CLAUDE-CLI": "argus-cli"}
COMPOSE = ["docker", "compose", "-f", str(ROOT / "runtimes" / "compose.yaml"), "run", "--rm", "-T"]
CLAUDE_TOOLS = ["Read", "Grep", "Glob", "Bash"]
# Only the listed Bash patterns are pre-approved. Tests execute checkout code;
# this allow-list does not isolate that code from credentials or network.
CLAUDE_ALLOWED = ["Read", "Grep", "Glob", "Bash(git log:*)", "Bash(git show:*)", "Bash(git diff:*)",
                  "Bash(git rev-parse:*)", "Bash(git status:*)", "Bash(python3 -m unittest:*)",
                  "Bash(python3 -B -m unittest:*)",
                  "Bash(python3 scripts/validate.py:*)", "Bash(python3 scripts/validate_hardening.py:*)",
                  "Bash(python3 -B scripts/validate.py:*)", "Bash(python3 -B scripts/validate_hardening.py:*)"]
CLAUDE_DENIED = ["Edit", "Write", "NotebookEdit", "WebFetch", "WebSearch", "Agent", "mcp__*"]


def sh(cmd, cwd, **kw):
    return subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), text=True, capture_output=True,
                          stdin=subprocess.DEVNULL, **kw)


def run_observed(cmd, cwd, timeout=1800, env=None):
    """Preserve failures; terminate the local process group on POSIX timeout."""
    try:
        proc = subprocess.Popen(cmd, cwd=cwd, shell=isinstance(cmd, str), text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.DEVNULL, start_new_session=os.name == 'posix', env=env)
    except FileNotFoundError:
        return subprocess.CompletedProcess(cmd, 127, "", "executor unavailable\n")
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        return subprocess.CompletedProcess(cmd, proc.returncode, stdout, stderr)
    except subprocess.TimeoutExpired:
        def stop(sig):
            try:
                if os.name == 'posix':
                    os.killpg(proc.pid, sig)
                else:
                    proc.kill()
            except ProcessLookupError:
                pass
        stop(signal.SIGTERM)
        try:
            stdout, stderr = proc.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            stop(signal.SIGKILL)
            stdout, stderr = proc.communicate()
        return subprocess.CompletedProcess(cmd, 124, stdout, stderr + "\nexecution timed out\n")


def provider_environment():
    """Keep GitHub transport authority outside the provider subprocess."""
    return {key: value for key, value in os.environ.items()
            if key not in {'GH_TOKEN', 'GITHUB_TOKEN', 'GH_ENTERPRISE_TOKEN', 'GITHUB_ENTERPRISE_TOKEN',
                           'SSH_AUTH_SOCK', 'GIT_ASKPASS', 'SSH_ASKPASS'}}


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def provider_cmd(env, prompt, run_dir, container=False, structured_review=False):
    if env.startswith("OPENAI-CLI"):
        # In a container the container is the sandbox (only the clone and evidence dir are mounted).
        sandbox = "danger-full-access" if container else ("read-only" if env == "OPENAI-CLI-B" else "workspace-write")
        out = "/evidence/last-message.md" if container else str(run_dir / "last-message.md")
        cmd = ["codex", "--ask-for-approval", "never", "exec", "--json", "--sandbox", sandbox, "--ephemeral", "-o", out]
        if structured_review:
            schema = "/evidence/provider-review.schema.json" if container else str(SCHEMA_PATH)
            cmd += ["--output-schema", schema]
        return cmd + [prompt]
    cmd = ["claude", "-p", prompt, "--output-format", "json" if structured_review else "stream-json", "--verbose",
            "--permission-mode", "dontAsk", "--permission-prompts", "none", "--max-turns", "30",
            "--restricted", "--settings", '{"disableAllHooks":true,"disableClaudeAiConnectors":true}',
            "--no-session-persistence", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
            # --tools is the effective allow-list; --allowedTools only pre-approves.
            "--tools", *CLAUDE_TOOLS, "--allowedTools", *CLAUDE_ALLOWED,
            "--disallowedTools", *CLAUDE_DENIED]
    if structured_review:
        cmd += ["--json-schema", SCHEMA_PATH.read_text()]
    return cmd


def keep(event):
    """Drop hidden reasoning and init credentials; redact known secret-valued keys."""
    if not isinstance(event, dict):
        return None
    if event.get('type') == 'system' and event.get('subtype') == 'init':
        return {key: event[key] for key in ('type', 'subtype', 'session_id', 'model') if key in event}
    secret_keys = {'access_token', 'refresh_token', 'id_token', 'api_key', 'apikey',
                   'authorization', 'client_secret', 'password'}
    def scrub(value):
        if isinstance(value, dict):
            if value.get('type') in ('reasoning', 'thinking', 'redacted_thinking'):
                return None
            return {key: '[REDACTED]' if key.lower() in secret_keys else scrub(item)
                    for key, item in value.items()}
        if isinstance(value, list):
            return [clean for item in value if (clean := scrub(item)) is not None]
        return value
    cleaned = scrub(event)
    if cleaned is not None and event.get('item', {}).get('type') == 'reasoning':
        return None
    return cleaned


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--env", required=True, choices=AGENTS)
    ap.add_argument("--risk", default="R0", choices=["R0", "R1", "R2", "R3"])
    ap.add_argument("--timeout-seconds", type=int, default=1800)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--structured-review", action="store_true", help="require provider JSON Schema review output")
    ap.add_argument("--pre", help="shell command run in the clone before the provider (fixture setup)")
    ap.add_argument("--check", help="evaluator shell command run in the clone after the provider")
    ap.add_argument("--container", action="store_true",
                    help="run the CLI in its runtimes/compose.yaml service instead of on the host")
    # Docker Desktop shares /home but not /tmp, so clones live in the gitignored .runs/.
    ap.add_argument("--workdir", default=str(ROOT / ".runs"), help="parent dir for the disposable clone")
    a = ap.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", a.run_id):
        ap.error("run-id must be a single safe path component")
    if a.timeout_seconds <= 0:
        ap.error("timeout-seconds must be positive")
    if a.structured_review and a.env == "OPENAI-CLI-A":
        ap.error("structured-review requires a reviewer environment")
    prompt = pathlib.Path(a.prompt_file).read_text()
    if a.structured_review:
        prompt += "\nReturn the review using the supplied JSON schema; bind head_sha to the actual checkout HEAD.\n"

    run_dir = ROOT / "validation" / "runs" / a.run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    clone = pathlib.Path(a.workdir) / f"clone-{a.run_id}"
    sh(["git", "clone", "--quiet", "--no-hardlinks", str(ROOT), str(clone)], ROOT).check_returncode()
    for k, v in (("user.name", "validation-harness"), ("user.email", "harness@invalid")):
        sh(["git", "config", k, v], clone)
    base_sha = sh("git rev-parse HEAD", clone).stdout.strip()
    pre = run_observed(a.pre, clone, a.timeout_seconds) if a.pre else None
    head_sha = sh("git rev-parse HEAD", clone).stdout.strip()

    (run_dir / "prompt.md").write_text(prompt)
    started = now()
    if a.structured_review:
        (run_dir / "provider-review.schema.json").write_text(SCHEMA_PATH.read_text())
    cmd = provider_cmd(a.env, prompt, run_dir, a.container, a.structured_review)
    if a.container:
        # Reviewers (Sentinel, Argus) get a read-only checkout, enforced by Docker, not by the agent.
        ro = ":ro" if a.env in ("OPENAI-CLI-B", "CLAUDE-CLI") else ""
        cmd = COMPOSE + ["-e", "PYTHONDONTWRITEBYTECODE=1", "-v", f"{clone}:/work{ro}",
                         "-v", f"{run_dir}:/evidence", SERVICES[a.env]] + cmd
    proc = (subprocess.CompletedProcess(cmd, pre.returncode, "", "fixture setup failed; provider not started\n")
            if pre and pre.returncode else run_observed(cmd, clone, a.timeout_seconds, env=provider_environment()))
    (run_dir / "stderr.txt").write_text(proc.stderr)
    if pre:
        (run_dir / "pre.txt").write_text(f"exit={pre.returncode}\n{pre.stdout}{pre.stderr}")
    finished = now()
    if not (run_dir / "last-message.md").exists():
        (run_dir / "last-message.md").write_text("")

    events = []
    lines = proc.stdout.splitlines()
    if a.env == "CLAUDE-CLI" and a.structured_review:
        # --output-format json is one document, possibly pretty-printed, not JSONL.
        try:
            payload = read_json(proc.stdout)
            lines = [json.dumps(payload)]
        except (ValueError, TypeError):
            lines = []
    for line in lines:
        try:
            e = keep(json.loads(line))
        except (json.JSONDecodeError, AttributeError, TypeError):
            continue
        if e is not None:
            events.append(json.dumps(e))
    if not proc.returncode and any(e.get('type') in ('error', 'turn.failed') or
                                  (e.get('type') == 'result' and e.get('is_error') is True)
                                  for e in map(json.loads, events)):
        proc.returncode = 65
    (run_dir / "events.jsonl").write_text("\n".join(events) + "\n")
    if a.env == "CLAUDE-CLI":
        result = [json.loads(e) for e in events if json.loads(e).get("type") == "result"]
        value = result[-1].get("result", "") if result else ""
        if a.structured_review and result:
            value = json.dumps(result[-1].get("structured_output"))
        (run_dir / "last-message.md").write_text(value)

    if a.structured_review and not proc.returncode:
        try:
            review = validate_review(read_json((run_dir / "last-message.md").read_text()))
            (run_dir / "review.json").write_text(json.dumps(review, indent=2) + "\n")
        except (OSError, ValueError, TypeError, ValidationError):
            proc.returncode = 65  # Invalid structured output never falls back to a prose PASS.
            (run_dir / "stderr.txt").write_text("invalid structured review output\n")

    sh("git add -A", clone)
    files_changed = sh(["git", "diff", "--cached", "--name-only", head_sha], clone).stdout.split()
    (run_dir / "diff.patch").write_text(sh(["git", "diff", "--cached", head_sha], clone).stdout)
    checks = [{"command": "<provider exit>", "exit_code": proc.returncode}]
    if a.check and not proc.returncode:
        chk = run_observed(a.check, clone, a.timeout_seconds)
        (run_dir / "check.txt").write_text(f"$ {a.check}\nexit={chk.returncode}\n{chk.stdout}{chk.stderr}")
        checks.append({"command": a.check, "exit_code": chk.returncode})

    agent, provider = AGENTS[a.env]
    manifest = yaml.safe_load((ROOT / "validation" / "RUN-MANIFEST-TEMPLATE.yaml").read_text())
    manifest.update(
        run_id=a.run_id, scenario_id=a.scenario, environment=a.env, agent_name=agent, provider=provider,
        base_sha=base_sha, head_sha=head_sha, started_at=started, finished_at=finished, risk=a.risk,
        structured_review=a.structured_review,
        prompt_artifact="prompt.md", files_changed=files_changed, checks=checks,
        commands_or_actions=[(f"container {SERVICES[a.env]}: " if a.container else "host: ")
                             + " ".join(provider_cmd(a.env, "<prompt.md>", pathlib.Path("<run>"), a.container, a.structured_review))]
        + ([f"pre: {a.pre} (exit {pre.returncode})"] if pre else []),
        evidence_locations=[f"validation/runs/{a.run_id}/{n}" for n in sorted(p.name for p in run_dir.iterdir())],
        status="FAIL" if (pre and pre.returncode) or any(c["exit_code"] != 0 for c in checks[1:]) or proc.returncode not in (0, 124, 127)
               else "BLOCKED" if proc.returncode == 127 else "INCONCLUSIVE",
        failures=(["fixture setup failed"] if pre and pre.returncode else [])
                 + ([f"provider exit {proc.returncode}"] if proc.returncode else [])
                 + (["required check failed"] if len(checks) > 1 and checks[-1]["exit_code"] else []),
        notes="executor unavailable" if proc.returncode == 127 else "execution timed out" if proc.returncode == 124
              else "execution failed" if proc.returncode else "status pending evaluator review",
    )
    (run_dir / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True))
    print(json.dumps({"run_id": a.run_id, "exit": proc.returncode, "files_changed": files_changed,
                      "checks": checks, "clone": str(clone)}))
    if proc.returncode and not events:
        sys.stderr.write(proc.stderr[-2000:])
    return 1 if any(c["exit_code"] for c in checks) else 0


if __name__ == "__main__":
    sys.exit(main())
