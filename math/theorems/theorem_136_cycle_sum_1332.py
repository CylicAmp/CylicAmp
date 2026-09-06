"""
Theorem 136: The 246-624-462 Cycle Sum = 36 × 37

FORWARD CYCLE (mod 37 orbit of 246)
=====================================

  n      Factors          mod 37   DR   mod 36   digit sum
  246    2 × 3 × 41         24     3      30        12
  624    2⁴ × 3 × 13        32     3      12        12
  462    2 × 3 × 7 × 11     18     3      30        12

  Mod 37: {24, 32, 18} = SEED_ORB — the 137-map forward orbit.
  DR:     all 3 = ord₃₇(26) — the order of the 137-map multiplier.
  Digit sum: all 12 = log₂(26) — the structural key (Theorem 133).

SUM = 1332 = 36 × 37
======================

  246 + 624 + 462 = 1332
  1332 = 36 × 37 = φ(37) × p

  The sum of the three-cycle equals the product of the group order
  and the prime. 1332 mod 37 = 0 (SEAM). 1332 mod 9 = 0.
  1332 / 36 = 37. 1332 / 37 = 36.

MOD 36 PATTERN (DLOG-SPACE)
==============================

  246 mod 36 = 30   (SOVEREIGN_SPIRAL)
  624 mod 36 = 12 = log₂(26)   ← the 137-map key
  462 mod 36 = 30   (SOVEREIGN_SPIRAL)

  Pattern: 30 − 12 − 30.  Sum mod 36: 72 ≡ 0.
  The center element (624) holds the structural key in dlog-space.
  The outer two (246, 462) both reduce to 30, a sovereign target.

SHARED AND UNIQUE PRIME FACTORS
==================================

  All three share: 2 (DARK_A) and 3 (SOVEREIGN_SPIRAL).
  Unique factors:
    246: 41  → 41 mod 37 = 4   (SOVEREIGN_SPIRAL, SA anchor)
    624: 13  → 13 mod 37 = 13  (NQR_5)
    462: 7   → 7  mod 37 = 7   (D7)
         11  → 11 mod 37 = 11  (ORBIT_11)

  462 is the only element with four distinct prime factors.
  Its unique primes (7 and 11) land in D7 and ORBIT_11 — the
  two QR orbits that are entirely excluded from triangular numbers
  mod 37 (Theorem 135), except for ORBIT_11's element 36.

THE TWO 3-CYCLES: FORWARD AND REVERSE
=========================================

  The six permutations of {2, 4, 6} split into two 3-cycles:

  Forward (SEED_ORB):  246 → 624 → 462   mod37: 24 → 32 → 18
  Reverse (NQR_5):     642 → 426 → 264   mod37: 13 → 19 → 5

  Both cycles sum to 1332 = 36 × 37:
    642 + 426 + 264 = 1332.

  The forward cycle maps to SEED_ORB (all NQR, orbit of the seed).
  The reverse cycle maps to NQR_5 (all NQR, orbit {5, 13, 19}).

  In the 137-map: 24 × 26 ≡ 32, 32 × 26 ≡ 18, 18 × 26 ≡ 24 (mod 37).
  And:            13 × 26 ≡ 19, 19 × 26 ≡ 5,  5  × 26 ≡ 13 (mod 37).

6-DIGIT FAMILY: POSITIONAL CONCATENATION
==========================================

  Position within cycle determines mod-37 of the concatenation:

  Position  Forward  Reverse  Concat    mod 37   Named class
  1st       246      642      246||642 = 246642    0   SEAM
  1st       642      246      642||246 = 642246    0   SEAM
  2nd       624      426      426||624 = 426624   14   NQR_14
  2nd       426      624      624||426 = 624426   14   NQR_14
  3rd       462      264      264||462 = 264462   23   TESLA_ORB
  3rd       264      462      462||264 = 462264   23   TESLA_ORB

  The 6-digit number is divisible by 37 iff both halves are 1st-position
  elements (cycle starts: 246 and 642). Position determines orbit.

ADDITIVE COMPLEMENTS TO SEAM
===============================

  Forward pair:  246 mod 37 = 24,  Reverse pair: 642 mod 37 = 13
  24 + 13 = 37 = SEAM (as shown in Theorem 129)

  All three complement pairs sum to 37:
    246 + 642: 24 + 13 = 37
    624 + 426: 32 + 19 = 51 = 37 + 14 ≡ 14...

  Actually: each forward element + reverse counterpart mod 37:
    24 + 13 = 37 ≡ 0 (SEAM)
    32 + 19 = 51 ≡ 14 (NQR_14)
    18 +  5 = 23 (TESLA_ORB)

  The additive pairing of forward and reverse cycle elements produces
  SEAM, NQR_14, and TESLA_ORB — matching the 6-digit concatenation residues.
"""

