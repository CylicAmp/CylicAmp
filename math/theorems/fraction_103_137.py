"""
fraction_103_137.py

103/137 = 0.75182481 75182481 ...   (period-8 repeating)

The 10-digit sequence 7518248175 is the first 10 decimal digits:
  8-digit block 75182481 + first 2 digits 75 of the next cycle.

This surfaced as the fractional part of 7775/137 = 56.7518248175...

STRUCTURE:
  7775 = 56 × 137 + 103   → numerator 103, whole part 56
  digit_sum(7775) = 7+7+7+5 = 26 = SCALAR_137  (= 137 mod 37)
  103 mod 37 = 29   → 29 is in the heartbeat orbit {14, 31, 29}
  Split-complement: 7518 + 2481 = 9999 = 10⁴ - 1  (same as 1/137)
"""

from fractions import Fraction
from sympy import factorint, isprime

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def repeating_block(numerator, p, length):
    n, digits = numerator, []
    for _ in range(length):
        n *= 10
        digits.append(n // p)
        n %= p
    return ''.join(str(d) for d in digits)


SCALAR_137 = 137 % 37   # = 26
assert SCALAR_137 == 26

# ──────────────────────────────────────────────────────────────────────────────
# 103/137: THE REPEATING BLOCK
# ──────────────────────────────────────────────────────────────────────────────

# ord₁₃₇(10) = 8, so all fractions k/137 (k not mult of 137) have period 8
assert pow(10, 8, 137) == 1
assert pow(10, 4, 137) == 136   # 10⁴ ≡ -1 (mod 137)

block = repeating_block(103, 137, 16)
assert block[:8] == block[8:]   # period is exactly 8
BLOCK_103 = block[:8]
assert BLOCK_103 == '75182481'

# ──────────────────────────────────────────────────────────────────────────────
# THE 10-DIGIT SEQUENCE 7518248175
# ──────────────────────────────────────────────────────────────────────────────

# The 10-digit number = first 8 digits + first 2 of repeat
ten_digit = int(block[:10])
assert ten_digit == 7518248175
assert block[:10] == '7518248175'

# It equals 75182481 × 100 + 75  (second cycle begins 75...)
assert ten_digit == int(BLOCK_103) * 100 + int(BLOCK_103[:2])


# ──────────────────────────────────────────────────────────────────────────────
# SPLIT-COMPLEMENT: 7518 + 2481 = 9999
# ──────────────────────────────────────────────────────────────────────────────

# 10⁴ ≡ -1 (mod 137) guarantees the midpoint split sums to 10⁴-1
A, B = int(BLOCK_103[:4]), int(BLOCK_103[4:])
assert A == 7518
assert B == 2481
assert A + B == 9999    # = 10⁴ - 1

# Compare with 1/137 block '00729927': 0072 + 9927 = 9999  (same theorem)
block_1_137 = repeating_block(1, 137, 8)
assert block_1_137 == '00729927'
assert int(block_1_137[:4]) + int(block_1_137[4:]) == 9999

# Every k/137 block satisfies the split-complement: it follows from 10⁴≡-1
for k in range(1, 137):
    if k % 137 == 0:
        continue
    b = repeating_block(k, 137, 8)
    X, Y = int(b[:4]), int(b[4:])
    assert X + Y == 9999, f"k={k}: {b[:4]}+{b[4:]}={X+Y}"


# ──────────────────────────────────────────────────────────────────────────────
# DIGITAL ROOT OF THE BLOCK
# ──────────────────────────────────────────────────────────────────────────────

digit_sum_block = sum(int(d) for d in BLOCK_103)
assert digit_sum_block == 36    # 7+5+1+8+2+4+8+1 = 36
assert dr(int(BLOCK_103)) == 9  # DR(75182481) = 9


# ──────────────────────────────────────────────────────────────────────────────
# 103 IN THE HEARTBEAT ORBIT
# ──────────────────────────────────────────────────────────────────────────────

# Heartbeat orbit: successive applications of ×SCALAR_137 (mod 37)
# 14 → 31 → 29 → 14 → ...
HEARTBEAT_ORBIT = {14, 31, 29}
assert (26 * 14) % 37 == 31
assert (26 * 31) % 37 == 29
assert (26 * 29) % 37 == 14   # cycle closes

# 103 mod 37 = 29: 103 lands in the heartbeat orbit
assert 103 % 37 == 29
assert 29 in HEARTBEAT_ORBIT

# Also: 103 is prime
assert isprime(103)
assert dr(103) == 4   # 1+0+3=4


# ──────────────────────────────────────────────────────────────────────────────
# 7775/137 = 56 + 103/137
# ──────────────────────────────────────────────────────────────────────────────

assert 56 * 137 + 103 == 7775
assert Fraction(7775, 137) == Fraction(7775, 137)
assert Fraction(7775, 137) - 56 == Fraction(103, 137)

# digit_sum(7775) = 26 = SCALAR_137
assert 7 + 7 + 7 + 5 == 26
assert 26 == SCALAR_137

# DR(7775) = DR(26) = 8
assert dr(7775) == 8
assert dr(26)   == 8


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Fraction 103/137 and the sequence 7518248175")
    print("=" * 62)

    print("\n── REPEATING BLOCK ──")
    print(f"  103/137 = 0.{BLOCK_103} {BLOCK_103} ...")
    print(f"  Period: {len(BLOCK_103)} digits  (ord₁₃₇(10) = 8)")

    print("\n── 10-DIGIT SEQUENCE ──")
    print(f"  7518248175 = {BLOCK_103} + {BLOCK_103[:2]}")
    print(f"  = first 8 digits + first 2 of next cycle")

    print("\n── SPLIT-COMPLEMENT ──")
    print(f"  10⁴ mod 137 = {pow(10,4,137)}  ≡ -1 (mod 137)")
    print(f"  {BLOCK_103[:4]} + {BLOCK_103[4:]} = {A} + {B} = {A+B}  = 10⁴-1")
    print(f"  (holds for ALL k/137 fractions — structural, not coincidental)")

    print("\n── DIGITAL ROOT ──")
    print(f"  digit_sum({BLOCK_103}) = {digit_sum_block}  → DR = {dr(int(BLOCK_103))}")

    print("\n── 103 IN THE HEARTBEAT ORBIT ──")
    print(f"  SCALAR_137 = 137 mod 37 = {SCALAR_137}")
    print(f"  Heartbeat orbit (×26 mod 37): 14 → 31 → 29 → 14")
    print(f"  103 mod 37 = {103%37}  ∈ {{14, 31, 29}}  ← heartbeat position")

    print("\n── 7775/137 = 56 + 103/137 ──")
    print(f"  7775 = 56 × 137 + 103")
    print(f"  digit_sum(7775) = 7+7+7+5 = {7+7+7+5} = SCALAR_137")
    print(f"  56.7518248175... decimal matches 10-digit sequence")

    print()
    print("All assertions passed.")
