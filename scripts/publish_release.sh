#!/bin/bash
# Package Donna and publish to GitHub Releases (requires: gh auth login).
set -euo pipefail
cd "$(dirname "$0")/.."

VERSION="${1:-v0.2.0}"
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

1. Download **Donna-Voice-Reader-${VER}-macOS.dmg** (recommended) or the ZIP below.
2. Open the DMG and drag **Donna** to **Applications**.
3. First launch: right-click Donna, choose **Open**, then **Open** again (unsigned app).

## What's new in ${VER}

- **Local offline voices** — Kokoro-82M bundled; no API key needed for default playback
- **Reactive fluid background** — audio-reactive WebGL themes (Donna, Ocean, Sunset, Forest, Mono)
- **Cloud providers** — optional OpenAI, ElevenLabs, and Cartesia API keys in Settings
- **Updated app icon** and glass UI polish

## Requirements

- macOS 13 or later
- ~700 MB download; ~1.2 GB installed (includes local TTS model)
- API keys only if you use cloud providers

## Files

- Donna-Voice-Reader-${VER}-macOS.dmg — recommended installer
- Donna-Voice-Reader-${VER}-macOS.zip — same app bundle, zip format
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
