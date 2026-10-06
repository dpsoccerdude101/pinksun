# PinkSun — concept site

A fictional indoor pickleball club in Fairport, New York, built as a design concept.

The mark and the colorway come from a screen-print proof: pink **PMS 806** (`#FF3D9A`),
yellow **PMS 803** (`#FFE800`), printed on white.

**Live:** https://dpsoccerdude101.github.io/pinksun/

## Pages

| Path | Job |
|---|---|
| `/` | The poster. Six courts under one loud sun, plus a live-looking booking widget. |
| `/play/` | Programs hub. Five rows, each with a real action. |
| `/join/` | First-timer onramp, then the three-tier price ladder, then first-visit FAQs. |
| `/visit/` | Hours, the building, directions. |
| `/faq/` | Ten questions, grouped. |

## The funnel

```
/            hero books, plus a scannable program ledger
/play/       picks a program, every row converts
/join/       start here, then pick a tier, deep-linked
```

Rules the build enforces (see `verify.py`):

1. **One primary action per page.** Exactly one `[data-cta="primary"]`. The sticky nav CTA is
   `[data-cta="nav"]` so it never competes with the page's own decision.
2. **Every page converts.** Each page carries at least one `[data-booking]` action and one
   reused reserve block at the foot.
3. **No dead links.** Every internal href resolves to a file on disk.
4. **No nav drift.** All five pages share the same four nav labels plus the CTA.
5. **Nothing overflows.** Checked at 390px wide.

Run the gate:

```bash
python3 verify.py
```

## Wiring the booking platform

Every reservation button carries `data-booking` (and `data-booking-path` for a specific
product). The URL lives in exactly one place:

```js
// assets/booking.js
var BOOKING_URL = "";
```

Set that to the reservation portal and the whole funnel goes live, e.g. a CourtReserve
portal URL. CourtReserve is the default assumption because every dedicated club in the
Rochester market uses it and it supports per-product deep links.

While it is empty, booking buttons point at an on-page notice instead. That is deliberate:
inventing a third-party URL would risk pointing at somebody else's real club.

## Structure

```
.
├── index.html            landing
├── play/index.html       programs hub
├── join/index.html       membership + first-timer funnel
├── visit/index.html      hours and directions
├── faq/index.html        full FAQ
├── assets/
│   ├── tokens.css        color and type tokens (do not drift these)
│   ├── site.css          shared components
│   ├── booking.js        the one place BOOKING_URL lives
│   └── mark.svg          the sunburst
└── verify.py             the gate
```

Paths are relative, not root-absolute, so the site works both on GitHub Pages under a
project subpath and opened straight off the filesystem.

## What is invented

Everything. There are no courts, no bookings and no charges. Program times, prices,
the address, the phone number and the email are all placeholders shaped like the real ones:
the local price band runs $12 drop-in, $65 to $100 monthly, and $40 to $45 an hour for a
court. Do not drive to 240 Sunfield Way.

Research behind the information architecture, including the sitemap and CTA audit of the
real comparables (Fairport Pickleball Club, Dinkers, ROC City, Pickleball Kingdom, Dill
Dinkers, Ace), is in [`design/`](design/): the build plan in `design/plan.md`, the findings
summary in `design/research-notes.md`, and the raw captures in `design/research/`.
