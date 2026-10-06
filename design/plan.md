# PinkSun site — information architecture + two-subpage funnel plan

> **For Hermes:** use the `subagent-driven-development` skill to implement this task-by-task. Each task is self-contained and verifiable on its own.

**Goal:** take the winning variant (001, sunburst poster) from a single landing page to a 3-page site — `/`, `/play`, `/join` — with a defined level-2 hierarchy behind `/play` and a funnel that gets a stranger from the hero to a booking-platform handoff in two clicks.

**Architecture:** static, self-contained HTML. Shared CSS lives in `src/css/` during development and is inlined into every page at build time so the files open correctly from the iOS Files app. No framework, no build server, no external JS beyond Google Fonts.

**Tech stack:** hand-authored HTML/CSS/JS, Google Fonts (Anton, Archivo, Caveat), Playwright + system Chromium for verification, Python `zipfile` for iPhone packaging.

---

## 1. Research: what the real sites actually do

Sitemaps were pulled from `robots.txt` and `/sitemap.xml`; nav labels, CTA text, booking vendors, and published prices were extracted from the live HTML. Raw data: `/data/pinksun/research/sitemaps.json`, `/data/pinksun/research/page_structures.json`.

### 1.1 The closest comparables

| Site | Pages | Booking vendor | Memberships |
|---|---|---|---|
| Fairport Pickleball Club (Fairport, NY) | 20 | CourtReserve | tiered grid, feature lists, non-member reservation $45/hr, guests $16 |
| Dinkers Pickleball Campus (E. Rochester, NY) | 10 | CourtReserve (widget embed) | Single $65/mo, Family $100/mo, **sold in person or by phone only** |
| ROC City Pickleball (Rochester, NY) | 1 + 4 deep pages | CourtReserve | 3 tiers, each with its own "Join Now" deep link to a membership product ID |
| Erie Canal Pickleball (DeWitt, NY) | 7 | CourtReserve | memberships top-level in nav |
| Ace Pickleball Club (national) | 135 | own member portal | per-club pages, MEMBER LOGIN in the main nav |
| Pickleball Kingdom (national) | 369 | PlayByPoint | $15/hr, $20/hr, $30 court rates |
| Dill Dinkers (national) | 275 | CourtReserve | "Get Started" funnel page with anchors |

Sources:
- https://www.fairportpickleballclub.com/sitemap.xml
- https://dinkerspb.com/sitemap
- https://roccitypickleball.com/sitemap.xml
- https://pickleballkingdom.com/sitemap.xml
- https://dilldinkers.com/sitemap.xml
- https://www.acepickleballclub.com/sitemap.xml
- https://www.eriecanalpickleball.com

### 1.2 Seven patterns that repeat across all of them

1. **Programs are a group with children, never a single page.** Fairport's `PLAY` holds eight children (`open-play-and-court-reservations`, `leagues`, `lessons-and-clinics`, `social-dinking`, `coaches`, `tournaments`, ...). Dinkers nests four under `/events/` (`leagues`, `drop-ins`, `lessons`, `tournaments`). Ace uses a `PROGRAMS & EVENTS` folder. This is the two-tier nav convention for the whole category.
2. **Memberships is always a top-level nav item and always shows prices.** Every site publishes at least a partial price ladder. Dill Dinkers is the outlier with no prices on its funnel page.
3. **Booking is off-site, and the website's job is routing.** CourtReserve in 4 of 4 local venues, PlayByPoint at Kingdom, a custom portal at Ace. Nobody books on their own marketing site.
4. **The best funnel deep-links a specific product, not a generic login.** ROC City's three `Join Now` buttons point at `app.courtreserve.com/.../ViewPublicMembership/10899?membershipId=107893`, `...108142`, `...113023` — one membership product ID each. Dinkers, by contrast, sends you to a bare CourtReserve login and sells memberships at the front desk. That gap is the single biggest funnel weakness in the local market.
5. **Mature sites have a dedicated first-timer page.** Dill Dinkers' `/get-started/` is the clearest: anchors for `create-account`, `code-of-conduct`, `rules-regulations`, `open-play-rules`, `faqs`. Fairport has `/faqs`, Kingdom has `/pickleball-101`, ROC City has `/learn-to-play/`. The category treats "I have never done this" as a separate funnel with its own page.
6. **Amenities are a nav item for club-style venues.** Dinkers `Backyard Bar`, Erie Canal `Restaurant`, Fairport `bar-and-food`.
7. **Local sites are small: 10 to 20 pages.** Only franchise networks run 100+. PinkSun should stay in the 8 to 14 page range.

