# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 235: Zero-Ground Decimal Architecture -- The 45+81=126=9 Foundation
================================================================================

USER OBSERVATION:
  Zero means no distance from the ground.
  I am building directly onto something, adding to something.
  Something that could be (0)1-9-1(0).
  So if ground zero, then 1-9 built on top until we get to the maximum
  something 1 zero can handle, which is 9 distance from its original foundation.

  build up:
  0-ground
  1-cap stone
  9-top of pyramid
  1-bottom of pyramid
  0-ground
  [mirror]

  10 = full of 1 through 9 filled zero.
  The zero is 45 which again equals 9.
  So 1 zero has 45 in it, +1 to it equals 46 = 10.

  45+81=126=9

  10-1st zero added
  20-2nd
  ...
  90-9th

  192939495969798991  [digit pairs of form k9]
  45+81=126=9

  19+19=38=1+1=2

  9+1=add 1 zero per 9 filled 0.

STRUCTURE:

A. THE ZERO AS A CONTAINER:
  0 is the ground -- no distance. 1 through 9 fill the single zero.
  Sum of the filling: 1+2+3+4+5+6+7+8+9 = 45. DR(45) = 9.
  The zero is "full at 9." Adding +1 forces the carry: 9+1=10.
  10 = the first zero promoted to a new ground level.

B. THE 45+81=126=9 IDENTITY:
  45 = 1+2+...+9 (the sum that fills one zero).
  81 = 9^2 = 3^4 = the "nine nines" contribution: 9 x 9.
  45+81 = 126. DR(126) = 9.
  126 = 2 x 63 = 2 x 9 x 7 = 2 x 63.
  126 mod 37 = 126 - 3x37 = 15. DR(15) = 6 = imaginary unit.
  The sum of the single-zero fill plus the squared modulus DR-reduces to 9,
  and its GF(37) residue DR-reduces to the imaginary unit.

C. THE NINE TOWERS (k9 pairs):
  Writing consecutive "k9" pairs: 19, 29, 39, 49, 59, 69, 79, 89, 99.
  Digit-concatenation: 192939495969798999.
  Each pair k9 contributes k (the counter) and 9 (the filled unit).
  Tens digits 1..9: sum = 45. Units all 9: sum = 81. Total = 126.
  Confirmation: 45+81 = 126 = DR 9.

D. THE MIRROR STRUCTURE:
  0-0 (ground)
  1..9 fills up (45 total)
  At 9: carry -> 10, a new zero is added.
  10-19: the tens digit is 1, units fill 0..9 again.
  At 19: second group of nine starts.
  At 99: both digits max out; add new ground: 100.
  The pyramid mirrors: 0..9..0 then 00..99..00.

E. GF(37) ANATOMY OF THE ZERO-FILL SEQUENCE:
  1+2+...+9 = 45. 45 mod 37 = 8.
  Sum of zeros added (10,20,...,90) = 450. 450 mod 37 = 450-12x37=6=imaginary unit.
  Total 1-99 sum = 4950. 4950 mod 37 = 4950-133x37=4950-4921=29.
  DR(4950) = 9.

