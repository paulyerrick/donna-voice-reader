#!/usr/bin/env python3
"""Generate Donna app icon via Higgsfield API.

Requires Higgsfield credentials (one of):
  export HF_KEY="your_key_id:your_key_secret"
  export HF_API_KEY=... HF_API_SECRET=...

Then:
  python scripts/generate_icon_higgsfield.py
"""

import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
OUT_PNG = os.path.join(ASSETS, "icon-1024.png")

PROMPT = (
    "macOS app icon, square 1024x1024. Deep black background #070709. "
    "Three thin luminous audio waveform lines flowing horizontally, glass glow. "
    "Gradient magenta #ff00aa, amber #ffaa00, cyan #00e5ff. "
    "Premium minimal voice reader app icon. No text. No letters. Clean modern."
)


def main():
    try:
        import higgsfield_client
    except ImportError:
        print("Install: pip install higgsfield-client")
        sys.exit(1)

    os.makedirs(ASSETS, exist_ok=True)

    result = higgsfield_client.subscribe(
        "bytedance/seedream/v4/text-to-image",
        arguments={
            "prompt": PROMPT,
            "resolution": "2K",
            "aspect_ratio": "1:1",
        },
    )

    url = result["images"][0]["url"]
    print(f"Downloading {url}")
    urllib.request.urlretrieve(url, OUT_PNG)
    print(f"Saved {OUT_PNG}")
    print("Run: ./scripts/build_icns.sh")


if __name__ == "__main__":
    main()
