# Verdict round 2 — PinkSun childlike worlds (board / crayon / notebook)

Reviewer: finish review, verdict pass. Method: read craft-floor, PRODUCT.md and the previous
round's `verdict.md`; read all three stylesheets and all three pages; measured the recaptured
build in Chromium at 390x844 (element order, computed contrast, computed box-shadow, tap
targets, `font-variant-numeric`, animation + reduced-motion, SVG symbol/use reconciliation);
inspected the recaptured screenshots and the mark crops with vision; reconciled the shipped
files for real-place names. Every score below is from a measurement or a screenshot, not from
the builder's summary.

## 1. VERDICT

**pass with open items**

Disposition phrase for the user:
*"Ship it — the two contract breaks and the crayon contrast failure are fixed. Before you call
the set done, copy the arrow symbol into crayon and notebook (their inline links lost the
arrow entirely), and decide whether the notebook mark reads ballpoint enough. Everything else
is shippable as-is."*

## 2. SCORES

Method column abbreviations: **DOM** = Chromium measurement against the current build;
**CSS** = computed style; **SS** = recaptured screenshot (vision); **GR** = grep/source.

| id | world | previous severity | score | measured / observed evidence |
|----|-------|-------------------|-------|------------------------------|
| F1 | crayon | material | **RESOLVED** | Ground is now `#1E4F92` (measured bg `rgb(30,79,146)`). `.wax-body` (.90) on the lifted panel `#1A4478` = **7.49:1** (was 3.86); `.wax-dim` (.80) on the ground = **5.31:1** (was 3.42); headline "Sun." `#FF8FC5` on paper = **3.86:1** (was 2.46) — clears 3:1 at 39px. Notebook `--ink-dim` raised to .70 = **5.37:1** (was 3.42). Whole-world sweep: 22/22 sampled text nodes pass their threshold in all three worlds. |
| F2 | notebook | material | **RESOLVED** | Computed `.btn.go` box-shadow = `rgba(27,42,74,0.3) 0px 3px 10px 0px` (blur 10); `.close` = `rgba(27,42,74,0.2) 0px 6px 18px 0px` (blur 18). Zero-blur hard offset is gone; both carry offset **and** soft blur. |
| F3 | all three | material | **RESOLVED** | At 390x844: `.hero-art` top = 96/100/98 vs `h1` top = 302/308/304 → `art_before_h1 = true` on all three (assertion "the pink sun … then 'Six courts…'" now holds). Primary CTA bottom = 587/593/595 < 844 → the primary action is fully visible without scrolling on a 390x844 viewport. `scrollWidth = 390` (no overflow). Screenshots confirm the sun + "pink sun" script sit above the headline. |
| F4 | notebook | minor | **PARTIAL** | The named defect is half-fixed. Removed: `#sun` now has **no** `url(#hatch)` reference and the dome `<path>` has **no** `stroke` attribute (was 16–18px dual-stroke outlines + hatched fill). **Still present:** the "crayon-stipple sun" the finding named — the notebook mark still renders through the page's `#chalk` filter (displacement 2.6 + alpha noise 1.05/0.32), so the fill reads a stippled pencil/crayon wash rather than flat ballpoint ink (**SS**: "does not read as ballpoint … reads more like textured crayon or colored pencil"). Structure is now correct; the material read is still short. |
| F5 | all three | minor | **RESOLVED** | Full `<a>`/`<button>` sweep at 390px: every inline funnel link is a 44px target — `First time? Start here` 135x44, `(585) 555-0142` 98x44, every `.curl` 44 tall (Reserve 85x44, See all three tiers 170x44, All five programs 235x44), footer nav 49–92 wide x 44 (was 29–35 wide). The previous 23px/15px targets are gone. |
| F6 | all three | minor | **RESOLVED** | `font-variant-numeric` computes to `tabular-nums` on `.slot .t`, `.spots`, `.when`, `.play .price` in all three worlds (12/12). |
| F7 | all three | minor | **RESOLVED** | `@keyframes drawsun` on `.hero-art .sun` and `writeit` on `.hero-art .scribble` are the single authored hero moment (sun lands, then the script writes) in all three stylesheets. `@media (prefers-reduced-motion:reduce){*{animation:none!important}}` is present in all three; under emulated reduced motion the sun/script `animation-name` computes to `none`. |
| F8 | crayon | nit | **RESOLVED** | `.hero-art::before/::after` computed `backdrop-filter = 'none'` (was `blur(0.4px)`). The tape strips remain (content `""`, clip-path, rotation) but the decorative blur is gone. |
| F9 | all three | nit | **PARTIAL** | The literal `→` glyph is gone — `grep '→'` over the three shipped pages returns **NONE**. An authored `<symbol id="arrowR">` was added and works on the board. But the symbol is defined **only in `index.html`**: both `v/crayon/index.html` and `v/notebook/index.html` carry 8 `<use href="#arrowR">` with no matching definition (DOM reconciliation: `MISSING refs: ['arrowR']` on both), so those inline links render nothing — `getBBox()` 0x0, and the curl crops show the text ending bare. The fix landed in one world of three. |
| F10 | board | nit | **RESOLVED** | `index.html` footer now ends with `<nav class="worlds" aria-label="Visual variants of this page">` linking `./` (Board, `aria-current="page"`), `v/crayon/`, `v/notebook/`. Reached from the flagship; crayon and notebook keep theirs. |
| F11 | all three | nit | **accepted (unchanged)** | Re-judged: `.facts` still reads `6 / 24 ft / $12 / $40` with a yellow accent. It carries real spec on the page that asks the first-timer to decide, so it is not the reflexive hero-metric template the floor refuses. Left as a note, no score change. |

