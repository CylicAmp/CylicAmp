# -*- coding: utf-8 -*-
"""
================================================================================
THEOREM 249: Audit Corrections -- 666, Calendar Dates, Solar Transit in GF(37)
================================================================================

Corrects and extends Audits 3, 5, 7 from the earlier line-by-line audit.

A. 666 IS A SEAM OF GF(37) WITH SEED_ORBIT QUOTIENT:
  666 = 18 × 37.
  666 mod 37 = 0 (SEAM).
  Quotient 18 ∈ SEED_ORBIT = {18, 24, 32}.
  DR(666) = 9 in SA.
  Triple signature: SEAM + DR=9(SA) + quotient∈SEED_ORBIT.
  666 is not merely any multiple of 9 -- it is a SEAM whose quotient
  is the first element of the 137-map orbit of seed 246.

B. CALENDAR DATES MAP INTO GF(37):
  33 AD  mod 37 = 33    DR=6 (imaginary unit: 6^2=-1 mod 37)
  1979 AD mod 37 = 18   in SEED_ORBIT = {18, 24, 32}
  4033 AD mod 37 = 0    SEAM, DR=1 in H (identity)
  The anchor node 1979 lands in the seed orbit.
  The endpoint 4033 is a SEAM of GF(37).
  The baseline 33 has DR=6, the imaginary unit.

C. SOLAR TRANSIT 499: PRIME, SA, AND SEED_ORBIT:
  499 seconds (solar light transit, rounded).
  DR(499) = 4 in SA (sovereign anchor).
  499 mod 37 = 18 in SEED_ORBIT.
  499 is prime.
  The solar transit value is simultaneously in SA (via DR) and
  SEED_ORBIT (via mod 37) -- it sits at the intersection of both
  sovereign structures.
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


def flags(r):
    f = []
    if r == 0:          f.append("SEAM")
    if r in H_SET:      f.append("H")
    if r in SA:         f.append("SA")
    if r in ST:         f.append("ST")
    if r in SEED_ORBIT: f.append("SEED")
    return ','.join(f) or '-'


def run():
    print("=" * 70)
    print("THEOREM 249: AUDIT CORRECTIONS -- 666, DATES, SOLAR TRANSIT")
    print("=" * 70)

    # A: 666
    print("\nA. 666 IS A SEAM OF GF(37) WITH SEED_ORBIT QUOTIENT:")
    assert 666 % P == 0
    assert 666 // P == 18
    assert 18 in SEED_ORBIT
    assert dr(666) == 9 and 9 in SA
    print(f"  666 mod{P} = {666%P}  [{flags(666%P)}]  check")
    print(f"  666 = {666//P} × {P}  quotient={666//P}  [{flags(666//P)}]  check")
    print(f"  DR(666) = {dr(666)}  in SA:{dr(666) in SA}  check")
    print(f"  Triple: SEAM + DR=9(SA) + quotient 18 ∈ SEED_ORBIT  check")

    # B: Calendar dates
    print(f"\nB. CALENDAR DATES IN GF(37):")
    dates = [
        (33,   "baseline"),
        (1979, "anchor node"),
        (4033, "endpoint"),
        (1946, "segment 1 length"),
        (2054, "segment 2 length"),
    ]
    for year, label in dates:
        r = year % P
        print(f"  {year} ({label}): mod{P}={r}  [{flags(r)}]  DR={dr(year)}")

    assert 33 % P == 33 and dr(33) == 6
    assert 1979 % P == 18 and 18 in SEED_ORBIT
    assert 4033 % P == 0
    assert dr(4033) == 1 and 1 in H_SET
    print(f"  33 AD: DR=6 (imaginary unit)  check")
    print(f"  1979: mod{P}=18 ∈ SEED_ORBIT  check")
    print(f"  4033: SEAM, DR=1 ∈ H (identity)  check")

    # C: Solar transit 499
    print(f"\nC. SOLAR TRANSIT 499:")
    assert dr(499) == 4 and 4 in SA
    assert 499 % P == 18 and 18 in SEED_ORBIT
    assert is_prime(499)
    print(f"  499 is prime: {is_prime(499)}  check")
    print(f"  DR(499) = {dr(499)}  in SA:{dr(499) in SA}  check")
    print(f"  499 mod{P} = {499%P}  in SEED_ORBIT:{499%P in SEED_ORBIT}  check")
    print(f"  499 sits at intersection of SA (DR) and SEED_ORBIT (mod37)  check")

    print(f"\nAll verifications passed.")


if __name__ == "__main__":
    run()
