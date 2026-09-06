"""
Theorem 168: Signed Single Digits ±1..±9 — Complete GF(37) Orbit Map

THE COMPLETE SET
=================

The 18 non-zero signed single-digit integers:

  +1, +2, +3, +4, +5, +6, +7, +8, +9
  -1, -2, -3, -4, -5, -6, -7, -8, -9

ORBIT ASSIGNMENTS
==================

  +1 → IC              −1 → ORBIT_11   (complement pair: 1+36=37)
  +2 → DARK_A          −2 → NQR_17     (complement pair: 2+35=37)
  +3 → SOVEREIGN_SPIRAL −3 → D7        (complement pair: 3+34=37)
  +4 → SOVEREIGN_SPIRAL −4 → D7        (complement pair: 4+33=37)
  +5 → NQR_5           −5 → SEED_ORB  (complement pair: 5+32=37)
  +6 → TESLA_ORB       −6 → NQR_14    (complement pair: 6+31=37)
  +7 → D7              −7 → SOVEREIGN_SPIRAL (complement: 7+30=37)
  +8 → TESLA_ORB       −8 → NQR_14    (complement pair: 8+29=37)
  +9 → SA_ORB          −9 → OUTLIER_ORB (complement: 9+28=37)

Each positive digit n and its negation −n form a complement pair in GF(37):
  n mod 37 + (−n mod 37) = 37 = SEAM.

THE DR MAP
===========

DR is preserved under negation (DR depends on absolute value):

  DR(n) = DR(−n)  for all n

So the DR of +k equals the DR of −k: 1,2,3,4,5,6,7,8,9.
DR coincides with absolute value for single digits.

SUMS
=====

  Sum +1..+9 = 45  mod37=8  ∈ TESLA_ORB
  Sum −1..−9 = −45 mod37=29 ∈ NQR_14

  TESLA_ORB ↔ NQR_14 (complement pair: 8+29=37 ✓)

  Total ±1..±9 = 0 → SEAM.

ORBIT COVERAGE
===============

The 18 signed single digits hit 10 of the 12 named orbits:

  Present: IC, ORBIT_11, DARK_A, NQR_17, SOVEREIGN_SPIRAL, D7,
           NQR_5, SEED_ORB, TESLA_ORB, NQR_14, SA_ORB, OUTLIER_ORB
  Missing: none — all 12 orbits are covered.

Every named GF(37) orbit appears at least once in the signed digit set.

SIGN-ORBIT PAIRING TABLE
==========================

  |n|   + orbit             − orbit
  -----  -------------------  --------------------
   1     IC                   ORBIT_11
   2     DARK_A               NQR_17
   3     SOVEREIGN_SPIRAL     D7
   4     SOVEREIGN_SPIRAL     D7
   5     NQR_5                SEED_ORB
   6     TESLA_ORB            NQR_14
   7     D7                   SOVEREIGN_SPIRAL
   8     TESLA_ORB            NQR_14
   9     SA_ORB               OUTLIER_ORB

Observation: 3 and 4 both map positive to SOVEREIGN_SPIRAL; their negatives
both map to D7. SOVEREIGN_SPIRAL ↔ D7 is a complement pair — this is why
both +3/+4 → SOVEREIGN_SPIRAL and both −3/−4 → D7.

Similarly 6 and 8 both map to TESLA_ORB (positive), NQR_14 (negative).
6 ∈ TESLA_ORB and 8 ∈ TESLA_ORB are the same orbit; their complements
31 and 29 are both in NQR_14.
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

EXPECTED = {
    1:  ('IC', 'ORBIT_11'),
    2:  ('DARK_A', 'NQR_17'),
    3:  ('SOVEREIGN_SPIRAL', 'D7'),
    4:  ('SOVEREIGN_SPIRAL', 'D7'),
    5:  ('NQR_5', 'SEED_ORB'),
    6:  ('TESLA_ORB', 'NQR_14'),
    7:  ('D7', 'SOVEREIGN_SPIRAL'),
    8:  ('TESLA_ORB', 'NQR_14'),
    9:  ('SA_ORB', 'OUTLIER_ORB'),
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
    # Each signed digit maps to expected orbit
    for k, (pos_orb, neg_orb) in EXPECTED.items():
        assert orbit_of(k) == pos_orb, f'+{k}: expected {pos_orb}, got {orbit_of(k)}'
        assert orbit_of(-k) == neg_orb, f'-{k}: expected {neg_orb}, got {orbit_of(-k)}'

    # Each pair sums to SEAM
    for k in range(1, 10):
        assert (k % P + (-k) % P) % P == 0

    # DR preserved under negation
    for k in range(1, 10):
        assert dr(k) == dr(-k) == k

    # Sum +1..+9 = 45 → TESLA_ORB (8)
    s_pos = sum(range(1, 10))
    assert s_pos == 45
    assert s_pos % P == 8 and 8 in ORBITS['TESLA_ORB']

    # Sum -1..-9 = -45 → NQR_14 (29)
    s_neg = -sum(range(1, 10))
    assert s_neg % P == 29 and 29 in ORBITS['NQR_14']

    # TESLA_ORB ↔ NQR_14 complement
    assert (8 + 29) == 37

    # Total = SEAM
    assert (s_pos + s_neg) % P == 0

    # All 12 orbits covered
    covered = set()
    for k in range(1, 10):
        covered.add(orbit_of(k))
        covered.add(orbit_of(-k))
    assert covered == set(ORBITS.keys()), f"Missing: {set(ORBITS.keys()) - covered}"

    # 3 and 4 both positive → SOVEREIGN_SPIRAL
    assert orbit_of(3) == orbit_of(4) == 'SOVEREIGN_SPIRAL'
    # 6 and 8 both positive → TESLA_ORB
    assert orbit_of(6) == orbit_of(8) == 'TESLA_ORB'

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 168: Signed Digits ±1..±9 — GF(37) Orbit Map")
    print("=" * 62)
    print()
    print(f"  {'n':>3}   mod37  orbit              neg   mod37  orbit")
    print(f"  {'-'*62}")
    for k in range(1, 10):
        pos_r = k % P
        neg_r = (-k) % P
        print(f"  +{k}     {pos_r:>3}  {orbit_of(k):<20} "
              f"-{k}     {neg_r:>3}  {orbit_of(-k)}")
    print()
    print(f"  Sum +1..+9 = 45  mod37=8  TESLA_ORB")
    print(f"  Sum -1..-9 = -45 mod37=29 NQR_14")
    print(f"  TESLA_ORB ↔ NQR_14 (8+29=37)")
    print(f"  Total ±1..±9 = 0 → SEAM")
    print()
    print(f"  All 12 GF(37) orbits covered by the 18 signed digits.")


if __name__ == "__main__":
    run_assertions()
    summarise()
