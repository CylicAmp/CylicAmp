# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 233: The (1)+n DR Addition Table -- Self-Feeding Chain {2,5,6,8}
================================================================================

USER NOTATION:
  (1)+0=(1)
  (1)+1=(2)
  (1)+11=(3)

  (1)+3=(4)+2=(6)
  (1)+4=(5)+6=(2)
  (1)+5=(6)+2=(8)
  (1)+6=(7)+8=(6)
  (1)+7=(8)+6=(5)
  (1)+8=(9)+5=(5)

STRUCTURE:
  (n) denotes DR(n). Each row has two steps:
    Step 1: DR(1+n) = first intermediate
    Step 2: DR(first_intermediate + m) = final result

  The second operand m of row n equals the final result of row n-1.
  The chain is self-feeding: each output becomes the next row's second input.

SELF-FEEDING SEQUENCE:
  Seed: m=2 for n=3 (the twin prime gap, first prime)
  n=3: DR(4)+2=DR(6)=6=imaginary unit      -> m=6 for n=4
  n=4: DR(5)+6=DR(11)=2=gap               -> m=2 for n=5
  n=5: DR(6)+2=DR(8)=8=DR(lower_twin)     -> m=8 for n=6
  n=6: DR(7)+8=DR(15)=6=imaginary unit    -> m=6 for n=7
  n=7: DR(8)+6=DR(14)=5=prime_seed        -> m=5 for n=8
  n=8: DR(9)+5=DR(14)=5=prime_seed

  The second operands cycle through {2, 6, 2, 8, 6, 5} -- all drawn from
  the canonical set {2, 5, 6, 8} = {gap, prime_seed, imaginary_unit, DR(17)}.

THE REPUNIT ENTRY (1)+11=(3):
  1+11 = 12. DR(12) = 3.
  11 = R_2 (the 2-digit repunit).
  DR(12) = 3 in ST (sovereign target).
  Adding R_2 to 1 jumps directly to ST without a second step.
  Compare: (1)+3=(4): adding 3 to 1 gives 4 in SA, requiring a second step to reach 6.
  The repunit short-circuits to ST in one step.

CHAIN ANATOMY:
  First intermediates: 4(SA), 5(C_4), 6(imag), 7(C_6), 8, 9(SA)
  Final results:       6(imag), 2(gap), 8(DR17), 6(imag), 5(seed), 5(seed)
  The system lands on {2,5,6,8} and cannot escape them.

  Row n=3 first intermediate 4 is in SA.
  Row n=8 first intermediate 9 is in SA.
  Both SA entries produce 5 (prime seed) as ultimate result: 4+2=6->imag, but 9+5=14->5.
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
CANONICAL = {2, 5, 6, 8}


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
    print("THEOREM 233: (1)+n DR ADDITION TABLE -- SELF-FEEDING CHAIN {2,5,6,8}")
    print("=" * 70)

    cosets = build_cosets()

    # Single-step rows
    print("\nSINGLE-STEP ROWS:")
    for n in [0, 1, 11]:
        r = 1 + n
        dr_r = dr(r)
        ci, c = coset_of(r, cosets)
        flags = []
        if r % P in H_SET:     flags.append("H")
        if r % P in SA:        flags.append("SA")
        if r % P in ST:        flags.append("ST")
        if r == 12:            flags.append(f"12=R_2+1=coset_count")
        flag_str = "  [" + ",".join(flags) + "]" if flags else ""
        print(f"  (1)+{n:2d} = ({dr_r})   [{r}]{flag_str}")

    assert dr(1+0) == 1
    assert dr(1+1) == 2
    assert dr(1+11) == 3 and 3 in ST
    print(f"  (1)+11=(3): 1+11=12, DR(12)=3 in ST  [R_2 short-circuits to ST]  check")

    # Two-step rows: the self-feeding chain
    print(f"\nTWO-STEP SELF-FEEDING CHAIN:")
    print(f"  {'n':>2}  step1  DR1  m   step2  DR2   flags")
    print("  " + "-"*50)

    second_ops = {3: 2, 4: 6, 5: 2, 6: 8, 7: 6, 8: 5}
    results = {}

    for n in range(3, 9):
        m = second_ops[n]
        step1 = 1 + n
        dr1 = dr(step1)
        step2 = step1 + m
        dr2 = dr(step2)
        results[n] = dr2

        flags = []
        if dr1 in SA:       flags.append(f"DR1:{dr1}=SA")
        if dr1 == 6:        flags.append("DR1=imag")
        if dr2 == 6:        flags.append("DR2=imag")
        if dr2 == 2:        flags.append("DR2=gap")
        if dr2 == 5:        flags.append("DR2=seed")
        if dr2 == 8:        flags.append("DR2=DR(17)")

        print(f"  n={n}  {step1:5d}  {dr1:3d}  {m:2d}  {step2:5d}  {dr2:3d}   {', '.join(flags)}")

    # Verify self-feeding property
    print(f"\nSELF-FEEDING VERIFICATION:")
    print(f"  (output of row n) == (second operand of row n+1):")
    for n in range(3, 8):
        out = results[n]
        next_m = second_ops[n+1]
        match = out == next_m
        print(f"  results[{n}]={out} == second_ops[{n+1}]={next_m}: {match}  {'check' if match else 'FAIL'}")
        assert match, f"Self-feeding broken at n={n}"

    # The canonical set
    all_results = set(results.values())
    all_m = set(second_ops.values())
    print(f"\nCANONICAL SET {{2,5,6,8}}:")
    print(f"  All second operands: {sorted(all_m)}")
    print(f"  All final results:   {sorted(all_results)}")
    assert all_m == CANONICAL and all_results == CANONICAL
    print(f"  Both sets = {{2,5,6,8}}  check")
    print(f"  2 = twin prime gap = first prime")
    print(f"  5 = prime seed (C_4)")
    print(f"  6 = imaginary unit of GF(37) (6^2=-1 mod 37)")
    print(f"  8 = DR(17) = DR(lower twin prime)")

    # Connection to (1)3813(3)9487(2) — encoded DRs
    print(f"\n(1)3813(3)9487(2) ENCODING:")
    val_a, val_b = 3813, 9487
    print(f"  Markers: (1) before {val_a}, (3) before {val_b}, (2) at end")
    print(f"  DR({val_a}) = {dr(val_a)}  [digit sum = {sum(int(d) for d in str(val_a))}]")
    print(f"  DR({val_b}) = {dr(val_b)}  [digit sum = {sum(int(d) for d in str(val_b))}]")
    print(f"  Framing DRs: (1), (3), (2) = identity, ST-member, gap")
    print(f"  {val_a} mod 37 = {val_a % P}")
    print(f"  {val_b} mod 37 = {val_b % P}")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
