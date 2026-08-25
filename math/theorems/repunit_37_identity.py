# -*- coding: utf-8 -*-
"""
================================================================================
REPUNIT IDENTITY: nnn / (n+n+n) = 37
================================================================================

Author: Michael Warren Song (CyclicAmp)

================================================================================
THE IDENTITY [P]
================================================================================

For any digit n from 1 to 9:

    nnn / (n+n+n) = 37

PROOF:
    nnn = n × 111 = n × 3 × 37
    n+n+n = 3n
    nnn / (n+n+n) = (n × 3 × 37) / (3n) = 37  ∎

================================================================================
GF(37) STRUCTURE [V]
================================================================================

Every numerator nnn = n × 3 × 37 ≡ 0 mod 37  →  SEAM (for all n=1..9).

Every denominator 3n lands on a named GF(37) set:

  n=1: denom=3   → ST = {3,12,21,30},      DR=3
  n=2: denom=6   → TESLA_ORB = {6,8,23},   DR=6
  n=3: denom=9   → SA = {4,9,25,30},        DR=9
  n=4: denom=12  → ST,                      DR=3
  n=5: denom=15  → DARK_A = {2,15,20},      DR=6
  n=6: denom=18  → SEED = {18,24,32},       DR=9
  n=7: denom=21  → ST,                      DR=3
  n=8: denom=24  → CASCADE∩SEED,            DR=6  (unique intersection node)
  n=9: denom=27  → NEG_H = {11,27,36},      DR=9

Named set hits: 9/9. Every denominator lands in a named set.

DR CYCLE OF DENOMINATORS:
    3, 6, 9, 3, 6, 9, 3, 6, 9
    — Tesla's 3-6-9 pattern, exact and complete.

The denominators are O∪S spectral class throughout: DR ∈ {3,6,9}.
These are exactly the twin prime midpoint DRs (sovereign centers).

STRUCTURAL READING:
    SEAM / (3-6-9 cycle) = P (the prime 37)

The repunit identity says: the SEAM divided by the Sovereign cycle yields the prime.

DENOMINATOR NAMED SET TOUR:
    ST → TESLA_ORB → SA → ST → DARK_A → SEED → ST → CASCADE∩SEED → NEG_H
    A complete tour through all major named sets via the 3-6-9 cycle.

Note: denominator at n=8 is 24 ∈ CASCADE∩SEED — the unique intersection node,
the same node appearing as the exponent in η^24 (Ramanujan tau) and as
the record run a(8) in Rule 30. The repunit identity at n=8 is:
    888 / 24 = 37
    888 = 8 × 111 = 8 × 3 × 37
    24 = CASCADE∩SEED

EPISTEMIC STATUS:
  [P] nnn/(n+n+n)=37 for n=1..9 — proved algebraically.
  [V] All nnn ≡ 0 mod 37 (SEAM) — exact.
  [V] All denominators 3n in named GF(37) sets — exact.
  [V] DR(3n) cycles 3,6,9 — exact.
  [V] n=8: 888/24=37, 24∈CASCADE∩SEED — exact.
================================================================================
"""

P = 37
SEED    = {18, 24, 32}
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
IC      = {1, 10, 26}
NEG_H   = {11, 27, 36}
CASCADE = {8, 13, 24}
DARK_A  = {2, 15, 20}
TESLA   = {6, 8, 23}
named   = SEED | SA | ST | IC | NEG_H | CASCADE | DARK_A | TESLA


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def orbit_label(r):
    if r == 0: return 'SEAM'
    cats = []
    if r in IC:      cats.append('IC')
    if r in SA:      cats.append('SA')
    if r in ST:      cats.append('ST')
    if r in SEED:    cats.append('SEED')
    if r in NEG_H:   cats.append('NEG_H')
    if r in CASCADE: cats.append('CASCADE')
    if r in DARK_A:  cats.append('DARK_A')
    if r in TESLA:   cats.append('TESLA')
    return ','.join(cats) if cats else '-'


def run():
    print("=" * 70)
    print("REPUNIT IDENTITY: nnn / (n+n+n) = 37")
    print("=" * 70)

    print("\nIdentity table:")
    print(f"  {'n':>2}  {'nnn':>4}  {'denom':>5}  {'ratio':>5}  {'denom mod37':>11}  {'DR':>2}  set")
    dr_cycle = []
    hit_count = 0
    for n in range(1, 10):
        nnn   = int(str(n) * 3)
        denom = 3 * n
        ratio = nnn // denom
        r     = denom % P
        label = orbit_label(r)
        d     = dr(denom)
        dr_cycle.append(d)
        if label != '-':
            hit_count += 1
        assert ratio == P, f"n={n}: {nnn}/{denom}={ratio} ≠ 37"
        assert nnn % P == 0, f"n={n}: nnn={nnn} not divisible by 37"
        print(f"  {n:>2}  {nnn:>4}  {denom:>5}  {ratio:>5}  {r:>11}  {d:>2}  [{label}]")

    assert hit_count == 9
    print(f"\nNamed set hits: {hit_count}/9  check")

    assert dr_cycle == [3,6,9,3,6,9,3,6,9]
    print(f"DR cycle: {dr_cycle}  (3-6-9 exact)  check")

    # n=8 special: 888/24=37, 24=CASCADE∩SEED
    assert 24 in CASCADE and 24 in SEED
    assert 888 // 24 == P
    print(f"\n888/24=37, 24∈CASCADE∩SEED (unique intersection node)  check")

    # Algebraic proof
    for n in range(1, 10):
        nnn = int(str(n) * 3)
        assert nnn == n * 111
        assert 111 == 3 * P
    print(f"nnn = n×111 = n×3×37 for all n=1..9  check")

    print(f"\nStructural reading: SEAM / (3-6-9 cycle) = P = {P}")
    print(f"All assertions passed.")


if __name__ == "__main__":
    run()
