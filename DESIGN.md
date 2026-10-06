# DESIGN.md — PinkSun

The durable visual system, recorded from the built world rather than from intention.
Product truth lives in PRODUCT.md and does not change here.

## The world in one line

A hand-made club: a chalked sign-in board, a kid's crayon drawing taped to the wall, and the
sign-up sheet on the clipboard. Three materials, one offer, one funnel.

## Color strategy

**Committed**, per world: one ground owns the whole surface and the brand inks sit on it as
material, not as accents scattered over a neutral page.

Three registered palettes, one per world. A world never borrows another world's ground.

### World A — board (the flagship, at `/`)
| Token | Value | Role |
|---|---|---|
| `--board` | `#242C28` | slate green-black chalkboard, the whole surface |
| `--board-deep` | `#1A211E` | the action bar and the close block |
| `--board-lift` | `#2E3833` | raised patches: the visit notice |
| `--chalk` | `#F3F6F1` | chalk, warm-tinted so it sits on slate rather than glares |
| `--chalk-body` | `rgba(243,246,241,.80)` | body copy, 8.6:1 on the board |
| `--chalk-dim` | `rgba(243,246,241,.62)` | small data text, 5.3:1 |
| `--rule` | `rgba(243,246,241,.22)` | hairlines only, never text |
| `--pink-solid` | `#FF3D9A` | the proof's ink exactly, for fills and the primary action |
| `--pink` | `#FF5AA7` | the same ink lifted for legibility as chalk on slate |
| `--yellow` | `#FFE800` | emphasis, prices, focus rings |

### World B — crayon (`/v/crayon/`)
Ground `#245FAE` construction-paper blue, wax `#F7F3E6`, crayon pink `#FF6FB2`, crayon yellow
`#FFE800`, masking tape `rgba(255,246,206,.74)`.

### World C — notebook (`/v/notebook/`)
Paper `#FFFFFF`, ballpoint `#1B2A4A`, marker pink `#D6216B` (one step deeper than the proof so
it holds on white), highlighter `#FFE23D`, amber marker `#C87A00` standing in for the yellow
ink where pure `#FFE800` would fail on paper, margin rule `#D8232A`.

The sheet is bare white: the only printed marks on it are the rules, and the margin rule is now
one flat printed line rather than a fade. An earlier build tiled a 5% `feTurbulence` grain over
the page to fake paper tooth, which against an off-white `#FCFCFA` ground read as a dirty,
greyed sheet rather than a clean one. Both are gone. `build/measure_paper.py` holds the line:
the ground has to measure `(255, 255, 255)` across most of the sheet while the rules keep
printing on the 30px pitch.

## The two registries (the rule that holds all three worlds together)

1. **WORLD** — ground, material, dividers, doodles, headings. Hand-drawn, hand-lettered,
   deliberately imperfect.
2. **DATA** — every time, price, spot count and address, always set in **Archivo**, never
   hand-lettered. A player reads a time in bad light, in a car, in February.

The split is a design commitment from the brief, not an accident of implementation. If a
future change makes a price hand-lettered, that change is wrong.

## Type

Self-hosted, three files, 77 KB total (`build/fonts.py`).

| Face | Role | Why |
|---|---|---|
| Gloria Hallelujah | headings, buttons, the mark script | Its uneven baseline and rounded terminals read as a marker held by a hand. |
| Patrick Hand | body copy, prose | Legible hand-lettering at paragraph length, where Gloria would fatigue. |
| Archivo | all data | Neutral, self-hosted, not a training-default display face. |

Archivo ships as one variable file serving weights 400 to 700. The build script dedupes by
content hash; declaring three weights shipped the same 35 KB file three times.

## The mark

The logo is the t-shirt proof's mark, and it stays the same mark in every world. Only the
material changes.

- **12 rays**, alternating pink and yellow, leftmost pink
- rays are **straight with flat ends** (butt caps), about 1:1 against the gap as judged mid-fan
- a **solid pink semicircle dome**, flat base, **no outline**
- a clear gap between the dome edge and the inner end of every ray
- the script sits under the dome and is **wider than the sun** (measured 1.44x; the proof runs
  1.43 to 1.67)
- the script is **two-tone**: pink in pink, sun in yellow
- **no outlines anywhere**, because the proof has none

Generated from `build/logo.py`, so the geometry has one source of truth across all three worlds.
Each world roughens the edge with its own material filter — `#chalk` on the board, `#chalkmark`
in crayon, `#ink` in the notebook — and none of them adds structure. `build/check_worlds.py`
asserts each world's own filter by name, so a world cannot quietly lose its material and still
pass: an earlier version of that gate looked for `#chalk` everywhere, which only passed by
accident.

One deliberate translation: the proof's yellow ink is unreadable on paper (about 1.1:1), so the
notebook world carries it as a deep amber marker. The board and crayon worlds keep the proof's
`#FFE800` exactly. If the yellow has to be exact everywhere, the notebook world is the wrong
world for it, not the wrong yellow.

## Materials, and how they are made

Materials are real SVG turbulence, not a flat imitation.

- **Chalk (A)** — `#chalk` filter: `feTurbulence` displaces the edge for brittleness, coarse
  fractal noise multiplied by fine tooth punches the stroke full of holes, then
  `feComponentTransfer` restores density and a 0.7 px blur adds dust, and a white
  turbulence overlay lays powder over the pigment so the colour reads matte. An early
  version used a dilated blurred halo and read as neon glow; blur is not chalk.
