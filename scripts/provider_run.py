#!/usr/bin/env python3
"""Run one provider-CLI validation scenario in a disposable clone and preserve observable evidence.

Usage:
  provider_run.py --run-id ID --scenario S01 --env OPENAI-CLI-A --risk R0 --prompt-file P [--pre CMD] [--check CMD]

The clone is taken from the committed HEAD, so fixtures must be committed first.
Reasoning/thinking events are dropped; only messages, tool calls and results are kept.
The manifest is written with status INCONCLUSIVE; the evaluator sets the final status.
"""
import argparse
import datetime
import json
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
AGENTS = {"OPENAI-CLI-A": ("Atlas", "openai"), "CLAUDE-CLI": ("Argus", "anthropic")}
CLAUDE_READ_ONLY = ["Read", "Grep", "Glob"]
CLAUDE_DENIED = ["Edit", "Write", "Bash", "NotebookEdit", "WebFetch", "WebSearch", "Agent"]


def sh(cmd, cwd, **kw):
    return subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), text=True, capture_output=True,
                          stdin=subprocess.DEVNULL, **kw)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def provider_cmd(env, prompt, run_dir):
    if env == "OPENAI-CLI-A":
        return ["codex", "exec", "--json", "--sandbox", "workspace-write", "--ephemeral",
                "-o", str(run_dir / "last-message.md"), prompt]
    return ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
            "--setting-sources", "project", "--no-session-persistence", "--strict-mcp-config",
            # --tools is the effective allow-list; --allowedTools only pre-approves.
            "--tools", *CLAUDE_READ_ONLY, "--allowedTools", *CLAUDE_READ_ONLY,
            "--disallowedTools", *CLAUDE_DENIED]


def keep(event):
    """Drop hidden reasoning; keep observable events."""
    if event.get("item", {}).get("type") == "reasoning":
        return None
    if event.get("type") == "assistant":
        content = event.get("message", {}).get("content", [])
        event["message"]["content"] = [c for c in content if c.get("type") not in ("thinking", "redacted_thinking")]
    return event


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--env", required=True, choices=AGENTS)
    ap.add_argument("--risk", default="R0")
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--pre", help="shell command run in the clone before the provider (fixture setup)")
    ap.add_argument("--check", help="evaluator shell command run in the clone after the provider")
    ap.add_argument("--workdir", default="/tmp", help="parent dir for the disposable clone")
    a = ap.parse_args()

    run_dir = ROOT / "validation" / "runs" / a.run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    clone = pathlib.Path(a.workdir) / f"clone-{a.run_id}"
    sh(["git", "clone", "--quiet", "--no-hardlinks", str(ROOT), str(clone)], ROOT).check_returncode()
    for k, v in (("user.name", "validation-harness"), ("user.email", "harness@invalid")):
        sh(["git", "config", k, v], clone)
    base_sha = sh("git rev-parse HEAD", clone).stdout.strip()
    pre = sh(a.pre, clone) if a.pre else None
    head_sha = sh("git rev-parse HEAD", clone).stdout.strip()

    prompt = pathlib.Path(a.prompt_file).read_text()
    (run_dir / "prompt.md").write_text(prompt)
    started = now()
    proc = sh(provider_cmd(a.env, prompt, run_dir), clone, timeout=1800)
    finished = now()

    events = []
    for line in proc.stdout.splitlines():
        try:
            e = keep(json.loads(line))
        except json.JSONDecodeError:
            continue
        if e is not None:
            events.append(json.dumps(e))
    (run_dir / "events.jsonl").write_text("\n".join(events) + "\n")
    if a.env == "CLAUDE-CLI":
        result = [json.loads(e) for e in events if json.loads(e).get("type") == "result"]
        (run_dir / "last-message.md").write_text(result[-1].get("result", "") if result else "")

    sh("git add -A", clone)
    files_changed = sh(["git", "diff", "--cached", "--name-only", head_sha], clone).stdout.split()
    (run_dir / "diff.patch").write_text(sh(["git", "diff", "--cached", head_sha], clone).stdout)
    checks = [{"command": "<provider exit>", "exit_code": proc.returncode}]
    if a.check:
        chk = sh(a.check, clone)
        (run_dir / "check.txt").write_text(f"$ {a.check}\nexit={chk.returncode}\n{chk.stdout}{chk.stderr}")
        checks.append({"command": a.check, "exit_code": chk.returncode})

    agent, provider = AGENTS[a.env]
    manifest = yaml.safe_load((ROOT / "validation" / "RUN-MANIFEST-TEMPLATE.yaml").read_text())
    manifest.update(
        run_id=a.run_id, scenario_id=a.scenario, environment=a.env, agent_name=agent, provider=provider,
        base_sha=base_sha, head_sha=head_sha, started_at=started, finished_at=finished, risk=a.risk,
        prompt_artifact="prompt.md", files_changed=files_changed, checks=checks,
        commands_or_actions=[" ".join(provider_cmd(a.env, "<prompt.md>", pathlib.Path("<run>")))]
        + ([f"pre: {a.pre} (exit {pre.returncode})"] if pre else []),
        evidence_locations=[f"validation/runs/{a.run_id}/{n}" for n in sorted(p.name for p in run_dir.iterdir())],
        notes="status pending evaluator review",
    )
    (run_dir / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True))
    print(json.dumps({"run_id": a.run_id, "exit": proc.returncode, "files_changed": files_changed,
                      "checks": checks, "clone": str(clone)}))
    if proc.returncode and not events:
        sys.stderr.write(proc.stderr[-2000:])


if __name__ == "__main__":
    main()
