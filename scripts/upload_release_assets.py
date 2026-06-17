from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'Releases' / '1.0'
REPO = 'ADROIT6G/PoC1DataSet'
TAG = '1.0'

GH_PATHS = [
    Path(r'C:/Program Files/GitHub CLI/gh.exe'),
    Path(r'C:/Program Files (x86)/GitHub CLI/gh.exe')
]

def find_gh():
    for path in GH_PATHS:
        if path.exists():
            return path
    gh = shutil.which('gh')
    if gh:
        return Path(gh)
    return None


def run(cmd, **kwargs):
    proc = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    return proc


def main():
    gh = find_gh()
    if gh is None:
        print('GitHub CLI not found. Install gh or add it to PATH.', file=sys.stderr)
        return 1

    if not BASE.exists():
        print(f'Release directory not found: {BASE}', file=sys.stderr)
        return 1

    all_files = sorted(p for p in BASE.rglob('*') if p.is_file() and p.name != 'README.md')
    if not all_files:
        print('No files found to upload.', file=sys.stderr)
        return 1

    proc = run([str(gh), 'release', 'view', TAG, '--repo', REPO, '--json', 'assets'])
    if proc.returncode != 0:
        print('Failed to query release assets:', proc.stderr.strip(), file=sys.stderr)
        return proc.returncode

    existing = set()
    try:
        import json
        data = json.loads(proc.stdout)
        existing = {asset['name'] for asset in data.get('assets', [])}
    except Exception as exc:
        print('Failed to parse release view output:', exc, file=sys.stderr)
        print(proc.stdout, file=sys.stderr)
        return 1

    missing = [p for p in all_files if p.name not in existing]
    print(f'Found {len(all_files)} local files, {len(missing)} missing from release.')
    for p in missing:
        print('Uploading', p.relative_to(ROOT))
        upload = run([str(gh), 'release', 'upload', TAG, str(p), '--repo', REPO, '--clobber'])
        if upload.stdout:
            print(upload.stdout.strip())
        if upload.stderr:
            print(upload.stderr.strip(), file=sys.stderr)
        if upload.returncode != 0:
            print(f'Upload failed for {p.name} (exit {upload.returncode})', file=sys.stderr)
            return upload.returncode

    proc = run([str(gh), 'release', 'view', TAG, '--repo', REPO, '--json', 'assets'])
    if proc.returncode != 0:
        print('Failed to query final assets:', proc.stderr.strip(), file=sys.stderr)
        return proc.returncode
    print('Final release assets:')
    print(proc.stdout.strip())
    return 0


if __name__ == '__main__':
    import shutil
    sys.exit(main())
