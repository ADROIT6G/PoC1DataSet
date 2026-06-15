param(
  [string]$tag = '1.0',
  [string]$releaseName = 'Release 1.0',
  [string]$releaseNotes = 'Recording archive assets for version 1.0',
  [string]$assetsDir = 'Releases/1.0'
)

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  Write-Error 'GitHub CLI (gh) is not installed. Install it from https://github.com/cli/cli and authenticate with gh auth login.'
  exit 1
}

$repo = git config --get remote.origin.url
if (-not $repo) {
  Write-Error 'No git remote origin configured.'
  exit 1
}

# Create release if missing
$release = gh release view $tag 2>$null
if ($LASTEXITCODE -ne 0) {
  gh release create $tag --title "$releaseName" --notes "$releaseNotes"
}

# Upload assets
Get-ChildItem -Path $assetsDir -File | ForEach-Object {
  Write-Host "Uploading $($_.Name)..."
  gh release upload $tag $_.FullName --clobber
}

Write-Host 'Upload finished. Verify assets in the GitHub release page.'
