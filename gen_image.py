#!/usr/bin/env python3
"""Draw the front page for Thursday 26 November 2026 as a 1024x1024 PNG.

Pure PIL, no network, no clock, no randomness: the same input always
produces the same bytes. Run: python3 gen_image.py [out.png]

Layout (1024x1024, all coordinates hand-measured so no text ever leaves
its card): masthead 0-134; lead card 148-496; row 2 cards 510-748;
row 3 cards 762-956; footer band 972-1024.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
NAVY_DARK = (13, 22, 41)
RED = (180, 35, 24)
GOLD = (201, 162, 39)
INK = (26, 26, 26)
GREY = (90, 88, 80)
CARD = (255, 253, 247)
ORANGE = (232, 116, 30)
FLAME = (245, 178, 44)
SMOKE = (120, 118, 112)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, x0, y0, x1, y1):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6,
                           fill=CARD, outline=(200, 192, 172), width=2)


def kicker(draw, x, y, text, size=20):
    f = font(SANS_B, size)
    draw.text((x, y), text, font=f, fill=RED)
    return y + size + 8


def headline(draw, x, y, text, size, max_w):
    f = font(SERIF_B, size)
    ld = int(size * 1.12)
    lines = wrap(draw, text, f, max_w)
    return draw_lines(draw, lines, x, y, f, INK, ld)


def caption(draw, x, y, text, size, max_w):
    f = font(SANS, size)
    ld = int(size * 1.3)
    lines = wrap(draw, text, f, max_w)
    return draw_lines(draw, lines, x, y, f, GREY, ld)


# ---------------------------------------------------------------- refinery art
# Box is 460 wide x 316 tall. Ground line at 5/6 height; every element is
# placed relative to the box so nothing paints outside it.
def draw_refinery(draw, x0, y0, x1, y1):
    """Stylised oil refinery at dusk: dark sky, tanks, towers, flames."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY_DARK)
    draw.rectangle([x0, y0 + (y1 - y0) * 2 // 3, x1, y1], fill=(58, 48, 66))
    gy = y0 + (y1 - y0) * 5 // 6
    draw.rectangle([x0, gy, x1, y1], fill=(24, 20, 18))
    # storage tanks
    tx, tw, th = x0 + 18, 92, 96
    for i in range(2):
        bx = tx + i * 112
        draw.rectangle([bx, gy - th, bx + tw, gy], fill=(74, 78, 92),
                       outline=(140, 140, 150), width=2)
        draw.ellipse([bx - 4, gy - th - 12, bx + tw + 4, gy - th + 12],
                     fill=(96, 100, 114), outline=(140, 140, 150), width=2)
        draw.line([bx + 8, gy - th + 26, bx + tw - 8, gy - th + 26],
                  fill=(140, 140, 150), width=2)
    # distillation towers
    for bx, th2 in ((x0 + 268, 190), (x0 + 330, 150)):
        draw.rectangle([bx, gy - th2, bx + 34, gy], fill=(88, 90, 104),
                       outline=(150, 150, 160), width=2)
        for k in range(4):
            yy = gy - th2 + 22 + k * 36
            draw.line([bx, yy, bx + 34, yy], fill=(150, 150, 160), width=2)
        draw.polygon([(bx, gy - th2), (bx + 17, gy - th2 - 26),
                      (bx + 34, gy - th2)], fill=(120, 122, 134))
    # flare stack with flame (tip kept inside the box)
    fx = x1 - 52
    draw.rectangle([fx - 5, gy - 180, fx + 5, gy], fill=(70, 72, 84))
    draw.polygon([(fx - 26, gy - 188), (fx, gy - 228), (fx + 26, gy - 188)],
                 fill=ORANGE)
    draw.polygon([(fx - 14, gy - 186), (fx, gy - 214), (fx + 14, gy - 186)],
                 fill=FLAME)
    # smoke clouds
    for cx, cy, r in ((x0 + 90, y0 + 46, 34), (x0 + 150, y0 + 30, 26),
                      (x0 + 300, y0 + 40, 30)):
        draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=SMOKE)
    # small flames at tank bases
    for bx in (x0 + 52, x0 + 168):
        draw.polygon([(bx - 16, gy), (bx, gy - 34), (bx + 16, gy)],
                     fill=ORANGE)
        draw.polygon([(bx - 8, gy), (bx, gy - 20), (bx + 8, gy)], fill=FLAME)
    # price tag, sized to the text so nothing spills out of the white box
    tag = "BRENT CRUDE  $94+"
    tf = font(SANS_B, 22)
    twd = draw.textlength(tag, font=tf)
    draw.rounded_rectangle([x0 + 12, y0 + 12, x0 + 24 + twd + 12, y0 + 52],
                           radius=6, fill=(255, 253, 247))
    draw.text((x0 + 24, y0 + 20), tag, font=tf, fill=RED)


# ---------------------------------------------------------------- tariff art
# Box is 440 wide x 96 tall: title top-left, subtitle top-right, four
# rising bars along the bottom.
def draw_tariffs(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(232, 236, 242))
    draw.text((x0 + 16, y0 + 8), "TARIFFS UP TO 15%",
              font=font(SANS_B, 22), fill=RED)
    sub = "TAIWAN  -1,926"
    sf = font(SANS_B, 17)
    draw.text((x1 - 16 - draw.textlength(sub, font=sf), y0 + 11), sub,
              font=sf, fill=INK)
    base = y1 - 8
    bars = [(0.30, (22, 35, 63)), (0.52, (60, 80, 120)),
            (0.78, (150, 60, 40)), (1.00, RED)]
    bw, gap = 64, 30
    x = x0 + 24
    for frac, col in bars:
        bh = int((y1 - y0 - 44) * frac)
        draw.rectangle([x, base - bh, x + bw, base], fill=col)
        x += bw + gap
    draw.line([x0 + 16, base, x1 - 16, base], fill=INK, width=3)


# ---------------------------------------------------------------- cairo art
# Box is 440 wide x 96 tall: night sky, converging road, small tanker
# with flames — all inside the box.
def draw_cairo(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(38, 32, 40))
    draw.polygon([(x0, y1), (x0 + 150, y0 + 44), (x1 - 150, y0 + 44),
                  (x1, y1)], fill=(70, 66, 70))
    draw.line([(x0 + 200, y0 + 44), (x0 + 110, y1)], fill=(220, 200, 90),
              width=4)
    draw.line([(x1 - 200, y0 + 44), (x1 - 110, y1)], fill=(220, 200, 90),
              width=4)
    tx, ty = x0 + 110, y0 + 52
    draw.rounded_rectangle([tx, ty, tx + 170, ty + 26], radius=12,
                           fill=(150, 152, 160), outline=(200, 200, 205),
                           width=2)
    draw.rectangle([tx + 170, ty + 8, tx + 205, ty + 26],
                   fill=(120, 122, 130))
    for wx in (tx + 24, tx + 118, tx + 182):
        draw.ellipse([wx, ty + 22, wx + 14, ty + 34], fill=(20, 20, 20))
    cx = tx + 85
    draw.polygon([(cx - 30, ty), (cx - 4, ty - 34), (cx + 16, ty - 18),
                  (cx + 30, ty)], fill=ORANGE)
    draw.polygon([(cx - 16, ty), (cx, ty - 22), (cx + 16, ty)], fill=FLAME)
    for sx, sy, r in ((cx - 52, ty - 38, 13), (cx + 34, ty - 42, 15)):
        draw.ellipse([sx - r, sy - r // 2, sx + r, sy + r // 2], fill=SMOKE)


# ---------------------------------------------------------------- mercury art
# Box is 280 wide x 68 tall.
def draw_mercury(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(12, 16, 34))
    for sx, sy in ((x0 + 16, y0 + 10), (x0 + 190, y0 + 8),
                   (x0 + 250, y0 + 50), (x0 + 30, y0 + 56)):
        draw.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 255, 255))
    cx, cy, r = x0 + 92, y0 + 34, 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(176, 160, 140))
    for ox, oy, orr in ((-10, -8, 5), (9, 6, 6), (-3, 13, 4), (13, -12, 4)):
        draw.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr,
                      cy + oy + orr], fill=(140, 126, 110))
    draw.rectangle([x0 + 196, y0 + 26, x0 + 228, y0 + 40],
                   fill=(200, 205, 215))
    draw.polygon([(x0 + 228, y0 + 26), (x0 + 246, y0 + 33),
                  (x0 + 228, y0 + 40)], fill=(160, 165, 178))
    draw.line([x0 + 196, y0 + 33, x0 + 176, y0 + 33], fill=GOLD, width=4)


