#!/usr/bin/env python3
"""
cyclic142857_audit.py

Audits all claims about 248%, 1/7, 142857, and the decimal structure of 3844/4375.

Claims verified:
  1. 248% = 62/25 (exact reduction)
  2. 248%/248%/7 = 1/7 (arithmetic)
  3. 1/7 = 0.142857 repeating
  4. 142857 = 3^3 × 11 × 13 × 37
  5. 999999 = 10^6 - 1 = 7 × 142857
  6. ord_7(10) = 6  (10 is primitive root mod 7)
  7. 142857 × k for k=1..6 are cyclic permutations of {1,4,2,8,5,7}
  8. (62/25)^2 / 7 = 3844/4375
  9. 4375 = 5^4 × 7
  10. Decimal split: 4 non-repeating digits + period-6 tail for 3844/4375
  11. 10 is a primitive root mod 7  (ord_7(10) = phi(7) = 6)
  12. Product formula / local factor split for rational denominators
"""

from fractions import Fraction
import math

FAIL = []
def check(cond, label, detail=""):
    if not cond:
        FAIL.append(label + (f": {detail}" if detail else ""))
    return cond

print("=" * 60)
print("142857 / cyclic 1/7 audit")
print("=" * 60)

# ---------------------------------------------------------------------------
# 1. 248% = 62/25
# ---------------------------------------------------------------------------
print("\n=== 1. 248% = 62/25 ===")
pct248 = Fraction(248, 100)
check(pct248 == Fraction(62, 25), "248% = 62/25")
print(f"  248/100 = {pct248} = 62/25  {'PASS' if pct248 == Fraction(62,25) else 'FAIL'}")

# ---------------------------------------------------------------------------
# 2. 248%/248%/7 = 1/7
# ---------------------------------------------------------------------------
print("\n=== 2. 248%/248%/7 = 1/7 ===")
expr_div = pct248 / pct248 / 7
check(expr_div == Fraction(1, 7), "248%/248%/7 = 1/7")
print(f"  (62/25) / (62/25) / 7 = {expr_div}  {'PASS' if expr_div == Fraction(1,7) else 'FAIL'}")

# ---------------------------------------------------------------------------
# 3. 1/7 decimal expansion
# ---------------------------------------------------------------------------
print("\n=== 3. 1/7 = 0.142857 repeating ===")