- **Wax (B)** — `#chalkmark`: anisotropic turbulence (`0.03 0.5`) drags the displacement along
  one axis so strokes streak the way a crayon does, with the paper's tooth showing through. It
  is a third of the board's displacement, because the full chalk pass ate the mark's rays.
- **Ballpoint (C)** — `#ink`: a 0.9 px displacement for a nervous but even line, over a broad,
  slow (`0.012 0.05`) density drag so the marker fill breathes across the stroke instead of
  sitting flat. Broad and smooth on purpose, never gritty: high-frequency grain is exactly what
  makes a fill read pencil, and pencil is the wrong material for a ruled sheet. Measured rather
  than eyeballed (`build/measure_fill.py`): the dome's luminance standard deviation is 8.3 in
  the notebook against 8.1 for the chalked board and 0.45 for the waxed crayon, whose waxiness
  lives in its edges rather than its fill.
- **Board ground** — layered radial gradients as wipe marks, a `repeating-linear-gradient` for
  the streaks a board dries in, and a fixed turbulence tile at 13% for slate grain. At phone
  size the strokes alone cannot carry "chalk", so the ground has to.
- **Tape (B)** — a translucent warm sheen, a torn-edge `clip-path`, and a soft shadow. A plain
  rectangle reads as a vector placeholder, not tape.

## Hierarchy

One path, four beats, and nothing said twice.

1. **Tonight's board** — what is on now, which is the reason to open a page like this at all.
2. **What you can book** — a five-row price list, one tap per row, one price each.
3. **Finding us** — address, hours, phone.
4. **Pick a block and go** — the closing reserve block.

Prices appear once (the list), hours once (Finding us), and the closing block repeats nothing the
hero already said. The previous pass carried five programme cards, each with a paragraph, a
schedule line and its own Reserve button; a four-cell stats grid that restated the numbers from
those cards; and membership pricing in a third place. That is five equal-weight choices and seven
booking controls, with no obvious one among them.

The stats grid is gone, its numbers absorbed into the list and the lede. The cards are now rows:
the same five programmes, the same prices on the same schedules, a fifth of the words, and a whole
row as the target instead of a small link inside a card.

## Composition

- **A** — asymmetric hero: copy left, the mark right. Poster pacing, hand-drawn dividers
  between sections.
- **B** — centred and taped up, like a sheet on a wall, with the hero art pinned.
- **C** — the paper's own rules and red margin are the dividers; the sheet needs no drawn
  rules at all, and prose is set on the rule pitch rather than scattered across it.

## Components

- `.btn.go` — the one loud action: pink fill, crisp 3px radius, soft shadow. Deliberately
  rectangular. A button is a booking affordance, so it stays plainly readable while the world
  around it is hand-drawn.
- `.btn.chalkline` — outlined secondary, same geometry.
- `.curl` — an in-prose action, 44 px tall hit area, underlined with a real
  `text-decoration` rather than a coloured box-shadow stripe (a stripe on one edge is a
  recognisable generated-UI tell).
- `.rule` — one authored hand-drawn divider path, stretched to width, generated once and
  shared. World C renders it as a spacer.
- `.actionbar` — the single persistent action. Fixed at the thumb on a phone, returned to the
  header row at 1024 px by CSS alone, so there is exactly one such element in the DOM.
- `.rows` / `.row` — the price list. One row per programme and the whole row is the booking
  control, so `min-height: 44 px` and one hairline between rows. World C needs no border at all:
  the printed rules are the separators and every line of the row is exactly one `--sheet` tall, so
  the list is written onto the paper's own grid rather than laid over it.
- `.close` — the reserve block closing every page.

## Depth, motion, states

- No hard zero-blur offset shadows. Shadows carry an offset and a soft blur, or they are not
  used. Depth is smudge and dust, not a coloured edge.
- Motion is one authored moment: the marquee is gone, and what remains is a 1 px press
  response and a 120 ms hover lift. `prefers-reduced-motion` removes all of it.
- Themed browser surfaces: selection, focus rings (dashed brand yellow), caret, and thin
  scrollbars on the board.
- States designed: hover, active, focus-visible, `disabled` on the reserve button in world A's
  earlier build, and the three availability states (open, low, gone) in the schedule.

## Responsive

Mobile-first. Base rules are written for a 390 px phone in one hand; widening happens in
`min-width: 640px` and `min-width: 1024px` blocks. `env(safe-area-inset-bottom)` is respected on
the fixed bar, and `body` reserves `94 px` beneath it so the bar never covers the footer.

## Bans held

No eyebrow or kicker above a heading. No section numbers. No hard offset shadows. No
card-with-icon-and-text grids. No gradient text. No glassmorphism. No coloured side stripe on
cards. No emoji or unicode glyph standing in for an icon: the sun, the arrow and the dividers
are authored SVG. No monospace costume; Archivo carries the data.

## Open items

- Worlds B and C exist to be chosen between, not to ship together. Only one should survive.
- The mark's rays read as chalk, wax and pen rather than crisp vector lines. That is the worlds
  doing their job. If a crisp mark is ever wanted, the filter comes off the mark element only,
  not off the world.
- `/play/`, `/join/`, `/visit/` and `/faq/` are still the previous poster world. They need the
  chosen world's tokens before the site is coherent.
- The booking platform URL is still unset (`assets/booking.js`, one line).
- The prices and the schedule are invented rather than copied from a real business.
