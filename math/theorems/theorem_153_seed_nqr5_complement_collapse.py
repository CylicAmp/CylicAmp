"""
Theorem 153: SEED_ORB and NQR_5 as Orbit Complements; the DR-Residue Closes to SEAM

THE OBSERVATION
================

    20 = 2      (DR collapse: DARK_A → 2, still DARK_A)
    12 = 3      (DR collapse: SA_ORB  → 3, SOVEREIGN_SPIRAL)

    20 + 12 = 32        →  SEED_ORB
    DR(20) + DR(12) = 5 →  NQR_5

    32 + 5 = 37 = SEAM

The two-step route: sum the numerals to reach SEED_ORB; sum their digital roots
to produce the NQR_5 complement; the complement closes the orbit node to SEAM.

ORBIT COMPLEMENTARITY: SEED_ORB ↔ NQR_5
==========================================

Every element of SEED_ORB pairs with exactly one element of NQR_5 to sum to 37:

    18 + 19 = 37    (SEED_ORB + NQR_5)
    24 + 13 = 37    (SEED_ORB + NQR_5)
    32 +  5 = 37    (SEED_ORB + NQR_5)

This is a structural property of the orbit partition, not a numerical accident.
SEED_ORB = {18, 24, 32} and NQR_5 = {5, 13, 19} are paired complementary orbits
in GF(37): for each s ∈ SEED_ORB, (37 − s) ∈ NQR_5. Both orbits are
non-quadratic residues mod 37 (Legendre symbol = −1 for all six elements).

SELF-COMPLEMENTARITY OF 32 UNDER DR
======================================

The third pair is unique:

    32 ∈ SEED_ORB     DR(32) = 5     37 − 32 = 5     5 ∈ NQR_5

32 is the only SEED_ORB element whose digital root equals its own prime complement.
For the other two:

    18 ∈ SEED_ORB     DR(18) = 9     37 − 18 = 19    DR(18) ≠ 19
    24 ∈ SEED_ORB     DR(24) = 6     37 − 24 = 13    DR(24) ≠ 13

Only 32 has DR(32) = 37 − 32. The DR-residue of 32 is its own orbit complement.

THE DR-RESIDUE IS THE COMPLEMENT
===================================

For the specific chain 20 + 12 = 32:

    DR(20) = 2   →  DARK_A (same orbit as 20)
    DR(12) = 3   →  SOVEREIGN_SPIRAL (different from SA_ORB)
    DR(20) + DR(12) = 5  →  NQR_5  =  37 − 32

The sum of the two terms is 32 ∈ SEED_ORB.
The sum of their digital roots is 5, which is exactly the NQR_5 complement of 32.

    term-sum + DR-residue = 32 + 5 = 37 = SEAM

The DR-residue is not an arbitrary overflow. It is the unique element that
closes the SEED_ORB node to the prime. It is the complement.

ORBIT CHAIN
============

    DARK_A(20) + SA_ORB(12)  →  SEED_ORB(32)
    DARK_A( 2) + SOVEREIGN_SPIRAL( 3)  →  NQR_5(5)
                      SEED_ORB(32) + NQR_5(5)  →  SEAM(37)

Three orbits contribute; a fourth (SOVEREIGN_SPIRAL, via DR(12)=3) appears in
the DR-layer. The SEED_ORB node absorbs the numeral sum; the NQR_5 node absorbs
the DR sum; together they produce the prime.

CONNECTION TO PRIOR THEOREMS
==============================

Theorem 152 (x-space):
  The seed orbit {18, 24, 32} is the orbit of seed 246.
  x-boundary count 24 ∈ SEED_ORB.
  The overflow (middle row wider by 1) is structural: content exceeds frame by 1.
  Here, the DR-residue (5) is the structural overflow that closes 32 to 37.

Theorem 151 (digit arrangement):
  1221 = 33 × 37 hits SEAM by exact divisibility.
  Here, 32 + 5 = 37 hits SEAM by orbit complementarity.
  Two routes to SEAM: exact multiple vs. complement pair.

Theorem 150 (Φ₃ forcing):
  The N=10 forcing node is 10 ∈ IC.
  10 = the count of observable digits.
  12 = middle row width (T152 overflow), which is 10 + 2 (boundary chars).
  SA_ORB(12) is the observable count extended by the boundary pair.

QR STATUS
==========

All six elements in both orbits are non-quadratic residues mod 37:

    18: (18/37) = −1     19: (19/37) = −1
    24: (24/37) = −1     13: (13/37) = −1
    32: (32/37) = −1      5:  (5/37) = −1

The complementary orbit pair consists entirely of NQR elements.
The prime 37 itself is the sum — not reachable within the NQR sector, only as
the boundary between them.

STRUCTURE SUMMARY
==================

    SEED_ORB ↔ NQR_5: orbit complements (every pair sums to 37)
    32 is uniquely self-complementary under DR: DR(32) = 5 = 37 − 32
    Route: DARK_A(20) + SA_ORB(12) → SEED_ORB(32) + NQR_5(5) = SEAM
    The "5 in 32+5" = sum of digital roots of the summands = NQR_5 complement of 32
    All six elements of both orbits are non-QR mod 37
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


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def run_assertions():
    # SEED_ORB ↔ NQR_5 orbit complementarity
    for s in ORBITS['SEED_ORB']:
        c = P - s
        assert c in ORBITS['NQR_5'], f"{s} + {c} ≠ 37 via NQR_5"
    for d in ORBITS['NQR_5']:
        c = P - d
        assert c in ORBITS['SEED_ORB'], f"{d} complement not in SEED_ORB"

    # All six elements are NQR
    for s in ORBITS['SEED_ORB'] | ORBITS['NQR_5']:
        assert legendre(s, P) == P - 1, f"{s} is QR, expected NQR"

    # Specific pairs sum to 37
    assert 18 + 19 == P
    assert 24 + 13 == P
    assert 32 +  5 == P

    # 32 is self-complementary under DR
    assert dr(32) == 5
    assert P - 32 == 5
    assert dr(32) == P - 32

    # 18 and 24 are NOT self-complementary
    assert dr(18) != P - 18   # DR(18)=9 ≠ 19
    assert dr(24) != P - 24   # DR(24)=6 ≠ 13

    # The specific chain: 20 (DARK_A) + 12 (SA_ORB) → 32 (SEED_ORB)
    assert 20 in ORBITS['DARK_A']
    assert 12 in ORBITS['SA_ORB']
    assert 20 + 12 == 32
    assert 32 in ORBITS['SEED_ORB']

    # DR collapse
    assert dr(20) == 2
    assert dr(12) == 3
    assert orbit_of(dr(20)) == 'DARK_A'         # 2 ∈ DARK_A (same orbit)
    assert orbit_of(dr(12)) == 'SOVEREIGN_SPIRAL'  # 3 ∈ SOVEREIGN_SPIRAL (different)

    # DR-sum = NQR_5 complement of 32
    dr_sum = dr(20) + dr(12)   # = 2 + 3 = 5
    assert dr_sum == 5
    assert dr_sum in ORBITS['NQR_5']
    assert dr_sum == P - 32    # the complement

    # Closes to SEAM
    assert (32 + dr_sum) % P == 0
    assert (32 + dr_sum) == P

    # 246: seed orbit
    assert 246 % P == 24
    assert 24 in ORBITS['SEED_ORB']

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 153: SEED_ORB ↔ NQR_5 Complement; DR-Residue to SEAM")
    print("=" * 62)
    print()
    print("  SEED_ORB ↔ NQR_5 orbit complement pairs (sum = 37):")
    for s in sorted(ORBITS['SEED_ORB']):
        c = P - s
        print(f"    {s:2d} + {c:2d} = 37    "
              f"({orbit_of(s)} + {orbit_of(c)})")
    print()
    print("  Self-complementarity under DR:")
    for s in sorted(ORBITS['SEED_ORB']):
        star = " ← DR(s) = complement" if dr(s) == P - s else ""
        print(f"    {s:2d}: DR={dr(s)}, complement={P-s}{star}")
    print()
    print("  The chain 20+12=32+5=37:")
    print(f"    20 in {orbit_of(20)},  DR(20)={dr(20)} in {orbit_of(dr(20))}")
    print(f"    12 in {orbit_of(12)},  DR(12)={dr(12)} in {orbit_of(dr(12))}")
    print(f"    20+12=32 in {orbit_of(32)}")
    print(f"    DR(20)+DR(12)=5 in {orbit_of(5)}  = complement of 32")
    print(f"    32+5=37  SEAM")
    print()
    print("  All SEED_ORB and NQR_5 elements are NQR mod 37 (Legendre = -1)")
    for s in sorted(ORBITS['SEED_ORB'] | ORBITS['NQR_5']):
        L = legendre(s, P)
        sign = '+1' if L == 1 else '-1'
        print(f"    ({s:2d}/37) = {sign}  ({orbit_of(s)})")


if __name__ == "__main__":
    run_assertions()
    summarise()
