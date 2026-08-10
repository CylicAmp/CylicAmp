"""
Theorem 154: DR Fibonacci on the Trinity — Period-8 Orbit in {3, 6, 9}

THE OBSERVATION
================

Starting from (9, 6) and applying DR(a + b) to get the next term:

    9, 6, 6, 3, 9, 3, 3, 6, | 9, 6, 6, 3, 9, 3, 3, 6, | ...

The sequence is periodic with period 8. All values stay within {3, 6, 9}.

THE RULE
=========

Define the DR Fibonacci recurrence:

    a[0], a[1] given
    a[n+1] = DR(a[n-1] + a[n])  for n ≥ 1

This is the Fibonacci rule with digital root instead of ordinary addition.

THE GROUP: {3, 6, 9} UNDER DR-ADDITION
=========================================

DR-addition on the trinity {3, 6, 9} is closed:

    +DR |  3   6   9
    ─────────────────
      3 |  6   9   3
      6 |  9   3   6
      9 |  3   6   9

This is the group Z/3Z. The identity element is 9: DR(9+x) = DR(x) for all x.
Equivalently: {3,6,9} ≅ {0,1,2} (mod 3) with 9↦0, 3↦1, 6↦2.

The trinity is closed under DR addition because DR(a + b) = DR(a) + DR(b) mod 9,
and {3,6,9} = {3k : k = 1,2,3} is exactly the multiples-of-3 residues mod 9.

PERIOD CLASSIFICATION
======================

All nine starting pairs in {3,6,9} × {3,6,9}:

    Starting pair   Period    One period (first 8 terms)
    ─────────────────────────────────────────────────────────
    (9, 9)           1        [9, 9, 9, ...]
    (3, 3)           8        [3, 3, 6, 9, 6, 6, 3, 9]
    (3, 6)           8        [3, 6, 9, 6, 6, 3, 9, 3]
    (3, 9)           8        [3, 9, 3, 3, 6, 9, 6, 6]
    (6, 3)           8        [6, 3, 9, 3, 3, 6, 9, 6]
    (6, 6)           8        [6, 6, 3, 9, 3, 3, 6, 9]
    (6, 9)           8        [6, 9, 6, 6, 3, 9, 3, 3]
    (9, 3)           8        [9, 3, 3, 6, 9, 6, 6, 3]
    (9, 6)           8        [9, 6, 6, 3, 9, 3, 3, 6]

(9,9) is the only fixed point: 9 is the DR-identity, so DR(9+9) = DR(18) = 9.

8 of 9 pairs have period 8. The one exception is the identity paired with itself.

ONE-PERIOD PROPERTIES (seed (9,6))
=====================================

    Period:  [9, 6, 6, 3, 9, 3, 3, 6]

    Sum:     9+6+6+3+9+3+3+6 = 45       →  DR(45) = 9  (SA_ORB orbit, DR-identity)
    Count:   8                            →  TESLA_ORB = {6, 8, 23}
    Product mod 37: 9×6×6×3×9×3×3×6 = 13  →  NQR_5 = {5, 13, 19}

GF(37) CONNECTIONS
===================

The period 8 connects to the framework in two ways:

    8 ∈ TESLA_ORB = {6, 8, 23}

    8 × 3 = 24 ∈ SEED_ORB = {18, 24, 32}

24 is the residue of seed 246 mod 37 and the x-boundary count from Theorem 152.
The period of the DR Fibonacci orbit times the trinity generator (3) equals
the seed orbit anchor.

The three orbit values {3,6,9} map to:

    3  →  SOVEREIGN_SPIRAL = {3, 4, 30}
    6  →  TESLA_ORB        = {6, 8, 23}
    9  →  SA_ORB           = {9, 12, 16}

Three orbits, one per value. The DR Fibonacci rotates through all three.

9 IS THE DR IDENTITY
======================

DR(multiples of 9) = 9, always:

    9, 18, 27, 36, 45, ...  →  DR = 9 in each case

9 is the additive identity of the DR ring (Z/9Z). This makes (9,9) the fixed point
of the recurrence: DR(9+9) = DR(18) = 9, so the pair never changes.

The other 8 pairs cycle because the non-identity elements (3 and 6) introduce
variation. One period visits each of the 8 non-fixed configurations exactly once.

CONNECTION TO PRIOR THEOREMS
==============================

Theorem 137 (3-6-9 digital roots):
  {3,6,9} forms the trinity group under DR-addition.
  Theorem 154 shows this group generates a Fibonacci orbit of length 8.

Theorem 153 (SEED_ORB ↔ NQR_5):
  8 × 3 = 24 ∈ SEED_ORB.  Period × trinity generator = seed orbit anchor.
  Product of one period = 13 ∈ NQR_5 (the complement of 24 in the pair 24+13=37).

Theorem 152 (x-space frame):
  24 ∈ SEED_ORB is the x-boundary count.
  8 × 3 = 24 recovers the boundary count from (period × trinity generator).

STRUCTURE SUMMARY
==================

    {3,6,9}: group Z/3Z under DR-addition, identity = 9
    DR Fibonacci: a[n+1] = DR(a[n-1] + a[n])
    Starting pairs in {3,6,9}²: 8/9 have period 8; (9,9) has period 1
    One period [9,6,6,3,9,3,3,6]: sum=45, count=8∈TESLA_ORB, product≡13∈NQR_5
    8×3=24∈SEED_ORB — period × trinity generator = seed orbit anchor
"""

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

