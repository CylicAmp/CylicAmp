# CLASS: AUDIT
"""
A screenshot (2026-11-21) lists eight results credited to L. Alpöge since July 2026. Two of them can be checked here by
direct computation, and both are RIGHT; the other six are recorded with their status from the sources found.

PRIOR WORK IN THIS REPO (found after this file was written): theorem_149_kakeya_jacobian_dimension_gf37.py and
theorem_259_jc3_falsification.py (in the repo since 2026-10-06) already hold this same map, written as
u = 1 + xy, F1 = u^3 z + y^2 u (4 + 3xy), F2 = y + 3x u^2 z + 3x y^2 (4 + 3xy), F3 = 2x - 3x^2 y - x^3 z,
with det JF = -2, three points (0, 0, -1/4), (1, -3/2, 13/2), (-1, 3/2, 13/2) all sent to (-1/4, 0, 0), eight stress
tests and the mod 37 reduction (T259), and the Kakeya comparison at dimension 3 (T149). What is this file's own: the
second fibre (three points over (0, -3, 1), from the cubic w^3 - 2w^2 + Xw - 2Y) and the Hadamard 668 check.

1. JACOBIAN CONJECTURE, DIMENSION 3 -- RIGHT (checked below).
   The explicit map of arXiv 2608.00222 (p(w) = -3w^2 + 4w, q(w) = -w^3 + w^2, g = 2 - 3xy - x^2 z, u = 1 + xy,
   w = g u, F = ((q + g w)/(g x)^2, (p + 2g)/(g x), g x)) is a polynomial map C^3 -> C^3:
       F1 = x^3 y^3 z + 3x^2 y^4 + 3x^2 y^2 z + 7x y^3 + 3x y z + 4y^2 + z
       F2 = 3x^3 y^2 z + 9x^2 y^3 + 6x^2 y z + 12x y^2 + 3x z + y
       F3 = -x^3 z - 3x^2 y + 2x
   Its Jacobian determinant is the constant -2, and the three points (-2/3, 3/2, 117/8), (1/6, -3, -90), (1/2, -3, 18)
   all map to (0, -3, 1), so F is not one-to-one: a counterexample to the Jacobian conjecture in dimension 3.
   (The points come from the inverse: w^3 - 2w^2 + X w - 2Y = 0 with X = v2 v3, Y = v1 v3^2; v = (0, -3, 1) gives
   w = 0, 3, -1.)

2. HADAMARD MATRIX OF ORDER 668 -- RIGHT (checked below).
   The 668 x 668 matrix published at github.com/nreff/hadamard-search, fixtures/known/hm-668/matrix.txt (fetched
   2026-11-21, stored as records/hadamard_668_matrix.txt.gz, sha256 of the text bdeb5059...387b0): every entry is +1 or
   -1 and H H^T = 668 I. 668 = 4 x 167 had been the smallest order with no known Hadamard matrix.

3-8. FROM SOURCES (2026-11-21), not checkable here:
   3. elliptic curve ranks >= 30 and >= 31 (with A. Howell): on the ICARM leaderboard, Aug 20 and Aug 23 2026; exact
      ranks conditional on GRH / BSD; since passed by a rank >= 32 curve (Elkies, Klagsbrun, Li).
   4. Carathéodory conjecture, smooth case: counterexample announced Aug 19 2026; Ando and Umehara (arXiv 2610.34036)
      give a simpler smooth surface with exactly one umbilic. The real-analytic case (Hamburger) is untouched.
   5. 3D Euler blow-up with T. Buckmaster: forced case reported Lean-checked (Aug-Sep 2026); unforced case posted
      Nov 20 2026, not yet verified.
   6. Hopf problem, complex structure on S^6: claimed (manuscript, partial Lean formalization), not settled.
   7. unforced 3D Navier-Stokes blow-up with Buckmaster: posted Nov 20 2026; certificate not released; unverified.
   8. Riemann hypothesis: claimed Nov 20 2026 as Lean code; no independent verification yet.

FALSIFICATION: any assertion failing.
"""
import gzip
import hashlib
import pathlib

