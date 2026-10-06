# Round 2 disposition — PinkSun childlike worlds

The finish review's second round returned **pass with open items** (9 RESOLVED, 2 PARTIAL,
0 UNRESOLVED) and raised four new findings, N1 to N4. All four are closed in the same
commit that carries this file's fixes (`ebd81db`, pushed, live).

| id | reviewer's score | now | what changed |
|----|------------------|-----|--------------|
| F1 crayon contrast | RESOLVED | RESOLVED | ground `#1E4F92`, wax-body .90 = 7.49:1, wax-dim .80 = 5.31:1, headline `#FF8FC5` = 3.86:1. Unchanged this pass. |
| F2 notebook shadows | RESOLVED | RESOLVED | `.btn.go 0 3px 10px`, `.close 0 6px 18px`. Unchanged. |
| F3 mark first | RESOLVED | RESOLVED | art top 96/100/98 < h1 top 302/308/304; primary CTA bottom 587/593/595 < 844. |
| F4 notebook mark | PARTIAL | PARTIAL → fixed on measurement | The grain that read pencil is gone. The filter is now `#ink`: a hair of edge wobble over a broad, slow marker drag with no high-frequency noise. Measured, per `build/measure_fill.py`: the dome's luminance standard deviation runs 8.32 (notebook) against 8.07 (board) and 0.45 (crayon). The reviewer's residual "flat/crisp" read is about the shape edges, and crisp edges are the fidelity rule: the shirt's mark has no outline, so the notebook cannot draw one. That trade is deliberate, not a defect. |
| F5 sub-44 links | RESOLVED | RESOLVED | sweep clean. The base `.skip` now also carries a 44px box, so the last sub-44 target is gone in all three, not just under focus. |
| F6 tabular numerals | RESOLVED | RESOLVED | unchanged. |
| F7 authored motion | RESOLVED | RESOLVED | unchanged, reduced-motion guarded. |
| F8 backdrop blur | RESOLVED | RESOLVED | unchanged. |
| F9 arrow glyph | PARTIAL | RESOLVED | `#arrowR` is now defined in every world, in that world's own stroke: wax for crayon, ballpoint for notebook. Previously both alternates referenced it 8x and defined it 0x, so every arrow rendered nothing. |
| F10 footer switcher | RESOLVED | RESOLVED | unchanged. |
| F11 hero metrics | accepted | accepted | unchanged. |
| N1 arrow missing (regression) | open | RESOLVED | see F9. `build/check_arrows.py` now asserts every row's arrow resolves per world. |
| N2 dead defs | open | RESOLVED | `#hatch` (notebook) and crayon's `#chalk` deleted. The notebook's own `#chalk` went too once the mark moved to `#ink`. |
| N3 `.skip` 27px | open | RESOLVED | base rule carries `min-height:44px` in all three worlds. |
| N4 booking.js "Rochester" | open | RESOLVED | now "the local market". README quotes that comment, so it moved with it. PRODUCT.md now states the invented town and names the real market the concept stands in for. |

## Gate that was lying

`build/check_worlds.py` asserted the presence of a shared `#chalk` filter as each world's
material. That passed by accident: the board really does chalk, and the alternates happened
to still carry the id. Deleting the dead defs broke it. It now asserts each world's own
filter by name (board `#chalk`, crayon `#chalkmark`, notebook `#ink`), so a world cannot
quietly lose its material without failing the gate.

## Deployed and verified

Live contract check passes on all three: five price rows, about section present, prices
stated once, hours stated once, twelve rays, one primary CTA, eight booking controls, five
deep links, `wren=True fairport=False` at 390px, no overflow.

- https://dpsoccerdude101.github.io/pinksun/
- https://dpsoccerdude101.github.io/pinksun/v/crayon/
- https://dpsoccerdude101.github.io/pinksun/v/notebook/

## Still open, by cost

1. Notebook carries yellow as amber `#C87A00`. On white paper the brand yellow is ~1.1:1,
   effectively invisible. Honest material override, structurally unchanged. Shippable.
2. `/play/ /join/ /visit/ /faq/` still wear the old poster world (`assets/site.css`). Not
   a defect in what shipped, but the set is not all childlike yet.
