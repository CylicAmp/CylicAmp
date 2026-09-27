"""
linear_form_11n_37m_primes.py

Prime generation from the binary linear form p(n,m) = 11n + 37m.

─────────────────────────────────────────────────────────────────
DEFINITION:
  L = { 11n + 37m : n,m ∈ Z⁺ }

THEOREM [PROVEN — Dirichlet]:
  For every fixed m ≥ 1 with gcd(11, 37m) = 1, the arithmetic
  progression { 11n + 37m : n ≥ 1 } contains infinitely many primes.
  Since gcd(11, 37) = 1, this holds for all m not divisible by 11.

NOTE on the binary form:
  The two-variable form L is not itself a single AP; Dirichlet applies
  to each single-variable slice (fix m, vary n, or fix n, vary m).
  Since gcd(11, 37) = 1, every sufficiently large integer is in L
  (Frobenius number for {11,37}: all integers ≥ 360 representable
  as 11a + 37b with a,b ≥ 0; shift by 48 for a,b ≥ 1).

VERIFIED PRIMES (n,m ∈ 1..20, value ≤ 500):
  35 primes found. First 8: 59, 103, 107, 151, 173, 181, 191, 199.
─────────────────────────────────────────────────────────────────
"""

from sympy import isprime
from math import gcd


# ──────────────────────────────────────────────────────────────────────────────
# FOUNDATION
# ──────────────────────────────────────────────────────────────────────────────

A, B = 11, 37

assert gcd(A, B) == 1

# Frobenius number: largest integer NOT representable as 11a+37b (a,b ≥ 0)
# For coprime a,b: Frobenius(a,b) = a*b - a - b
FROBENIUS = A * B - A - B
assert FROBENIUS == 359

# Every integer > FROBENIUS is representable as 11a+37b with a,b ≥ 0
for n in range(FROBENIUS + 1, FROBENIUS + 50):
    a, found = 0, False
    while A * a <= n:
        rem = n - A * a
        if rem % B == 0:
            found = True
            break
        a += 1
    assert found, f"{n} not representable — Frobenius bound wrong"


# ──────────────────────────────────────────────────────────────────────────────
# DIRICHLET SLICES
# ──────────────────────────────────────────────────────────────────────────────

# For fixed m, {11n + 37m : n ≥ 1} is AP with first term 11+37m and step 11.
# gcd(11, 37m) = gcd(11, 37) × gcd(11, m/gcd(11,m)) = 1 when 11 ∤ m.
for m in range(1, 12):
    first_term = A + B * m
    if gcd(first_term, A) == 1:
        # Dirichlet guarantees infinitely many primes in this AP
        primes_in_slice = [A*n + B*m for n in range(1, 500)
                           if isprime(A*n + B*m)]
        assert len(primes_in_slice) >= 5, \
            f"m={m}: fewer than 5 primes found in first 500 terms"


# ──────────────────────────────────────────────────────────────────────────────
# PRIME ENUMERATION
# ──────────────────────────────────────────────────────────────────────────────

# All primes representable as 11n+37m with n,m ∈ 1..20
L_vals = sorted({A*n + B*m for n in range(1, 21) for m in range(1, 21)})
L_primes = [v for v in L_vals if isprime(v)]

assert len([p for p in L_primes if p <= 200]) == 8
assert len([p for p in L_primes if p <= 500]) == 35

# First 8 primes
assert L_primes[:8] == [59, 103, 107, 151, 173, 181, 191, 199]

# 59 = 11×2 + 37×1 (smallest prime in L)
assert 59 == A*2 + B*1 and isprime(59)

# 191 is in range and is prime; verify it's in L
assert any(191 == A*n + B*m for n in range(1,21) for m in range(1,21))
assert isprime(191)


# ──────────────────────────────────────────────────────────────────────────────
# FRAMEWORK CONSTANTS
# ──────────────────────────────────────────────────────────────────────────────

# 11: ord₃₇(10) = 3, and 11 is the first prime with residue 11 mod 37
# 37: the framework modulus
# 11×37 = 407: generator product
assert A * B == 407
# gcd(407, 9) = 1: no overlap with mod-9 structure
assert gcd(407, 9) == 1


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Linear Form 11n + 37m — Prime Generation")
    print("=" * 62)
    print(f"\n  A=11, B=37, gcd(A,B)={gcd(A,B)}")
    print(f"  Frobenius number: {FROBENIUS}  (all n>{FROBENIUS} representable, a,b≥0)")
    print(f"  A×B = {A*B}")
    print(f"\n  Primes from L (n,m ∈ 1..20):")
    print(f"    ≤ 200: {[p for p in L_primes if p <= 200]}")
    print(f"    ≤ 500: {len([p for p in L_primes if p <= 500])} primes")
    print(f"\n  Smallest prime: 59 = 11×2 + 37×1")
    print(f"\n  Dirichlet: for fixed m (11∤m), {{11n+37m : n≥1}} contains ∞ primes.")
    print(f"  Applied to 11 slices (m=1..11, m≠11): each verified ≥5 primes.")
    print()
    print("All assertions passed.")