import numpy as np
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parents[2]

# 1. the Jacobian counterexample
x, y, z = sp.symbols("x y z")
g, u = 2 - 3 * x * y - x ** 2 * z, 1 + x * y
w = g * u
p, q = -3 * w ** 2 + 4 * w, -w ** 3 + w ** 2
F = [sp.cancel((q + g * w) / (g * x) ** 2), sp.cancel((p + 2 * g) / (g * x)), sp.expand(g * x)]
WRITTEN = [x**3*y**3*z + 3*x**2*y**4 + 3*x**2*y**2*z + 7*x*y**3 + 3*x*y*z + 4*y**2 + z,
           3*x**3*y**2*z + 9*x**2*y**3 + 6*x**2*y*z + 12*x*y**2 + 3*x*z + y,
           -x**3*z - 3*x**2*y + 2*x]
assert all(sp.expand(f - h) == 0 for f, h in zip(F, WRITTEN))                 # the quotients are exact polynomials
assert [sp.Poly(f, x, y, z).total_degree() for f in WRITTEN] == [7, 6, 4]
assert sp.expand(sp.Matrix(WRITTEN).jacobian([x, y, z]).det()) == -2
PTS = [(sp.Rational(-2, 3), sp.Rational(3, 2), sp.Rational(117, 8)), (sp.Rational(1, 6), -3, -90), (sp.Rational(1, 2), -3, 18)]
assert len(set(PTS)) == 3
assert all(tuple(f.subs({x: a, y: b, z: c}) for f in WRITTEN) == (0, -3, 1) for a, b, c in PTS)
W = sp.symbols("W")
assert sorted(sp.solve(W ** 3 - 2 * W ** 2 + (-3 * 1) * W - 2 * (0 * 1), W)) == [-1, 0, 3]

# 2. the Hadamard matrix of order 668
raw = gzip.decompress((ROOT / "records" / "hadamard_668_matrix.txt.gz").read_bytes())
assert hashlib.sha256(raw).hexdigest() == "bdeb5059d77e2703211082627b60441b8c888c928a55cc6f295e011941a387b0"
rows = raw.decode().split()
assert len(rows) == 668 and all(len(r) == 668 and set(r) <= {"+", "-"} for r in rows)
H = np.array([[1 if c == "+" else -1 for c in r] for r in rows], dtype=np.int64)
assert np.array_equal(H @ H.T, 668 * np.eye(668, dtype=np.int64))
assert 668 == 4 * 167 and sp.isprime(167)

if __name__ == "__main__":
    print("Jacobian dim 3: det J = -2 and three points -> (0, -3, 1): counterexample right")
    print("Hadamard 668: H H^T = 668 I: right")

# the same map as T149 / T259, in their form, and their fibre over (-1/4, 0, 0)
U = 1 + x * y
T259 = [U ** 3 * z + y ** 2 * U * (4 + 3 * x * y), y + 3 * x * U ** 2 * z + 3 * x * y ** 2 * (4 + 3 * x * y), 2 * x - 3 * x ** 2 * y - x ** 3 * z]
assert all(sp.expand(a - b) == 0 for a, b in zip(T259, WRITTEN))
T149_PTS = [(0, 0, sp.Rational(-1, 4)), (1, sp.Rational(-3, 2), sp.Rational(13, 2)), (-1, sp.Rational(3, 2), sp.Rational(13, 2))]
assert all(tuple(f.subs({x: a, y: b, z: c}) for f in WRITTEN) == (sp.Rational(-1, 4), 0, 0) for a, b, c in T149_PTS)
assert (ROOT / "math" / "theorems" / "theorem_259_jc3_falsification.py").exists()
assert (ROOT / "math" / "theorems" / "theorem_149_kakeya_jacobian_dimension_gf37.py").exists()
