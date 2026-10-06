#!/usr/bin/env python3
"""Capture the reshaped landing page: full page plus the two new sections, per world."""
import os
from playwright.sync_api import sync_playwright

ROOT = "/data/pinksun/site"
OUT = "/data/pinksun/shots/childlike"
os.makedirs(OUT, exist_ok=True)
WORLDS = {"board": "index.html", "crayon": "v/crayon/index.html", "notebook": "v/notebook/index.html"}

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    for name, page in WORLDS.items():
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                            is_mobile=True, has_touch=True)
        pg = ctx.new_page()
        pg.goto("file://" + os.path.join(ROOT, page), wait_until="networkidle")
        pg.wait_for_timeout(1800)
        pg.screenshot(path=f"{OUT}/{name}-full.png", full_page=True)
        for sec in ("play", "visit"):
            el = pg.query_selector(f"#{sec}")
            if el:
                el.screenshot(path=f"{OUT}/{name}-{sec}.png")
        h = pg.evaluate("document.documentElement.scrollHeight")
        rows = pg.evaluate("document.querySelectorAll('.row').length")
        print(f"{name}: height={h} rows={rows}")
        ctx.close()
    b.close()
print("shots written to", OUT)
