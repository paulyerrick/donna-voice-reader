#!/bin/bash
# Build Donna.app for macOS (double-clickable, no Python required for users)
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo "Building Donna.app..."
rm -rf build dist

./scripts/build_icns.sh

pyinstaller --noconfirm --clean Donna.spec

echo ""
echo "Done! Install with:"
echo "  open dist/Donna.app"
echo "Or copy to Applications:"
echo "  cp -R dist/Donna.app /Applications/"
