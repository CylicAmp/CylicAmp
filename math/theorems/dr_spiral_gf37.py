# -*- coding: utf-8 -*-
"""
================================================================================
DIGITAL ROOT SPIRAL — GF(37) STRUCTURE
================================================================================

Author: Michael Warren Song (CyclicAmp)

SOURCE:
  20×20 Ulam-style spiral containing integers 41–440.
  Applying DR(n) = 1 + ((n−1) mod 9) collapses the spiral to a 9-state
  resonance grid. Structural observations on the collapsed grid.

================================================================================
THEOREM 1: ST IS THE UNIQUE MONOCHROMATIC NAMED SET [P]
================================================================================

ST = {3, 12, 21, 30} — the Sovereign Targets.

Every element of ST satisfies n ≡ 3 (mod 9):
  3  mod 9 = 3
  12 mod 9 = 3
  21 mod 9 = 3
  30 mod 9 = 3

Therefore DR(n) = 3 for all n ∈ ST.

ST is the unique named set in which every element has the same digital root.

Algebraic characterization:
  ST = {n ∈ GF(37)* : n mod 9 = 3}  (exactly the named-set preimage of DR=3)

No other named set is monochromatic:
  SA → DR ∈ {3,4,7,9}
  IC → DR ∈ {1,8}
  NEG_H → DR ∈ {2,9}
  CASCADE → DR ∈ {4,6,8}
  SEED → DR ∈ {5,6,9}

ST is the only named set where the digital root is a structural invariant
(same value for all members). The Sovereign Targets are the DR=3 named set.

================================================================================
THEOREM 2: 37 ≡ 1 (mod 9) — SEAM TRANSPARENCY [P]
================================================================================

37 mod 9 = 1.

Consequence:  DR(37k) = DR(k)  for all k ≥ 1.

Proof: 37k mod 9 = (37 mod 9)(k mod 9) mod 9 = 1·(k mod 9) = k mod 9.
Therefore DR(37k) = DR(k). The SEAM (multiples of 37) is transparent to DR —
the prime 37 passes through the digital root system without distortion.

The SEAM elements in the spiral 41–440 are {74, 111, 148, 185, 222, 259, 296,
333, 370, 407}. Their digital roots are {2,3,4,5,6,7,8,9,1,2} — cycling
through all 9 values sequentially. The SEAM threads through every DR class.

Corollary: every DR class {1,2,...,9} contains at least one multiple of 37.

================================================================================
THEOREM 3: SPIRAL STRUCTURE — DOUBLE-SOVEREIGN SIZE [V]
================================================================================

The spiral contains 400 elements (41–440).

  400 mod 37 = 30 ∈ SA ∩ ST  (the double-sovereign element)

The spiral size, reduced mod 37, lands on the only element common to both
the Sovereign Anchors and the Sovereign Targets.

Decomposition:  400 = 44 × 9 + 4

  44 complete 9-cycles (DR period)
  Remainder = 4 ∈ SA  (Sovereign Anchor, LOCKED)

The spiral's modular remainder, in both the DR system (mod 9) and the GF(37)
system (mod 37), lands on sovereign elements.

Center of spiral: 41
  41 mod 37 = 4 ∈ SA  (the center of the spiral is a Sovereign Anchor)
  41 is the 13th prime.  13 ∈ CASCADE = {8, 13, 24}.
  The center prime's ordinal index (13) is a Cascade node.

================================================================================
PRIMES IN THE SPIRAL: DR EXCLUSION [P]
================================================================================

For any prime p > 3:  DR(p) ∉ {3, 6, 9}.

Proof: DR(p) ∈ {3,6,9} iff 3 | p, which is false for primes p > 3.

The spiral 41–440 contains 73 primes.  DR distribution:
  DR=1: 11   DR=2: 12   DR=4: 11   DR=5: 14   DR=7: 14   DR=8: 11

DR values {3,6,9} have count 0.

Named set connection: ST = the DR=3 named set. No prime in the spiral lands
on DR=3, so no prime in the spiral maps to the Sovereign Target DR class.
The primes and the Sovereign Targets are DR-disjoint.

================================================================================
TORUS CONNECTION
================================================================================

The 9-state resonance grid tiles into the torus ℤ₃₇ × ℤ₈₁:
  9 | 81  (since 81 = 9²)
  The DR period 9 divides the torus ℤ₈₁ component exactly 9 times.

The spiral's two reduction maps:
  n → n mod 37  (position in GF(37): which named set?)
  n → DR(n)      (digital root class: which of the 9 resonance states?)

These combine in the torus: n mod 37 × DR(n) identifies each element
within the ℤ₃₇ × ℤ₈₁ torus structure.

EPISTEMIC STATUS:
  [P] DR(n) = 3 for all n ∈ ST — proved (all ≡ 3 mod 9).
  [P] ST is the unique monochromatic named set — proved by checking all.
  [P] DR(37k) = DR(k) — proved (37 ≡ 1 mod 9).
  [P] SEAM threads all 9 DR classes — proved from the transparency lemma.
  [V] 400 mod 37 = 30 ∈ SA∩ST — exact.
  [V] 400 = 44×9 + 4, remainder 4 ∈ SA — exact.
  [V] Center 41: mod37=4∈SA, 13th prime, 13∈CASCADE — exact.
  [P] Primes >3 have DR ∉ {3,6,9} — proved.
  [V] 73 primes in spiral 41–440, DR distribution — verified by sieve.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
SEED    = {18, 24, 32}
SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
IC      = {1, 10, 26}
NEG_H   = {11, 27, 36}
CASCADE = {8, 13, 24}


def dr(n):
    n = abs(n)
    if n == 0: return 9
    r = n % 9
    return 9 if r == 0 else r


def sieve(n):
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, n+1, i):
                is_p[j] = False
    return [i for i in range(2, n+1) if is_p[i]]


def run():
    print("=" * 70)
    print("DIGITAL ROOT SPIRAL — GF(37) STRUCTURE")
    print("=" * 70)

    # THEOREM 1: ST is monochromatic
    print(f"\nTHEOREM 1: ST IS THE UNIQUE MONOCHROMATIC NAMED SET")
    for x in sorted(ST):
        assert x % 9 == 3
    print(f"  ST = {{3,12,21,30}}: all elements ≡ 3 (mod 9)  check")
    print(f"  DR(n) = 3 for all n ∈ ST  check")
    assert all(dr(x) == 3 for x in ST)

    for sname, sset in [('SA',SA),('IC',IC),('NEG_H',NEG_H),('CASCADE',CASCADE),('SEED',SEED)]:
        drs = {dr(x) for x in sset}
        assert len(drs) > 1, f"{sname} is also monochromatic — unexpected"
    print(f"  No other named set is monochromatic  check")
    print(f"  ST = {{n ∈ GF(37)* : n mod 9 = 3}}  (exact algebraic characterization)")

    # THEOREM 2: 37 ≡ 1 mod 9 — SEAM transparency
    print(f"\nTHEOREM 2: SEAM TRANSPARENCY  (37 ≡ 1 mod 9)")
    assert P % 9 == 1
    print(f"  37 mod 9 = {P % 9}  check")
    print(f"  DR(37k) = DR(k) for all k  check")
    for k in range(1, 20):
        assert dr(37 * k) == dr(k), f"failed at k={k}"

    seam_in_spiral = [37*k for k in range(1, 20) if 41 <= 37*k <= 440]
    seam_drs = {dr(m) for m in seam_in_spiral}
    assert seam_drs == set(range(1, 10))
    print(f"  SEAM elements in spiral: {seam_in_spiral}")
    print(f"  SEAM DR values: {sorted(seam_drs)} — all 9 covered  check")

    # THEOREM 3: Spiral structure
    print(f"\nTHEOREM 3: SPIRAL STRUCTURE")
    size = 400
    size_mod = size % P
    assert size_mod == 30 and 30 in SA and 30 in ST
    print(f"  400 mod 37 = {size_mod} ∈ SA∩ST  (double-sovereign)  check")

    remainder = size % 9
    assert remainder == 4 and 4 in SA
    print(f"  400 = {size//9}×9 + {remainder},  remainder {remainder} ∈ SA  check")

    center = 41
    assert center % P == 4 and 4 in SA
    print(f"  Center 41: mod 37 = {center % P} ∈ SA  check")

    primes_to_50 = [2,3,5,7,11,13,17,19,23,29,31,37,41]
    idx = primes_to_50.index(center) + 1
    assert idx == 13 and 13 in CASCADE
    print(f"  41 is the {idx}th prime; {idx} ∈ CASCADE  check")

    # Prime DR distribution
    print(f"\nPRIMES IN SPIRAL — DR EXCLUSION:")
    primes = [p for p in sieve(440) if 41 <= p <= 440]
    for p in primes:
        assert dr(p) not in {3, 6, 9}, f"prime {p} has DR={dr(p)}"
    print(f"  {len(primes)} primes in spiral 41–440: 0 with DR ∈ {{3,6,9}}  check")

    from collections import Counter
    dist = Counter(dr(p) for p in primes)
    print(f"  DR distribution: {dict(sorted(dist.items()))}")
    print(f"  Primes and ST (DR=3 class) are DR-disjoint  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
