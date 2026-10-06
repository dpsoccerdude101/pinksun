#!/usr/bin/env python3
"""Two content fixes across the whole site:

1. The club is no longer in a real village. Fairport, New York becomes Wren Hollow,
   New York, an invented town, and the real highway reference goes with it.
2. The mark is redrawn to the t-shirt proof's geometry (see build/logo.py).

Run from the site root. Idempotent: safe to run twice.
"""
import os, re

ROOT = "/data/pinksun/site"
SKIP_DIRS = {".git", "node_modules", ".impeccable", "fonts"}

EDITS = [
    # order matters: longest and most specific first
    ("240 Sunfield Way<br>Fairport, New York 14450", "240 Sunfield Way<br>Wren Hollow, New York"),
    ("240 Sunfield Way<br>Fairport, New York", "240 Sunfield Way<br>Wren Hollow, New York"),
    ("240 Sunfield Way, Fairport, New York 14450", "240 Sunfield Way, Wren Hollow, New York"),
    ("Fairport, New York · 6 indoor courts", "Wren Hollow, New York · 6 indoor courts"),
    ("Indoor pickleball · Fairport NY", "Indoor pickleball · Wren Hollow NY"),
    ("Indoor pickleball · Fairport, NY", "Indoor pickleball · Wren Hollow, NY"),
    ("Fairport, New York", "Wren Hollow, New York"),
    ("Fairport NY", "Wren Hollow NY"),
    ("Fairport, NY", "Wren Hollow, NY"),
    ("the village of Fairport", "the village"),
    ("From the village of Fairport", "From the village center"),
    ("Fairport residents", "Wren Hollow residents"),
    ("a Fairport resident", "a Wren Hollow resident"),
    ("Fairport resident", "Wren Hollow resident"),
    ("in Fairport", "in Wren Hollow"),
    ("Fairport", "Wren Hollow"),
    # a real state highway ran past the invented town
    ("Two minutes off Route 31, parking at the door", "Two minutes off the village line, parking at the door"),
    ("two minutes off Route 31", "two minutes off the village line"),
    ("Exit at Moseley Road, head north about a mile, then left onto Sunfield Way. Second driveway on the right.",
     "Take the county road north about a mile, then left onto Sunfield Way. Second driveway on the right."),
    ("Six minutes. Take Main Street to Route 31 west, then the same turn at Moseley.",
     "Six minutes. Take Main Street west out of the village, then the same left onto Sunfield Way."),
    ("We are on the north side of the building, second driveway past the light.",
     "We are on the north side of the building, second driveway past the light."),
    ("Route 31", "the village line"),
]

files, hits = [], []
for base, dirs, names in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for n in names:
        if n.endswith((".html", ".md")):
            files.append(os.path.join(base, n))

total = 0
for path in files:
    src = open(path).read()
    out = src
    for old, new in EDITS:
        if old in out:
            total += out.count(old)
            out = out.replace(old, new)
    if out != src:
        open(path, "w").write(out)
        hits.append((os.path.relpath(path, ROOT), sum(1 for _ in re.finditer("Wren Hollow", out))))

print(f"replacements: {total}")
for rel, n in sorted(hits):
    print(f"  {rel:38} {n} 'Wren Hollow' references")

leftover = []
for path in files:
    t = open(path).read()
    if "Fairport" in t or "Route 31" in t:
        leftover.append((os.path.relpath(path, ROOT), t.count("Fairport"), t.count("Route 31")))
if leftover:
    print("\nSTILL PRESENT (fix by hand):")
    for rel, a, b in leftover:
        print(f"  {rel}: Fairport x{a}, Route 31 x{b}")
else:
    print("\nno Fairport or Route 31 strings remain")