### 1.3 What PinkSun should copy, and what it should beat

Copy: the two-tier Play group, a public price ladder, a first-timer onramp, and off-site booking handoff.

Beat: nobody local sells a membership online in fewer than three clicks, and one venue does not sell online at all. PinkSun's `/join` should put the tier and its checkout link on the same screen.

---

## 2. Information architecture

### 2.1 Sitemap

```
/                          Landing (variant 001, poster)          BUILD THIS PASS
├── /play                  Programs hub, 5 rows, each converts     BUILD THIS PASS
│   ├── /play/open-play        Level, format, when, price
│   ├── /play/leagues          Session dates, DUPR, waitlist
│   ├── /play/clinics          Group of four, coach, video
│   ├── /play/rentals          Hourly, 1-6 courts, BYO four
│   └── /play/juniors          Sat mornings, ages 8-14
├── /join                  Membership + first-visit funnel        BUILD THIS PASS
│   ├── #start                 Create booking account, waiver, level
│   ├── #tiers                 Drop-in / Monthly / Founding fifty
│   └── #faq                   6 questions, first-timer weighted
├── /visit                 Address, hours, parking, café           phase 2
└── /faq                   Full FAQ                                phase 2
```

Level-2 children under `/play` are **specified here, built in phase 2**. `/play` must still convert without them: each program row's primary action deep-links straight into the booking platform's filtered schedule, exactly as Dinkers does with its CourtReserve widget embed. That keeps the hub from being a dead end on day one.

### 2.2 Nav contract (identical on every page)

```
[PinkSun mark]  Play   Join   Visit   FAQ        [CONCEPT]  [Book a court]
```

- Four text links plus one primary CTA. Dinkers runs five, Fairport runs seventeen; four plus a CTA is right for a six-court club.
- `Book a court` is the only primary CTA in the nav and is styled `data-cta="primary"`.
- The `CONCEPT` flag stays, so nobody mistakes the mockup for a live facility.
- Current page gets `aria-current="page"` and a pink underline. Never a second filled button in the nav.

### 2.3 The funnel

```
STRANGER                    EVALUATOR                        READY
google "indoor pickleball   /play  or  /join                 booking platform
fairport"          ──►      ├─ reads level, when, price ──►  (CourtReserve /
        │                   └─ picks a program row           PlayByPoint)
        ▼                        │                                ▲
   / (poster)                    └── "Reserve" deep link ─────────┘
        │
        ├── "Book a court" ──────────────────────────────────────►  handoff
        └── "See programs" ──► /play
```

Rules that make it a funnel rather than a set of pages:

1. **One primary action per page.** `/` books. `/play` picks a program. `/join` picks a tier. No page has two competing filled buttons.
2. **Two clicks to money.** From `/`, a booking handoff is reachable in at most two clicks: `/` → `/play` → program row action, or `/` → `/join` → tier action.
3. **The reserve block is one component, reused at the foot of every page.** Same markup, same copy shape: what you are about to do, what it costs, one button.
4. **Every price is on the page that asks for the decision.** No "call for pricing". Dinkers loses the online membership sale by making you phone the front desk.
5. **The first-timer path never dead-ends.** `/join#start` ends with the same booking handoff, not with a contact form.

---

## 3. Task-by-task plan

Working directory: `/data/pinksun/site/`

