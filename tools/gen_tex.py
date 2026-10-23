import math, sys, os
from PIL import Image, ImageDraw, ImageFilter

OUT = sys.argv[1]
S = 4                 # supersampling
N = 256               # final texture size
W = N * S

BLACK  = (24, 26, 29, 255)
STEEL  = (96, 103, 110, 255)
STEEL_L= (142, 150, 157, 255)
STEEL_D= (58, 63, 69, 255)
GUN    = (52, 57, 62, 255)
GUN_L  = (86, 93, 99, 255)
OLIVE  = (82, 94, 62, 255)
OLIVE_L= (112, 126, 84, 255)
OLIVE_D= (54, 63, 41, 255)
BRASS  = (190, 150, 62, 255)
YELLOW = (214, 178, 40, 255)
RED    = (150, 48, 40, 255)
LW = int(2.0 * S)

def canvas():
    return Image.new("RGBA", (W, W), (0, 0, 0, 0))

def sc(v):
    return [int(round(x * S)) for x in v]

def rect(d, x0, y0, x1, y1, fill, r=3, outline=BLACK, hl=True):
    box = sc((x0, y0, x1, y1))
    d.rounded_rectangle(box, radius=int(r * S), fill=fill, outline=outline, width=LW)
    if hl and (x1 - x0) > 8:
        # light strip on the left edge for a simple lit-from-left look
        lx0 = x0 + 2.2; lx1 = min(x0 + 2.2 + max(1.5, (x1 - x0) * 0.16), x1 - 2.2)
        c = tuple(min(255, int(v * 1.3)) for v in fill[:3]) + (255,)
        d.rounded_rectangle(sc((lx0, y0 + 2.4, lx1, y1 - 2.4)), radius=int(1.2 * S), fill=c)

def circ(d, cx, cy, r, fill, outline=BLACK, w=LW):
    d.ellipse(sc((cx - r, cy - r, cx + r, cy + r)), fill=fill, outline=outline, width=w)

def line(d, p0, p1, width, fill):
    d.line(sc((p0[0], p0[1], p1[0], p1[1])), fill=fill, width=int(width * S))

def poly(d, pts, fill, outline=BLACK):
    d.polygon([tuple(sc(p)) for p in pts], fill=fill)
    d.line([tuple(sc(p)) for p in pts] + [tuple(sc(pts[0]))], fill=outline, width=LW, joint="curve")

def octagon(cx, cy, r):
    return [(cx + r * math.cos(math.radians(22.5 + 45 * i)), cy + r * math.sin(math.radians(22.5 + 45 * i))) for i in range(8)]

def shadow(img, offset=(5, 6), blur=7, alpha=120):
    a = img.split()[3]
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    black = Image.new("RGBA", img.size, (0, 0, 0, alpha))
    sh.paste(black, (offset[0] * S, offset[1] * S), a)
    sh = sh.filter(ImageFilter.GaussianBlur(blur * S / 2))
    sh.alpha_composite(img)
    return sh

def finish(img, path):
    img = img.resize((N, N), Image.LANCZOS)
    img.save(path)

def rivets(d, pts, r=2.6):
    for (x, y) in pts:
        circ(d, x, y, r, STEEL_L, outline=BLACK, w=int(1.2 * S))

def screws_octagon(d, cx, cy, r, n=8):
    rivets(d, [(cx + r * math.cos(math.radians(22.5 + 360 / n * i)), cy + r * math.sin(math.radians(22.5 + 360 / n * i))) for i in range(n)])

# ------------------------------------------------------------------ bases
def base_common(d, plate_r=84, hub_r=34):
    poly(d, octagon(128, 128, plate_r), STEEL_D)
    poly(d, octagon(128, 128, plate_r - 9), STEEL)
    screws_octagon(d, 128, 128, plate_r - 4.5)
    circ(d, 128, 128, hub_r + 8, STEEL_D)
    circ(d, 128, 128, hub_r, GUN)
    circ(d, 128, 128, hub_r - 12, STEEL_D)

def ammo_can(d, x, y, w, h, color=OLIVE):
    rect(d, x, y, x + w, y + h, color, r=3)
    rect(d, x + 4, y + 4, x + w - 4, y + h - 4, OLIVE_D if color == OLIVE else STEEL_D, r=2, hl=False)
    line(d, (x + w / 2, y + 2), (x + w / 2, y - 6), 3, BLACK)   # handle

