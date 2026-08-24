# -*- coding: utf-8 -*-
"""
================================================================================
TWIN PRIME CHAMBER CLASSIFICATION — C3 / C6 / C9
================================================================================

Author: Michael Warren Song (CyclicAmp)

================================================================================
THE TRIPARTITE χ_{-3} STRUCTURE [P]
================================================================================

For every twin prime pair (p, p+2) with p > 3:

    p = 6m − 1  ≡ 2 (mod 3)  →  χ_{-3}(p)   = −1
    p+1 = 6m    ≡ 0 (mod 3)  →  χ_{-3}(p+1) =  0  (the seam)
    p+2 = 6m+1  ≡ 1 (mod 3)  →  χ_{-3}(p+2) = +1

The tripartite structure is exact for all twin primes p > 3:

    −1  |  0  |  +1

The left twin is always in the χ_{-3} = −1 class.
The right twin is always in the χ_{-3} = +1 class.
The center is always on the χ_{-3} = 0 seam.

This is not a Chebyshev-bias claim (statistical). It is an exact modular
theorem: p = 6m−1 ≡ 2 (mod 3), so χ_{-3}(p) = −1 with no exceptions.

Verified: 204 twin prime pairs to 10,000 — 0 violations.

================================================================================
CENTER CLASSIFICATION: C3 / C6 / C9 [P]
================================================================================

The center of every twin prime pair is 6m. Its digital root is determined
entirely by m mod 3:

    m ≡ 0 (mod 3):  6m ≡ 0 (mod 9)  →  DR(6m) = 9  →  C9
    m ≡ 1 (mod 3):  6m ≡ 6 (mod 9)  →  DR(6m) = 6  →  C6
    m ≡ 2 (mod 3):  6m ≡ 3 (mod 9)  →  DR(6m) = 3  →  C3

The center class (C3, C6, or C9) completely determines the digital roots
of both twin primes:

    | m mod 3 | Center | Lower DR | Upper DR |
    |---------|--------|----------|----------|
    |    0    |   C9   |    8     |    1     |
    |    1    |   C6   |    5     |    7     |
    |    2    |   C3   |    2     |    4     |

This is exact: the same m mod 3 that determines the χ_{-3} class of the
twin prime DRs (proved in twin_prime_rh_qr_gf37.py) also determines the
digital root of the center.

================================================================================
GF(37) NAMED SET STRUCTURE BY CENTER CLASS [V]
================================================================================

Upper twin DR and named set by class:

    C9 case (m≡0): upper DR = 1 ∈ IC  (Inner Core, 137-map identity orbit)
    C6 case (m≡1): upper DR = 7 ∈ QR  (not in a named set)
    C3 case (m≡2): upper DR = 4 ∈ SA  (Sovereign Anchor, LOCKED)

Center mod 37 examples:

    (17,19):  m=3, m≡0 → C9.  Center 18 mod 37 = 18 ∈ SEED.
    (11,13):  m=2, m≡2 → C3.  Center 12 mod 37 = 12 ∈ ST.
    (29,31):  m=5, m≡2 → C3.  Center 30 mod 37 = 30 ∈ SA∩ST (double-sovereign).

C3 centers (m≡2, center DR=3) naturally land in ST when they are ST elements,
since ST = {n ∈ GF(37)* : n mod 9 = 3} (the monochromatic DR=3 named set).
C3 center DR and ST definition share the same modular condition (≡3 mod 9).

================================================================================
CLEAN MATHEMATICAL OBJECT: mod-3 × mod-9 INTERACTION [P]
================================================================================

The center of every twin prime pair sits on the χ_{-3} = 0 seam. The DR of
that center classifies which subcase the pair belongs to:

    DR(center = 6m) = 3, 6, or 9  (only these three values — since 6m is
    always divisible by 6, DR(6m) ∈ {3,6,9} for all m ≥ 1)

These are exactly the DR values excluded from twin prime DRs (no prime p > 3
has DR(p) ∈ {3,6,9}). So:

    Twin prime walls:  DR ∉ {3,6,9}
    Twin prime center: DR ∈ {3,6,9}

The center and its walls are DR-disjoint. This is the interaction of the
mod-3 character seam with the mod-9 digital-root dynamics.

EPISTEMIC STATUS:
  [P] χ_{-3}(p) = −1, χ_{-3}(p+1) = 0, χ_{-3}(p+2) = +1 for all twin p>3 — proved.
  [P] DR(6m) ∈ {3,6,9} for all m ≥ 1 — proved (6m always divisible by 3).
  [P] Center class C3/C6/C9 determined by m mod 3 — proved by congruence.
  [P] Center DR and wall DRs are DR-disjoint — proved (walls DR ∉ {3,6,9}).
  [V] Upper twin DR ∈ {IC, QR, SA} by class — exact.
  [V] 204 twin pairs to 10,000: χ_{-3} pattern −1|0|+1, 0 violations — verified.
  [V] (17,19) → C9, center 18 ∈ SEED — exact.
  [V] (11,13) → C3, center 12 ∈ ST — exact.
  [V] (29,31) → C3, center 30 ∈ SA∩ST — exact.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
SEED    = {18, 24, 32}
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
IC      = {1, 10, 26}
NEG_H   = {11, 27, 36}
CASCADE = {8, 13, 24}


def dr(n):
    n = abs(n)
    if n == 0: return 9
    r = n % 9
    return 9 if r == 0 else r


def sieve(n):
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, n+1, i):
                is_p[j] = False
    return [i for i in range(2, n+1) if is_p[i]]


def run():
    print("=" * 70)
    print("TWIN PRIME CHAMBER CLASSIFICATION — C3 / C6 / C9")
    print("=" * 70)

    QR  = {pow(x, 2, P) for x in range(1, P)}

    # Tripartite chi_{-3} structure
    print(f"\nTRIPARTITE χ_{{-3}} STRUCTURE:")
    primes = set(sieve(10000))
    twins = [(p, p+2) for p in range(5, 9999, 2) if p in primes and p+2 in primes]
    for p, q in twins:
        assert p % 3 == 2
        assert (p+1) % 3 == 0
        assert q % 3 == 1
    print(f"  χ_{{-3}} pattern −1|0|+1 verified on {len(twins)} twin pairs to 10,000  check")
    print(f"  Left wall always χ_{{-3}} = −1 (exact modular theorem, not statistical)  check")

    # C3/C6/C9 classification
    print(f"\nCENTER CLASSIFICATION C3/C6/C9:")
    center_class = {0: 9, 1: 6, 2: 3}
    lower_dr     = {0: 8, 1: 5, 2: 2}
    upper_dr     = {0: 1, 1: 7, 2: 4}

    for m3 in [0, 1, 2]:
        m_rep = {0: 3, 1: 1, 2: 2}[m3]
        p = 6*m_rep - 1
        q = 6*m_rep + 1
        center = 6*m_rep
        assert dr(center) == center_class[m3]
        assert dr(p) == lower_dr[m3]
        assert dr(q) == upper_dr[m3]
        print(f"  m≡{m3}: ({p},{q}) center={center} → C{center_class[m3]} | lower DR={lower_dr[m3]} | upper DR={upper_dr[m3]}  check")

    # Verify on ALL twin pairs
    for p, q in twins:
        m = (p + 1) // 6
        m3 = m % 3
        center = p + 1
        assert dr(center) == center_class[m3]
        assert dr(p) == lower_dr[m3]
        assert dr(q) == upper_dr[m3]
    print(f"  Verified on all {len(twins)} pairs  check")

    # Upper twin DR named set
    print(f"\nUPPER TWIN DR → NAMED SET BY CLASS:")
    assert 1 in IC
    assert 4 in SA
    assert 7 in QR
    print(f"  C9 (m≡0): upper DR=1 ∈ IC  check")
    print(f"  C6 (m≡1): upper DR=7 ∈ QR (not named)  check")
    print(f"  C3 (m≡2): upper DR=4 ∈ SA  check")

    # GF(37) examples
    print(f"\nGF(37) CENTER EXAMPLES:")
    examples = [((17,19),3), ((11,13),2), ((29,31),5)]
    for (p,q), m in examples:
        center = p+1
        m3 = m % 3
        cr = center % P
        cats = []
        if cr in SEED:    cats.append('SEED')
        if cr in SA:      cats.append('SA')
        if cr in ST:      cats.append('ST')
        if cr in IC:      cats.append('IC')
        if cr in NEG_H:   cats.append('NEG_H')
        if cr in CASCADE: cats.append('CASCADE')
        lab = ','.join(cats) if cats else '-'
        print(f"  ({p},{q}) m={m} m≡{m3} → C{center_class[m3]}: center {center} mod37={cr} [{lab}]  check")

    assert (18 % P) in SEED
    assert (12 % P) in ST
    assert (30 % P) in SA and (30 % P) in ST

    # DR disjointness
    print(f"\nDR DISJOINTNESS (center vs walls):")
    print(f"  Twin prime walls: DR ∉ {{3,6,9}}  (primes >3 not divisible by 3)")
    print(f"  Twin prime centers: DR ∈ {{3,6,9}}  (6m always divisible by 3)")
    print(f"  Center and walls are DR-disjoint  check")
    for p, q in twins:
        assert dr(p) not in {3, 6, 9}
        assert dr(q) not in {3, 6, 9}
        assert dr(p+1) in {3, 6, 9}
    print(f"  Verified on all {len(twins)} pairs  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
