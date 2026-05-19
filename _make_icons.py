"""Generate PWA icons for the Kid Apps launcher.
Design: 2x2 grid of colored tiles on a sky-yellow background, suggesting an app drawer.
"""
from PIL import Image, ImageDraw
import os

SKY = (255, 216, 107)
INK = (42, 26, 10)
TILE_COLORS = [
    (255, 59, 107),   # hot pink
    (46, 184, 255),   # cool blue
    (67, 230, 165),   # mint
    (168, 107, 255),  # grape
]

def create_launcher_icon(size, output_path, safe_zone_pct=0.0):
    img = Image.new('RGBA', (size, size), SKY + (255,))
    draw = ImageDraw.Draw(img)

    pad = int(size * safe_zone_pct)
    inner = size - 2 * pad

    # 2x2 tile grid centered in the canvas
    grid_size = int(inner * 0.70)
    grid_x = pad + (inner - grid_size) // 2
    grid_y = pad + (inner - grid_size) // 2

    gap = max(4, size // 28)
    cell = (grid_size - gap) // 2
    radius = max(4, size // 22)
    border = max(3, size // 64)
    shadow_offset = max(2, size // 100)

    for i, color in enumerate(TILE_COLORS):
        row, col = i // 2, i % 2
        x = grid_x + col * (cell + gap)
        y = grid_y + row * (cell + gap)

        # Shadow
        draw.rounded_rectangle(
            [x + shadow_offset, y + shadow_offset, x + cell + shadow_offset, y + cell + shadow_offset],
            radius=radius, fill=(0, 0, 0, 60)
        )
        # Tile body
        draw.rounded_rectangle(
            [x, y, x + cell, y + cell],
            radius=radius, fill=color, outline=INK, width=border
        )

    # Add subtle gloss highlights as a separate alpha-composited layer
    # (skip on very small icons where the geometry would degenerate)
    if size >= 64:
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        for i in range(4):
            row, col = i // 2, i % 2
            x = grid_x + col * (cell + gap)
            y = grid_y + row * (cell + gap)
            h_inset = border + 3
            h_height = int(cell * 0.22)
            x1, y1 = x + h_inset, y + h_inset
            x2, y2 = x + cell - h_inset, y + h_inset + h_height
            if x2 > x1 and y2 > y1:
                odraw.rounded_rectangle(
                    [x1, y1, x2, y2],
                    radius=max(2, radius // 2), fill=(255, 255, 255, 60)
                )
        img = Image.alpha_composite(img, overlay)
    img.save(output_path, 'PNG')
    print(f"Wrote {output_path} ({size}x{size})")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    create_launcher_icon(192, os.path.join(out_dir, "icon-192.png"))
    create_launcher_icon(512, os.path.join(out_dir, "icon-512.png"))
    create_launcher_icon(512, os.path.join(out_dir, "icon-maskable-512.png"), safe_zone_pct=0.10)
    create_launcher_icon(32, os.path.join(out_dir, "favicon-32.png"))