### Task 1: Scaffold the workspace and lift the shared tokens

**Objective:** get variant 001's design system out of its single file and into shared CSS, without changing how it looks.

**Files:**
- Create: `/data/pinksun/site/src/css/tokens.css`
- Create: `/data/pinksun/site/src/css/site.css`
- Read: `/data/pinksun/sketches/001-sunburst-poster/index.html`

**Step 1:** Copy the `:root` block from variant 001 into `tokens.css` verbatim. Values that must not drift: `--pink:#FF3D9A`, `--yellow:#FFE800`, `--paper:#FCF8F3`, `--ink:#161110`, `--pink-ink:#B8005F`, `--disp`, `--body`, `--hand`.

**Step 2:** Move the shared component CSS into `site.css`: `.btn` (all three variants), `.label`, `.rule`, `.disp`, the ledger `.row` and its `.hot` state, `.book`/`.chip`/`.day`, `.rates`/`.rate`, `.hours`, `footer`.

**Step 3:** Add the two new components this plan needs:

```css
/* sticky nav, identical on every page */
.bar-in{display:flex;align-items:center;gap:clamp(12px,2vw,28px)}
.bar nav a[aria-current="page"]{border-color:var(--pink)}
[data-cta="primary"]{background:var(--pink);color:#2B0014;border-color:var(--ink)}

/* the reserve block, reused at the foot of every page */
.reserve{border:2px solid var(--ink);background:var(--paper-2);box-shadow:10px 10px 0 var(--ink);
  padding:clamp(20px,3vw,36px);display:grid;grid-template-columns:1fr auto;gap:24px;align-items:center}
@media (max-width:760px){.reserve{grid-template-columns:1fr}}
```

**Step 4:** Verify no visual drift.

Run:
```bash
cd /data/pinksun && python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1440,'height':960})
    pg.goto('file:///data/pinksun/sketches/001-sunburst-poster/index.html',wait_until='networkidle')
    pg.wait_for_timeout(1200)
    pg.screenshot(path='shots/baseline-001.png')
    b.close()"
```
Expected: `shots/baseline-001.png` written. Keep it; Task 8 diffs against it.

**Step 5:** Commit.
```bash
cd /data/pinksun && git init -q 2>/dev/null; git add -A && git commit -q -m "chore: scaffold site workspace and lift 001 tokens"
```

---

### Task 2: Build the shared page shell

**Objective:** one HTML skeleton every page uses, so nav and footer can never drift.

**Files:**
- Create: `/data/pinksun/site/src/partials/shell.html`
- Create: `/data/pinksun/site/build/inline.py`

**Step 1:** Write the shell with three placeholders: `<!--NAV-->`, `<!--MAIN-->`, `<!--FOOTER-->`, plus `<title>{{TITLE}}</title>` and `<meta name="description" content="{{DESC}}">`.

**Step 2:** The nav block, exactly this markup shape:

```html
<header class="bar">
  <div class="bar-in">
    <a class="logo" href="/"><svg …>…</svg><b>PinkSun</b></a>
    <nav>
      <a href="/play/" data-nav="play">Play</a>
      <a href="/join/" data-nav="join">Join</a>
      <a href="/visit/" data-nav="visit">Visit</a>
      <a href="/faq/" data-nav="faq">FAQ</a>
      <span class="concept">Concept</span>
      <a class="btn pink" data-cta="primary" href="{{BOOKING_URL}}" target="_blank" rel="noopener">Book a court</a>
    </nav>
  </div>
</header>
```

**Step 3:** `inline.py` reads a page's `src/pages/*.html`, swaps the partials in, inlines every `<link rel="stylesheet">` as a `<style>` block, and writes `site/<path>/index.html`. This is the pattern the `html-to-screenshot` skill documents: build with shared CSS, inline before delivery, because the iOS Files sandbox will not load sibling CSS.

**Step 4:** Verify the build runs and produces self-contained output.

