#!/usr/bin/env python3
"""Draw the news-image-20261117 front page (1024x1024) with PIL.

Newspaper front-page style: masthead + date, lead story (Kerch Bridge)
with a drawn bridge illustration, then a 3x2 grid of five more stories
plus an 'Also in the news' box. Everything is drawn with PIL shapes;
no photographs, no network, no invented facts.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (248, 245, 238)
INK = (20, 20, 20)
RED = (178, 34, 34)
NAVY = (30, 50, 90)
GREY = (90, 90, 90)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def centered(d, cx, y, text, fnt, fill):
    w = fnt.getlength(text)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- icons
def icon_aid(d, x, y, s=48):
    # humanitarian aid box with a cross
    d.rectangle([x + 4, y + 14, x + s - 4, y + s - 4], fill=(185, 138, 74),
                outline=INK, width=2)
    d.rectangle([x + 4, y + 14, x + s - 4, y + 24], fill=(150, 105, 50),
                outline=INK, width=2)
    cx, cy = x + s // 2, y + s // 2 + 4
    d.rectangle([cx - 4, cy - 10, cx + 4, cy + 10], fill=(255, 255, 255))
    d.rectangle([cx - 10, cy - 4, cx + 10, cy + 4], fill=(255, 255, 255))


def icon_globe(d, x, y, s=48):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(74, 127, 181),
              outline=INK, width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(255, 255, 255),
              width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 180,
          fill=(255, 255, 255), width=2)


def icon_jet(d, x, y, s=48):
    # simple delta jet, nose to the upper right
    d.polygon([(x + 6, y + s - 8), (x + s - 4, y + 8), (x + s - 16, y + s - 10)],
              fill=(70, 70, 70))
    d.polygon([(x + 10, y + s - 14), (x + 22, y + s - 26), (x + 26, y + s - 12)],
              fill=(120, 120, 120))
    d.line([x + 4, y + s - 4, x + 16, y + s - 16], fill=GREY, width=2)
    d.line([x + 2, y + s - 10, x + 14, y + s - 22], fill=GREY, width=2)


def icon_gavel(d, x, y, s=48):
    # gavel: chunky head tilted 45 degrees + handle + sounding block
    # head as a rotated rectangle (polygon), two end caps
    d.polygon([(x + 12, y + 4), (x + 30, y + 4), (x + 38, y + 12),
               (x + 20, y + 12)], fill=(120, 80, 40), outline=INK)
    d.polygon([(x + 18, y + 14), (x + 36, y + 14), (x + 44, y + 22),
               (x + 26, y + 22)], fill=(150, 105, 55), outline=INK)
    d.line([x + 28, y + 20, x + 42, y + 36], fill=(90, 60, 30), width=5)
    d.line([x + 6, y + 42, x + 44, y + 42], fill=INK, width=3)


def icon_pin(d, x, y, s=48):
    cx, cy = x + s // 2, y + s // 2 - 4
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(178, 34, 34),
              outline=INK, width=2)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
    d.polygon([(cx - 8, cy + 9), (cx + 8, cy + 9), (cx, cy + 22)],
              fill=(178, 34, 34), outline=INK)


def icon_paper(d, x, y, s=48):
    d.rectangle([x + 8, y + 6, x + s - 8, y + s - 6], fill=(255, 255, 255),
                outline=INK, width=2)
    d.rectangle([x + 8, y + 6, x + s - 8, y + 14], fill=INK)
    for i, yy in enumerate((y + 20, y + 27, y + 34, y + 41)):
        d.line([x + 13, yy, x + s - 13, yy], fill=GREY, width=2)


# ------------------------------------------------------- bridge drawing
def draw_bridge(d, x0, y0, w, h):
    """Draw the Kerch Bridge: sea, deck with a broken gap, drooping arch,
    smoke plumes. x0,y0 top-left, w,h size of the illustration box."""
    # sky and sea
    d.rectangle([x0, y0, x0 + w, y0 + int(h * 0.55)], fill=(207, 227, 239))
    d.rectangle([x0, y0 + int(h * 0.55), x0 + w, y0 + h], fill=(127, 168, 201))
    # sun
    d.ellipse([x0 + w - 70, y0 + 14, x0 + w - 30, y0 + 54], fill=(240, 200, 90))
    # support pillars in the sea
    for px in (x0 + 70, x0 + w - 100):
        d.rectangle([px, y0 + int(h * 0.52), px + 16, y0 + h - 12],
                    fill=(90, 90, 90))
    deck_y = y0 + int(h * 0.52)
    # deck: left part, gap, right part (broken ends jagged)
    d.rectangle([x0 + 8, deck_y, x0 + int(w * 0.46), deck_y + 14], fill=(58, 58, 58))
    d.rectangle([x0 + int(w * 0.62), deck_y, x0 + w - 8, deck_y + 14],
                fill=(58, 58, 58))
    d.polygon([(x0 + int(w * 0.46), deck_y), (x0 + int(w * 0.46) + 12, deck_y + 7),
               (x0 + int(w * 0.46), deck_y + 14)], fill=(58, 58, 58))
    d.polygon([(x0 + int(w * 0.62), deck_y), (x0 + int(w * 0.62) - 12, deck_y + 7),
               (x0 + int(w * 0.62), deck_y + 14)], fill=(58, 58, 58))
    # arch: feet planted on the deck, left half standing, right half
    # snapped and drooping into the gap
    import math
    cx, rx = x0 + w // 2, w // 2 - 80
    top_y = y0 + 26
    ry = deck_y - top_y
    pts = []
    for i in range(0, 26):
        t = math.pi - (math.pi / 2) * i / 25  # left foot -> top
        pts.append((cx + rx * math.cos(t), deck_y - ry * math.sin(t)))
    d.line(pts, fill=(85, 85, 85), width=9, joint="curve")
    # drooping broken half: top -> sagging down into the gap
    d.line([(cx, top_y), (cx + 52, top_y + 42), (cx + 88, deck_y - 8)],
           fill=(85, 85, 85), width=9, joint="curve")
    # explosion flash at the gap
    gx, gy = x0 + w // 2, deck_y - 4
    d.polygon([(gx - 26, gy - 6), (gx - 8, gy - 22), (gx + 2, gy - 6),
               (gx + 20, gy - 18), (gx + 14, gy + 2), (gx + 26, gy + 8),
               (gx + 4, gy + 10), (gx - 6, gy + 20), (gx - 14, gy + 6)],
              fill=(232, 161, 58))
    # smoke plumes: clusters of overlapping circles above the gap
    for (sx, sy, r, col) in ((gx - 40, y0 + 16, 12, (150, 150, 150)),
                             (gx - 26, y0 + 6, 15, (120, 120, 120)),
                             (gx - 8, y0 + 14, 12, (170, 170, 170)),
                             (gx + 12, y0 + 2, 14, (120, 120, 120)),
                             (gx + 30, y0 + 12, 11, (150, 150, 150))):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=col)
    # label
    fnt = font(SANS_B, 15)
    d.text((x0 + 12, y0 + h - 24), "ROAD ARCH DOWN  ·  270m OF ROADWAY",
           font=fnt, fill=INK)


# ------------------------------------------------------------- main page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=3)

    # ---- masthead
    centered(d, W // 2, 30, "THE WORLD TODAY", font(SERIF_B, 60), INK)
    d.line([30, 102, W - 30, 102], fill=INK, width=2)

    # ---- date band (black, white text)
    d.rectangle([30, 110, W - 30, 152], fill=INK)
    centered(d, W // 2, 118, "TUESDAY 17 NOVEMBER 2026",
             font(SANS_B, 32), (255, 255, 255))

    # ---- lead story
    d.text((30, 166), "UKRAINE WAR", font=font(SANS_B, 22), fill=RED)
    d.text((30, 192), "KERCH BRIDGE SEVERED", font=font(SERIF_B, 54), fill=INK)
    sub = "Ukraine strikes badly damage the road and rail link to Crimea."
    d.text((30, 252), sub, font=font(SERIF, 24), fill=INK)

    # bridge illustration, left
    draw_bridge(d, 30, 292, 560, 215)
    # caption under illustration
    d.text((30, 512), "The bridge linking Russia to Crimea: traffic halted.",
           font=font(SANS, 17), fill=GREY)

    # right-hand fact column
    rx, rw = 622, W - 30 - 622
    y = 292
    facts = [
        "Road arch down — 270m of roadway destroyed",
        "Rail damaged; all traffic halted",
        "306 drones in one overnight attack",
    ]
    fnt = font(SANS, 20)
    for f in facts:
        lines = wrap_text("•  " + f, fnt, rw)
        y = draw_lines(d, rx, y, lines, fnt, INK, 27)
        y += 8
    y += 6
    d.line([rx, y, rx + rw, y], fill=INK, width=2)
    y += 12
    d.text((rx, y), "RUSSIA RETALIATES", font=font(SANS_B, 20), fill=RED)
    y += 30
    ret = ("Ballistic missiles hit Kyiv's Southern and Northern "
           "bridges.")
    y = draw_lines(d, rx, y, wrap_text(ret, fnt, rw), fnt, INK, 27)

    # ---- divider before the grid
    d.line([30, 556, W - 30, 556], fill=INK, width=3)

    # ---- grid: 3 columns x 2 rows, 5 stories + ALSO box
    cells = [
        ("FOUR NATIONS URGE GAZA AID ACCESS",
         "UK, Australia, Canada and Italy call on Israel to open "
         "crossings. Situation called catastrophic.",
         icon_aid),
        ("PUTIN IN SHENZHEN FOR APEC",
         "First Trump–Xi–Putin trilateral set; Xi urges free trade.",
         icon_globe),
        ("JAPAN SCRAMBLES JETS",
         "Russian aircraft violate Japanese airspace; Tokyo protests.",
         icon_jet),
        ("DEPARDIEU ADMITS ASSAULT",
         "Actor drops his appeal and admits a sexual assault charge "
         "in a Paris court.",
         icon_gavel),
        ("HOUTHIS PUSH TO ADEN",
         "Yemeni government forces retreat from the Red Sea coast "
         "to defend Aden.",
         icon_pin),
        ("ALSO IN THE NEWS",
         "Mongolia: president resigns amid a corruption scandal. "
         "US: loses measles elimination status after 26 years.",
         icon_paper),
    ]
    gx0, gy0 = 30, 572
    cw, ch = 310, 176
    gapx, gapy = 17, 14
    for i, (head, summ, icon) in enumerate(cells):
        cx = gx0 + (i % 3) * (cw + gapx)
        cy = gy0 + (i // 3) * (ch + gapy)
        d.line([cx, cy, cx + cw, cy], fill=INK, width=2)
        hy = cy + 10
        hlines = wrap_text(head, font(SERIF_B, 23), cw)
        hy = draw_lines(d, cx, hy, hlines, font(SERIF_B, 23), INK, 27)
        icon(d, cx, hy + 6)
        slines = wrap_text(summ, font(SANS, 17), cw - 58)
        draw_lines(d, cx + 58, hy + 8, slines, font(SANS, 17), INK, 21)

    # ---- footer
    fy = 952
    d.line([30, fy, W - 30, fy], fill=INK, width=2)
    centered(d, W // 2, fy + 10,
             "Sources: BBC  ·  Foreign Exchanges  ·  Standard Topic  ·  "
             "Meanwhile in Ukraine",
             font(SANS, 14), GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
