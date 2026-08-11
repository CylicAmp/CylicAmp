"""
Theorem 157: Repdigit Triples Are SEAM — Trinity DRs, 37 as Factor

THE OBSERVATION
================

    333 = 9 × 37

333 is an exact multiple of 37. It maps to SEAM (0 mod 37). Its DR is 9,
the trinity identity.

THIS EXTENDS TO ALL REPDIGIT TRIPLES
========================================

Every 3-digit repdigit number ddd (for d = 1..9) is divisible by 37:

    111 = 3 × 37      DR = 3
    222 = 6 × 37      DR = 6
    333 = 9 × 37      DR = 9
    444 = 12 × 37     DR = 3
    555 = 15 × 37     DR = 6
    666 = 18 × 37     DR = 9
    777 = 21 × 37     DR = 3
    888 = 24 × 37     DR = 6
    999 = 27 × 37     DR = 9

All nine map to SEAM. The DR cycle is exactly the trinity: {3,6,9,3,6,9,3,6,9}.

WHY THIS IS EXACT
==================

ddd = d × 111 = d × 3 × 37 = 3d × 37

111 = 3 × 37 is the seed identity: the repunit R(3) is exactly divisible by 37,
and the factor 3 is a trinity element.

Therefore ddd ≡ 0 (mod 37) for every digit d. No exceptions.

THE DR CYCLE
=============

DR(ddd) = DR(d × 111) = DR(d × 3) = DR(3d)

The factors (3d) cycle through: 3,6,9,12,15,18,21,24,27.
Their DRs: 3,6,9,3,6,9,3,6,9 — the trinity cycle exactly, period 3.

The trinity {3,6,9} controls the DR of every repdigit triple through the
multiplicative structure: 3d for d=1..9 rotates through all three trinity values
with period 3, then repeats.

CONNECTION TO Φ₃ FORCING (Theorem 150)
=========================================

111 = 3 × 37 = Φ₃(10) — the cyclotomic polynomial value that forces SEAM.
This theorem shows 111 is not special: all repdigit triples share the structure.
But 111 is the generator: ddd = d × 111 for any digit d.

The Φ₃ forcing from T150 operates on 111. The nine repdigit triples are its
complete scalar multiple family (d=1..9).

FACTORS AND THEIR ORBITS
==========================

The factorization ddd = k × 37 where k = 3d:

    d=1: k=3   ∈ SOVEREIGN_SPIRAL
    d=2: k=6   ∈ TESLA_ORB
    d=3: k=9   ∈ SA_ORB
    d=4: k=12  ∈ SA_ORB
    d=5: k=15  ∈ DARK_A
    d=6: k=18  ∈ SEED_ORB   ← 666 = 18×37; 18 ∈ SEED_ORB
    d=7: k=21  ∈ OUTLIER_ORB
    d=8: k=24  ∈ SEED_ORB   ← 888 = 24×37; 24 ∈ SEED_ORB (seed anchor!)
    d=9: k=27  ∈ ORBIT_11

The factors k=18 and k=24 are in SEED_ORB. 666 = 18×37 and 888 = 24×37
are the two SEED_ORB multiples among the nine repdigit triples. 24 is the
seed 246 residue (246 mod 37 = 24).

THE THREE SEAM MULTIPLES: 111, 222, 333
==========================================

The trinity digits (3, 6, 9) produce the "pure trinity" triples:
    d=3: 333 = 9×37 = 3×111     DR=9 (trinity identity)
    d=6: 666 = 18×37 = 6×111    DR=9 (trinity identity)
    d=9: 999 = 27×37 = 9×111    DR=9 (trinity identity)

All three have DR=9. They are the trinity multiples of 111.

111 and 333 are the Φ₃-forcing pair (3 and 9 as multipliers of 37×3):
  111 = 3 × 37: minimum repdigit triple SEAM
  333 = 9 × 37: trinity-scaled SEAM
  999 = 27 × 37 = 3³ × 37: cube-scaled SEAM

CONNECTION TO 369
==================

3+6+9 = 18 ∈ SEED_ORB (also the factor in 666 = 18×37).
3×6×9 = 162 = 4×37+14. 162 mod 37 = 14 ∈ NQR_14, DR(162)=9.
T(9) = 1+2+...+9 = 45. 45 mod 37 = 8 ∈ TESLA_ORB.

369 itself: 369 mod 37 = 36 ∈ ORBIT_11 = {11, 27, 36}.
DR(369) = 3+6+9 → 18 → 9. The number 369 does NOT hit SEAM (it is 36 mod 37).

The digits {3,6,9} do not force SEAM when used as a number. They force SEAM
only as repdigit triples: 333, 666, 999. The digit pattern is the mechanism;
the number 369 has different orbit behavior.

STRUCTURE SUMMARY
==================

    ddd = d × 111 = 3d × 37  for d = 1..9
    All nine repdigit triples: SEAM (exact multiples of 37)
    DR cycle: 3,6,9,3,6,9,3,6,9 — the trinity, period 3
    k=18 (d=6) and k=24 (d=8) factors are in SEED_ORB
    333 = 9×37 (the user's observation): DR=9, trinity identity
    Extends Theorem 150's 111=3×37 to the complete repdigit triple family
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
    # 111 = 3 × 37
    assert 111 == 3 * P

    # All repdigit triples d×111 are SEAM
    for d in range(1, 10):
        rep = d * 111
        assert rep % P == 0, f"{rep} not divisible by 37"

    # DR cycle: {3,6,9,3,6,9,3,6,9}
    dr_cycle = [dr(d * 111) for d in range(1, 10)]
    assert dr_cycle == [3, 6, 9, 3, 6, 9, 3, 6, 9]
    assert all(v in TRINITY for v in dr_cycle)

    # Period 3 in DR cycle
    for d in range(1, 7):
        assert dr(d * 111) == dr((d + 3) * 111)

    # Factors k = 3d and their orbits
    assert 3  in ORBITS['SOVEREIGN_SPIRAL']  # d=1
    assert 6  in ORBITS['TESLA_ORB']         # d=2
    assert 9  in ORBITS['SA_ORB']            # d=3
    assert 12 in ORBITS['SA_ORB']            # d=4
    assert 15 in ORBITS['DARK_A']            # d=5
    assert 18 in ORBITS['SEED_ORB']          # d=6 (666 = 18×37)
    assert 21 in ORBITS['OUTLIER_ORB']       # d=7
    assert 24 in ORBITS['SEED_ORB']          # d=8 (888 = 24×37, seed anchor)
    assert 27 in ORBITS['ORBIT_11']          # d=9

    # 666 and 888 have SEED_ORB factors
    assert 666 == 18 * P and 18 in ORBITS['SEED_ORB']
    assert 888 == 24 * P and 24 in ORBITS['SEED_ORB']
    assert 246 % P == 24   # 24 is the seed 246 anchor

    # 333 = 9×37 (user's observation)
    assert 333 == 9 * P
    assert dr(333) == 9
    assert 9 in TRINITY

    # Trinity multiples of 111: DR=9 for all three
    for d in [3, 6, 9]:
        assert dr(d * 111) == 9

    # 369 is NOT SEAM
    assert 369 % P == 36
    assert 36 in ORBITS['ORBIT_11']
    assert dr(369) == 9   # DR=9 but not SEAM

    # 3+6+9=18 ∈ SEED_ORB
    assert 3 + 6 + 9 == 18
    assert 18 in ORBITS['SEED_ORB']

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 157: Repdigit Triples Are SEAM — Trinity DR Cycle")
    print("=" * 62)
    print()
    print("  ddd = d × 111 = 3d × 37  (exact multiple of 37 for all d=1..9)")
    print()
    print("  d  |  ddd  |  k=3d  |  k-orbit        |  DR")
    print("  ───────────────────────────────────────────────")
    for d in range(1, 10):
        rep = d * 111
        k = 3 * d
        star = " ←" if k in ORBITS['SEED_ORB'] else ""
        print(f"  {d}  |  {rep}  |   {k:2d}   |  {orbit_of(k):<16} |  {dr(rep)}{star}")
    print()
    print("  DR cycle: 3,6,9,3,6,9,3,6,9 — exactly the trinity, period 3")
    print()
    print("  SEED_ORB factors: k=18 (d=6, 666=18×37) and k=24 (d=8, 888=24×37)")
    print("  24 = seed 246 residue; 888 = 24×37 carries the seed orbit anchor")
    print()
    print("  Trinity multiples (DR=9 for all): 333=9×37, 666=18×37, 999=27×37")
    print()
    print("  369 (digits 3,6,9): 369 mod 37=36 ∈ ORBIT_11 — NOT SEAM")
    print("  Digit pattern as a number ≠ repdigit triple SEAM mechanism")


if __name__ == "__main__":
    run_assertions()
    summarise()
