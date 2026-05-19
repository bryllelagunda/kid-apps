"""Generate PWA icons for Crane Stacker."""
from PIL import Image, ImageDraw, ImageFont
import os

# Colors matching the game palette
SKY = (255, 216, 107)         # #ffd86b
BLOCK_RED = (255, 59, 107)    # #ff3b6b
INK = (42, 26, 10)            # #2a1a0a

def darken(rgb, amount):
    return tuple(max(0, c - amount) for c in rgb[:3])

def find_font(size):
    """Try a series of likely font paths; fall back to default."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def create_icon(size, output_path, safe_zone_pct=0.0):
    """Render a single icon at the given size.
    
    safe_zone_pct: fraction of the icon to reserve as padding around the
    content (for maskable icons, ~0.10 keeps content in the safe area).
    """
    # Background fills the full canvas
    img = Image.new('RGBA', (size, size), SKY + (255,))
    draw = ImageDraw.Draw(img)

    # Define content area (smaller for maskable so OS can mask edges)
    pad = int(size * safe_zone_pct)
    content_size = size - 2 * pad
    content_x = pad
    content_y = pad

    # Block geometry — centered, large
    block_size = int(content_size * 0.62)
    block_x = content_x + (content_size - block_size) // 2
    block_y = content_y + (content_size - block_size) // 2 + int(size * 0.03)

    # Block shadow
    sh = max(3, size // 64)
    draw.rounded_rectangle(
        [block_x + sh, block_y + sh, block_x + block_size + sh, block_y + block_size + sh],
        radius=size // 28, fill=(0, 0, 0, 70)
    )

    # LEGO studs on top (two visible, drawn before block body so block covers their bases)
    stud_w = int(block_size * 0.22)
    stud_h = int(block_size * 0.18)
    stud_gap = int(block_size * 0.14)
    stud_color = darken(BLOCK_RED, 28)
    stud_y = block_y - stud_h + max(2, size // 100)
    border = max(3, size // 64)

    left_stud_x = block_x + block_size // 2 - stud_gap // 2 - stud_w
    draw.rounded_rectangle(
        [left_stud_x, stud_y, left_stud_x + stud_w, stud_y + stud_h],
        radius=size // 56, fill=stud_color, outline=INK, width=border
    )
    right_stud_x = block_x + block_size // 2 + stud_gap // 2
    draw.rounded_rectangle(
        [right_stud_x, stud_y, right_stud_x + stud_w, stud_y + stud_h],
        radius=size // 56, fill=stud_color, outline=INK, width=border
    )

    # Main block body
    draw.rounded_rectangle(
        [block_x, block_y, block_x + block_size, block_y + block_size],
        radius=size // 28, fill=BLOCK_RED, outline=INK, width=border
    )

    # Subtle highlight near top of block (gloss, not a label)
    h_inset = border + 4
    highlight_h = int(block_size * 0.22)
    # Use an overlay layer for true alpha blending
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(
        [block_x + h_inset, block_y + h_inset,
         block_x + block_size - h_inset, block_y + h_inset + highlight_h],
        radius=size // 56, fill=(255, 255, 255, 45)
    )
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Letter "S" centered on the block (first letter of SATPIN)
    text = "S"
    font_size = int(block_size * 0.62)
    font = find_font(font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    tx = block_x + (block_size - text_w) // 2 - bbox[0]
    ty = block_y + (block_size - text_h) // 2 - bbox[1] + int(size * 0.01)
    draw.text((tx, ty), text, fill=INK, font=font)

    # Save as PNG
    img.save(output_path, 'PNG')
    print(f"Wrote {output_path} ({size}x{size})")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    create_icon(192, os.path.join(out_dir, "icon-192.png"))
    create_icon(512, os.path.join(out_dir, "icon-512.png"))
    create_icon(512, os.path.join(out_dir, "icon-maskable-512.png"), safe_zone_pct=0.10)
    # Also a small favicon-style 32 for completeness
    create_icon(32, os.path.join(out_dir, "favicon-32.png"))
