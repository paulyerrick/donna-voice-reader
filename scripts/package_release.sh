#!/bin/bash
# Build Donna.app and package ZIP + DMG for GitHub Releases.
set -euo pipefail
cd "$(dirname "$0")/.."

VERSION="${1:-v0.1.0}"
# Strip leading 'v' for filenames if present
VER="${VERSION#v}"
OUT_DIR="release"
DMG_NAME="Donna-Voice-Reader-${VER}-macOS.dmg"
ZIP_NAME="Donna-Voice-Reader-${VER}-macOS.zip"

echo "==> Building Donna.app..."
./build_mac.sh

echo "==> Packaging..."
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

# ZIP (drag-and-drop install)
ditto -c -k --sequesterRsrc --keepParent "dist/Donna.app" "${OUT_DIR}/${ZIP_NAME}"

# DMG (standard macOS installer experience)
rm -f "${OUT_DIR}/${DMG_NAME}"
hdiutil create \
  -volname "Donna Voice Reader" \
  -srcfolder "dist/Donna.app" \
  -ov -format UDZO \
  "${OUT_DIR}/${DMG_NAME}"

echo ""
echo "Created:"
echo "  ${OUT_DIR}/${ZIP_NAME}"
echo "  ${OUT_DIR}/${DMG_NAME}"
ls -lh "${OUT_DIR}/"
