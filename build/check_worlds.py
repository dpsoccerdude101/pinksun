#!/usr/bin/env python3
"""Check every world in the childlike build: funnel contract, mobile geometry, dead links."""
import json, os, urllib.parse
from playwright.sync_api import sync_playwright

ROOT = "/data/pinksun/site"
WORLDS = {
    "board": "index.html",
    "crayon": "v/crayon/index.html",
    "notebook": "v/notebook/index.html",
}
REVIEW = os.path.join(ROOT, ".impeccable/review")

def resolve(page, href):
    if not href or href.startswith(("#", "mailto:", "tel:", "http:", "https:", "data:")):
        return None
    base = os.path.dirname(os.path.join(ROOT, page))
    t = os.path.normpath(os.path.join(base, urllib.parse.urlparse(href).path))
    if t.endswith(os.sep) or not os.path.splitext(t)[1]:
        t = os.path.join(t, "index.html")
    return t

fails, report = [], {}
os.makedirs(REVIEW, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    for name, page in WORLDS.items():
        url = "file://" + os.path.join(ROOT, page)
        m = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                          is_mobile=True, has_touch=True)
        pg = m.new_page()
        errs, failed = [], []
        pg.on("console", lambda x: errs.append(f"{x.type}: {x.text}") if x.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: failed.append(r.url))
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_timeout(1700)
        pg.screenshot(path=f"{REVIEW}/{name}-mobile.png")
        if name != "board":
            pg.screenshot(path=f"{REVIEW}/{name}-full.png", full_page=True)
        d = pg.evaluate("""() => {
            const ctrls = [...document.querySelectorAll('a.btn,button.btn,a.curl,.actionbar a,.strip .logo')]
              .filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; })
              .map(e => { const r = e.getBoundingClientRect(); return [e.textContent.trim().slice(0,24), Math.round(r.width), Math.round(r.height)]; });
            return {
              primary: document.querySelectorAll('[data-cta="primary"]').length,
              nav: document.querySelectorAll('[data-cta="nav"]').length,
              booking: document.querySelectorAll('[data-booking]').length,
              close: document.querySelectorAll('.close').length,
              ctrls, links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')),
              fonts: ['Gloria Hallelujah','Patrick Hand','Archivo'].map(f => document.fonts.check('20px "'+f+'"')),
              scrollW: document.documentElement.scrollWidth,
              padBottom: getComputedStyle(document.body).paddingBottom,
              filterIds: [...document.querySelectorAll('filter')].map(f => f.id),
              themeColor: (document.querySelector('meta[name=theme-color]')||{}).content || '',
            };
        }""")
        pg.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        pg.wait_for_timeout(500)
        occ = pg.evaluate("""() => { const bar = document.querySelector('.actionbar').getBoundingClientRect();
            const last = document.querySelector('footer .fine').getBoundingClientRect();
            return { clear: last.bottom < bar.top, barTop: Math.round(bar.top), lastBottom: Math.round(last.bottom) }; }""")

        if errs: fails.append(f"{name}: console {errs[:2]}")
        if failed: fails.append(f"{name}: failed {failed[:2]}")
        if d["scrollW"] > 392: fails.append(f"{name}: overflow {d['scrollW']}")
        if d["primary"] != 1: fails.append(f"{name}: primary CTA = {d['primary']}")
        if d["nav"] != 1: fails.append(f"{name}: nav CTA = {d['nav']}")
        if d["close"] != 1: fails.append(f"{name}: close block = {d['close']}")
        if not all(d["fonts"]): fails.append(f"{name}: font missing {d['fonts']}")
        # each world draws its own material: the board chalks, the crayon waxes,
        # the notebook inks. Asserting one shared id would only pass by accident.
        want_filter = {"board": "chalk", "crayon": "chalkmark", "notebook": "ink"}.get(name)
        if want_filter and want_filter not in d["filterIds"]:
            fails.append(f"{name}: material filter #{want_filter} missing (has {d['filterIds']})")
        if not occ["clear"]: fails.append(f"{name}: bottom bar occludes footer")
        small = [c for c in d["ctrls"] if c[2] < 44]
        if small: fails.append(f"{name}: controls under 44px {small}")
        for h in d["links"]:
            t = resolve(page, h)
            if t and not os.path.exists(t):
                fails.append(f"{name}: dead link {h}")
        report[name] = {"primary": d["primary"], "nav": d["nav"], "booking": d["booking"],
                        "controls": len(d["ctrls"]), "scrollW": d["scrollW"],
                        "barClear": occ["clear"], "padBottom": d["padBottom"],
                        "theme": d["themeColor"]}
        m.close()

    for name, page in WORLDS.items():
        ctx = b.new_context(viewport={"width": 1440, "height": 960})
        pg = ctx.new_page()
        pg.goto("file://" + os.path.join(ROOT, page), wait_until="networkidle")
        pg.wait_for_timeout(1500)
        pg.screenshot(path=f"{REVIEW}/{name}-desktop.png")
        report[name]["desktopScrollW"] = pg.evaluate("document.documentElement.scrollWidth")
        ctx.close()
    b.close()

print(json.dumps(report, indent=1))
print("=" * 60)
if fails:
    print(f"FAIL ({len(fails)})")
    for f in fails:
        print("  x", f)
    raise SystemExit(1)
print("PASS — three worlds, funnel and mobile contract hold.")
