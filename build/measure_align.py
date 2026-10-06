from playwright.sync_api import sync_playwright as sp
S = ".top .strip .logo .who .actionbar .hero h1 .hero-art .sun .scribble"
JS = "(()=>{const o={};for(const s of '%s'.split(' ')){const e=document.querySelector(s);if(!e){o[s]=null;continue}const r=e.getBoundingClientRect();o[s]=[Math.round(r.left),Math.round(r.right)]}return {vw:innerWidth,o}})()" % S
with sp() as p:
    b = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 390, "height": 900})
    pg.goto("file:///data/pinksun/site/v/notebook/index.html")
    for w in (390, 640, 1024):
        pg.set_viewport_size({"width": w, "height": 900})
        d = pg.evaluate(JS)
        print("vp", w, "sheet centre", w / 2, d["o"])
    b.close()
