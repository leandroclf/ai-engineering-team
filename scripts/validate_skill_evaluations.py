"""Validate benchmark and internal skill-evaluation contracts offline."""
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "evaluation" / "benchmarks.yaml"
TASKS = ROOT / "evaluation" / "tasks"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def main():
    errors = []
    try:
        catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"catalog invalid: {exc}", file=sys.stderr)
        return 1
    if catalog.get("evaluation_contract") != "skill-evaluation-v1":
        errors.append("unsupported evaluation contract")
    if not SEMVER.match(str(catalog.get("catalog_version", ""))):
        errors.append("catalog_version must be semantic version")
    benchmark_ids = set()
    for item in catalog.get("benchmarks", []):
        benchmark_id = item.get("id")
        if benchmark_id in benchmark_ids:
            errors.append(f"duplicate benchmark {benchmark_id}")
        benchmark_ids.add(benchmark_id)
        for field in ("name", "kind", "purpose", "source", "status", "verifier"):
            if not item.get(field):
                errors.append(f"{benchmark_id}: missing {field}")
        if not str(item.get("source", "")).startswith(("https://", "repository")):
            errors.append(f"{benchmark_id}: source must be https or repository")
        if not isinstance(item.get("limitations"), list) or not item["limitations"]:
            errors.append(f"{benchmark_id}: limitations must be non-empty")
    metric_ids = set()
    for metric in catalog.get("metrics", []):
        if metric.get("id") in metric_ids:
            errors.append(f"duplicate metric {metric.get('id')}")
        metric_ids.add(metric.get("id"))
        if not metric.get("unit"):
            errors.append(f"{metric.get('id')}: missing unit")
    for path in sorted(TASKS.glob("*.yaml")):
        try:
            suite = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"{path.name}: invalid YAML: {exc}")
            continue
        if not suite.get("suite_id") or not SEMVER.match(str(suite.get("version", ""))):
            errors.append(f"{path.name}: suite_id/version invalid")
        if not suite.get("conditions") or "baseline" not in suite["conditions"]:
            errors.append(f"{path.name}: baseline condition required")
        for task in suite.get("tasks", []):
            for field in ("id", "objective", "required_skills", "verifier", "expected"):
                if not task.get(field):
                    errors.append(f"{path.name}/{task.get('id')}: missing {field}")
            if not set(task.get("required_skills", [])).issubset({"architect", "backend", "qa", "security", "observability", "code-review", "tech-lead"}):
                errors.append(f"{path.name}/{task.get('id')}: unknown skill")
    if not benchmark_ids or not metric_ids or not list(TASKS.glob("*.yaml")):
        errors.append("evaluation catalog must contain benchmarks, metrics and task suites")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {len(benchmark_ids)} benchmarks, {len(metric_ids)} metrics and {len(list(TASKS.glob('*.yaml')))} task suites validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
