#!/usr/bin/env python3
"""Verify the deployed site after the logo and town changes."""
import json
from playwright.sync_api import sync_playwright

BASE = "https://dpsoccerdude101.github.io/pinksun/"
WORLDS = [("board", ""), ("crayon", "v/crayon/"), ("notebook", "v/notebook/")]
EXPECT = {"board": "rgb(36, 44, 40)", "crayon": "rgb(30, 79, 146)", "notebook": "rgb(252, 252, 250)"}

out, fails = {}, []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    for name, slug in WORLDS:
        m = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                          is_mobile=True, has_touch=True)
        pg = m.new_page()
        errs, failed = [], []
        pg.on("console", lambda x: errs.append(f"{x.type}: {x.text}") if x.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: failed.append(r.url))
        pg.goto(BASE + slug, wait_until="networkidle")
        pg.wait_for_timeout(2200)
        d = pg.evaluate("""() => ({
            bg: getComputedStyle(document.body).backgroundColor,
            fonts: ['Gloria Hallelujah','Patrick Hand','Archivo'].map(f => document.fonts.check('20px "'+f+'"')),
            rays: document.querySelectorAll('#sun line').length,
            domeR: document.querySelector('#sun path').getAttribute('d'),
            script: document.querySelector('.scribble').textContent.trim(),
            wren: document.body.innerText.includes('Wren Hollow'),
            fairport: document.body.innerText.includes('Fairport'),
            markAria: (document.querySelector('.sun')||{}).getAttribute ? document.querySelector('.sun').getAttribute('aria-label') : '',
            scrollW: document.documentElement.scrollWidth,
            ctaBottom: Math.round(document.querySelector('[data-cta=primary]').getBoundingClientRect().bottom),
            theme: (document.querySelector('meta[name=theme-color]')||{}).content,
        })""")
        pg.screenshot(path=f"/data/pinksun/site/.impeccable/review/live-{name}-mobile.png")
        out[name] = d
        if errs: fails.append(f"{name}: console {errs[:2]}")
        if failed: fails.append(f"{name}: failed {failed[:2]}")
        if d["bg"] != EXPECT[name]: fails.append(f"{name}: ground {d['bg']} != {EXPECT[name]}")
        if not all(d["fonts"]): fails.append(f"{name}: fonts {d['fonts']}")
        if d["rays"] != 12: fails.append(f"{name}: {d['rays']} rays, expected 12")
        if d["script"] != "pink sun": fails.append(f"{name}: script is {d['script']!r}")
        if not d["wren"]: fails.append(f"{name}: town missing")
        if d["fairport"]: fails.append(f"{name}: Fairport still present")
        if d["scrollW"] > 392: fails.append(f"{name}: overflow {d['scrollW']}")
        if d["ctaBottom"] > 844: fails.append(f"{name}: primary CTA below the fold ({d['ctaBottom']})")
        m.close()
    ctx = b.new_context()
    pg = ctx.new_page()
    for f in ["assets/fonts/gloria-hallelujah-f3c465.woff2", "assets/fonts.css", "assets/chalk.css",
              "assets/crayon.css", "assets/notebook.css", "v/crayon/", "v/notebook/"]:
        st = pg.request.get(BASE + f).status
        if st != 200: fails.append(f"{f}: HTTP {st}")
    ctx.close()
    b.close()

print(json.dumps(out, indent=1))
print("=" * 58)
if fails:
    print(f"FAIL ({len(fails)})")
    for f in fails:
        print("  x", f)
else:
    print("PASS — live site: mark, town, fonts and funnel all check out.")