**Tally:** 9 RESOLVED, 2 PARTIAL (F4, F9), 0 UNRESOLVED.

## 3. REBUILT T-SHIRT MARK — all three worlds

Target geometry (from the brief and `shots/proof-artwork.png`): 12 straight flat-ended rays
alternating pink and yellow, a solid pink semicircular dome with **no** outline, a gap between
dome and rays, a script wider than the sun, two-tone script.

| world | rays | ray ends | dome | dome outline | gap | script width | two-tone | verdict |
|-------|-----:|----------|------|--------------|-----|--------------|----------|---------|
| board (chalk) | 12 (`#sun` = 12 `<line>`) | flat (butt) | solid `#FF3D9A` | **none** (`stroke` attr absent) | yes | wider than sun (~1.5x) | yes (pink / yellow) | matches |
| crayon (wax) | 12 | flat (`stroke-linecap="butt"`) | solid `#FF3D9A` | **none** | yes | wider than sun | yes (pink / yellow) | matches |
| notebook (ballpoint) | 12 | flat (`stroke-linecap="butt"`) | solid `#FF3D9A` | **none** | yes | wider than sun | yes (pink / amber) | matches (structural) |

All three worlds render the shirt's mark. The only divergence is the notebook's documented
material override — yellow rays and the "sun" script are carried as amber `#C87A00` because
yellow is unreadable on white paper. That is a colour substitution inside one world's material
rule, not a structural change; ray count, flat ends, solid unoutlined dome, the dome-to-ray
gap, and the wider two-tone script all hold. Crayon and board preserve pink/yellow exactly.
The material is allowed to roughen the edge and it does (chalk turbulence, wax streak, paper
fibre); the structure does not change. Confirmed by DOM (12 `<line>` + strokeless dome `<path>`
in each page) and by the three mark crops and `mark-comparison.png`.

## 4. REAL-PLACE-NAME CHECK (new since the last round)

The club moved Fairport, NY → Wren Hollow, NY. Verified by source reconciliation.

- **Shipped pages — clean.** No `Fairport`, `Rochester`, `Monroe`, `Route 31`, `Pittsford`,
  `Penfield`, `Perinton`, `Henrietta`, `Brighton`, `Greece`, `Victor` or zip `14450` in any
  shipped `.html` or `.css`. Rendered address is `240 Sunfield Way, Wren Hollow, New York`.
