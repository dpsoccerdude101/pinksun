#!/usr/bin/env python3
"""Simpler hierarchy for the PinkSun landing page, and an about section.

What this changes, and why:

1. The five program cards become a five-row price list. The cards carried a
   heading, a price, a two-to-three line paragraph and their own Reserve button;
   five of them is five equal-weight decisions and five competing actions. The
   row list keeps every fact (name, price, schedule) and every booking link,
   including the tier-specific deep link, at a fraction of the height and one
   affordance per row. The prose that was there belongs on /play/ and is on /play/.

2. "What the place is" (a four-cell stat grid restating numbers the hero and the
   price list already give, plus a membership teaser) is replaced by "Who we are".
   That adds the about section and removes the page's weakest section in the same
   edit. Its membership line moves to the price list, which is where pricing lives.

3. Two duplications go: the close block repeated the hero's free-session offer, and
   the footer repeated the visit section's hours verbatim.

Prices now appear once, hours once, and the closing block repeats nothing.

Death of the old selectors: .plays/.play/.when and .facts/.fact are removed from
all three stylesheets, including their references in the tabular-numerals rule and
in the min-width media blocks. No world divides by a card grid any more.
"""
import re
import sys

ROOT = "/data/pinksun/site"
I = f"{ROOT}/index.html"
CK, CR, NB = (f"{ROOT}/assets/{n}.css" for n in ("chalk", "crayon", "notebook"))

log = []


def sub(path, old, new, label):
    with open(path) as f:
        s = f.read()
    if new.strip() and new in s and old not in s:
        log.append(f"skip  {label} (already applied)")
        return
    if old not in s:
        sys.exit(f"FAIL  {label}: anchor not found in {path}")
    with open(path, "w") as f:
        f.write(s.replace(old, new, 1))
    log.append(f"ok    {label}")


ARW = '<svg class="arw" viewBox="0 0 58 20" aria-hidden="true"><use href="#arrowR"/></svg>'


def rows(programs):
    """One row per program: name, price, schedule, drawn arrow. Whole row is the link."""
    out = []
    for nm, pr, small, wt, path in programs:
        out.append(
            f'      <a class="row" data-booking data-booking-path="{path}" href="#booking-note">\n'
            f'        <span class="nm">{nm}</span>\n'
            f'        <span class="pr">{pr}<small>{small}</small></span>\n'
            f'        <span class="wt">{wt}</span>\n'
            f'        {ARW}\n'
            f'      </a>'
        )
    return "\n".join(out)


PROGRAMS = [
    ("Open play, levelled", "$12", "drop in", "Daily &middot; four blocks", "/book/open-play"),
    ("Eight-week leagues", "$95", "per player", "Tue, Wed, Thu &middot; 6:30 PM", "/programs/leagues"),
    ("Clinics of four", "$45", "group of 4", "Mon and Thu &middot; 9:00 AM", "/programs/clinics"),
    ("Court rental", "$40", "per hour", "Any open hour", "/book/court-rental"),
    ("Junior program", "$120", "6 weeks", "Saturdays &middot; 9:00 AM", "/programs/juniors"),
]

NEW_PLAY = f'''  <section id="play" class="wrap">
    <h2>What you can book<span class="sm">Five ways in, and not one of them needs a partner, a tryout, or a phone call.</span></h2>

    <div class="rows">
{rows(PROGRAMS)}
    </div>

    <p class="note">Membership runs $79 a month, or $749 for one of fifty founding seats. <a class="curl" href="join/#tiers">See all three tiers {ARW}</a></p>
  </section>
'''

NEW_ABOUT = '''  <section id="about" class="wrap">
    <h2>Who we are<span class="sm">The name came off a fence, and the courts came out of an empty warehouse.</span></h2>
    <div class="about">
      <p>The first PinkSun sign was scrap plywood on a fence on Sunfield Way, painted by somebody's kid: a pink sun, and the words underneath it. It stayed up long enough that people started calling those courts the pink sun courts.</p>
      <p>We were four players sick of taping lines onto a basketball floor and pulling them up again at nine at night. The warehouse turned up two minutes off the village line, empty, with nothing else claiming the floor.</p>
      <p>So the name stayed and the sign got repainted. We run the place ourselves, the open play, the leagues, the clinics, Saturday mornings for the kids, which means the person at the desk is somebody who plays here.</p>
    </div>
  </section>
'''

# ---------------------------------------------------------------- index.html
with open(I) as f:
    html = f.read()

m = re.search(r'  <section id="play" class="wrap">.*?\n  </section>\n', html, re.S)
if m:
    sub(I, m.group(0), NEW_PLAY, "the five cards become a price list")
else:
    log.append("skip  price list (already applied)")

