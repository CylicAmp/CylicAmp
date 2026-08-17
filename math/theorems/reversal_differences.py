# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 234: Reversal Differences -- 198=18×11 and the {594,396} Pair
================================================================================

USER NOTATION:
  123-321
  456-654
  789-987

  137-731
  246-642
  589-985

  125-137-149
  ----12---12

STRUCTURE:

A. THE 198 FAMILY (digit-block reversals):
  321-123 = 198
  654-456 = 198
  987-789 = 198
  All three consecutive-digit-block pairs give the same difference: 198.
  DR(198) = 9.  198 mod 37 = 13 in C_4 = {5,13,19} (prime seed coset).
  198 = 18 × 11 = seed_orbit_element × R_2.
  The reversal constant factors as seed orbit × repunit.

B. THE {594, 396} PAIR (3-digit reversals):
  731-137 = 594  DR=9  594 mod 37 = 2  (first prime, gap)
  642-246 = 396  DR=9  396 mod 37 = 26 in H_SET (sovereign kernel)
  985-589 = 396  DR=9  396 mod 37 = 26 in H_SET

  137 mod 37 = 26 in H  ->  731 mod 37 = 28
  246 mod 37 = 24 in seed orbit  ->  642 mod 37 = 13 in C_4
  589 mod 37 = 34  ->  985 mod 37 = 23

  The two distinct differences: 594 and 396.
  594 + 396 = 990 = 10 × 99 = 10 × 9 × 11.  [10 in H, 9 in SA, 11 = R_2]
  396 = 4 × 99 = 4 × 9 × 11 = SA_element × 9 × R_2.
  594 = 6 × 99 = 6 × 9 × 11 = imaginary_unit × 9 × R_2.

  594 mod 37 = 2.  396 mod 37 = 26 in H.
  2 × 26 = 52 mod 37 = 15.  DR(15) = 6 = imaginary unit.
  The product of the two difference residues DR-reduces to the imaginary unit.

C. AP {125, 137, 149} WITH STEP 12:
  125, 137, 149: common difference 12 (the coset count of H in GF(37)*).
  137 mod 37 = 26 in H.
  149 mod 37 = 1 in H.
  Two of three terms of the AP land in H.
  125 mod 37 = 14 (not in a sovereign set).
  The AP has step 12 = |GF(37)*:H|; the step itself is the coset count.

AP {123, 147, 159} WITH HALVING STEPS:
  123 mod 37 = 12 in ST.
  147 mod 37 = 36 = -1 (antipode).
  159 mod 37 = 11 in C_8 = {11, 27, 36}.
  Differences: 147-123 = 24 in seed orbit; 159-147 = 12 in ST.
  The step halves: 24 -> 12. Both steps are sovereign (seed orbit, then ST).
  147 is at the -1 pivot: the AP passes through -1.
================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H_SET = {1, 10, 26}
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED_ORBIT = {18, 24, 32}


def dr(n):
    n = abs(n)
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def build_cosets():
    used, cosets = set(), []
    for g in range(1, P):
        if g in used:
            continue
        c = sorted((g * h) % P for h in H_SET)
        for x in c:
            used.add(x)
        cosets.append(c)
    return cosets


def coset_of(x, cosets):
    r = x % P
    for i, c in enumerate(cosets):
        if r in c:
            return i + 1, c
    return None, None


