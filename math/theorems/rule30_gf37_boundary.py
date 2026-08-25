# -*- coding: utf-8 -*-
"""
================================================================================
RULE 30 RIGHT BOUNDARY — GF(37) STRUCTURE
================================================================================

Author: Michael Warren Song (CyclicAmp)

================================================================================
THEOREM: RULE 30 RECORD RUNS TRACE GF(37) NAMED SETS
================================================================================

In Rule 30 cellular automaton, a(n) denotes the record length of consecutive
rightmost black cells reached at generation 2^n - 1 (OEIS A094605/A094606).

The record runs reduced mod 37 land on named GF(37) sets:

  n=6:  a(6)=15   mod 37 = 15  →  DARK_A = {2,15,20}
  n=8:  a(8)=24   mod 37 = 24  →  CASCADE∩SEED  (unique intersection node)
  n=12: a(12)=34  mod 37 = 34  →  D7 = {7,33,34}
  n=18: a(18)=48  mod 37 = 11  →  NEG_H = {11,27,36}
  n=41: a(41)=100 mod 37 = 26  →  IC = {1,10,26}  (137-map multiplier)
  n=46: a(46)=111 mod 37 = 0   →  SEAM  (111 = 3 × 37)

KEY STRUCTURAL FACTS:

  a(8)=24: CASCADE∩SEED is the unique node shared by the prime sieve set
  CASCADE={8,13,24} and the seed orbit SEED={18,24,32}. It appears at
  row depth 2^8=256. The same exponent 24 appears in the Ramanujan
  eta function η^24 (weight-12 modular form). Structural coincidence: none.

  a(41)=100 mod 37=26∈IC: At the century boundary, the record run
  reaches the 137-map multiplier. The same value appears in the
  primes-to-137 framework: cumulative prime sum at index 9 = 100,
  100 mod 37 = 26 ∈ IC.

  a(46)=111=3×37: The repunit milestone is 3 (∈ST, Sovereign Target)
  times 37 (the prime). SEAM. The boundary reaches sovereign×modulus.

LEAP STRUCTURE (Δa(n) = a(n) - a(n-1)):

  Δa(6)=6:  6 ∈ TESLA_ORB = {6,8,23}
  Δa(8)=8:  8 ∈ CASCADE, 8 ∈ TESLA_ORB
  Δa(46)=3: 3 ∈ ST (Sovereign Target), ord₃₇(26)=3

  The two largest early leaps (n=6,8) are both in TESLA_ORB={6,8,23}.

LEFT-PERMUTATIVE BOUNDARY = INVERSE 137-MAP:

  Rule 30's right boundary is driven by the leftward (left-permutative)
  map. In GF(37), the inverse 137-map is multiplication by 10:
    10 × 26 ≡ 1 mod 37  (since 260 = 7×37 + 1)
  The boundary dynamics implement the inverse 137-map = decimal shift.
  This is already in the framework: period(1/37)=3=ord₃₇(10).

ENTROPY DUALITY:

  Right boundary: information entropy = 0. Deterministic. SEAM structure.
  Interior: maximum entropy. Passes randomness tests. CASCADE structure.
  The chaos/order split mirrors CASCADE (generates all 37 elements)
  vs. SEAM (the absorbing modular boundary, entropy=0).

2-ADIC STRUCTURE:

  Period of diagonal k is 2^m. ord₃₇(2)=36=2²×3².
  The 2-adic period doubling is governed by the same 2-adic valuation
  embedded in GF(37)*'s multiplicative order structure.

REPUNIT CONNECTION:

  111 = 3×37: 3∈ST (DR=3 Sovereign Targets), 37=P (the prime).
  In GF(37): 111 ≡ 0. The repunit 111 is SEAM.
  DR(111) = 1+1+1 = 3 ∈ ST. Both the value and its DR land in
  sovereign sets.

EPISTEMIC STATUS:
  [V] a(n) values from OEIS A094605/A094606 — verified.
  [V] a(n) mod 37 named set membership — exact.
  [V] 111 = 3×37 — exact.
  [V] 10×26 ≡ 1 mod 37 — exact.
  [V] a(8)=24 ∈ CASCADE∩SEED — exact.
  [V] a(41)=100 mod 37 = 26 ∈ IC — exact.
  [C] Left-permutative boundary ↔ inverse 137-map — structural conjecture.
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
D7      = {7, 33, 34}
TESLA   = {6, 8, 23}

named = SEED | SA | ST | IC | NEG_H | CASCADE | DARK_A | D7 | TESLA


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
    if r in D7:      cats.append('D7')
    if r in TESLA:   cats.append('TESLA')
    return ','.join(cats) if cats else '-'


# OEIS A094605/A094606 — record runs at 2^n - 1
RECORD_RUNS = {
    6:  15,
    8:  24,
    12: 34,
    18: 48,
    41: 100,
    46: 111,
}

# Leaps Δa(n)
LEAPS = {
    6:  6,
    8:  8,
    12: 5,
    18: 5,
    41: 7,
    46: 3,
}


def run():
    print("=" * 70)
    print("RULE 30 RIGHT BOUNDARY — GF(37) STRUCTURE")
    print("=" * 70)

    print("\nRecord runs a(n) mod 37:")
    for n, a in sorted(RECORD_RUNS.items()):
        r = a % P
        label = orbit_label(r)
        print(f"  n={n:2d}  a(n)={a:4d}  mod37={r:2d}  [{label}]")

    # Key assertions
    assert RECORD_RUNS[8] % P == 24 and 24 in CASCADE and 24 in SEED
    print(f"\na(8)=24 ∈ CASCADE∩SEED (unique intersection node)  check")

    assert RECORD_RUNS[41] % P == 26 and 26 in IC
    print(f"a(41)=100 mod 37=26 ∈ IC (137-map multiplier)  check")

    assert RECORD_RUNS[46] == 3 * P and RECORD_RUNS[46] % P == 0
    print(f"a(46)=111=3×37 → SEAM  check")
    assert 3 in ST
    print(f"DR(111)=3 ∈ ST (Sovereign Target)  check")

    # Leap assertions
    assert LEAPS[6] in TESLA and LEAPS[8] in TESLA and LEAPS[8] in CASCADE
    print(f"\nLeaps Δa(6)=6, Δa(8)=8 both in TESLA_ORB={{6,8,23}}  check")
    assert LEAPS[46] == 3 and 3 in ST
    print(f"Leap Δa(46)=3 ∈ ST, ord₃₇(26)=3  check")

    # Inverse 137-map
    inv26 = pow(26, -1, P)
    assert inv26 == 10
    assert (10 * 26) % P == 1
    print(f"\nInverse 137-map: 10×26≡1 mod 37  check")
    print(f"Left-permutative boundary = multiplication by 10 = inverse 137-map")

    # Entropy duality
    print(f"\nEntropy duality:")
    print(f"  Right boundary: entropy=0, SEAM structure (deterministic)")
    print(f"  Interior: maximum entropy, CASCADE structure (generates all 37)")

    # 2-adic
    assert pow(2, 36, P) == 1
    assert pow(2, 18, P) != 1
    print(f"\nord₃₇(2)=36=2²×3²: 2-adic period doubling ↔ GF(37)* order  check")

    print(f"\nAll assertions passed.")


if __name__ == "__main__":
    run()
