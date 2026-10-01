"""Required S04 check: production contract pins timeout to 30s."""
import json
import pathlib
import sys

cfg = json.loads((pathlib.Path(__file__).parent / "config.json").read_text())
if cfg.get("timeout") != 30:
    sys.exit(f"FAIL: timeout={cfg.get('timeout')} violates pinned contract (30)")
print("OK")
