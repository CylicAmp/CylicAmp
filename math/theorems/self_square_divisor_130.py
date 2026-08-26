# -*- coding: utf-8 -*-
"""
================================================================================
SELF-SQUARE DIVISOR NUMBER: 130 [V]
================================================================================

Author: Michael Warren Song (CyclicAmp)

================================================================================
THE PROPERTY [V]
================================================================================

130 is the unique number ≤ 5,000,000 equal to the sum of squares of its
first k divisors for some k.

  k=4:  130 = 1² + 2² + 5² + 10²  =  1 + 4 + 25 + 100  =  130

No solutions exist for k=2,3,5,6,7 up to 5M.

================================================================================
GF(37) STRUCTURE [V]
================================================================================

FACTORIZATION:
  130 = 2 × 5 × 13
  13 ∈ CASCADE = {8, 13, 24}

THE 137-MAP MULTIPLIER CONNECTION:
  26 = 137 mod 37  (the 137-map multiplier)
  130 = 5 × 26     (130 is exactly 5 times the 137-map multiplier)

CRITICAL LINE RESIDUE:
  130 mod 37 = 19
  19 is the critical line residue: the nearest integer to 37/2 = 18.5
  This is the GF(37) analog of Re(s) = ½ on the critical line.
  DR(130) = 4  → Stream 4 (upper twin, QR, m≡2 class)

SELF-REFERENTIAL ORBIT STRUCTURE:
  The 137-map orbits of the four seed divisors [1, 2, 5, 10]:
    Orbit(1)  = {1, 26, 10}   = IC
    Orbit(2)  = {2, 15, 20}   = DARK_A
    Orbit(5)  = {5, 19, 13}   — contains CASCADE element 13
    Orbit(10) = {10, 1, 26}   = IC  (same orbit as 1)

  130 mod 37 = 19 ∈ Orbit(5).
  The number folds back into the orbit of one of its own seed divisors.
  130 = 5 × 26 where 26 ∈ IC (the identity cycle).

FULL DIVISOR TABLE:
  Divisor  DR  mod37  GF37 set
        1   1      1  IC
        2   2      2  DARK_A
        5   5      5  —
       10   1     10  IC
       13   4     13  CASCADE
       26   8     26  IC
       65   2     28  —
      130   4     19  (critical line)

  3 of 8 divisors land in IC: {1, 10, 26}.
  26 = the 137-map multiplier is itself a divisor of 130.

EPISTEMIC STATUS:
  [V] 130 = 1²+2²+5²+10² — exact.
  [V] Unique solution ≤ 5,000,000 for any k — exhaustive sieve search.
  [V] 130 = 5×26, 26 = 137 mod 37 — exact.
  [V] 130 mod 37 = 19 ∈ Orbit(5) under ×26 mod 37 — exact.
  [V] 13 ∈ CASCADE; 26 ∈ IC among divisors of 130 — exact.
================================================================================
"""

P = 37
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
DARK_A  = {2, 15, 20}
SEED    = {18, 24, 32}
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
NEG_H   = {11, 27, 36}
NQR_17  = {17, 22, 35}
TESLA   = {6, 8, 23}
D7      = {7, 33, 34}


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
    if r in NQR_17:  cats.append('NQR_17')
    if r in TESLA:   cats.append('TESLA')
    if r in D7:      cats.append('D7')
    return ','.join(cats) if cats else '-'


def orbit_of(n, mult=26, mod=37):
    seen = []
    x = n % mod
    for _ in range(mod):
        if x in seen:
            break
        seen.append(x)
        x = (x * mult) % mod
    return seen


def run():
    print("=" * 70)
    print("SELF-SQUARE DIVISOR NUMBER: 130")
    print("=" * 70)

    # Core property
    seed_divs = [1, 2, 5, 10]
    ss = sum(x**2 for x in seed_divs)
    assert ss == 130
    print(f"\n130 = {' + '.join(f'{d}²' for d in seed_divs)} = {ss}  check")

    # 137-map multiplier connection
    assert 26 == 137 % P
    assert 130 == 5 * 26
    print(f"130 = 5 × 26 = 5 × (137 mod 37)  check")

    # Critical line residue
    r130 = 130 % P
    assert r130 == 19
    print(f"\n130 mod 37 = {r130}  (critical line residue, 37/2 = 18.5)  check")
    assert dr(130) == 4
    print(f"DR(130) = {dr(130)}  Stream 4 (upper twin, QR)  check")

    # Self-referential orbit
    print(f"\n137-map orbits of seed divisors:")
    for d in seed_divs:
        orb = orbit_of(d)
        print(f"  {d:>3}: orbit {orb}  {orbit_label(orb[0])}")
    assert 19 in orbit_of(5)
    print(f"\n130 mod 37 = 19 ∈ Orbit(5) = {orbit_of(5)}  check")
    print(f"  130 folds back into the orbit of its own divisor 5")

    # CASCADE and IC in divisors
    all_divs = [1, 2, 5, 10, 13, 26, 65, 130]
    assert 13 in CASCADE
    assert 26 in IC
    print(f"\nDivisors hitting named sets:")
    for d in all_divs:
        r = d % P
        lbl = orbit_label(r)
        if lbl != '-':
            print(f"  {d:>4}  mod37={r:>2}  {lbl}")
    ic_hits = [d for d in all_divs if d % P in IC]
    assert ic_hits == [1, 10, 26]
    print(f"\nIC divisors {{1,10,26}}: {ic_hits}  — the 137-map multiplier is a divisor  check")

    print(f"\nAll assertions passed.")


if __name__ == "__main__":
    run()