def base_m240():
    img = canvas(); d = ImageDraw.Draw(img)
    # tripod legs
    for (ex, ey) in [(38, 214), (218, 214), (128, 28)]:
        line(d, (128, 128), (ex, ey), 15, BLACK)
        line(d, (128, 128), (ex, ey), 10, STEEL_D)
        line(d, (128, 128), (ex, ey), 4, STEEL)
        circ(d, ex, ey, 13, STEEL_D)
        circ(d, ex, ey, 7, STEEL)
    circ(d, 128, 128, 40, STEEL_D)
    circ(d, 128, 128, 30, GUN)
    circ(d, 128, 128, 16, STEEL_D)
    ammo_can(d, 170, 150, 44, 34)
    ammo_can(d, 150, 196, 34, 26, OLIVE)
    return shadow(img)

def base_m2():
    img = canvas(); d = ImageDraw.Draw(img)
    base_common(d, 86, 34)
    # pintle post
    rect(d, 112, 112, 144, 144, STEEL, r=4)
    ammo_can(d, 36, 150, 48, 38)
    ammo_can(d, 34, 196, 40, 28)
    # seat plate (operator position is south)
    rect(d, 100, 206, 156, 240, STEEL_D, r=5, hl=False)
    return shadow(img)

def base_mk19():
    img = canvas(); d = ImageDraw.Draw(img)
    # square plate
    rect(d, 40, 40, 216, 216, STEEL_D, r=10, hl=False)
    rect(d, 50, 50, 206, 206, STEEL, r=8, hl=False)
    rivets(d, [(56, 56), (200, 56), (56, 200), (200, 200), (128, 56), (128, 200), (56, 128), (200, 128)])
    circ(d, 128, 128, 44, STEEL_D)
    circ(d, 128, 128, 34, GUN)
    circ(d, 128, 128, 18, STEEL_D)
    ammo_can(d, 156, 160, 40, 32)
    ammo_can(d, 60, 164, 36, 30)
    rect(d, 106, 214, 150, 240, STEEL_D, r=4, hl=False)
    return shadow(img)

def base_m134():
    img = canvas(); d = ImageDraw.Draw(img)
    base_common(d, 88, 34)
    # hazard ring
    for i in range(24):
        a0 = i * 15
        d.pieslice(sc((128 - 62, 128 - 62, 128 + 62, 128 + 62)), a0, a0 + 15, fill=YELLOW if i % 2 == 0 else BLACK)
    circ(d, 128, 128, 50, GUN)
    circ(d, 128, 128, 36, STEEL_D)
    circ(d, 128, 128, 20, GUN)
    # power block + cables
    rect(d, 150, 28, 214, 76, STEEL_D, r=4)
    rect(d, 156, 34, 208, 70, GUN, r=3, hl=False)
    circ(d, 168, 52, 6, RED); circ(d, 190, 52, 6, (60, 170, 70, 255))
    line(d, (150, 60), (128, 100), 5, BLACK)
    line(d, (150, 60), (128, 100), 3, (40, 44, 50, 255))
    ammo_can(d, 36, 168, 48, 40)
    rect(d, 100, 214, 156, 240, STEEL_D, r=5, hl=False)
    return shadow(img)

# ------------------------------------------------------------------ tops (barrel points UP, pivot at 128,128)
def belt(d, x0, y0, x1, y1, n=7):
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
        rect(d, x - 3.2, y - 3.2, x + 3.2, y + 3.2, BRASS, r=1, hl=False)

def top_m240():
    img = canvas(); d = ImageDraw.Draw(img)
    # barrel + muzzle brake
    rect(d, 123, 24, 133, 112, GUN, r=2)
    rect(d, 117, 14, 139, 34, STEEL_D, r=3)
    for y in (18, 24, 30):
        line(d, (117, y), (139, y), 1.2, BLACK)
    # heat shield / handguard
    rect(d, 115, 56, 141, 118, STEEL, r=4)
    for y in range(64, 114, 9):
        rect(d, 121, y, 135, y + 4, GUN, r=1, hl=False)
    # ammo box + belt
    ammo_can(d, 70, 120, 38, 42)
    belt(d, 108, 132, 118, 138, 3)
    # receiver
    rect(d, 106, 110, 150, 176, STEEL, r=6)
    rect(d, 114, 120, 142, 166, STEEL_D, r=3, hl=False)
    line(d, (128, 116), (128, 170), 2.2, STEEL_L)
    rect(d, 140, 128, 156, 136, GUN, r=2)         # charging handle
    # stock / grips
    rect(d, 118, 174, 138, 206, GUN, r=3)
    rect(d, 104, 198, 152, 208, STEEL_D, r=3)
    circ(d, 108, 203, 6, BLACK); circ(d, 148, 203, 6, BLACK)
    return img

