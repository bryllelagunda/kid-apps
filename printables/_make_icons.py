"""Generate PWA icons for Printables.

Requires Pillow. If it isn't installed globally:

    python3 -m venv /tmp/iconvenv && /tmp/iconvenv/bin/pip install Pillow
    /tmp/iconvenv/bin/python printables/_make_icons.py

Icon concept: a worksheet page with dashed practice lines, and an orange
pencil laid across it. Palette matches the app's CSS custom properties.
"""
from PIL import Image, ImageDraw
import os

CREAM = (246, 243, 236)   # --cream
PAPER = (255, 255, 255)   # --paper
INK = (31, 36, 48)        # --ink
CRAYON = (255, 122, 69)   # --crayon
CRAYON_D = (232, 95, 41)  # --crayon-d
MUTED = (168, 161, 148)   # dashed guide lines


def dashed_line(draw, y, x0, x1, width, dash, gap, fill):
    """Horizontal dashed line from x0 to x1 at height y."""
    x = x0
    while x < x1:
        draw.line([(x, y), (min(x + dash, x1), y)], fill=fill, width=width)
        x += dash + gap


def create_icon(size, output_path, safe_zone_pct=0.0):
    """Render a single icon. safe_zone_pct pads content in from the edges
    so an OS mask (maskable icons) can't clip anything meaningful."""
    # Supersample 4x, then downscale — gives clean edges on the rotated pencil.
    S = size * 4
    img = Image.new('RGBA', (S, S), CREAM + (255,))
    draw = ImageDraw.Draw(img)

    pad = int(S * safe_zone_pct)
    content = S - 2 * pad
    border = max(2, int(S * 0.016))

    # ── The sheet of paper ──
    pw = int(content * 0.60)
    ph = int(content * 0.76)
    px = pad + (content - pw) // 2
    py = pad + (content - ph) // 2
    radius = int(S * 0.03)

    # Drop shadow
    sh = int(S * 0.018)
    draw.rounded_rectangle(
        [px + sh, py + sh, px + pw + sh, py + ph + sh],
        radius=radius, fill=(0, 0, 0, 45)
    )
    draw.rounded_rectangle(
        [px, py, px + pw, py + ph],
        radius=radius, fill=PAPER, outline=INK, width=border
    )

    # ── Practice lines on the page ──
    inset = int(pw * 0.13)
    lx0, lx1 = px + inset, px + pw - inset
    dash = int(pw * 0.09)
    gap = int(pw * 0.06)
    thin = max(2, int(S * 0.011))
    thick = max(3, int(S * 0.019))

    # Three writing bands: each is a solid baseline with a dashed midline above.
    band_top = py + int(ph * 0.20)
    band_step = int(ph * 0.24)
    for i in range(3):
        mid = band_top + i * band_step
        base = mid + int(band_step * 0.42)
        dashed_line(draw, mid, lx0, lx1, thin, dash, gap, MUTED)
        draw.line([(lx0, base), (lx1, base)], fill=INK, width=thick)

    # ── The pencil, laid diagonally across the lower right ──
    pen = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pen)

    body_w = int(S * 0.115)
    body_len = int(content * 0.72)
    cx, cy = S // 2, S // 2
    bx0 = cx - body_len // 2
    bx1 = cx + body_len // 2
    by0 = cy - body_w // 2
    by1 = cy + body_w // 2

    tip_len = int(body_w * 1.15)
    # Barrel
    pd.rounded_rectangle(
        [bx0 + tip_len, by0, bx1, by1],
        radius=int(body_w * 0.22), fill=CRAYON, outline=INK, width=border
    )
    # Ferrule band near the eraser end
    band_x = bx1 - int(body_len * 0.17)
    pd.rectangle([band_x, by0, band_x + int(body_w * 0.30), by1],
                 fill=CRAYON_D, outline=INK, width=border)
    # Sharpened tip
    pd.polygon(
        [(bx0, cy), (bx0 + tip_len, by0), (bx0 + tip_len, by1)],
        fill=PAPER, outline=INK
    )
    pd.line([(bx0, cy), (bx0 + tip_len, by0), (bx0 + tip_len, by1), (bx0, cy)],
            fill=INK, width=border, joint='curve')
    # Graphite point
    lead = int(tip_len * 0.36)
    pd.polygon(
        [(bx0, cy), (bx0 + lead, cy - int(body_w * 0.19)),
         (bx0 + lead, cy + int(body_w * 0.19))],
        fill=INK
    )

    pen = pen.rotate(-32, resample=Image.BICUBIC, center=(cx, cy))
    # Nudge the pencil down-right so the page's top lines stay readable.
    pen = pen.transform(
        pen.size, Image.AFFINE,
        (1, 0, -int(S * 0.055), 0, 1, -int(S * 0.10)),
        resample=Image.BICUBIC
    )
    img = Image.alpha_composite(img, pen)

    img = img.resize((size, size), Image.LANCZOS)
    img.save(output_path, 'PNG')
    print(f"Wrote {output_path} ({size}x{size})")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    create_icon(192, os.path.join(out_dir, "icon-192.png"))
    create_icon(512, os.path.join(out_dir, "icon-512.png"))
    create_icon(512, os.path.join(out_dir, "icon-maskable-512.png"), safe_zone_pct=0.10)
    create_icon(32, os.path.join(out_dir, "favicon-32.png"))
