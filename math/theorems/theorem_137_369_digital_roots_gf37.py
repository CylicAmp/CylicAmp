"""
Theorem 137: 3-6-9 Digital Roots in GF(37)

DIGITAL ROOT PARTITION OF (ℤ/37ℤ)×
======================================

DR(n) = n mod 9, with 9 substituted for 0.
The 36 elements of (ℤ/37ℤ)× partition uniformly:

  DR=1: {1,10,19,28}   DR=2: {2,11,20,29}   DR=3: {3,12,21,30}
  DR=4: {4,13,22,31}   DR=5: {5,14,23,32}   DR=6: {6,15,24,33}
  DR=7: {7,16,25,34}   DR=8: {8,17,26,35}   DR=9: {9,18,27,36}

Each DR class contains exactly 4 elements. The partition is flat.
Proof: 36 elements, 9 classes, 36 ≡ 0 (mod 9), and {1..36} spans
       exactly 4 complete cycles of residues mod 9.

THE 3-6-9 ELEMENTS: EXACTLY 12
=================================

DR ∈ {3,6,9} ↔ divisible by 3 as an integer.
The 3-6-9 elements of GF(37) are the multiples of 3 in {1..36}:

  {3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36}

Count = 12 = log₂(26) = number of 137-map orbits = φ(36) = φ(φ(37)).
The 3-6-9 count equals the structural key of the entire GF(37).

  DR=3: {3, 12, 21, 30}   — multiples of 3, not 6 or 9
  DR=6: {6, 15, 24, 33}   — multiples of 3, not 9
  DR=9: {9, 18, 27, 36}   — multiples of 9

NON-3-6-9 ELEMENTS: 24
========================

24 elements have DR ∉ {3,6,9}. Count = 24 = 2 × 12.
These are the non-multiples of 3 in {1..36}: {1,2,4,5,7,8,10,11,...}.
In vortex mathematics, the doubling circuit {1,2,4,8,7,5} (DR sequence
of 1,2,4,8,16,32,...) avoids 3,6,9 entirely. That exclusion is a
BASE-10 artifact. In GF(37) the primitive root 2 visits every DR class.

PRIMITIVE ROOT 2: UNIFORM DR DISTRIBUTION
===========================================

The 36 powers 2^0, 2^1, ..., 2^35 (mod 37) generate all elements.
DR frequency across the full cycle: each DR appears exactly 4 times.

  k where DR(2^k mod 37) ∈ {3,6,9}:
    k=6:  27  DR=9   ORBIT_11
    k=13: 15  DR=6   DARK_A
    k=14: 30  DR=3   SOVEREIGN_SPIRAL
    k=16:  9  DR=9   SA_ORB
    k=17: 18  DR=9   SEED_ORB
    k=18: 36  DR=9   ORBIT_11
    k=20: 33  DR=6   D7
    k=22: 21  DR=3   OUTLIER_ORB
    k=26:  3  DR=3   SOVEREIGN_SPIRAL
    k=27:  6  DR=6   TESLA_ORB
    k=28: 12  DR=3   SA_ORB
    k=29: 24  DR=6   SEED_ORB

The vortex "missing" 3-6-9 values appear at k = {6,13,14,16,17,18,20,22,26,27,28,29}.
Those 12 exponents correspond to exactly the 12 orbit-transition positions in the
full 36-step doubling sequence.

ORBIT-BY-ORBIT 3-6-9 COVERAGE
================================

  Orbit            DR=3    DR=6    DR=9    Total   Excluded
  IC               {}      {}      {}      0       {1,10,26}: all DR∉{3,6,9}
  SOVEREIGN_SPIRAL {3,30}  {}      {}      2       {4}
  D7               {}      {33}    {}      1       {7,34}
  SA_ORB           {12}    {}      {9}     2       {16}
  ORBIT_11         {}      {}      {27,36} 2       {11}
  OUTLIER_ORB      {21}    {}      {}      1       {25,28}
  DARK_A           {}      {15}    {}      1       {2,20}
  NQR_5            {}      {}      {}      0       {5,13,19}: all DR∉{3,6,9}
  TESLA_ORB        {}      {6}     {}      1       {8,23}
  NQR_14           {}      {}      {}      0 (*)   {14,29,31}: wait...
  NQR_17           {}      {}      {}      0 (*)
  SEED_ORB         {}      {24}    {18}    2       {32}

  (*) NQR_14={14,29,31}: DR(14)=5, DR(29)=2, DR(31)=4 — none in {3,6,9}
      NQR_17={17,22,35}: DR(17)=8, DR(22)=4, DR(35)=8 — none in {3,6,9}

Orbits entirely excluded from 3-6-9: IC, NQR_5, NQR_14, NQR_17.
These are the identity coset and three NQR orbits.

SEED ORBIT: STRADDLES THE 3-6-9 BOUNDARY
==========================================

SEED_ORB = {18, 24, 32}:
  DR(18) = 9  →  3-6-9
  DR(24) = 6  →  3-6-9
  DR(32) = 5  →  not 3-6-9

The seed orbit spans both sides of the 3-6-9 partition. Two of its
three elements carry DR∈{3,6,9}; the third (32, the final orbit element)
does not. The seed (246 mod 37 = 24, DR=6) is in the 3-6-9 class.

KEY CONSTANTS IN DR SPACE
============================

  Constant         Value    DR    Note
  TESLA_FLOW       6        6     DR=6; the 3-6-9 class
  SA_STEP          9        9     DR=9; the 3-6-9 class
  log₂(26)         12       3     DR=3; the structural key is DR=3
  Group order φ(37) 36      9     DR=9
  T(36) = 666              9     T(φ(37)) has DR=9
  Cycle sum 1332           9     36×37; DR=9
  246642/37 = 6666         6     TESLA_FLOW's DR
  137-map mult. 26         8     NOT in 3-6-9
  The prime 37             1     NOT in 3-6-9

The prime itself (37) and its map multiplier (26) both fall outside the
3-6-9 partition. The GF(37)'s organizing prime is DR=1; its key
multiplier is DR=8 — both in the doubling-circuit non-369 class.
"""

