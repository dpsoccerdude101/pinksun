#!/usr/bin/env python3
"""Generate the two alternate worlds from world A's page.

One skeleton, three materials: the copy, the funnel contract and the data
registry are identical across worlds, so only the material block, the
stylesheet and the paths change. Nothing about the offer drifts between them.
"""
import os, re

ROOT = "/data/pinksun/site"
SRC = os.path.join(ROOT, "index.html")
html = open(SRC).read()

# --------------------------------------------------------------------------
# shared: pull out the pieces the worlds replace
# --------------------------------------------------------------------------
defs_re = re.compile(r"<svg width=\"0\" height=\"0\".*?</svg>", re.S)
old_defs = defs_re.search(html).group(0)
contract_re = re.compile(r"<!--\nTHESIS.*?-->\n", re.S)
old_contract = contract_re.search(html).group(0)

CRAYON_DEFS = '''<svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute">
  <defs>
    <!-- Crayon is wax dragged across card stock: streaky deposit, wobbly edge,
         and the paper's tooth punching through where the stick skipped. -->
    <filter id="chalk" x="-12%" y="-12%" width="124%" height="124%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.02 0.42" numOctaves="2" seed="6" result="e"/>
      <feDisplacementMap in="SourceGraphic" in2="e" scale="7" xChannelSelector="R" yChannelSelector="G" result="rough"/>
      <!-- the streaks a wax stick leaves: fine across, long along -->
      <feTurbulence type="fractalNoise" baseFrequency="0.03 0.5" numOctaves="2" seed="13" result="wax"/>
      <feColorMatrix in="wax" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  2.9 0 0 0 -0.55" result="waxA"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.62" numOctaves="2" seed="3" result="tooth"/>
      <feColorMatrix in="tooth" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1.3 0 0 0 0.3" result="toothA"/>
      <feComposite in="waxA" in2="toothA" operator="arithmetic" k1="1" k2="0" k3="0" k4="0" result="mask"/>
      <feComposite in="rough" in2="mask" operator="in" result="waxy"/>
      <feComponentTransfer in="waxy" result="dense"><feFuncA type="linear" slope="1.35"/></feComponentTransfer>
      <feGaussianBlur in="dense" stdDeviation="0.6" result="softedge"/>
      <feMerge><feMergeNode in="softedge"/><feMergeNode in="dense"/></feMerge>
    </filter>

{{SUN_CRAYON}}

    <!-- the mark keeps its shape: same wax streaks, a third of the displacement -->
    <filter id="chalkmark" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.03 0.5" numOctaves="2" seed="6" result="e"/>
      <feDisplacementMap in="SourceGraphic" in2="e" scale="3.4" xChannelSelector="R" yChannelSelector="G" result="rough"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.04 0.45" numOctaves="2" seed="13" result="wax"/>
      <feColorMatrix in="wax" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1.9 0 0 0 0.12" result="waxA"/>
      <feComposite in="rough" in2="waxA" operator="in" result="waxy"/>
      <feComponentTransfer in="waxy" result="dense"><feFuncA type="linear" slope="1.5"/></feComponentTransfer>
      <feGaussianBlur in="dense" stdDeviation="0.5" result="soft"/>
      <feMerge><feMergeNode in="soft"/><feMergeNode in="dense"/></feMerge>
    </filter>

    <symbol id="ruleline" viewBox="0 0 1440 12" preserveAspectRatio="none">
      <path d="M0,6.2 L110,4.1 L230,7.4 L350,3.6 L470,7.9 L590,4.8 L710,8.1 L830,4.2 L950,7.6 L1070,4.4 L1180,8.3 L1300,5.1 L1440,7.2"
            fill="none" stroke="currentColor" stroke-width="4.2" stroke-linecap="round"/>
    </symbol>

    <symbol id="down" viewBox="0 0 60 54">
      <path d="M6,4 C26,10 44,20 50,44" fill="none" stroke="currentColor" stroke-width="5"
            stroke-linecap="round" stroke-dasharray="8 7"/>
      <path d="M39,33 L50.5,45.5 L57,29" fill="none" stroke="currentColor" stroke-width="5"
            stroke-linecap="round" stroke-linejoin="round"/>
    </symbol>
  </defs>
</svg>

'''

NOTEBOOK_DEFS = '''<svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute">
  <defs>
    <!-- Ballpoint is an even, slightly nervous line; the colouring is marker,
         laid on after the outline the way a kid fills a drawing in. -->
    <filter id="chalk" x="-8%" y="-8%" width="116%" height="116%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="8" result="e"/>
      <feDisplacementMap in="SourceGraphic" in2="e" scale="2.6" xChannelSelector="R" yChannelSelector="G" result="rough"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.72" numOctaves="2" seed="2" result="t"/>
      <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1.05 0 0 0 0.32" result="tA"/>
      <feComposite in="rough" in2="tA" operator="in"/>
    </filter>
    <pattern id="hatch" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(-38)">
      <line x1="0" y1="0" x2="0" y2="10" stroke="#D6216B" stroke-width="1.5"/>
    </pattern>

{{SUN_NOTEBOOK}}

    <symbol id="ruleline" viewBox="0 0 1440 12" preserveAspectRatio="none">
      <path d="M0,6 L1440,6" fill="none" stroke="currentColor" stroke-width="1"/>
    </symbol>

    <symbol id="down" viewBox="0 0 60 54">
      <path d="M6,4 C26,10 44,20 50,44" fill="none" stroke="currentColor" stroke-width="3"
            stroke-linecap="round" stroke-dasharray="6 5"/>
      <path d="M41,34 L50.5,45.5 L56,30" fill="none" stroke="currentColor" stroke-width="3"
            stroke-linecap="round" stroke-linejoin="round"/>
    </symbol>
  </defs>
</svg>

'''

