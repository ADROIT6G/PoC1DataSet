from pathlib import Path
import hashlib

def sha256_file(path: Path) -> str:
    hash_obj = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

base = Path(__file__).resolve().parent.parent / 'Releases' / '1.0'
files = sorted(base.glob('recordings.7z.*'), key=lambda p: p.name)
if not files:
    raise SystemExit('No recordings archive parts found in Releases/1.0')

manifest = base / 'recordings_manifest.sha256'
with manifest.open('w', encoding='ascii') as out:
    out.write('# SHA256 checksums for recordings archive parts\n')
    out.write('# Format: <sha256> <filename>\n')
    out.write('# Generated for GitHub Release 1.0\n')
    for path in files:
        out.write(f'{sha256_file(path)} {path.name}\n')

print('Wrote', manifest)
