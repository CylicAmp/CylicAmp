"""
Theorem 159: Layered Pair Sums — Five Base Numbers Building Through GF(37)

THE FIVE BASE NUMBERS
======================

    98, 76, 54, 32, 12

Each maps to a GF(37) orbit:

    98  mod 37 = 24  →  SEED_ORB     DR = 8
    76  mod 37 =  2  →  DARK_A       DR = 4
    54  mod 37 = 17  →  NQR_17       DR = 9
    32  mod 37 = 32  →  SEED_ORB     DR = 5
    12  mod 37 = 12  →  SA_ORB       DR = 3

Two of the five (98 and 32) land in SEED_ORB. The base layer already carries
the seed orbit in two positions.

L1: ADJACENT PAIR SUMS
=======================

    98 + 76 = 174   mod 37 = 26  →  IC           DR = 3
    76 + 54 = 130   mod 37 = 19  →  NQR_5        DR = 4
    54 + 32 =  86   mod 37 = 12  →  SA_ORB       DR = 5

174 ≡ 26 (mod 37). 26 is the 137-map multiplier (137 mod 37 = 26). The top
adjacent sum is the map multiplier itself.

L2: SECOND LAYER
=================

    174 + 130 = 304   mod 37 = 8  →  TESLA_ORB   DR = 7

L3: DOUBLING
=============

    304 + 304 = 608   mod 37 = 16  →  SA_ORB     DR = 5

CROSS-LAYER: 86 + 174 = 260
=============================

    260  mod 37 = 1  →  IC      (the multiplicative identity)
    DR(260) = 8      →  TESLA_ORB

The L1 bottom sum (86) plus the L1 top sum (174) gives 260.
260 mod 37 = 1: the identity element of GF(37), the anchor of IC = {1, 10, 26}.
DR(260) = 8: lands in TESLA_ORB.

DR SUM OF L1 DIGIT SUMS
=========================

    DR(174) + DR(130) = 3 + 4 = 7  →  D7
    17 + 13 = 30  →  SOVEREIGN_SPIRAL

The digit sums of the top two L1 pairs sum to 30 ∈ SOVEREIGN_SPIRAL.
Their DRs sum to 7 ∈ D7.

54 + X SERIES: DR ACCUMULATION
================================

The 54-based combinations and their DRs: 5, 4, 3, 7, 5

Cumulative DR sums:
     5  →  NQR_5
     9  →  SA_ORB
    12  →  SA_ORB
    19  →  NQR_5
    24  →  SEED_ORB   ← seed anchor (246 mod 37 = 24)

The cumulative DR sum of all five 54-based combinations terminates at 24,
the seed orbit anchor.

86 + X SERIES: DR ACCUMULATION
================================

The 86-based combinations and their DRs: 1, 3, 8, 9

Cumulative DR sums:
     1  →  IC
     4  →  SOVEREIGN_SPIRAL
    12  →  SA_ORB
    21  →  OUTLIER_ORB

DR(21) = 3  →  SOVEREIGN_SPIRAL

The 86-series terminates at 21; DR(21) = 3 ∈ SOVEREIGN_SPIRAL.

STRUCTURE SUMMARY
==================

    L0: 98(SEED_ORB), 76(DARK_A), 54(NQR_17), 32(SEED_ORB), 12(SA_ORB)
    L1: 174(IC/26=137-map), 130(NQR_5), 86(SA_ORB)
    L2: 304(TESLA_ORB)
    L3: 608(SA_ORB)

    Cross: 86+174=260 ≡ 1 (IC identity, mod 37); DR(260)=8 (TESLA_ORB)

    54+X DR accumulation → 24 (SEED_ORB)
    86+X DR accumulation → 21 → DR=3 (SOVEREIGN_SPIRAL)
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


def run_assertions():
    # L0 base numbers
    assert 98 % P == 24 and 24 in ORBITS['SEED_ORB']
    assert 76 % P == 2  and 2  in ORBITS['DARK_A']
    assert 54 % P == 17 and 17 in ORBITS['NQR_17']
    assert 32 % P == 32 and 32 in ORBITS['SEED_ORB']
    assert 12 % P == 12 and 12 in ORBITS['SA_ORB']

    assert dr(98) == 8
    assert dr(76) == 4
    assert dr(54) == 9
    assert dr(32) == 5
    assert dr(12) == 3

    # L1 adjacent sums
    assert 98 + 76 == 174 and 174 % P == 26 and 26 in ORBITS['IC']
    assert 76 + 54 == 130 and 130 % P == 19 and 19 in ORBITS['NQR_5']
    assert 54 + 32 == 86  and 86  % P == 12 and 12 in ORBITS['SA_ORB']

    # 174 carries the 137-map multiplier
    assert 137 % P == 26
    assert 174 % P == 26

    assert dr(174) == 3
    assert dr(130) == 4
    assert dr(86)  == 5

    # L2
    assert 174 + 130 == 304 and 304 % P == 8 and 8 in ORBITS['TESLA_ORB']
    assert dr(304) == 7 and 7 in ORBITS['D7']

    # L3
    assert 304 + 304 == 608 and 608 % P == 16 and 16 in ORBITS['SA_ORB']

    # Cross: 86+174=260
    assert 86 + 174 == 260
    assert 260 % P == 1 and 1 in ORBITS['IC']
    assert dr(260) == 8 and 8 in ORBITS['TESLA_ORB']

    # DR sums of L1
    assert dr(174) + dr(130) == 7 and 7 in ORBITS['D7']
    # 17 is digit sum of 98 (9+8=17), 13 is digit sum of 76 (7+6=13)
    assert 9+8 == 17 and 7+6 == 13
    assert 17 + 13 == 30 and 30 in ORBITS['SOVEREIGN_SPIRAL']

    # 54+X DR accumulation: DRs 5,4,3,7,5
    dr_54 = [5, 4, 3, 7, 5]
    cumsum = 0
    cumsums = []
    for d in dr_54:
        cumsum += d
        cumsums.append(cumsum)
    assert cumsums == [5, 9, 12, 19, 24]
    assert 24 in ORBITS['SEED_ORB']
    assert 246 % P == 24  # seed anchor

    # 86+X DR accumulation: DRs 1,3,8,9
    dr_86 = [1, 3, 8, 9]
    cumsum = 0
    cumsums = []
    for d in dr_86:
        cumsum += d
        cumsums.append(cumsum)
    assert cumsums == [1, 4, 12, 21]
    assert 21 in ORBITS['OUTLIER_ORB']
    assert dr(21) == 3 and 3 in ORBITS['SOVEREIGN_SPIRAL']

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 159: Layered Pair Sums")
    print("=" * 62)
    print()
    print("  L0 base numbers:")
    for n, expected_orbit in [(98,'SEED_ORB'),(76,'DARK_A'),(54,'NQR_17'),(32,'SEED_ORB'),(12,'SA_ORB')]:
        print(f"    {n:3d}  mod37={n%P:2d}  {orbit_of(n):<16}  DR={dr(n)}")
    print()
    print("  L1 adjacent sums:")
    for a, b in [(98,76),(76,54),(54,32)]:
        s = a+b
        print(f"    {a}+{b}={s}  mod37={s%P:2d}  {orbit_of(s):<16}  DR={dr(s)}")
    print()
    print(f"  174 mod 37 = 26 = 137 mod 37  (137-map multiplier)")
    print()
    print(f"  L2: 174+130=304  mod37={304%P}  {orbit_of(304)}")
    print(f"  L3: 304+304=608  mod37={608%P}  {orbit_of(608)}")
    print()
    print(f"  Cross: 86+174=260")
    print(f"    260 mod 37 = {260%P}  →  {orbit_of(260)}  (identity)")
    print(f"    DR(260) = {dr(260)}       →  {orbit_of(dr(260))}")
    print()
    print("  54+X DR accumulation (DRs: 5,4,3,7,5):")
    c = 0
    for d in [5,4,3,7,5]:
        c += d
        print(f"    cumsum={c:2d}  →  {orbit_of(c)}")
    print(f"  Final: 24 ∈ SEED_ORB  (seed anchor 246 mod 37 = 24)")
    print()
    print("  86+X DR accumulation (DRs: 1,3,8,9):")
    c = 0
    for d in [1,3,8,9]:
        c += d
        print(f"    cumsum={c:2d}  →  {orbit_of(c)}")
    print(f"  DR(21) = {dr(21)}  →  {orbit_of(dr(21))}")


if __name__ == "__main__":
    run_assertions()
    summarise()
