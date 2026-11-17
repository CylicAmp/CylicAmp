#!/usr/bin/env python3
"""
I.V test case, week of November 16-23, 2026: the refinement rule run in reverse.

Given an area tolerance eps and a display tolerance (a quarter pixel), find the shortest unary word 1^k that
certifies both for the ellipse diag(2, 3) drawn at 100 pixels per unit, on the family n = 6 * 2^k
(math/exhaustion/: the September 22 bundle -- L_n inscribed, U_n circumscribed, g_n = U_n - L_n).

Everything here is exact rational arithmetic (fractions.Fraction). Run it:

    python3 verify_selector.py            runs every check, writes selector_results.json, prints PASS / FAIL
    python3 verify_selector.py --check    re-validates the committed selector_results.json (and the altered copy)

DEFINITIONS (stated here because the addendum with its l_n, u_n is not in the repository):
  x = pi/n.  g_n = U_n - L_n = n sin^3 x / cos x  (math/exhaustion/README.md).
  pi is bracketed by Machin's formula with alternating-series remainders:  PI_LO < pi < PI_HI  (rationals).
  lower bound  l_n = n (y - y^3/6)^3,  y = PI_LO/n     (sin x >= x - x^3/6, increasing on [0, sqrt 2]; cos x <= 1)
  upper bound  u_n = n z^3 / (1 - z^2/2),  z = PI_HI/n (sin x <= x; cos x >= 1 - x^2/2 > 0)
  ellipse diag(2, 3): every area scales by det = 6, so its gap is 6 g_n, with bounds 6 l_n < 6 g_n < 6 u_n.
  display: b = 10/(3n) >= pi/n (pi < 10/3). The circumscribed outline is at most 3 (sec x - 1) units from the
    ellipse (largest semiaxis 3), and sec x - 1 <= x^2/(2 - x^2), so the outline error in pixels is at most
    300 b^2/(2 - b^2). Display certified when that is <= 1/4.
  decision for (eps, n): "certified" if 6 u_n <= eps and the display bound holds; "rejected" if 6 l_n > eps;
    otherwise "undecided" (none occur in the rows here).
  words: C(1^k) = k, side count 6 * 2^C(w); rewrite-result tags 11 -> 2, 111 -> 3.
  selector(eps, k_max): the first k with a certified row; with k_max given (the addendum's nine-mark interface,
    k <= 9) it returns "limit_reached" when no k <= k_max is certified.
"""
import json
import pathlib
import sys
from fractions import Fraction as F

HERE = pathlib.Path(__file__).resolve().parent
RESULTS = HERE / "selector_results.json"
EPSILONS = {"1e-3": F(1, 10 ** 3), "1e-4": F(1, 10 ** 4), "1e-5": F(1, 10 ** 5)}
K_TOP = 10                      # rows k = 0 .. 10
K_LIMIT = 9                     # the addendum's nine-mark interface
DET = 6                         # det diag(2, 3)
PX = 300                        # largest semiaxis 3 at 100 pixels per unit
DISPLAY_TOL = F(1, 4)


def arctan_inv_bounds(m, terms=40):
    """arctan(1/m) bracketed by two consecutive partial sums of its alternating series"""
    s, prev = F(0), F(0)
    for j in range(terms):
        prev = s
        s += F((-1) ** j, (2 * j + 1) * m ** (2 * j + 1))
    return (min(s, prev), max(s, prev))


def pi_bounds():
    a_lo, a_hi = arctan_inv_bounds(5)
    b_lo, b_hi = arctan_inv_bounds(239)
    return 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo   # Machin: pi = 16 atan(1/5) - 4 atan(1/239)


PI_LO, PI_HI = pi_bounds()


def C(word):
    """the supplied count: C(1^k) = k"""
    if set(word) - {"1"}:
        raise ValueError("unary words only")
    return len(word)


def refine(n, word):
    return n * 2 ** C(word)


def bounds(n):
    y, z = PI_LO / n, PI_HI / n
    lo = n * (y - y ** 3 / 6) ** 3
    hi = n * z ** 3 / (1 - z ** 2 / 2)
    return lo, hi


