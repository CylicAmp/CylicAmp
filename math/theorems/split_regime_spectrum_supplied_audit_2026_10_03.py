# CLASS: AUDIT
"""
Audit of supplied text (2026-10-03): "Harmonic Analysis in the Split Regime", Paley graph
analogs, and a unified quadratic-form engine (code verbatim in
tools/supplied/quadratic_regime_harmonics_2026_10_03.py). Checked for p = 5..61.

WRONG
  H1 The "Spectral Magnitude" theorem. With f(j) = chi(g^j) and g a generator, chi(g^j) =
     (-1)^j: the sequence IS a character of C_{p-1}. Its DFT over C_{p-1} is p-1 at
     k = (p-1)/2 and 0 at every other k -- one spike, not a flat sqrt(p). The supplied
     code's own fourier_spectrum returns exactly that (p = 13: twelve entries, all 0 except
     12 at k = 6).
     What IS true: the ADDITIVE transform over Z/p, sum_x chi(x) e^(2 pi i k x / p), has
     magnitude exactly sqrt(p) for every k != 0 (quadratic Gauss sum). That is the sqrt(p)
     in the Paley spectrum. The text puts it on the wrong group.
  H2 The "anisotropic Paley-type graph" on mu_{p+1} with connection set the squares: the
     squares form a SUBGROUP H of the cyclic group, so the Cayley graph is two disjoint
     cliques (the two cosets of H), with loops since 1 is in H. Eigenvalues (p+1)/2 twice
     and 0 -- no sqrt(p), no Jacobi sums. The symmetry condition "p = 3 mod 4" is not
     needed: a subgroup is always closed under inversion.
  H3 Code: SplitQuadraticForm / DegenerateQuadraticForm never store p, so get_partition()
     raises AttributeError; AnisotropicQuadraticForm and TorusHarmonicAnalysis are not
     defined, so any anisotropic input raises NameError. "Probabilistic check" in
     _find_generator is a deterministic check (it works).
  H4 Degenerate partition {"null": 1, "square": p, "nonsquare": 0} is right only when the
     surviving coefficient is a square; for A x^2 with A a non-square the p points are all
     non-square.

CORRECT
  P1 Paley graph on F_p, p = 1 mod 4: strongly regular (p, (p-1)/2, (p-5)/4, (p-1)/4),
     eigenvalues (p-1)/2 once and (-1 +- sqrt(p))/2 each (p-1)/2 times.
  P2 Regime by discriminant; split forms have 2 projective null points and (p-1)/2 points
     of each square class; anisotropic forms have 0 null points and (p+1)/2 of each.
  P3 Torus normalizers dihedral of order 2(p-1) (split) and 2(p+1) (anisotropic): stated,
     not re-checked here.
FALSIFICATION: any assertion failing.
"""
import cmath
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "supplied"))
import quadratic_regime_harmonics_2026_10_03 as sup

PRIMES = [p for p in range(5, 62) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
chi = lambda x, p: 0 if x % p == 0 else (1 if pow(x, (p - 1) // 2, p) == 1 else -1)

for p in PRIMES:
    # H1: multiplicative DFT is a single spike; supplied code agrees
    spec = sup.SplitHarmonicAnalysis(p).fourier_spectrum()
    assert spec == [p - 1 if k == (p - 1) // 2 else 0 for k in range(p - 1)], p
    # the true sqrt(p): additive Gauss sum
    for k in range(1, p):
        G = sum(chi(x, p) * cmath.exp(2j * cmath.pi * k * x / p) for x in range(p))
        assert abs(abs(G) - math.sqrt(p)) < 1e-9

    # P2: projective partition counts by regime
    for (A, B, C) in [(1, 0, -1), (1, 0, 1), (1, 1, 1), (2, 1, 3)]:
        d = (B * B - 4 * A * C) % p
        if d == 0:
            continue
        pts = [(x, 1) for x in range(p)] + [(1, 0)]
        vals = [chi(A * x * x + B * x * y + C * y * y, p) for x, y in pts]
        if chi(d, p) == 1:
            assert (vals.count(0), vals.count(1), vals.count(-1)) == (2, (p - 1) // 2, (p - 1) // 2)
        else:
            assert (vals.count(0), vals.count(1), vals.count(-1)) == (0, (p + 1) // 2, (p + 1) // 2)

    # H4: degenerate A x^2 with A non-square
    A = next(a for a in range(2, p) if chi(a, p) == -1)
    pts_vals = [chi(A * (x * x), p) for x in range(1, p)] + [chi(A, p), 0]  # (x:1) x!=0, (1:0), (0:1) null
    assert pts_vals.count(0) == 1 and pts_vals.count(-1) == p and pts_vals.count(1) == 0

    # P1: Paley graph, p = 1 mod 4
    if p % 4 == 1:
        Adj = np.array([[1 if i != j and chi(i - j, p) == 1 else 0 for j in range(p)] for i in range(p)])
        ev = sorted(np.round(np.linalg.eigvalsh(Adj), 9))
        r, s = (-1 + math.sqrt(p)) / 2, (-1 - math.sqrt(p)) / 2
        assert abs(ev[-1] - (p - 1) / 2) < 1e-6
        assert sum(abs(e - r) < 1e-6 for e in ev) == (p - 1) // 2 == sum(abs(e - s) < 1e-6 for e in ev)
        A2 = Adj @ Adj
        k, lam, mu = (p - 1) // 2, (p - 5) // 4, (p - 1) // 4
        for i in range(p):
            for j in range(p):
                if i != j:
                    assert A2[i, j] == (lam if Adj[i, j] else mu)

    # H2: Cayley graph on cyclic C_{p+1}, connection set = squares (even exponents)
    n = p + 1
    S = {e for e in range(0, n, 2)}
    Adj = np.array([[1 if (j - i) % n in S else 0 for j in range(n)] for i in range(n)])
    ev = sorted(np.round(np.linalg.eigvalsh(Adj), 9))
    assert ev.count(0.0) == n - 2 and ev[-1] == ev[-2] == n // 2              # two cliques
    assert all((-(e)) % n in S for e in S)                                     # closed under inversion, any p

# H3: supplied engine fails as written
u = sup.UnifiedQuadraticForm(1, 0, -1, 13)
try:
    u.get_partition(); raise AssertionError("expected AttributeError")
except AttributeError:
    pass
try:
    sup.UnifiedQuadraticForm(1, 0, 1, 7); raise AssertionError("expected NameError")
except NameError:
    pass

if __name__ == "__main__":
    print("H1: chi(g^j) = (-1)^j -> one spike of height p-1; sqrt(p) is the ADDITIVE Gauss sum")
    print("H2: squares in mu_{p+1} are a subgroup -> two cliques, eigenvalues (p+1)/2, (p+1)/2, 0")
    print(f"P1/P2 verified for p in {PRIMES[0]}..{PRIMES[-1]}")
