# math/theorems/fraction_1111_12800_audit.py
"""
Binary / Fraction Audit — 0.086796875 = 1111/12800
====================================================

Key identity:  0.086796875 × 128 = 11.11
               ⟹  0.086796875 = 11.11 / 128 = 1111 / 12800

Doubling chain (numerator and denominator both ×2, ratio fixed):
  × 128  →  11.11
  × 256  →  22.22
  × 512  →  44.44
  × 1024 →  88.88

37-field position: 1111 ≡ 1 (mod 37);  12800 ≡ 35 ≡ −2 (mod 37)
  ⟹  1111/12800 ≡ 1/(−2) ≡ −1/2 (mod 37)
  Inverse of −2 mod 37:  −2 × 18 = −36 ≡ 1 (mod 37)  ⟹  (−2)⁻¹ = 18
  ⟹  value sits at 18 in ℤ/37ℤ  (= T=1 fraction_val in the mirror table)
"""

import math
from fractions import Fraction

N = 0.086796875
P = 37

# ── Exact fraction ────────────────────────────────────────────────────────────

frac = Fraction(N).limit_denominator(100000)
assert frac == Fraction('0.086796875'), "FAIL: exact fraction mismatch"
assert frac.numerator   == 1111
assert frac.denominator == 12800

# ── Doubling chain ────────────────────────────────────────────────────────────

chain = {128: 11.11, 256: 22.22, 512: 44.44, 1024: 88.88}
for mult, expected in chain.items():
    result = N * mult
    assert abs(result - expected) < 1e-10, f"FAIL: {N} × {mult} ≠ {expected}"

# ── 37-field ──────────────────────────────────────────────────────────────────

assert 1111 % P == 1,  "FAIL: 1111 not ≡ 1 mod 37"
assert 12800 % P == 35, "FAIL: 12800 not ≡ 35 mod 37"   # 35 = −2

# inverse of −2 mod 37
inv_neg2 = pow(-2, -1, P)
assert inv_neg2 == 18, f"FAIL: (−2)⁻¹ mod 37 ≠ 18, got {inv_neg2}"

# value in ℤ/37ℤ: 1 × 18 = 18
val_mod37 = (1111 % P) * inv_neg2 % P
assert val_mod37 == 18

# ── Binary representation ─────────────────────────────────────────────────────

# 1111/12800 = 1111/(2^9 × 5^2) — NOT a finite binary fraction (factor of 5^2).
# The Python float is the nearest double; int(N × 2^30) truncates the expansion.
truncated = int(N * (2**30))
bits      = bin(truncated)
popcount  = bits.count('1')

# Confirm NOT exact: 1111 × 2^21 / 25 is not an integer
assert (1111 * (2**21)) % 25 != 0, "FAIL: unexpectedly finite binary"


# ── Report ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Binary / Fraction Audit — 0.086796875")
    print()
    print(f"  Exact fraction:    {frac}  ({frac.numerator}/{frac.denominator})")
    print(f"  Binary (×2^30):    {bits}")
    print(f"  Set bits:          {popcount}")
    print()
    print("  Doubling chain:")
    for mult, expected in chain.items():
        print(f"    × {mult:4d}  →  {N*mult}")
    print()
    print(f"  37-field:")
    print(f"    1111  mod 37 = {1111 % P}      (≡ 1 — the 37-field identity)")
    print(f"    12800 mod 37 = {12800 % P}     (≡ −2)")
    print(f"    (−2)⁻¹ mod 37 = {inv_neg2}     (18 × −2 = −36 ≡ 1)")
    print(f"    value mod 37  = {val_mod37}     (= T=1 fraction_val in mirror table)")
    print()
    print("All assertions passed.")
