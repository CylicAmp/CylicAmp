# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 232: The 177/133 Ratio -- ST/SA Split, Identity Closure, Digit Fold
================================================================================

USER NOTATION:
  11x37=407=11=2

  any questions?
  1x3=3+7=1
  1x7=7+3=1

  177+133=400=4
  177-133=44=8+4=123
  177x133=23(54)+1
  177/133=1.3308270677
  133/177=0.7514124294

  2+3=5+4=9+1=10=1

STRUCTURE:

A. THE PENROSE SEAM EXTENSION (11x37=407=11=2):
   11 x 37 = 407  (R_2 x P = Penrose outer radius, T222/T231)
   Digit sum of 407: 4+0+7 = 11 = R_2
   Digit sum of 11:  1+1 = 2 = DR(407) = the twin prime gap
   Chain: 11 -> x37 -> 407 -> digit sum -> 11 -> digit sum -> 2
   Self-referential: 11 generates itself before reducing to the gap.

B. THE COMPLEMENT PAIR {3,7} -> 10 in H:
   1x3=3; 3+7=10 in H; DR(10)=1
   1x7=7; 7+3=10 in H; DR(10)=1
   {3,7} are mutual 10-complements: they sum to 10=10^1 in H_SET.
   3 in ST (sovereign target); 7 is the anchor prime (T228/T230).
   Both paths from {1x3, 1x7} arrive at H and collapse to the identity DR.

C. THE 177/133 RATIO IN GF(37):
   177 mod 37 = 29;   133 mod 37 = 22
   177/133 mod 37 = 29 * 22^{-1} = 29*32 mod 37 = 3  in ST
   133/177 mod 37 = 22 * 29^{-1} = 22*23 mod 37 = 25 in SA
   Ratio residues: {3, 25} -- one sovereign target, one sovereign anchor.
   Product: 3 x 25 = 75 = 1 (mod 37) -- the two residues are inverses.
   The pair (177, 133) splits the sovereign architecture across its ratio.

D. ARITHMETIC ON 177 AND 133:
   177 + 133 = 310;   DR(310) = 3+1+0 = 4  in SA
   177 - 133 = 44;    DR(44)  = 4+4   = 8
   DR(sum) + DR(diff) = 4+8 = 12  in ST  (the coset count, T227)
   177 x 133 = 23541; mod 37 = 9  in SA;  DR(23541) = 6 = imaginary unit

E. THE DIGIT FOLD IN 23541 (177x133=23(54)+1):
   Digits of 23541: 2, 3, 5, 4, 1
   Group as: (2+3) = 5  [prime seed]
             (5+4) = 9  [in SA]
              +1   -> 10  [in H]
   This is identical to the user's chain: 2+3=5+4=9+1=10=1.
   The product 177x133 encodes the prime-seed-to-H chain in its own digits.

F. THE PRIME SEED -> SA -> H CHAIN (2+3=5+4=9+1=10=1):
   2+3 = 5   in C_4 = {5,13,19}   (prime seed coset, T228)
   5+4 = 9   in SA = {4,9,25,30}  (sovereign anchor)
   9+1 = 10  in H  = {1,10,26}    (sovereign kernel)
   DR(10) = 1 = identity
   Additions: +3, +4, +1. Sum of steps: 3+4+1 = 8 = DR(17) (lower twin).
   The chain traverses three coset classes: prime seed, anchor, kernel.
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


