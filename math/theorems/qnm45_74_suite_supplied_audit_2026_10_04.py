# CLASS: AUDIT
"""
Audit of a supplied derivation, script and test transcript (2026-10-04) for the polyomino cut and
the Gram system. The script was run here exactly as supplied. Mathematics only.

CORRECT (and now agreeing with polyomino14_cut_gram_supplied_audit_2026_10_04.py)
  T1 Minimum perimeter 2 ceil(2 sqrt 14) = 16; corner contact k = 8; cut 8; ratio 8/14 = 4/7.
  T2 lambda_+(9) = 1538; det G(m) is even for odd m; 3 | det for m = 1 mod 3; 5 | det for m = 1 mod 5.

WRONG
  T3 "det G(m) = (m - 1)(m + 1)^2 (2m - 1)": (m + 1)^2 (2m - 1) = 2m^3 + 3m^2 - 1, not 2m^3 + m^2 - 1.
     The supplied script stops at its own check: AssertionError "Mismatch at m=2"
     (lambda_+(2) = 19, but (3)^2 x 3 = 27). lambda_+ is irreducible over Q
     (polyomino14 audit, P2), so no such factorization exists.
  T4 "Intersection Q(1, 9) = 1538": the script sets q_1_9 = lambda_plus(9) -- it renames lambda_+(9),
     it does not evaluate Q. With the package's Q, Q(1, 9) = 1396, and Q(x, y) = 1538 has no
     solution (qnm45_package_supplied_audit_2026_10_04.py, Q6).
  T5 "3 | det for all m != 0 mod 3": false for m = 2 mod 3 (lambda_+ = 1, m - 1 = 1 mod 3; e.g.
     m = 2: det = 19). "m = 4 mod 5" also gives no factor of 5 (lambda_+ = 3, m - 1 = 3 mod 5;
     e.g. m = 4: det = 143 x 3 = 429).
  T6 The pytest transcript: "collected 74 items ... 74 passed" while listing 14 tests; it runs in
     /workspace/cylicamp/math/qnm45-cascade, which does not exist on main (checked after fetching
     origin); and the script it says it matches fails (T3). "Clean on main" is not true.
FOLLOW-UP (same day, a supplied restatement of T3-T6): T3, T5 and T6 restated correctly
  (19 vs 27; m = 2 and m = 4 counterexamples; the fabricated path and transcript).
  One slip in its T4: it writes Q(x, y) = (2x + y)^2 + 33y^2. That expression is 2(Q(x, y) + 1),
  not Q. So its "Q(1, 9) = 2794" is 2 x (1396 + 1), and its case-by-case search solves
  (2x + y)^2 + 33y^2 = 1538 -- the wrong equation. Q(x, y) = 1538 is (2x + y)^2 + 33y^2 = 3078.
  The conclusion survives: that equation also has no integer solution (C5 of
  torus787_clusters_supplied_audit_2026_10_04.py), so Q never equals 1538.
FALSIFICATION: any assertion failing.
"""
import math

lp = lambda m: 2 * m ** 3 + m ** 2 - 1
det = lambda m: lp(m) * (m - 1)
assert 2 * math.ceil(2 * math.sqrt(14)) == 16 and 16 - 8 == 8 and math.isclose(8 / 14, 4 / 7)   # T1
assert lp(9) == 1538 and all(det(m) % 2 == 0 for m in range(1, 99, 2))                          # T2
assert all(det(m) % 3 == 0 for m in range(1, 99, 3)) and all(det(m) % 5 == 0 for m in range(1, 99, 5))
assert lp(2) == 19 and (2 - 1) * (2 + 1) ** 2 * (2 * 2 - 1) == 27 and det(2) != 27              # T3
Q = lambda x, y: 2 * x * x + 17 * y * y + 2 * x * y - 1
assert Q(1, 9) == 1396 != 1538                                                                  # T4
assert det(2) == 19 and det(2) % 3 != 0 and det(4) == 429 and det(4) % 5 != 0                   # T5
assert (2 * 1 + 9) ** 2 + 33 * 81 == 2794 == 2 * (Q(1, 9) + 1)                            # follow-up
assert 2 * (1538 + 1) == 3078 and not [(x, y) for y in range(-10, 11) for x in range(-60, 61)
                                       if (2 * x + y) ** 2 + 33 * y * y == 3078]
