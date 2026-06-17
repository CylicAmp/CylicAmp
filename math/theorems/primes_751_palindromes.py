"""
primes_751_palindromes.py

Verified table entries and framework connections for:
  751   — prime, not in Euler n²+n+41 sequence
  23    — prime, consecutive digits
  353   — palindrome prime, DS=11, mod37=20
  373   — palindrome prime, DS=13, mod37=3
  787   — palindrome prime, DS=22, mod37=10

Cross-product pattern:
  353×373 = 131669  digit_sum=26 = SCALAR_137
  353×787 = 277811  digit_sum=26 = SCALAR_137
  751×137 = 102887  digit_sum=26 = SCALAR_137
"""

from sympy import isprime
import math

SCALAR_137 = 26   # = 137 mod 37
HEARTBEAT_ORBIT = {14, 31, 29}
SOVEREIGN       = {4, 9, 25, 30}

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def digit_sum(n):
    return sum(int(d) for d in str(n))


# ──────────────────────────────────────────────────────────────────────────────
# 751
# ──────────────────────────────────────────────────────────────────────────────

assert isprime(751)
assert digit_sum(751) == 13      # 7+5+1
assert dr(751) == 4
assert 751 % 37 == 11

# 751 is NOT in the Euler prime-generating polynomial n²+n+41
# n²+n+41=751  →  discriminant = 1+4×(751-41) = 2841
disc_751 = 1 + 4 * (751 - 41)
assert disc_751 == 2841
assert not math.isqrt(disc_751) ** 2 == disc_751   # √2841 is not an integer
assert math.isqrt(disc_751) == 53                  # floor(√2841)=53, 53²=2809≠2841

# 751 × 137: digit sum = SCALAR_137
prod_751_137 = 751 * 137
assert prod_751_137 == 102887
assert digit_sum(prod_751_137) == 26
assert digit_sum(prod_751_137) == SCALAR_137


# ──────────────────────────────────────────────────────────────────────────────
# 23 — CONSECUTIVE-DIGIT PRIME
# ──────────────────────────────────────────────────────────────────────────────

assert isprime(23)
# Digits of 23 are consecutive integers
digits_23 = [int(d) for d in str(23)]
assert digits_23 == [2, 3]
assert digits_23[1] - digits_23[0] == 1   # consecutive

assert dr(23) == 5
assert 23 % 37 == 23   # 23 < 37, so residue is itself

# 751 + 23 = 774
assert dr(751 + 23) == 9    # the "overflow" DR (same as 142857 rotations)

# DR(751 × 23) = DR(137)
assert dr(751 * 23) == dr(137)   # both = 2


# ──────────────────────────────────────────────────────────────────────────────
# 353, 373, 787 — PALINDROME PRIMES
# ──────────────────────────────────────────────────────────────────────────────

palindromes = [353, 373, 787]

for p in palindromes:
    assert isprime(p)
    assert str(p) == str(p)[::-1]   # palindrome

assert digit_sum(353) == 11;  assert 353 % 37 == 20;  assert dr(353) == 2
assert digit_sum(373) == 13;  assert 373 % 37 == 3;   assert dr(373) == 4
assert digit_sum(787) == 22;  assert 787 % 37 == 10;  assert dr(787) == 4

# 787 mod 37 = 10 = 10¹ mod 37 — the first step of the 3-cycle {10, 26, 1}
assert pow(10, 1, 37) == 10
assert 787 % 37 == pow(10, 1, 37)

# DR(353) = 2 = DR(137): 353 and 137 share the twin-prime-anchor digit root
assert dr(353) == dr(137)


# ──────────────────────────────────────────────────────────────────────────────
# CROSS-PRODUCT PATTERN: digit_sum = 26 = SCALAR_137
# ──────────────────────────────────────────────────────────────────────────────

# 353 × 373
p1 = 353 * 373
assert p1 == 131669
assert digit_sum(p1) == 26
assert digit_sum(p1) == SCALAR_137

# 353 × 787
p2 = 353 * 787
assert p2 == 277811
assert digit_sum(p2) == 26
assert digit_sum(p2) == SCALAR_137