- **One reference survives in a shipped asset:** `assets/booking.js:9` — a code comment
  reading *"every dedicated club in the Rochester market uses it"*. Invisible to visitors, but
  it is a real-place string inside a shipped file (nit, N4 below).
- **Documentation (allowed):** `PRODUCT.md` and `README.md` keep the real market region
  ("Rochester and Monroe County"). They are documentation, not shipped pages.
- **Intentionally kept, must not have been renamed — confirmed intact:** `design/plan.md` and
  `design/research-notes.md` still name the real competitor businesses (Fairport Pickleball
  Club, Dinkers Pickleball Campus, ROC City Pickleball, Erie Canal Pickleball, Ace Pickleball
  Club, Pickleball Kingdom, Dill Dinkers) with their live URLs. Migration/verify tooling
  (`design/research/page-structures.json`, `build/retown.py`, `build/check_live_worlds.py`)
  also retains `Fairport` as expected.

**Deployment parity:** the three `live-*-mobile.png` recaptures are byte-identical to the local
`{board,crayon,notebook}-mobile.png` captures (matching MD5s), so the deployed site matches the
build under review — no stale-deploy gap.

## 5. NEW FINDINGS (introduced or exposed by the fix batch)

| id | severity | finding | one-line fix |
|----|----------|---------|--------------|
| N1 | minor (regression) | **The arrow icon is missing on crayon and notebook.** The fix for F9 replaced the `→` glyph with `<use href="#arrowR">`, but the `<symbol id="arrowR">` is defined only in `index.html`. Both variants therefore render 8 empty arrow slots (each "Reserve" and curl link ends in nothing). Proven by symbol/use reconciliation (`MISSING refs: ['arrowR']` x2), `getBBox()` 0x0, and the curl crops. | Copy the `<symbol id="arrowR">` block into the `<defs>` of `v/crayon/index.html` and `v/notebook/index.html` (or externalise to `assets/icons.svg` and point both at `../../assets/icons.svg#arrowR`). |
| N2 | nit | **Dead SVG defs left behind.** `v/notebook/index.html` still defines `<pattern id="hatch">`, now referenced nowhere (orphaned by the F4 fix); `v/crayon/index.html` defines a `#chalk` filter it no longer uses (it renders through `#chalkmark`). | Delete the unused `#hatch` pattern and the unused crayon `#chalk` filter. |
| N3 | nit (exposed) | **The skip link is the last sub-44px target.** `.skip` ("Skip to tonight's board") measures 146x27 at 390px. It is a focus-only utility link (conventionally exempt from 2.5.8), so it is not a real hit, but a literal target-size sweep now flags it. | `.skip:focus{min-height:44px}` (or padding) if the rule is applied literally. |
| N4 | nit | **Real-place string in a shipped asset.** `assets/booking.js:9` names "the Rochester market" in a comment. | Change the comment to "the local market". |

Nothing else in the batch regressed: no console errors, no horizontal overflow (scrollWidth
390 x3), exactly one primary CTA and one `.close` per page, and the contract's first-viewport
order holds in all three worlds.

## 6. OPEN ITEMS (ordered by cost to the user)

1. **Arrow icons missing on crayon and notebook (N1, F9).** — **worth-fixing.** Visible to any
   visitor who opens an alternate: eight inline links per page end in a blank gap. One shared
   symbol copy; cheapest visible win left in the batch.
2. **The notebook mark still reads crayon/pencil, not ballpoint (F4).** — **worth-fixing** if
   the three worlds ship as a set (it is the world's own material claim); **shippable-as-is**
   if only the board ships. Cost: one filter retune of `#chalk` for the notebook mark.
3. **`booking.js` comment naming Rochester (N4); skip link at 27px (N3); dead `#hatch`/`#chalk`
   defs (N2); notebook amber ray substitution.** — **shippable-as-is.** Invisible to visitors or
   a documented world rule; tidy when convenient.
