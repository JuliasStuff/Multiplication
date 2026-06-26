#!/usr/bin/env python3
"""
Generate Multiplication Quest PWA icons (icon-192.png, icon-512.png).
Requires Pillow:  pip install Pillow

Run from the Multiplication folder:  python generate_icons.py

Styled to match Spelling Quest's icon: dark navy rounded square, two large
letters in the app's accent color, with a gold motif in the middle. Here the
motif is a thick multiplication "x" instead of Spelling Quest's star arrow.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys


# ── Theme (matches Multiplication Quest CSS variables) ─────────────
BG_COLOR     = "#0b0f1f"   # --bg
LETTER_COLOR = "#a78bfa"   # --accent (purple)
ACCENT_COLOR = "#facc15"   # --gold (for the × motif)


def find_font(size: int) -> ImageFont.FreeTypeFont:
    """Try several common bold fonts; fall back to Pillow's default."""
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/consolab.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVu-Sans-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_x(draw: ImageDraw.ImageDraw, cx: float, cy: float,
           arm: float, thickness: float, color: str) -> None:
    """Draw a thick multiplication × using two rotated rectangles."""
    # Build a horizontal thick bar, rotate it, paste it twice.
    # Easier: draw two diagonal polygons.
    half_t = thickness / 2

    # Diagonal 1: top-left → bottom-right
    poly1 = [
        (cx - arm - half_t,  cy - arm + half_t),
        (cx - arm + half_t,  cy - arm - half_t),
        (cx + arm + half_t,  cy + arm - half_t),
        (cx + arm - half_t,  cy + arm + half_t),
    ]
    # Diagonal 2: top-right → bottom-left
    poly2 = [
        (cx + arm - half_t,  cy - arm - half_t),
        (cx + arm + half_t,  cy - arm + half_t),
        (cx - arm + half_t,  cy + arm + half_t),
        (cx - arm - half_t,  cy + arm - half_t),
    ]
    draw.polygon(poly1, fill=color)
    draw.polygon(poly2, fill=color)


def make_icon(size: int) -> None:
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ── Rounded-square dark navy background ────────────────────────
    radius = size // 6
    draw.rounded_rectangle(
        [0, 0, size - 1, size - 1],
        radius=radius,
        fill=BG_COLOR,
    )

    cx, cy = size / 2, size / 2

    # ── Letters M and Q on either side ─────────────────────────────
    font_px = int(size * 0.56)
    font    = find_font(font_px)

    # Push the letters farther apart so the × has clean room in between.
    offset_x = size * 0.30
    y_letter = cy + size * 0.02

    draw.text(
        (cx - offset_x, y_letter),
        "M",
        font=font,
        fill=LETTER_COLOR,
        anchor="mm",
    )
    draw.text(
        (cx + offset_x, y_letter),
        "Q",
        font=font,
        fill=LETTER_COLOR,
        anchor="mm",
    )

    # ── Gold × in the middle ───────────────────────────────────────
    # Smaller, slimmer × that sits in the gap rather than swallowing letters.
    arm       = size * 0.14
    thickness = size * 0.055
    draw_x(draw, cx, cy, arm, thickness, ACCENT_COLOR)

    path = f"icon-{size}.png"
    img.save(path)
    print(f"  Created {path}  ({size}x{size})")


def make_favicon_ico() -> None:
    """Create favicon.ico containing 16, 32, and 48 px variants."""
    # Render at a larger size and downsample for crisp small icons.
    base = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)

    size = 256
    radius = size // 6
    draw.rounded_rectangle(
        [0, 0, size - 1, size - 1],
        radius=radius,
        fill=BG_COLOR,
    )

    cx, cy = size / 2, size / 2
    font_px = int(size * 0.56)
    font = find_font(font_px)

    offset_x = size * 0.30
    y_letter = cy + size * 0.02

    draw.text((cx - offset_x, y_letter), "M", font=font,
              fill=LETTER_COLOR, anchor="mm")
    draw.text((cx + offset_x, y_letter), "Q", font=font,
              fill=LETTER_COLOR, anchor="mm")

    arm       = size * 0.14
    thickness = size * 0.055
    draw_x(draw, cx, cy, arm, thickness, ACCENT_COLOR)

    sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    # Save individual PNGs for direct <link rel="icon"> use.
    for w, _ in [(16, 16), (32, 32)]:
        resized = base.resize((w, w), Image.LANCZOS)
        resized.save(f"favicon-{w}.png")
        print(f"  Created favicon-{w}.png  ({w}x{w})")

    base.save("favicon.ico", format="ICO", sizes=sizes)
    print("  Created favicon.ico  (16/32/48/64)")


def main() -> int:
    print("Generating Multiplication Quest icons...")
    make_icon(192)
    make_icon(512)
    make_favicon_ico()
    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