# 751 × 137  (already shown above — same pattern)
assert digit_sum(751 * 137) == SCALAR_137

# 373 × 787 does NOT follow (DS=25, not 26)
p3 = 373 * 787
assert p3 == 293551
assert digit_sum(p3) == 25   # ≡8 mod 9 but digit_sum≠26

# Pattern: DR(353)=2 is the anchor — 353×(DR=4 prime) → DS=26
assert dr(353) == 2
assert dr(373) == 4 and dr(787) == 4
# 373×787: both have DR=4, product DR=7, DS≠26


# ──────────────────────────────────────────────────────────────────────────────
# ALL 3-DIGIT PALINDROME PRIMES: FRAMEWORK MAP
# ──────────────────────────────────────────────────────────────────────────────

all_palprimes_3 = [n for n in range(100, 1000)
                   if str(n) == str(n)[::-1] and isprime(n)]

assert all_palprimes_3 == [101,131,151,181,191,313,353,373,383,727,757,787,797,919,929]

# 919 mod 37 = 31  ← heartbeat orbit {14, 31, 29}
assert 919 % 37 == 31
assert 31 in HEARTBEAT_ORBIT

# 929 mod 37 = 4  ← sovereign anchor {4, 9, 25, 30}
assert 929 % 37 == 4
assert 4 in SOVEREIGN

# Tally of framework membership among all 3-digit palindrome primes
heartbeat_members = [p for p in all_palprimes_3 if p % 37 in HEARTBEAT_ORBIT]
sovereign_members = [p for p in all_palprimes_3 if p % 37 in SOVEREIGN]
assert heartbeat_members == [919]
assert sovereign_members == [929]


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Primes: 751, 23, and the Palindrome Set {353, 373, 787}")
    print("=" * 62)

    print("\n── 751 ──")
    print(f"  prime: {isprime(751)},  DR={dr(751)},  mod37={751%37}")
    print(f"  Euler discriminant: {disc_751},  floor(√)={math.isqrt(disc_751)},  not a square")
    print(f"  751 × 137 = {prod_751_137}  digit_sum={digit_sum(prod_751_137)} = SCALAR_137")

    print("\n── 23 (consecutive-digit prime) ──")
    print(f"  digits: {digits_23},  consecutive: {digits_23[1]-digits_23[0]==1}")
    print(f"  DR={dr(23)},  mod37={23%37}")
    print(f"  751+23 = {751+23}  DR={dr(774)}  (= 9, overflow)")
    print(f"  DR(751×23) = {dr(751*23)} = DR(137) = {dr(137)}")

    print("\n── PALINDROME PRIMES ──")
    for p in palindromes:
        tag = ""
        if p % 37 == pow(10, 1, 37): tag = "  ← 10¹ mod 37"
        if p % 37 == pow(10, 2, 37): tag = "  ← SCALAR_137 (10² mod 37)"
        print(f"  {p}: DS={digit_sum(p)}, DR={dr(p)}, mod37={p%37}{tag}")

    print("\n── CROSS-PRODUCT PATTERN (digit_sum = SCALAR_137 = 26) ──")
    print(f"  353 × 373 = {p1}   digit_sum = {digit_sum(p1)}")
    print(f"  353 × 787 = {p2}   digit_sum = {digit_sum(p2)}")
    print(f"  751 × 137 = {prod_751_137}   digit_sum = {digit_sum(prod_751_137)}")
    print(f"  373 × 787 = {p3}   digit_sum = {digit_sum(p3)}  (not 26 — DR pattern breaks)")
    print(f"  Gate: DR(353)=2 (twin-prime anchor) drives DS=26 in the product")

    print("\n── ALL 3-DIGIT PALINDROME PRIMES: FRAMEWORK MAP ──")
    print(f"  Total: {len(all_palprimes_3)}")
    for p in all_palprimes_3:
        tag = ""
        if p % 37 in HEARTBEAT_ORBIT: tag = f"  ← HEARTBEAT {p%37}"
        if p % 37 in SOVEREIGN:       tag = f"  ← SOVEREIGN {p%37}"
        print(f"  {p}: mod37={p%37:2d}  DR={dr(p)}{tag}")

    print()
    print("All assertions passed.")
