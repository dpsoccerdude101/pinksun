#!/usr/bin/env python3
"""Compose the review images for the reshaped landing page.

1. shots/childlike/hierarchy.jpg - the price list stacked over the visit section,
   in all three materials, side by side.
2. shots/childlike/board-whole.jpg - the whole board page, one column, so the
   shape of the funnel is visible at a glance.
"""
import os
from PIL import Image, ImageDraw

S = "/data/pinksun/shots/childlike"
PANELS = [("board", "A · chalk on the dark board"), ("crayon", "B · crayon on blue paper"),
          ("notebook", "C · ballpoint on ruled paper")]
GAP = 26
LABEL = 44
BAR = (250, 246, 240)


def labelled(img, text, width):
    h = int(img.height * width / img.width)
    im = img.resize((width, h), Image.LANCZOS)
    out = Image.new("RGB", (width, h + LABEL), BAR)
    out.paste(im, (0, LABEL))
    d = ImageDraw.Draw(out)
    d.rectangle([0, 0, width, LABEL - 8], fill=(34, 40, 37))
    d.text((14, 15), text, fill=(250, 246, 240))
    return out


def stack(a, b, gap=10):
    w = max(a.width, b.width)
    out = Image.new("RGB", (w, a.height + gap + b.height), (235, 231, 224))
    out.paste(a, (0, 0))
    out.paste(b, (0, a.height + gap))
    return out


os.makedirs(S, exist_ok=True)
PANEL_W = 460
cols = []
for key, label in PANELS:
    top = labelled(Image.open(f"{S}/{key}-play.png").convert("RGB"), label, PANEL_W)
    bottom = Image.open(f"{S}/{key}-visit.png").convert("RGB")
    bottom = bottom.resize((PANEL_W, int(bottom.height * PANEL_W / bottom.width)), Image.LANCZOS)
    cols.append(stack(top, bottom))

H = max(c.height for c in cols)
W = sum(c.width for c in cols) + GAP * (len(cols) + 1)
sheet = Image.new("RGB", (W, H + GAP * 2), (235, 231, 224))
x = GAP
for c in cols:
    sheet.paste(c, (x, GAP))
    x += c.width + GAP
sheet.save(f"{S}/hierarchy.jpg", quality=88, optimize=True)
print("hierarchy.jpg", sheet.size)

whole = Image.open(f"{S}/board-full.png").convert("RGB")
w = 430
whole = whole.resize((w, int(whole.height * w / whole.width)), Image.LANCZOS)
# a 1:9 strip is unreadable in a chat, so split the page in half and set the
# halves side by side, like a folded poster.
half = whole.height // 2
left = whole.crop((0, 0, whole.width, half))
right = whole.crop((0, half, whole.width, whole.height))
sheet_w = left.width * 2 + GAP * 3
sheet_h = max(left.height, right.height) + GAP * 2
two = Image.new("RGB", (sheet_w, sheet_h), (235, 231, 224))
two.paste(left, (GAP, GAP))
two.paste(right, (GAP * 2 + left.width, GAP))
# a hairline between the two halves so the seam reads as a fold
ImageDraw.Draw(two).rectangle([GAP * 2 + left.width - GAP // 2, GAP,
                               GAP * 2 + left.width - GAP // 2 + 1, GAP + sheet_h - GAP * 2],
                              fill=(190, 184, 174))
two.save(f"{S}/board-whole.jpg", quality=88, optimize=True)
print("board-whole.jpg", two.size)
