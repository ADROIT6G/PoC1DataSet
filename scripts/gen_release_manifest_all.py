from pathlib import Path
import hashlib

base = Path(__file__).resolve().parent.parent / 'Releases' / '1.0'
if not base.exists():
    raise SystemExit('Releases/1.0 not found')

def sha256_file(p:Path):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

patterns = ['*.7z','*.7z.*','*.json','*.md']
files = []
for p in sorted(base.rglob('*')):
    if p.is_file():
        # include common asset files; skip hidden/tmp
        files.append(p)

manifest = base / 'release_manifest.sha256'
with manifest.open('w', encoding='ascii') as out:
    out.write('# SHA256 checksums for all release assets\n')
    out.write('# Format: <sha256> <relative-path>\n')
    for p in sorted(files):
        rel = p.relative_to(base)
        out.write(f"{sha256_file(p)} {rel.as_posix()}\n")

print('Wrote', manifest)