# the mark comes from build/logo.py, so all three worlds draw the same logo
import logo

SUN_CRAYON = logo.sun_symbol(color_a="#FF8FC5", color_b="#FFE800", dome_fill="#FF3D9A")
# no outlines: the shirt's mark has none. Yellow ink is illegible on paper, so the
# paper world carries the proof's yellow as a deep amber marker.
SUN_NOTEBOOK = logo.sun_symbol(color_a="#D6216B", color_b="#C87A00", dome_fill="#FF3D9A")

CRAYON_CONTRACT = '''<!--
THESIS  The drawing a kid pins to the gym wall. Same club, same offer, told in
        wax on cheap card stock instead of on the board.
OWN-WORLD  Construction-paper blue, white and fluorescent crayon, masking tape,
        paper fibre, wax streaks where the stick skipped. Centred and taped up,
        not asymmetric. Archivo still carries every time, price and spot count.
STORY  Identical to world A. A first-timer books, a regular books in two taps.
FIRST VIEWPORT  Taped sheet: the crayon sun, "pink sun" under it, the headline,
        the readable line naming indoor pickleball, the pink button.
FORM  Crayon on construction paper. Position 2 of my ordered list. Seed 4d276e5f.
FINISH  unreviewed and undocumented is unfinished; this build ends with the
        finish review, the verdict, and DESIGN.md.
-->

'''

NOTEBOOK_CONTRACT = '''<!--
THESIS  The sign-up sheet on the clipboard at the front desk: ballpoint
        handwriting between printed rules, coloured in with marker.
OWN-WORLD  Ruled school paper, blue-black ballpoint, a red margin rule, marker
        pink and highlighter yellow for the brand. The paper's own lines are the
        only dividers this world needs. Archivo carries every time and price.
STORY  Identical to world A. A first-timer books, a regular books in two taps.
FIRST VIEWPORT  The ballpoint sun outlined and coloured in, "pink sun" under it,
        the headline with a highlighter swipe, the readable line naming indoor
        pickleball, the pink button.
FORM  Ballpoint on a ruled sheet. Position 3 of my ordered list. Seed 4d276e5f.
FINISH  unreviewed and undocumented is unfinished; this build ends with the
        finish review, the verdict, and DESIGN.md.
-->

'''


def rewrite(page_html, defs, contract, world_css, depth, world_name):
    out = page_html
    out = defs_re.sub(lambda m: defs, out, count=1)
    out = contract_re.sub(lambda m: contract, out, count=1)
    out = out.replace('href="assets/chalk.css"', f'href="{depth}assets/{world_css}"')
    out = out.replace('href="assets/fonts.css"', f'href="{depth}assets/fonts.css"')
    out = out.replace('src="assets/booking.js"', f'src="{depth}assets/booking.js"')
    # internal navigation
    for seg in ("play/", "join/", "visit/", "faq/"):
        # prefix match so anchor links like join/#start are rewritten too
        out = out.replace(f'href="{seg}', f'href="{depth}{seg}')
    out = out.replace('href="./"', f'href="{depth}"')
    for seg in ("v/crayon/", "v/notebook/"):
        out = out.replace(f'href="{seg}"', f'href="{depth}{seg}"')
    if world_css == "crayon.css":
        # the mark uses the gentler pass so its rays survive the wax
        out = out.replace('filter="url(#chalk)"', 'filter="url(#chalkmark)"')
    # the mark's label describes this world's material, not the board's
    ARIA = {"crayon.css": "A pink sun with rays drawn by hand in pink and yellow crayon",
            "notebook.css": "A pink sun drawn in ballpoint and coloured in with marker"}
    if world_css in ARIA:
        out = out.replace("A pink sun with rays drawn by hand in pink and yellow chalk", ARIA[world_css])
    theme = {"crayon.css": "#245FAE", "notebook.css": "#FCFCFA"}.get(world_css)
    if theme:
        out = out.replace('<meta name="theme-color" content="#242C28">',
                          f'<meta name="theme-color" content="{theme}">')
    return out


for slug, defs, contract, css in (
    ("crayon", CRAYON_DEFS.replace("{{SUN_CRAYON}}", SUN_CRAYON), CRAYON_CONTRACT, "crayon.css"),
    ("notebook", NOTEBOOK_DEFS.replace("{{SUN_NOTEBOOK}}", SUN_NOTEBOOK), NOTEBOOK_CONTRACT, "notebook.css"),
):
    d = os.path.join(ROOT, "v", slug)
    os.makedirs(d, exist_ok=True)
    page = rewrite(html, defs, contract, css, "../../", slug)
    assert "{{SUN" not in page, "unsubstituted mark placeholder"
    assert 'chalk.css' not in page, "world A stylesheet leaked into " + slug
    open(os.path.join(d, "index.html"), "w").write(page)
    print(f"wrote v/{slug}/index.html  ({len(page)} bytes)")