Run: `python3 /data/pinksun/site/build/inline.py --check`
Expected: prints each output path and `0 external stylesheets remaining`.

**Step 5:** Commit: `feat: shared page shell + CSS inliner`

---

### Task 3: Rebuild `/` on the shell

**Objective:** variant 001's landing page, now using the shell and pointing at real routes.

**Files:**
- Create: `/data/pinksun/site/src/pages/index.html`
- Output: `/data/pinksun/site/index.html`

**Step 1:** Move the existing hero, marquee band, program ledger, booking widget, rates grid, and visit block into the shell unchanged. Keep the poster composition: the mark at scale on the right, the pink band, the outlined `LOUD SUN.` line.

**Step 2:** Change the nav from the current `Play / Book / Rates / Visit` to the nav contract. `Book` is no longer a nav item, it is the CTA.

**Step 3:** Repoint links:
- `See programs` → `/play/`
- `Book a court — $40/hr` → `{{BOOKING_URL}}` (new tab)
- Each of the five ledger rows gets a trailing action cell: `Open play →` linking to `/play/#open-play`, and so on.
- `Rates` section's three tier CTAs → `/join/#tiers` instead of the on-page anchor.

**Step 4:** Keep the on-page booking widget. It is the strongest interaction on the page and it demonstrates the schedule without leaving the site. Add one line under it: `Reservations run through our booking system — this demo does not hold a court.`

**Step 5:** Verify the landing page still passes.

Run: `python3 /data/pinksun/site/verify.py --page /`
Expected: `console: 0 errors · overflow 390px: none · internal links: all resolve · primary CTA count: 1`

**Step 6:** Commit: `feat: rebuild landing page on shared shell`

---

### Task 4: Build `/play` (subpage 1)

**Objective:** the programs hub. Absorbs every long-tail program query and converts each one, with or without its children existing.

**Files:**
- Create: `/data/pinksun/site/src/pages/play.html`
- Output: `/data/pinksun/site/play/index.html`

**Step 1:** Hero, short. Eyebrow `Programs`, headline `Five ways to play`, one paragraph, and a secondary link `Not sure where you fit? Start here →` pointing at `/join/#start`. No big image; the poster statement already happened on `/`.

**Step 2:** The five program rows, reusing the ledger component. Each row is a two-column block, not a card:

| # | Program | Who it is for | When | Price | Row action |
|---|---|---|---|---|---|
| 01 | Open play, levelled | 3.0 / 3.5 / 4.0+ bands, hosted | Daily, 4 blocks | $12 drop-in | `Reserve →` (booking URL, filtered to open play) |
| 02 | Eight-week leagues | Fixed partner, DUPR reported | Tue / Wed / Thu 6:30p | $95 per player | `See session dates →` (`/play/leagues/`) |
| 03 | Clinics of four | Four players, one coach | Mon / Thu 9:00a | $45 group | `Reserve →` (booking URL) |
| 04 | Court rental | Groups of four, 1-6 courts | Any open hour | $40/hr | `Reserve →` (booking URL) |
| 05 | Junior program | Ages 8-14 | Sat 9:00a | $120 per block | `Reserve →` (booking URL) |

Every row's action is a real outbound or internal href. No row is a dead end. This is the pattern Dinkers uses when it embeds the CourtReserve widget on its drop-ins page.

**Step 3:** A "how booking works" block, three steps, because the research says the category treats this as a real objection:

```
1. Create your account — one time, on the booking system. Name, email, phone, waiver.
2. Pick your block — every session we run is published with a level and a court count.
3. Show up — arrive 10 minutes early, paddles and balls are at the desk.
```

End it with `Create your account →` linking to `{{BOOKING_URL}}/register` (or `/join/#start` if the platform URL is unknown at build time).

**Step 4:** The reserve block at the foot, using the shared `.reserve` component.

**Step 5:** Verify.

Run: `python3 /data/pinksun/site/verify.py --page /play/`
Expected: `console: 0 errors · overflow 390px: none · internal links: all resolve · rows with actions: 5/5 · primary CTA count: 1`

