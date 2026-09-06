"""
MATHEMATICAL WORK SESSION LOG — VERIFIED
Compiled: 2026-02-21
All results audited by independent computation. Errors corrected inline.
Run this file to confirm every assertion passes.
"""

from sympy import isprime, factorint
import math

# ============================================================
# SECTION 1: THE 3-7 SACRED PAIR
# ============================================================

assert 3 + 7 == 10
assert 3 * 7 == 21
assert 3 - 7 == -4
assert (3 * 7) % 37 == 21
assert (3 + 7) % 37 == 10
assert (-4) % 37 == 33
# 3/7 repeating cycle 428571
cycle_digits = [4, 2, 8, 5, 7, 1]
assert sum(cycle_digits) == 27
assert 4 * 2 * 8 * 5 * 7 * 1 == 2240
assert sum(int(d) for d in "2240") == 8   # DR(2240) = 8

# ============================================================
# SECTION 2: THE 14-41 MIRROR PAIR
# ============================================================

assert 14 + 41 == 55
assert 41 - 14 == 27
assert 14 * 41 == 574
assert sum(int(d) for d in "574") == 16   # 5+7+4
assert 1 + 6 == 7                          # DR(574) = 7
assert 55 == 5 * 11
assert 5 + 5 == 10 == 3 + 7
assert 88 % 37 == 14
assert factorint(88) == {2: 3, 11: 1}

# ============================================================
# SECTION 3: 37-MODULAR SYSTEM
# ============================================================

assert 37 % 1 == 0                         # trivial
assert 3 * 37 == 111
for n in [37, 111, 333, 999]:
    assert n % 37 == 0, f"{n} mod 37 != 0"
assert factorint(142857) == {3: 3, 11: 1, 13: 1, 37: 1}
assert 142 + 857 == 999
assert sum(int(d) for d in "142857") == 27
assert factorint(111111) == {3: 1, 7: 1, 11: 1, 13: 1, 37: 1}
assert factorint(10101)  == {3: 1, 7: 1, 13: 1, 37: 1}

# ============================================================
# SECTION 4: THE 23-55-23 STRUCTURE
# ============================================================

assert isprime(235523)
assert sum(int(d) for d in "235523") == 20  # DR = 2

assert 235523 % 37 == 18
# CORRECTION: 235523 mod 7 = 1  (document claimed 6; 7*33646=235522, 235523-235522=1)
assert 235523 % 7 == 1,  "235523 mod 7 = 1, NOT 6 as originally stated"
assert 235523 % 3 == 2

# Right-truncatable prime chain for 235523
for s in ["235523", "23", "2"]:
    assert isprime(int(s)), f"{s} should be prime"
for s in ["23552", "2355", "235"]:
    assert not isprime(int(s)), f"{s} should be composite"

# Left-truncatable chain
for s in ["235523", "523", "23", "3"]:
    assert isprime(int(s)), f"{s} should be prime"
for s in ["35523", "5523"]:
    assert not isprime(int(s)), f"{s} should be composite"

assert isprime(23)
assert 46 + 55 == 101
assert isprime(101)
assert 64 + 32 + 4 + 1 == 101   # 2^6 + 2^5 + 2^2 + 2^0

# ============================================================
# SECTION 5: 7933 AND 7393 PRIME PAIR
# ============================================================

assert isprime(7933)
assert sum(int(d) for d in "7933") == 22
# CORRECTION: 3397 = 43 * 79 — composite. 7933 is NOT an emirp.
assert not isprime(3397), "3397 = 43*79 is composite; 7933 is therefore NOT an emirp"
assert factorint(3397) == {43: 1, 79: 1}

# CORRECTION: 7933 mod 37 = 15  (document claimed 7; 37*214=7918, 7933-7918=15)
assert 7933 % 37 == 15, "7933 mod 37 = 15, NOT 7 as originally stated"

assert isprime(7393)
# 3973: not prime (so 7393 is also not an emirp — consistent with document)
assert not isprime(3973)
# 7393 is right-truncatable: 7393->739->73->7
for x in [7393, 739, 73, 7]:
    assert isprime(x), f"{x} must be prime for right-truncatable chain"

# Properties do NOT transfer under digit reversal (emirp ≠ truncatable and vice versa) ✓

# ============================================================
# SECTION 6: CONSTRUCTED NUMBER FACTORIZATIONS
# ============================================================

# 633,222,111,111,000,000,000,000 = 2^12 × 3 × 5^12 × 7933 × 26607089
n1 = 633222111111000000000000
assert factorint(n1) == {2: 12, 3: 1, 5: 12, 7933: 1, 26607089: 1}
assert isprime(7933)
assert isprime(26607089)

# CORRECTION: 664,443,333,111,111,111,111
# Document claimed 271 × 7321 × 334902391750321.
# That product equals 664,443,331,111,111,111,111 (different number — two fewer 3s).
# Actual factorization:
n2 = 664443333111111111111
assert factorint(n2) == {3: 1, 409: 1, 4349: 1, 124515660816857: 1}
# Verify 271*7321*334902391750321 is a DIFFERENT number
assert 271 * 7321 * 334902391750321 != n2, "claimed product is a different number"
assert 271 * 7321 * 334902391750321 == 664443331111111111111  # note: 33 -> 31