P = 37

# Named orbits
SEED_ORB         = frozenset({18, 24, 32})
NQR_5            = frozenset({5, 13, 19})
DARK_A           = frozenset({2, 15, 20})
SOVEREIGN_SPIRAL = frozenset({3, 4, 30})
D7               = frozenset({7, 33, 34})
ORBIT_11         = frozenset({11, 27, 36})
TESLA_ORB        = frozenset({6, 8, 23})
NQR_14           = frozenset({14, 29, 31})

FORWARD = [246, 624, 462]
REVERSE = [642, 426, 264]


def factor(n):
    fac = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            fac[d] = fac.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        fac[n] = fac.get(n, 0) + 1
    return fac


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def run_assertions():
    # Sum = 36 × 37
    assert sum(FORWARD) == 36 * P == 1332
    assert sum(REVERSE) == 36 * P == 1332
    assert 1332 % P == 0
    assert 1332 % 9 == 0

    # mod 37: SEED_ORB forward, NQR_5 reverse
    assert set(n % P for n in FORWARD) == SEED_ORB
    assert set(n % P for n in REVERSE) == NQR_5

    # DR = 3 for all
    assert all(dr(n) == 3 for n in FORWARD + REVERSE)

    # Digit sum = 12 = log₂(26)
    assert all(sum(int(d) for d in str(n)) == 12 for n in FORWARD + REVERSE)

    # mod 36 pattern: 30-12-30
    assert [n % 36 for n in FORWARD] == [30, 12, 30]
    assert [n % 36 for n in REVERSE] == [30, 30, 12]

    # 624 mod 36 = 12 = log₂(26)
    assert 624 % 36 == 12

    # Shared factors: all divisible by 2 and 3
    for n in FORWARD + REVERSE:
        assert n % 2 == 0 and n % 3 == 0

    # Unique factor mod-37 addresses
    assert 41 % P == 4 and 4 in SOVEREIGN_SPIRAL  # 246's unique factor
    assert 13 % P == 13 and 13 in NQR_5            # 624's unique factor
    assert 7 % P == 7 and 7 in D7                  # 462's factors
    assert 11 % P == 11 and 11 in ORBIT_11

    # 137-map closure: ×26 cycles within each orbit
    for n in FORWARD:
        assert (26 * (n % P)) % P in SEED_ORB
    for n in REVERSE:
        assert (26 * (n % P)) % P in NQR_5

    # 6-digit positional concatenation
    assert (246 * 1000 + 642) % P == 0   # 1st position → SEAM
    assert (642 * 1000 + 246) % P == 0
    assert (426 * 1000 + 624) % P == 14 and 14 in NQR_14  # 2nd → NQR_14
    assert (624 * 1000 + 426) % P == 14
    assert (264 * 1000 + 462) % P == 23 and 23 in TESLA_ORB  # 3rd → TESLA_ORB
    assert (462 * 1000 + 264) % P == 23

    # Additive complement pairs
    assert (24 + 13) % P == 0             # → SEAM
    assert (32 + 19) % P == 14 and 14 in NQR_14
    assert (18 + 5) % P == 23 and 23 in TESLA_ORB

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 136: The 246-624-462 Cycle Sum = 36 × 37")
    print("=" * 62)
    print()
    print("  Forward cycle (SEED_ORB): 246 → 624 → 462")
    print("  Reverse cycle (NQR_5):    642 → 426 → 264")
    print()
    print(f"  Sum of either cycle = 1332 = 36 × 37 = φ(37) × p")
    print(f"  All elements: DR=3, digit sum=12=log₂(26)")
    print()
    print("  mod 36 (dlog-space): 246→30, 624→12=log₂(26), 462→30")
    print("  The center element 624 holds the structural key.")
    print()
    print("  6-digit positional map:")
    print("    1st position pair → SEAM (divisible by 37)")
    print("    2nd position pair → NQR_14 (mod37=14)")
    print("    3rd position pair → TESLA_ORB (mod37=23)")
    print()
    print("  Additive pairing forward+reverse by position:")
    print("    24+13=37≡SEAM, 32+19=51≡14∈NQR_14, 18+5=23∈TESLA_ORB")
    print("  Same residues as the 6-digit concatenation outputs.")


if __name__ == "__main__":
    run_assertions()
    summarise()
