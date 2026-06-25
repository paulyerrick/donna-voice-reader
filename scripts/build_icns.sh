#!/bin/bash
# Build macOS .icns from assets/icon-1024.png
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/make_dock_icon.py

SRC="assets/icon-1024.png"
ICONSET="assets/Donna.iconset"
OUT="assets/Donna.icns"

if [ ! -f "$SRC" ]; then
  echo "Missing $SRC — run generate_icon_higgsfield.py or place a 1024x1024 PNG there."
  exit 1
fi

rm -rf "$ICONSET"
mkdir -p "$ICONSET"

sips -z 16 16 "$SRC" --out "$ICONSET/icon_16x16.png"
sips -z 32 32 "$SRC" --out "$ICONSET/icon_16x16@2x.png"
sips -z 32 32 "$SRC" --out "$ICONSET/icon_32x32.png"
sips -z 64 64 "$SRC" --out "$ICONSET/icon_32x32@2x.png"
sips -z 128 128 "$SRC" --out "$ICONSET/icon_128x128.png"
sips -z 256 256 "$SRC" --out "$ICONSET/icon_128x128@2x.png"
sips -z 256 256 "$SRC" --out "$ICONSET/icon_256x256.png"
sips -z 512 512 "$SRC" --out "$ICONSET/icon_256x256@2x.png"
sips -z 512 512 "$SRC" --out "$ICONSET/icon_512x512.png"
sips -z 1024 1024 "$SRC" --out "$ICONSET/icon_512x512@2x.png"

iconutil -c icns "$ICONSET" -o "$OUT"
rm -rf "$ICONSET"
echo "Created $OUT"