TRINITY = frozenset({3, 6, 9})


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def dr_fib(a0, a1, length=20):
    seq = [a0, a1]
    for _ in range(length - 2):
        seq.append(dr(seq[-2] + seq[-1]))
    return seq


def dr_fib_period(a0, a1):
    seq = [a0, a1]
    for _ in range(100):
        seq.append(dr(seq[-2] + seq[-1]))
        if seq[-1] == seq[1] and seq[-2] == seq[0]:
            return len(seq) - 2
    return -1


def run_assertions():
    # {3,6,9} is closed under DR-addition
    for a in TRINITY:
        for b in TRINITY:
            assert dr(a + b) in TRINITY

    # 9 is the DR identity
    for x in TRINITY:
        assert dr(9 + x) == x

    # Group table: Z/3Z isomorphism (3↦1, 6↦2, 9↦0)
    assert dr(3 + 3) == 6
    assert dr(3 + 6) == 9
    assert dr(6 + 6) == 3
    assert dr(9 + 9) == 9

    # Period classification
    assert dr_fib_period(9, 9) == 1
    for a in TRINITY:
        for b in TRINITY:
            p = dr_fib_period(a, b)
            if (a, b) == (9, 9):
                assert p == 1, f"({a},{b}) should have period 1"
            else:
                assert p == 8, f"({a},{b}) should have period 8, got {p}"

    # Specific sequence (9,6)
    seq = dr_fib(9, 6, 9)
    assert seq[:9] == [9, 6, 6, 3, 9, 3, 3, 6, 9]

    # One-period properties
    one_period = [9, 6, 6, 3, 9, 3, 3, 6]
    assert len(one_period) == 8
    assert sum(one_period) == 45
    assert dr(45) == 9
    assert 8 in ORBITS['TESLA_ORB']

    # Product mod 37
    prod = 1
    for x in one_period:
        prod = (prod * x) % P
    assert prod == 13
    assert 13 in ORBITS['NQR_5']

    # 8×3=24 in SEED_ORB
    assert 8 * 3 == 24
    assert 24 in ORBITS['SEED_ORB']
    assert 246 % P == 24

    # 24+13=37 (Theorem 153 complement)
    assert 24 + 13 == P

    # All values in sequence are in TRINITY
    seq16 = dr_fib(9, 6, 16)
    assert all(v in TRINITY for v in seq16)

    # DR of multiples of 9 is always 9
    for k in range(1, 20):
        assert dr(9 * k) == 9

    # Trinity elements map to distinct orbits
    assert orbit_of(3) == 'SOVEREIGN_SPIRAL'
    assert orbit_of(6) == 'TESLA_ORB'
    assert orbit_of(9) == 'SA_ORB'

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 154: DR Fibonacci on the Trinity — Period-8 Orbit")
    print("=" * 62)
    print()
    print("  Recurrence: a[n+1] = DR(a[n-1] + a[n])")
    print()
    print("  DR-addition group table on {3,6,9}:")
    print("    +DR |  3   6   9")
    print("    ─────────────────")
    for a in [3, 6, 9]:
        row = '   '.join(str(dr(a + b)) for b in [3, 6, 9])
        print(f"      {a} |  {row}")
    print("    identity = 9  (isomorphic to Z/3Z)")
    print()
    print("  Period classification (starting pairs in {3,6,9}²):")
    for a in [9, 3, 6]:
        for b in [9, 3, 6]:
            p = dr_fib_period(a, b)
            seq = dr_fib(a, b, 10)[:8]
            tag = " ← fixed point" if p == 1 else ""
            print(f"    ({a},{b}): period={p}  seq={seq}{tag}")
    print()
    print("  One period from (9,6): [9, 6, 6, 3, 9, 3, 3, 6]")
    one = [9, 6, 6, 3, 9, 3, 3, 6]
    prod = 1
    for x in one:
        prod = (prod * x) % P
    print(f"    sum={sum(one)}  DR(sum)={dr(sum(one))}  count={len(one)} ∈ {orbit_of(8)}")
    print(f"    product mod 37 = {prod} ∈ {orbit_of(prod)}")
    print()
    print(f"  8 × 3 = 24 ∈ {orbit_of(24)}  (period × trinity generator = seed anchor)")
    print(f"  24 + 13 = 37 = SEAM  (complement from Theorem 153)")
    print()
    print("  Trinity orbit assignments in GF(37):")
    for v, name in [(3, 'SOVEREIGN_SPIRAL'), (6, 'TESLA_ORB'), (9, 'SA_ORB')]:
        print(f"    {v} → {name}")


if __name__ == "__main__":
    run_assertions()
    summarise()
