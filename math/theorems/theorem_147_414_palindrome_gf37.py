"""
Theorem 147: The 414 Palindrome Tower in GF(37)

THE CORE: 414 ≡ 7 (mod 37) ∈ D7
==================================

414 = 4×100 + 1×10 + 4×1
    ≡ 4×26 + 1×10 + 4×1  (mod 37)  [positional weights {26,10,1} = IC]
    = 104 + 10 + 4 = 118 ≡ 118 − 3×37 = 7  (mod 37)
    ∈ D7 = {7, 33, 34}

The digit 1 surrounded by 4s (4−1−4) maps to D7.

THE PALINDROME TOWER (concentric nesting)
==========================================

Layer 0  (center):        1          ≡ 1  ∈ IC
Layer 1:                414          ≡ 7  ∈ D7
Layer 2:              34143          ≡ 29 ∈ NQR_14
Layer 3:            2341432          ≡ 35 ∈ NQR_17
Layer 4:          123414321          ≡ 7  ∈ D7        ← same as 414
Layer 5:        51234143215          ≡ 14 ∈ NQR_14

Each layer wraps the previous by prepending n and appending n
(where n decreases from 4 to 5 going outward: center=1, wrap with 4, then 3, 2, 1, 5).

WHY 414 ≡ 123414321 (mod 37): ord₃₇(10) = 3
==============================================

Since 10³ ≡ 1 (mod 37), positional weights cycle with period 3:
   position 0: 10⁰ ≡  1
   position 1: 10¹ ≡ 10
   position 2: 10² ≡ 26
   position 3: 10³ ≡  1   (restart)
   ...

For 123414321 (9 digits), reading from least-significant:
   pos 0: digit 1 → 1×1  =  1
   pos 1: digit 2 → 2×10 = 20
   pos 2: digit 3 → 3×26 = 78 ≡ 4
   pos 3: digit 4 → 4×1  =  4
   pos 4: digit 1 → 1×10 = 10
   pos 5: digit 4 → 4×26 = 104 ≡ 30
   pos 6: digit 3 → 3×1  =  3
   pos 7: digit 2 → 2×10 = 20
   pos 8: digit 1 → 1×26 = 26
   Sum = 1+20+4+4+10+30+3+20+26 = 118 ≡ 7 (mod 37) ∈ D7

The palindrome structure combined with the period-3 weight cycle forces
123414321 ≡ 414 (mod 37). Both collapse to 7 ∈ D7.

THE HEX RING: 1-4-2-4-3-4
===========================

On the 6-node hexagonal ring, assign:
   Triangle A (the "4-triangle"): vertices show digit 4
   Triangle B (the "1-2-3-triangle"): vertices show 1, 2, 3 in sequence

When interleaved (Star of David): ring = 4, 1, 4, 2, 4, 3   (or cyclic rotation)

All 3-digit windows around the ring:
   Position  Reading  mod 37  Orbit
   0         142      31      NQR_14
   1         424      17      NQR_17
   2         243      21      OUTLIER_ORB
   3         434      27      ORBIT_11
   4         341       8      TESLA_ORB
   5         414       7      D7

The six consecutive windows span six distinct orbits.
No orbit is repeated. The ring encodes one element from each of:
   NQR_14, NQR_17, OUTLIER_ORB, ORBIT_11, TESLA_ORB, D7.

Ring digit sum = 1+4+2+4+3+4 = 18 ∈ SEED_ORB = {18, 24, 32}
The ring sum is the canonical seed value (seed 246 → orbit {18,24,32}).

The 414 reading (nodes: 150°, top, 30°) gives 4−1−4 → 414 ≡ 7 ∈ D7.
This is the "home position": digit 1 at the top, surrounded by 4s.

1234 AND 4321
==============

The two halves of layer 4:

   1234 mod 37 = 13  ∈ NQR_5   (same orbit as 142241 mod 37 = 13, Theorem 146)
   4321 mod 37 = 29  ∈ NQR_14
   1234 + 4321 = 5555
   5555 mod 37 = 5   ∈ NQR_5

   DR(1+2+3+4) = DR(10) = 1
   DR(4+3+2+1) = DR(10) = 1

The sum 5555 ≡ 5 ∈ NQR_5: the same orbit as 1234's residue (13 ∈ NQR_5).
The outer digit "5" in the palindrome tower is ∈ NQR_5 — self-consistent.

OUTER DIGIT 5
=============

The palindrome tower has outer digit 5:
   5 − 1 2 3 4 1 4 3 2 1 − 5

5 ∈ NQR_5 = {5, 13, 19}.
13 ∈ NQR_5 is the residue of 142241 (Theorem 146) and of 1234.
The outer wrapper digit belongs to the same orbit as the ascending half.

DR CHAIN OF THE TOWER
======================

Layer 0: dsum=1    DR=1    1 ∈ IC
Layer 1: dsum=9    DR=9    ← SEAM digit sum
Layer 2: dsum=15   DR=6
Layer 3: dsum=19   DR=1
Layer 4: dsum=21   DR=3    3 ∈ SOVEREIGN_SPIRAL
Layer 5: dsum=31   DR=4    4 ∈ SOVEREIGN_SPIRAL

DR reaches 3 (SOVEREIGN_SPIRAL) at layer 4, the palindrome 123414321.
DR(123414321 digit sum) = DR(21) = 3.  21 ∈ OUTLIER_ORB.  DR(21) = 3.

STRUCTURE SUMMARY
==================

   414        ≡ 7 ∈ D7        (core, DR=9)
   123414321  ≡ 7 ∈ D7        (full palindrome, same residue — forced by ord₃₇(10)=3)
   Ring sum   = 18 ∈ SEED_ORB (sum of 1-4-2-4-3-4)
   1234       ≡ 13 ∈ NQR_5    (ascending half = 142241's orbit)
   5555       ≡ 5  ∈ NQR_5    (sum of halves, outer digit orbit)
   DR(123414321) = 3 ∈ SOVEREIGN_SPIRAL
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
    # Core: 414 ≡ 7 ∈ D7
    assert 414 % P == 7 and 7 in ORBITS['D7']

    # Positional weight formula for 414
    assert (4*26 + 1*10 + 4*1) % P == 7

    # 123414321 ≡ 7 ∈ D7 (same as 414)
    assert 123414321 % P == 7 and 7 in ORBITS['D7']

    # Verify the digit-by-digit computation of 123414321 mod 37
    digits_lsb = [1, 2, 3, 4, 1, 4, 3, 2, 1]  # least-significant first
    weights = [pow(10, i, P) for i in range(9)]
    total = sum(d * w for d, w in zip(digits_lsb, weights)) % P
    assert total == 7

    # Tower layers
    tower = [1, 414, 34143, 2341432, 123414321, 51234143215]
    expected_mods = [1, 7, 29, 35, 7, 14]
    expected_orbits = ['IC', 'D7', 'NQR_14', 'NQR_17', 'D7', 'NQR_14']
    for n, em, eo in zip(tower, expected_mods, expected_orbits):
        assert n % P == em, f"{n}: expected {em}, got {n%P}"
        assert orbit_of(n) == eo, f"{n}: expected {eo}"

    # Hex ring 1-4-2-4-3-4
    ring = [1, 4, 2, 4, 3, 4]
    assert sum(ring) == 18 and 18 in ORBITS['SEED_ORB']
    windows = [(ring[i]*100 + ring[(i+1)%6]*10 + ring[(i+2)%6]) for i in range(6)]
    expected_windows = [142, 424, 243, 434, 341, 414]
    assert windows == expected_windows
    window_orbits = [orbit_of(w) for w in windows]
    expected_worbs = ['NQR_14', 'NQR_17', 'OUTLIER_ORB', 'ORBIT_11', 'TESLA_ORB', 'D7']
    assert window_orbits == expected_worbs
    assert len(set(window_orbits)) == 6  # all six distinct orbits

    # 1234 and 4321
    assert 1234 % P == 13 and 13 in ORBITS['NQR_5']
    assert 4321 % P == 29 and 29 in ORBITS['NQR_14']
    assert (1234 + 4321) == 5555 and 5555 % P == 5 and 5 in ORBITS['NQR_5']

    # Outer digit 5 ∈ NQR_5
    assert 5 in ORBITS['NQR_5']

    # DR of layer 4 digit sum
    assert sum(int(c) for c in '123414321') == 21
    assert dr(21) == 3 and 3 in ORBITS['SOVEREIGN_SPIRAL']

    # DR of 414 digit sum
    assert sum(int(c) for c in '414') == 9 and dr(9) == 9

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 147: The 414 Palindrome Tower in GF(37)")
    print("=" * 62)
    print()
    print("  414 ≡ 7 ∈ D7    (digit 1 surrounded by 4s)")
    print("  123414321 ≡ 7 ∈ D7   (same as 414 — forced by ord₃₇(10)=3)")
    print()
    print("  Tower:")
    tower = [1, 414, 34143, 2341432, 123414321, 51234143215]
    for t in tower:
        print(f"    {t:>12d}  ≡ {t%P:2d}  {orbit_of(t)}")
    print()
    print("  Hex ring 1-4-2-4-3-4: sum=18 ∈ SEED_ORB")
    ring = [1, 4, 2, 4, 3, 4]
    for i in range(6):
        w = ring[i]*100 + ring[(i+1)%6]*10 + ring[(i+2)%6]
        print(f"    pos {i}: {w} ≡ {w%P:2d}  {orbit_of(w)}")
    print()
    print("  1234 ≡ 13 ∈ NQR_5  (= 142241's orbit, Theorem 146)")
    print("  1234+4321 = 5555 ≡ 5 ∈ NQR_5  (outer digit orbit)")
    print()
    print("  DR(123414321) = DR(21) = 3 ∈ SOVEREIGN_SPIRAL")


if __name__ == "__main__":
    run_assertions()
    summarise()
