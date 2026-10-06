from playwright.sync_api import sync_playwright as sp
JS = """(()=>{const g=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.right),Math.round((r.left+r.right)/2)]};return {vw:innerWidth,hero:g('.hero'),h1:g('h1'),lede:g('.lede'),refH2:g('#visit h2'),sun:g('.sun'),scr:g('.scribble')}})()"""
with sp() as p:
    b = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 390, "height": 900})
    pg.goto("file:///data/pinksun/site/v/notebook/index.html")
    for w in (390, 640, 1024):
        pg.set_viewport_size({"width": w, "height": 900})
        d = pg.evaluate(JS)
        print("vp", w, "sheet centre", round(w / 2, 1), "[L,R,C]", d)
    b.close()
