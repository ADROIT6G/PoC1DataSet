# Release 1.0 - Recording Assets

This release contains the compressed recording archive parts for version `1.0`.

## Files included
- `recordings.7z.001`
- `recordings.7z.002`
- `recordings.7z.003`
- `recordings.7z.004`
- `recordings_manifest.sha256`

## Verification
Before extracting, verify each part's checksum.

### Windows PowerShell
```powershell
Get-Content .\recordings_manifest.sha256 | ForEach-Object {
  $cols = $_ -split '\s+'; $expected=$cols[0]; $file=$cols[1]
  $actual=(Get-FileHash $file -Algorithm SHA256).Hash
  if ($actual -ne $expected) { Write-Error "MISMATCH: $file"; exit 1 } else { Write-Host "OK: $file" }
}
```

### Linux/macOS
```bash
sha256sum -c recordings_manifest.sha256
```

## Extraction
```powershell
7z x recordings.7z.001 -oRecordings
```

If the release assets are downloaded somewhere else, copy them into this directory before running the checksum verification.
