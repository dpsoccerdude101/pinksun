#!/usr/bin/env python3
"""Measure whether each world's sun fill is flat or material.

The dome is a solid shape in the source artwork, so any visible variation inside it
comes from the world's material filter. A flat vector fill measures near zero; chalk
and wax measure high. This gives a number instead of an opinion.

Prints, per world: the dome region's luminance standard deviation, and how many
distinct luminance levels survive in it.
"""
import io
from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

ROOT = "file:///data/pinksun/site"
PAGES = {"board": f"{ROOT}/index.html", "crayon": f"{ROOT}/v/crayon/index.html",
         "notebook": f"{ROOT}/v/notebook/index.html"}

def dome_stats(png_bytes):
    im = Image.open(io.BytesIO(png_bytes)).convert("L")
    w, h = im.size
    # strictly inside the dome (path spans x 66-134, y 70-104 of a 200x112 mark),
    # so no background or dome edge is in the sample: this is fill character only
    box = (int(w * 0.40), int(h * 0.72), int(w * 0.60), int(h * 0.88))
    crop = im.crop(box)
    st = ImageStat.Stat(crop)
    levels = len(set(crop.getdata()))
    return st.stddev[0], levels, st.mean[0], crop.size

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    for name, url in PAGES.items():
        pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg.goto(url, wait_until="load")
        pg.wait_for_timeout(900)
        el = pg.locator(".sun").first
        png = el.screenshot()
        sd, lv, mean, size = dome_stats(png)
        print(f"{name:9} stddev={sd:6.2f}  levels={lv:4d}  mean={mean:6.1f}  crop={size}")
        open(f"/tmp/dome-{name}.png", "wb").write(png)
        pg.close()
    b.close()
