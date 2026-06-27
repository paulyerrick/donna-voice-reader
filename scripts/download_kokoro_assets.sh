#!/bin/bash
# Download Kokoro model + curated voices into assets/kokoro for bundling in Donna.app
set -euo pipefail
cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python3}"
if [ -x "venv/bin/python" ]; then
  PYTHON="venv/bin/python"
fi

DEST="assets/kokoro"
VOICES=(af_heart af_bella am_adam am_michael bf_emma)

mkdir -p "$DEST/voices"

"$PYTHON" - <<'PY'
import os
from huggingface_hub import hf_hub_download

repo = "hexgrad/Kokoro-82M"
dest = "assets/kokoro"
os.makedirs(f"{dest}/voices", exist_ok=True)

for name in ("config.json", "kokoro-v1_0.pth"):
    path = hf_hub_download(repo_id=repo, filename=name)
    target = os.path.join(dest, name)
    if os.path.lexists(target):
        os.remove(target)
    os.link(path, target) if hasattr(os, "link") else open(target, "wb").write(open(path, "rb").read())
    print(f"Ready {target}")

for voice in ["af_heart", "af_bella", "am_adam", "am_michael", "bf_emma"]:
    path = hf_hub_download(repo_id=repo, filename=f"voices/{voice}.pt")
    target = os.path.join(dest, "voices", f"{voice}.pt")
    if os.path.lexists(target):
        os.remove(target)
    try:
        os.link(path, target)
    except OSError:
        open(target, "wb").write(open(path, "rb").read())
    print(f"Ready {target}")
PY

echo ""
du -sh "$DEST" "$DEST/kokoro-v1_0.pth"
echo "Kokoro assets ready in $DEST"
