# PoC1DataSet

This repository contains the source and metadata for the `PoC1DataSet` project.

## Large recording files
The actual recording data is stored as split archive assets in GitHub Releases rather than in the Git repository.

Release assets are available under the `1.0` release and include:
- `recordings.7z.001`
- `recordings.7z.002`
- `recordings.7z.003`
- `recordings.7z.004`
- `merged_point_clouds.7z`
- `renders.7z`
- `metadata.json`
- `recordings_manifest.sha256`
- `release_manifest.sha256`
- `camera0_skeleton.bvh`
- `camera0_skeleton.json`
- `camera1_skeleton.bvh`
- `camera1_skeleton.json`
- `camera2_skeleton.bvh`
- `camera2_skeleton.json`

## Download and verify recordings
1. Download all assets from the release (in `Releases/1.0`):
  - `recordings.7z.001`
  - `recordings.7z.002`
  - `recordings.7z.003`
  - `recordings.7z.004`
  - `merged_point_clouds.7z`
  - `renders.7z`
  - `skeleton/` (skeleton files in BVH/JSON formats)
  - `release_manifest.sha256` (checksums for all release assets)

2. Verify checksums before extraction.

### Windows (PowerShell)
```powershell
Get-Content .\Releases\1.0\release_manifest.sha256 | ForEach-Object {
  $cols = $_ -split '\s+'; $expected=$cols[0]; $file=$cols[1]
  $actual=(Get-FileHash (Join-Path '.\Releases\1.0' $file) -Algorithm SHA256).Hash
  if ($actual -ne $expected) { Write-Error "MISMATCH: $file"; exit 1 } else { Write-Host "OK: $file" }
}
```

### Linux/macOS
```bash
sha256sum -c Releases/1.0/release_manifest.sha256
```

3. Extract assets:
```powershell
# Extract recordings
7z x Releases\1.0\recordings.7z.001 -oReleases\1.0\Recordings
# Extract merged point clouds
7z x Releases\1.0\merged_point_clouds.7z -oReleases\1.0\PointClouds
# Extract renders
7z x Releases\1.0\renders.7z -oReleases\1.0\Renders
```

## Notes
- If GitHub Release upload fails due to asset size limits, use smaller parts.
- The repo tracks only metadata and release instructions; the actual data assets are in GitHub Releases.