def repeating_decimal(p, q):
    """Returns (finite_part, repeating_block) for fraction p/q in lowest terms."""
    f = Fraction(p, q)
    p2, q2 = f.numerator, f.denominator
    # Remove factors of 2 and 5 from denominator
    a, b = 0, 0
    qq = q2
    while qq % 2 == 0: qq //= 2; a += 1
    while qq % 5 == 0: qq //= 5; b += 1
    finite_len = max(a, b)
    # Shift: multiply by 10^finite_len
    shifted = f * 10**finite_len
    # Now shifted has denominator qq (coprime to 10)
    snum, sden = shifted.numerator, shifted.denominator
    # Integer part
    int_part = snum // sden
    rem = snum % sden
    # Repeating: ord_{sden}(10) gives period length
    period = []
    seen = {}
    r = rem
    while r not in seen:
        seen[r] = len(period)
        r = (r * 10) % sden
        period.append((r * 10 // sden + (sden - r) // sden * 0))
        # Re-do: digit = (r_prev * 10) // sden
    # Redo cleanly
    digits = []
    r = rem
    seen2 = {}
    while r not in seen2:
        seen2[r] = len(digits)
        d = (r * 10) // sden
        r = (r * 10) % sden
        digits.append(d)
    start = seen2[r]
    finite_digits = digits[:start]
    repeat_digits = digits[start:]
    return int_part, finite_digits, repeat_digits, finite_len

int_part, finite_d, repeat_d, flen = repeating_decimal(1, 7)
repeat_block = ''.join(map(str, repeat_d))
check(repeat_block == '142857', "1/7 repeating block = 142857")
print(f"  1/7 = 0.{repeat_block} repeating")
print(f"  Repeating block: {repeat_block}  {'PASS' if repeat_block == '142857' else 'FAIL'}")
print(f"  Block length: {len(repeat_d)}  (= ord_7(10) = 6)")

# Verify numerically
val_1_7 = 0
for k, d in enumerate(repeat_d * 20, 1):
    val_1_7 += d / 10**k
check(abs(val_1_7 - 1/7) < 1e-15, "Decimal series converges to 1/7")
print(f"  Numerical check: {val_1_7:.15f} ≈ 1/7 = {1/7:.15f}  PASS")

# ---------------------------------------------------------------------------
# 4. Factorization of 142857
# ---------------------------------------------------------------------------
print("\n=== 4. 142857 = 3^3 × 11 × 13 × 37 ===")

def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

rep = 142857
fac = factorize(rep)
claimed_fac = {3: 3, 11: 1, 13: 1, 37: 1}
check(fac == claimed_fac, "142857 = 3^3 * 11 * 13 * 37", str(fac))
print(f"  142857 = {fac}  {'PASS' if fac == claimed_fac else 'FAIL'}")
print(f"  = 27 × 11 × 13 × 37 = {27*11*13*37}")
check(27 * 11 * 13 * 37 == 142857, "27*11*13*37 = 142857")

# 142857 / 37 = 3861 = 3^3 * 11 * 13
check(142857 % 37 == 0, "37 | 142857")
q = 142857 // 37
check(q == 3861, f"142857/37 = 3861", str(q))
fac_q = factorize(q)
check(fac_q == {3: 3, 11: 1, 13: 1}, f"3861 = 3^3*11*13", str(fac_q))
print(f"  142857 / 37 = {q} = {fac_q}  PASS")

# ---------------------------------------------------------------------------
# 5. 999999 = 10^6 - 1 = 7 × 142857
# ---------------------------------------------------------------------------
print("\n=== 5. 999999 = 10^6 - 1 = 7 × 142857 ===")
check(10**6 - 1 == 999999, "10^6 - 1 = 999999")
check(999999 == 7 * 142857, "999999 = 7 × 142857")
check(999999 % 7 == 0, "7 | 999999")
print(f"  10^6 - 1 = {10**6 - 1}")
print(f"  7 × 142857 = {7*142857}")
print(f"  Equal: {'PASS' if 10**6-1 == 7*142857 else 'FAIL'}")
fac_999999 = factorize(999999)
print(f"  999999 = {fac_999999}")
print(f"  = 3^3 × 7 × 11 × 13 × 37  (combines factor 7 with 142857's factors)")
check(fac_999999 == {3: 3, 7: 1, 11: 1, 13: 1, 37: 1}, "999999 factorization")

# ---------------------------------------------------------------------------
# 6. ord_7(10) = 6
# ---------------------------------------------------------------------------
print("\n=== 6. Multiplicative order ord_7(10) = 6 ===")
print(f"  Powers of 10 mod 7:")
powers = []
for k in range(1, 8):
    pk = pow(10, k, 7)
    powers.append(pk)
    print(f"  10^{k} ≡ {pk} (mod 7){'  <- 1 (period found)' if pk == 1 and k == 6 else ''}")

ord10_7 = next(k for k, v in enumerate(powers, 1) if v == 1)
check(ord10_7 == 6, f"ord_7(10) = 6", f"got {ord10_7}")
print(f"  ord_7(10) = {ord10_7}  {'PASS' if ord10_7 == 6 else 'FAIL'}")
print(f"  φ(7) = 6  (7 is prime);  ord_7(10) = φ(7) => 10 is primitive root mod 7")
check(ord10_7 == 6, "10 is primitive root mod 7 (ord = phi(7))")

# The six residues 10^k mod 7 for k=1..6
res = [pow(10, k, 7) for k in range(1, 7)]
check(sorted(res) == [1, 2, 3, 4, 5, 6], "10^1..10^6 hit all residues mod 7")
print(f"  Residues {{10^k mod 7 : k=1..6}} = {sorted(res)} = Z/7Z*  PASS")

# ---------------------------------------------------------------------------
# 7. Cyclic multiplication table
# ---------------------------------------------------------------------------
print("\n=== 7. 142857 × k cyclic permutations ===")
base_digits = '142857'
print(f"  {'k':>3}  {'product':>10}  {'digits':>8}  {'cyclic permutation?'}")
all_cyclic = True
for k in range(1, 7):
    prod = 142857 * k
    prod_str = str(prod)
    # Is prod_str a cyclic permutation of '142857'?
    is_cyclic = (prod_str in base_digits + base_digits) and len(prod_str) == 6
    check(is_cyclic, f"142857×{k} is cyclic permutation of 142857", prod_str)
    all_cyclic = all_cyclic and is_cyclic
    print(f"  {k:>3}  {prod:>10}  {prod_str:>8}  {'✓' if is_cyclic else 'FAIL'}")

check(142857 * 7 == 999999, "142857 × 7 = 999999")
print(f"  {7:>3}  {142857*7:>10}  (999999 — one less than 10^6)  ✓")
print(f"  All k=1..6 are cyclic permutations: {'PASS' if all_cyclic else 'FAIL'}")

# Connection to ord_7(10): cyclic shifts correspond to k * (1/7) for different k
print()
print("  Connection: 1/7 = 0.142857..., 2/7 = 0.285714..., 3/7 = 0.428571..., etc.")
for k in range(1, 7):
    _, _, rep_k, _ = repeating_decimal(k, 7)
    print(f"  {k}/7: repeating block = {''.join(map(str, rep_k))}")

# ---------------------------------------------------------------------------
# 8. (62/25)^2 / 7 = 3844/4375
# ---------------------------------------------------------------------------
print("\n=== 8. (62/25)^2 / 7 = 3844/4375 ===")
expr_mul = pct248 * pct248 / 7
claimed = Fraction(3844, 4375)
check(expr_mul == claimed, "(62/25)^2 / 7 = 3844/4375")
print(f"  (62/25)^2 = {62**2}/{25**2} = {Fraction(62**2, 25**2)}")
print(f"  / 7 = {Fraction(62**2, 25**2 * 7)}")
print(f"  = {expr_mul}  {'PASS' if expr_mul == claimed else 'FAIL'}")

# ---------------------------------------------------------------------------
# 9. 4375 = 5^4 × 7
# ---------------------------------------------------------------------------
print("\n=== 9. 4375 = 5^4 × 7 ===")
fac_4375 = factorize(4375)
check(fac_4375 == {5: 4, 7: 1}, "4375 = 5^4 × 7")
print(f"  4375 = {fac_4375}  {'PASS' if fac_4375 == {5:4,7:1} else 'FAIL'}")
check(5**4 * 7 == 4375, "5^4 * 7 = 4375")
print(f"  5^4 × 7 = {5**4} × 7 = {5**4*7}  PASS")

# ---------------------------------------------------------------------------
# 10. Decimal split for 3844/4375
# ---------------------------------------------------------------------------
print("\n=== 10. Decimal expansion of 3844/4375 ===")

# Denominator = 5^4 × 7; non-repeating length = max(0,4) = 4; period = ord_7(10) = 6
int_part2, finite_d2, repeat_d2, flen2 = repeating_decimal(3844, 4375)
finite_str = ''.join(map(str, finite_d2))
repeat_str = ''.join(map(str, repeat_d2))
print(f"  3844/4375 = 0.{finite_str}|{repeat_str} (bar over {repeat_str})")
print(f"  Non-repeating length: {flen2}  (from 5^4 factor)")
print(f"  Period length: {len(repeat_d2)}  (from 7 factor, = ord_7(10) = 6)")

check(flen2 == 4, "Non-repeating length = 4", str(flen2))
check(len(repeat_d2) == 6, "Period length = 6", str(len(repeat_d2)))

# Numerical check
val_num = float(Fraction(3844, 4375))
print(f"  Decimal: {val_num:.15f}")
print(f"  Claimed: 0.878628571428571...")

# Check that the repeating block is a cyclic shift of 142857
check(repeat_str in '142857142857', f"Repeating block {repeat_str} is cyclic shift of 142857")
print(f"  Repeating block {repeat_str} ∈ cyclic shifts of 142857:  "
      f"{'PASS' if repeat_str in '142857142857' else 'FAIL'}  ✓")

# The finite prefix + period structure:
# 3844/4375 = N/(5^4 × 7) → multiply by 10^4: 3844×10^4 / (5^4×7) = 3844×2^4/7
prefix_shifted = Fraction(3844 * 10**4, 4375)
int_shifted = int(prefix_shifted)
frac_shifted = prefix_shifted - int_shifted
print(f"\n  × 10^4: 3844×10^4/4375 = {int_shifted} + {frac_shifted}")
print(f"  Integer part gives first 4 digits: {str(int_shifted)[:4]} (= 8786)")
print(f"  Fractional part = {frac_shifted} = {float(frac_shifted):.6f}")
print(f"  = {frac_shifted} × (repeating 1/7 orbit)")
print(f"  {frac_shifted} / (1/7) = {frac_shifted * 7}  "
      f"(→ this/7 = 2/7 = 0.285714... cycle)")

# 2/7 confirmation
_, _, rep_2_7, _ = repeating_decimal(2, 7)
print(f"  2/7 repeating block: {''.join(map(str, rep_2_7))} ✓  (= 285714 = 142857×2 cyclic)")

# ---------------------------------------------------------------------------
# 11. Local factor split: structural interpretation
# ---------------------------------------------------------------------------
print("\n=== 11. Local factor split ===")
print(f"  For x = p/q with q = 2^a × 5^b × m, gcd(m,10)=1:")
print(f"  - Finite prefix length = max(a, b)")
print(f"  - Period length = ord_m(10)")
print()
print(f"  x = 3844/4375 = 3844 / (2^0 × 5^4 × 7):")
print(f"    a=0, b=4 → finite length = max(0,4) = 4  ✓")
print(f"    m=7 → period = ord_7(10) = 6  ✓")
print()
print(f"  x = 1/7 = 1 / (2^0 × 5^0 × 7):")
print(f"    a=0, b=0 → finite length = 0  (purely periodic)  ✓")
print(f"    m=7 → period = ord_7(10) = 6  ✓")
print()

# Verify the split claim for 3844/4375 generically
# Finite part arises from: after multiplying by 10^max(a,b) the denominator is coprime to 10
q_remaining = 4375
a, b = 0, 4  # from factorization
for _ in range(b): q_remaining //= 5
for _ in range(a): q_remaining //= 2
check(q_remaining == 7, f"After removing 2^0×5^4, remaining denominator = 7", str(q_remaining))
check(math.gcd(q_remaining, 10) == 1, "Remaining denominator coprime to 10")
print(f"  After × 10^4: residual denominator = {q_remaining} (coprime to 10, generates period)  PASS")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
if FAIL:
    print(f"FAILED ({len(FAIL)}):")
    for f in FAIL:
        print(f"  FAIL  {f}")
    import sys; sys.exit(1)
else:
    print("ALL CHECKS PASS")
    print()
    print("  248% = 62/25  ✓")
    print("  248%/248%/7 = 1/7  ✓")
    print("  1/7 = 0.142857̄  ✓")
    print("  142857 = 3^3 × 11 × 13 × 37  ✓")
    print("  999999 = 10^6-1 = 7 × 142857  ✓")
    print("  ord_7(10) = 6 = φ(7) => 10 primitive root mod 7  ✓")
    print("  142857 × k (k=1..6): all cyclic permutations of {1,4,2,8,5,7}  ✓")
    print("  (62/25)^2/7 = 3844/4375  ✓")
    print("  4375 = 5^4 × 7  ✓")
    print("  3844/4375 = 0.8786|285714̄ (4 finite + period-6 tail)  ✓")
    print("  Local split: finite part from {2,5}, periodic from primes coprime to 10  ✓")
    print()
    print("  Cyclic table (142857 × k mod-digit permutation):")
    for k in range(1, 7):
        _, _, rk, _ = repeating_decimal(k, 7)
        print(f"    {k}/7 = 0.{''.join(map(str,rk))}̄   (= 142857×{k} / 999999)")
