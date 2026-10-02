#!/usr/bin/env python3
"""Unauthenticated, network-disabled container smoke; never starts a model task."""
import json
import sys
from preflight import probe

results = [probe(provider) for provider in ('codex', 'claude')]
print(json.dumps(results, indent=2))
# The fresh image must have compatible CLIs and no stored provider login.
sys.exit(0 if all(r['status'] == 'BLOCKED_PERMISSION' and r.get('version_matches_reviewed')
                 for r in results) else 1)
