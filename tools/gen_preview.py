"""Generate the Steam Workshop / mod-menu preview image About/Preview.png.

Composites the mod's own turret textures (1.6/Textures/MountedArms/*_Base.png
with the matching *_Top.png centered on it, at the in-game draw-size ratio)
into a 1280x720 lineup on an olive ground, with the shared header/footer
style used by all of Felipe's mod previews (Mounted Arms, Mounted Arms:
Strategic, Colony Organizer).

Run from the mod folder (all paths are relative to it):

    python tools/gen_preview.py

Deterministic: the only noise uses a fixed seed. Requires Pillow.
"""
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H = 1280, 720
HEADER_H = 132
ACCENT_H = 6
FOOTER_H = 64
MARGIN = 48

ACCENT = (0xC9, 0xA2, 0x27)
BAND = (0x15, 0x17, 0x1A)
TITLE_COL = (0xF2, 0xF2, 0xF2)
TEXT_COL = (0xD8, 0xD8, 0xD8)

TITLE = "MOUNTED ARMS"
TAGLINE = "Modern mounted-weapon turrets  |  Vanilla + Combat Extended"
BADGE = "RimWorld 1.6 \u00b7 1.7"

TEX_DIR = os.path.join("1.6", "Textures", "MountedArms")
OUT = os.path.join("About", "Preview.png")

# name: (base drawSize in tiles, turretTopDrawSize) -- from 1.6/Defs/Buildings.xml
TURRETS = {
    "M2": (2, 2.06),
    "M134": (2, 2.16),
    "Mk44": (2, 2.06),
    "CIWS": (2, 2.06),
    "Goalkeeper": (2, 2.06),
    "BoforsQuad": (3, 2.19),
    "ZU23": (2, 2.43),
    "Avenger": (2, 2.4),
    "LaserCIWS": (2, 2.38),
}


def font(size, weight="Regular"):
    try:
        f = ImageFont.truetype(r"C:\Windows\Fonts\bahnschrift.ttf", size)
        f.set_variation_by_name(weight)
        return f
    except Exception:
        bold = weight in ("Bold", "SemiBold")
        name = "segoeuib.ttf" if bold else "segoeui.ttf"
        return ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", name), size)


