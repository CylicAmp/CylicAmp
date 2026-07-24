"""
100 Prisoners Problem — Permutation Cycles and GF(37) Structure

Setup:
  100 prisoners, 100 boxes. Box i contains number p(i), where p is a random
  permutation of {1,...,100}. Each prisoner opens up to 50 boxes.
  If ALL prisoners find their own number, they survive.

Strategy (cycle-following):
  Prisoner j starts at box j, then opens the box whose number is inside,
  then the box whose number is inside that, etc.
  Prisoner j is traversing the cycle of j in the permutation p.

═══════════════════════════════════════════════════════════════════════════

THEOREM P1 (Survival Criterion)
  Under the cycle-following strategy, prisoner j finds their number within
  50 opens iff the cycle of j in p has length ≤ 50.
  All 100 prisoners survive iff p has no cycle of length > 50.

  Proof:  Prisoner j starts at box j. The sequence of boxes opened is:
    j → p(j) → p(p(j)) → ...
  This is exactly the cycle of j in p. Prisoner j finds their number (j)
  when the sequence returns to j — i.e., after exactly the cycle length
  many steps. So j succeeds within 50 steps iff the cycle has length ≤ 50.
  All survive iff every cycle has length ≤ 50, which means no cycle has
  length > 50.  ∎

THEOREM P2 (Cycle Probability)
  In a random permutation of [n], the probability that a specific k-cycle
  exists (for any k ≤ n) satisfies:
    E[number of k-cycles] = 1/k.
  For k > n/2: at most one k-cycle can exist, so P(k-cycle exists) = 1/k.

  Proof:  Count favorable permutations:
    - Choose k elements from [n]:  C(n,k) ways
    - Arrange them in a directed k-cycle:  (k-1)! ways
    - Arrange remaining n-k elements freely:  (n-k)! ways
    - Total permutations: n!

  E[# k-cycles] = C(n,k) · (k-1)! · (n-k)! / n!
                = [n! / (k!(n-k)!)] · (k-1)! · (n-k)! / n!
                = 1/k.  ✓

  For k > n/2: two k-cycles would require 2k > n elements, but there are
  only n. So at most one k-cycle can exist:
    E[# k-cycles] = 0·P(none) + 1·P(exactly one) = P(k-cycle exists) = 1/k.  ∎

THEOREM P3 (Survival Probability)
  The probability all 100 prisoners survive is:

    P(survival) = 1 − Σ_{k=51}^{100} 1/k  ≈  0.31183

  Proof:  By Theorem P1, failure occurs iff some cycle has length > 50.
  The events {∃ k-cycle} for k=51,...,100 are mutually exclusive (since k>50
  means at most one such cycle, and two such cycles would require >100 elements).
  By Theorem P2, P(k-cycle exists) = 1/k.
  So P(failure) = Σ_{k=51}^{100} 1/k,  and survival is the complement.  ∎

THEOREM P4 (Why This Hacks the Math)
  Random guessing: each prisoner has probability 1/2 of success independently.
  P(all survive | random) = (1/2)^100 ≈ 10^{-30}.

  Cycle strategy: the event is now a GLOBAL statement about one permutation,
  not 100 independent events. The boxes are no longer independent variables.
  The strategy converts independent guessing into deterministic traversal of
  permutation cycles. Success probability improves from ~10^{-30} to ~0.31.

═══════════════════════════════════════════════════════════════════════════

GF(37) STRUCTURE

  THE THRESHOLD (50 boxes):
    50 mod 37 = 13  ∈ CASCADE_BASE = {8, 13, 24}
    The "halfway" threshold of the problem is the cascade mediator — the
    unique non-iterable element of {8,13,24} (13 is the only cascade base
    element that is not a power of 8 mod ratio structure).

  THE UPPER LIMIT (100 prisoners):
    100 mod 37 = 26 = SCALAR_137  (the 137-map multiplier; 137 mod 37 = 26)
    The problem size maps to the 137-map operator.

  TOP THREE CYCLE LENGTHS (98, 99, 100):
    98  mod 37 = 24  ∈ CB ∩ PR ∩ SEED_ORBIT  (cascade base, prim root, seed orbit start)
    99  mod 37 = 25  ∈ SA  (Sovereign Anchor; π(100)=25∈SA also)
    100 mod 37 = 26  = SCALAR_137
    The longest-allowed failures span CB → SA → SCALAR_137.

  THE FIELD PRIME IN RANGE:
    37 ≤ 50: a 37-cycle is allowed — prisoners survive it.
    The field prime's own cycle is within the safe threshold.
    37 mod 37 = 0 (SEAM): the field prime maps to the seam.
    A 37-cycle's length is exactly the field modulus.

  SIEVE CONNECTION (π(100) = 25):
    There are exactly 25 primes ≤ 100.
    25 ∈ SA (Sovereign Anchor).
    The count of primes up to the problem size is a sovereign anchor.
    (Proven in sieve_eratosthenes_gf37.py.)

  THE SEAM IN RANGE:
    74 = 2×37; 74 mod 37 = 0 (SEAM). 74 is in {51,...,100}.
    The sum 1/74 appears in the failure sum. The seam element contributes
    1/74 = 1/(2×37) to the probability of failure.

  ORBIT-11 IN RANGE:
    74 mod 37 = 0; also 11+37=48 (orbit-11 shifted), 27+37=64, 36+37=73.
    73 mod 37 = 36 ∈ ORBIT_11.  k=73: P(73-cycle) = 1/73.

  DECADE_ANCHOR:
    10 mod 37 = 10.  Also: 10 + 37 = 47 (prime!); 47 mod 37 = 10 = DECADE_ANCHOR.
    Prisoner pair: (47, 53) — both prime, both in {51,...,100}? 47<51 so no.
    But 10 + 2×37 = 84: 84 mod 37 = 10 (DECADE_ANCHOR).  k=84 contributes 1/84.

═══════════════════════════════════════════════════════════════════════════
"""