def run():
    print("=" * 70)
    print("THEOREM 234: REVERSAL DIFFERENCES -- 198=18x11 AND THE {594,396} PAIR")
    print("=" * 70)

    cosets = build_cosets()

    # A: The 198 family
    print("\nA. THE 198 FAMILY (digit-block reversals):")
    pairs_198 = [(123, 321), (456, 654), (789, 987)]
    for a, b in pairs_198:
        d = b - a
        ci, c = coset_of(d, cosets)
        print(f"  {b}-{a} = {d}  DR={dr(d)}  mod{P}={d%P}  C_{ci}={c}")
    d = 198
    assert all(b-a == d for a,b in pairs_198)
    assert dr(d) == 9 and d % P == 13 and 13 in {5,13,19}
    print(f"  All differences = {d}")
    print(f"  {d} = 18x11 = {18*11}  [18 in seed orbit, 11=R_2]  check")
    assert d == 18 * 11 and 18 in SEED_ORBIT
    print(f"  {d} mod {P} = {d%P}  in C_4 (prime seed coset {{5,13,19}})  check")

    # B: The {594, 396} pair
    print(f"\nB. THE {{594,396}} PAIR (3-digit reversals):")
    pairs_big = [(137, 731), (246, 642), (589, 985)]
    diffs = []
    for a, b in pairs_big:
        d = abs(b - a)
        diffs.append(d)
        ri_a, ri_b = a % P, b % P
        ci_a, c_a = coset_of(a, cosets)
        flags_a = []
        if ri_a in H_SET:      flags_a.append("H")
        if ri_a in SA:         flags_a.append("SA")
        if ri_a in SEED_ORBIT: flags_a.append("seed")
        flags_b = []
        if ri_b in H_SET:      flags_b.append("H")
        if ri_b in SA:         flags_b.append("SA")
        if ri_b in SEED_ORBIT: flags_b.append("seed")
        print(f"  {a}(mod37={ri_a} [{','.join(flags_a) or '-'}])  "
              f"{b}(mod37={ri_b} [{','.join(flags_b) or '-'}])  "
              f"diff={d}  DR={dr(d)}  mod37={d%P}")

    assert diffs == [594, 396, 396]
    d1, d2 = 594, 396
    print(f"\n  Distinct differences: {d1} and {d2}")
    print(f"  {d1} + {d2} = {d1+d2} = 10 x 99 = 10x9x11  [H x SA x R_2]")
    assert d1 + d2 == 990 == 10 * 9 * 11
    print(f"  {d2} = 4 x 99 = 4x9x11  [SA_elem x SA x R_2]")
    assert d2 == 4 * 99
    print(f"  {d1} = 6 x 99 = 6x9x11  [imaginary_unit x SA x R_2]")
    assert d1 == 6 * 99
    r1, r2 = d1 % P, d2 % P
    print(f"  {d1} mod {P} = {r1}  (first prime/gap)")
    print(f"  {d2} mod {P} = {r2}  in H: {r2 in H_SET}")
    assert r2 in H_SET
    prod_r = (r1 * r2) % P
    print(f"  {r1} x {r2} = {r1*r2} = {prod_r} (mod {P})  DR({prod_r}) = {dr(prod_r)} = imaginary unit  check")
    assert dr(prod_r) == 6

    # C: AP {125, 137, 149} step=12
    print(f"\nC. AP {{125, 137, 149}} WITH STEP 12:")
    ap1 = [125, 137, 149]
    for x in ap1:
        r = x % P
        flags = []
        if r in H_SET:      flags.append("H")
        if r in SA:         flags.append("SA")
        if r in ST:         flags.append("ST")
        if r in SEED_ORBIT: flags.append("seed")
        if r == P-1:        flags.append("-1")
        print(f"  {x} mod {P} = {r:2d}  [{','.join(flags) or '-'}]")
    assert ap1[1]-ap1[0] == 12 and ap1[2]-ap1[1] == 12
    assert 137%P in H_SET and 149%P in H_SET
    print(f"  Step = 12 = coset count of H in GF({P})*  check")
    print(f"  137 mod {P} = {137%P} in H; 149 mod {P} = {149%P} in H  check")

    # AP {123, 147, 159} with halving steps
    print(f"\nAP {{123, 147, 159}} WITH HALVING STEPS:")
    ap2 = [123, 147, 159]
    for x in ap2:
        r = x % P
        flags = []
        if r in H_SET:      flags.append("H")
        if r in SA:         flags.append("SA")
        if r in ST:         flags.append("ST")
        if r in SEED_ORBIT: flags.append("seed")
        if r == P-1:        flags.append("-1=antipode")
        if r in {11,27,36}: flags.append("C_8")
        print(f"  {x} mod {P} = {r:2d}  [{','.join(flags) or '-'}]")
    d1_2, d2_2 = ap2[1]-ap2[0], ap2[2]-ap2[1]
    print(f"  Steps: {d1_2} (seed orbit), {d2_2} (ST)  -- step halves")
    assert d1_2 == 24 and d2_2 == 12
    assert 24 in SEED_ORBIT and 12 in ST
    assert 147%P == P-1
    print(f"  147 mod {P} = {147%P} = -1 (antipode): the AP passes through -1  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
