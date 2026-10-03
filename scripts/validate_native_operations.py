#!/usr/bin/env python3
"""Validate versioned schemas and the concrete delegation example."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from dot_contracts import validate

ROOT = Path(__file__).resolve().parents[1]


def main():
    schemas = sorted((ROOT / 'schemas').glob('*.schema.json'))
    required = {'authorization-lease', 'authorization-state', 'dot-codex-task', 'execution-evidence', 'provider-review',
                'local-plan', 'local-implementation', 'local-review'}
    if {p.name.removesuffix('.schema.json') for p in schemas} != required:
        raise ValueError('native-operation/review schema inventory mismatch')
    for path in schemas:
        Draft202012Validator.check_schema(json.loads(path.read_text()))
    for kind in ['dot-codex-task', 'authorization-state']:
        validate(kind, json.loads((ROOT / 'validation/examples' / f'{kind}.json').read_text()))
    print(f'OK: {len(schemas)} JSON schemas and concrete task/state examples validated (repository layer only)')


if __name__ == '__main__': main()
