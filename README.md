# PoC1DataSet

This repository contains the source and metadata for the `PoC1DataSet` project.

## Large recording files
The actual recording data is stored as split archive assets in GitHub Releases rather than in the Git repository.

Release assets are available under the `1.0` release.

## Download and verify recordings
1. Download all parts from the release:
   - `recordings.7z.001`
   - `recordings.7z.002`
   - `recordings.7z.003`
   - `recordings.7z.004`
   - `recordings_manifest.sha256`

2. Verify checksums before extraction.

### Windows (PowerShell)
```powershell
Get-Content .\Releases\1.0\recordings_manifest.sha256 | ForEach-Object {
  $cols = $_ -split '\s+'; $expected=$cols[0]; $file=$cols[1]
  $actual=(Get-FileHash $file -Algorithm SHA256).Hash
  if ($actual -ne $expected) { Write-Error "MISMATCH: $file"; exit 1 } else { Write-Host "OK: $file" }
}
```

### Linux/macOS
```bash
sha256sum -c Releases/1.0/recordings_manifest.sha256
```

3. Extract the recordings:
```powershell
7z x Releases\1.0\recordings.7z.001 -oReleases\1.0\Recordings
```

## Notes
- If GitHub Release upload fails due to asset size limits, use smaller parts.
- The repo tracks only metadata and release instructions; the actual data assets are in GitHub Releases.
