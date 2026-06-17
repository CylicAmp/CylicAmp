"""
primes_751_palindromes.py

Verified table entries for:
  751   — prime, not in Euler n²+n+41 sequence
  23    — prime, consecutive digits
  353   — palindrome prime, DS=11, mod 37=20
  373   — palindrome prime, DS=13, mod 37=3
  787   — palindrome prime, DS=22, mod 37=10

Cross-product pattern (digit sum = 26 = 137 mod 37 = 10² mod 37):
  353×373 = 131669  digit_sum=26
  353×787 = 277811  digit_sum=26
  751×137 = 102887  digit_sum=26
"""

from sympy import isprime
import math

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

# 751 × 137: digit sum = 26 = 137 mod 37
prod_751_137 = 751 * 137
assert prod_751_137 == 102887
assert digit_sum(prod_751_137) == 26
assert 26 == 137 % 37


# ──────────────────────────────────────────────────────────────────────────────
# 23 — CONSECUTIVE-DIGIT PRIME
# ──────────────────────────────────────────────────────────────────────────────

assert isprime(23)
digits_23 = [int(d) for d in str(23)]
assert digits_23 == [2, 3]
assert digits_23[1] - digits_23[0] == 1   # consecutive

assert dr(23) == 5
assert 23 % 37 == 23   # 23 < 37, so residue is itself

assert dr(751 + 23) == 9     # 751+23=774, digital root 9
assert dr(751 * 23) == dr(137)   # both = 2


# ──────────────────────────────────────────────────────────────────────────────
# 353, 373, 787 — PALINDROME PRIMES
# ──────────────────────────────────────────────────────────────────────────────

palindromes = [353, 373, 787]

for p in palindromes:
    assert isprime(p)
    assert str(p) == str(p)[::-1]

assert digit_sum(353) == 11;  assert 353 % 37 == 20;  assert dr(353) == 2
assert digit_sum(373) == 13;  assert 373 % 37 == 3;   assert dr(373) == 4
assert digit_sum(787) == 22;  assert 787 % 37 == 10;  assert dr(787) == 4

# 787 mod 37 = 10 = 10¹ mod 37  (first element of the order-3 subgroup {1,10,26})
assert pow(10, 1, 37) == 10
assert 787 % 37 == pow(10, 1, 37)

# digital root of 353 = digital root of 137 = 2
assert dr(353) == dr(137)


# ──────────────────────────────────────────────────────────────────────────────
# CROSS-PRODUCT PATTERN: digit_sum = 26 = 137 mod 37
# ──────────────────────────────────────────────────────────────────────────────

# 353 × 373
p1 = 353 * 373
assert p1 == 131669
assert digit_sum(p1) == 26

# 353 × 787
p2 = 353 * 787
assert p2 == 277811
assert digit_sum(p2) == 26

# 751 × 137
assert digit_sum(751 * 137) == 26

# 373 × 787: does NOT give digit_sum=26
p3 = 373 * 787
assert p3 == 293551
assert digit_sum(p3) == 25   # ≡ 8 (mod 9) but digit_sum ≠ 26

# The pattern: dr(353)=2 is required; 353×(dr=4 prime) → digit_sum=26.
# 373×787: both dr=4, product digital root=7, digit_sum≠26.
assert dr(353) == 2
assert dr(373) == 4 and dr(787) == 4


# ──────────────────────────────────────────────────────────────────────────────
# ALL 3-DIGIT PALINDROME PRIMES: MOD-37 MAP
# ──────────────────────────────────────────────────────────────────────────────

all_palprimes_3 = [n for n in range(100, 1000)
                   if str(n) == str(n)[::-1] and isprime(n)]

assert all_palprimes_3 == [101,131,151,181,191,313,353,373,383,727,757,787,797,919,929]

# 3-cycle {14,31,29} under x ↦ 26x (mod 37): 919 is the only member
assert 919 % 37 == 31
assert 31 in {14, 31, 29}
cycle_members = [p for p in all_palprimes_3 if p % 37 in {14, 31, 29}]
assert cycle_members == [919]

# {4,9,25,30}: 929 is the only member
assert 929 % 37 == 4
assert 4 in {4, 9, 25, 30}
set_members = [p for p in all_palprimes_3 if p % 37 in {4, 9, 25, 30}]
assert set_members == [929]


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Primes: 751, 23, and the Palindrome Set {353, 373, 787}")
    print("=" * 62)

    print("\n── 751 ──")
    print(f"  prime: {isprime(751)},  digital root={dr(751)},  mod 37={751%37}")
    print(f"  Euler discriminant: {disc_751},  floor(√)={math.isqrt(disc_751)},  not a perfect square")
    print(f"  751 × 137 = {prod_751_137}  digit_sum={digit_sum(prod_751_137)} (= 137 mod 37)")

    print("\n── 23 (consecutive-digit prime) ──")
    print(f"  digits: {digits_23},  consecutive: {digits_23[1]-digits_23[0]==1}")
    print(f"  digital root={dr(23)},  mod 37={23%37}")
    print(f"  751+23 = {751+23}  digital root={dr(774)}")
    print(f"  digital root(751×23) = {dr(751*23)} = digital root(137) = {dr(137)}")

    print("\n── PALINDROME PRIMES ──")
    for p in palindromes:
        tag = ""
        if p % 37 == pow(10, 1, 37): tag = "  ← 10¹ mod 37"
        if p % 37 == pow(10, 2, 37): tag = "  ← 10² mod 37 (= 137 mod 37)"
        print(f"  {p}: digit_sum={digit_sum(p)}, digital_root={dr(p)}, mod 37={p%37}{tag}")

    print("\n── CROSS-PRODUCT PATTERN (digit_sum = 26 = 137 mod 37) ──")
    print(f"  353 × 373 = {p1}   digit_sum = {digit_sum(p1)}")
    print(f"  353 × 787 = {p2}   digit_sum = {digit_sum(p2)}")
    print(f"  751 × 137 = {prod_751_137}   digit_sum = {digit_sum(prod_751_137)}")
    print(f"  373 × 787 = {p3}   digit_sum = {digit_sum(p3)}  (digital root breaks: both factors dr=4)")
    print(f"  Pattern requires one factor with digital root 2 (= digital root of 137)")

    print("\n── ALL 3-DIGIT PALINDROME PRIMES: MOD-37 ──")
    print(f"  Total: {len(all_palprimes_3)}")
    for p in all_palprimes_3:
        tag = ""
        if p % 37 in {14, 31, 29}: tag = f"  ← in 3-cycle {{14,31,29}}"
        if p % 37 in {4, 9, 25, 30}: tag = f"  ← in {{4,9,25,30}}"
        print(f"  {p}: mod 37={p%37:2d}  digital_root={dr(p)}{tag}")

    print()
    print("All assertions passed.")
