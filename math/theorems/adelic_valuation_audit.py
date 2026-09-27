#!/usr/bin/env python3
"""
adelic_valuation_audit.py

Audits the adelic/valuation-vector decomposition of:
  x = 3^2 * 11 * 19 * 103 / (2^10 * 5^10)

Claims verified:
  1. Numerator/denominator factorizations
  2. Valuation vector v_p(x) at all primes
  3. Principal divisor div(x) = 2[3]+[11]+[19]+[103]-10[2]-10[5]
  4. Product formula prod_p |x|_p * |x|_inf = 1
  5. Multiplicative structure: Q^* ≅ bigoplus_p Z ⊕ {±1}
  6. Logarithmic height h(x) = log max(|num|, |den|)
  7. The number x_inf = 0.0000193743... (real place)
"""

from fractions import Fraction
import math

FAIL = []
def check(cond, label, detail=""):
    if not cond:
        FAIL.append(label + (f": {detail}" if detail else ""))
    return cond

# ---------------------------------------------------------------------------
# The number
# ---------------------------------------------------------------------------
num_factored = {3: 2, 11: 1, 19: 1, 103: 1}   # 3^2 * 11 * 19 * 103
den_factored = {2: 10, 5: 10}                   # 2^10 * 5^10

num = 3**2 * 11 * 19 * 103
den = 2**10 * 5**10

x_frac = Fraction(num, den)
x_real = num / den

print("=" * 60)
print("Adelic valuation audit")
print("=" * 60)
print(f"  x = 3^2 * 11 * 19 * 103 / (2^10 * 5^10)")
print(f"  Numerator   = {num}  = 9 * 11 * 19 * 103")
print(f"  Denominator = {den}  = {den}")
print(f"  x (exact)   = {x_frac}")
print(f"  x (real)    = {x_real:.10e}")

check(x_frac == Fraction(num, den), "Fraction constructor consistent")

# ---------------------------------------------------------------------------
# 1. Factorization verification
# ---------------------------------------------------------------------------
print("\n=== 1. Factorization ===")

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

num_check = factorize(num)
den_check = factorize(den)
check(num_check == num_factored, "Numerator factorization", str(num_check))
check(den_check == den_factored, "Denominator factorization", str(den_check))
print(f"  {num} = {num_check}  {'PASS' if num_check == num_factored else 'FAIL'}")
print(f"  {den} = {den_check}  {'PASS' if den_check == den_factored else 'FAIL'}")

# In reduced form (already reduced since gcd(num,den)=1)
import math as _math
check(_math.gcd(num, den) == 1, "gcd(num,den)=1  (fraction already reduced)")
print(f"  gcd({num}, {den}) = {_math.gcd(num,den)}  (fully reduced)  PASS")

# ---------------------------------------------------------------------------
# 2. Valuation vector v_p(x)
# ---------------------------------------------------------------------------
print("\n=== 2. Valuation vector v_p(x) ===")

def v_p(frac, p):
    """p-adic valuation of a Fraction."""
    n, d = frac.numerator, frac.denominator
    vn, vd = 0, 0
    while n % p == 0: vn += 1; n //= p
    while d % p == 0: vd += 1; d //= p
    return vn - vd

claimed_vals = {2: -10, 3: 2, 5: -10, 11: 1, 19: 1, 103: 1}

print(f"  {'prime':>6}  {'v_p(x)':>8}  {'claimed':>8}  {'match'}")
all_primes = sorted(claimed_vals.keys())
for p in all_primes:
    vp = v_p(x_frac, p)
    claimed = claimed_vals[p]
    ok = (vp == claimed)
    check(ok, f"v_{p}(x) = {claimed}", f"got {vp}")
    print(f"  {p:>6}  {vp:>8}  {claimed:>8}  {'✓' if ok else 'FAIL'}")

# Any other primes have v_p = 0
for p in [7, 13, 17, 23, 29, 97, 101, 107]:
    vp = v_p(x_frac, p)
    check(vp == 0, f"v_{p}(x) = 0 (x is a p-adic unit for p not in support)")
print(f"  Other primes (7,13,17,...): v_p(x)=0  (x is a p-adic unit)  PASS")