def top_m2():
    img = canvas(); d = ImageDraw.Draw(img)
    # barrel + flash hider
    rect(d, 122, 12, 134, 52, GUN, r=2)
    rect(d, 118, 10, 138, 26, STEEL_D, r=3)
    # perforated cooling jacket
    rect(d, 112, 44, 144, 124, STEEL, r=5)
    for row in range(5):
        for col in range(2):
            circ(d, 121 + col * 14, 56 + row * 14, 3.4, BLACK, outline=BLACK, w=1)
    # receiver
    rect(d, 98, 118, 158, 184, STEEL, r=6)
    rect(d, 108, 128, 148, 174, STEEL_D, r=4, hl=False)
    rect(d, 122, 120, 134, 182, GUN_L, r=2, hl=False)
    rect(d, 156, 134, 176, 144, GUN, r=3)         # charging handle
    circ(d, 178, 139, 6, STEEL_L)
    # ammo can + belt
    ammo_can(d, 52, 128, 42, 50)
    belt(d, 94, 146, 104, 152, 3)
    # spade grips
    rect(d, 94, 190, 162, 200, STEEL_D, r=3)
    rect(d, 86, 186, 98, 214, BLACK, r=3, hl=False)
    rect(d, 158, 186, 170, 214, BLACK, r=3, hl=False)
    return img

def top_mk19():
    img = canvas(); d = ImageDraw.Draw(img)
    # short fat barrel with shroud and muzzle ring
    rect(d, 117, 34, 139, 116, GUN, r=3)
    rect(d, 112, 48, 144, 108, STEEL, r=5)
    for y in range(54, 106, 10):
        line(d, (112, y), (144, y), 1.4, BLACK)
    rect(d, 112, 28, 144, 40, STEEL_D, r=4)
    circ(d, 128, 34, 7, BLACK)
    # receiver
    rect(d, 92, 108, 164, 184, STEEL, r=7)
    rect(d, 102, 118, 154, 174, STEEL_D, r=4, hl=False)
    for x in (112, 128, 144):
        line(d, (x, 122), (x, 170), 2, GUN_L)
    # drum ammo can on the left + strap
    rect(d, 48, 112, 96, 176, OLIVE, r=10)
    rect(d, 55, 119, 89, 169, OLIVE_D, r=7, hl=False)
    line(d, (72, 112), (72, 176), 3, BLACK)
    belt(d, 96, 138, 104, 144, 3)
    # charging handle + grips
    rect(d, 162, 130, 182, 140, GUN, r=3)
    rect(d, 96, 190, 160, 200, STEEL_D, r=3)
    rect(d, 90, 186, 102, 212, BLACK, r=3, hl=False)
    rect(d, 154, 186, 166, 212, BLACK, r=3, hl=False)
    return img

def top_m134():
    img = canvas(); d = ImageDraw.Draw(img)
    # six barrels seen from above: bundle of parallel strips
    for i, x in enumerate((113, 120.5, 128, 135.5, 143)):
        c = GUN if i % 2 == 0 else GUN_L
        rect(d, x - 3.4, 14, x + 3.4, 124, c, r=1.5, hl=False)
    # clamp rings
    for y, h in ((22, 8), (64, 8), (104, 8)):
        rect(d, 104, y, 152, y + h, STEEL_D, r=3)
    rect(d, 106, 12, 150, 20, BLACK, r=2, hl=False)   # muzzle ring
    # motor housing
    rect(d, 98, 120, 158, 174, STEEL, r=7)
    rect(d, 108, 130, 148, 166, STEEL_D, r=4, hl=False)
    circ(d, 128, 148, 9, GUN_L)
    # big drum on the left + chute
    circ(d, 74, 150, 34, OLIVE)
    circ(d, 74, 150, 24, OLIVE_D)
    circ(d, 74, 150, 8, BLACK)
    rect(d, 100, 140, 112, 160, STEEL_D, r=2)
    belt(d, 100, 150, 108, 150, 2)
    # feed cable + grips
    line(d, (158, 150), (186, 168), 5, BLACK)
    line(d, (158, 150), (186, 168), 3, (46, 50, 56, 255))
    rect(d, 96, 182, 160, 192, STEEL_D, r=3)
    rect(d, 90, 178, 102, 204, BLACK, r=3, hl=False)
    rect(d, 154, 178, 166, 204, BLACK, r=3, hl=False)
    return img


