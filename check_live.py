import json, re, urllib.request, urllib.error

BASE = "https://dpsoccerdude101.github.io/pinksun/"
CHECKS = [
    ("", "Six courts", "landing"),
    ("play/", "Five ways", "programs hub"),
    ("join/", "Three ways", "join funnel"),
    ("visit/", "Two minutes", "visit"),
    ("faq/", "Questions,", "faq"),
    ("assets/site.css", ".playrow", "shared css"),
    ("assets/tokens.css", "--pink:#FF3D9A", "tokens css"),
    ("assets/mark.svg", "FF3D9A", "mark svg"),
    ("assets/booking.js", "BOOKING_URL", "booking wiring"),
    ("favicon.svg", "FFE800", "favicon"),
]

ok, bad = [], []
for path, marker, label in CHECKS:
    url = BASE + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8", "replace")
            code = r.status
        if code == 200 and marker in body:
            ok.append(f"200  {label:14} {url}")
        else:
            bad.append(f"{code}  {label:14} missing marker {marker!r} in {url}")
    except urllib.error.HTTPError as e:
        bad.append(f"{e.code}  {label:14} {url}")
    except Exception as e:
        bad.append(f"ERR {label:14} {type(e).__name__} {url}")

print("LIVE HTTP CHECKS")
for line in ok:
    print("  ok ", line)
for line in bad:
    print("  BAD", line)

# extract the internal hrefs the live page actually serves, confirm they are relative
req = urllib.request.Request(BASE, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=30).read().decode()
hrefs = sorted(set(re.findall(r'href="([^"]+)"', html)))
internal = [h for h in hrefs if not h.startswith(("http", "mailto:", "tel:", "#"))]
print("\ninternal hrefs served from the live landing page (must be relative, not root-absolute):")
for h in internal:
    flag = "  <-- ROOT-ABSOLUTE, would break on a project subpath" if h.startswith("/") else ""
    print(f"  {h}{flag}")

print("\nRESULT:", "PASS" if not bad else f"FAIL ({len(bad)})")
