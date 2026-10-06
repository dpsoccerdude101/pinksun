#!/usr/bin/env python3
"""Capture just the hero mark from each world, plus a side-by-side with the shirt proof."""
import os
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = "/data/pinksun/site"
R = os.path.join(ROOT, ".impeccable/review")
WORLDS = [("board", "index.html"), ("crayon", "v/crayon/index.html"), ("notebook", "v/notebook/index.html")]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    for name, page in WORLDS:
        m = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3,
                          is_mobile=True, has_touch=True)
        pg = m.new_page()
        pg.goto("file://" + os.path.join(ROOT, page), wait_until="networkidle")
        pg.wait_for_timeout(1600)
        y = pg.evaluate("""() => { const a = document.querySelector('.hero-art');
            const s = document.querySelector('.scribble');
            return { top: a.getBoundingClientRect().top, bottom: s.getBoundingClientRect().bottom }; }""")
        pg.screenshot(path=f"{R}/{name}-mark.png",
                      clip={"x": 0, "y": max(0, y["top"] - 10), "width": 390,
                            "height": y["bottom"] - y["top"] + 18})
        m.close()
    b.close()

panels = [("PROOF (t-shirt)", Image.open("/data/pinksun/shots/proof-artwork.png").convert("RGB"))]
panels += [(n.title(), Image.open(f"{R}/{n}-mark.png").convert("RGB")) for n, _ in WORLDS]
H, pad, lab = 560, 16, 30
scaled = [(l, im.resize((int(im.width * (H / im.height)), H), Image.LANCZOS)) for l, im in panels]
W = sum(s.width for _, s in scaled) + pad * (len(scaled) + 1)
canvas = Image.new("RGB", (W, H + lab + pad * 2), (250, 250, 248))
d = ImageDraw.Draw(canvas)
x = pad
for label, s in scaled:
    canvas.paste(s, (x, lab + pad))
    d.text((x + 4, 10), label, fill=(20, 20, 20))
    x += s.width + pad
canvas.save("/data/pinksun/shots/mark-comparison.png")
print("wrote mark-comparison.png", canvas.size)
