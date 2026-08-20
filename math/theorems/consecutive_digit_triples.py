# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 242: Consecutive Digit Triples -- Sovereign Reduction and Imaginary Chain
================================================================================

USER OBSERVATIONS:
  2x3=6
  12+3=1+5=6
  1+23=2+4=6       [all groupings of {1,2,3} reduce to 6]
  1+2+3=6

  1-2 = -1  (antipode)
  2-1 = +1  (identity, H)

  123: DR=6 (imaginary unit)
  123 -> 6x2=12=3  [ST]
  123 -> 6x3=18=9  [SEED_ORBIT]
  123 -> 6x4=24=6  [SEED_ORBIT]

  3+45=48=12=3
  34+5=39=12=3
  345=12 (mod 37, in ST)
  12x3=36=-1  DR=9

  6+78=84=12=3
  67+8=75=12=3
  678=12 (mod 37, in ST)

  9=333  [333=9x37, SEAM]

STRUCTURE:

A. THE {1,2,3} TRIPLE -> IMAGINARY UNIT:
  Every partition of digits {1,2,3} into an addition reaches 6:
    1+2+3 = 6
    12+3  = 15 -> 1+5 = 6
    1+23  = 24 -> 2+4 = 6
    2x3   = 6  (product)
  6 is the imaginary unit of GF(37): 6^2 = 36 = -1 (mod 37).

B. IDENTITY AND ANTIPODE:
  2-1 = 1 = identity element in H = {1,10,26}.  (+)
  1-2 = -1 = antipode = P-1 = 36 (mod 37).      (-)
  The two orderings of consecutive digits {1,2} give the two extremes of GF(37)*.

C. THE IMAGINARY UNIT MULTIPLICATION CHAIN (123 -> 6 x {2,3,4}):
  DR(123) = 1+2+3 = 6 = imaginary unit.
  6x2 = 12  mod 37 = 12 in ST,         DR = 3 (ST element)
  6x3 = 18  mod 37 = 18 in SEED_ORBIT, DR = 9 (SA element)
  6x4 = 24  mod 37 = 24 in SEED_ORBIT, DR = 6 (imaginary unit restored)
  Multiplying the imaginary unit by {2,3,4} cycles {ST, SEED, SEED} in GF(37)*.
  The multipliers {2,3,4}: 2 = first prime, 3 in ST, 4 in SA.

D. THE {3,4,5} TRIPLE -> ST (all groupings):
  Every partition of digits {3,4,5} into an addition reaches DR=3 in ST:
    3+4+5 = 12  DR = 3 in ST
    3+45  = 48 -> 4+8=12 -> 1+2=3  check
    34+5  = 39 -> 3+9=12 -> 1+2=3  check
  345 mod 37 = 12 in ST.
  34+5 = 39: 39 mod 37 = 2 (the primitive root; ord_37(2)=36).
  12x3 = 36 = -1 = antipode.  DR(36) = 9 in SA.

E. THE {6,7,8} TRIPLE -> ST (all groupings):
  Every partition of digits {6,7,8} into an addition reaches DR=3:
    6+7+8 = 21  DR = 3 in ST
    6+78  = 84 -> 8+4=12 -> 1+2=3  check
    67+8  = 75 -> 7+5=12 -> 1+2=3  check
  678 mod 37 = 12 in ST.
  Note: 345 mod 37 = 678 mod 37 = 12. Both consecutive triples hit the same residue.

F. 9 = 333: SA AND SEAM:
  333 = 9 x 37 -> 333 mod 37 = 0 (SEAM).
  DR(333) = 9 in SA.
  DR(9) = 9 in SA.
  The digit 9 and the repdigit 333 share DR = 9 (SA element);
  333 is the seam of GF(37) (divisible by 37).

