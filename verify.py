#!/usr/bin/env python3
"""PinkSun site gate. Asserts the funnel contract on every page.

Run:  python3 /data/pinksun/site/verify.py
Exit: 0 = all pass, 1 = at least one failure
"""
import json, os, re, sys, urllib.parse

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = ["index.html", "play/index.html", "join/index.html", "visit/index.html", "faq/index.html"]
EXPECTED_NAV = ["Play", "Join", "Visit", "FAQ"]
CHROMIUM = "/usr/bin/chromium"

fails, notes = [], []


def fail(page, msg):
    fails.append(f"{page}: {msg}")


def resolve(page, href):
    """Return the on-disk path an internal href points at, or None if external."""
    if not href or href.startswith(("#", "mailto:", "tel:", "http://", "https://", "data:")):
        return None
    base = os.path.dirname(os.path.join(ROOT, page))
    path = urllib.parse.urlparse(href).path
    target = os.path.normpath(os.path.join(base, path))
    if target.endswith(os.sep) or not os.path.splitext(target)[1]:
        target = os.path.join(target, "index.html")
    return target


def main():
    report = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM, args=["--no-sandbox"])
        for page in PAGES:
            url = "file://" + os.path.join(ROOT, page)
            ctx = browser.new_context(viewport={"width": 1440, "height": 960})
            pg = ctx.new_page()
            console, failed_req = [], []
            pg.on("console", lambda m: console.append(f"{m.type}: {m.text}") if m.type == "error" else None)
            pg.on("pageerror", lambda e: console.append(f"pageerror: {e}"))
            pg.on("requestfailed", lambda r: failed_req.append(r.url))
            pg.goto(url, wait_until="networkidle")
            pg.wait_for_timeout(1200)

            data = pg.evaluate(
                """() => {
                const cs = el => getComputedStyle(el);
                return {
                  primary: document.querySelectorAll('[data-cta="primary"]').length,
                  navcta: document.querySelectorAll('[data-cta="nav"]').length,
                  booking: [...document.querySelectorAll('[data-booking]')].map(a => a.getAttribute('href')),
                  deepLinks: document.querySelectorAll('[data-booking-path]').length,
                  reserve: document.querySelectorAll('.reserve').length,
                  crumbs: document.querySelectorAll('.crumbs').length,
                  navLabels: [...document.querySelectorAll('.bar nav > a:not([data-booking])')].map(a => a.textContent.trim()),
                  current: document.querySelectorAll('.bar nav a[aria-current="page"]').length,
                  docH: document.documentElement.scrollHeight,
                  stylesheets: [...document.querySelectorAll('link[rel=stylesheet]')].map(l => l.getAttribute('href')),
                  inlineStyleTags: document.querySelectorAll('style').length,
                  h1: (document.querySelector('h1')||{}).textContent,
                  title: document.title,
                  desc: (document.querySelector('meta[name=description]')||{}).content || '',
                  links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')),
                };
            }"""
            )

            # desktop assertions
            if console:
                fail(page, f"console errors: {console[:3]}")
            if failed_req:
                fail(page, f"failed requests: {failed_req[:3]}")
            if data["primary"] != 1:
                fail(page, f"expected exactly 1 [data-cta=primary], found {data['primary']}")
            if data["navcta"] != 1:
                fail(page, f"expected exactly 1 [data-cta=nav], found {data['navcta']}")
            if data["reserve"] != 1:
                fail(page, f"expected exactly 1 reserve block, found {data['reserve']}")
            if data["booking"] and any(h is None or h.strip() == "" for h in data["booking"]):
                fail(page, "a [data-booking] link has an empty href")
            if page != "index.html" and data["crumbs"] != 1:
                fail(page, f"interior page missing breadcrumb (found {data['crumbs']})")
            if page != "index.html" and data["current"] != 1:
                fail(page, f"expected 1 aria-current=page nav item, found {data['current']}")
            if data["navLabels"] != EXPECTED_NAV:
                fail(page, f"nav contract drift: {data['navLabels']} != {EXPECTED_NAV}")
            if not data["h1"]:
                fail(page, "no h1")
            if len(data["desc"]) < 50:
                fail(page, f"meta description too short ({len(data['desc'])} chars)")

            # every internal link resolves on disk
            for href in data["links"]:
                tgt = resolve(page, href)
                if tgt and not os.path.exists(tgt):
                    fail(page, f"dead internal link: {href} -> {os.path.relpath(tgt, ROOT)}")

            # mobile overflow
            m = browser.new_context(viewport={"width": 390, "height": 844},
                                    device_scale_factor=2, is_mobile=True, has_touch=True)
            mp = m.new_page()
            mp.goto(url, wait_until="networkidle")
            mp.wait_for_timeout(900)
            scroll_w = mp.evaluate("document.documentElement.scrollWidth")
            if scroll_w > 392:
                fail(page, f"horizontal overflow at 390px (scrollWidth {scroll_w})")
            m.close()

            report[page] = {
                "console": len(console), "primary": data["primary"], "navcta": data["navcta"],
                "bookingLinks": len(data["booking"]), "deepLinks": data["deepLinks"],
                "reserveBlocks": data["reserve"], "docHeight": data["docH"],
                "mobileScrollWidth": scroll_w, "stylesheets": len(data["stylesheets"]),
            }
            ctx.close()

        # ---- funnel: every page reachable from / in one hop, and every page books ----
        idx_links = set()
        with open(os.path.join(ROOT, "index.html")) as f:
            for href in re.findall(r'href="([^"#]+)"', f.read()):
                if not href.startswith(("http", "mailto:", "tel:", "assets/", "favicon", "#")):
                    idx_links.add(os.path.normpath(href).rstrip("/") or "/")
        for page in PAGES[1:]:
            section = os.path.dirname(page)
            if section not in idx_links:
                fail("index.html", f"nav target '{section}' not linked from the landing page")

        # ---- self-containment check (optional, reported) ----
        for page in PAGES:
            with open(os.path.join(ROOT, page)) as f:
                html = f.read()
            if 'rel="stylesheet"' not in html:
                notes.append(f"{page}: no stylesheet link (unexpected)")
        browser.close()

    print(json.dumps(report, indent=1))
    print("\n" + "=" * 64)
    if notes:
        print("notes:")
        for n in notes:
            print("  -", n)
    if fails:
        print(f"FAIL — {len(fails)} problem(s):")
        for f_ in fails:
            print("  x", f_)
        return 1
    print(f"PASS — {len(PAGES)} pages, all funnel assertions hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
