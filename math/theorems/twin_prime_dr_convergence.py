# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 230: Twin Prime (17,19) -- DR Convergence to the Imaginary Unit
================================================================================

USER NOTATION (decoded):
  17 19 36
  --2--  17=19=1     gap=2; DR(19) = 1  (1+9=10->1)
  8--1---9=18=9      DR(17)=8, DR(19)=1, 8+1=9=DR(36)=DR(18)
  --7--8=6           unit digit of 17 is 7; DR(17)=8; 7+8=15->DR=6
  9+6=15=6           DR(sum)+imaginary_unit = 15 -> DR=6

STRUCTURE: Every path from (17,19,36) leads to 6.

PATH 1: Digital roots of the pair
  DR(17)=8, DR(19)=1.  8+1=9=DR(36).
  The two primes' DRs are complementary in the 9-system: 8+1=9.

PATH 2: Digits of 17
  17 has tens digit 1, unit digit 7.  1+7=8=DR(17).
  Unit digit alone: 7.  7+8(DR)=15.  1+5=6.
  Unit digit + DR = 15 -> DR = 6 = imaginary unit.

PATH 3: DR of sum + imaginary unit
  DR(36)=9.  9+6=15.  1+5=6.
  The modular residue (9) and the imaginary unit (6) sum to 15->6.

THE FOUR FACES OF 36:
  36 = 17+19          (twin prime pair sum)
  36 = 6 x 6 = 6^2   (square of the imaginary unit, literally)
  36 = 4 x 9          (product of two sovereign anchors: 4,9 in SA)
  36 = -1 (mod 37)    (the antipode of the identity in GF(37)*)
  All four are the same number; the imaginary unit squared IS -1 IS SA x SA.

COMPLEMENTARY DRs:
  DR(17)+DR(19) = 8+1 = 9 = DR modulus.
  This holds for the twin pair (p, p+2) whenever DR(p)+DR(p+2)=9.
  Equivalently: p+2 and p have DRs that are 9-complements.
  For (17,19): 8 and 1 are 9-complements (8+1=9).
  The midpoint 18 has DR(18)=9: the DR of the midpoint = the modulus.

SA PRODUCT:
  SA = {4, 9, 25, 30}.  4 x 9 = 36 = -1 (mod 37).
  The product of the two smallest sovereign anchors = the antipode.
  4 = 2^2 (square of the first prime).
  9 = 3^2 (square of the second prime).
  4 x 9 = (2x3)^2 = 6^2 = 36: product of atomic generators squared.
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


