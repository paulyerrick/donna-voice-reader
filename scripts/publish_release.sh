#!/bin/bash
# Package Donna and publish to GitHub Releases (requires: gh auth login).
set -euo pipefail
cd "$(dirname "$0")/.."

VERSION="${1:-v0.1.0}"
VER="${VERSION#v}"
REPO="paulyerrick/donna-voice-reader"

if ! command -v gh >/dev/null 2>&1; then
  echo "Install GitHub CLI: brew install gh"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Not logged into GitHub. Run: gh auth login"
  exit 1
fi

./scripts/package_release.sh "$VERSION"

ZIP="release/Donna-Voice-Reader-${VER}-macOS.zip"
DMG="release/Donna-Voice-Reader-${VER}-macOS.dmg"

NOTES="$(cat <<EOF
## Install

1. Download **Donna-Voice-Reader-${VER}-macOS.dmg** (or the ZIP).
2. Open the DMG and drag **Donna** to Applications.
3. First launch: right-click Donna → **Open** → **Open** (unsigned app).

## Requirements

- macOS (Apple Silicon build)
- API key for OpenAI, ElevenLabs, or Cartesia (Settings in the app)

## Files

- \`Donna-Voice-Reader-${VER}-macOS.dmg\` — recommended
- \`Donna-Voice-Reader-${VER}-macOS.zip\` — same app, zip format
EOF
)"

echo "==> Creating GitHub release ${VERSION}..."
gh release create "$VERSION" \
  --repo "$REPO" \
  --title "Donna Voice Reader ${VER}" \
  --notes "$NOTES" \
  "$ZIP" \
  "$DMG"

echo ""
echo "Published: https://github.com/${REPO}/releases/tag/${VERSION}"