G. SUMMARY TABLE:
  {1,2,3} -> 6  (imaginary unit)
  {3,4,5} -> 12 (ST, mod 37 = 12)
  {6,7,8} -> 21 (ST, mod 37 = 12)
  {9}     -> 9  (SA, 333 = SEAM)
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
    print("THEOREM 242: CONSECUTIVE DIGIT TRIPLES -- SOVEREIGN REDUCTION")
    print("=" * 70)

    # A: {1,2,3} -> imaginary unit
    print("\nA. {1,2,3} TRIPLE -> IMAGINARY UNIT:")
    partitions_123 = [
        (1+2+3,   "1+2+3"),
        (12+3,    "12+3 -> digit sum"),
        (1+23,    "1+23 -> digit sum"),
        (2*3,     "2x3  (product)"),
    ]
    for val, label in partitions_123:
        d = dr(val)
        print(f"  {label} = {val}  DR={d}  imaginary:{d==6}")
        assert d == 6
    assert 6**2 % P == P - 1
    print(f"  6^2 = 36 = -1 mod {P}  (imaginary unit)  check")

    # B: Identity and antipode
    print(f"\nB. IDENTITY AND ANTIPODE:")
    print(f"  2-1 = {2-1} in H:{(2-1) in H_SET}  (+identity)")
    print(f"  1-2 = -1 = {(-1)%P} mod {P} = P-1 = antipode")
    assert (2-1) in H_SET
    assert (-1) % P == P - 1

    # C: Imaginary unit multiplication chain
    print(f"\nC. IMAGINARY UNIT MULTIPLICATION CHAIN:")
    print(f"  DR(123) = {1+2+3} = imaginary unit")
    for mult in [2, 3, 4]:
        prod = 6 * mult
        r = prod % P
        d = dr(prod)
        flags = []
        if r in H_SET:      flags.append("H")
        if r in SA:         flags.append("SA")
        if r in ST:         flags.append("ST")
        if r in SEED_ORBIT: flags.append("SEED")
        print(f"  6x{mult}={prod}  mod{P}={r}  DR={d}  [{','.join(flags) or '-'}]  check")
    assert 12 % P in ST
    assert 18 % P in SEED_ORBIT
    assert 24 % P in SEED_ORBIT
    assert dr(24) == 6
    print(f"  Chain: ST -> SEED -> SEED (DR returns to imaginary unit=6)  check")

    # D: {3,4,5} -> ST
    print(f"\nD. {{3,4,5}} TRIPLE -> ST (all groupings):")
    partitions_345 = [
        (3+4+5,  "3+4+5"),
        (3+45,   "3+45"),
        (34+5,   "34+5"),
    ]
    for val, label in partitions_345:
        d = dr(val)
        print(f"  {label} = {val}  DR_chain->{d}  in ST:{d in ST}  check")
        assert d == 3
    r345 = 345 % P
    print(f"  345 mod {P} = {r345}  in ST:{r345 in ST}  check")
    assert r345 in ST
    r39 = 39 % P
    print(f"  34+5=39: 39 mod {P} = {r39}  (primitive root 2)  check")
    assert r39 == 2
    print(f"  12x3=36=-1 mod {P}  DR(36)={dr(36)} in SA:{dr(36) in SA}  check")
    assert 12*3 % P == P-1 and dr(36) in SA

    # E: {6,7,8} -> ST
    print(f"\nE. {{6,7,8}} TRIPLE -> ST (all groupings):")
    partitions_678 = [
        (6+7+8,  "6+7+8"),
        (6+78,   "6+78"),
        (67+8,   "67+8"),
    ]
    for val, label in partitions_678:
        d = dr(val)
        print(f"  {label} = {val}  DR_chain->{d}  in ST:{d in ST}  check")
        assert d == 3
    r678 = 678 % P
    print(f"  678 mod {P} = {r678}  in ST:{r678 in ST}  check")
    assert r678 in ST
    assert r678 == r345
    print(f"  345 mod {P} = 678 mod {P} = {r345}  (both triples hit same residue)  check")

    # F: 9 = 333
    print(f"\nF. 9 = 333 (SA AND SEAM):")
    print(f"  333 = 9x{P} = {9*P}  check:{333 == 9*P}")
    print(f"  333 mod {P} = {333%P}  (SEAM)")
    print(f"  DR(333) = {dr(333)}  in SA:{dr(333) in SA}  check")
    print(f"  DR(9)   = {dr(9)}    in SA:{dr(9) in SA}    check")
    assert 333 == 9 * P and 333 % P == 0 and dr(333) == 9 and dr(9) == 9

    # G: Summary
    print(f"\nG. SUMMARY TABLE:")
    rows = [
        ([1,2,3], 6,  "imaginary unit"),
        ([3,4,5], 12, "ST, mod37=12"),
        ([6,7,8], 21, "ST, mod37=12"),
        ([9],     9,  "SA; 333=SEAM"),
    ]
    for digits, target, label in rows:
        s = sum(digits)
        d = dr(s)
        flags = []
        if s%P in ST: flags.append("ST")
        if s%P in SA: flags.append("SA")
        if s%P in H_SET: flags.append("H")
        print(f"  {{{','.join(str(x) for x in digits)}}}: sum={s}  DR={d}  mod{P}={s%P}  [{label}]")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