def run():
    print("=" * 70)
    print("THEOREM 230: TWIN PRIME (17,19) -- DR CONVERGENCE TO IMAGINARY UNIT")
    print("=" * 70)

    p, q = 17, 19
    s = p + q
    mid = (p + q) // 2

    # Path 1: DRs of pair
    print(f"\nPATH 1: DIGITAL ROOTS OF THE PAIR")
    dr_p = dr(p)
    dr_q = dr(q)
    dr_s = dr(s)
    dr_m = dr(mid)
    print(f"  DR({p}) = {dr_p}   (1+7 = 8)")
    print(f"  DR({q}) = {dr_q}   (1+9 = 10 -> 1)")
    print(f"  {dr_p} + {dr_q} = {dr_p+dr_q} = DR({s}) = DR(midpoint {mid}) = {dr_m}")
    assert dr_p + dr_q == 9
    assert dr_s == 9 and dr_m == 9
    print(f"  {dr_p} and {dr_q} are 9-complements: {dr_p}+{dr_q}=9 (the DR modulus)  check")

    # Path 2: Digits of 17
    print(f"\nPATH 2: DIGITS OF {p}")
    tens, unit = p // 10, p % 10
    digit_sum = tens + unit
    unit_plus_dr = unit + dr_p
    dr_result = dr(unit_plus_dr)
    print(f"  {p}: tens={tens}, unit={unit}")
    print(f"  tens+unit = {tens}+{unit} = {digit_sum} = DR({p})={dr_p}  check")
    print(f"  unit + DR({p}) = {unit}+{dr_p} = {unit_plus_dr}  ->  DR({unit_plus_dr}) = {dr_result}")
    assert dr_result == 6
    print(f"  {unit}+{dr_p}={unit_plus_dr} -> DR={dr_result} = imaginary unit of GF({P})  check")

    # Path 3: DR(sum) + imaginary unit
    print(f"\nPATH 3: DR(SUM) + IMAGINARY UNIT")
    imag = 6
    chain = dr_s + imag
    dr_chain = dr(chain)
    print(f"  DR({s}) = {dr_s}")
    print(f"  imaginary unit = {imag}  (6^2 = {pow(6,2)} = -1 mod {P})")
    print(f"  {dr_s} + {imag} = {chain}  ->  DR({chain}) = {dr_chain}")
    assert dr_chain == 6
    print(f"  Returns to imaginary unit {imag}  check")

    # The four faces of 36
    print(f"\nFOUR FACES OF 36:")
    print(f"  17+19 = {s}          (twin prime sum)")
    print(f"  6 x 6 = {6*6} = 6^2  (square of imaginary unit)")
    print(f"  4 x 9 = {4*9}          (product of SA elements {4} and {9})")
    print(f"  36 mod {P} = {s % P} = -1  (antipode of identity in GF({P})*)")
    assert s == 36 == 6**2 == 4*9 and s % P == P - 1
    print(f"  All four representations equal 36  check")

    # SA product: 4x9
    print(f"\nSA PRODUCT:")
    print(f"  SA = {sorted(SA)}")
    print(f"  4 = 2^2  (first prime squared)")
    print(f"  9 = 3^2  (second prime squared)")
    print(f"  4 x 9 = (2x3)^2 = 6^2 = 36 = -1 (mod {P})")
    assert 4 in SA and 9 in SA and 4*9 % P == P-1
    print(f"  Product of atomic-generator squares = imaginary unit squared = -1  check")

    # Check which SA pairs multiply to -1
    print(f"\n  All SA x SA products mod {P}:")
    sa_list = sorted(SA)
    for i in range(len(sa_list)):
        for j in range(i, len(sa_list)):
            prod = (sa_list[i] * sa_list[j]) % P
            flags = []
            if prod in H_SET:    flags.append("H")
            if prod in SA:       flags.append("SA")
            if prod in ST:       flags.append("ST")
            if prod == P-1:      flags.append("-1 (antipode)")
            flag_str = "  " + ", ".join(flags) if flags else ""
            print(f"    {sa_list[i]:2d} x {sa_list[j]:2d} = {sa_list[i]*sa_list[j]:4d} = {prod:2d} (mod {P}){flag_str}")

    # DR convergence for all twin prime pairs
    print(f"\nDR COMPLEMENTARITY IN TWIN PRIME PAIRS:")
    print(f"  (p, p+2) pairs where DR(p)+DR(p+2)=9:")
    def sieve(limit):
        is_p = bytearray([1])*(limit+1); is_p[0]=is_p[1]=0
        for i in range(2, int(limit**0.5)+1):
            if is_p[i]: is_p[i*i::i] = bytearray(len(is_p[i*i::i]))
        return [n for n in range(2,limit+1) if is_p[n]]
    primes = sieve(200)
    twins = [(p,p+2) for p in primes if p+2 in set(primes)]
    complement_pairs = [(p,q) for p,q in twins if dr(p)+dr(q)==9]
    for p,q in complement_pairs[:8]:
        s = p+q
        print(f"  ({p:3d},{q:3d}): DR={dr(p)}+{dr(q)}=9  sum={s}  DR(sum)={dr(s)}")
    frac = len(complement_pairs)/len(twins)
    print(f"  {len(complement_pairs)} of {len(twins)} twin pairs below 200 are 9-complementary ({frac:.0%})")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
