# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 239: The Mirror Seam-Antipode Sequence -- 37/73 Reversal Palindrome
================================================================================

OBSERVATION:
  33+4=37   DR=1
  33+3=36   DR=9
  66+7=73   DR=1   [center axis]
  33+3=36   DR=9
  33+4=37   DR=1

  DR palindrome: 1, 9, 1, 9, 1

STRUCTURE:

A. THE FACTOR ANATOMY:
  33 = 3 x 11 = ST_element x R_2    [3 in ST, 11 = R_2]
  66 = 6 x 11 = imaginary_unit x R_2

  33 + 4 = 37 = P          (adding SA_element -> canvas prime = seam)
  33 + 3 = 36 = P-1 = -1   (adding ST_element -> antipode)
  66 + 7 = 73 = 2P-1 = -1  (adding anchor_prime -> antipode)

B. THE 37/73 REVERSAL PAIR:
  37 reversed (digit reversal) = 73.
  37 mod 37 = 0   (SEAM: the canvas prime divides itself)
  73 mod 37 = 36  (ANTIPODE: -1 in GF(37)*)
  Both are prime. The reversal of the seam is the antipode.

  37: units digit 7 = anchor prime; tens digit 3 in ST.
  73: units digit 3 in ST; tens digit 7 = anchor prime.
  The reversal swaps ST and anchor prime, and maps seam -> antipode.

C. THE DR PALINDROME:
  DR(37) = 1   (in H: identity)
  DR(36) = 9   (in SA: sovereign anchor)
  DR(73) = 1   (in H: identity -- same as 37 despite different mod 37)
  Sequence: 1, 9, [1], 9, 1 -- palindrome centered on DR=1.

  The center 73 ≡ -1 (mod 37) but DR = 1: the antipode in GF(37) has DR = identity.

D. THE ADDITIONS AND WHY THEY WORK:
  To reach seam (37) from 33:    add 4 in SA.
  To reach antipode (36) from 33: add 3 in ST.
  To reach antipode (73) from 66: add 7 = anchor prime.

  33 = 3 x R_2 (three times the repunit)
  66 = 6 x R_2 (imaginary unit times the repunit)

  The step from 33 to 66 is x2 (doubling = first prime).
  The additions {4, 3, 7} sum: 4+3+7 = 14. DR(14) = 5 = prime seed.

E. CONNECTIONS:
  33 + 4 = 37: sovereign_target x repunit + sovereign_anchor = canvas prime
  66 + 7 = 73: imaginary_unit x repunit + anchor_prime = 2P-1
  Both results are prime.
  DR of both = 1 (H-element: identity DR).
  The two primes differ by: 73-37 = 36 = -1 (mod 37) = twin prime pair sum (17+19).
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


def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True


def run():
    print("=" * 70)
    print("THEOREM 239: MIRROR SEAM-ANTIPODE -- 37/73 REVERSAL PALINDROME")
    print("=" * 70)

    # A: Factor anatomy
    print("\nA. FACTOR ANATOMY:")
    print(f"  33 = 3 x 11  [3 in ST:{3 in ST}, 11=R_2]")
    print(f"  66 = 6 x 11  [6=imaginary unit, 11=R_2]")
    assert 33 == 3 * 11 and 66 == 6 * 11
    assert 3 in ST

    lines = [(33, 4, 37), (33, 3, 36), (66, 7, 73), (33, 3, 36), (33, 4, 37)]
    labels = ["seam=P", "antipode=-1", "center: antipode=-1", "antipode=-1", "seam=P"]
    print(f"\n  {'sum':10s}  {'DR':4s}  {'mod37':8s}  {'prime':6s}  label")
    print("  " + "-"*52)
    for (a, b, s), label in zip(lines, labels):
        assert a + b == s
        r = s % P
        d = dr(s)
        flags = []
        if r == 0:     flags.append("SEAM")
        if r == P-1:   flags.append("-1")
        if r in H_SET: flags.append("H")
        if r in SA:    flags.append("SA")
        print(f"  {a}+{b}={s:<5d}  DR={d}  mod37={r:<5d}  prime:{is_prime(s)}  [{label}]")

    # B: 37/73 reversal pair
    print(f"\nB. THE 37/73 REVERSAL PAIR:")
    print(f"  37 reversed = 73  (digit reversal)")
    print(f"  37 mod {P} = {37%P}   [SEAM: P divides itself]")
    print(f"  73 mod {P} = {73%P}  [-1 = antipode]  check")
    assert 37 % P == 0 and 73 % P == P - 1
    assert is_prime(37) and is_prime(73)
    print(f"  Both prime.  The digit-reversal of the seam is the antipode.  check")
    print(f"  37: tens=3(ST), units=7(anchor).  73: tens=7(anchor), units=3(ST).")
    print(f"  Reversal swaps ST and anchor prime; maps seam->antipode.")

    # C: DR palindrome
    print(f"\nC. DR PALINDROME:")
    dr_seq = [dr(s) for _, _, s in lines]
    print(f"  DR values: {dr_seq}")
    assert dr_seq == [1, 9, 1, 9, 1]
    print(f"  Palindrome: 1, 9, [1], 9, 1  check")
    print(f"  Center DR=1 corresponds to 73 which is -1 mod {P}.")
    print(f"  The antipode in GF({P}) has digital root = 1 = identity.")
    assert dr(P-1) == 9 and dr(73) == 1

    # D: Addition anatomy
    print(f"\nD. ADDITION ANATOMY:")
    adds = [4, 3, 7, 3, 4]
    targets = [37, 36, 73, 36, 37]
    for a_val, t_val, add in zip([33,33,66,33,33], targets, adds):
        flags = []
        if add in SA: flags.append("SA")
        if add in ST: flags.append("ST")
        if add == 7:  flags.append("anchor_prime")
        print(f"  {a_val}+{add}={t_val}  add in [{','.join(flags) or '-'}]")
    inner_adds = [4, 3, 7]
    s_adds = sum(inner_adds)
    print(f"\n  Distinct additions: {inner_adds}  sum={s_adds}  DR({s_adds})={dr(s_adds)} = prime seed  check")
    assert dr(s_adds) == 5

    # E: Connections
    print(f"\nE. CONNECTIONS:")
    diff = 73 - 37
    print(f"  73 - 37 = {diff} = P-1 = -1 mod P = 17+19 (twin prime pair sum)")
    assert diff == P - 1 == 17 + 19
    print(f"  33 = 3xR_2: ST_element x repunit -> +SA -> seam  check")
    print(f"  66 = 6xR_2: imag_unit x repunit -> +anchor -> antipode  check")
    print(f"  DR(33)={dr(33)}, DR(66)={dr(66)}: 33 -> 66 is x2 (first prime, doubling)")
    assert 66 == 2 * 33

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
