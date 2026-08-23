# -*- coding: utf-8 -*-
"""
================================================================================
MONTE CARLO PI / PI DIGITS — GF(37) CONNECTIONS
================================================================================

Author: Michael Warren Song (CyclicAmp)

VERIFIED RESULTS:

1. 314 mod 37 = 18 ∈ SEED = {18, 24, 32}
   The first 3 significant digits of π (314) land on SEED entry point 18.
   SEED = {18, 24, 32}: the 137-map orbit of the pipeline reference seed 246.

2. Integer digit of π = 3 ∈ ST = {3, 12, 21, 30}
   3 is a Sovereign Target node.

3. DR(355) = 4 ∈ SA = {4, 9, 25, 30}
   355/113 is the best rational approximation to π with denominator ≤ 113.
   (Milü: |π - 355/113| < 3×10⁻⁷)
   DR(355) = 3+5+5 = 13 → 1+3 = 4 ∈ SA.

4. Monte Carlo multiplier 4 ∈ SA
   Monte Carlo π estimation: ratio of hits to total × 4 → π.
   The factor 4 is a Sovereign Anchor node.

5. π[:18] mod 37 = 30 ∈ SA ∩ ST (double-sovereign)
   3141592653589793238 mod 37 = 30.
   30 is the only element in both SA and ST simultaneously.
   This is the same double-sovereign residue as Ramanujan's constant 1103.

EPISTEMIC STATUS:
  [V] 314 mod 37 = 18 ∈ SEED — exact integer arithmetic on the decimal truncation.
  [V] 3 ∈ ST — exact.
  [V] DR(355) = 4 ∈ SA — exact for the integer 355.
  [V] 4 (MC multiplier) ∈ SA — exact.
  [V] π[:18] mod 37 = 30 ∈ SA ∩ ST — exact integer arithmetic.

NOTE ON π ITSELF:
  π is irrational and transcendental; "π mod 37" is not defined as a GF(37) element.
  All connections here are to integer truncations or approximations of π.

GF(37) STRUCTURE:
  SEED = {18, 24, 32}: 137-map orbit of pipeline reference seed 246.
  SA = {4, 9, 25, 30}: Sovereign Anchor nodes (LOCKED).
  ST = {3, 12, 21, 30}: Sovereign Target nodes (DR=3 residues).
  30 is the double-sovereign element: the only member of both SA and ST.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
SEED = {18, 24, 32}
SA   = {4, 9, 25, 30}
ST   = {3, 12, 21, 30}
IC   = {1, 10, 26}
NEG_H = {11, 27, 36}

PI_DIGITS = '314159265358979323846264338327950288419716939937510'


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def run():
    print("=" * 70)
    print("MONTE CARLO PI / PI DIGITS — GF(37) CONNECTIONS")
    print("=" * 70)

    # 1. 314 mod 37 = 18 ∈ SEED
    assert 314 % P == 18
    assert 18 in SEED
    print(f"\n1. FIRST 3 DIGITS (314):")
    print(f"   314 mod 37 = {314 % P} ∈ SEED = {{18,24,32}}  check")
    print(f"   SEED = 137-map orbit of reference seed 246")

    # 2. Integer digit 3 ∈ ST
    assert 3 in ST
    print(f"\n2. INTEGER PART OF π = 3:")
    print(f"   3 ∈ ST = {{3,12,21,30}} (Sovereign Target)  check")

    # 3. DR(355) = 4 ∈ SA
    assert dr(355) == 4
    assert 4 in SA
    print(f"\n3. MILÜ APPROXIMATION 355/113:")
    print(f"   DR(355) = {dr(355)} ∈ SA = {{4,9,25,30}}  check")
    print(f"   355/113 ≈ π (error < 3×10⁻⁷, best rational approx denom ≤ 113)")

    # 4. Monte Carlo multiplier 4 ∈ SA
    assert 4 in SA
    print(f"\n4. MONTE CARLO MULTIPLIER:")
    print(f"   4 (hits/total × 4 → π) ∈ SA  check")

    # 5. π[:18] mod 37 = 30 ∈ SA ∩ ST
    n18 = int(PI_DIGITS[:18])
    assert n18 % P == 30
    assert 30 in SA and 30 in ST
    print(f"\n5. π[:18] = {n18}:")
    print(f"   mod 37 = {n18 % P} ∈ SA ∩ ST (double-sovereign)  check")
    print(f"   30 is the only element in both SA and ST")
    print(f"   Same double-sovereign residue as Ramanujan constant 1103")

    # Digit truncation table
    print(f"\nPi digit truncations mod 37:")
    print(f"  k | truncation[:k] | mod37 | dr | category")
    for k in [1, 3, 8, 15, 18, 19]:
        n = int(PI_DIGITS[:k])
        r = n % P
        cats = []
        if r in SEED: cats.append('SEED')
        if r in SA:   cats.append('SA')
        if r in ST:   cats.append('ST')
        if r in IC:   cats.append('IC')
        print(f"  {k:2d} | {n:>22d} | {r:5d} |  {dr(n)} | {', '.join(cats) if cats else '-'}")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
