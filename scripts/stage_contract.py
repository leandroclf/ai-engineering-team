"""Fixed local workflow contracts; no model router or external service."""
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
STAGES = {
    'plan': ('atlas', 'codex'),
    'implement': ('argus', 'claude'),
    'validate': ('sentinel', 'codex'),
    'review': ('atlas', 'claude'),
}
DEFAULT_MODELS = {
    'plan': {'model': 'gpt-6-astra', 'effort': 'xhigh'},
    'implement': {'model': 'claude-opus-5-5', 'effort': 'high'},
    'validate': {'model': 'gpt-6-astra', 'effort': 'xhigh'},
    'review': {'model': 'claude-opus-5-5', 'effort': 'high'},
}
PLAN_SCHEMA = ROOT / 'schemas/local-plan.schema.json'
REVIEW_SCHEMA = ROOT / 'schemas/local-review.schema.json'
IMPLEMENT_SCHEMA = ROOT / 'schemas/local-implementation.schema.json'


def validate_plan(value, sha):
    Draft202012Validator(json.loads(PLAN_SCHEMA.read_text())).validate(value)
    if value['base_sha'] != sha:
        raise ValueError('plan does not match planning HEAD')
    criteria = [x['id'] for x in value['acceptance_criteria']]
    tasks = [x['id'] for x in value['tasks']]
    referenced = {x for task in value['tasks'] for x in task['acceptance_ids']}
    if len(set(criteria)) != len(criteria) or len(set(tasks)) != len(tasks) or referenced != set(criteria):
        raise ValueError('plan has duplicate ids, missing coverage or unknown acceptance ids')
    return value


def plan_id(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def validate_assessment(value, plan, identifier):
    Draft202012Validator(json.loads(REVIEW_SCHEMA.read_text())).validate(value)
    expected = {x['id'] for x in plan['acceptance_criteria']}
    observed = [x['id'] for x in value['acceptance_results']]
    if value['plan_id'] != identifier or len(set(observed)) != len(observed) or set(observed) != expected:
        raise ValueError('assessment does not cover the current plan exactly')
    return value
