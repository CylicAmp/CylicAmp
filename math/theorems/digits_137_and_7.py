"""
digits_137_and_7.py

The digits of 137 are {1, 3, 7}.  Any basic arithmetic on these digits
produces a decimal containing 142857 — because 3÷7 = 3/7, and all
fractions k/7 produce cyclic rotations of 142857.

Six calculator expressions (from images):
  11+3÷7  = 80/7  = 11.4285714286...
  11-3÷7  = 74/7  = 10.5714285714...
  11×3÷7  = 33/7  =  4.7142857143...
  1÷1+3÷7 = 10/7  =  1.4285714286...
  1÷1-3÷7 =  4/7  =  0.5714285714...
  1÷1×3÷7 =  3/7  =  0.4285714286...

All denominators reduce to 7.  All decimals are cyclic rotations of 142857.

SPLIT-COMPLEMENT THEOREM (unified):
  For prime p with ord_p(10)=k and 10^(k/2) ≡ -1 (mod p):
  the k-digit repeating block of 1/p splits at the midpoint into
  two halves summing to 10^(k/2) - 1.

  p=7:   ord₇(10)=6,   10³≡-1 (mod 7),   142+857=999    (=10³-1)
  p=137: ord₁₃₇(10)=8, 10⁴≡-1 (mod 137), 0072+9927=9999 (=10⁴-1)

α (measured) = 0.00729735256 ≈ 1/137 = 0.00729927...
"""

