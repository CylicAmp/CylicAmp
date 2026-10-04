# CLASS: COMPUTATION
"""
Unified engine for binary quadratic forms Q(x, y) = A x^2 + B x y + C y^2 over F_p.

Working replacement for the supplied engine of 2026-10-03
(tools/supplied/quadratic_regime_harmonics_2026_10_03.py; audit in
split_regime_spectrum_supplied_audit_2026_10_03.py). Same entry point and method names;
every value is computed, not hard-coded, and the two spectral claims the audit found wrong
are replaced by what is true.

    from quadratic_regime_engine import UnifiedQuadraticForm
    q = UnifiedQuadraticForm(1, 0, -1, 13)
    q.regime                      # Regime.SPLIT
    q.get_partition()             # {'null': 2, 'square': 6, 'nonsquare': 6}
    q.get_stabilizer()            # {'group': 'D_12', 'order': 24}
    q.get_spectrum_magnitudes()   # multiplicative: one spike, p-1 at k=(p-1)/2
    q.get_spectrum_magnitudes("additive")   # Gauss sum: sqrt(p) at every k != 0
    q.graph_eigenvalues()         # Paley graph (split, p = 1 mod 4)

Regimes (by the discriminant D = B^2 - 4AC):
  SPLIT        D a non-zero square: 2 null points, torus F_p^* = C_{p-1}, normalizer D_{p-1}
  ANISOTROPIC  D a non-square: 0 null points, torus mu_{p+1} = C_{p+1}, normalizer D_{p+1}
  DEGENERATE   D = 0: 1 null point (form is a scalar times a square), stabilizer a Borel
               subgroup of order p(p-1)
Stabilizer = {g in PGL_2(F_p) : Q o g = lambda Q for some lambda != 0}; verified by brute
force over PGL_2 in test_quadratic_regime_engine.py for p <= 13.

Graphs:
  Paley graph on F_p (p = 1 mod 4): eigenvalues (p-1)/2 and (-1 +- sqrt p)/2 -- the sqrt p
  is the additive Gauss sum.
  On the anisotropic torus C_{p+1}, the squares form an index-2 SUBGROUP, so the Cayley graph
  is two disjoint cliques: eigenvalues (p+1)/2 (twice) and 0. Returned as such; it is not a
  Paley analog.
"""
import cmath
import math
from enum import Enum


class Regime(Enum):
    SPLIT = "Hyperbolic"
    ANISOTROPIC = "Elliptic"
    DEGENERATE = "Degenerate"


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, math.isqrt(n) + 1))


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def prime_factors(n):
    out, q = [], 2
    while q * q <= n:
        if n % q == 0:
            out.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        out.append(n)
    return out


def primitive_root(p):
    qs = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in qs):
            return g
    if p == 2:
        return 1
    raise ValueError(f"no primitive root mod {p}")


def projective_points(p):
    return [(x, 1) for x in range(p)] + [(1, 0)]


def dft_magnitudes(seq):
    n = len(seq)
    return [abs(sum(seq[j] * cmath.exp(-2j * cmath.pi * j * k / n) for j in range(n)))
            for k in range(n)]


class QuadraticGeometry:
    """Values of Q on P^1(F_p), up to squares; shared by all regimes."""

    def __init__(self, A, B, C, p):
        self.A, self.B, self.C, self.p = A, B, C, p

    def value(self, x, y):
        return (self.A * x * x + self.B * x * y + self.C * y * y) % self.p

    def get_partition_counts(self):
        cls = [legendre(self.value(x, y), self.p) for x, y in projective_points(self.p)]
        return {"null": cls.count(0), "square": cls.count(1), "nonsquare": cls.count(-1)}


class SplitQuadraticForm(QuadraticGeometry):
    def get_stabilizer_structure(self):
        return {"group": f"D_{self.p - 1}", "order": 2 * (self.p - 1)}


class AnisotropicQuadraticForm(QuadraticGeometry):
    def get_stabilizer_structure(self):
        return {"group": f"D_{self.p + 1}", "order": 2 * (self.p + 1)}


class DegenerateQuadraticForm(QuadraticGeometry):
    def get_stabilizer_structure(self):
        return {"group": "Borel", "order": self.p * (self.p - 1)}


