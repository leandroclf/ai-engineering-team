#!/usr/bin/env python3
"""Read-only CLI capability probe. Authentication output is reduced to a status."""
import json
import shutil
import subprocess
import sys


def probe(executable="codex"):
    path = shutil.which(executable)
    if not path:
        return {"status": "UNAVAILABLE", "reason": "Codex CLI not installed", "authenticated": False}
    try:
        version = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
        auth = subprocess.run([path, "login", "status"], capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired):
        return {"status": "UNAVAILABLE", "reason": "CLI probe failed/timed out", "authenticated": False}
    if version.returncode:
        return {"status": "INCOMPATIBLE", "reason": "version probe failed", "authenticated": False}
    authenticated = auth.returncode == 0
    # Version/auth capability only: no task, shell or cloud delegation has been tested.
    return {"status": "INCONCLUSIVE" if authenticated else "BLOCKED_PERMISSION",
            "reason": "execution/delegation still requires a controlled real scenario" if authenticated else "CLI login unavailable",
            "authenticated": authenticated}


if __name__ == "__main__":
    result = probe()
    print(json.dumps(result))
    sys.exit(0 if result["authenticated"] else 2)