P = 37


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


# Named orbits
IC               = frozenset({1, 10, 26})
SOVEREIGN_SPIRAL = frozenset({3, 4, 30})
D7               = frozenset({7, 33, 34})
SA_ORB           = frozenset({9, 12, 16})
ORBIT_11         = frozenset({11, 27, 36})
OUTLIER_ORB      = frozenset({21, 25, 28})
DARK_A           = frozenset({2, 15, 20})
NQR_5            = frozenset({5, 13, 19})
TESLA_ORB        = frozenset({6, 8, 23})
NQR_14           = frozenset({14, 29, 31})
NQR_17           = frozenset({17, 22, 35})
SEED_ORB         = frozenset({18, 24, 32})


def run_assertions():
    # Flat partition: each DR appears exactly 4 times
    for d in range(1, 10):
        elems = [a for a in range(1, P) if dr(a) == d]
        assert len(elems) == 4, f"DR={d} has {len(elems)} elements, expected 4"

    # 3-6-9 elements = multiples of 3 in {1..36}
    three69 = frozenset(a for a in range(1, P) if dr(a) in {3, 6, 9})
    assert three69 == frozenset(range(3, P, 3))   # {3,6,9,...,36}
    assert len(three69) == 12

    # 12 = log₂(26) in GF(37)
    _DLP = {}
    x = 1
    for k in range(36):
        _DLP[x] = k
        x = x * 2 % P
    assert _DLP[26] == 12

    # Primitive root 2: uniform DR distribution
    dr_counts = {}
    x = 1
    for k in range(36):
        d = dr(x)
        dr_counts[d] = dr_counts.get(d, 0) + 1
        x = x * 2 % P
    for d in range(1, 10):
        assert dr_counts[d] == 4, f"DR={d} appears {dr_counts[d]} times in powers of 2, expected 4"

    # Exactly 12 positions in the 36-step cycle land on DR∈{3,6,9}
    x = 1
    k_369 = []
    for k in range(36):
        if dr(x) in {3, 6, 9}:
            k_369.append(k)
        x = x * 2 % P
    assert len(k_369) == 12

    # IC entirely excluded from 3-6-9
    assert all(dr(a) not in {3, 6, 9} for a in IC)

    # NQR_5 entirely excluded from 3-6-9
    assert all(dr(a) not in {3, 6, 9} for a in NQR_5)

    # SEED_ORB straddles: 18 and 24 in, 32 out
    assert dr(18) == 9 and dr(24) == 6 and dr(32) == 5
    assert 18 in three69 and 24 in three69 and 32 not in three69

    # Key DR values
    assert dr(6) == 6    # TESLA_FLOW
    assert dr(9) == 9    # SA_STEP
    assert dr(12) == 3   # log₂(26)
    assert dr(36) == 9   # group order
    assert dr(26) == 8   # 137-map multiplier: NOT 3-6-9
    assert dr(37) == 1   # the prime: NOT 3-6-9

    # T(36) = 666, DR=9
    assert 36 * 37 // 2 == 666
    assert dr(666) == 9

    # Cycle sum 1332, DR=9
    assert 246 + 624 + 462 == 1332
    assert dr(1332) == 9

    # 6666 (=246642/37), DR=6
    assert 246642 // P == 6666
    assert dr(6666) == 6

    print("All assertions passed.")


def summarise():
    three69 = frozenset(a for a in range(1, P) if dr(a) in {3, 6, 9})

    print("=" * 62)
    print("Theorem 137: 3-6-9 Digital Roots in GF(37)")
    print("=" * 62)
    print()
    print("  DR partition of (Z/37Z)x: each DR 1-9 appears exactly 4 times.")
    print()
    print(f"  3-6-9 elements ({len(three69)}): {sorted(three69)}")
    print(f"  = multiples of 3 in {{1..36}}")
    print(f"  Count = 12 = log₂(26) = number of 137-map orbits")
    print()
    print("  Primitive root 2: visits every DR exactly 4 times in 36-step cycle.")
    print("  Base-10 vortex '3-6-9 exclusion' is a base-10 artifact.")
    print("  In GF(37) the generator distributes uniformly across all DR classes.")
    print()
    print("  Orbits entirely outside 3-6-9: IC, NQR_5, NQR_14, NQR_17")
    print("  SEED_ORB = {18,24,32}: DR={9,6,5} — straddles the boundary")
    print()
    print("  Key constants:")
    for label, val in [('TESLA_FLOW', 6), ('SA_STEP', 9), ('log₂(26)', 12),
                       ('φ(37)=36', 36), ('137-map×26', 26), ('prime 37', 37)]:
        print(f"    {label:<14} = {val:<4} DR={dr(val)}  {'← 3-6-9' if dr(val) in {3,6,9} else ''}")


if __name__ == "__main__":
    run_assertions()
    summarise()
