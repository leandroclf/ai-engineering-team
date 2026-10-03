#!/usr/bin/env python3
"""Real Docker mounts for four stages, offline and without provider credentials/inference."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
from local_team import provider_command, env_without_authority, STAGES, DEFAULT_MODELS


def main():
    image = os.environ.get('AI_TEAM_SMOKE_IMAGE', 'ai-eng-provider-cli:validation')
    with tempfile.TemporaryDirectory(prefix='ai-team-stages-') as tmp:
        root = Path(tmp); root.chmod(0o755)
        workspace = root / 'workspace'; workspace.mkdir(mode=0o755)
        metadata = workspace / '.git'; metadata.mkdir(mode=0o755)
        (metadata / 'marker').write_text('immutable'); (metadata / 'marker').chmod(0o666)
        marker = workspace / 'marker'; marker.write_text('original'); marker.chmod(0o666)
        for kind in STAGES:
            output = root / (kind + '-output'); output.mkdir(mode=0o777); output.chmod(0o777)
            handoff = root / (kind + '-input'); handoff.mkdir(mode=0o755)
            (handoff / 'marker').write_text('immutable'); (handoff / 'marker').chmod(0o444)
            config = dict(provider_image=image, models=DEFAULT_MODELS)
            cmd = provider_command(kind, 'ai-team-stage-canary-' + kind, config, workspace, output, 'unused', handoff)
            # Exercise production mount construction, replacing account volume with empty tmpfs.
            volume = next(i for i, value in enumerate(cmd) if '-home:/home/agent' in value)
            cmd[volume - 1:volume + 1] = ['--tmpfs', '/home/agent:uid=1001,gid=1001,mode=700']
            end = cmd.index(image)
            script = '''import os,pathlib
assert os.getuid() == 1001
assert not list(pathlib.Path('/home/agent').iterdir())
assert not pathlib.Path('/var/run/docker.sock').exists()
for filename in ('/work/.git/marker', '/handoff/marker'):
 try: pathlib.Path(filename).write_text('tampered')
 except OSError: pass
 else: raise AssertionError('unexpected write: '+filename)
try: pathlib.Path('/work/marker').write_text('changed')
except OSError:
 assert not IMPLEMENT
else:
 assert IMPLEMENT
pathlib.Path('/output/result.json').write_text('stage output')
'''.replace('IMPLEMENT', repr(kind == 'implement'))
            cmd = cmd[:end] + ['--network', 'none', image, 'python3', '-c', script]
            result = subprocess.run(cmd, text=True, capture_output=True, timeout=30, env=env_without_authority())
            if result.returncode:
                raise RuntimeError(kind + ': ' + result.stderr)
            assert (output / 'result.json').read_text() == 'stage output'
            assert marker.read_text() == ('changed' if kind == 'implement' else 'original')
            assert (metadata / 'marker').read_text() == 'immutable'
            marker.write_text('original')
    print(json.dumps(dict(status='PASS', stages=list(STAGES), live_provider=False,
                         boundary='Docker mounts only; native CLI sandbox/tool execution requires separate acceptance')))


if __name__ == '__main__':
    main()