# ----------------------------------------------------------------- background
def background():
    rng = random.Random(1337)
    base = (60, 70, 46)
    img = Image.new("RGB", (W, H), base)

    # broad mottling: low-res noise blown up and blurred
    lo = Image.new("L", (W // 40, H // 40))
    lo.putdata([rng.randint(0, 255) for _ in range(lo.width * lo.height)])
    lo = lo.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(28))
    dark = Image.new("RGB", (W, H), (46, 55, 35))
    light = Image.new("RGB", (W, H), (74, 85, 56))
    img = Image.composite(light, dark, lo)

    # fine grain
    grain = Image.new("L", (W, H))
    grain.putdata([rng.randint(108, 148) for _ in range(W * H)])
    grain = grain.filter(ImageFilter.GaussianBlur(0.6))
    img = ImageChops.overlay(img, Image.merge("RGB", (grain, grain, grain)))
    return img


def tile_grid(img, cell, ox, oy):
    """Faint RimWorld-like tile grid."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = ox % cell
    while x < W:
        d.line([(x, 0), (x, H)], fill=(20, 26, 14, 34), width=1)
        x += cell
    y = oy % cell
    while y < H:
        d.line([(0, y), (W, y)], fill=(20, 26, 14, 34), width=1)
        y += cell
    img.alpha_composite(layer)


def vignette(img):
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-260, -120, W + 260, H + 160), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(150))
    shade = Image.new("RGBA", (W, H), (8, 10, 6, 0))
    shade.putalpha(ImageChops.invert(mask).point(lambda v: int(v * 0.62)))
    img.alpha_composite(shade)


def glow(img, cx, cy, r, alpha):
    layer = Image.new("L", (W, H), 0)
    ImageDraw.Draw(layer).ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), fill=alpha)
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.45))
    lit = Image.new("RGBA", (W, H), (150, 160, 110, 0))
    lit.putalpha(layer)
    img.alpha_composite(lit)


# ------------------------------------------------------------------- sprites
def turret(name, unit, angle=0):
    """Base + top composited at in-game proportions; unit = px per tile.

    angle: degrees counter-clockwise to turn the gun top (textures aim east).
    """
    tiles, top_size = TURRETS[name]
    base = Image.open(os.path.join(TEX_DIR, name + "_Base.png")).convert("RGBA")
    top = Image.open(os.path.join(TEX_DIR, name + "_Top.png")).convert("RGBA")
    b = base.resize((int(round(tiles * unit)),) * 2, Image.LANCZOS)
    # rotate at 2x then downscale, so the turned top stays crisp
    t2 = top.resize((int(round(top_size * unit * 2)),) * 2, Image.LANCZOS)
    if angle:
        t2 = t2.rotate(angle, resample=Image.BICUBIC, expand=True)
    t = t2.resize((t2.width // 2, t2.height // 2), Image.LANCZOS)
    canvas_px = max(b.width, t.width) + 4
    c = Image.new("RGBA", (canvas_px, canvas_px), (0, 0, 0, 0))
    c.alpha_composite(b, ((canvas_px - b.width) // 2, (canvas_px - b.height) // 2))
    c.alpha_composite(t, ((canvas_px - t.width) // 2, (canvas_px - t.height) // 2))
    return c.crop(c.getchannel("A").getbbox())


def place(img, sprite, cx, cy, shadow=(7, 11), blur=9, alpha=0.45):
    x = int(cx - sprite.width / 2)
    y = int(cy - sprite.height / 2)
    pad = blur * 3
    sh = Image.new("RGBA", (sprite.width + pad * 2, sprite.height + pad * 2), (0, 0, 0, 0))
    a = sprite.getchannel("A").point(lambda v: int(v * alpha))
    blk = Image.new("RGBA", sprite.size, (0, 0, 0, 255))
    blk.putalpha(a)
    sh.alpha_composite(blk, (pad, pad))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(sh, (x - pad + shadow[0], y - pad + shadow[1]))
    img.alpha_composite(sprite, (x, y))
    return x, y, sprite.width, sprite.height


def label(img, text, cx, top, size=19, colour=(226, 226, 214)):
    d = ImageDraw.Draw(img)
    f = font(size, "SemiBold")
    w = d.textlength(text, font=f)
    # soft dark backing so it reads on the mottled ground
    d.text((cx - w / 2 + 1, top + 2), text, font=f, fill=(10, 12, 8, 170))
    d.text((cx - w / 2, top), text, font=f, fill=colour + (255,))


# ------------------------------------------------------------- header/footer
def header(img):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, HEADER_H), fill=BAND + (255,))
    d.rectangle((0, HEADER_H, W, HEADER_H + ACCENT_H - 1), fill=ACCENT + (255,))
    f = font(86, "Bold")
    l, t, r, b = d.textbbox((0, 0), TITLE, font=f)
    y = (HEADER_H - (b - t)) // 2 - t
    d.text((MARGIN, y), TITLE, font=f, fill=TITLE_COL + (255,))


def footer(img):
    band = Image.new("RGBA", (W, FOOTER_H), BAND + (int(255 * 0.88),))
    img.alpha_composite(band, (0, H - FOOTER_H))
    d = ImageDraw.Draw(img)
    f = font(28, "Regular")
    l, t, r, b = d.textbbox((0, 0), TAGLINE, font=f)
    y0 = H - FOOTER_H
    d.text((MARGIN, y0 + (FOOTER_H - (b - t)) // 2 - t), TAGLINE, font=f, fill=TEXT_COL + (255,))

    fb = font(24, "SemiBold")
    l, t, r, b = d.textbbox((0, 0), BADGE, font=fb)
    tw, th = r - l, b - t
    px, ph = 18, 40
    bx1 = W - MARGIN
    bx0 = bx1 - tw - px * 2
    by0 = y0 + (FOOTER_H - ph) // 2
    d.rounded_rectangle((bx0, by0, bx1, by0 + ph), radius=ph // 2, outline=ACCENT + (255,), width=2)
    d.text((bx0 + px - l, by0 + (ph - th) // 2 - t), BADGE, font=fb, fill=TITLE_COL + (255,))


# ---------------------------------------------------------------------- main
def main():
    img = background().convert("RGBA")
    art_top, art_bot = HEADER_H + ACCENT_H, H - FOOTER_H
    cy = (art_top + art_bot) // 2  # ~397

    tile_grid(img, 52, 640 - 26, cy - 26)
    glow(img, 640, cy, 300, 70)
    vignette(img)

    # (name, unit px/tile, cx, cy, gun angle, label); guns face outward
    layout = [
        ("BoforsQuad", 104, 640, cy - 10, 90, "BOFORS QUAD"),
        ("CIWS", 96, 392, cy - 10, 158, "PHALANX CIWS"),
        ("Avenger", 96, 888, cy - 10, 22, "AVENGER"),
        ("M2", 80, 148, art_top + 116, 150, "M2"),
        ("M134", 80, 148, art_bot - 134, 206, "M134"),
        ("Mk44", 80, 1132, art_top + 116, 30, "MK44 30MM"),
        ("LaserCIWS", 80, 1132, art_bot - 134, -26, "IRON BEAM"),
    ]
    for name, unit, x, y, ang, text in layout:
        spr = turret(name, unit, ang)
        px, py, pw, phh = place(img, spr, x, y, blur=11 if unit > 90 else 8)
        if name == "BoforsQuad":  # hero: larger label in the accent colour
            label(img, text, x, py + phh + 10, 24, ACCENT)
        else:
            label(img, text, x, py + phh + 8, 21 if unit > 90 else 18)

    header(img)
    footer(img)

    out = img.convert("RGB")
    out.save(OUT, optimize=True)
    if os.path.getsize(OUT) >= 1_000_000:
        q = out.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
        q.convert("RGB").save(OUT, optimize=True)
    chk = Image.open(OUT)
    print(OUT, chk.size, chk.mode, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