**Step 6:** Commit: `feat: add /play programs hub with five converting rows`

---

### Task 5: Build `/join` (subpage 2)

**Objective:** the money page. Public price ladder plus the first-timer onramp, ending in a tier-specific checkout handoff.

**Files:**
- Create: `/data/pinksun/site/src/pages/join.html`
- Output: `/data/pinksun/site/join/index.html`

**Step 1:** Section `#start`, first on the page because the research says a first-timer is the most common visitor to a new club. Heading `First time? Three things and you are in.` Content:

```
1. Create a booking account — 60 seconds, one waiver, no card needed.
2. Tell us your level — or take the free 20-minute assessment on your first visit.
3. Book your first block — first session free for Fairport residents.
```
Then one button: `Create my account →`.

**Step 2:** Section `#tiers`, the three tiers from variant 001, unchanged in copy, with two additions:

| Tier | Price | Action | Deep link |
|---|---|---|---|
| Drop-in | $12 / visit | `Book a block →` | `{{BOOKING_URL}}` |
| Monthly | $79 / month | `Start monthly →` | `{{BOOKING_URL}}/membership/monthly` |
| Founding fifty | $749 / first year | `Claim a seat →` | `{{BOOKING_URL}}/membership/annual` |

Each action is a tier-specific deep link, not a generic login. This is the one thing ROC City does well and Dinkers does not do at all. Under the grid, one line: `Prices are for the concept build. A real club would publish the same ladder and let you buy without calling the front desk.`

**Step 3:** Section `#faq`, six questions weighted to the first-timer:

