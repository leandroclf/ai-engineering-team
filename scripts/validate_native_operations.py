#!/usr/bin/env python3
"""Validate versioned schemas and the concrete delegation example."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from dot_contracts import validate

ROOT = Path(__file__).resolve().parents[1]


def main():
    schemas = sorted((ROOT / 'schemas').glob('*.schema.json'))
    if len(schemas) != 4:
        raise ValueError('expected four native-operation schemas')
    for path in schemas:
        Draft202012Validator.check_schema(json.loads(path.read_text()))
    for kind in ['dot-codex-task', 'authorization-state']:
        validate(kind, json.loads((ROOT / 'validation/examples' / f'{kind}.json').read_text()))
    print('OK: four JSON schemas and concrete task/state examples validated (repository layer only)')


if __name__ == '__main__': main()
