#!/usr/bin/env python3
"""og.png generator — LORE: Tea and Coffee (1200x630, shop identity only, no builder markers).
Letterpress storybook: parchment field + brass double-rule frame + Palatino book serif +
ink cup mark + espresso footer strip."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.environ.get("OG_OUT", "/Users/rleon/sites/lore-tea-and-coffee/public/og.png")
W, H = 1200, 630
PARCH = (246, 239, 223); INK = (36, 23, 19); JAM = (122, 47, 74)
BRASS = (154, 111, 44); RULE = (211, 191, 154); CREAM = (243, 231, 207); BRASSLT = (236, 201, 143)
INKSOFT = (107, 87, 72)

PALATINO = "/System/Library/Fonts/Palatino.ttc"

def font(size, index=0, stroke=0):
    try:
        f = ImageFont.truetype(PALATINO, size, index=index)
        return f
    except Exception:
        return ImageFont.load_default()

F_KICK = font(24)
F_DISP = font(168)
F_SUB  = font(72)
F_LINE = font(26)
F_STRIP= font(24)

img = Image.new("RGB", (W, H), PARCH)
d = ImageDraw.Draw(img)

def spaced(x, y, text, f, fill, sp=6):
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=f, fill=fill, stroke_width=1, stroke_fill=fill if fill != BRASSLT else fill)
        cx += d.textlength(ch, font=f) + sp
    return cx

# double letterpress rule frame (brass outer, light inner)
d.rectangle([22, 22, W - 23, H - 23], outline=BRASS, width=3)
d.rectangle([32, 32, W - 33, H - 33], outline=RULE, width=1)

# kicker
spaced(84, 84, "DOWNTOWN CAMAS  \u00b7  WASHINGTON", F_KICK, INKSOFT, sp=4)

# wordmark: "LORE:" huge Palatino + italic companion line
d.text((78, 122), "LORE:", font=F_DISP, fill=INK, stroke_width=2, stroke_fill=INK)
try:
    ital = ImageFont.truetype(PALATINO, 66, index=1)  # italic face
except Exception:
    ital = F_SUB
d.text((82, 320), "Tea and Coffee", font=ital, fill=JAM, stroke_width=1, stroke_fill=JAM)

# steaming-cup mark, connected line work, right side
def steam(x, y):
    p = [(x, y)]
    for k in range(6):
        p.append((x + (10 if k % 2 else -10), y - 14 * (k + 1)))
    d.line(p, fill=INK, width=5, joint="curve")
steam(912, 244); steam(972, 230); steam(1032, 244)
cup_pts = [(872, 282), (1078, 282), (1054, 332), (1022, 346), (928, 346), (896, 332)]
d.polygon(cup_pts, fill=(255, 250, 240), outline=INK, width=5)
# jam band flush to the inner rim corners (no notch)
band = [(872, 282), (1078, 282), (1071, 297), (879, 297)]
d.polygon(band, fill=JAM)
d.line([(872, 282), (1078, 282)], fill=INK, width=5)                       # rim closing stroke
d.polygon([(852, 366), (1104, 366), (1096, 373), (860, 373)], fill=BRASS)  # saucer

# promise line + chips
spaced(84, 420, "COFFEE  \u00b7  TEA  \u00b7  FRIDAY COCKTAIL NIGHTS", F_LINE, INK, sp=3)
spaced(84, 458, "4.8 STARS ON GOOGLE  \u00b7  OPEN SEVEN DAYS", F_KICK, JAM, sp=2)

# espresso footer strip
d.rectangle([32, H - 96, W - 33, H - 33], fill=INK)
d.text((84, H - 82), "536 NE 5th Ave  \u00b7  (360) 980-9210  \u00b7  Hidden River roasts on the menu", font=F_STRIP, fill=BRASSLT)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size)
