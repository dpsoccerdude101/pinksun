# PRODUCT.md — PinkSun

Product truth only. DESIGN.md owns the visual system; this file does not change with a redesign.

## What this is

PinkSun is a **fictional** indoor pickleball club in Wren Hollow, New York, built as a design
concept. Six courts. It exists to demonstrate what a dedicated court club's website could be.

## Audience

Pickleball players in and around Wren Hollow, the invented town the site is set in. The
concept is aimed at a real market of the same shape: Rochester and Monroe County, rated
2.5 to 4.5, looking for indoor courts from November through April. Two distinct visitors:

- **The regular** who wants a specific block on a specific day and is annoyed by a phone call.
- **The first-timer** who has heard about the sport, is not sure they are good enough, and is
  not sure whether they need a partner or their own paddle.

## Surface and mode

**Persuade.** The landing page has to make the offer intelligible and desirable and expose a
clear action. Interior reference pages (visit, FAQ) are Read; the programs hub is Compare.

## Success

A first-time visitor knows what this is, why it matters, and what to do within seconds, on a
phone, in one hand. A regular can reach a booking handoff without calling anyone.

## Constraints

- **Nothing is real.** No courts, no bookings, no charges. Booking hands off to an external
  platform whose URL is not yet chosen (`assets/booking.js`, one line).
- The address, phone number, email and prices are invented, shaped like the real local band
  ($12 drop-in, $65 to $100 monthly, $40 to $45 an hour for a court).
- No blog, no news page, no franchise page. Six-court club, not a network.
- Static HTML. No build step, no framework, no backend.
- Works on GitHub Pages under a project subpath, so all paths stay relative.
- Must be usable in one hand, on a phone, in a cold car in a parking lot in February.
  Mobile is the primary surface, not the fallback.

## Brand commitments

- Colorway is pinned by a real screen-print proof: pink **PMS 806** (`#FF3D9A`) and yellow
  **PMS 803** (`#FFE800`) printed on white. This does not change.
- The mark is a pink semicircular dome with rays alternating pink and yellow.
- The words "pink sun" are set in the hand-lettered brush script from that proof.
- The name is always written "PinkSun" in prose, "pink sun" only in the script mark.

## What must not be lost in a redesign

- The funnel contract: one primary action per surface, every page converts, no dead links.
- Booking, prices and schedules stay plainly readable even when the surrounding world is
  hand-drawn. A player must be able to read a time and a price at a glance, in bad light,
  without decoding lettering.
- Honesty about the concept. No visitor should mistake this for a bookable facility.

## Chosen direction for the current build

Replacing the poster look in place with a **hand-drawn, childlike world**, built mobile-first.
Scope for this pass: the landing page as the flagship surface. Other pages follow the chosen
direction once it is picked.
