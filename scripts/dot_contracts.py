"""Deterministic repository-side checks; never grants native/provider permission.

Call with trusted, freshly observed state immediately before a bounded operation.
This checker performs no external operation and is not a persistent agent runtime.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
FORMATS = FormatChecker()


@FORMATS.checks("date-time", raises=(ValueError, TypeError))
def aware_datetime(value):
    if not isinstance(value, str):
        return True  # JSON Schema handles the type independently.
    return timestamp(value).tzinfo is not None and "T" in value


def validate(kind, value):
    schema = json.loads((ROOT / "schemas" / f"{kind}.schema.json").read_text())
    Draft202012Validator(schema, format_checker=FORMATS).validate(value)


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed


def safe_path(value):
    path = PurePosixPath(value)
    return (bool(value) and not path.is_absolute() and ".." not in path.parts
            and "\\" not in value and path.as_posix() == value and value != ".")


def in_scope(path, roots):
    return safe_path(path) and any(safe_path(r) and (path == r or path.startswith(r.rstrip("/") + "/")) for r in roots)


def authorize(task, state, action, paths=(), *, now=None, external=False):
    validate("dot-codex-task", task)
    validate("authorization-state", state)
    lease = task["authorization"]
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("timezone required")
    if (lease["task_id"], lease["project_id"], lease["repository"]) != (task["task_id"], task["project_id"], task["repository"]):
        return "BLOCKED_PERMISSION"
    if (lease["scope_id"], lease["revision"], lease["task_id"], lease["project_id"]) != (state["scope_id"], state["revision"], state["task_id"], state["project_id"]) or state["revoked"]:
        return "EXPIRED_SCOPE"
    if not timestamp(lease["issued_at"]) <= now < timestamp(lease["expires_at"]):
        return "EXPIRED_SCOPE"
    if state["repository"] != task["repository"]:
        return "INCONCLUSIVE"
    if task["risk"] == "R3":
        return "BLOCKED_APPROVAL"  # R3 is handed to native/operator approval, never auto-approved here.
    if action not in lease["allowed_actions"] or action in lease["denied_actions"]:
        return "BLOCKED_PERMISSION"
    writes = {"modify_branch", "create_commit", "create_pr"}
    if task["risk"] == "R0" and action in writes:
        return "BLOCKED_PERMISSION"
    if action in writes and (not paths or not all(in_scope(p, lease["allowed_paths"]) for p in paths)):
        return "BLOCKED_PERMISSION"
    if any(not in_scope(p, lease["allowed_paths"]) for p in paths):
        return "BLOCKED_PERMISSION"
    budget = task["budgets"]
    if state["circuit_open"]:
        return "UNAVAILABLE"
    if state["attempts_used"] >= budget["max_attempts"] or state["elapsed_seconds"] >= budget["max_elapsed_seconds"]:
        return "CANCELLED"
    if (external or action == "create_pr") and state["external_writes_used"] >= budget["max_external_writes"]:
        return "CANCELLED"
    return "PASS"


def verify_evidence(task, evidence, artifact_root, observed_final_sha):
    """Validate a claim against artifact bytes and a separately observed final SHA.

    Recorded exit codes/CI are not authenticated by a hash. The caller must obtain
    those records from a trusted runner/GitHub; an executor-authored claim alone
    never establishes successful execution.
    """
    validate("dot-codex-task", task)
    validate("execution-evidence", evidence)
    problems = []
    if (evidence["task_id"], evidence["project_id"], evidence["observed_base_sha"]) != (task["task_id"], task["project_id"], task["repository"]["base_sha"]):
        problems.append("task/project/base mismatch")
    if evidence["final_sha"] != observed_final_sha:
        problems.append("final SHA mismatch")
    if not all(in_scope(p, task["authorization"]["allowed_paths"]) for p in evidence["changed_files"]):
        problems.append("changes outside authorized paths")
    if evidence["external_writes"] > task["budgets"]["max_external_writes"]:
        problems.append("external write budget exceeded")
    root = Path(artifact_root).resolve()
    commands = {}
    for check in evidence["checks"]:
        command = check["command"]
        if command in commands:
            problems.append("duplicate command evidence")
        commands[command] = check["exit_code"]
        artifact = check["artifact"]
        path = (root / artifact).resolve()
        if not safe_path(artifact) or not path.is_relative_to(root) or not path.is_file():
            problems.append("missing/unsafe check artifact")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != check["sha256"]:
            problems.append("artifact hash mismatch")
    if evidence["status"] == "PASS":
        if evidence["failures"] or any(c != 0 for c in commands.values()):
            problems.append("PASS with failures")
        if any(commands.get(c) != 0 for c in task["required_validation"]):
            problems.append("required successful command missing")
        if evidence["ci"] != {"head_sha": observed_final_sha, "status": "success"}:
            problems.append("successful CI on final SHA missing")
        if task["risk"] == "R0" and (evidence["changed_files"] or evidence["external_writes"]):
            problems.append("R0 mutation")
    return problems
