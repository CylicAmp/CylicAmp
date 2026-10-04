# CLASS: AUDIT
"""
Audit of supplied records (2026-10-04): AUD-WAV-026-GRAM (Gram matrix of the 26-node forward-and-
flip sequence 77 78 87 88 89 98 99 91 19 11 12 21 22 23 32 33 34 43 44 45 54 55 56 65 66 67) and
WAV-009-RECON. Mathematics only.

CORRECT
  G1 sum L^2 = 806 and sum L*R = 741.
  G2 WAV-009-RECON: on the 9 distinct nodes 12 23 ... 89 91 the digit sums are 45 / 45, drift
     8(-1) + 8 = 0, mod-5 sums 20 / 20 -- the correction made in
     outer_step_mod5_supplied_audit_2026_10_04.py, restated accurately.

WRONG
  G3 "sum L^2 = sum R^2 = 806": sum R^2 = 819. The record's own "terminal correction" sees why --
     the right column has three 7s and two 6s, the left two 7s and three 6s -- so the squares
     differ by 49 - 36 = 13. (Digit sums: left 128, right 129.)
  G4 So G = [[806, 741], [741, 819]], not [[806, 741], [741, 806]]:
       trace 1625 (not 1612); det = 806 x 819 - 741^2 = 111,033 = 3^2 x 13^2 x 73 (not 100,555);
       eigenvalues (1625 +- 13 sqrt 12997) / 2 = 1553.53 and 71.47 (not 1547 and 65).
     The matrix is still positive definite (det > 0, trace > 0).
  G5 "13 is the shared common divisor": true of 806 = 2 x 13 x 31, 741 = 3 x 13 x 19 and also of the
     correct 819 = 3^2 x 7 x 13, so 13 divides every entry of G and 13^2 divides det G.
FALSIFICATION: any assertion failing.
"""
import sympy as sp

seq = [77, 78, 87, 88, 89, 98, 99, 91, 19, 11, 12, 21, 22, 23, 32, 33, 34, 43, 44, 45, 54, 55, 56, 65, 66, 67]
L = [x // 10 for x in seq]
R = [x % 10 for x in seq]
a, c, b = sum(x * x for x in L), sum(x * x for x in R), sum(x * y for x, y in zip(L, R))
assert len(seq) == 26 and (a, b) == (806, 741)                                          # G1
nine = [12, 23, 34, 45, 56, 67, 78, 89, 91]                                             # G2
assert sum(x // 10 for x in nine) == sum(x % 10 for x in nine) == 45
assert sum(x // 10 % 5 for x in nine) == sum(x % 10 % 5 for x in nine) == 20
assert c == 819 != 806 and c - a == 49 - 36 and (sum(L), sum(R)) == (128, 129)          # G3
assert (L.count(7), L.count(6), R.count(7), R.count(6)) == (2, 3, 3, 2)
G = sp.Matrix([[a, b], [b, c]])
assert G.trace() == 1625 and G.det() == 111033 == 3 ** 2 * 13 ** 2 * 73                 # G4
ev = sorted(float(v) for v in G.eigenvals())
assert abs(ev[0] - 71.4715) < 1e-3 and abs(ev[1] - 1553.5285) < 1e-3
assert all(x % 13 == 0 for x in (806, 741, 819)) and G.det() % 169 == 0                 # G5
