#!/usr/bin/env python3
"""Build a full-bleed macOS dock icon (system applies the squircle mask at display)."""

import math
import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "icon-1024.png")
SIZE = 1024
BG = (7, 7, 9)

STRANDS = [
    {"color": (255, 0, 170), "phase": 0.0, "y_offset": -72, "amp": 58, "freq": 0.018},
    {"color": (255, 187, 0), "phase": 1.4, "y_offset": 0, "amp": 64, "freq": 0.016},
    {"color": (0, 229, 255), "phase": 2.8, "y_offset": 72, "amp": 58, "freq": 0.019},
]


def wave_points(strand):
    cx, cy = SIZE / 2, SIZE / 2 + strand["y_offset"]
    pts = []
    for x in range(SIZE):
        t = (x - cx) / SIZE
        env = max(0.0, 1.0 - abs(t) * 1.35) ** 1.6
        y = cy + math.sin(x * strand["freq"] + strand["phase"]) * strand["amp"] * env
        y += math.sin(x * strand["freq"] * 1.7 - strand["phase"] * 0.6) * strand["amp"] * 0.28 * env
        pts.append((x, y))
    return pts


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    canvas = Image.new("RGBA", (SIZE, SIZE), BG + (255,))
    glow_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    core_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    for strand in STRANDS:
        pts = wave_points(strand)
        r, g, b = strand["color"]
        ImageDraw.Draw(glow_layer).line(pts, fill=(r, g, b, 120), width=24, joint="curve")
        ImageDraw.Draw(core_layer).line(pts, fill=(r, g, b, 255), width=8, joint="curve")
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=16))
    canvas = Image.alpha_composite(canvas, glow_layer)
    canvas = Image.alpha_composite(canvas, core_layer)

    vignette = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(vignette).ellipse([120, 280, 904, 744], fill=(255, 255, 255, 18))
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=80))
    canvas = Image.alpha_composite(canvas, vignette)

    canvas.convert("RGB").save(OUT, "PNG")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
