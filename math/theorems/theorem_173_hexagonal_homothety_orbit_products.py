"""
Theorem 173: Hexagonal Homothety and GF(37) Orbit Product Laws

SETUP
======

Concentric regular hexagons, same center and orientation (homothetic).
  Inner side:  s = 2 cm    (s² = 4,  Area_inner = (3√3/2)s² = 6√3 cm²)
  Outer side:  S = 6 cm    (Area_outer = 54√3 cm²)
  Scale factor: k = S/s = 3
  Area ratio:  k² = 9

THREE ORBIT PRODUCT LAWS
=========================

These arise directly from the hexagon dimensions:

  Law 1:  DARK_A × SOVEREIGN_SPIRAL = TESLA_ORB
    s=2 ∈ DARK_A,  k=3 ∈ SOVEREIGN_SPIRAL,  S=sk=6 ∈ TESLA_ORB
    Proof: {2,15,20} × {3,4,30} mod 37 = {6,8,23} = TESLA_ORB  ✓

  Law 2:  SOVEREIGN_SPIRAL × SOVEREIGN_SPIRAL = SA_ORB
    k=3 ∈ SOVEREIGN_SPIRAL,  k²=9 ∈ SA_ORB
    Proof: {3,4,30} × {3,4,30} mod 37 = {9,12,16} = SA_ORB  ✓

  Law 3:  SA_ORB × TESLA_ORB = NQR_17
    k²=9 ∈ SA_ORB,  inner coeff 6 ∈ TESLA_ORB,  outer coeff 54≡17 ∈ NQR_17
    Proof: {9,12,16} × {6,8,23} mod 37 = {17,22,35} = NQR_17  ✓

SQUARING CHAIN
===============

Law 2 is the first step of a squaring chain:

  SOVEREIGN_SPIRAL →² SA_ORB →² D7 →² SA_ORB →² D7 → ...

  {3,4,30}² mod 37 = {9,12,16}     = SA_ORB   (entry: k → k²)
  {9,12,16}² mod 37 = {7,33,34}    = D7        (contraction residue)
  {7,33,34}² mod 37 = {9,12,16}    = SA_ORB   (period-2 cycle)

  SA_ORB and D7 form a squaring 2-cycle. SOVEREIGN_SPIRAL maps into it.
  Complement pair: SOVEREIGN_SPIRAL ↔ D7 (Theorem 168: 3+34=7+30=37).

  inv(k²) = inv(9) = 33 ∈ D7: the area contraction factor lands in D7,
  which is the orbit SA_ORB squares into.

AREA COEFFICIENTS IN GF(37)
=============================

  Coefficient     Value   mod37   Orbit
  Area_inner      6       6       TESLA_ORB
  Area_annulus    48      11      ORBIT_11
  Area_outer      54      17      NQR_17

  Additive law: 6 + 48 = 54 → in GF(37): 6 + 11 = 17
    TESLA_ORB element + ORBIT_11 generator = NQR_17 element

  Law 3 in action: k² × Area_inner_coeff = Area_outer_coeff
    9 × 6 = 54 ≡ 17 mod 37 ∈ NQR_17  (SA_ORB × TESLA_ORB = NQR_17 ✓)

  Annulus = outer − inner:
    54 − 6 = 48 ≡ 11 mod 37 ∈ ORBIT_11
    NQR_17 − TESLA_ORB → ORBIT_11 (specific: 17−6=11)

GEOMETRIC SERIES IN GF(37)
============================

  Infinite sum of nested annuli:
    48√3 × Σ(1/9)ⁿ = 48√3 × 9/8 = 54√3

  In GF(37): 48 × 9 × inv(8) mod 37
    = 11 × 9 × 14 mod 37  (inv(8)=14)
    = 17 ∈ NQR_17  ✓

  The geometric series closure (sum = outer area) is preserved mod 37.

30-60-90 PINWHEEL
==================

  Outer triangle (hypotenuse = S = 6):
    Short leg = 6 sin(30°) = 3  ∈ SOVEREIGN_SPIRAL
    Long leg  = 6 cos(30°) = 3√3  (coefficient 3 ∈ SOVEREIGN_SPIRAL)

  Inner layer (anchored by s = 2):
    Green side = 2  ∈ DARK_A
    Blue = 2√3      (coefficient 2 ∈ DARK_A)

  Both layers have their integer coefficients in the same orbit:
    Outer: 3 ∈ SOVEREIGN_SPIRAL; Inner: 2 ∈ DARK_A.
    The orbit shifts from SOVEREIGN_SPIRAL to DARK_A across the scale.
"""

import math

P = 37

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}