m = re.search(r'  <section id="board" class="wrap">.*?\n  </section>\n', html, re.S)
if m:
    sub(I, m.group(0), NEW_ABOUT, "'what the place is' becomes 'who we are'")
else:
    log.append("skip  about section (already applied)")

sub(I,
    "        <p>Twelve dollars, ninety minutes, paddle included. First session free for a Wren Hollow resident. If it is not for you, you have lost nothing.</p>",
    "        <p>Twelve dollars, ninety minutes, paddle included. If it is not for you, you have lost nothing.</p>",
    "the close stops repeating the hero's free session")

sub(I,
    '    <p class="fine">Indoor pickleball &middot; Wren Hollow, NY &nbsp;&middot;&nbsp; Mon to Fri 6a&ndash;11p &nbsp;&middot;&nbsp; Sat and Sun 7a&ndash;9p</p>',
    '    <p class="fine">Indoor pickleball &middot; Wren Hollow, NY</p>',
    "the footer stops repeating the opening hours")

sub(I,
    "FIRST VIEWPORT  The hand-drawn pink sun with the brush-script \"pink sun\" under\n"
    "        it, then \"Six courts. One loud sun.\" in chalk, one readable line naming\n"
    "        indoor pickleball, and the pink Book a court button. On a phone the same\n"
    "        action sits fixed at the thumb.",
    "FIRST VIEWPORT  The hand-drawn pink sun with the brush-script \"pink sun\" under\n"
    "        it, then \"Six courts. One loud sun.\" in chalk, one readable line naming\n"
    "        indoor pickleball, and the pink Book a court button. On a phone the same\n"
    "        action sits fixed at the thumb.\n"
    "FUNNEL  Five sections, one path: what is on tonight, what a session costs, who we\n"
    "        are, how to find us, then book. Prices appear once and hours appear once;\n"
    "        the closing block repeats nothing the hero already said. The five programs\n"
    "        are rows, not cards: one affordance each, and the tier-specific booking\n"
    "        deep link survives on every row.",
    "the page's thesis records the funnel")

# ------------------------------------------------------------- the stylesheets
ROW_CSS_COMMON = '''.row{display:grid;grid-template-columns:1fr auto;grid-template-areas:"nm pr" "wt ar";
  align-items:center;gap:2px 14px;padding:13px 2px;min-height:44px;
  color:inherit;text-decoration:none}
.row .nm{grid-area:nm;font-family:var(--hand);font-size:clamp(19px,5vw,21px);line-height:1.12}
.row .pr{grid-area:pr;font-family:var(--data);font-weight:700;font-size:17px;text-align:right;
  white-space:nowrap;font-variant-numeric:tabular-nums}
.row .pr small{display:block;font-family:var(--data);font-weight:600;font-size:10.5px;
  letter-spacing:.07em;text-transform:uppercase;margin-top:3px}
.row .wt{grid-area:wt;font-family:var(--data);font-size:12px;font-weight:600;letter-spacing:.05em;
  text-transform:uppercase;font-variant-numeric:tabular-nums}
.row .arw{grid-area:ar;width:34px;height:12px;justify-self:end;transition:transform .16s ease}
.row:hover .arw,.row:focus-visible .arw{transform:translateX(4px)}
.row:active{transform:translateY(1px)}
'''

ABOUT_CSS_COMMON = '''.about{margin-top:15px;max-width:60ch}
.about p{margin:0 0 14px;font-size:17.5px}
.about p:first-child{font-size:19px}
.about p:last-child{margin-bottom:0}
'''

# --- world A: chalk on a board
sub(CK,
    "/* ---------- program rows ---------- */\n"
    ".plays{margin-top:12px}\n"
    ".play{padding:22px 0;display:grid;grid-template-columns:1fr auto;gap:3px 12px;align-items:start}\n"
    ".play + .play{box-shadow:inset 0 1px 0 var(--rule)}\n"
    ".play h3{font-family:var(--hand);font-size:22px;line-height:1.2;margin:0;grid-column:1}\n"
    ".play .price{font-family:var(--data);font-weight:700;font-size:17px;color:var(--yellow);grid-column:2;text-align:right;white-space:nowrap}\n"
    ".play .price small{display:block;font-weight:600;font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;color:var(--chalk-dim);margin-top:4px}\n"
    ".play p{margin:7px 0 0;grid-column:1/-1;font-size:16.5px;color:var(--chalk-body);max-width:48ch}\n"
    ".play .go2{grid-column:1/-1;margin-top:10px;display:flex;gap:14px;align-items:center;justify-content:space-between}\n"
    ".when{font-family:var(--data);font-size:12px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--chalk-dim)}\n",
    "/* ---------- the price list: one chalked row per program ---------- */\n"
    ".rows{margin-top:12px}\n"
    + ROW_CSS_COMMON
    + ".row{border-bottom:1px solid var(--rule)}\n"
    ".row:last-child{border-bottom:0}\n"
    ".row .pr{color:var(--yellow)}\n"
    ".row .pr small,.row .wt{color:var(--chalk-dim)}\n"
    ".row .arw{color:var(--chalk-dim)}\n"
    ".row:hover .nm,.row:focus-visible .nm{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:5px}\n",
    "chalk: rows replace the cards")

