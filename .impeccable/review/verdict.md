# Finish review — PinkSun childlike worlds (board / crayon / notebook)

Reviewer: finish review (no build history). Method: read craft-floor, PRODUCT, all three
stylesheets and pages; inspected all six screenshots with vision; re-ran the anti-pattern
detector and the Playwright world suite myself; measured contrast, element order, tap
targets and computed shadows in Chromium at 390px. "Report what the artifact does."

## 1. VERDICT

**pass with open items**

Disposition phrase for the user: *"Ship the board once the hero order is fixed; hold crayon
and notebook — crayon fails contrast and notebook wears a banned hard-offset shadow."*

## 2. FINDINGS

| id | world | severity | rule / claim | evidence (measured) | fix |
|----|-------|----------|--------------|---------------------|-----|
| F1 | crayon | material | Craft floor — Contrast: small/body text ≥4.5:1, large ≥3:1, tint from the hue | `.wax-dim` (rgba .66) on construction-paper blue `#245FAE` = **3.42:1** (used by `h2 .sm`, `.when`, `.play .price small` 10.5px, `.strip .who`, `footer .fine`); `.wax-body` (.84) on the lifted panels `#2C6BC0` = **3.86:1** (`.fact span`, `.notice .hours span` = the schedule hours); headline "Sun." pink `#FF6FB2` on paper = **2.46:1** (<3:1 even at 39px) | Lighten dims (≥.90 alpha or a lighter tint), step pink up to a ≥3:1 hue on blue, or darken the panels |
| F2 | notebook | material | Craft floor — Refuse: hard offset shadows outside a neobrutalist world; Depth: offset **and** soft blur | Computed `.btn.go` box-shadow `rgba(27,42,74,.35) 0 4px 0` and `.close` `…0 6px 0` — **zero blur, hard offset** (sticker/neobrutalist costume) | Replace with a soft blur (`0 3px 8px`) or drop; the ballpoint-on-paper world is not neobrutalist |
| F3 | board, crayon, notebook | material | Direction contract — FIRST VIEWPORT: "the pink sun … **then** 'Six courts…'" | Measured `h1.top` = 99–118px vs `.hero-art` top = 520–559px; `sun_before_h1 = false` in all three. Render order is headline → lede → 2 CTAs → sun | On mobile put `.hero-art` before `.hero-copy` (or float the sun first) so the signature image leads |
| F4 | notebook | minor | Material claim — "Ballpoint on a ruled sheet" / "blue-black ballpoint" | Screenshot reads marker + highlighter + crayon: 16–18px dual-stroke outlines, hatched fill, Gloria Hallelujah fat hand, crayon-stipple sun — converges with world B's wax, not pen | Thin outlines to a ballpoint register (1.5–3px), drop the hatch fill, one pen weight |
| F5 | board, crayon, notebook | minor | Tap targets ≥44px at 390px | `(585) 555-0142` = **98×15px**; `First time? Start here` = **135×23px** (board, notebook); footer nav links are 44 tall but only **29–35px wide**. Only `.btn`/`.curl` carry min-height:44 | Give inline funnel links `.curl` padding/min-height:44 or wrap them in a 44px target |
| F6 | board, crayon, notebook | minor | Craft floor — Browser surfaces: numerals in tabular data | No `font-variant-numeric` anywhere; schedule times/spots set in proportional Archivo | Add `font-variant-numeric:tabular-nums` to `.slot .t`, `.spots`, `.when` |
| F7 | board, crayon, notebook | minor | Craft floor — Motion: one authored moment | No `@keyframes`/animation in any stylesheet; only hover/active transitions | Add one reduced-motion-guarded authored moment (chalk/crayon draw-on of the sun or ruleline) |
| F8 | crayon | nit | Craft floor — blur/glass as decoration | `.hero-art::before/::after` computed `backdrop-filter: blur(0.4px)` (imperceptible) | Remove the backdrop-filter |
| F9 | board, crayon, notebook | nit | Craft floor — Unicode glyphs standing in for an icon system | Authored SVG `#down` arrow used once, but every `.curl` uses a literal "→" (`Reserve →`, `All five programs →`) | Use the authored arrow, or drop the glyph for a consistent icon set |
| F10 | board | nit | Funnel/coverage — alternates reachable from the flagship | `index.html` footer nav = Play/Join/Visit/FAQ + More by Dennis; no Board/Crayon/Notebook links (crayon & notebook have them) | Add the variant links to the root footer (or a dev switcher) |
| F11 | board, crayon, notebook | nit | Craft floor — Refuse default: hero-metric template | `.facts` = 4 × `<b>number</b><span>label</span>` with yellow accent | Acceptable here (carries real spec); note only |

