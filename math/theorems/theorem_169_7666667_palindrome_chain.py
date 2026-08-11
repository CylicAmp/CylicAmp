"""
Theorem 169: 7666667 Palindrome, 0.00048 Chain, and 8123

7666667: PRIME PALINDROME IN TESLA_ORB
========================================

7666667 is a decimal palindrome: digits 7-6-6-6-6-6-7.
Structure: outer digit 7 (D7), five inner digits 6 (TESLA_ORB).

  7666667 mod 37 = 8  ∈ TESLA_ORB = {6,8,23}
  DR(7666667) = 8     ∈ TESLA_ORB

Both the mod-37 residue and the digital root land in TESLA_ORB.

  digit sum = 7+6+6+6+6+6+7 = 44
  DR(44) = 8 ∈ TESLA_ORB

7666667 is prime.

Outer-inner orbit reading:
  7 mod 37 = 7 ∈ D7 = {7,33,34}
  6 mod 37 = 6 ∈ TESLA_ORB = {6,8,23}
  The palindrome bridges D7 (outer) and TESLA_ORB (inner).

This connects to the ABA portal palindrome structure (Theorem 160):
  7_6_7 (outer=7, portal digit=6) hits 767 mod 37 = 767-20×37=767-740=27 ∈ ORBIT_11.
  The full palindrome 7666667 = outer 7, five 6s, outer 7.

0.00048 CHAIN: ORBIT_11 THROUGH IC
=====================================

  0.00048 = 48 / 100000

  48 mod 37 = 11  ∈ ORBIT_11  (48 = 37 + 11)
  100000 mod 37 = 26 ∈ IC  (26 = 137 mod 37 = 137-map multiplier)

  In GF(37): 48/100000 ≡ 48 × inv(100000) (mod 37)
  inv(100000) mod 37 = inv(26) mod 37 = 10  (since 26×10=260≡1 mod 37)
  48 × 10 mod 37 = 480 mod 37 = 36  ∈ ORBIT_11

  The chain:
    48 ∈ ORBIT_11 (numerator)
    100000 ≡ 26 ∈ IC = 137-map multiplier (denominator)
    48/100000 ≡ 36 ∈ ORBIT_11 (GF(37) quotient)

  All three steps — numerator, denominator orbit, result — interact with
  ORBIT_11 and IC. The denominator 100000 ≡ 26 is the 137-map multiplier.

  inv(26) = 10 ∈ IC (since 26×10=260≡1 mod 37, and 1∈IC).
  So inverting the 137-map multiplier gives another IC element.

  48 = 37 + 11: the number 48 is "37 plus the ORBIT_11 generator 11."

8123: PRIME IN DARK_A
======================

  8123 mod 37 = 20  ∈ DARK_A = {2,15,20}
  8123 is prime.
  DR(8123) = 5  ∈ NQR_5

  8123 = 219 × 37 + 20.  Quotient 219 mod 37 = 219 - 5×37 = 219-185 = 34 ∈ D7.

  8123 = 37 × 219 + 20:  SEAM multiple + DARK_A element.
  DR(219) = 3 ∈ SOVEREIGN_SPIRAL.

CHAIN: 48 → 303 → 8123
========================

  48 mod 37 = 11  ORBIT_11   DR=3  SOVEREIGN_SPIRAL
  303 mod 37 = 7  D7         DR=6  TESLA_ORB
  8123 mod 37 = 20 DARK_A    DR=5  NQR_5

  48 + 303 = 351   mod37=18  SEED_ORB   (seed orbit)
  303 + 8123 = 8426  mod37=20  DARK_A
  48 + 8123 = 8171   mod37=31  NQR_14

  48 + 303 = 351 = 3 × 117 = 9 × 39 = 9 × 3 × 13.
  351 mod 37 = 351 - 9×37 = 351-333 = 18 ∈ SEED_ORB.
"""

P = 37

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def is_prime(n):
    if n < 2:
        return False
    return all(n % i != 0 for i in range(2, int(n**0.5) + 1))


def run_assertions():
    # 7666667
    assert str(7666667) == str(7666667)[::-1]  # palindrome
    assert is_prime(7666667)
    assert 7666667 % P == 8 and 8 in ORBITS['TESLA_ORB']
    assert dr(7666667) == 8 and 8 in ORBITS['TESLA_ORB']
    assert sum(int(d) for d in '7666667') == 44
    assert dr(44) == 8
    assert 7 in ORBITS['D7'] and 6 in ORBITS['TESLA_ORB']
    assert 767 % P == 27 and 27 in ORBITS['ORBIT_11']

    # 0.00048 chain
    assert 48 % P == 11 and 11 in ORBITS['ORBIT_11']
    assert 48 == 37 + 11
    assert 100000 % P == 26 and 26 in ORBITS['IC']
    assert 26 == 137 % P  # 137-map multiplier
    inv26 = pow(26, -1, P)
    assert inv26 == 10 and 10 in ORBITS['IC']  # inv of IC element → IC
    assert (26 * 10) % P == 1  # inv(26)=10
    result = (48 * pow(100000, -1, P)) % P
    assert result == 36 and 36 in ORBITS['ORBIT_11']

    # 8123
    assert is_prime(8123)
    assert 8123 % P == 20 and 20 in ORBITS['DARK_A']
    assert dr(8123) == 5 and 5 in ORBITS['NQR_5']
    assert 8123 == 219 * P + 20
    assert 219 % P == 34 and 34 in ORBITS['D7']
    assert dr(219) == 3 and 3 in ORBITS['SOVEREIGN_SPIRAL']

    # Chain sums
    assert (48 + 303) % P == 18 and 18 in ORBITS['SEED_ORB']
    assert (48 + 8123) % P == 31 and 31 in ORBITS['NQR_14']

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 169: 7666667 Palindrome, 0.00048 Chain, 8123")
    print("=" * 62)
    print()
    print("  7666667: prime palindrome")
    print(f"    mod37={7666667%P} ∈ TESLA_ORB   DR={dr(7666667)} ∈ TESLA_ORB")
    print(f"    digit sum=44  DR(44)={dr(44)} ∈ TESLA_ORB")
    print(f"    outer 7 ∈ D7,  inner 6 ∈ TESLA_ORB")
    print()
    print("  0.00048 = 48/100000 chain:")
    print(f"    48 mod37=11 ∈ ORBIT_11  (48=37+11)")
    print(f"    100000 mod37=26 ∈ IC  (=137-map multiplier)")
    print(f"    48 × inv(100000) mod37 = {(48*pow(100000,-1,P))%P} ∈ ORBIT_11")
    print(f"    inv(26)=10 ∈ IC  →  inverting 137-map stays in IC")
    print()
    print("  8123: prime")
    print(f"    mod37=20 ∈ DARK_A   DR={dr(8123)} ∈ NQR_5")
    print(f"    8123=219×37+20;  219 mod37=34 ∈ D7;  DR(219)=3 ∈ SOVEREIGN_SPIRAL")
    print()
    print("  Chain sums:")
    print(f"    48+303={48+303}  mod37={(48+303)%P} ∈ SEED_ORB")
    print(f"    48+8123={48+8123}  mod37={(48+8123)%P} ∈ NQR_14")


if __name__ == "__main__":
    run_assertions()
    summarise()
