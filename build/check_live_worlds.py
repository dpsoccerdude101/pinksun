#!/usr/bin/env python3
"""Verify the deployed PinkSun worlds after the hierarchy reshape.

Asserts, per world: the five-row price list, the about section, one price surface,
hours in exactly one place, the mark, the town, and no horizontal overflow.
"""
from playwright.sync_api import sync_playwright

BASE = "https://dpsoccerdude101.github.io/pinksun/"
WORLDS = {
    "board": BASE,
    "crayon": BASE + "v/crayon/",
    "notebook": BASE + "v/notebook/",
}

JS = """() => {
  const t = document.body.innerText;
  return {
    rows: document.querySelectorAll('.row').length,
    rowNames: [...document.querySelectorAll('.row .nm')].map(e => e.textContent.trim()),
    rowPrices: [...document.querySelectorAll('.row .pr')].map(e => e.textContent.replace(/\\s+/g,' ').trim()),
    aboutP: document.querySelectorAll('.about p').length,
    aboutH2: (document.querySelector('#about h2') || {}).textContent || '',
    sections: [...document.querySelectorAll('main > section')].map(e => e.id),
    h2s: [...document.querySelectorAll('h2')].map(e => e.textContent.split('\\n')[0].trim()),
    hoursMentions: (t.match(/Monday to Friday/g) || []).length,
    freeMentions: (t.match(/first one is free|first session free/gi) || []).length,
    fairport: /fairport/i.test(t),
    wrenHollow: /Wren Hollow/.test(t),
    rays: document.querySelectorAll('#sun line').length,
    booking: document.querySelectorAll('[data-booking]').length,
    deep: document.querySelectorAll('[data-booking-path]').length,
    primary: document.querySelectorAll('[data-cta="primary"]').length,
    words: t.split(/\\s+/).filter(Boolean).length,
    scrollW: document.documentElement.scrollWidth,
  };
}"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
        fails = []
        for name, url in WORLDS.items():
            pg = b.new_page(viewport={"width": 390, "height": 844})
            pg.goto(url, wait_until="load")
            pg.wait_for_timeout(600)
            d = pg.evaluate(JS)
            print(f"--- {name}  ({url})")
            print(f"    sections   {d['sections']}")
            print(f"    h2         {d['h2s']}")
            print(f"    rows={d['rows']} aboutP={d['aboutP']} rays={d['rays']} "
                  f"primary={d['primary']} booking={d['booking']} deep={d['deep']} words={d['words']}")
            print(f"    prices     {d['rowPrices']}")
            print(f"    hours mentions={d['hoursMentions']} free-session mentions={d['freeMentions']} "
                  f"wren={d['wrenHollow']} fairport={d['fairport']} scrollW={d['scrollW']}")

            def want(cond, msg):
                if not cond:
                    fails.append(f"{name}: {msg}")

            want(d["rows"] == 5, f"expected 5 price rows, found {d['rows']}")
            for p in ["$12", "$95", "$45", "$40", "$120"]:
                want(any(p in x for x in d["rowPrices"]), f"row list is missing {p}")
            want(d["aboutP"] == 3, f"expected 3 about paragraphs, found {d['aboutP']}")
            want("who we are" in d["aboutH2"].lower(), "about section has no heading")
            want([s for s in d["sections"] if s] == ["tonight", "play", "about", "visit"]
                 and len(d["sections"]) == 6,
                 f"section order is {d['sections']} (want hero, then the four, then the close)")
            want(d["hoursMentions"] == 1, f"hours appear {d['hoursMentions']} times, want exactly 1")
            want(d["freeMentions"] == 1, f"'first session free' appears {d['freeMentions']} times, want 1")
            want(d["rays"] == 12, f"mark has {d['rays']} rays, want 12")
            want(d["primary"] == 1, f"{d['primary']} primary CTAs, want 1")
            want(d["deep"] == 5, f"{d['deep']} tier-specific booking links, want 5")
            want(d["wrenHollow"], "Wren Hollow missing")
            want(not d["fairport"], "Fairport still present")
            want(d["scrollW"] <= 390, f"horizontal overflow: scrollWidth {d['scrollW']}")
            pg.close()
        b.close()

    print()
    if fails:
        print(f"FAIL — {len(fails)} problem(s):")
        for f in fails:
            print("  *", f)
        raise SystemExit(1)
    print("PASS — three worlds, reshaped hierarchy live and correct.")


if __name__ == "__main__":
    main()