def base_mk44():
    img = canvas(); d = ImageDraw.Draw(img)
    # heavy square plate with chamfered look
    rect(d, 34, 34, 222, 222, STEEL_D, r=12, hl=False)
    rect(d, 44, 44, 212, 212, STEEL, r=9, hl=False)
    rivets(d, [(52, 52), (204, 52), (52, 204), (204, 204), (128, 52), (128, 204), (52, 128), (204, 128), (90, 52), (166, 52), (90, 204), (166, 204)])
    circ(d, 128, 128, 48, STEEL_D)
    circ(d, 128, 128, 38, GUN)
    circ(d, 128, 128, 20, STEEL_D)
    # two ammunition boxes (HE and AP feed)
    ammo_can(d, 150, 156, 46, 34)
    ammo_can(d, 56, 156, 46, 34)
    # seat plate (operator position is south)
    rect(d, 104, 212, 152, 242, STEEL_D, r=4, hl=False)
    return shadow(img)

def top_mk44():
    img = canvas(); d = ImageDraw.Draw(img)
    # long barrel with heat shroud and muzzle brake
    rect(d, 120, 18, 136, 112, GUN, r=3)
    rect(d, 114, 50, 142, 108, STEEL, r=4)
    for y in range(56, 104, 9):
        line(d, (114, y), (142, y), 1.4, BLACK)
    rect(d, 112, 14, 144, 32, STEEL_D, r=3)
    line(d, (112, 20), (144, 20), 1.6, BLACK); line(d, (112, 26), (144, 26), 1.6, BLACK)
    circ(d, 128, 18, 6, BLACK)
    # receiver / feed
    rect(d, 88, 106, 168, 190, STEEL, r=8)
    rect(d, 98, 116, 158, 180, STEEL_D, r=5, hl=False)
    for x in (110, 128, 146):
        line(d, (x, 120), (x, 176), 2, GUN_L)
    # dual feed chutes with belts toward the side boxes
    rect(d, 62, 124, 90, 146, GUN, r=3)
    belt(d, 62, 135, 48, 150, 4)
    rect(d, 166, 124, 194, 146, GUN, r=3)
    belt(d, 194, 135, 208, 150, 4)
    # cocking handle and rear grips
    rect(d, 166, 156, 186, 166, GUN, r=3)
    rect(d, 96, 194, 160, 206, STEEL_D, r=3)
    rect(d, 90, 190, 102, 218, BLACK, r=3, hl=False)
    rect(d, 154, 190, 166, 218, BLACK, r=3, hl=False)
    return img


# ------------------------------------------------------------------ batch 2: TOW, Hydra pod, CIWS, M252
def tube_cluster(d, cx, cy, r=5.2, gap=11.0):
    pts = [(cx, cy)] + [(cx + gap * math.cos(math.radians(60 * i)), cy + gap * math.sin(math.radians(60 * i))) for i in range(6)]
    for (x, y) in pts:
        circ(d, x, y, r, BLACK, outline=GUN_L, w=int(1.2 * S))

def base_tow():
    img = canvas(); d = ImageDraw.Draw(img)
    # tripod: three splayed legs and feet pads
    for ang in (90, 210, 330):
        ex = 128 + 92 * math.cos(math.radians(ang)); ey = 128 + 92 * math.sin(math.radians(ang))
        line(d, (128, 128), (ex, ey), 11, BLACK)
        line(d, (128, 128), (ex, ey), 7, STEEL)
        circ(d, ex, ey, 13, STEEL_D); circ(d, ex, ey, 6, GUN)
    circ(d, 128, 128, 36, STEEL_D); circ(d, 128, 128, 28, GUN); circ(d, 128, 128, 14, STEEL_D)
    ammo_can(d, 164, 168, 44, 30)
    rect(d, 100, 208, 156, 242, STEEL_D, r=5, hl=False)
    return shadow(img)