sub(CK,
    "/* ---------- facts ---------- */\n"
    ".facts{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:16px}\n"
    ".fact{padding:15px 13px 13px;background:var(--board-lift);border-radius:3px;box-shadow:0 4px 14px rgba(0,0,0,.24)}\n"
    ".fact b{display:block;font-family:var(--data);font-weight:700;font-size:26px;line-height:1;color:var(--yellow)}\n"
    ".fact span{display:block;margin-top:7px;font-size:15.5px;color:var(--chalk-body)}\n",
    "/* ---------- who we are ---------- */\n" + ABOUT_CSS_COMMON
    + ".about p{color:var(--chalk-body)}\n.about p:first-child{color:var(--chalk)}\n",
    "chalk: the stat grid becomes prose")

sub(CK, ".slot .t,.spots,.when,.play .price,.fact b,.strip .who b{font-variant-numeric:tabular-nums}",
    ".slot .t,.spots,.row .pr,.row .wt,.strip .who b{font-variant-numeric:tabular-nums}",
    "chalk: tabular numerals follow the new data")

sub(CK, "  .facts{grid-template-columns:repeat(4,1fr)}\n  .play{grid-template-columns:1fr auto}\n",
    '  .row{grid-template-columns:1.7fr 8.5em 12em 34px;grid-template-areas:"nm pr wt ar";gap:0 18px}\n'
    "  .row .pr small{display:inline;margin:0 0 0 7px}\n",
    "chalk: the price list goes to one line at 640")

sub(CK, "  .play h3{font-size:26px}\n  .play p{font-size:17.5px}\n",
    "  .row .nm{font-size:22px}\n  .about p{font-size:18px}\n",
    "chalk: desktop type steps")

# --- world B: crayon on construction paper
sub(CR,
    "/* ---------- program rows ---------- */\n"
    ".plays{margin-top:12px}\n"
    ".play{padding:22px 0;display:grid;grid-template-columns:1fr auto;gap:3px 12px;align-items:start}\n"
    ".play + .play{box-shadow:inset 0 1px 0 var(--rule)}\n"
    ".play h3{font-family:var(--hand);font-size:22px;line-height:1.2;margin:0;grid-column:1}\n"
    ".play .price{font-family:var(--data);font-weight:700;font-size:17px;color:var(--yellow);grid-column:2;text-align:right;white-space:nowrap}\n"
    ".play .price small{display:block;font-weight:600;font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;color:var(--wax-dim);margin-top:4px}\n"
    ".play p{margin:7px 0 0;grid-column:1/-1;font-size:16.5px;color:var(--wax-body);max-width:48ch}\n"
    ".play .go2{grid-column:1/-1;margin-top:10px;display:flex;gap:14px;align-items:center;justify-content:space-between}\n"
    ".when{font-family:var(--data);font-size:12px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--wax-dim)}\n",
    "/* ---------- the price list: one wax row per program ---------- */\n"
    ".rows{margin-top:12px}\n"
    + ROW_CSS_COMMON
    + ".row + .row{box-shadow:inset 0 2px 0 var(--rule)}\n"
    ".row .pr{color:var(--yellow)}\n"
    ".row .pr small,.row .wt,.row .arw{color:var(--wax-dim)}\n"
    ".row:hover .nm,.row:focus-visible .nm{text-decoration:underline;text-decoration-thickness:3px;text-underline-offset:5px}\n",
    "crayon: rows replace the cards")

sub(CR,
    "/* ---------- facts ---------- */\n"
    ".facts{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:16px}\n"
    ".fact{padding:15px 13px 13px;background:var(--paper-inset);border-radius:3px;box-shadow:0 4px 14px rgba(0,0,0,.26)}\n"
    ".fact b{display:block;font-family:var(--data);font-weight:700;font-size:26px;line-height:1;color:var(--yellow)}\n"
    ".fact span{display:block;margin-top:7px;font-size:15.5px;color:var(--wax-body)}\n",
    "/* ---------- who we are ---------- */\n" + ABOUT_CSS_COMMON
    + ".about p{color:var(--wax-body)}\n.about p:first-child{color:var(--wax)}\n",
    "crayon: the stat grid becomes prose")