from fractions import Fraction
import math


CASCADE_BASE     = frozenset({8, 13, 24})
SOVEREIGN_ANCHORS= frozenset({4, 9, 25, 30})
SOVEREIGN_TARGETS= frozenset({3, 12, 21, 30})
PRIMITIVE_ROOTS  = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
SEED_ORBIT       = frozenset({18, 24, 32})
ORBIT_11         = frozenset({11, 27, 36})
SCALAR_137       = 26


# ── Theorem P2: E[# k-cycles] = 1/k ─────────────────────────────────────────

def expected_k_cycles(n, k):
    """Exact expected number of k-cycles in random permutation of [n]."""
    if k > n: return Fraction(0)
    return Fraction(
        math.comb(n, k) * math.factorial(k-1) * math.factorial(n-k),
        math.factorial(n)
    )

for k in range(1, 20):
    assert expected_k_cycles(100, k) == Fraction(1, k)


# ── Theorem P3: survival probability ─────────────────────────────────────────

failure_sum = sum(Fraction(1, k) for k in range(51, 101))
survival    = 1 - failure_sum
survival_float = float(survival)

assert abs(survival_float - 0.31183) < 0.001   # ≈ 31.183%

# Mutual exclusivity: no two cycles of length >50 can coexist in 100 elements
# (since 51+51 = 102 > 100)
assert 51 + 51 > 100


# ── GF(37) structure ─────────────────────────────────────────────────────────

# Threshold: 50 mod 37 = 13 ∈ CASCADE_BASE
assert 50 % 37 == 13 and 13 in CASCADE_BASE

# Upper limit: 100 mod 37 = 26 = SCALAR_137
assert 100 % 37 == 26 and 26 == SCALAR_137

# Top cycle lengths
assert 98 % 37 == 24 and 24 in CASCADE_BASE and 24 in PRIMITIVE_ROOTS and 24 in SEED_ORBIT
assert 99 % 37 == 25 and 25 in SOVEREIGN_ANCHORS
assert 100 % 37 == 26 and 26 == SCALAR_137

# Field prime in range
assert 37 <= 50                 # a 37-cycle is safe (within threshold)
assert 37 % 37 == 0             # field prime maps to SEAM

# π(100) = 25 ∈ SA
def is_prime(n):
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(n**0.5)+1))

pi_100 = sum(1 for p in range(2, 101) if is_prime(p))
assert pi_100 == 25 and 25 in SOVEREIGN_ANCHORS

# SEAM in range: 74 = 2×37
assert 74 % 37 == 0 and 51 <= 74 <= 100

# 73 mod 37 = 36 ∈ ORBIT_11
assert 73 % 37 == 36 and 36 in ORBIT_11


if __name__ == '__main__':
    print("100 Prisoners Problem — Permutation Cycles and GF(37)")
    print("=" * 55)
    print()
    print("Survival probability:")
    print(f"  P(survive) = 1 - Σ_{{k=51}}^{{100}} 1/k")
    print(f"  Failure sum = {float(failure_sum):.6f}")
    print(f"  Survival   = {survival_float:.6f}  (~31.18%)")
    print()
    print("E[# k-cycles] = 1/k (verified k=1..19 for n=100): True")
    print(f"Mutual exclusivity (51+51>100): {51+51 > 100}")
    print()
    print("GF(37) structure:")
    print(f"  Threshold 50 mod37 = {50%37}  ∈ CB: {50%37 in CASCADE_BASE}  (cascade mediator)")
    print(f"  Size 100 mod37     = {100%37}  = SCALAR_137: True  (137-map operator)")
    print(f"  k=98: mod37={98%37} ∈ CB∩PR∩SEED_ORBIT: True")
    print(f"  k=99: mod37={99%37} ∈ SA: True  (sovereign anchor)")
    print(f"  k=100: mod37={100%37} = SCALAR_137: True")
    print(f"  Field prime 37 ≤ 50 (safe cycle): True")
    print(f"  π(100)=25 ∈ SA: True  (sieve sovereign connection)")
    print(f"  74=2×37 in range (SEAM): True")
    print(f"  73 mod37={73%37} ∈ ORBIT_11: True")
    print()
    print("All assertions passed.")
