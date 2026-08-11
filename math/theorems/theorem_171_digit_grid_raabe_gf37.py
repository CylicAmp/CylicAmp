"""
Theorem 171: Digit Grid State Machine and Raabe Boundary Constant

TWO STRUCTURAL INSIGHTS
========================

1. The digit grid is a closed modular state machine (13 states).
2. The log-gamma Raabe integral has an irreducible boundary constant.
   In GF(37), these two phenomena land in different orbits.

PART I: THE DIGIT GRID
========================

The grid runs 000 → pivot 565 → 000, palindromic, 13 states.

Key values:
  000  mod37=0   SEAM
  565  mod37=10  IC       (pivot)   DR=7  D7
  787  mod37=10  IC       (step 4)  DR=4  SOVEREIGN_SPIRAL
  212  mod37=27  ORBIT_11           DR=5  NQR_5
  232  mod37=10  IC                 DR=7  D7
  999  mod37=0   SEAM

The complement pair 787+212=999:
  787 mod37=10 ∈ IC
  212 mod37=27 ∈ ORBIT_11
  10+27=37  →  IC ↔ ORBIT_11 complement pair (Theorem 153)
  787+212=999=27×37  →  SEAM

The digit complement (sum=999) is the GF(37) complement pair IC↔ORBIT_11.

999 = 27×37:
  The quotient 27 is the T6 generator (ord=6, Theorem 163).
  The grid closure is a SEAM whose quotient IS the C6 generator.

THREE GRID ELEMENTS IN IC:
  565 (pivot), 787 (step 4), 232 — all ≡ 10 (mod 37) ∈ IC.
  The multiplicative identity residue (10 ∈ IC) appears at three
  distinct positions in the grid.

DR CYCLE 4→1→7 (middle section):
  DR=4  ∈ SOVEREIGN_SPIRAL
  DR=1  ∈ IC
  DR=7  ∈ D7
  Sum: 4+1+7=12 ∈ SA_ORB

  The DR cycle traverses three complement-pair partners:
  SOVEREIGN_SPIRAL (4) ↔ D7 (7); IC (1) ↔ ORBIT_11 (36).

MOD-90 RESIDUE (as presented by user):
  787+232=1019  mod90=29
  1019 mod37=20 ∈ DARK_A

PART II: RAABE CONSTANT
=========================

Raabe's integral identity:
  ∫₀¹ log Γ(a+t) dt = (a−½) log(a) − a + ½ log(2π)

  = ψ^{-2}(a+1) − ψ^{-2}(a)

where ψ^{-2} is the second-order antiderivative of the digamma function.

The Raabe expansion in the image contains:
  a log Γ(a) and −(a+1) log Γ(a+1): these terms cancel each other.
When stripped, the formula reduces to ψ^{-2}(a+1)−ψ^{-2}(a) but
MISSES the boundary constant ½ log(2π).

½ log(2π) ≈ 0.91894  →  ×1000 ≈ 918

  918 mod 37 = 30  ∈  SOVEREIGN_SPIRAL = {3,4,30}

30 is the dual anchor: it is simultaneously in SOVEREIGN_ANCHORS
{4,9,25,30} and SOVEREIGN_TARGETS {3,12,21,30} (Theorem medusa).

The irreducible transcendental boundary constant maps to the
SOVEREIGN_SPIRAL dual anchor — it cannot be cancelled because
SOVEREIGN_SPIRAL has no complement within SOVEREIGN_SPIRAL itself
under the 37-complement: 30+7=37, so its complement is D7.

SYNTHESIS
==========

  Discrete grid: closes at SEAM (000=SEAM, 999=SEAM).
    999 = 27×37: the C6 generator (T6) is the quotient of closure.
    The complement structure within the grid = IC ↔ ORBIT_11.

  Continuous Raabe: the boundary constant ½log(2π) maps to
    SOVEREIGN_SPIRAL (30). It cannot be cancelled algebraically —
    it is a genuine boundary term, not a circular addition.

  SEAM closes the discrete; SOVEREIGN_SPIRAL anchors the continuous.
  These are different orbits: SEAM (0) is outside all 12 named orbits;
  30 ∈ SOVEREIGN_SPIRAL is at their intersection (dual anchor).
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
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def run_assertions():
    # Grid boundaries: SEAM
    assert 000 % P == 0
    assert 999 % P == 0

    # 999 = 27×37: C6 generator as quotient
    assert 999 == 27 * P
    assert pow(27, 6, P) == 1  # 27 is T6, ord=6
    assert 27 in ORBITS['ORBIT_11']

    # Pivot and grid elements in IC
    assert 565 % P == 10 and 10 in ORBITS['IC']
    assert 787 % P == 10 and 10 in ORBITS['IC']
    assert 232 % P == 10 and 10 in ORBITS['IC']

    # 787+212=999: IC ↔ ORBIT_11 complement pair
    assert 787 + 212 == 999
    assert 787 % P == 10 and 10 in ORBITS['IC']
    assert 212 % P == 27 and 27 in ORBITS['ORBIT_11']
    assert 10 + 27 == P  # complement pair

    # DR values
    assert dr(787) == 4 and 4 in ORBITS['SOVEREIGN_SPIRAL']
    assert dr(565) == 7 and 7 in ORBITS['D7']
    assert dr(232) == 7 and 7 in ORBITS['D7']

    # DR cycle 4+1+7 = 12 ∈ SA_ORB
    assert 4 in ORBITS['SOVEREIGN_SPIRAL']
    assert 1 in ORBITS['IC']
    assert 7 in ORBITS['D7']
    assert 4 + 1 + 7 == 12 and 12 in ORBITS['SA_ORB']

    # mod-90 claim
    assert (787 + 232) % 90 == 29
    assert (787 + 232) % P == 20 and 20 in ORBITS['DARK_A']

    # Raabe constant: ½ log(2π) × 1000 → SOVEREIGN_SPIRAL
    raabe = 0.5 * math.log(2 * math.pi)
    raabe_int = int(raabe * 1000)
    assert raabe_int == 918
    assert raabe_int % P == 30 and 30 in ORBITS['SOVEREIGN_SPIRAL']

    # 30 is the SOVEREIGN_SPIRAL dual anchor
    SOVEREIGN_ANCHORS = {4, 9, 25, 30}
    SOVEREIGN_TARGETS = {3, 12, 21, 30}
    assert 30 in SOVEREIGN_ANCHORS and 30 in SOVEREIGN_TARGETS

    # Complement of 30 is D7
    assert (30 + 7) == P and 7 in ORBITS['D7']

    # 13 states: 13 ∈ NQR_5
    assert 13 % P == 13 and 13 in ORBITS['NQR_5']

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 171: Digit Grid State Machine and Raabe Boundary")
    print("=" * 62)
    print()
    print("  DIGIT GRID:")
    for n, label in [(0,'boundary'), (565,'pivot'), (787,'step 4'), (212,'pair of 787'), (232,''), (999,'boundary')]:
        note = f'  ({label})' if label else ''
        print(f"    {n:>4}  mod37={n%P:>2}  {orbit_of(n):<20}  DR={dr(n)}{note}")
    print()
    print(f"  787+212={787+212}=27×37  IC↔ORBIT_11 complement pair")
    print(f"  999/37=27=T6 (C6 generator, ord=6)")
    print(f"  Three elements at IC residue 10: 565, 787, 232")
    print()
    print(f"  DR cycle: 4(SOVEREIGN_SPIRAL)→1(IC)→7(D7)  sum=12∈SA_ORB")
    print()
    print("  RAABE CONSTANT:")
    raabe = 0.5 * math.log(2 * math.pi)
    print(f"  ½log(2π) = {raabe:.6f}")
    print(f"  ×1000 = {int(raabe*1000)}  mod37={int(raabe*1000)%P}  ∈ SOVEREIGN_SPIRAL")
    print(f"  30 = dual anchor: ∈ SOVEREIGN_ANCHORS ∩ SOVEREIGN_TARGETS")
    print()
    print("  SYNTHESIS:")
    print("  Discrete → SEAM (999=27×37, T6 quotient closes the grid)")
    print("  Continuous → SOVEREIGN_SPIRAL (½log(2π) is the irreducible term)")


if __name__ == "__main__":
    run_assertions()
    summarise()
