#!/usr/bin/env python3
"""Check that every price row shows its arrow in all three worlds."""
from playwright.sync_api import sync_playwright

ROOT = "file:///data/pinksun/site"
PAGES = {"board": f"{ROOT}/index.html", "crayon": f"{ROOT}/v/crayon/index.html",
         "notebook": f"{ROOT}/v/notebook/index.html"}

JS = """() => [...document.querySelectorAll('.row')].map(r => {
  const a = r.querySelector('.arw');
  if (!a) return 'NO ARROW ELEMENT';
  const cs = getComputedStyle(a);
  const b = a.getBoundingClientRect();
  const u = a.querySelector('use');
  return {
    row: r.querySelector('.nm').textContent.trim(),
    w: Math.round(b.width), h: Math.round(b.height),
    color: cs.color, opacity: cs.opacity,
    useHref: u ? u.getAttribute('href') : 'none',
    // the referenced graphic's own ink, which is what actually paints
    refFill: (() => { const s = document.querySelector('svg use[href="#arrowR"]');
      const def = document.querySelector('#arrowR');
      return def ? (getComputedStyle(def).stroke || 'n/a') : 'DEF MISSING'; })(),
  };
})"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    for name, url in PAGES.items():
        pg = b.new_page(viewport={"width": 390, "height": 844})
        pg.goto(url, wait_until="load")
        pg.wait_for_timeout(400)
        rows = pg.evaluate(JS)
        print(f"--- {name}")
        for r in rows:
            if isinstance(r, str):
                print("   ", r)
            else:
                print(f"    {r['row'][:22]:24} box={r['w']}x{r['h']} color={r['color']} "
                      f"href={r['useHref']} defStroke={r['refFill']}")
        pg.close()
    b.close()
