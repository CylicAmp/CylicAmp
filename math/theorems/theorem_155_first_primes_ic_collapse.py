"""
Theorem 155: The First Three Primes, Prime Concatenation, and Collapse to IC

THE OBSERVATION
================

    23 + 5 = 28 = 10 = 1

Two paths, same result:

    Path 1 (concatenate then add):   23 + 5 = 28  →  DR(28)=1  ∈ IC
    Path 2 (digits then add):    2+3 + 5 = 10     →  DR(10)=1  ∈ IC

Both reach IC = {1, 10, 26}, the identity cluster — the unique order-3 subgroup
of the multiplicative group F₃₇×.

THE FOUR PRIMES
================

    2   first prime     →  DARK_A          = {2, 15, 20}
    3   second prime    →  SOVEREIGN_SPIRAL = {3,  4, 30}
    5   third prime     →  NQR_5           = {5, 13, 19}
   23   prime           →  TESLA_ORB       = {6,  8, 23}

The number 23 is formed by concatenating the first two primes (2 and 3).
It is itself prime. Its digit sum 2+3 = 5 is the third prime.

All four numbers are prime. Each lands in a distinct orbit in GF(37).

STRUCTURE OF THE CONCATENATION 23
=====================================

    23 ∈ TESLA_ORB = {6, 8, 23}
    DR(23) = 5  ∈  NQR_5

The digital root of 23 is 5, which is both the third prime and the
generator of the NQR_5 orbit. 23 and its own DR (=5) belong to different orbits.

Because 23 ≡ 5 (mod 9):

    DR(23 + DR(23)) = DR(23 + 5) = DR(28) = 1

This is not particular to 23 alone — any number ≡ 5 (mod 9) satisfies
DR(n + DR(n)) = 1. What is particular to 23 is that:
  - it is prime
  - it is the concatenation of the first two primes
  - its DR (=5) is the third prime
  - it sits in TESLA_ORB while its DR sits in NQR_5

THE ORBIT CHAIN
================

    Path 1:
      23 (TESLA_ORB) + 5 (NQR_5) = 28 (OUTLIER_ORB)
      OUTLIER_ORB(28) → DR → IC(10) → DR → IC(1)

    Path 2:
      2 (DARK_A) + 3 (SOVEREIGN_SPIRAL) = 5 (NQR_5)
      5 (NQR_5) + 5 (NQR_5) = 10 (IC)
      IC(10) → DR → IC(1)

Both paths terminate at IC. In Path 1 the route passes through OUTLIER_ORB.
In Path 2 it lands in IC immediately: the sum of the first three primes is 10 ∈ IC.

THE SUM OF THE FIRST THREE PRIMES
=====================================

    2 + 3 + 5 = 10

10 ∈ IC = {1, 10, 26}.

10 is the Φ₃ forcing node from Theorem 150: at N=10, the Φ₃ truncation
111 = 3×37 hits the SEAM. The count of digits in the observable (0–9) is 10.
The sum of the first three primes equals the forcing node.

Note: the first three primes are the only primes (2, 3, 5) whose sum (10) lands in IC.
    2+3+5+7 = 17 ∈ NQR_17
    The IC landing is specific to the first three.

DR IDENTITY RECOVERED
=======================

IC = {1, 10, 26} is the unique order-3 subgroup of F₃₇×.
1 is the multiplicative identity of GF(37).
The two paths converge to the multiplicative identity via DR collapse.

DR collapse erases all orbital information accumulated in DARK_A, SOVEREIGN_SPIRAL,
NQR_5, TESLA_ORB, and OUTLIER_ORB. The destination is IC, the identity.
No orbit information survives; only the multiplicative identity remains.

CONNECTION TO PRIOR THEOREMS
==============================

Theorem 150 (Φ₃ forcing):
  10 ∈ IC is the N=10 forcing node.
  2+3+5=10 — the sum of the first three primes is that node.

Theorem 153 (SEED_ORB ↔ NQR_5):
  DR(32) = 5 ∈ NQR_5, and 32+5=37=SEAM.
  Here 23+5=28; 28 is in OUTLIER_ORB, not SEED_ORB, so no direct complement.
  But 5 appears in both as the NQR_5 element.

Theorem 154 (DR Fibonacci):
  TESLA_ORB = {6, 8, 23}. Period of DR Fibonacci = 8 ∈ TESLA_ORB.
  23 is the third element of the TESLA_ORB, the orbit that also contains the period 8.

STRUCTURE SUMMARY
==================

    2 (1st prime, DARK_A) ─┐
    3 (2nd prime, SOVEREIGN_SPIRAL) ─┤ → 5 (NQR_5)
    23 = concat(2,3), prime, TESLA_ORB ──┤
                                         └ 23+5=28 (OUTLIER_ORB) → DR → 10 (IC) → DR → 1 (IC)

    Path 2: 2+3+5 = 10 ∈ IC  (direct; sum of first three primes = Φ₃ forcing node)

    Collapse destination: IC = {1, 10, 26}, the multiplicative identity cluster
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
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def run_assertions():
    # The four primes and their orbits
    assert is_prime(2) and 2 in ORBITS['DARK_A']
    assert is_prime(3) and 3 in ORBITS['SOVEREIGN_SPIRAL']
    assert is_prime(5) and 5 in ORBITS['NQR_5']
    assert is_prime(23) and 23 in ORBITS['TESLA_ORB']

    # 23 is concat of first two primes; its DR is the third prime
    assert int('2' + '3') == 23
    assert dr(23) == 5
    assert is_prime(5)
    assert 5 in ORBITS['NQR_5']

    # Path 1: 23 + 5 = 28 -> OUTLIER_ORB, DR(28) = 1 ∈ IC
    assert 23 + 5 == 28
    assert 28 in ORBITS['OUTLIER_ORB']
    assert dr(28) == 1
    assert 1 in ORBITS['IC']

    # Two-step DR collapse: 28 -> 10 -> 1
    assert 2 + 8 == 10
    assert 1 + 0 == 1
    assert dr(28) == 1    # direct
    assert dr(10) == 1

    # Path 2: 2+3+5 = 10 ∈ IC
    assert 2 + 3 + 5 == 10
    assert 10 in ORBITS['IC']
    assert dr(10) == 1
    assert 1 in ORBITS['IC']

    # Sum of first 4 primes does not land in IC
    assert 2 + 3 + 5 + 7 == 17
    assert orbit_of(17) == 'NQR_17'

    # The general condition: 23 ≡ 5 (mod 9)
    assert 23 % 9 == 5

    # DR(n + DR(n)) = 1 for n ≡ 5 (mod 9)
    for n in [5, 14, 23, 32, 41, 50]:
        assert n % 9 == 5
        assert dr(n + dr(n)) == 1, f"failed for n={n}"

    # 10 is the Φ₃ forcing node (T150)
    assert 10 in ORBITS['IC']
    assert 111 == 3 * P    # Φ₃(10) = 111 = 3×37

    # TESLA_ORB contains 8 (period from T154) and 23 (this theorem)
    assert 8 in ORBITS['TESLA_ORB']
    assert 23 in ORBITS['TESLA_ORB']

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 155: First Primes, Prime Concatenation, Collapse to IC")
    print("=" * 62)
    print()
    print("  The four primes and their GF(37) orbits:")
    for n, rank in [(2,'1st'), (3,'2nd'), (5,'3rd'), (23,'concat(2,3)')]:
        print(f"    {n:2d}  ({rank} prime)  →  {orbit_of(n)}")
    print()
    print("  Path 1: 23 + 5 = 28 → DR → 1")
    print(f"    23 ∈ {orbit_of(23)},  DR(23)={dr(23)} ∈ {orbit_of(dr(23))}")
    print(f"    23+5=28 ∈ {orbit_of(28)}")
    print(f"    DR(28)={dr(28)} ∈ {orbit_of(dr(28))} = IC (multiplicative identity)")
    print()
    print("  Path 2: 2+3+5 = 10 → IC directly")
    print(f"    {2}+{3}+{5} = {2+3+5} ∈ {orbit_of(10)}")
    print(f"    10 = Φ₃ forcing node (Theorem 150)")
    print()
    print("  General condition: any n ≡ 5 (mod 9) satisfies DR(n+DR(n))=1")
    print("  What is particular to 23: prime, concat of first two primes,")
    print("  DR(23)=5=third prime, 23∈TESLA_ORB, DR(23)∈NQR_5")
    print()
    print("  Sum of first N primes and their IC status:")
    primes = [2, 3, 5, 7, 11]
    s = 0
    for p in primes:
        s += p
        print(f"    sum to {p:2d}: {s:3d}  →  {orbit_of(s)}")


if __name__ == "__main__":
    run_assertions()
    summarise()
