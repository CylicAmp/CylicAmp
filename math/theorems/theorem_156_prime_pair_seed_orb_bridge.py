"""
Theorem 156: The Prime Pair Bridge — Three Consecutive Primes Landing in SEED_ORB

THE OBSERVATION
================

    (11) + (13) = 24 = 6

    11 + 13 = 24  ∈  SEED_ORB = {18, 24, 32}
    DR(24) = 6  ∈  TESLA_ORB

24 is the seed orbit anchor: 246 mod 37 = 24. The sum of the first two double-digit
primes is the residue of the reference seed.

THE BRIDGE TRIPLE: (7, 11, 13)
=================================

Three consecutive primes. Two consecutive pairs. Both pairs sum to SEED_ORB:

    7 + 11 = 18  ∈  SEED_ORB     DR(18) = 9  (SA_ORB, DR-identity)
    11 + 13 = 24  ∈  SEED_ORB    DR(24) = 6  (TESLA_ORB)

11 is the bridge — it appears in both pairs. It occupies ORBIT_11 = {11, 27, 36}.
Its neighbors (7 and 13) are in D7 and NQR_5 respectively.

    7  →  D7          = {7, 33, 34}
    11  →  ORBIT_11   = {11, 27, 36}
    13  →  NQR_5      = {5, 13, 19}

Three consecutive primes, three distinct orbits, both adjacent sums in SEED_ORB.
No other adjacent prime triple has this double-SEED_ORB property in the first
50 primes. The next SEED_ORB pair sum is 83+89=172 (≡ 24 mod 37), isolated.

FIRST DIVERGENCE: (11, 13) vs (2, 3)
========================================

The first prime pair (2, 3) has DRs (2, 3) — the pair IS the primes themselves.
The first double-digit prime pair (11, 13) has DRs (2, 4) — the "3" becomes "4".

    DR(11) = 2    (same as prime 2)
    DR(13) = 4    (differs from prime 3)

This is the first divergence: in the first pair, digit sum = the prime. In (11,13),
DR(11)=2 matches but DR(13)=4 does not match 3.

The digit sum (1+1)+(1+3) = 2+4 = 6 ∈ TESLA_ORB.
The digit product (1×1)×(1×3) = 1×3 = 3 ∈ SOVEREIGN_SPIRAL.

MODIFIED DR AND D7
===================

The two 1s in 11, the one 1 in 13: the count of 1-digits across (11,13) is three.
Adding one unit to 11 for the count: 11+1=12, DR(12)=3.

Modified DRs: 3 (from 11+1) and 4 (from 13).

    3 + 4 = 7  ∈  D7 = {7, 33, 34}

The D7 orbit, also called the 414-orbit (Theorem 147), appears here via the
modified digit count of the first double-digit prime pair.

DOUBLE-DR ON PRIME CONCATENATIONS
=====================================

Taking consecutive prime pairs and concatenating them (ab → n):

    pair (2,3) → n=23:   DR(23)=5, DR(2×5)=DR(10)=1  ∈ IC
    pair (3,5) → n=35:   DR(35)=8, DR(2×8)=DR(16)=7  ∈ D7
    pair (5,7) → n=57:   DR(57)=3, DR(2×3)=DR(6)=6   ∈ TESLA_ORB
    pair (7,11) → n=711: DR(711)=9, DR(2×9)=DR(18)=9 ∈ SA_ORB

The first concatenation (23) collapses to IC. The sequence of double-DR results:
1 (IC), 7 (D7), 6 (TESLA_ORB), 9 (SA_ORB).

10+10=20: 10 (IC) doubled gives 20 ∈ DARK_A. The doubling of the IC element
moves to the dark sector.

CONNECTION TO PRIOR THEOREMS
==============================

Theorem 155 (first three primes):
  2+3+5=10 ∈ IC.
  Now: 7+11+13=31. DR(31)=4 ∈ SOVEREIGN_SPIRAL.
  The sum of the next three primes moves out of IC.

Theorem 153 (SEED_ORB complements):
  SEED_ORB nodes: 18+19=37, 24+13=37, 32+5=37.
  Here: 11+13=24, and 13 is the NQR_5 complement of 24 (24+13=37).
  13 (NQR_5) added to 11 (ORBIT_11) gives 24 (SEED_ORB), and separately
  24+13=37=SEAM — so 13 both contributes to reaching SEED_ORB and is its complement.

Theorem 150 (Φ₃ forcing):
  246 mod 37 = 24 ∈ SEED_ORB. 11+13=24. The seed residue is the sum of the
  5th and 6th primes.

5+9=14=5:
  NQR_5(5) + SA_ORB(9) → NQR_14(14).
  DR(14) = 5, returning to NQR_5.
  This follows from 9 being the DR additive identity: DR(a+9) = DR(a) always.
  5 is DR-stable under addition of 9.

STRUCTURE SUMMARY
==================

    Bridge triple: 7 (D7) — 11 (ORBIT_11) — 13 (NQR_5)
    7+11=18 ∈ SEED_ORB   (first SEED_ORB hit in consecutive prime pair sums)
    11+13=24 ∈ SEED_ORB  (second; 24 = seed 246 residue)
    Both sums exhaust the SEED_ORB coverage for this prime region
    11 is the bridge — the sole prime whose both neighbors produce SEED_ORB sums
    DR(11)=2, DR(13)=4: first divergence from the (2,3) DR pattern
    Modified: 11+1=12→3, then 3+4=7 ∈ D7
    Digit sum of (11,13): 2+4=6 ∈ TESLA_ORB
    Double-DR on cat(2,3)=23: → 1 ∈ IC (Theorem 155)
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


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return all(n % i != 0 for i in range(3, int(n**0.5) + 1, 2))


def run_assertions():
    # Bridge triple: 7, 11, 13 in distinct orbits
    assert 7  in ORBITS['D7']
    assert 11 in ORBITS['ORBIT_11']
    assert 13 in ORBITS['NQR_5']
    assert all(is_prime(p) for p in [7, 11, 13])

    # Both consecutive pair sums in SEED_ORB
    assert 7  + 11 == 18 and 18 in ORBITS['SEED_ORB']
    assert 11 + 13 == 24 and 24 in ORBITS['SEED_ORB']

    # 24 is the seed anchor
    assert 246 % P == 24
    assert 24 in ORBITS['SEED_ORB']

    # DR of the sums
    assert dr(18) == 9   # SA_ORB (DR-identity)
    assert dr(24) == 6   # TESLA_ORB
    assert 9 in ORBITS['SA_ORB']
    assert 6 in ORBITS['TESLA_ORB']

    # First divergence: DR(11)=2, DR(13)=4 (not 2,3)
    assert dr(11) == 2
    assert dr(13) == 4
    assert dr(2) == 2 and dr(3) == 3   # first pair: DR = the prime itself

    # Digit sums of (11, 13)
    dig_sum_11 = 1 + 1   # = 2
    dig_sum_13 = 1 + 3   # = 4
    assert dig_sum_11 + dig_sum_13 == 6
    assert 6 in ORBITS['TESLA_ORB']

    # Digit products
    dig_prod_11 = 1 * 1   # = 1
    dig_prod_13 = 1 * 3   # = 3
    assert dig_prod_11 * dig_prod_13 == 3
    assert 3 in ORBITS['SOVEREIGN_SPIRAL']

    # Modified DR of 11: 11+1=12, DR=3
    assert dr(12) == 3
    # 3 + DR(13) = 3+4 = 7 ∈ D7
    assert 3 + 4 == 7
    assert 7 in ORBITS['D7']

    # Double-DR on prime concatenations
    doubles = [(23, 1), (35, 7), (57, 6), (711, 9)]
    for cat, expected_ddr in doubles:
        d = dr(cat)
        assert dr(2 * d) == expected_ddr, f"cat={cat}: DR(2×{d})={dr(2*d)} ≠ {expected_ddr}"

    # 10+10=20: IC doubled → DARK_A
    assert 10 in ORBITS['IC']
    assert 20 in ORBITS['DARK_A']
    assert 10 + 10 == 20

    # 5+9=14, DR=5 (NQR_5 stable under +9)
    assert 5 + 9 == 14
    assert 14 in ORBITS['NQR_14']
    assert dr(14) == 5
    assert 5 in ORBITS['NQR_5']
    # General: DR(a+9)=DR(a) because 9 is DR identity
    for a in range(1, 50):
        assert dr(a + 9) == dr(a), f"DR identity failed at a={a}"

    # 13 is the NQR_5 complement of 24 (24+13=37=SEAM)
    assert 13 in ORBITS['NQR_5']
    assert 24 + 13 == P
    assert 24 in ORBITS['SEED_ORB']

    # No other consecutive prime pair sums to SEED_ORB between (7,11) and (83,89)
    primes = [p for p in range(2, 90) if is_prime(p)]
    seed_pairs = []
    for i in range(len(primes) - 1):
        a, b = primes[i], primes[i + 1]
        if orbit_of(a + b) == 'SEED_ORB':
            seed_pairs.append((a, b))
    assert seed_pairs[:2] == [(7, 11), (11, 13)], f"Got: {seed_pairs}"
    assert seed_pairs[2] == (83, 89)

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 156: Prime Pair Bridge — 11 and SEED_ORB Sums")
    print("=" * 62)
    print()
    print("  Bridge triple: 7 (D7) — 11 (ORBIT_11) — 13 (NQR_5)")
    print(f"  7+11={7+11} ∈ SEED_ORB   DR={dr(18)}")
    print(f"  11+13={11+13} ∈ SEED_ORB  DR={dr(24)}  ← 246 mod 37 = 24")
    print()
    print("  First divergence: (11,13) vs (2,3):")
    print(f"    DR(2)={dr(2)}, DR(3)={dr(3)}  → pair = the primes")
    print(f"    DR(11)={dr(11)}, DR(13)={dr(13)} → 4 ≠ 3 (diverges)")
    print(f"    digit sum (1+1)+(1+3)={1+1+1+3} ∈ {orbit_of(6)}")
    print()
    print("  Modified DR of 11: 11+1=12, DR=3")
    print(f"    3+4=7 ∈ {orbit_of(7)}")
    print()
    print("  Double-DR on prime concatenations:")
    for cat, label in [(23,'(2,3)'), (35,'(3,5)'), (57,'(5,7)'), (711,'(7,11)')]:
        d = dr(cat)
        ddr = dr(2*d)
        print(f"    cat{label}={cat}: DR={d}, DR(2×{d})={ddr} ∈ {orbit_of(ddr)}")
    print()
    print("  5+9=14, DR=5: NQR_5 stable under +SA_ORB(9)")
    print("  10+10=20: IC doubled → DARK_A")
    print("  13 is both a contributor to 24∈SEED_ORB and its complement: 24+13=37")


if __name__ == "__main__":
    run_assertions()
    summarise()