class Fp2:
    """F_{p^2} = F_p[t]/(t^2 - n), n a non-square. Elements are pairs (a, b) = a + b t."""

    def __init__(self, p):
        self.p = p
        self.n = next(a for a in range(2, p) if legendre(a, p) == -1)

    def mul(self, u, v):
        p, n = self.p, self.n
        return ((u[0] * v[0] + n * u[1] * v[1]) % p, (u[0] * v[1] + u[1] * v[0]) % p)

    def power(self, u, e):
        r = (1, 0)
        while e:
            if e & 1:
                r = self.mul(r, u)
            u = self.mul(u, u)
            e >>= 1
        return r

    def norm(self, u):
        return (u[0] * u[0] - self.n * u[1] * u[1]) % self.p

    def torus_generator(self):
        """A generator of the norm-one torus mu_{p+1}."""
        p = self.p
        qs = prime_factors(p + 1)
        for a in range(p):
            for b in range(1, p):
                z = (a, b)
                if self.norm(z) != 1:
                    continue
                if all(self.power(z, (p + 1) // q) != (1, 0) for q in qs):
                    return z
        raise ValueError("no generator of mu_{p+1}")


class SplitHarmonicAnalysis:
    """Torus C_{p-1} = F_p^*, indexed by a primitive root g."""

    def __init__(self, p):
        self.p, self.order = p, p - 1
        g = primitive_root(p)
        self.sequence = [legendre(pow(g, j, p), p) for j in range(self.order)]   # = (-1)^j

    def fourier_spectrum(self):
        """Multiplicative DFT over C_{p-1}: p-1 at k = (p-1)/2, 0 elsewhere."""
        return dft_magnitudes(self.sequence)

    def additive_spectrum(self):
        """|sum_x chi(x) e(kx/p)|: 0 at k = 0, sqrt(p) at every k != 0."""
        p = self.p
        return dft_magnitudes([legendre(x, p) for x in range(p)])

    def graph_eigenvalues(self):
        """Paley graph on F_p; needs p = 1 mod 4 so the connection set is symmetric."""
        p = self.p
        if p % 4 != 1:
            raise ValueError("Paley graph needs p = 1 mod 4")
        r = math.sqrt(p)
        return {(p - 1) / 2: 1, (-1 + r) / 2: (p - 1) // 2, (-1 - r) / 2: (p - 1) // 2}


class TorusHarmonicAnalysis:
    """Torus C_{p+1} = mu_{p+1} in F_{p^2}, indexed by a generator z."""

    def __init__(self, p):
        self.p, self.order = p, p + 1
        F = Fp2(p)
        z = F.torus_generator()
        # square class inside the cyclic group C_{p+1}: z^j is a square there iff j is even
        self.elements = [F.power(z, j) for j in range(self.order)]
        self.sequence = [1 if j % 2 == 0 else -1 for j in range(self.order)]

    def fourier_spectrum(self):
        """Same shape as the split case: p+1 at k = (p+1)/2, 0 elsewhere."""
        return dft_magnitudes(self.sequence)

    def additive_spectrum(self):
        return SplitHarmonicAnalysis(self.p).additive_spectrum()

    def graph_eigenvalues(self):
        """Cayley graph of C_{p+1} on its index-2 subgroup of squares: two cliques."""
        h = (self.p + 1) // 2
        return {float(h): 2, 0.0: self.p - 1}


class UnifiedQuadraticForm:
    def __init__(self, A, B, C, p):
        if not is_prime(p) or p == 2:
            raise ValueError("p must be an odd prime")
        self.p = p
        self.A, self.B, self.C = A % p, B % p, C % p
        if self.A == self.B == self.C == 0:
            raise ValueError("zero form")
        self.delta = (self.B ** 2 - 4 * self.A * self.C) % p
        self.regime = self._detect_regime()
        self._init_geometry()

    def _detect_regime(self):
        if self.delta == 0:
            return Regime.DEGENERATE
        return Regime.SPLIT if legendre(self.delta, self.p) == 1 else Regime.ANISOTROPIC

    def _init_geometry(self):
        args = (self.A, self.B, self.C, self.p)
        if self.regime == Regime.SPLIT:
            self.geometry = SplitQuadraticForm(*args)
            self.harmonics = SplitHarmonicAnalysis(self.p)
        elif self.regime == Regime.ANISOTROPIC:
            self.geometry = AnisotropicQuadraticForm(*args)
            self.harmonics = TorusHarmonicAnalysis(self.p)
        else:
            self.geometry = DegenerateQuadraticForm(*args)
            self.harmonics = None

    def get_partition(self):
        return self.geometry.get_partition_counts()

    def get_stabilizer(self):
        return self.geometry.get_stabilizer_structure()

    def get_spectrum_magnitudes(self, kind="multiplicative"):
        if self.harmonics is None:
            raise NotImplementedError("no torus in the degenerate regime")
        if kind == "multiplicative":
            return self.harmonics.fourier_spectrum()
        if kind == "additive":
            return self.harmonics.additive_spectrum()
        raise ValueError("kind is 'multiplicative' or 'additive'")

    def graph_eigenvalues(self):
        if self.harmonics is None:
            raise NotImplementedError("no torus in the degenerate regime")
        return self.harmonics.graph_eigenvalues()


if __name__ == "__main__":
    for (A, B, C, p) in [(1, 0, -1, 13), (1, 0, 1, 7), (1, 2, 1, 11), (2, 0, 0, 11)]:
        q = UnifiedQuadraticForm(A, B, C, p)
        spec = [round(m, 6) for m in q.get_spectrum_magnitudes()] if q.harmonics else None
        print(f"{A}x^2+{B}xy+{C}y^2 mod {p}: {q.regime.name:11s} {q.get_partition()} {q.get_stabilizer()}")
        if spec:
            print(f"   multiplicative spectrum {spec}")
