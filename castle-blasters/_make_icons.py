"""Generate PWA icons for Castle Blasters.

Pure standard library (zlib + struct) — no Pillow, no pip, nothing to install.
Crane Stacker's version needs Pillow; this one deliberately does not, so the
icons can be regenerated on any machine that has python3.

Run:  python3 castle-blasters/_make_icons.py
"""

import os
import struct
import zlib

# Palette — DESIGN.md slot 2 (golden yellow) is this game's permanent colour.
GOLD = (255, 215, 0)      # #ffd700  background
WOOD = (217, 160, 91)     # #d9a05b  castle blocks
INK = (42, 26, 10)        # #2a1a0a  borders
CREAM = (255, 248, 231)   # #fff8e7
BALL = (74, 74, 82)       # projectile

SS = 4  # supersample factor, box-downsampled for antialiasing


class Canvas:
    """Tiny RGB raster target with the handful of primitives the icon needs."""

    def __init__(self, size, bg):
        self.n = size
        self.px = bytearray(bg * (size * size))

    def _set(self, x, y, rgb):
        if 0 <= x < self.n and 0 <= y < self.n:
            i = (y * self.n + x) * 3
            self.px[i:i + 3] = bytes(rgb)

    def rect(self, x0, y0, x1, y1, rgb):
        x0, x1 = int(min(x0, x1)), int(max(x0, x1))
        y0, y1 = int(min(y0, y1)), int(max(y0, y1))
        for y in range(max(0, y0), min(self.n, y1)):
            i = (y * self.n + max(0, x0)) * 3
            span = (min(self.n, x1) - max(0, x0))
            if span > 0:
                self.px[i:i + span * 3] = bytes(rgb) * span

    def rect_outlined(self, x0, y0, x1, y1, fill, border, bw):
        self.rect(x0, y0, x1, y1, border)
        self.rect(x0 + bw, y0 + bw, x1 - bw, y1 - bw, fill)

    def disc(self, cx, cy, r, rgb):
        r2 = r * r
        for y in range(int(cy - r), int(cy + r) + 1):
            dy = y - cy
            for x in range(int(cx - r), int(cx + r) + 1):
                dx = x - cx
                if dx * dx + dy * dy <= r2:
                    self._set(x, y, rgb)

    def downsample(self, factor):
        n = self.n // factor
        out = bytearray(n * n * 3)
        inv = 1.0 / (factor * factor)
        for y in range(n):
            for x in range(n):
                r = g = b = 0
                for sy in range(factor):
                    base = ((y * factor + sy) * self.n + x * factor) * 3
                    for sx in range(factor):
                        i = base + sx * 3
                        r += self.px[i]
                        g += self.px[i + 1]
                        b += self.px[i + 2]
                o = (y * n + x) * 3
                out[o] = int(r * inv)
                out[o + 1] = int(g * inv)
                out[o + 2] = int(b * inv)
        return n, out


def write_png(path, size, rgb_bytes):
    raw = bytearray()
    stride = size * 3
    for y in range(size):
        raw.append(0)  # filter type 0 (None)
        raw += rgb_bytes[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data
                + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)


def create_icon(size, output_path, safe_zone_pct=0.0):
    """A castle with battlements and a cannonball on its way in."""
    n = size * SS
    c = Canvas(n, GOLD)

    pad = int(n * safe_zone_pct)
    area = n - 2 * pad

    def u(v):
        """Fraction of the content area -> absolute pixels."""
        return pad + v * area

    bw = max(SS, int(area * 0.028))  # border width

    # Ground strip
    c.rect(u(0.0) - n, u(0.80), u(1.0) + n, u(0.86), INK)

    # Castle body: three columns, two rows
    left, right = u(0.24), u(0.76)
    top, bottom = u(0.42), u(0.80)
    col_w = (right - left) / 3.0
    row_h = (bottom - top) / 2.0
    for row in range(2):
        for col in range(3):
            x0 = left + col * col_w
            y0 = top + row * row_h
            c.rect_outlined(x0, y0, x0 + col_w, y0 + row_h, WOOD, INK, bw)

    # Battlements (merlons) across the top
    mer_w = (right - left) / 5.0
    mer_h = area * 0.09
    for i in (0, 2, 4):
        x0 = left + i * mer_w
        c.rect_outlined(x0, top - mer_h, x0 + mer_w, top + bw, WOOD, INK, bw)

    # Cannonball incoming from the upper left, with a dotted trail
    ball_r = area * 0.085
    bx, by = u(0.22), u(0.20)
    for k in range(4):
        t = k / 4.0
        c.disc(u(0.03) + (bx - u(0.03)) * t,
               u(0.10) + (by - u(0.10)) * t * t,
               area * 0.018, CREAM)
    c.disc(bx, by, ball_r + bw, INK)
    c.disc(bx, by, ball_r, BALL)
    c.disc(bx - ball_r * 0.35, by - ball_r * 0.35, ball_r * 0.28, CREAM)

    out_n, data = c.downsample(SS)
    write_png(output_path, out_n, data)
    print(f"Wrote {output_path} ({out_n}x{out_n})")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    create_icon(192, os.path.join(out_dir, "icon-192.png"))
    create_icon(512, os.path.join(out_dir, "icon-512.png"))
    create_icon(512, os.path.join(out_dir, "icon-maskable-512.png"), safe_zone_pct=0.10)
    create_icon(32, os.path.join(out_dir, "favicon-32.png"))
