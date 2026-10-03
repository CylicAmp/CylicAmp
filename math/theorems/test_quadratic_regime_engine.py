"""Tests for quadratic_regime_engine.py: every regime, brute-force stabilizers over PGL_2."""
import itertools
import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from quadratic_regime_engine import (Fp2, Regime, UnifiedQuadraticForm, legendre,
                                     projective_points)

PRIMES = [3, 5, 7, 11, 13]


def forms(p):
    return [(a, b, c) for a, b, c in itertools.product(range(p), repeat=3) if (a, b, c) != (0, 0, 0)]


def brute_stabilizer(A, B, C, p):
    Q = lambda x, y: (A * x * x + B * x * y + C * y * y) % p
    pts = [(x, y) for x in range(p) for y in range(p)]
    count = 0
    for a, b, c, d in itertools.product(range(p), repeat=4):
        if (a * d - b * c) % p == 0:
            continue
        vals = [(Q(x, y), Q((a * x + b * y) % p, (c * x + d * y) % p)) for x, y in pts]
        lam = next((w * pow(v, -1, p)) % p for v, w in vals if v)
        if all(w == lam * v % p for v, w in vals):
            count += 1
    return count // (p - 1)


@pytest.mark.parametrize("p", PRIMES)
def test_partition_and_regime(p):
    for A, B, C in forms(p):
        q = UnifiedQuadraticForm(A, B, C, p)
        part = q.get_partition()
        assert sum(part.values()) == p + 1
        if q.regime == Regime.SPLIT:
            assert part == {"null": 2, "square": (p - 1) // 2, "nonsquare": (p - 1) // 2}
        elif q.regime == Regime.ANISOTROPIC:
            assert part == {"null": 0, "square": (p + 1) // 2, "nonsquare": (p + 1) // 2}
        else:
            assert part["null"] == 1 and sorted([part["square"], part["nonsquare"]]) == [0, p]


@pytest.mark.parametrize("p", [3, 5, 7])
def test_stabilizer_orders_brute_force(p):
    seen = set()
    for A, B, C in forms(p):
        q = UnifiedQuadraticForm(A, B, C, p)
        if q.regime in seen and p > 3:
            continue
        seen.add(q.regime)
        assert brute_stabilizer(A, B, C, p) == q.get_stabilizer()["order"], (A, B, C, p)


@pytest.mark.parametrize("p", PRIMES + [17, 37])
def test_spectra(p):
    split = UnifiedQuadraticForm(1, 0, -1, p)
    assert split.regime == Regime.SPLIT
    m = split.get_spectrum_magnitudes()
    assert all(abs(v - (p - 1 if k == (p - 1) // 2 else 0)) < 1e-6 for k, v in enumerate(m))
    a = split.get_spectrum_magnitudes("additive")
    assert abs(a[0]) < 1e-6 and all(abs(v - math.sqrt(p)) < 1e-6 for v in a[1:])
    n = next(x for x in range(2, p) if legendre(x, p) == -1)
    aniso = UnifiedQuadraticForm(1, 0, -n, p)
    assert aniso.regime == Regime.ANISOTROPIC
    t = aniso.get_spectrum_magnitudes()
    assert all(abs(v - (p + 1 if k == (p + 1) // 2 else 0)) < 1e-6 for k, v in enumerate(t))


@pytest.mark.parametrize("p", PRIMES + [17])
def test_torus_is_mu_p_plus_1(p):
    F = Fp2(p)
    els = UnifiedQuadraticForm(1, 0, -F.n, p).harmonics.elements
    assert len(set(els)) == p + 1 and all(F.norm(z) == 1 for z in els)


@pytest.mark.parametrize("p", [5, 13, 17, 29, 37])
def test_paley_eigenvalues(p):
    ev = UnifiedQuadraticForm(1, 0, -1, p).graph_eigenvalues()
    Adj = np.array([[1 if i != j and legendre(i - j, p) == 1 else 0 for j in range(p)] for i in range(p)])
    got = np.linalg.eigvalsh(Adj)
    for val, mult in ev.items():
        assert sum(abs(g - val) < 1e-6 for g in got) == mult


@pytest.mark.parametrize("p", [7, 11, 13])
def test_torus_graph_two_cliques(p):
    n = next(x for x in range(2, p) if legendre(x, p) == -1)
    ev = UnifiedQuadraticForm(1, 0, -n, p).graph_eigenvalues()
    N = p + 1
    Adj = np.array([[1 if (j - i) % N % 2 == 0 else 0 for j in range(N)] for i in range(N)])
    got = np.linalg.eigvalsh(Adj)
    for val, mult in ev.items():
        assert sum(abs(g - val) < 1e-6 for g in got) == mult


def test_degenerate_and_errors():
    q = UnifiedQuadraticForm(2, 0, 0, 11)            # 2 is a non-square mod 11
    assert q.regime == Regime.DEGENERATE
    assert q.get_partition() == {"null": 1, "square": 0, "nonsquare": 11}
    with pytest.raises(NotImplementedError):
        q.get_spectrum_magnitudes()
    with pytest.raises(ValueError):
        UnifiedQuadraticForm(1, 0, 1, 9)
