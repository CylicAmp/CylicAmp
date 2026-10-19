# CLASS: AUDIT
"""
Checks of the Egor Checks page (dashboards/egor_checks/index.html), built from the review the owner pasted
(owner_work #353, 2026-10-19). Plain Python + sympy; the browser part needs playwright and Chromium and is skipped
if they are missing. Run: python3 dashboards/egor_checks/check_egor_checks.py

THE REVIEW, claim by claim (the page it reviewed is not in the repository, so these are checked as mathematics):
  RIGHT   61 twin pairs (18x-1, 18x+1) for x <= 500; 2 is a primitive root mod 37; the order counts 12, 6, 4, 6, 2, 2, 2, 1, 1;
          53 primes up to 246; 235 and 679 are 13 mod 37; 130 = 1+4+25+100 over its four smallest divisors;
          the order-3 elements are 10 and 26 (11 has order 6, 27 too); 9x28 = 252, not 246; the twin rows for x <= 37 are
          x = 1, 4, 6, 10, 11, 15, 24, 29 (8 of 37); 72x+9 = 9(8x+1) has digital root 9; 13+37k is 13 mod 37; a finite search
          cannot prove the uniqueness of 130 (the theorem is T245).
  WRONG   "mislabels 17 of the 36 nodes": the rule "every even number is a residue" mislabels 18 (9 even non-residues,
          9 odd residues).
  CAN'T CHECK  the ODE row (amplitude ratio, 125.4 ms, 1.84 ms): no equation in the paste; "both sums come to 333": no sums named;
          the "special cells", the ledger, the Kahan sieve and the hash chain: not in the paste.
  ALSO    the repository's T245 says: k = 4 has 130 alone (proved); k = 5, n even is impossible (proved) and n odd is open.
          So "k = 5 proven" is not what T245 says. The cross-k claim "130 is unique" is retracted there: 1860 (k = 11) and
          148480 (k = 19) also work.

THE PAGE: every row computes its value in the browser and compares it with an expected value; the pill follows from the comparison.
  A yellow control row states a false claim (11 has order 3) and must show FAIL. This script loads the page, reads every pill and every
  value, compares them with Python, and then breaks one expected value in a copy of the page and requires the page to show FAIL.

FALSIFICATION: any assertion failing.
"""
import os
import pathlib
import re
import sys

from sympy import isprime, n_order, primerange, divisors

HERE = pathlib.Path(__file__).resolve().parent
P = 37

