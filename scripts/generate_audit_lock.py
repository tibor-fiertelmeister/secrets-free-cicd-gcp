"""Generate a hash lock from reviewed CPython 3.12 wheel directories."""
import argparse
import hashlib
import re
from pathlib import Path
from zipfile import ZipFile
from email.parser import BytesParser


def inventory(directory):
    result = {}
    if not directory.is_dir():
        raise ValueError(f'Missing directory: {directory}')
    for wheel in sorted(directory.glob('*.whl')):
        with ZipFile(wheel) as archive:
            entries = [n for n in archive.namelist() if re.fullmatch(r'[^/]+\.dist-info/METADATA', n)]
            if len(entries) != 1:
                raise ValueError(f'Invalid metadata: {wheel.name}')
            meta = BytesParser().parsebytes(archive.read(entries[0]))
        name, version = meta.get('Name'), meta.get('Version')
        if not name or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', name) or not version or not re.fullmatch(r'[A-Za-z0-9.!+_-]+', version):
            raise ValueError(f'Invalid name/version: {wheel.name}')
        name = re.sub(r'[-_.]+', '-', name).lower()
        if name in result:
            raise ValueError(f'Duplicate package: {name} in {directory}')
        with wheel.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        result[name] = (version, digest)
    if not result:
        raise ValueError(f'No wheels: {directory}')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('windows', type=Path)
    parser.add_argument('linux', type=Path)
    parser.add_argument('--output', type=Path, default=Path('requirements-audit.txt'))
    parser.add_argument('--expected-count', type=int, required=True)
    args = parser.parse_args()
    win, linux = inventory(args.windows), inventory(args.linux)
    if win.keys() != linux.keys():
        raise ValueError(f'Package mismatch: Windows-only {sorted(win.keys()-linux.keys())}; Linux-only {sorted(linux.keys()-win.keys())}')
    if len(win) != args.expected_count:
        raise ValueError(f'Expected {args.expected_count} packages, found {len(win)}')
    lines = ['# Generated from reviewed Windows/Linux CPython 3.12 wheels.', '# Hashes verify integrity, not provenance or vulnerability status.']
    count = 0
    for name in sorted(win):
        version, digest = win[name]
        if version != linux[name][0]:
            raise ValueError(f'Version mismatch: {name}')
        hashes = sorted({digest, linux[name][1]})
        count += len(hashes)
        lines.append(f'{name}=={version}' + ''.join(f' --hash=sha256:{h}' for h in hashes))
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write('\n'.join(lines) + '\n')
    print(f'Generated {args.output}: {len(win)} packages, {count} unique per-package hashes')


if __name__ == '__main__':
    main()