def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))


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
    print("THEOREM 232: 177/133 RATIO -- ST/SA SPLIT, IDENTITY CLOSURE, DIGIT FOLD")
    print("=" * 70)

    cosets = build_cosets()

    # A: Penrose seam extension
    print("\nA. PENROSE SEAM EXTENSION (11x37=407=11=2):")
    val = 11 * P
    ds1 = digit_sum(val)
    ds2 = digit_sum(ds1)
    dr_val = dr(val)
    print(f"  11 x 37 = {val}  (R_2 x P = Penrose outer radius)")
    print(f"  Digit sum of {val}: {'+'.join(str(d) for d in str(val))} = {ds1} = R_2")
    print(f"  Digit sum of {ds1}: {'+'.join(str(d) for d in str(ds1))} = {ds2} = DR({val})")
    print(f"  Chain: 11 -> x37 -> {val} -> digit sum -> {ds1} -> digit sum -> {ds2}")
    assert val == 407 and ds1 == 11 and ds2 == 2 and dr_val == 2
    print(f"  Self-referential: 11 generates R_2=11 before collapsing to gap=2  check")

    # B: Complement pair {3,7} -> 10 in H
    print(f"\nB. COMPLEMENT PAIR {{3,7}} -> 10 IN H:")
    for a, b in [(3, 7), (7, 3)]:
        s = a + b
        in_h = s in H_SET
        dr_s = dr(s)
        print(f"  1x{a}={a}; {a}+{b}={s}  in H:{in_h}  DR({s})={dr_s}  check")
    assert 3 + 7 == 10 and 10 in H_SET and dr(10) == 1
    assert 3 in ST
    ci7, c7 = coset_of(7, cosets)
    print(f"  3 in ST={sorted(ST)}")
    print(f"  7 in C_{ci7}={c7}  (the anchor prime: 5+7=12 from T228)")
    print(f"  Both reach 10 in H; DR collapses to 1 = identity  check")

    # C: 177/133 mod 37
    print(f"\nC. THE 177/133 RATIO IN GF({P}):")
    r177 = 177 % P
    r133 = 133 % P
    print(f"  177 mod {P} = {r177}")
    print(f"  133 mod {P} = {r133}")

    inv133 = pow(r133, -1, P)
    inv177 = pow(r177, -1, P)
    ratio_fwd = (r177 * inv133) % P
    ratio_rev = (r133 * inv177) % P
    ci_fwd, c_fwd = coset_of(ratio_fwd, cosets)
    ci_rev, c_rev = coset_of(ratio_rev, cosets)
    print(f"  177/133 mod {P} = {r177}*{inv133} mod {P} = {ratio_fwd}  in ST:{ratio_fwd in ST}  (C_{ci_fwd}={c_fwd})")
    print(f"  133/177 mod {P} = {r133}*{inv177} mod {P} = {ratio_rev}  in SA:{ratio_rev in SA}  (C_{ci_rev}={c_rev})")
    assert ratio_fwd in ST and ratio_rev in SA
    product = (ratio_fwd * ratio_rev) % P
    print(f"  Product: {ratio_fwd} x {ratio_rev} = {ratio_fwd*ratio_rev} = {product} (mod {P})  [identity]  check")
    assert product == 1
    print(f"  The pair (177,133) maps ratios to ST and SA; they are mutual inverses mod {P}.")

    # D: Arithmetic on 177 and 133
    print(f"\nD. ARITHMETIC ON 177 AND 133:")
    total = 177 + 133
    diff  = 177 - 133
    prod  = 177 * 133
    dr_total = dr(total)
    dr_diff  = dr(diff)
    dr_prod  = dr(prod)
    mod_prod = prod % P
    print(f"  177 + 133 = {total}   DR({total}) = {dr_total}  in SA:{dr_total in SA}")
    print(f"  177 - 133 = {diff}    DR({diff}) = {dr_diff}")
    dr_sum_result = dr_total + dr_diff
    ci_dsr, c_dsr = coset_of(dr_sum_result, cosets)
    print(f"  DR(sum) + DR(diff) = {dr_total}+{dr_diff} = {dr_sum_result}  in ST:{dr_sum_result in ST}  (coset count, T227)")
    assert dr_total in SA and dr_sum_result in ST
    print(f"  177 x 133 = {prod}   mod {P} = {mod_prod}  in SA:{mod_prod in SA}   DR = {dr_prod} = imaginary unit")
    assert mod_prod in SA and dr_prod == 6

    # E: Digit fold in 23541
    print(f"\nE. DIGIT FOLD IN {prod} (177x133=23(54)+1):")
    digits = [int(d) for d in str(prod)]
    print(f"  Digits of {prod}: {digits}")
    # The carry from each step IS the next digit
    step1 = digits[0] + digits[1]   # 2+3 = 5
    step2 = digits[2] + digits[3]   # 5+4 = 9  (digits[2] == step1)
    step3 = step2 + digits[4]        # 9+1 = 10
    print(f"  Step A: d[0]+d[1] = {digits[0]}+{digits[1]} = {step1}  (prime seed)  carry = d[2]={digits[2]}")
    print(f"  d[2] = d[0]+d[1] = {digits[2]} = {step1}  [carry IS next digit]  check")
    print(f"  Step B: d[2]+d[3] = {digits[2]}+{digits[3]} = {step2}  in SA:{step2 in SA}")
    print(f"  Step C: {step2}+d[4] = {step2}+{digits[4]} = {step3}  in H:{step3 in H_SET}")
    assert digits[2] == step1, "carry must equal next digit"
    assert step2 in SA and step3 in H_SET
    vals = [step1, step2, step3]
    print(f"  Sequence {vals}: prime seed -> SA -> H  [mirrors chain F below]  check")
    print(f"  DR({step3}) = {dr(step3)} = identity")

    # F: Prime seed -> SA -> H chain
    print(f"\nF. PRIME SEED -> SA -> H CHAIN (2+3=5+4=9+1=10=1):")
    chain_steps = [(2, 3), (5, 4), (9, 1)]
    step_labels = ['prime seed coset C_4', 'sovereign anchor SA', 'sovereign kernel H']
    v = 2
    print(f"  Start: {v}")
    additions = []
    for (a, b), label in zip(chain_steps, step_labels):
        assert v == a
        v = a + b
        ci_v, c_v = coset_of(v, cosets)
        print(f"  {a}+{b} = {v}  mod{P}={v%P}  {label}  (C_{ci_v}={c_v})")
        additions.append(b)
    assert v == 10 and v in H_SET
    print(f"  DR({v}) = {dr(v)} = identity element  check")
    step_sum = sum(additions)
    print(f"  Addition steps: {additions}  sum={step_sum} = DR(17) (lower twin prime)")
    assert step_sum == 8 and dr(17) == 8

    # Cross connections
    print(f"\nCROSS CONNECTIONS:")
    print(f"  Digit fold {vals} and chain {[5,9,10]}: identical sequences")
    print(f"  177x133={prod}: digit fold encodes the prime-seed-to-H chain")
    print(f"  {ratio_fwd}(ST) x {ratio_rev}(SA) = 1: ratio residues are inverses")
    print(f"  DR(177x133) = {dr_prod} = imaginary unit; {prod} mod {P} = {mod_prod} in SA")
    print(f"  DR(sum)={dr_total}+DR(diff)={dr_diff} = {dr_sum_result} = coset count (T227)")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