def display_bound(n):
    b = F(10, 3 * n)
    return PX * b ** 2 / (2 - b ** 2)


def decision(n, eps):
    lo, hi = bounds(n)
    if DET * hi <= eps and display_bound(n) <= DISPLAY_TOL:
        return "certified"
    if DET * lo > eps:
        return "rejected"
    return "undecided"


def selector(eps, k_max=None):
    k = 0
    while k_max is None or k <= k_max:
        n = 6 * 2 ** k
        if decision(n, eps) == "certified":
            out = {"status": "certified", "k": k, "word": "1" * k, "n": n, "certificate_6u": str(DET * bounds(n)[1])}
            if k:
                out["predecessor_n"] = n // 2
                out["predecessor_6l"] = str(DET * bounds(n // 2)[0])
            return out
        k += 1
        if k > 60:
            raise RuntimeError("no certificate found")
    return {"status": "limit_reached", "k_max": k_max}


def build():
    rows = []
    for k in range(K_TOP + 1):
        n = 6 * 2 ** k
        lo, hi = bounds(n)
        rows.append({"k": k, "word": "1" * k, "n": n, "ellipse_gap_lower": str(DET * lo), "ellipse_gap_upper": str(DET * hi),
                     "display_bound_px": str(display_bound(n)),
                     "decisions": {name: decision(n, eps) for name, eps in EPSILONS.items()}})
    thresholds = []
    for name, eps in EPSILONS.items():
        s = selector(eps)
        thresholds.append({"eps": name, "first_certified_n": s["n"], "k": s["k"], "preceding_n": s.get("predecessor_n"),
                           "certificate_6u": s["certificate_6u"], "predecessor_6l": s.get("predecessor_6l"),
                           "nine_mark_interface": selector(eps, K_LIMIT)["status"]})
    splits = []
    for k in range(K_TOP + 1):
        for a in range(k + 1):
            n_direct = refine(6, "1" * k)
            n_split = refine(refine(6, "1" * a), "1" * (k - a))
            same = (n_direct == n_split and bounds(n_direct) == bounds(n_split)
                    and all(decision(n_direct, e) == decision(n_split, e) for e in EPSILONS.values()))
            splits.append({"k": k, "a": a, "b": k - a, "n": n_split, "identical": same})
    return {"definitions": "see verify_selector.py docstring", "pi_lo": str(PI_LO), "pi_hi": str(PI_HI),
            "rows": rows, "thresholds": thresholds, "splits": splits,
            "tags": {"11": C("11"), "111": C("111")}}


def validate(results):
    """recompute everything and compare; returns a list of mismatches (empty = valid)"""
    fresh = build()
    bad = []
    for r_old, r_new in zip(results["rows"], fresh["rows"]):
        for key in ("n", "ellipse_gap_lower", "ellipse_gap_upper", "display_bound_px", "decisions"):
            if r_old[key] != r_new[key]:
                bad.append(f"row k={r_new['k']} {key}: recorded {r_old[key]} != computed {r_new[key]}")
    if len(results["rows"]) != len(fresh["rows"]):
        bad.append("row count differs")
    if results["thresholds"] != fresh["thresholds"]:
        bad.append("thresholds differ")
    if results["splits"] != fresh["splits"]:
        bad.append("splits differ")
    return bad


def run_checks():
    out = []

    def claim(name, ok):
        out.append(bool(ok))
        print(("PASS  " if ok else "FAIL  ") + name)

    claim("pi bracketed: %.12f < pi < %.12f" % (float(PI_LO), float(PI_HI)), PI_LO < PI_HI and PI_HI - PI_LO < F(1, 10 ** 20))
    claim("pi < 10/3, so b = 10/(3n) >= pi/n", PI_HI < F(10, 3))
    res = build()
    table = [(t["eps"], t["preceding_n"], t["first_certified_n"], t["k"]) for t in res["thresholds"]]
    claim("thresholds %s" % table, table == [("1e-3", 384, 768, 7), ("1e-4", 768, 1536, 8), ("1e-5", 3072, 6144, 10)])
    for t in res["thresholds"]:
        eps = EPSILONS[t["eps"]]
        n = t["first_certified_n"]
        claim("eps %s: 6 u_%d = %.4g <= eps (first certified)" % (t["eps"], n, float(F(t["certificate_6u"]))),
              F(t["certificate_6u"]) <= eps and display_bound(n) <= DISPLAY_TOL)
        claim("eps %s: 6 l_%d = %.4g > eps (predecessor rejected)" % (t["eps"], n // 2, float(F(t["predecessor_6l"]))),
              F(t["predecessor_6l"]) > eps)
        claim("eps %s: every smaller k rejected directly (proved minimal on 6*2^k)" % t["eps"],
              all(decision(6 * 2 ** j, eps) == "rejected" for j in range(t["k"])))
    claim("no undecided decision in any row", all(d != "undecided" for r in res["rows"] for d in r["decisions"].values()))
    claim("display bound holds from k = 4 (n = 96) on, fails at k = 3: never the binding tolerance in these rows",
          display_bound(96) <= DISPLAY_TOL < display_bound(48))
    claim("strict nesting: both bounds fall at every step k -> k + 1 (g_n decreases in n; proof in the note)",
          all(F(res["rows"][k + 1]["ellipse_gap_upper"]) < F(res["rows"][k]["ellipse_gap_upper"]) and
              F(res["rows"][k + 1]["ellipse_gap_lower"]) < F(res["rows"][k]["ellipse_gap_lower"]) for k in range(K_TOP)))
    claim("nine-mark interface: 1e-3 -> k 7, 1e-4 -> k 8, 1e-5 -> limit_reached",
          [t["nine_mark_interface"] for t in res["thresholds"]] == ["certified", "certified", "limit_reached"])
    claim("at nine marks the 1e-5 row (n = 3072) is rejected, so limit_reached is not hiding a pass",
          decision(3072, EPSILONS["1e-5"]) == "rejected")
    claim("unrestricted unary word: 1e-5 -> k = 10 (n = 6144)", selector(EPSILONS["1e-5"])["k"] == 10)
    claim("66 splits (lengths 0 .. 10): direct = two refinements in side count, bounds and decisions",
          len(res["splits"]) == 66 and all(s["identical"] for s in res["splits"]))
    claim("rewrite-result tags 11 -> 2, 111 -> 3", res["tags"] == {"11": 2, "111": 3})
    claim("unit disk: first n with g_n <= 1e-4 is 768 (the September 22 result), from the same bounds",
          next(6 * 2 ** k for k in range(12) if bounds(6 * 2 ** k)[1] <= F(1, 10 ** 4)) == 768
          and bounds(384)[0] > F(1, 10 ** 4))
    claim("the results validate against a fresh recomputation", validate(res) == [])
    altered = json.loads(json.dumps(res))
    altered["rows"][9]["decisions"]["1e-5"] = "certified"           # n = 3072, eps = 1e-5 changed to pass
    found = validate(altered)
    claim("altered row (n = 3072, eps = 1e-5 set to pass) is rejected: %s" % (found[:1],),
          any("k=9 decisions" in m for m in found))
    return all(out), res


if __name__ == "__main__":
    if "--check" in sys.argv:
        recorded = json.loads(RESULTS.read_text())
        bad = validate(recorded)
        print("committed results valid" if not bad else "INVALID: " + "; ".join(bad))
        sys.exit(1 if bad else 0)
    ok, res = run_checks()
    if ok:
        res["altered_row_test"] = {"row": "n = 3072, eps = 1e-5", "changed_to": "certified", "verifier": "rejected"}
        res["domain_tests"] = {"nine_mark_1e-5": "limit_reached", "unrestricted_1e-5": "k = 10, n = 6144"}
        RESULTS.write_text(json.dumps(res, indent=1) + "\n")
        print("wrote", RESULTS.name)
    sys.exit(0 if ok else 1)