def top_tow():
    img = canvas(); d = ImageDraw.Draw(img)
    # launch tube with blast cover and a rear venturi
    rect(d, 116, 22, 140, 150, OLIVE, r=6)
    rect(d, 112, 16, 144, 38, GUN, r=4)
    circ(d, 128, 20, 9, BLACK)
    rect(d, 112, 104, 144, 124, STEEL_D, r=3, hl=False)
    rect(d, 118, 148, 138, 176, GUN, r=5)
    circ(d, 128, 178, 10, BLACK, outline=GUN_L)
    # optical guidance unit on the right with lens
    rect(d, 146, 66, 186, 124, STEEL, r=7)
    circ(d, 156, 74, 7, (30, 60, 80, 255), outline=BLACK)
    rect(d, 150, 96, 182, 118, STEEL_D, r=3, hl=False)
    # missile canister strapped on the left
    rect(d, 84, 56, 112, 146, OLIVE_D, r=7)
    line(d, (84, 80), (112, 80), 2, BLACK); line(d, (84, 120), (112, 120), 2, BLACK)
    # grips
    rect(d, 100, 150, 156, 160, STEEL_D, r=3)
    rect(d, 96, 148, 108, 176, BLACK, r=3, hl=False); rect(d, 148, 148, 160, 176, BLACK, r=3, hl=False)
    return img

def base_hydra():
    img = canvas(); d = ImageDraw.Draw(img)
    base_common(d, 86, 34)
    rect(d, 112, 112, 144, 144, STEEL, r=4)
    ammo_can(d, 34, 150, 52, 34, color=STEEL_D)
    ammo_can(d, 170, 160, 46, 32, color=STEEL_D)
    rect(d, 96, 212, 160, 242, STEEL_D, r=4, hl=False)
    return shadow(img)

def top_hydra():
    img = canvas(); d = ImageDraw.Draw(img)
    # seven-tube rocket pod: boxy body with a hex tube cluster drawn on the front end
    rect(d, 88, 52, 168, 176, STEEL, r=10)
    rect(d, 96, 62, 160, 166, STEEL_D, r=6, hl=False)
    for y in (96, 126, 156):
        line(d, (96, y), (160, y), 2, GUN_L)
    rect(d, 92, 22, 164, 66, STEEL_D, r=8)
    tube_cluster(d, 128, 44, 6.0, 12.5)
    # warning band and rear electronics box
    rect(d, 88, 84, 168, 92, YELLOW, r=1, hl=False)
    rect(d, 106, 176, 150, 204, GUN, r=5)
    return img

def base_ciws():
    img = canvas(); d = ImageDraw.Draw(img)
    poly(d, octagon(128, 128, 90), STEEL_D)
    poly(d, octagon(128, 128, 80), STEEL)
    screws_octagon(d, 128, 128, 84)
    circ(d, 128, 128, 56, STEEL_D); circ(d, 128, 128, 48, GUN); circ(d, 128, 128, 32, STEEL_D)
    ammo_can(d, 40, 160, 50, 36, color=STEEL_D)
    ammo_can(d, 166, 160, 50, 36, color=STEEL_D)
    rect(d, 100, 210, 156, 242, STEEL_D, r=4, hl=False)
    return shadow(img)

def top_ciws():
    img = canvas(); d = ImageDraw.Draw(img)
    # six-barrel cluster seen from above: three visible barrels, shroud rings, muzzle collar
    for x in (113, 128, 143):
        rect(d, x - 6, 20, x + 6, 122, GUN, r=3)
    rect(d, 104, 50, 152, 66, STEEL, r=4); rect(d, 104, 92, 152, 106, STEEL, r=4)
    rect(d, 102, 16, 154, 30, STEEL_D, r=4)
    # gun body and big white-grey radome / ammo drum behind
    rect(d, 92, 118, 164, 170, STEEL, r=8)
    circ(d, 128, 186, 38, STEEL_L); circ(d, 128, 186, 30, (210, 214, 216, 255)); circ(d, 128, 186, 10, STEEL_D)
    rect(d, 56, 128, 90, 160, GUN, r=5); rect(d, 166, 128, 200, 160, GUN, r=5)
    return img

