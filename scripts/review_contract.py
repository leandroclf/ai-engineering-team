"""Strict provider review format. Provider output constrains syntax, not truth."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parents[1] / 'schemas/provider-review.schema.json'


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def read_json(text):
    return json.loads(text, object_pairs_hook=unique_object)


def validate_review(value):
    Draft202012Validator(json.loads(SCHEMA_PATH.read_text())).validate(value)
    return value