# ---------------------------------------------------------------- chess art
# Box is 288 wide x 68 tall: a centred 4x4 board, 16 px squares.
def draw_chess(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(240, 232, 214))
    sq = 16
    ox = x0 + (x1 - x0 - 4 * sq) // 2
    oy = y0 + 2
    for r in range(4):
        for c in range(4):
            fill = (250, 248, 240) if (r + c) % 2 == 0 else (60, 52, 44)
            draw.rectangle([ox + c * sq, oy + r * sq,
                            ox + (c + 1) * sq, oy + (r + 1) * sq], fill=fill)
    draw.ellipse([ox + 4, oy + 4, ox + sq - 4, oy + sq - 4], fill=(20, 20, 20))
    draw.ellipse([ox + 3 * sq + 4, oy + 3 * sq + 4,
                  ox + 4 * sq - 4, oy + 4 * sq - 4],
                 fill=(245, 245, 240), outline=(20, 20, 20), width=2)


# ---------------------------------------------------------------- swiss art
# Box is 280 wide x 68 tall: Swiss flag, cross sized to fit the box.
def draw_swiss(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(200, 40, 32))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.rectangle([cx - 10, cy - 26, cx + 10, cy + 26],
                   fill=(255, 255, 255))
    draw.rectangle([cx - 26, cy - 10, cx + 26, cy + 10],
                   fill=(255, 255, 255))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 128], fill=NAVY)
    d.text((W // 2, 12), "THE WORLD", font=font(SERIF_B, 74),
           fill=(255, 253, 247), anchor="ma")
    d.text((W // 2, 96), "THURSDAY 26 NOVEMBER 2026",
           font=font(SANS_B, 24), fill=GOLD, anchor="ma")
    d.rectangle([0, 128, W, 134], fill=GOLD)

    # ---- lead story: Houthi strike on Ras Tanura ----
    card(d, 24, 148, 1000, 496)
    draw_refinery(d, 40, 164, 500, 480)
    tx = 524
    y = kicker(d, tx, 168, "MIDDLE EAST  •  ENERGY")
    y = headline(d, tx, y + 4, "HOUTHIS STRIKE SAUDI REFINERY", 40, 452)
    y = caption(d, tx, y + 10,
                "Ras Tanura hit and Riyadh's financial district targeted; "
                "Brent tops $94 on fears for Gulf supplies.", 22, 452)
    d.line([tx, 452, 984, 452], fill=(200, 192, 172), width=2)
    d.text((tx, 462), "YEMEN'S HOUTHIS CLAIM THE ATTACK",
           font=font(SANS_B, 19), fill=RED)

    # ---- row 2: tariffs + Cairo ----
    card(d, 24, 510, 496, 748)
    draw_tariffs(d, 40, 526, 480, 622)
    y = kicker(d, 40, 630, "TRADE  •  USA")
    y = headline(d, 40, y + 2, "TRUMP READIES NEW TARIFFS", 23, 440)
    caption(d, 40, y + 6,
            "Up to 15% on Taiwan goods; Taiwan shares fall 1,926 points.",
            18, 440)

    card(d, 528, 510, 1000, 748)
    draw_cairo(d, 544, 526, 984, 622)
    y = kicker(d, 544, 630, "EGYPT  •  CAIRO")
    y = headline(d, 544, y + 2, "CAIRO TANKER FIRE KILLS 30", 23, 440)
    caption(d, 544, y + 6,
            "Fuel tanker crash ignites a huge blaze on a highway ringing "
            "the capital.", 18, 440)

    # ---- row 3: Mercury, Swiss expulsion, chess ----
    card(d, 24, 762, 336, 956)
    draw_mercury(d, 40, 774, 320, 842)
    y = kicker(d, 40, 848, "SPACE")
    y = headline(d, 40, y + 2, "BEPICOLOMBO REACHES MERCURY", 20, 280)
    caption(d, 40, y + 4, "Orbit after an 8-year voyage.", 16, 280)

    card(d, 352, 762, 664, 956)
    draw_swiss(d, 368, 774, 648, 842)
    y = kicker(d, 368, 848, "DIPLOMACY")
    y = headline(d, 368, y + 2, "N. KOREA EXPELS SWISS DIPLOMAT", 20, 280)
    caption(d, 368, y + 4, "Shut in a sanctions row.", 16, 280)

    card(d, 680, 762, 1000, 956)
    draw_chess(d, 696, 774, 984, 842)
    y = kicker(d, 696, 848, "CHESS  •  WORLD TITLE")
    y = headline(d, 696, y + 2, "GUKESH–SINDAROV DRAW", 20, 288)
    caption(d, 696, y + 4, "Game 2 ends in a 20-move draw.", 16, 288)

    # ---- footer strip ----
    d.rectangle([0, 972, W, H], fill=NAVY)
    d.text((W // 2, 984),
           "ALSO TODAY: Solomon Islands–Australia sign a security treaty  •  "
           "India marks the 26/11 anniversary",
           font=font(SANS, 19), fill=(255, 253, 247), anchor="ma")

    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} {W}x{H}")


if __name__ == "__main__":
    main()
