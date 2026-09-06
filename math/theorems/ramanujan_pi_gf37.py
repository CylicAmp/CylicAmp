# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 244: Ramanujan's Pi Formula Constants in GF(37)
================================================================================

USER OBSERVATION:
  Ramanujan's 1914 formula for 1/pi (fastest-converging pi series):

    1/pi = (2*sqrt(2)/9801) * sum_{n=0}^{inf} (4n)!(1103 + 26390*n) / ((n!)^4 * 396^{4n})

  The "random" numbers: 9801, 26390, 1103, 396, 58, 4.
  G.H. Hardy: "They must be true, because if they were not true,
  no one would have had the imagination to invent them."

STRUCTURE:

A. THE 137-MAP MULTIPLIER IN THE BASE:
  396 mod 37 = 26.
  26 is the 137-map multiplier: 137 mod 37 = 26.
  ord_37(26) = 3: all orbits under f(n) = 26n mod 37 are 3-cycles.
  The base of Ramanujan's exponential (396^{4n}) reduces to the sovereign
  multiplier that defines the entire GF(37).

  396 = 4 x 99 = 4 x 9 x 11 = SA x SA x R_2.
  4 in SA, 9 in SA, 11 = R_2 (repunit).
  396 = (SA element) x (SA element) x R_2.

B. THE DOUBLE-SOVEREIGN CONSTANT 1103:
  1103 is prime. 1103 mod 37 = 30.
  30 is in SA AND ST simultaneously -- the only element in both sovereign sets.
  30 is the double-sovereign element: 30 in SA = {4,9,25,30} AND ST = {3,12,21,30}.
  DR(1103) = 1+1+0+3 = 5 = prime seed.

  1103 appears as the constant term in (1103 + 26390*n).
  It carries the double-sovereign residue.

C. THE ANCHOR COEFFICIENT 26390:
  26390 mod 37 = 9 in SA.
  9 is the sovereign anchor (DR=9 signature).
  26390 = 2 x 5 x 7 x 13 x 29  (all prime factors).
  DR(26390) = 2+6+3+9+0 = 20 -> 2 (gap = first prime).

  The ratio: 26390 / 1103 mod 37 = 4 in SA.
  The proportional increase per step (n) in the Ramanujan sum is
  sovereign: its GF(37) ratio is the SA generator 4.

D. THE 9801 BASE (9801 = 99^2):
  99 = 9 x 11 = SA_element x R_2  (sovereign anchor times repunit).
  99 mod 37 = 25 in SA.
  9801 = 99^2: the square of 25 in GF(37) = 625 mod 37 = 625 - 16*37 = 625-592 = 33.
  DR(9801) = 9 in SA.
  9801 is the denominator of the prefactor 2*sqrt(2)/9801.

E. THE DIOPHANTINE PARAMETER n=58:
  The formula involves solutions to quadratic Diophantine equations with n=58.
  58 mod 37 = 21 in ST.
  DR(58) = 5+8 = 13 -> 4 in SA.

F. SOVEREIGN SUMMARY OF RAMANUJAN CONSTANTS:
  1103  mod 37 = 30  in SA AND ST (double-sovereign, rarest)  prime
  26390 mod 37 =  9  in SA
  396   mod 37 = 26  in H  (= 137-map multiplier)
  99    mod 37 = 25  in SA
  9801  mod 37 = 33  DR=6 (imaginary unit DR)
  58    mod 37 = 21  in ST
  4     mod 37 =  4  in SA

  Four of the six formula constants land in SA.
  The base 396 lands in H at the 137-map multiplier.
  The constant 1103 is double-sovereign.