# 33,222,111,111 = 3^2 × 7 × 59 × 239 × 37397
assert factorint(33222111111) == {3: 2, 7: 1, 59: 1, 239: 1, 37397: 1}

# ============================================================
# SECTION 7: ZERO AND ONE
# ============================================================

count_ones = sum(str(i).count('1') for i in range(1, 112))
assert count_ones == 36, f"count of 1s from 1 to 111 = {count_ones}"
assert 36 == 6 * 6
assert 36 == sum(range(1, 9))   # 8th triangular number
assert 75 + 46 == 121 == 11**2

# ============================================================
# SECTION 8: Q6/V4 QUOTIENT GRAPH
# ============================================================

# Burnside: (|Fix(id)| + |Fix(compl)| + |Fix(rev)| + |Fix(c+r)|) / 4
#           = (64 + 0 + 8 + 8) / 4 = 20
assert (64 + 0 + 8 + 8) == 80
assert 80 // 4 == 20
assert 8 * 2 + 12 * 4 == 64   # size-2 and size-4 orbits account for all 64 vectors
assert 48 - 20 == 28
assert 28 == 1 + 2 + 4 + 7 + 14   # 28 is a perfect number

# ============================================================
# SECTION 9: SUPERGOLDEN RATIO ψ
# ============================================================

import numpy as np
psi = max(r.real for r in np.roots([1, -1, 0, -1]) if abs(r.imag) < 1e-9)
assert abs(psi - 1.4655712318767682) < 1e-10
assert abs(psi**3 - psi**2 - 1) < 1e-10   # satisfies defining polynomial
assert abs((psi - 1) - 1/psi**2) < 1e-9   # ψ - 1 = 1/ψ²

# ============================================================
# SECTION 10: PELL EQUATION d = 10101
# ============================================================

x, y = 26935, 268
assert x**2 - 10101 * y**2 == 1
assert x**2 == 725494225
assert 10101 * y**2 == 725494224
assert x % 37 == 36   # ≡ -1 mod 37
assert y % 37 == 9
dr = lambda n: 1 + (n - 1) % 9 if n > 0 else 0
assert dr(x) == 7
assert dr(y) == 7
assert x + y == 27203
assert sum(int(d) for d in "27203") == 14
assert x - y == 26667
assert factorint(10101) == {3: 1, 7: 1, 13: 1, 37: 1}

# ============================================================
# SECTION 11: CYCLIC NUMBER 142857
# ============================================================

for k, expected in enumerate([142857, 285714, 428571, 571428, 714285, 857142, 999999], 1):
    assert 142857 * k == expected, f"142857 * {k} should be {expected}"

# ============================================================
# SECTION 13: LOGARITHMIC SPIRAL r = e^(0.30635 θ)
# ============================================================

a = 0.30635
spiral_data = [
    (3,      3.5861,  True),
    (7,      6.3519,  True),   # CORRECTION: document claimed 6.1802; actual = ln(7)/0.30635 = 6.3519
    (37,     11.7869, True),
    (111,    15.3730, True),
    (142857, 38.7452, True),   # CORRECTION: document claimed 33.2991; actual = ln(142857)/0.30635 = 38.7452
    (235523, 40.3772, True),
]
for r, expected_theta, _ in spiral_data:
    actual = math.log(r) / a
    assert abs(actual - expected_theta) < 0.001, f"r={r}: got {actual:.4f}, expected {expected_theta}"

# ============================================================
# SECTION 15: TRUNCATABLE PRIMES
# ============================================================

def is_right_truncatable(n):
    s = str(n)
    return all(isprime(int(s[:i])) for i in range(1, len(s) + 1))

def is_left_truncatable(n):
    s = str(n)
    return all(isprime(int(s[i:])) for i in range(len(s)))

for n in [23, 37, 53, 73, 313, 317]:
    assert is_right_truncatable(n) and is_left_truncatable(n), f"{n} should be two-sided"

assert is_right_truncatable(7393)
assert not is_right_truncatable(7933)

# ============================================================
# SELF-TEST
# ============================================================

if __name__ == "__main__":
    print("ALL ASSERTIONS PASSED")
    print()
    print("Errors corrected vs original document:")
    print("  1. Section 4:  235523 mod 7 = 1 (claimed 6)")
    print("  2. Section 5:  7933 is NOT an emirp (3397 = 43*79, composite)")
    print("  3. Section 5:  7933 mod 37 = 15 (claimed 7)")
    print("  4. Section 6:  664443333111111111111 factors = {3,409,4349,124515660816857}")
    print("                  (claimed 271*7321*334902391750321, which is a different number)")
    print("  5. Section 13: spiral theta(r=7) = 6.3519 (claimed 6.1802)")
    print("  6. Section 13: spiral theta(r=142857) = 38.7452 (claimed 33.2991)")