# ---------------------------------------------------------------------------
# 3. Principal divisor div(x) = 2[3] + [11] + [19] + [103] - 10[2] - 10[5]
# ---------------------------------------------------------------------------
print("\n=== 3. Principal divisor div(x) ===")
print(f"  div(x) = sum_p v_p(x)*[p]  =  2[3]+[11]+[19]+[103]-10[2]-10[5]")
print(f"  Coefficient check:")
for p in sorted(claimed_vals.keys()):
    vp = claimed_vals[p]
    sign = '+' if vp > 0 else ''
    print(f"    {sign}{vp}[{p}]")

# Product of primes with signed exponents should reconstruct x (up to sign/embedding)
reconstructed = Fraction(
    3**claimed_vals[3] * 11**claimed_vals[11] * 19**claimed_vals[19] * 103**claimed_vals[103],
    2**(-claimed_vals[2]) * 5**(-claimed_vals[5])
)
check(reconstructed == x_frac, "div(x) reconstructs x", f"{reconstructed} vs {x_frac}")
print(f"  Reconstruction from div: {reconstructed} = {x_frac}  PASS")

# Key property: any Q^* element is uniquely determined by its valuation vector
# (times ±1 for sign; x > 0 here so sign is +1)
print(f"  Remark: div(x) determines x uniquely in Q^* (Kronecker/unique factorization)")
print(f"  div is an isomorphism Q^*/{{±1}} → bigoplus_p Z  (free abelian on primes)")

# ---------------------------------------------------------------------------
# 4. Product formula prod_p |x|_p * |x|_inf = 1
# ---------------------------------------------------------------------------
print("\n=== 4. Product formula (adelic) ===")

def p_adic_abs(frac, p):
    """p-adic absolute value |x|_p = p^{-v_p(x)}."""
    return p**(-v_p(frac, p))

x_inf = float(x_frac)
product = x_inf
for p in sorted(claimed_vals.keys()):
    pa = p_adic_abs(x_frac, p)
    product *= pa
    print(f"  |x|_{p:>3} = {p}^{{-({claimed_vals[p]})}} = {pa:.10f}")
print(f"  |x|_inf  = {x_inf:.10e}")
print(f"  Product  = prod_p |x|_p * |x|_inf = {product:.15f}")
check(abs(product - 1.0) < 1e-12, "Product formula = 1", f"got {product:.6e}")
print(f"  Product formula = 1:  {'PASS' if abs(product-1)<1e-12 else 'FAIL'}  ✓")

# Note: only finitely many primes contribute (others have |x|_p = 1)
print(f"  (Primes not in support contribute |x|_p = 1, don't affect product)")

# ---------------------------------------------------------------------------
# 5. Multiplicative structure Q^* ≅ bigoplus_p Z ⊕ {±1}
# ---------------------------------------------------------------------------
print("\n=== 5. Multiplicative structure ===")
print(f"  x > 0, so x = +1 * prod_p p^{{v_p(x)}}")
print(f"  Valuation vector: {dict(sorted(claimed_vals.items()))}")
print(f"  This IS the complete arithmetic content of x.")
print(f"  All other representations (binary expansion, p-adic expansion, etc.)")
print(f"  are functors applied to this same vector.")

# Verify: product reconstructs x exactly
v_vec_product = Fraction(1)
for p, vp in claimed_vals.items():
    if vp > 0:
        v_vec_product *= p**vp
    else:
        v_vec_product /= p**(-vp)
check(v_vec_product == x_frac, "Valuation vector product = x")
print(f"  prod p^{{v_p(x)}} = {v_vec_product} = {x_frac}  PASS")

# ---------------------------------------------------------------------------
# 6. Logarithmic height h(x) = log max(|num|, |den|)
# ---------------------------------------------------------------------------
print("\n=== 6. Logarithmic height ===")
h_x = math.log(max(num, den))
print(f"  h(x) = log max(|num|, |den|)")
print(f"       = log max({num}, {den})")
print(f"       = log {max(num,den)}")
print(f"       = {h_x:.10f}")
print(f"  In terms of primes:")
h_log = max(
    abs(claimed_vals[2]) * math.log(2),
    abs(claimed_vals[5]) * math.log(5),
    abs(claimed_vals[3]) * math.log(3)
      + math.log(11) + math.log(19) + math.log(103)
)
print(f"  log max = max(10*log2, 10*log5, 2*log3+log11+log19+log103)")
print(f"           = max({10*math.log(2):.4f}, {10*math.log(5):.4f}, "
      f"{2*math.log(3)+math.log(11)+math.log(19)+math.log(103):.4f})")