def orbit_of(v):
    v = v % P
    if v == 0: return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def run_assertions():
    DA = ORBITS['DARK_A']
    SS = ORBITS['SOVEREIGN_SPIRAL']
    SA = ORBITS['SA_ORB']
    TE = ORBITS['TESLA_ORB']
    D7 = ORBITS['D7']
    O11 = ORBITS['ORBIT_11']
    N17 = ORBITS['NQR_17']

    # Hexagon parameters
    s, S, k = 2, 6, 3
    assert s in DA
    assert S in TE
    assert k in SS
    assert k * k == 9 and 9 in SA

    # Inner area coefficient = 6 (3√3/2 × 4 = 6√3)
    area_inner_coeff = 6
    assert area_inner_coeff in TE

    # Law 1: DARK_A × SOVEREIGN_SPIRAL = TESLA_ORB
    prod1 = {(a * b) % P for a in DA for b in SS}
    assert prod1 == TE, f"Law 1 failed: {prod1}"

    # Law 2: SOVEREIGN_SPIRAL × SOVEREIGN_SPIRAL = SA_ORB
    prod2 = {(a * b) % P for a in SS for b in SS}
    assert prod2 == SA, f"Law 2 failed: {prod2}"

    # Law 3: SA_ORB × TESLA_ORB = NQR_17
    prod3 = {(a * b) % P for a in SA for b in TE}
    assert prod3 == N17, f"Law 3 failed: {prod3}"

    # Squaring chain: SS → SA → D7 → SA (period-2 cycle)
    sq_SS = {pow(x, 2, P) for x in SS}
    sq_SA = {pow(x, 2, P) for x in SA}
    sq_D7 = {pow(x, 2, P) for x in D7}
    assert sq_SS == SA
    assert sq_SA == D7
    assert sq_D7 == SA  # D7 ↔ SA_ORB 2-cycle

    # inv(k²) = inv(9) ∈ D7
    inv9 = pow(9, -1, P)
    assert inv9 in D7  # contraction residue is in D7

    # Area coefficients
    assert 48 % P == 11 and 11 in O11   # annulus
    assert 54 % P == 17 and 17 in N17   # outer
    assert (6 + 11) % P == 17           # additive: TESLA_ORB + ORBIT_11 → NQR_17

    # Law 3 in action: 9 × 6 = 54 ≡ 17 ∈ NQR_17
    assert (9 * 6) % P == 17 and 17 in N17

    # Annulus = outer - inner: 17 - 6 = 11 ∈ ORBIT_11
    assert (17 - 6) % P == 11 and 11 in O11

    # Geometric series: 48 × 9 × inv(8) ≡ 17 mod 37
    inv8 = pow(8, -1, P)
    assert (48 * 9 * inv8) % P == 17 and 17 in N17

    # Geometric correctness (real arithmetic)
    s2, S2, k2 = 2.0, 6.0, 3.0
    area_inner = 3 * math.sqrt(3) / 2 * s2**2
    assert abs(area_inner - 6 * math.sqrt(3)) < 1e-10
    area_outer = k2**2 * area_inner
    assert abs(area_outer - 54 * math.sqrt(3)) < 1e-10
    annulus = area_outer - area_inner
    assert abs(annulus - 48 * math.sqrt(3)) < 1e-10
    inf_sum = annulus / (1 - 1/9)
    assert abs(inf_sum - 54 * math.sqrt(3)) < 1e-10

    # 30-60-90 pinwheel legs
    short_outer = S2 * math.sin(math.radians(30))  # = 3
    long_outer  = S2 * math.cos(math.radians(30))  # = 3√3
    assert abs(short_outer - 3) < 1e-10
    assert abs(long_outer - 3 * math.sqrt(3)) < 1e-10
    assert round(short_outer) == 3 and 3 in SS  # 3 ∈ SOVEREIGN_SPIRAL

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 173: Hexagonal Homothety — GF(37) Orbit Product Laws")
    print("=" * 62)
    print()
    print("  Homothety: s=2 (DARK_A) × k=3 (SOVEREIGN_SPIRAL) = S=6 (TESLA_ORB)")
    print()
    print("  THREE ORBIT PRODUCT LAWS:")
    print("    1. DARK_A × SOVEREIGN_SPIRAL  = TESLA_ORB   [s × k = S]")
    print("    2. SOVEREIGN_SPIRAL × SOVEREIGN_SPIRAL = SA_ORB  [k²]")
    print("    3. SA_ORB × TESLA_ORB         = NQR_17      [k² × A_inner → A_outer]")
    print()
    print("  SQUARING CHAIN:")
    print("    SOVEREIGN_SPIRAL →² SA_ORB →² D7 →² SA_ORB → (D7↔SA_ORB cycle)")
    print("    inv(k²) = inv(9) = 33 ∈ D7  (contraction in D7)")
    print()
    print("  AREA COEFFICIENTS mod 37:")
    for label, coeff in [("inner", 6), ("annulus", 48), ("outer", 54)]:
        print(f"    {label:8s}  {coeff}√3  →  {coeff % P:>2}  ∈ {orbit_of(coeff)}")
    print()
    print("  SERIES CLOSURE: 48×9×inv(8) ≡ 17 ≡ 54 (mod 37) ∈ NQR_17")
    print()
    inv9 = pow(9, -1, P)
    print(f"  inv(9) = {inv9} ∈ D7  (D7 = SA_ORB² = inverse of area ratio)")


if __name__ == "__main__":
    run_assertions()
    summarise()
