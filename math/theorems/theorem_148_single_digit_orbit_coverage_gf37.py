"""
Theorem 148: Single-Digit Orbit Coverage and the {1,3,5}/{2,4,6}/{7,8,9} Partition in GF(37)

THE COMPLETE ORBIT TABLE
=========================

The map x → 26x (mod 37) partitions (ℤ/37ℤ)× into exactly 12 orbits of size 3.
Since ord₃₇(26) = 3 and |(ℤ/37ℤ)×| = 36 = 12 × 3, this is forced.
Every orbit is a 3-cycle: x → 26x → 10x → x (mod 37).

 #   Name               Cycle            Orbit trace (×26 each step)
──────────────────────────────────────────────────────────────────────
 1   IC                {1,  26, 10}      1→26→10→1
 2   DARK_A            {2,  15, 20}      2→15→20→2
 3   SOVEREIGN_SPIRAL  {3,   4, 30}      3→4→30→3
 4   NQR_5             {5,  19, 13}      5→19→13→5
 5   TESLA_ORB         {6,   8, 23}      6→8→23→6
 6   D7                {7,  34, 33}      7→34→33→7
 7   SA_ORB            {9,  12, 16}      9→12→16→9
 8   ORBIT_11          {11, 27, 36}     11→27→36→11
 9   NQR_14            {14, 31, 29}     14→31→29→14
10   NQR_17            {17, 35, 22}     17→35→22→17
11   SEED_ORB          {18, 24, 32}     18→24→32→18
12   OUTLIER_ORB       {21, 28, 25}     21→28→25→21

SINGLE-DIGIT COVERAGE
======================

The range {1,...,9} covers exactly 7 of 12 orbits.

  Digit → Orbit
  1     → IC
  2     → DARK_A
  3     → SOVEREIGN_SPIRAL
  4     → SOVEREIGN_SPIRAL  ← doubly represented
  5     → NQR_5
  6     → TESLA_ORB
  7     → D7
  8     → TESLA_ORB         ← doubly represented
  9     → SA_ORB

Two orbits appear twice in {1,...,9}:
  SOVEREIGN_SPIRAL via {3, 4}
  TESLA_ORB        via {6, 8}

Five orbits have no single-digit representative:
  ORBIT_11      smallest element = 11
  NQR_14        smallest element = 14
  NQR_17        smallest element = 17
  SEED_ORB      smallest element = 18
  OUTLIER_ORB   smallest element = 21

SEED_ORB — the 137-map orbit of seed 246, {18, 24, 32} — lies entirely outside the
single-digit domain. No element of SEED_ORB is reachable by a single decimal digit.

THE {1,3,5}/{2,4,6}/{7,8,9} PARTITION
=======================================

Partition of {1,...,9} into three symbolic blocks:
  Block A = {1, 3, 5}  (odd digits below 7)
  Block B = {2, 4, 6}  (even digits below 7)
  Block C = {7, 8, 9}  (digits above 6)

These are NOT multiplicative orbits under x → 26x (mod 37).
Each block crosses three distinct orbits — no block is orbit-homogeneous.

  Block A: 1∈IC,   3∈SOVEREIGN_SPIRAL,  5∈NQR_5
  Block B: 2∈DARK_A, 4∈SOVEREIGN_SPIRAL, 6∈TESLA_ORB
  Block C: 7∈D7,   8∈TESLA_ORB,         9∈SA_ORB

The partition is a chosen symbolic structure, not an orbit partition.

BLOCK PRODUCTS MOD 37
======================

  Block A: 1×3×5  =  15        15 mod 37 = 15  ∈ DARK_A
  Block B: 2×4×6  =  48        48 mod 37 = 11  ∈ ORBIT_11
  Block C: 7×8×9  = 504       504 mod 37 = 23  ∈ TESLA_ORB

  Sum: 15 + 48 + 504 = 567     567 mod 37 = 12  ∈ SA_ORB

Residue signature: (15, 11, 23) spanning DARK_A, ORBIT_11, TESLA_ORB.
Total product-sum residue: 12 ∈ SA_ORB = {9, 12, 16}.

The block product of A lands in DARK_A — the orbit of digit 2 (Block B's first element).
The block product of B lands in ORBIT_11 — outside the single-digit domain entirely.
The block product of C lands in TESLA_ORB — the orbit shared by digits 6 and 8.

BRIDGE PRINCIPLE: SPAN L = 18
================================

Span L = 18 ∈ SEED_ORB = {18, 24, 32} (the 137-map orbit of seed 246).
A digit n ∈ {0,...,9} is bridge-valid iff n | 18.

  Divisors of 18: 1, 2, 3, 6, 9, 18
  Valid digits (∩ {0,...,9}): {1, 2, 3, 6, 9}
  Invalid digits: {0, 4, 5, 7, 8}

Orbits of valid digits:
  1 ∈ IC
  2 ∈ DARK_A
  3 ∈ SOVEREIGN_SPIRAL
  6 ∈ TESLA_ORB
  9 ∈ SA_ORB

The bridge-valid set spans 5 distinct orbits. Divisibility by L does not respect
orbit membership:
  3 and 4 share SOVEREIGN_SPIRAL; 3 | 18, 4 ∤ 18
  6 and 8 share TESLA_ORB;        6 | 18, 8 ∤ 18

TRUTH-TYPE STRATIFICATION
===========================

Computational truth   (direct calculation):
  137 ≡ 26 (mod 37); ord₃₇(26) = 3; 567 ≡ 12 (mod 37)

Structural truth      (follows from group theory):
  36 nonzero residues split into exactly 12 cycles of length 3

Invariant truth       (survives re-decomposition):
  Residue 12 is independent of the path taken to reach 567

Relational truth      (requires the orbit dictionary):
  12 ∈ SA_ORB

Classification truth  (requires the span-L rule):
  "bridge-valid" = divides 18

The partition {1,3,5}/{2,4,6}/{7,8,9} is relational truth, not structural truth:
it is imposed, not derived from the 137-map.
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

M = 26  # 137 mod 37


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def compute_orbits():
    """Return the 12 actual orbits under x -> M*x (mod P)."""
    seen = set()
    orbits = []
    for start in range(1, P):
        if start in seen:
            continue
        cycle = []
        x = start
        for _ in range(3):
            cycle.append(x)
            seen.add(x)
            x = (x * M) % P
        assert x == start, f"cycle did not close at {start}"
        orbits.append(frozenset(cycle))
    return orbits


def run_assertions():
    # Multiplier order
    assert pow(M, 3, P) == 1
    assert pow(M, 1, P) == 26
    assert pow(M, 2, P) == 10

    # 12 orbits of size 3
    actual_orbits = compute_orbits()
    assert len(actual_orbits) == 12
    assert all(len(o) == 3 for o in actual_orbits)
    total = set()
    for o in actual_orbits:
        total |= o
    assert total == set(range(1, P))

    # Every named orbit matches an actual orbit
    for name, s in ORBITS.items():
        assert s in actual_orbits, f"{name} = {s} not an actual orbit"

    # Single-digit coverage: 7 of 12 orbits
    single_digit_orbits = set(orbit_of(d) for d in range(1, 10))
    assert len(single_digit_orbits) == 7

    # Doubly represented orbits
    from collections import Counter
    digit_orbit_counts = Counter(orbit_of(d) for d in range(1, 10))
    double = {k for k, v in digit_orbit_counts.items() if v == 2}
    assert double == {'SOVEREIGN_SPIRAL', 'TESLA_ORB'}
    assert orbit_of(3) == orbit_of(4) == 'SOVEREIGN_SPIRAL'
    assert orbit_of(6) == orbit_of(8) == 'TESLA_ORB'

    # Five absent orbits
    absent = set(ORBITS.keys()) - single_digit_orbits
    assert absent == {'ORBIT_11', 'NQR_14', 'NQR_17', 'SEED_ORB', 'OUTLIER_ORB'}
    assert all(min(ORBITS[name]) >= 11 for name in absent)

    # SEED_ORB smallest element
    assert min(ORBITS['SEED_ORB']) == 18

    # Partition {1,3,5}/{2,4,6}/{7,8,9}: no block is orbit-homogeneous
    blocks = [frozenset({1,3,5}), frozenset({2,4,6}), frozenset({7,8,9})]
    for block in blocks:
        block_orbits = {orbit_of(d) for d in block}
        assert len(block_orbits) == 3, f"block {block} expected 3 distinct orbits"

    # Block A orbit members
    assert orbit_of(1) == 'IC'
    assert orbit_of(3) == 'SOVEREIGN_SPIRAL'
    assert orbit_of(5) == 'NQR_5'

    # Block B orbit members
    assert orbit_of(2) == 'DARK_A'
    assert orbit_of(4) == 'SOVEREIGN_SPIRAL'
    assert orbit_of(6) == 'TESLA_ORB'

    # Block C orbit members
    assert orbit_of(7) == 'D7'
    assert orbit_of(8) == 'TESLA_ORB'
    assert orbit_of(9) == 'SA_ORB'

    # Partition blocks are not actual orbits
    for block in blocks:
        assert block not in actual_orbits

    # Block products mod 37
    assert (1*3*5) == 15  and 15 % P == 15 and 15 in ORBITS['DARK_A']
    assert (2*4*6) == 48  and 48 % P == 11 and 11 in ORBITS['ORBIT_11']
    assert (7*8*9) == 504 and 504 % P == 23 and 23 in ORBITS['TESLA_ORB']

    # Sum of block products
    assert 15 + 48 + 504 == 567
    assert 567 % P == 12 and 12 in ORBITS['SA_ORB']

    # Bridge principle: span L=18, valid digits divide 18
    L = 18
    assert L in ORBITS['SEED_ORB']
    valid = {n for n in range(1, 10) if L % n == 0}
    assert valid == {1, 2, 3, 6, 9}
    invalid = set(range(1, 10)) - valid
    assert invalid == {4, 5, 7, 8}

    # Valid digit orbits span 5 distinct orbits
    valid_orbit_set = {orbit_of(n) for n in valid}
    assert valid_orbit_set == {'IC', 'DARK_A', 'SOVEREIGN_SPIRAL', 'TESLA_ORB', 'SA_ORB'}

    # Divisibility does not respect orbit membership
    assert orbit_of(3) == orbit_of(4) == 'SOVEREIGN_SPIRAL'
    assert 18 % 3 == 0 and 18 % 4 != 0
    assert orbit_of(6) == orbit_of(8) == 'TESLA_ORB'
    assert 18 % 6 == 0 and 18 % 8 != 0

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 148: Single-Digit Orbit Coverage in GF(37)")
    print("=" * 62)
    print()
    print("  12 orbits under x → 26x (mod 37):")
    actual_orbits = compute_orbits()
    for name, s in ORBITS.items():
        rep = min(s)
        cycle = []
        x = rep
        for _ in range(3):
            cycle.append(x)
            x = (x * M) % P
        in_single = [e for e in s if 1 <= e <= 9]
        tag = f"  ← digit{'s' if len(in_single)>1 else ''} {sorted(in_single)}" if in_single else ""
        print(f"  {name:<20} {cycle[0]:2d}→{cycle[1]:2d}→{cycle[2]:2d}→…{tag}")
    print()
    print("  Single-digit coverage: 7 of 12 orbits")
    print("  Doubly represented: SOVEREIGN_SPIRAL {3,4}, TESLA_ORB {6,8}")
    print("  Absent (min element > 9): ORBIT_11, NQR_14, NQR_17, SEED_ORB, OUTLIER_ORB")
    print()
    print("  Partition {1,3,5}/{2,4,6}/{7,8,9}: each block crosses 3 orbits")
    print("  Block products mod 37: 15(DARK_A), 11(ORBIT_11), 23(TESLA_ORB)")
    print("  Sum 567 ≡ 12 ∈ SA_ORB")
    print()
    print("  Bridge principle: L=18 ∈ SEED_ORB")
    print("  Valid digits (divide 18): {1,2,3,6,9} → IC,DARK_A,SOVEREIGN_SPIRAL,TESLA_ORB,SA_ORB")
    print("  Divisibility by 18 does not respect orbit membership.")


if __name__ == "__main__":
    run_assertions()
    summarise()
