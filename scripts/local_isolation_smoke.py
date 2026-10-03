#!/usr/bin/env python3
"""Real offline container canary; no provider execution or account login."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
from local_team import test_command

with tempfile.TemporaryDirectory(prefix='ai-team-canary-') as tmp:
    source = Path(tmp) / 'source'
    source.mkdir(mode=0o755)
    (source / 'marker').write_text('original')
    command = '''python3 -c 'import os,socket,pathlib
assert not any(k in os.environ for k in ("GH_TOKEN","GITHUB_TOKEN","OPENAI_API_KEY","ANTHROPIC_API_KEY"))
assert not pathlib.Path("/var/run/docker.sock").exists()
assert not pathlib.Path("/home/agent/.codex/auth.json").exists()
assert not pathlib.Path("/home/agent/.claude/.credentials.json").exists()
assert os.getuid() != 0
pathlib.Path("marker").write_text("changed only in tmpfs")
try:
 socket.create_connection(("1.1.1.1",443),timeout=1)
except OSError:
 pass
else:
 raise AssertionError("unexpected outbound connection")
print("offline credential-free boundary PASS")' '''
    config = {'test_image': os.environ.get('AI_TEAM_SMOKE_IMAGE', 'ai-eng-provider-cli:validation'), 'checks': [command]}
    cmd = test_command('ai-team-offline-canary', config, source)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    print(result.stdout)
    if result.returncode:
        print(result.stderr)
        raise SystemExit(result.returncode)
    assert (source / 'marker').read_text() == 'original'
    print(json.dumps({'status': 'PASS', 'source_unchanged': True, 'live_provider': False}))