sub(CR, ".slot .t,.spots,.when,.play .price,.fact b,.strip .who b{font-variant-numeric:tabular-nums}",
    ".slot .t,.spots,.row .pr,.row .wt,.strip .who b{font-variant-numeric:tabular-nums}",
    "crayon: tabular numerals follow the new data")

sub(CR, "  .facts{grid-template-columns:repeat(4,1fr)}\n",
    '  .row{grid-template-columns:1.7fr 8.5em 12em 34px;grid-template-areas:"nm pr wt ar";gap:0 18px}\n'
    "  .row .pr small{display:inline;margin:0 0 0 7px}\n",
    "crayon: the price list goes to one line at 640")

sub(CR, "  .play h3{font-size:26px}\n  .play p{font-size:17.5px}\n",
    "  .row .nm{font-size:22px}\n  .about p{font-size:18px}\n",
    "crayon: desktop type steps")

# --- world C: ballpoint on a ruled sheet. Rows sit on the rule pitch.
sub(NB,
    "/* ---------- program rows ---------- */\n"
    ".plays{margin-top:8px}\n"
    ".play{padding:22px 0;display:grid;grid-template-columns:1fr auto;gap:3px 12px;align-items:start}\n"
    ".play h3{font-family:var(--hand);font-size:22px;line-height:1.2;margin:0;grid-column:1}\n"
    ".play .price{font-family:var(--data);font-weight:700;font-size:17px;color:var(--pink);grid-column:2;text-align:right;white-space:nowrap}\n"
    ".play .price small{display:block;font-weight:600;font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-dim);margin-top:4px}\n"
    ".play p{margin:7px 0 0;grid-column:1/-1;font-size:16.5px;color:var(--ink-body);max-width:48ch}\n"
    ".play .go2{grid-column:1/-1;margin-top:8px;display:flex;gap:14px;align-items:center;justify-content:space-between}\n"
    ".when{font-family:var(--data);font-size:12px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-dim)}\n",
    "/* ---------- the price list, written on the printed rules ---------- */\n"
    ".rows{margin-top:calc(var(--sheet) - 4px)}\n"
    + ROW_CSS_COMMON
    + ".row{gap:0 14px;padding:0;min-height:calc(var(--sheet) * 2);align-content:center}\n"
    ".row .pr{color:var(--pink)}\n"
    ".row .pr small,.row .wt,.row .arw{color:var(--ink-dim)}\n"
    ".row:hover .nm,.row:focus-visible .nm{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px}\n",
    "notebook: rows replace the cards")

sub(NB,
    "/* ---------- facts ---------- */\n"
    ".facts{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:14px}\n"
    ".fact{padding:14px 12px 12px;background:#fff;border:2px solid var(--ink);border-radius:3px}\n"
    ".fact b{display:block;font-family:var(--data);font-weight:700;font-size:26px;line-height:1;color:var(--pink)}\n"
    ".fact span{display:block;margin-top:7px;font-size:15.5px;color:var(--ink-body)}\n",
    "/* ---------- who we are ---------- */\n" + ABOUT_CSS_COMMON
    + ".about p{color:var(--ink-body)}\n.about p:first-child{color:var(--ink)}\n",
    "notebook: the stat grid becomes prose")

sub(NB, ".lede,.play p,.note,.close p,footer p,#booking-note p{line-height:var(--sheet)}",
    ".lede,.about p,.note,.close p,footer p,#booking-note p{line-height:var(--sheet)}",
    "notebook: the new prose is written on the ruled lines")

sub(NB, ".slot .t,.spots,.when,.play .price,.fact b,.strip .who b{font-variant-numeric:tabular-nums}",
    ".slot .t,.spots,.row .pr,.row .wt,.strip .who b{font-variant-numeric:tabular-nums}",
    "notebook: tabular numerals follow the new data")

sub(NB, "  .facts{grid-template-columns:repeat(4,1fr)}\n",
    '  .row{grid-template-columns:1.7fr 8.5em 12em 34px;grid-template-areas:"nm pr wt ar";\n'
    "    gap:0 18px;min-height:var(--sheet)}\n"
    "  .row .pr small{display:inline;margin:0 0 0 7px}\n",
    "notebook: the price list goes to one line at 640")

sub(NB, "  .play h3{font-size:26px}\n  .play p{font-size:17.5px}\n",
    "  .row .nm{font-size:22px}\n  .about p{font-size:18px}\n",
    "notebook: desktop type steps")

print("\n".join(log))
leftover = []
for p in (I, CK, CR, NB):
    with open(p) as f:
        s = f.read()
    for dead in (".play", ".plays", ".facts", ".fact ", ".fact{", ".when", "go2"):
        if dead in s:
            leftover.append(f"{p.split('/')[-1]}: {dead}")
print("\nleftover dead selectors: " + ("none" if not leftover else ", ".join(leftover)))
