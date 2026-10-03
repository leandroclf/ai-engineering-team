"""Check repository Markdown local targets and closed fences, without network access.

This is a bounded Markdown check, not a full renderer or an external URL validator.
Consolidated requirement identifiers/anchors have a separate verifier.
"""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


def check_file(path, root):
    errors = []
    prose = []
    fence = None
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
        if marker:
            token, tail = marker.groups()
            if fence is None:
                fence = (token[0], len(token), number)
            elif token[0] == fence[0] and len(token) >= fence[1] and not tail.strip():
                fence = None
            continue
        if fence is None:
            # Inline code contains examples, not actual links.
            prose.append(re.sub(r'`+[^`]*`+', '', line))
    if fence:
        errors.append(f'{path.relative_to(root)}:{fence[2]}: unclosed code fence')
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', '\n'.join(prose)):
        target = target.strip().split(' "', 1)[0].strip('<>')
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        destination = (path.parent / unquote(parsed.path)).resolve()
        if not destination.is_relative_to(root.resolve()):
            errors.append(f'{path.relative_to(root)}: target outside repository: {target}')
        elif not destination.exists():
            errors.append(f'{path.relative_to(root)}: missing local target: {target}')
    return errors


def main():
    paths = [ROOT / 'README.md', ROOT / 'AGENTS.md']
    for directory in ('docs', 'runbooks', 'templates', 'openspec'):
        paths.extend(sorted((ROOT / directory).rglob('*.md')))
    errors = [error for path in paths for error in check_file(path, ROOT)]
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'OK: {len(paths)} Markdown documents; local link targets and code fences verified')
    return 0


if __name__ == '__main__':
    sys.exit(main())