# ---- the mathematics -------------------------------------------------------------------------------
orders = {a: n_order(a, P) for a in range(1, P)}
assert orders[2] == 36
counts = sorted(((o, sum(1 for v in orders.values() if v == o)) for o in set(orders.values())), reverse=True)
assert counts == [(36, 12), (18, 6), (12, 4), (9, 6), (6, 2), (4, 2), (3, 2), (2, 1), (1, 1)]
assert [a for a, o in orders.items() if o == 3] == [10, 26] and [a for a, o in orders.items() if o == 6] == [11, 27]
QR = {x * x % P for x in range(1, P)}
assert len(QR) == 18
orbit = [pow(2, k, P) for k in range(36)]
assert all((k % 2 == 0) == (orbit[k] in QR) for k in range(36))
assert sum(1 for n in range(1, 37) if (n % 2 == 0) != (n in QR)) == 18                  # the review said 17
assert len(list(primerange(2, 247))) == 53 and 235 % P == 679 % P == 13
assert 9 * 28 == 252 != 246 and -(-246 // 9) == 28
assert sum(1 for x in range(1, 501) if isprime(18 * x - 1) and isprime(18 * x + 1)) == 61
twins37 = [x for x in range(1, 38) if isprime(18 * x - 1) and isprime(18 * x + 1)]
assert twins37 == [1, 4, 6, 10, 11, 15, 24, 29] and len(twins37) == 8
assert all(sum(map(int, str(72 * x + 9))) % 9 == 0 and 72 * x + 9 == 9 * (8 * x + 1) for x in range(1, 500))
assert all((13 + 37 * k) % 37 == 13 for k in range(1000))
d130 = divisors(130)[:4]
assert d130 == [1, 2, 5, 10] and sum(d * d for d in d130) == 130


def search(N):
    out = []
    for n in range(2, N + 1):
        s = k = 0
        for d in divisors(n):
            s += d * d
            k += 1
            if s >= n:
                break
        if s == n:
            out.append((n, k))
    return out


found = search(200000)
assert found == [(130, 4), (1860, 11), (148480, 19)]

# ---- the page, in a browser ------------------------------------------------------------------------
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

CHROME = next((str(p) for p in (pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux/chrome"))), None)


def run_page(html_path, shot=None):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 900, "height": 1200})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(html_path.as_uri(), wait_until="domcontentloaded")
        page.wait_for_function("document.body.dataset.done", timeout=60000)
        data = page.evaluate("""() => ({
            done: document.body.dataset.done,
            tally: document.getElementById('tally').textContent,
            note: document.getElementById('tally-note').textContent,
            checks: [...document.querySelectorAll('.check')].filter(c => c.querySelector('.pill')).map(c => ({
                title: c.querySelector('h3').textContent, pill: c.querySelector('.pill').textContent,
                cls: c.querySelector('.pill').className, vals: c.querySelector('.vals').textContent})),
            cells: document.querySelectorAll('#grid .cell').length,
            primes: [...document.querySelectorAll('#grid .cell.prime')].map(c => +c.dataset.n),
            twinRows: [...document.querySelectorAll('#twins tr.twin')].map(r => +r.dataset.x),
            twinAll: document.querySelectorAll('#twins tr[data-x]').length,
            ringQR: [...document.querySelectorAll('svg circle.qr')].map(c => +c.dataset.v).sort((a, b) => a - b)})""")
        if shot:
            page.screenshot(path=shot, full_page=True)
        browser.close()
    return data, errors


if sync_playwright is None or CHROME is None:
    print("browser part skipped (playwright or Chromium missing); the mathematics above holds")
    sys.exit(0)

data, errors = run_page(HERE / "index.html", os.environ.get("EGOR_SHOT"))
assert not errors, errors
pills = [c["pill"] for c in data["checks"]]
n_ctl = sum(1 for c in data["checks"] if "ctl" in c["cls"])
n_id = sum(1 for c in data["checks"] if "pill id" in c["cls"])
n_scored = len(pills) - n_ctl - n_id
assert (n_ctl, n_id) == (1, 3) and n_scored == 15, (n_ctl, n_id, n_scored)
assert data["done"] == "pass" and data["tally"] == f"{n_scored} of {n_scored}", data["tally"]
assert pills.count("PASS") == n_scored and pills.count("FAIL (as it must)") == 1 and pills.count("IDENTITY") == 3, pills
assert [c["pill"] for c in data["checks"] if "ctl" in c["cls"]] == ["FAIL (as it must)"]
assert data["cells"] == 246 and data["primes"] == list(primerange(2, 247)) and len(data["primes"]) == 53
assert 3 in data["primes"] and 79 in data["primes"]
assert data["twinRows"] == twins37 and data["twinAll"] == 37
assert data["ringQR"] == sorted(QR)
want = {"Number of primes up to 246": "53", "2 is a primitive root mod 37": "36"}
for c in data["checks"]:
    for k, v in want.items():
        if c["title"] == k:
            assert f"got {v}" in c["vals"], c
assert any("[[130, 4], [1860, 11], [148480, 19]]" in c["vals"] for c in data["checks"])

# null control: break one expected value in a copy of the page; the page has to show FAIL
src = (HERE / "index.html").read_text(encoding="utf-8")
broken = src.replace('exp: 53, run: () => primesUpTo(246).length', 'exp: 54, run: () => primesUpTo(246).length')
assert broken != src
copy = HERE / "_broken_copy.html"
copy.write_text(broken, encoding="utf-8")
try:
    bdata, berrors = run_page(copy)
finally:
    copy.unlink()
assert not berrors and bdata["done"] == "fail" and bdata["tally"] == f"{n_scored - 1} of {n_scored}", bdata["tally"]
assert [c["title"] for c in bdata["checks"] if c["pill"] == "FAIL"] == ["Number of primes up to 246"]

if __name__ == "__main__":
    print("Egor Checks: all rows computed in the browser, control fails as it must; a broken expected value shows FAIL; "
          "twin rows 1, 4, 6, 10, 11, 15, 24, 29; 246 cells, 53 green; the even-number rule mislabels 18, not 17")
