"""
Theorem 127: Emirp Pair 37↔73, Genesis Gematria, and GF(37)

37 and 73 are emirps: both prime, digit-reversals of each other.
Their product 37×73 = 2701 is the gematria of Genesis 1:1 in Hebrew.
Both triangular numbers T(37) and T(73) are SEAM in GF(37).
The emirp partner 73 encodes φ(37) as its residue mod 37.

EMIRP STRUCTURE
===============

  37 prime, 73 prime (digit-reversed pair)
  DR chain: 37 → 10 → 1   (10 ∈ IC, 1 ∈ IC)
  DR chain: 73 → 10 → 1   (10 ∈ IC, 1 ∈ IC)
  Both digit sums = 10 ∈ IC = {1, 10, 26}
  Both DRs = 1 ∈ IC

TOTIENT ENCODING
================

  73 mod 37 = 36 = φ(37) = ord₃₇(2)
  37 + 73 = 110 ≡ 36 mod 37 = φ(37)
  The emirp partner of 37 is congruent to 37's own totient mod 37.
  73 ∈ ORBIT_11 = {11, 27, 36}: 73 ≡ 36 ∈ ORBIT_11

GENESIS GEMATRIA: 2701
=======================

  2701 = 37 × 73                         SEAM mod 37
  2701 = T(73) = 73×74/2                 73rd triangular number
  T(37) = 37×38/2 = 703 = 19×37         37th triangular number; SEAM mod 37
  Both T(37) and T(73) are exact multiples of 37 → SEAM in GF(37)
  703 = T(37): DR(703) = 1 ∈ IC

  The gematria of Genesis 1:1 (בְּרֵאשִׁית בָּרָא אֱלֹהִים...) = 2701 = T(73).
  T(73) mod 37 = 0 = SEAM: the text's numerical value maps to SEAM in GF(37).

REPUNIT CONNECTION
==================

  R_n = 111...1 (n ones) mod 37 cycles with period 3:
    R_1 = 1    ∈ IC
    R_2 = 11   ∈ ORBIT_11
    R_3 = 111 = 3×37 ≡ 0 = SEAM
    R_4 ≡ 1, R_5 ≡ 11, R_6 ≡ 0, ...
  Cycle: IC → ORBIT_11 → SEAM → IC → ...
  11² ≡ 10 mod 37, and 10 ∈ IC (ORBIT_11 squared maps to IC)

PISANO CONNECTION
=================

  pi(37) = 76  (Fibonacci Pisano period mod 37)
  76 mod 37 = 2 ∈ DARK_A {2, 15, 20}
  pi(9) = 24 ∈ CB ∩ SEED_ORB
  pi(333) = lcm(pi(9), pi(37)) = lcm(24, 76) = 456
  333 = 9 × 37 ≡ 0 mod 37 = SEAM  (9 = SA-step)

GF(37) CONNECTIONS SUMMARY
===========================

  73 mod 37 = 36 = φ(37) ∈ ORBIT_11
  37+73 mod 37 = 36 = φ(37)
  T(37) = T(73) = SEAM mod 37
  DR(37) = DR(73) = 1 ∈ IC; digit sums both = 10 ∈ IC
  R_3 = 111 = 3×37: first repunit hitting SEAM
  11² ≡ 10 ∈ IC mod 37
  pi(37) = 76 → 2 ∈ DARK_A
  pi(9) = 24 ∈ CB ∩ SEED_ORB
  333 = 9×37 = SEAM (SA-step × prime = SEAM multiple)
"""

P = 37
IC       = frozenset({1,  10, 26})
ORBIT_11 = frozenset({11, 27, 36})
DARK_A   = frozenset({2,  15, 20})
CB       = frozenset({8,  13, 24})
SEED_ORB = frozenset({18, 24, 32})
SA_STEP  = 9


def triangular(n):
    return n * (n + 1) // 2


def dr(n):
    if n == 0: return 9
    return (abs(n) - 1) % 9 + 1


def repunit(n):
    return int('1' * n)


def fibonacci_pisano(m, limit=500):
    a, b = 0, 1
    for i in range(1, limit + 1):
        a, b = b, (a + b) % m
        if a == 0 and b == 1:
            return i
    return None


def run_assertions():
    from sympy import isprime

    # Emirp pair
    assert isprime(37) and isprime(73)
    assert str(37)[::-1] == str(73)          # digit reversal

    # DR and digit sums
    assert sum(int(d) for d in '37') == 10 and 10 in IC
    assert sum(int(d) for d in '73') == 10 and 10 in IC
    assert dr(37) == 1 and dr(73) == 1 and 1 in IC

    # Totient encoding
    assert 73 % P == 36 == P - 1            # φ(37) = 36
    assert (37 + 73) % P == 36
    assert 36 in ORBIT_11
    assert pow(2, 36, P) == 1               # Fermat

    # Genesis gematria
    assert 37 * 73 == 2701
    assert triangular(73) == 2701
    assert 2701 % P == 0                    # SEAM
    assert triangular(37) == 703
    assert 703 % P == 0                     # SEAM
    assert dr(703) == 1 and 1 in IC

    # Repunit cycle
    for n in range(1, 13):
        r = repunit(n) % P
        expected = [1, 11, 0][(n - 1) % 3]
        assert r == expected, f"R_{n} mod 37 = {r}, expected {expected}"
    assert 1 in IC and 11 in ORBIT_11

    # 11² ∈ IC
    assert pow(11, 2, P) == 10 and 10 in IC

    # Pisano periods
    assert fibonacci_pisano(9)  == 24
    assert fibonacci_pisano(37) == 76
    assert 24 in CB and 24 in SEED_ORB
    assert 76 % P == 2 and 2 in DARK_A

    # 333 = 9×37
    assert SA_STEP * P == 333
    assert 333 % P == 0

    print("All assertions passed.")


def summarise():
    print("=" * 58)
    print("Theorem 127: Emirp 37↔73, Genesis 2701, GF(37)")
    print("=" * 58)
    print(f"  73 mod 37 = {73%P} = φ(37)  ∈ ORBIT_11 {sorted(ORBIT_11)}")
    print(f"  37+73 = 110 ≡ {110%P} = φ(37) mod 37")
    print(f"  DR(37)=DR(73)={dr(37)}, digit sums both 10 ∈ IC {sorted(IC)}")
    print(f"  T(37) = {triangular(37)} = 19×37  ≡ 0 (SEAM)")
    print(f"  T(73) = {triangular(73)} = 37×73 = Genesis 1:1 ≡ 0 (SEAM)")
    print(f"  R_n mod 37: IC → ORBIT_11 → SEAM (period 3)")
    print(f"  11² ≡ {pow(11,2,P)} ∈ IC mod 37")
    print(f"  pi(37)={fibonacci_pisano(37)} → {fibonacci_pisano(37)%P} ∈ DARK_A")
    print(f"  pi(9)={fibonacci_pisano(9)} ∈ CB ∩ SEED_ORB")
    print(f"  333 = 9×37 ≡ SEAM  (SA-step × prime)")


if __name__ == "__main__":
    run_assertions()
    summarise()