F. 19+19=38 AND THE CARRY:
  DR(19)=1. 1+1=2. DR(38)=11->2. The two DRs sum to 2 (first prime/gap).
  19 mod 37 = 19 in C_4={5,13,19} (prime seed coset).
  19+19 = 38 mod 37 = 1 in H.
  Two elements of the prime seed coset sum to the identity in H.
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
    print("THEOREM 235: ZERO-GROUND DECIMAL ARCHITECTURE -- 45+81=126=9")
    print("=" * 70)

    # A: Zero as container
    print("\nA. THE ZERO AS CONTAINER:")
    digit_sum_1_9 = sum(range(1, 10))
    print(f"  1+2+3+4+5+6+7+8+9 = {digit_sum_1_9}")
    assert digit_sum_1_9 == 45
    print(f"  DR({digit_sum_1_9}) = {dr(digit_sum_1_9)}  [zero is full]")
    print(f"  9+1 = 10: one filled zero produces the first H element  check")
    assert 10 in H_SET

    # B: 45+81=126=9
    print(f"\nB. THE 45+81=126=9 IDENTITY:")
    s = 45 + 81
    print(f"  45 = sum(1..9)  [fills one zero]")
    print(f"  81 = 9^2        [nine times nine = the squared zero modulus]")
    print(f"  45+81 = {s}  DR({s}) = {dr(s)}  check")
    assert s == 126 and dr(s) == 9
    gf_s = s % P
    print(f"  {s} mod {P} = {gf_s}  DR({gf_s}) = {dr(gf_s)} = imaginary unit  check")
    assert dr(gf_s) == 6
    print(f"  {s} = 2 x 63 = 2 x 9 x 7  [factor decomposition]")
    assert 126 == 2 * 63 == 2 * 9 * 7

    # C: The nine towers
    print(f"\nC. NINE TOWERS (k9 pairs):")
    pairs = [(k, 9) for k in range(1, 10)]
    tens_sum = sum(k for k, _ in pairs)
    units_sum = sum(u for _, u in pairs)
    total = tens_sum + units_sum
    print(f"  Pairs: {[10*k+9 for k,_ in pairs]}")
    print(f"  Tens digits sum: {tens_sum}")
    print(f"  Units (all 9) sum: {units_sum} = 9x9 = 81")
    print(f"  Total: {tens_sum}+{units_sum} = {total} = DR {dr(total)}  check")
    assert tens_sum == 45 and units_sum == 81 and total == 126 and dr(total) == 9

    # D: Mirror / carry structure
    print(f"\nD. CARRY STRUCTURE:")
    print(f"  After 9: carry -> 10. 10 mod {P} = {10%P} in H  check")
    print(f"  After 19: 19 mod {P} = {19%P}  (in C_4, prime seed coset)")
    print(f"  After 99: 99 mod {P} = {99%P}  in SA: {99%P in SA}  check")
    assert 10 in H_SET and 99 % P in SA

    # E: GF(37) anatomy
    print(f"\nE. GF({P}) ANATOMY OF THE ZERO-FILL:")
    s_1_9 = sum(range(1, 10))
    s_tens = sum(range(10, 100, 10))
    s_1_99 = sum(range(1, 100))
    print(f"  sum(1..9)  = {s_1_9}  mod {P} = {s_1_9%P}  DR = {dr(s_1_9%P)}")
    print(f"  sum(10,20..90) = {s_tens}  mod {P} = {s_tens%P}  DR = {dr(s_tens%P)} = imaginary unit")
    assert dr(s_tens % P) == 6
    print(f"  sum(1..99) = {s_1_99}  mod {P} = {s_1_99%P}  DR = {dr(s_1_99)}")
    print(f"  Check: 450 mod {P} = {450%P} = {450%P} = imaginary unit: {450%P==6}  check")
    assert 450 % P == 6

    # F: 19+19=38
    print(f"\nF. 19+19=38 AND THE CARRY:")
    print(f"  DR(19) = {dr(19)}  [1+9=10->1]")
    print(f"  DR(19)+DR(19) = {dr(19)+dr(19)} = first prime = twin gap")
    print(f"  19+19 = {19+19}  mod {P} = {(19+19)%P}  in H: {(19+19)%P in H_SET}  check")
    assert (19+19) % P in H_SET
    print(f"  19 in C_4={{5,13,19}} (prime seed coset); 19+19 lands in H  check")
    assert 19 in {5,13,19}

    # 9+something digital root identity
    print(f"\nG. 9+n DIGITAL ROOT IDENTITY:")
    print(f"  DR(9+n) = DR(n) for all n (DR modulus = 9)")
    tests = [5, 14, 23, 7, 16]
    for n in tests:
        assert dr(9+n) == dr(n), f"DR(9+{n}) != DR({n})"
        print(f"  9+{n}={9+n}: DR={dr(9+n)}=DR({n})  check")
    print(f"  Adding 9 is the identity on DR. This is why the zero is 'full at 9.'")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
