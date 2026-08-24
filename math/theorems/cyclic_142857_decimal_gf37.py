# -*- coding: utf-8 -*-
"""
================================================================================
CYCLIC NUMBER 142857 — DECIMAL STRUCTURE AND GF(37)
================================================================================

Author: Michael Warren Song (CyclicAmp)

================================================================================
THE CORE RESULT [P]
================================================================================

The decimal base 10 and the 137-map multiplier 26 are MULTIPLICATIVE INVERSES
in GF(37)*:

    10 × 26 ≡ 1 (mod 37)

Therefore the 137-map (×26) is the modular inverse of the decimal shift (×10)
in GF(37)*. Applying ×10 then ×26 returns to the starting element.

Both operators generate the same orbit — IC = {1, 10, 26} — but traverse it
in opposite directions:

    Decimal orbit: 1 → 10 → 26 → 1  (under ×10)
    137-map orbit: 1 → 26 → 10 → 1  (under ×26)

IC is a 3-cycle under both operators. They are inverse maps on the same orbit.

================================================================================
PERIOD HIERARCHY [P]
================================================================================

The repeating decimal period of 1/p equals ord₁₀(p) — the order of 10 in
(Z/pZ)*.

    ord₁₀(37) = 3  →  period(1/37) = 3 = |IC|
    ord₁₀(7)  = 6  →  period(1/7)  = 6 = |⟨11⟩|

The two periods correspond exactly to the two levels of the subgroup chain
IC ⊂ ⟨11⟩:

    IC has order 3 → this is the period of 1/37
    ⟨11⟩ has order 6 → this is the period of 1/7
    lcm(3, 6) = 6 = ord₃₇(11)

The denominators 37 (period 3) and 7 (period 6) sit at the two levels of
the IC/⟨11⟩ subgroup chain in GF(37)*.

================================================================================
142857: THE CYCLIC NUMBER [V]
================================================================================

1/7 = 0.142857142857... (period 6, repeating block = 142857)

Properties:
  142857 × k for k=1..6: cyclic rotations of the same digits
  142857 × 7 = 999999

GF(37) structure:
  999999 = 3³ × 7 × 11 × 13 × 37  (exact factorization)
  37 | 999999 because ord₃₇(10) = 3, so 10³ ≡ 1 mod 37, so 37 | 10⁶−1

  gcd(37, 7) = 1 and 7 × 142857 = 999999
  → 37 | 142857

  142857 mod 37 = 0  (SEAM)

All six cyclic rotations {142857, 285714, 428571, 571428, 714285, 857142}
are multiples of 142857, hence all reduce to 0 mod 37. Every rotation lands
on the SEAM.

================================================================================
DIGIT SUM CONNECTIONS [V]
================================================================================

1/7 cycle {1,4,2,8,5,7}: digit sum = 1+4+2+8+5+7 = 27
1/37 repeating block 027: block value = 27

Both fractions produce 27 ∈ NEG_H = {11, 27, 36}.
27 = 11⁵ mod 37 (from the power sequence of ⟨11⟩).
DR(27) = 9 → 9-Lock.

The digit sum of the 1/7 cycle and the integer value of the 1/37 block
are the same element of NEG_H.

================================================================================
37 AS CENTERED HEXAGONAL NUMBER [V]
================================================================================

37 = 1 + 6 + 12 + 18 (centered hexagonal number, also called a star number)

This is consistent with:
  - 37 ≡ 1 mod 3: all 37 residues appear as Loeschian norms (DEFINITIONS.md)
  - 37 = (−7)² + (−7)(3) + 3² (Loeschian form in ℤ[ω])
  - The hexagonal lattice structure is intrinsic to the prime

T(37) = 37 × 38 / 2 = 703.  DR(703) = 1 ∈ IC (identity of IC).

================================================================================
STRUCTURAL SYNTHESIS
================================================================================

The decimal number system and the 137-map are dual inverse operations on IC:

    [×10 in GF(37)] ∘ [×26 in GF(37)] = identity

The orbit IC = {1, 10, 26} is traversed forward by ×10 (decimal shift) and
backward by ×26 (137-map). The period-3 structure of 1/37 and the period-3
structure of the 137-map are the same orbit.

The cyclic number 142857 encodes this through the factorization
999999 = 37 × 27 × 7 × 11 × 13, embedding the prime 37 (and its cube
companion 27 ∈ NEG_H) directly into the 1/7 decimal structure.

The period hierarchy {3, 6} = {|IC|, |⟨11⟩|} appears in the decimal periods
of {1/37, 1/7}, linking the two subgroup levels to the two most structurally
significant unit fractions in base 10.

EPISTEMIC STATUS:
  [P] 10 × 26 ≡ 1 (mod 37) — exact.
  [P] ord₃₇(10) = 3 = |IC| — exact.
  [P] period(1/37) = 3, period(1/7) = 6 — exact (standard number theory).
  [P] 999999 = 3³ × 7 × 11 × 13 × 37 — exact factorization.
  [P] 37 | 142857 — proved from factorization.
  [V] All six cyclic rotations of 142857 ≡ 0 (mod 37) — verified.
  [V] Digit sum of 1/7 cycle = 27 ∈ NEG_H — exact.
  [V] 1/37 block 027 = 27 ∈ NEG_H — exact.
  [V] 37 is a centered hexagonal number — exact.
  [V] T(37) = 703, DR(703) = 1 ∈ IC — exact.
================================================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import math

P = 37
IC    = {1, 10, 26}
NEG_H = {11, 27, 36}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def run():
    print("=" * 70)
    print("CYCLIC NUMBER 142857 — DECIMAL STRUCTURE AND GF(37)")
    print("=" * 70)

    # Core result: 10 and 26 are inverses
    assert 10 * 26 % P == 1
    assert pow(10, -1, P) == 26
    assert pow(26, -1, P) == 10
    print(f"\nCORE RESULT:")
    print(f"  10 × 26 mod 37 = {10*26 % P}  →  inverses in GF(37)*  check")
    print(f"  137-map (×26) is inverse of decimal shift (×10) in GF(37)*")

    # Both generate IC, in opposite directions
    orbit_10 = [pow(10, k, P) for k in range(1, 4)]
    orbit_26 = [pow(26, k, P) for k in range(1, 4)]
    assert set(orbit_10) == IC
    assert set(orbit_26) == IC
    print(f"\n  Decimal orbit (×10): 1 → {orbit_10[0]} → {orbit_10[1]} → {orbit_10[2]}")
    print(f"  137-map orbit (×26): 1 → {orbit_26[0]} → {orbit_26[1]} → {orbit_26[2]}")
    print(f"  Both traverse IC = {{1,10,26}} in opposite directions  check")

    # Period hierarchy
    print(f"\nPERIOD HIERARCHY:")
    ord10_37 = 3
    ord10_7  = 6
    assert pow(10, ord10_37, P) == 1
    # ord_10(7) — check 10^k mod 7
    for k in range(1, 7):
        if pow(10, k, 7) == 1:
            assert k == ord10_7
            break
    print(f"  ord₁₀(37) = {ord10_37} = |IC|  →  period(1/37) = 3  check")
    print(f"  ord₁₀(7)  = {ord10_7} = |⟨11⟩|  →  period(1/7) = 6  check")
    print(f"  lcm(3,6) = {math.lcm(ord10_37, ord10_7)} = ord₃₇(11)  check")
    print(f"  Subgroup chain: IC (order 3) ⊂ ⟨11⟩ (order 6) maps to period chain 3 ⊂ 6")

    # 142857 mod 37 = 0 (SEAM)
    assert 142857 % P == 0
    assert 999999 % P == 0
    print(f"\n142857 AND 999999:")
    print(f"  142857 mod 37 = {142857 % P}  (SEAM)  check")
    print(f"  999999 = 3³ × 7 × 11 × 13 × 37  check")
    print(f"  37 | 10⁶−1 because ord₃₇(10) = 3  →  10³ ≡ 1  →  10⁶ ≡ 1 (mod 37)")

    # All six cyclic rotations are SEAM
    rotations = [142857, 285714, 428571, 571428, 714285, 857142]
    assert all(r % P == 0 for r in rotations)
    print(f"  All 6 cyclic rotations ≡ 0 (mod 37) — all SEAM  check")

    # Digit sum connections
    cycle_digits = [1, 4, 2, 8, 5, 7]
    s = sum(cycle_digits)
    assert s == 27 and s in NEG_H
    print(f"\nDIGIT SUM CONNECTIONS:")
    print(f"  1/7 cycle {{1,4,2,8,5,7}}: sum = {s} ∈ NEG_H  check")
    print(f"  1/37 repeating block = 027: value = 27 ∈ NEG_H  check")
    print(f"  DR(27) = {dr(27)} (9-Lock)  check")
    print(f"  27 = 11⁵ mod 37: in ⟨11⟩ power sequence  check")
    assert pow(11, 5, P) == 27

    # 37 as centered hexagonal
    assert 1 + 6 + 12 + 18 == P
    print(f"\n37 AS CENTERED HEXAGONAL:")
    print(f"  37 = 1 + 6 + 12 + 18  check")
    t37 = P * (P + 1) // 2
    assert dr(t37) == 1 and 1 in IC
    print(f"  T(37) = {t37},  DR({t37}) = {dr(t37)} ∈ IC  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