1. Do I need to be good at this? (band structure, hosts, no tryouts)
2. Do I need a partner? (open play pairs you, leagues need a partner)
3. What does it cost to try it? ($12, or free for a Fairport resident's first session)
4. Do I need my own paddle? (loan included)
5. Can I cancel a membership? (monthly, any month, no fee)
6. Where do I park? (60 spaces at the door)

Each answer is two sentences maximum and states a number.

**Step 4:** The reserve block at the foot, pointing at `{{BOOKING_URL}}`.

**Step 5:** Verify.

Run: `python3 /data/pinksun/site/verify.py --page /join/`
Expected: `console: 0 errors · overflow 390px: none · tiers with deep links: 3/3 · primary CTA count: 1`

**Step 6:** Commit: `feat: add /join with first-timer onramp and tier deep links`

---

### Task 6: Wire the funnel

**Objective:** prove the two-click rule holds, mechanically.

**Files:**
- Create: `/data/pinksun/site/verify.py`
- Modify: `src/partials/shell.html` (only if a nav target is missing)

**Step 1:** Write `verify.py` to assert, per page:
- zero console errors and zero failed requests
- `document.documentElement.scrollWidth <= 392` at a 390px viewport
- every internal `href` resolves to a file that exists on disk
- exactly one element with `data-cta="primary"`
- the nav contains exactly the four contract links plus the CTA
- every element with `data-funnel="program"` has a non-empty `href`

**Step 2:** Add the two-click assertion: from `/`, count clicks to reach any element whose href contains the booking host, following only internal links. Fail if the minimum is greater than 2.

**Step 3:** Run the full pass.
```bash
python3 /data/pinksun/site/verify.py
```
Expected: all three pages pass every assertion; the report prints the click distance.

**Step 4:** Commit: `test: funnel assertions for nav, CTAs, and two-click handoff`

---

### Task 7: Phase-2 child template (specified, not built)

**Objective:** make the five level-2 pages mechanical to add later. Do not build them this pass.

Each `/play/<program>/` child uses this fixed block order:

```
1. Breadcrumb:  Play / Open play            (links to /play/)
2. H1 + one-line what it is
3. Three data cells: When · Level · Price   (mono, from the 003 board style)
4. "What a session looks like" — 4 short lines, no paragraph over 25 words
5. "What to bring" — one line
6. Three FAQs, same six-question pool as /join#faq, filtered
7. The reserve block, identical component
```

Verification for each child: same `verify.py` pass, plus `breadcrumb present` and `reserve block present`.

---

### Task 8: Visual regression and packaging

**Objective:** confirm the poster look survived the refactor, then package for iPhone.

**Step 1:** Re-screenshot `/` at 1440x960 and compare against `shots/baseline-001.png` from Task 1. They must match at the hero; differences are allowed only below the fold where the ledger actions were added.

**Step 2:** Screenshot all three pages at 1440 and at 390 wide.

**Step 3:** Package.
```bash
cd /data/pinksun/site && python3 -c "
import zipfile,os
z=zipfile.ZipFile('/data/pinksun/pinksun-site.zip','w',zipfile.ZIP_DEFLATED)
for r,d,f in os.walk('.'):
    if 'src' in r.split(os.sep) or 'build' in r.split(os.sep): continue
    for n in f:
        if n.endswith(('.html','.md')):
            p=os.path.join(r,n); z.write(p,os.path.relpath(p,'.'))
z.close(); print('ok')"
```
Expected: `/data/pinksun/pinksun-site.zip`, containing three self-contained HTML files.

**Step 4:** Verify self-containment: `grep -c 'rel="stylesheet"' pinksun-site.zip` style check on each extracted page returns 0.

**Step 5:** Commit: `chore: package self-contained site for iPhone delivery`

---

## 4. Files likely to change

```
/data/pinksun/site/
├── src/css/tokens.css              NEW  Task 1
├── src/css/site.css                NEW  Task 1
├── src/partials/shell.html         NEW  Task 2
├── src/pages/index.html            NEW  Task 3
├── src/pages/play.html             NEW  Task 4
├── src/pages/join.html             NEW  Task 5
├── build/inline.py                 NEW  Task 2
├── verify.py                       NEW  Task 6
├── index.html                      GEN  Task 3
├── play/index.html                 GEN  Task 4
└── join/index.html                 GEN  Task 5
```

Untouched: `/data/pinksun/sketches/001-sunburst-poster/index.html` stays as the design reference. `/data/pinksun/research/*` is the evidence base.

## 5. Validation

- `python3 /data/pinksun/site/verify.py` — the gate. Must pass before any commit that touches a page.
- Two-click rule: `/` to a booking host in 2 clicks maximum.
- Zero console errors, zero failed requests, zero horizontal overflow at 390px.
- Every internal link resolves on disk (catches the `/visit/` and `/faq/` links, which are phase 2 and must either exist as stubs or be removed from the nav).
- Self-containment check after inlining: no external stylesheet references remain.

## 6. Risks, tradeoffs, open questions

1. **Booking platform is not chosen.** `{{BOOKING_URL}}` is a placeholder. CourtReserve is what all four local venues use and supports per-product deep links, so it is the default assumption. Confirm before Task 4.
2. **Deep-link URL shape is platform-specific.** ROC City's pattern (`/Online/Memberships/ViewPublicMembership/<id>?membershipId=<id>`) is CourtReserve-specific. If PlayByPoint or Skedda is chosen, every tier link in Task 5 changes. Keep them in one place: a `booking.py` dict, not scattered through HTML.
3. **`/visit` and `/faq` are in the nav contract but phase 2.** Either ship them as thin stubs this pass or drop them from the nav until they exist. Do not ship a nav link to a 404.
4. **iOS may not follow links between local HTML files** in the Files app. If it does not, the fallback is a single long page with anchors, or serving the three pages from a static host. Verify on the phone before promising cross-page navigation.
5. **Prices and program details are invented.** They are placeholders shaped like real ones, drawn from the local price band ($12 drop-in, $65-$100 monthly, $45/hr court). Replace with real numbers before anyone sees this as a business plan.
6. **Deliberate omission:** no blog, no news, no franchise page. Every franchise site has them and every local club does not. PinkSun is a six-court club.
