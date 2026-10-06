# Research notes: what the real sites do

Collected 2026-10-06. Sitemaps were read from each site's `robots.txt` and `/sitemap.xml`;
nav labels, CTA text, booking vendor references and published prices were extracted from the
live HTML. Raw data is in `design/research/`.

## The comparables

| Site | Pages | Booking vendor | Memberships |
|---|---|---|---|
| Fairport Pickleball Club (Fairport, NY) | 20 | CourtReserve | tiered grid with feature lists, non-member court $45/hr, guests $16 |
| Dinkers Pickleball Campus (E. Rochester, NY) | 10 | CourtReserve widget embed | Single $65/mo, Family $100/mo, sold in person or by phone only |
| ROC City Pickleball (Rochester, NY) | 1 page + 4 deep pages | CourtReserve | 3 tiers, each with its own Join Now deep link to a membership product ID |
| Erie Canal Pickleball (DeWitt, NY) | 7 | CourtReserve | memberships top-level in nav |
| Ace Pickleball Club (national) | 135 | own member portal | per-club pages, MEMBER LOGIN in the main nav |
| Pickleball Kingdom (national) | 369 | PlayByPoint | $15/hr, $20/hr, $30 court rates |
| Dill Dinkers (national) | 275 | CourtReserve | Get Started funnel page with anchors |

Sources:

- https://www.fairportpickleballclub.com/sitemap.xml
- https://dinkerspb.com/sitemap
- https://roccitypickleball.com/sitemap.xml
- https://pickleballkingdom.com/sitemap.xml
- https://dilldinkers.com/sitemap.xml
- https://www.acepickleballclub.com/sitemap.xml
- https://www.eriecanalpickleball.com

## Seven patterns that repeat

1. **Programs are a group with children, never a single page.** Fairport's `PLAY` holds eight
   children (open play and reservations, leagues, lessons and clinics, social dinking, coaches,
   tournaments). Dinkers nests four under `/events/` (leagues, drop-ins, lessons, tournaments).
   Ace uses a `PROGRAMS & EVENTS` folder. This is the two-tier nav convention for the category.
2. **Memberships is always a top-level nav item and always shows prices.** Every site publishes
   at least a partial ladder. Dill Dinkers is the outlier with no prices on its funnel page.
3. **Booking is off-site, and the website's job is routing.** CourtReserve at four of four local
   venues, PlayByPoint at Kingdom, a custom portal at Ace. Nobody books on their own site.
4. **The best funnel deep-links a specific product, not a generic login.** ROC City's three
   Join Now buttons point at `app.courtreserve.com/.../ViewPublicMembership/10899?membershipId=`
   with a different product ID each. Dinkers sends you to a bare CourtReserve login and sells
   memberships at the front desk. That gap is the biggest funnel weakness in the local market.
5. **Mature sites have a dedicated first-timer page.** Dill Dinkers' `/get-started/` is the
   clearest, with anchors for `create-account`, `code-of-conduct`, `rules-regulations`,
   `open-play-rules`, `faqs`. Fairport has `/faqs`, Kingdom has `/pickleball-101`, ROC City has
   `/learn-to-play/`. The category treats "I have never done this" as a separate funnel.
6. **Amenities are a nav item for club-style venues.** Dinkers `Backyard Bar`, Erie Canal
   `Restaurant`, Fairport `bar-and-food`.
7. **Local sites run 10 to 20 pages.** Only franchise networks run 100+.

## What PinkSun copied, and what it beats

Copied: the two-tier Play group, a public price ladder, a first-timer onramp, and off-site
booking handoff instead of pretending to book in-house.

Beaten: nobody local sells a membership online in fewer than three clicks, and one venue does
not sell online at all. PinkSun's `/join` puts the tier and its checkout link on one screen.

## Note on the local price band

Used to shape the invented prices: drop-in $12 (Dinkers), monthly $65 to $100 (Dinkers, ROC
City), court rental $40 to $45 an hour (Fairport), free intro sessions advertised by both
ROC City and 3TC in East Rochester.