from fractions import Fraction
from sympy import isprime

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def repeating_block(p, length):
    """Compute the repeating decimal block of 1/p."""
    n, digits = 1, []
    for _ in range(length):
        n *= 10
        digits.append(n // p)
        n %= p
    return ''.join(str(d) for d in digits)


# ──────────────────────────────────────────────────────────────────────────────
# SIX CALCULATOR EXPRESSIONS
# ──────────────────────────────────────────────────────────────────────────────

ops = [
    ('11+3÷7',  Fraction(11) + Fraction(3, 7)),
    ('11-3÷7',  Fraction(11) - Fraction(3, 7)),
    ('11×3÷7',  Fraction(11) * Fraction(3, 7)),
    ('1÷1+3÷7', Fraction(1, 1) + Fraction(3, 7)),
    ('1÷1-3÷7', Fraction(1, 1) - Fraction(3, 7)),
    ('1÷1×3÷7', Fraction(1, 1) * Fraction(3, 7)),
]

# All results are k/7 for some k
for label, f in ops:
    assert f.denominator == 7

# The numerators
numerators = [f.numerator for _, f in ops]
assert numerators == [80, 74, 33, 10, 4, 3]

# None divisible by 7 → all produce full cyclic period
for n in numerators:
    assert n % 7 != 0

# All decimal fractional parts are cyclic rotations of 142857
ROTATIONS = {142857, 285714, 428571, 571428, 714285, 857142}
for label, f in ops:
    # Extract repeating block: multiply fractional part by 10^6
    frac_part = f - int(f)
    block = int(frac_part * 10**6)
    assert block in ROTATIONS, f"{label}: {block} not in rotations"


# ──────────────────────────────────────────────────────────────────────────────
# SPLIT-COMPLEMENT: p=7, k=6
# ──────────────────────────────────────────────────────────────────────────────

assert pow(10, 3, 7) == 6   # 10³ ≡ -1 (mod 7): 6 ≡ -1 (mod 7)
assert 6 == 7 - 1

block_7 = repeating_block(7, 6)
assert block_7 == '142857'
A7, B7 = int(block_7[:3]), int(block_7[3:])
assert A7 + B7 == 999       # = 10³ - 1


# ──────────────────────────────────────────────────────────────────────────────
# SPLIT-COMPLEMENT: p=137, k=8
# ──────────────────────────────────────────────────────────────────────────────

assert pow(10, 4, 137) == 136   # 10⁴ ≡ -1 (mod 137): 136 ≡ -1 (mod 137)
assert 136 == 137 - 1

block_137 = repeating_block(137, 8)
assert block_137 == '00729927'
A137, B137 = int(block_137[:4]), int(block_137[4:])
assert A137 + B137 == 9999      # = 10⁴ - 1

# DR of the 8-digit block
assert dr(int(block_137)) == dr(729927)   # leading zeros don't change DR
assert dr(729927) == 9    # 7+2+9+9+2+7=36→9


# ──────────────────────────────────────────────────────────────────────────────
# THE UNIFYING CONDITION: 10^(k/2) ≡ -1 (mod p)
# ──────────────────────────────────────────────────────────────────────────────

# Both 7 and 137 satisfy this — that's why both have the split-complement property
assert pow(10, 3,   7) ==   6   # ≡ -1 (mod 7)
assert pow(10, 4, 137) == 136   # ≡ -1 (mod 137)

# Consequence: 10^k ≡ 1 (mod p) — the period closes
assert pow(10, 6,   7) == 1
assert pow(10, 8, 137) == 1

# Period ratio: ord₁₃₇ / ord₇ = 8/3 (not integer — different families)
# But: lcm(6, 8) = 24 — they meet at k=24
from math import lcm, gcd
assert lcm(6, 8) == 24
assert pow(10, 24,   7) == 1
assert pow(10, 24, 137) == 1


# ──────────────────────────────────────────────────────────────────────────────
# α COMPARISON
# ──────────────────────────────────────────────────────────────────────────────

ALPHA_INV_EXACT   = 137.035999177    # CODATA measured α⁻¹
ALPHA_MEASURED    = 1 / ALPHA_INV_EXACT
ALPHA_ONE_OVER_137 = 1 / 137

assert abs(ALPHA_MEASURED - 0.007297352) < 1e-9
assert abs(ALPHA_ONE_OVER_137 - 0.007299270) < 1e-9
assert abs(ALPHA_MEASURED - ALPHA_ONE_OVER_137) < 1e-5   # close but not equal

# The repeating block of 1/137 = "00729927"
# α⁻¹ ≈ 137.036 (not exactly 137) — the .036 is the residue
# but the period-8 decimal of 1/137 satisfies split-complement


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Digits of 137 and the 7-family")
    print("=" * 62)

    print("\n── SIX OPERATIONS ──")
    for label, f in ops:
        frac_part = f - int(f)
        block = int(frac_part * 10**6)
        print(f"  {label:12s} = {str(f):6s} = {float(f):.10f}  [{block}]")

    print("\n── SPLIT-COMPLEMENT: p=7 (k=6) ──")
    print(f"  10³ mod 7 = {pow(10,3,7)}  ≡ -1 (mod 7)")
    print(f"  Block: {block_7}")
    print(f"  {block_7[:3]} + {block_7[3:]} = {A7} + {B7} = {A7+B7}  = 10³-1")

    print("\n── SPLIT-COMPLEMENT: p=137 (k=8) ──")
    print(f"  10⁴ mod 137 = {pow(10,4,137)}  ≡ -1 (mod 137)")
    print(f"  Block: {block_137}")
    print(f"  {block_137[:4]} + {block_137[4:]} = {A137} + {B137} = {A137+B137}  = 10⁴-1")
    print(f"  DR({block_137}) = DR(729927) = {dr(729927)}")

    print("\n── α COMPARISON ──")
    print(f"  1/137      = {ALPHA_ONE_OVER_137:.11f}  (period-8 repeating)")
    print(f"  α measured = {ALPHA_MEASURED:.11f}  (CODATA)")
    print(f"  difference = {ALPHA_MEASURED - ALPHA_ONE_OVER_137:.2e}")

    print("\n── UNIFYING THEOREM ──")
    print(f"  p=7:   10^(6/2)=10³ ≡ -1 (mod 7)   → 142+857=999")
    print(f"  p=137: 10^(8/2)=10⁴ ≡ -1 (mod 137) → 0072+9927=9999")
    print(f"  lcm(ord₇, ord₁₃₇) = lcm(6,8) = {lcm(6,8)}: meet at k=24")

    print()
    print("All assertions passed.")