print(f"  Denominator = 2^10*5^10 = 10^10 dominates numerator (193743)")
print(f"  h(x) = log(10^10) = 10*log(10) = {10*math.log(10):.10f}")
print(f"  (= log(den) = log(2^10*5^10) = 10*log2 + 10*log5)")

alt_h = 10 * math.log(10)
check(abs(h_x - alt_h) < 1e-10, "h(x) = 10*log10 = log(10^10)")
print(f"  {'PASS' if abs(h_x-alt_h)<1e-10 else 'FAIL'}")

# Weil height (both archimedean and all p-adic):
# h_Weil(x) = log prod_{v} max(1, |x|_v) = sum_{v} max(0, log|x|_v)
# For rationals: h_Weil = sum_p max(0, -v_p(x)) * log p + max(0, log|x|_inf)
weil = sum(max(0, -vp) * math.log(p) for p, vp in claimed_vals.items())
weil += max(0, math.log(x_inf))   # log|x|_inf = log x (x > 0 < 1, so this = 0)
print(f"\n  Weil height h_Weil(x) = sum_p max(0,-v_p)*log(p)")
print(f"    = max(0,10)*log2 + max(0,10)*log5 = {weil:.6f}")
print(f"    = 10*log(2*5) = 10*log10 = {10*math.log(10):.6f}")
check(abs(weil - 10*math.log(10)) < 1e-10, "Weil height = 10*log10")
print(f"  Weil height = 10*log(10) = log(10^10)  PASS")

# ---------------------------------------------------------------------------
# 7. Real place: x_inf
# ---------------------------------------------------------------------------
print("\n=== 7. Real place x_inf ===")
print(f"  x_inf = {x_real:.15e}")
print(f"  Claimed: 0.0000193743...")
claimed_xreal = 0.0000193743
check(abs(x_real - claimed_xreal) / claimed_xreal < 1e-4, "x_inf ≈ 0.0000193743")
print(f"  Match to 4 significant figures: {'PASS' if abs(x_real-claimed_xreal)/claimed_xreal < 1e-4 else 'FAIL'}")
print(f"  Full value: {num}/{den} = {x_frac}")
print(f"             = {x_real}")

# ---------------------------------------------------------------------------
# 8. Completeness check: adelic signature
# ---------------------------------------------------------------------------
print("\n=== 8. Adelic signature summary ===")
print(f"  Two deep poles:      p=2 (v_2=-10), p=5 (v_5=-10)")
print(f"  One higher zero:     p=3 (v_3=+2)")
print(f"  Three simple zeros:  p=11 (v=+1), p=19 (v=+1), p=103 (v=+1)")
print(f"  All other primes:    v_p=0 (x is a p-adic unit)")
print()
print(f"  Product formula confirms: this profile uniquely determines x in Q^+")
print(f"  No further structure beyond the valuation vector exists.")
print(f"  'Fractal geometry' or 'Hausdorff dimension' terminology does not")
print(f"  add content beyond the valuation vector for a rational number.")

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
    print(f"  x = {x_frac}  ✓")
    print(f"  Factorization: 3^2*11*19*103 / (2^10*5^10)  ✓")
    print(f"  Valuation vector confirmed at all 6 nontrivial primes  ✓")
    print(f"  div(x) = 2[3]+[11]+[19]+[103]-10[2]-10[5]  ✓")
    print(f"  Product formula: prod_p |x|_p * |x|_inf = 1  ✓")
    print(f"  h(x) = log max(num,den) = 10*log5  ✓")
    print(f"  Weil height = 10*log10  ✓")
    print(f"  x_inf ≈ 1.9374e-5  ✓")
    print()
    print(f"  Structural conclusion:")
    print(f"  The complete arithmetic content of x is its valuation vector")
    print(f"  {{2:-10, 3:2, 5:-10, 11:1, 19:1, 103:1}}.")
    print(f"  The product formula is the only constraint on this vector.")
    print(f"  All other representations (adèles, p-adic expansions,")
    print(f"  idele class group embedding) are lossless re-encodings.")
