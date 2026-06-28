#!/usr/bin/env python3
"""Build a macOS dock icon matching the Donna UI nav logo."""

import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "icon-1024.png")
SIZE = 1024
BG = (7, 7, 9)

ACCENT1 = (255, 0, 170)   # #ff00aa
ACCENT2 = (0, 229, 255)   # #00e5ff


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def rounded_rect_mask(size, box, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius, fill=255)
    return mask


def gradient_rounded_rect(size, box, radius, c1, c2):
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    width = max(x1 - x0, 1)
    for x in range(x0, x1):
        t = (x - x0) / (width - 1) if width > 1 else 0
        draw.line([(x, y0), (x, y1)], fill=lerp_color(c1, c2, t) + (255,))
    mask = rounded_rect_mask(size, box, radius)
    layer.putalpha(mask)
    return layer


def draw_soundwave(size, box, bar_heights, bar_width, gap, color=(255, 255, 255, 240)):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    max_h = (y1 - y0) * 0.62
    total_w = len(bar_heights) * bar_width + (len(bar_heights) - 1) * gap
    start_x = cx - total_w / 2
    for i, h in enumerate(bar_heights):
        bh = max_h * h
        bx0 = start_x + i * (bar_width + gap)
        bx1 = bx0 + bar_width
        by0 = cy - bh / 2
        by1 = cy + bh / 2
        draw.rounded_rectangle([bx0, by0, bx1, by1], radius=bar_width / 2, fill=color)
    return layer


def ambient_glow(size):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse([80, 180, 560, 660], fill=(255, 0, 170, 42))
    draw.ellipse([464, 364, 944, 844], fill=(0, 229, 255, 36))
    return layer.filter(ImageFilter.GaussianBlur(radius=90))


def glass_highlight(size, box, radius):
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    inset = radius * 0.18
    draw.rounded_rectangle(
        [x0 + inset, y0 + inset, x1 - inset, y0 + (y1 - y0) * 0.42],
        radius=radius * 0.55,
        fill=(255, 255, 255, 38),
    )
    mask = rounded_rect_mask(size, box, radius)
    return Image.composite(
        layer, Image.new("RGBA", size, (0, 0, 0, 0)), mask
    ).filter(ImageFilter.GaussianBlur(radius=6))


def outer_glow(size, box, radius):
    glow = gradient_rounded_rect(size, box, radius, ACCENT1, ACCENT2)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=28))
    alpha = glow.split()[3].point(lambda a: int(a * 0.55))
    glow.putalpha(alpha)
    return glow


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    dim = (SIZE, SIZE)

    canvas = Image.new("RGBA", dim, BG + (255,))
    canvas = Image.alpha_composite(canvas, ambient_glow(dim))

    logo_size = 620
    margin = (SIZE - logo_size) // 2
    box = (margin, margin, margin + logo_size, margin + logo_size)
    radius = int(logo_size * 0.28)

    canvas = Image.alpha_composite(canvas, outer_glow(dim, box, radius))
    canvas = Image.alpha_composite(canvas, gradient_rounded_rect(dim, box, radius, ACCENT1, ACCENT2))
    canvas = Image.alpha_composite(canvas, glass_highlight(dim, box, radius))

    wave_box = (box[0] + 130, box[1] + 130, box[2] - 130, box[3] - 130)
    canvas = Image.alpha_composite(
        canvas,
        draw_soundwave(dim, wave_box, [0.38, 0.72, 1.0, 0.58, 0.34], bar_width=34, gap=24),
    )

    vignette = Image.new("RGBA", dim, (0, 0, 0, 0))
    ImageDraw.Draw(vignette).ellipse([0, 0, SIZE, SIZE], fill=(0, 0, 0, 0))
    for i, alpha in enumerate(range(0, 90, 3)):
        inset = i * 5
        ImageDraw.Draw(vignette).rectangle(
            [inset, inset, SIZE - inset, SIZE - inset],
            outline=(7, 7, 9, min(alpha, 80)),
            width=8,
        )
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=18))
    canvas = Image.alpha_composite(canvas, vignette)

    canvas.convert("RGB").save(OUT, "PNG")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