def base_m252():
    img = canvas(); d = ImageDraw.Draw(img)
    # round baseplate with ribs plus shell crates
    circ(d, 128, 128, 84, STEEL_D); circ(d, 128, 128, 74, STEEL)
    for ang in range(0, 360, 45):
        line(d, (128, 128), (128 + 70 * math.cos(math.radians(ang)), 128 + 70 * math.sin(math.radians(ang))), 3, STEEL_D)
    circ(d, 128, 128, 30, GUN); circ(d, 128, 128, 16, STEEL_D)
    ammo_can(d, 26, 170, 50, 36, color=OLIVE)
    ammo_can(d, 180, 176, 46, 32, color=OLIVE)
    rect(d, 100, 214, 156, 242, STEEL_D, r=4, hl=False)
    return shadow(img)

def top_m252():
    img = canvas(); d = ImageDraw.Draw(img)
    # tube with muzzle ring, bipod legs and sight on the side
    rect(d, 120, 18, 136, 150, GUN, r=5)
    rect(d, 116, 14, 140, 28, STEEL_D, r=4)
    circ(d, 128, 18, 6, BLACK)
    rect(d, 112, 140, 144, 160, STEEL, r=5)
    circ(d, 128, 168, 12, STEEL_D)
    line(d, (128, 96), (88, 176), 5, BLACK); line(d, (128, 96), (88, 176), 3, STEEL)
    line(d, (128, 96), (168, 176), 5, BLACK); line(d, (128, 96), (168, 176), 3, STEEL)
    rect(d, 146, 108, 170, 132, STEEL, r=4)
    circ(d, 158, 120, 5, (30, 60, 80, 255), outline=BLACK)
    return img

def icon(base, top, scale_top=1.0):
    a = base.copy()
    a.alpha_composite(top)
    return a

# ------------------------------------------------------------------ run
F_FRONT = 0.62   # cells from pivot (projectile origin) to muzzle
R_REAR  = 1.00   # cells from pivot to the rear of the gun

def reposition(t):
    """Move the muzzle close to the pivot, keep barrel axis on x=128. Returns (img, drawSize)."""
    bb = t.getbbox()
    top = bb[1] / S; bot = bb[3] / S; h = bot - top
    f = min(1.0, 124 / (R_REAR / (F_FRONT + R_REAR) * h), 124 / (F_FRONT / (F_FRONT + R_REAR) * h))
    ds = 256 * (F_FRONT + R_REAR) / (f * h)
    y_m = 128 - F_FRONT / (F_FRONT + R_REAR) * f * h
    n = int(W * f)
    sc_img = t.resize((n, n), Image.LANCZOS)
    ox = int(128 * S - 128 * S * f); oy = int(y_m * S - top * S * f)
    out = canvas(); out.paste(sc_img, (ox, oy), sc_img)
    return out, ds

def icon2(base, top_east, ds):
    k = ds / 2.0                       # base is drawn at 2 cells
    n = int(W * k)
    big = top_east.resize((n, n), Image.LANCZOS)
    layer = canvas(); layer.paste(big, ((W - n) // 2, (W - n) // 2), big)
    a = base.copy(); a.alpha_composite(layer)
    return a

os.makedirs(OUT, exist_ok=True)
items = {"M240": (base_m240, top_m240), "M2": (base_m2, top_m2), "Mk19": (base_mk19, top_mk19), "M134": (base_m134, top_m134), "Mk44": (base_mk44, top_mk44), "TOW": (base_tow, top_tow), "Hydra": (base_hydra, top_hydra), "CIWS": (base_ciws, top_ciws), "M252": (base_m252, top_m252)}
only = sys.argv[2:]
if only: items = {k: v for k, v in items.items() if k in only}
sizes = {}
for name, (fb, ft) in items.items():
    b = fb()
    t, ds = reposition(ft())
    t = t.rotate(-90, resample=Image.BICUBIC)       # vanilla turret tops point EAST (right)
    sizes[name] = round(ds, 2)
    finish(b, os.path.join(OUT, f"{name}_Base.png"))
    finish(shadow(t, (2, 3), 4, 90), os.path.join(OUT, f"{name}_Top.png"))
    finish(icon2(b, t, ds), os.path.join(OUT, f"{name}_Icon.png"))
import json; print(json.dumps(sizes))
