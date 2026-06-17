# Release 1.0 - Recording Assets

This release contains the compressed recording archive parts for version `1.0`.

## Files included
- `recordings.7z.001`
- `recordings.7z.002`
- `recordings.7z.003`
- `recordings.7z.004`
- `merged_point_clouds.7z` (PLY files of merged point cloud)
- `renders.7z` (render images from virtual classroom viewpoints)
- `metadata.json` (dataset metadata file)
- `recordings_manifest.sha256` (SHA-256 checksums for recordings archive parts)
- `release_manifest.sha256` (SHA-256 checksums for all release assets)
- `skeleton/` (BVH and JSON skeleton files for teacher)

## Verification
Before extracting, verify each asset's checksum.

### Windows PowerShell
```powershell
Get-Content .\release_manifest.sha256 | ForEach-Object {
  $cols = $_ -split '\s+'; $expected=$cols[0]; $file=$cols[1]
  $actual=(Get-FileHash $file -Algorithm SHA256).Hash
  if ($actual -ne $expected) { Write-Error "MISMATCH: $file"; exit 1 } else { Write-Host "OK: $file" }
}
```

### Linux/macOS
```bash
sha256sum -c release_manifest.sha256
```

## Extraction
```powershell
# Extract recordings
7z x recordings.7z.001 -oRecordings
# Extract merged point clouds
7z x merged_point_clouds.7z -oPointClouds
# Extract renders
7z x renders.7z -oRenders
```

If the release assets are downloaded somewhere else, copy them into this directory before running the checksum verification.