**Verified fine (no action):** board contrast passes everywhere (body 8.96:1, dim 6.02:1,
headline pink 4.96:1, yellow 11.46:1); prices/times/spots readable in all three (times
5.69–13.84:1, prices 4.77–11.46:1); no kicker/eyebrow above any heading (`.strip .who` is a
header status block, not a kicker); no section numbers; no gradient text; no glass cards; no
coloured 1px+ card side borders; no system display face (Gloria Hallelujah / Patrick Hand /
Archivo are self-hosted woff2); focus rings, ::selection, scrollbar and skip-link all themed;
card/notice shadows carry offset + blur in board and crayon.

## 3. CONTRACT

| world | FIRST VIEWPORT promise | material claim |
|-------|------------------------|----------------|
| board (chalk) | **No** — all promised elements are in the first viewport, but the order is inverted: headline (y≈112) and both CTAs render *above* the sun (y≈527); the contract said the sun comes first | **Yes** — reads as chalk on a dark board: real SVG turbulence chalk filter, slate grain, wiped-board gradient streaks, hand-drawn wobble ruleline, "never a blur"; data set in Archivo |
| crayon | **No** — same inversion (h1 y≈118, sun y≈559) | **Yes** — reads as wax crayon on construction paper: waxy streak filter, paper-fibre background, torn masking tape; fails contrast (F1) but not the material |
| notebook | **No** — same inversion (h1 y≈99, sun y≈520) | **Partial / no** — ruled lines and the red margin are present and correct, but the drawing reads marker/highlighter/crayon, not ballpoint; converges with world B (F4) |

## 4. PRE-EXISTING MECHANICAL CHECKS — scoring

| check | score | note |
|-------|-------|------|
| detector (`scripts/detect.mjs`) returns `[]` on 3 pages + 3 stylesheets | **RESOLVED** | Re-ran it; empty on all six. Caveat: weak signal — my positive control (kicker + Impact + `4px 4px 0` shadow + low contrast) yielded only 2 of 4 flags, so `[]` does not clear those rules |
| exactly one `data-cta="primary"` and one `data-cta="nav"` per page | **RESOLVED** | primary=1, nav=1 ×3 (script + grep) |
| one `.close` per page | **RESOLVED** | 1 each (grep + suite) |
| no horizontal overflow at 390px | **RESOLVED** | scrollWidth 390 ×3 |
| no dead internal links | **RESOLVED** | path resolution passes; `join/#start`, `join/#tiers` anchors exist; all dir targets exist. Caveat: the script skips fragment-only hrefs (verified by hand) |
| no console errors | **RESOLVED** | console/pageerror listeners recorded none |
| fixed bottom action bar clears the footer | **RESOLVED** | `barClear = true` ×3; body padding-bottom 94px |

Overall mechanicals: **PASS.** One sub-check is **PARTIAL**: the suite's "controls under 44px"
selector (`a.btn,button.btn,a.curl,.actionbar a,.strip .logo`) excludes inline links, which is
why F5 exists despite a green run.

## 5. WHAT THE BUILD MISSED (≤5, by user cost)

1. **The signature image leads nothing (F3).** The contract's first-viewport promise is inverted in all three worlds: a first-timer meets a headline, four lines of copy and two buttons before the sun that is supposed to sell the world. — **Fix before shipping** (one CSS reorder).
2. **Readability in bad light is broken in crayon, marginal in notebook (F1).** Schedule hours on the lifted panel read at 3.86:1, dim labels at 3.42:1, the "Sun." headline at 2.46:1 — the PRODUCT brief's "read a time and a price in bad light" is not met for the alternates. — **Fix before shipping** if crayon/notebook ship; board is clean.
3. **Notebook wears a floor-banned costume (F2).** Hard zero-blur offset shadows on the buttons and the close block are the neobrutalist tell, off-world for ballpoint-on-paper. — **Fix before shipping** if notebook ships.
4. **The "three materials" are really two and a half (F4).** Notebook's drawing reads marker/crayon, overlapping world B, so the alternates don't demonstrate three distinct materials. — **Can wait** unless the alternates are shipped as a set.
5. **Craft polish the floor names explicitly (F5–F7, F9):** no tabular numerals in the schedule, no authored motion moment, mixed iconography (authored SVG arrow vs "→" glyph), and sub-44px inline funnel links. — **Can wait;** each is a cheap targeted fix.

## Evidence trail

- Detector re-run: `node …/scripts/detect.mjs <file>` → empty on all three pages + three CSS.
- Suite re-run: `python3 build/check_worlds.py` → PASS (primary 1 / nav 1 / close 1 / scrollW 390 / barClear true ×3).
- Order + tap targets measured in Chromium 390×844 (`/tmp/measure.py`); computed colors (`/tmp/colors.py`).
- Contrast ratios computed from the CSS palette with WCAG relative-luminance compositing.
