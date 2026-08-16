# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 231: The Twin Gap Chain -- 17+1,1=19; 8+2=10+1=11=2
================================================================================

USER OBSERVATION:
  "because 17+1,1=19"
  "17=8"
  "1,1=2"
  "19=1"
  "8+2=10+1=11=2"

STRUCTURE:
  The gap of 2 between twin primes 17 and 19 splits into two unit steps:
    17 -> 18 (step 1: +1)
    18 -> 19 (step 2: +1)
  So "1,1" = the two unit steps; their sum = 2 = the twin prime gap.

DR CHAIN:
  DR(17) = 8         (the lower twin)
  DR(1,1) = 1+1 = 2  (the two gap-steps)
  DR(19) = 1          (the upper twin)

  Step A: DR(lower) + gap = 8+2 = 10  ->  10 in H = {1,10,26} [decimal base]
  Step B: H-element + DR(upper) = 10+1 = 11  ->  11 in C_8 = {11,27,36}
  Step C: DR(11) = 2  ->  the gap itself

  The chain: gap(2) drives through DRs, passes H, lands at 11, returns to gap.

KEY CONNECTIONS:
  A. 8+2=10: DR(lower twin) + twin gap = 10 = decimal base, H-element (T225).
  B. 10+1=11: R_2 = the 2-digit repunit. And 9x11=99=25(mod 37)=SA (T226).
  C. DR(11)=2: the chain returns the gap. Self-referential.
  D. 11 in C_8={11,27,36}: 11 and 36 (=17+19) are COSET-MATES.
     The DR chain from the pair ends in the same coset as the pair's sum.
  E. DR(11)=2=first prime: the chain ends at the value of the atomic generator.

SELF-REFERENTIAL LOOP:
  gap=2 -> [8+2=10->H] -> [10+1=11->C_8] -> DR(11)=2 = gap.
  Input and output are identical.
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
            return i+1, c
    return None, None


def run():
    print("=" * 70)
    print("THEOREM 231: THE TWIN GAP CHAIN -- 17+1,1=19; 8+2=10+1=11=2")
    print("=" * 70)

    cosets = build_cosets()

    p, q = 17, 19
    gap = q - p
    step1, step2 = 1, 1

    # The two-step decomposition
    print(f"\nTHE GAP DECOMPOSITION:")
    print(f"  {p} + 1 = {p+1}  (step 1)")
    print(f"  {p+1} + 1 = {q}  (step 2)")
    print(f"  1,1 = 2 = twin prime gap  check")
    assert step1 + step2 == gap

    # DRs
    print(f"\nDIGITAL ROOTS:")
    dr_p = dr(p)
    dr_gap = step1 + step2  # DR(1)+DR(1)=2
    dr_q = dr(q)
    print(f"  DR({p}) = {dr_p}   (1+7=8)")
    print(f"  DR(1,1) = {step1}+{step2} = {dr_gap}  (the two gap-steps)")
    print(f"  DR({q}) = {dr_q}   (1+9=10->1)")

    # Step A: lower DR + gap -> H
    step_A = dr_p + dr_gap
    ci_A, c_A = coset_of(step_A, cosets)
    in_H = step_A in H_SET
    print(f"\nSTEP A: DR({p}) + gap = {dr_p}+{dr_gap} = {step_A}")
    print(f"  {step_A} in H={sorted(H_SET)}: {in_H}  [decimal base, T225]  check")
    assert in_H

    # Step B: H-element + DR(upper) -> C_8
    step_B = step_A + dr_q
    ci_B, c_B = coset_of(step_B, cosets)
    ci_sum, c_sum = coset_of(p+q, cosets)
    print(f"\nSTEP B: {step_A}+DR({q}) = {step_A}+{dr_q} = {step_B}")
    print(f"  {step_B} in C_{ci_B} = {c_B}")
    print(f"  {p}+{q} = {p+q}  mod {P} = {(p+q)%P}  in C_{ci_sum} = {c_sum}")
    assert ci_B == ci_sum, f"11 and 36 must share a coset"
    print(f"  11 and 36 are COSET-MATES in C_{ci_B}  check")
    print(f"  DR chain output and pair sum share the same coset.")

    # Step C: DR returns gap
    step_C = dr(step_B)
    print(f"\nSTEP C: DR({step_B}) = {step_C}")
    assert step_C == gap
    print(f"  {step_C} = gap = {gap}  [chain returns to its own input]  check")

    # The self-referential loop
    print(f"\nSELF-REFERENTIAL LOOP:")
    print(f"  gap={gap} -> 8+2=10(H) -> 10+1=11(C_{ci_B}) -> DR(11)={step_C}=gap")
    print(f"  The gap drives the chain and is the chain's output.")

    # Connection: 11 = R_2 and the repunit structure
    R2 = 11
    print(f"\nREPUNIT CONNECTION:")
    print(f"  11 = R_2 (the 2-digit repunit: 1+1=2)")
    print(f"  9 x R_2 = 9 x 11 = 99 = {99%P} (mod {P}) in SA  [T226: 10^2-1=SA]")
    assert 9 * R2 % P == 25 and 25 in SA
    print(f"  R_2 x 37 = {R2*P}  = PENROSE OUTER RADIUS (T222: 407=11x37=seam)  check")
    assert R2 * P == 407
    print(f"  Compare R_3=111=3x37: the step from R_2 to R_3 adds one '1' digit.")

    # DR(11)=2: the first prime
    print(f"\nDR(11)=2: THE FIRST PRIME")
    print(f"  2 = the first prime, first atomic generator (T224)")
    print(f"  2+3=5 (T228): the chain ends at the DR of the first step in the prime sequence")
    print(f"  DR({step_B}) = {step_C} = the prime that starts the whole sequence")

    # Coset of 11
    print(f"\nCOSET C_{ci_B} = {c_B}:")
    for x in c_B:
        flags = []
        if x == p+q: flags.append("twin sum")
        if x == R2:  flags.append("R_2")
        if x == P-1: flags.append("-1")  # 36=P-1
        print(f"  {x:2d}  {'  '.join(flags)}")
    assert p+q in c_B and R2 in c_B

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