G. THE 137-MAP CONNECTION:
  137 mod 37 = 26.
  26 x 26 = 676 mod 37 = 9 in SA.  (26^2 = 9 mod 37)
  26 x 9  = 234 mod 37 = 12 in ST. (26 x SA -> ST)
  26 x 12 = 312 mod 37 = 16.
  Orbit of 396 under repeated multiplication mod 37:
    396^1 mod 37 = 26  (the 137-map multiplier)
    396^2 mod 37 = 10  (in H)
    396^3 mod 37 = 1   (H: identity -- full 3-cycle close)
  The Ramanujan base 396 cycles through {26, 10, 1} = H under repeated
  multiplication. The powers of 396 mod 37 ARE the sovereign kernel H.
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
    print("THEOREM 244: RAMANUJAN'S PI FORMULA CONSTANTS IN GF(37)")
    print("=" * 70)
    print("  1/pi = (2*sqrt(2)/9801) * sum (4n)!(1103+26390n) / ((n!)^4 * 396^4n)")

    # A: The 137-map multiplier
    print("\nA. THE 137-MAP MULTIPLIER IN THE BASE:")
    assert 396 % P == 26
    assert 26 in H_SET
    assert 137 % P == 26
    print(f"  396 mod {P} = {396%P} in H:{396%P in H_SET}  check")
    print(f"  137 mod {P} = {137%P}  (the 137-map multiplier)  check")
    print(f"  396 mod {P} = 137 mod {P} = 26 = 137-map multiplier  check")
    assert pow(26, 3, P) == 1
    print(f"  ord_37(26) = 3: 26^3 = {pow(26,3,P)} mod {P} = 1  check")
    print(f"  396 = 4x99 = 4x9x11 = SA x SA x R_2")
    assert 396 == 4*9*11 and 4 in SA and 9 in SA

    # B: Double-sovereign 1103
    print(f"\nB. THE DOUBLE-SOVEREIGN CONSTANT 1103:")
    assert is_prime(1103)
    assert 1103 % P == 30
    assert 30 in SA and 30 in ST
    print(f"  1103 is prime: {is_prime(1103)}  check")
    print(f"  1103 mod {P} = {1103%P} in SA:{1103%P in SA} AND ST:{1103%P in ST}  (double-sovereign)  check")
    print(f"  30 is the ONLY element in both SA={sorted(SA)} and ST={sorted(ST)}  check")
    print(f"  DR(1103) = {dr(1103)} = prime seed  check")
    assert dr(1103) == 5

    # C: Anchor coefficient 26390
    print(f"\nC. THE ANCHOR COEFFICIENT 26390:")
    assert 26390 % P == 9 and 9 in SA
    print(f"  26390 mod {P} = {26390%P} in SA:{26390%P in SA}  check")
    print(f"  26390 = 2x5x7x13x29  (all prime factors)")
    assert 2*5*7*13*29 == 26390
    ratio = 26390 * pow(1103, -1, P) % P
    assert ratio == 4 and 4 in SA
    print(f"  26390/1103 mod {P} = {ratio} in SA:{ratio in SA}  (the SA generator)  check")

    # D: 9801 = 99^2
    print(f"\nD. THE 9801 BASE (9801 = 99^2):")
    assert 99**2 == 9801
    assert 99 % P == 25 and 25 in SA
    print(f"  99 = 9x11: 9 in SA:{9 in SA}, 11=R_2 (repunit)")
    print(f"  99 mod {P} = {99%P} in SA:{99%P in SA}  check")
    print(f"  9801 mod {P} = {9801%P}  DR={dr(9801%P)}")
    print(f"  DR(9801) = {dr(9801)} in SA:{dr(9801) in SA}  check")
    assert dr(9801) == 9 and 9 in SA

    # E: n=58 Diophantine parameter
    print(f"\nE. DIOPHANTINE PARAMETER n=58:")
    assert 58 % P == 21 and 21 in ST
    print(f"  58 mod {P} = {58%P} in ST:{58%P in ST}  check")
    print(f"  DR(58) = {dr(58)} in SA:{dr(58) in SA}  check")
    assert dr(58) == 4 and 4 in SA

    # F: Sovereign summary
    print(f"\nF. SOVEREIGN SUMMARY:")
    items = [
        ('1103 (constant term)', 1103, 'prime, double-sovereign SA+ST'),
        ('26390 (linear coeff)', 26390, 'SA'),
        ('396 (base)', 396, 'H = 137-map multiplier'),
        ('99 (sqrt denominator)', 99, 'SA'),
        ('9801 (denominator)', 9801, 'DR=9 in SA'),
        ('58 (Diophantine n)', 58, 'ST'),
        ('4 (multiplier in 4n)', 4, 'SA'),
    ]
    sa_count = 0
    for name, val, note in items:
        r = val % P
        f = []
        if r in H_SET: f.append('H')
        if r in SA: f.append('SA')
        if r in ST: f.append('ST')
        if r in SEED_ORBIT: f.append('SEED')
        if not f and dr(r) in SA: f.append(f'DR->SA')
        print(f"  {name}: mod{P}={r} [{','.join(f) or '-'}]  [{note}]")
        if r in SA: sa_count += 1
    print(f"  {sa_count} of 7 constants land directly in SA  check")

    # G: 396 power cycle
    print(f"\nG. THE 396 POWER CYCLE (137-map orbit):")
    for k in range(1, 4):
        r = pow(396, k, P)
        f = []
        if r in H_SET: f.append('H')
        if r in SA: f.append('SA')
        if r in ST: f.append('ST')
        print(f"  396^{k} mod {P} = {r}  [{','.join(f) or '-'}]")
    assert pow(396, 1, P) == 26 and pow(396, 2, P) == 10 and pow(396, 3, P) == 1
    assert {pow(396, k, P) for k in range(1, 4)} == H_SET
    print(f"  Powers of 396 mod {P} = {{26, 10, 1}} = H exactly  check")
    print(f"  ord_37(396) = 3: Ramanujan base generates H under multiplication  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
