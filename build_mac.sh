#!/bin/bash
# Build Donna.app for macOS (double-clickable, no Python required for users)
set -euo pipefail
cd "$(dirname "$0")"

pick_python() {
  local candidates=(
    /opt/homebrew/opt/python@3.12/bin/python3.12
    /opt/homebrew/opt/python@3.11/bin/python3.11
    /usr/local/opt/python@3.12/bin/python3.12
    /usr/local/opt/python@3.11/bin/python3.11
    python3.12
    python3.11
    python3
  )
  for candidate in "${candidates[@]}"; do
    if [ -x "$candidate" ] || command -v "$candidate" >/dev/null 2>&1; then
      local py="$candidate"
      if "$py" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if (3, 10) <= sys.version_info[:2] < (3, 13) else 1)
PY
      then
        echo "$py"
        return 0
      fi
    fi
  done
  return 1
}

PYTHON="$(pick_python || true)"
if [ -z "$PYTHON" ]; then
  echo "Python 3.10–3.12 is required for Kokoro local voices."
  echo "Install with: brew install python@3.12"
  exit 1
fi

PY_ARCH=$("$PYTHON" -c 'import platform; print(platform.machine())')
if [ "$PY_ARCH" = "arm64" ]; then
  TARGET_ARCH=arm64
else
  TARGET_ARCH=x86_64
fi

echo "Using Python: $PYTHON ($PY_ARCH, target $TARGET_ARCH)"

if [ -d "venv" ]; then
  venv_arch=$(file venv/bin/python 2>/dev/null | grep -oE 'arm64|x86_64' | head -1 || true)
  venv_py=$("venv/bin/python" - <<'PY' 2>/dev/null || echo 0
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
PY
)
  want_py=$("$PYTHON" - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
PY
)
  if [ -n "$venv_arch" ] && { [ "$venv_arch" != "$PY_ARCH" ] || [ "$venv_py" != "$want_py" ]; }; then
    echo "Recreating venv ($venv_arch python$venv_py -> $PY_ARCH python$want_py)..."
    rm -rf venv
  fi
fi

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  "$PYTHON" -m venv venv
fi

source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "Downloading bundled Kokoro model assets..."
chmod +x scripts/download_kokoro_assets.sh
./scripts/download_kokoro_assets.sh

echo "Building Donna.app for $TARGET_ARCH..."
rm -rf build dist

./scripts/build_icns.sh

pyinstaller --noconfirm --clean Donna.spec

echo ""
du -sh dist/Donna.app
echo ""
echo "Done! Install with:"
echo "  open dist/Donna.app"
echo "Or copy to Applications:"
echo "  cp -R dist/Donna.app /Applications/"
