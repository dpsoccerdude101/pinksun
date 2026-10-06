#!/usr/bin/env python3
"""Is the notebook sheet actually clean white paper?

Three claims to check, all of them measurable rather than eyeballed:

  1. the ground is pure white, not the off-white it used to be
  2. there is no grain on it (the old sheet carried a 5% feTurbulence tile)
  3. the rules are still printed, evenly, at the 30px pitch

Samples the left margin of the page, which sits outside .wrap, so nothing but
paper and rules is ever in frame.
"""
import statistics
from collections import Counter

from PIL import Image
from playwright.sync_api import sync_playwright

PAGE = "file:///data/pinksun/site/v/notebook/index.html"
SHEET = 30      # --sheet, the rule pitch
DPR = 2


def run():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=DPR)
        pg.goto(PAGE)
        pg.wait_for_timeout(900)
        pg.screenshot(path="/tmp/paper-check.png", full_page=True)
        b.close()

    im = Image.open("/tmp/paper-check.png").convert("RGB")
    w, h = im.size
    px = im.load()
    # do not assume the screenshot came back DPR-scaled: derive it. Sampling in
    # CSS coordinates is the only way to be sure of sitting left of the margin
    # rule (34px) and left of .wrap (46px), where nothing but paper and rules is.
    scale = w / 390
    x0, x1 = int(2 * scale), int(30 * scale)

    # 1 + 2: the ground is the most common colour in a strip that holds nothing
    # but paper and rules. Spread is the wrong test, since any vertical strip
    # crosses rules by construction. So: is the dominant colour pure white, and
    # does it cover the sheet the way paper should?
    vals = [px[x, y] for y in range(0, h, 3) for x in range(x0, x1, 5)]
    counts = Counter(vals)
    (ground, hits), (runner, rl_hits) = counts.most_common(2)
    share = hits / len(vals)

    # 3: rules print as blue-leaning rows (ruleline #D3E1F0 has B > R; paper does not)
    column = 30
    rule_rows = [y for y in range(h) if px[column, y][2] - px[column, y][0] >= 3]
    gaps = [b - a for a, b in zip(rule_rows, rule_rows[1:]) if b - a > 1]
    pitch = round(statistics.median(gaps), 1) if gaps else 0

    print(f"ground colour   : {ground} on {share:.1%} of the sheet  (want (255, 255, 255))")
    print(f"runner-up       : {runner} on {rl_hits / len(vals):.1%}  (the rule line)")
    print(f"rule rows found : {len(rule_rows)}")
    print(f"rule pitch      : {pitch} px at scale {scale:g}  (want {SHEET * scale:g})")

    ok = ground == (255, 255, 255) and share > 0.90 and abs(pitch - SHEET * scale) < 3
    print("VERDICT         :", "clean white ruled paper" if ok else "NOT clean")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(run())
