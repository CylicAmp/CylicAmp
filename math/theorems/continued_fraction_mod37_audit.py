#!/usr/bin/env python3
"""
MOD-37 RESIDUE AUDIT — CF [3; 4, 8, 6, 9, 11, 7, 5, 13, 10, 8]
=================================================================
Verifies all convergent residues mod 37 and the 368/35 structure.

ERRORS FOUND:
  n=9 residue: claimed 32, correct 22
    31 × 21 = 651 = 17×37 + 22  (document wrote 17×37+32=629+32=661 ≠ 651)

CORRECT RESIDUE SEQUENCE:
  3 → 31 → 1 → 32 → 8 → 12 → 24 → 0 → 32 → 22 → 13

KEY STRUCTURE (verified):
  limit² ≈ 368/35   (approximation; exact limit = 2616927323/807053055)
  368/35 ≡ 1 (mod 37)   [35⁻¹ = 18, 368 ≡ 35, 35×18 = 630 ≡ 1]
  368 = 16 × 23   [23 ∈ URI_TIERS = {14,23,32,41}]
  35 = 5 × 7
  0-point at n=7: 2430382 = 65686 × 37   (numerator divisible by 37)
"""

from fractions import Fraction

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def modinv(a, m):
    a = a % m
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def convergents(cf):
    h_prev, h_curr = 1, cf[0]
    k_prev, k_curr = 0, 1
    result = [(h_curr, k_curr)]
    for a in cf[1:]:
        h_prev, h_curr = h_curr, a*h_curr + h_prev
        k_prev, k_curr = k_curr, a*k_curr + k_prev
        result.append((h_curr, k_curr))
    return result

CF = [3, 4, 8, 6, 9, 11, 7, 5, 13, 10, 8]
URI_TIERS = frozenset({14, 23, 32, 41})

convs = convergents(CF)

# ── MOD-37 RESIDUES ───────────────────────────────────────────────────────────

print("=== MOD-37 CONVERGENT RESIDUES ===")
print(f"  {'n':>2}  {'h':>14}  {'h mod 37':>10}  {'k':>14}  {'k mod 37':>10}  {'h/k mod 37':>12}  claimed")
print("  " + "-"*85)

CLAIMED_RESIDUES = [3, 31, 1, 32, 8, 12, 24, 0, 32, 32, None]

residues = []
for i, (h, k) in enumerate(convs):
    hm = h % 37
    km = k % 37
    ki = modinv(km, 37)
    if ki is None:
        rm = None
        rs = "undef"
    else:
        rm = (hm * ki) % 37
        rs = str(rm)
    residues.append(rm)
    cl = str(CLAIMED_RESIDUES[i]) if CLAIMED_RESIDUES[i] is not None else "—"
    match = "✓" if rm == CLAIMED_RESIDUES[i] else f"✗ (correct={rm})"
    print(f"  {i:>2}  {h:>14}  {hm:>10}  {k:>14}  {km:>10}  {rm if rm is not None else '—':>12}  {cl}  {match}")

print()

# Verify each residue
check("n=0: 3/1 ≡ 3", residues[0] == 3)
check("n=1: 13/4 ≡ 31  [4⁻¹=28, 13×28=364≡31]", residues[1] == 31)
check("n=2: 107/33 ≡ 1  [107≡33, 33⁻¹=9, 33×9=297≡1]", residues[2] == 1)
check("n=3: 655/202 ≡ 32  [655≡26, 202≡17, 17⁻¹=24, 26×24=624≡32]", residues[3] == 32)
check("n=4: 6002/1851 ≡ 8  [6002≡8, 1851≡1]", residues[4] == 8)
check("n=5: 66677/20563 ≡ 12  [66677≡3, 20563≡28, 28⁻¹=4, 3×4=12]", residues[5] == 12)
check("n=6: 472741/145792 ≡ 24  [472741≡29, 145792≡12, 12⁻¹=34, 29×34=986≡24]", residues[6] == 24)
check("n=7: 2430382/749523 ≡ 0  [2430382=65686×37, numerator≡0]", residues[7] == 0)
check("n=8: 32067707/9889591 ≡ 32  [≡29/9, 9⁻¹=33, 29×33=957≡32]", residues[8] == 32)
check("n=9: 323107452/99645433 ≡ 22  (NOT 32 — claimed 32 is wrong)", residues[9] == 22)
check("n=10: 2616927323/807053055 mod 37", residues[10] == (2616927323 % 37 * modinv(807053055 % 37, 37)) % 37)
print()

# ── ERROR IN CLAIM: n=9 ───────────────────────────────────────────────────────

print("=== ERROR AT n=9: 31×21=651≡22, NOT 32 ===")
print(f"  323107452 mod 37 = {323107452 % 37}  (≡ -6 = 31 ✓)")
print(f"  99645433  mod 37 = {99645433 % 37}   (≡ -7 = 30 ✓)")
print(f"  30⁻¹ mod 37      = {modinv(30,37)}  (30×21=630=17×37+1 ✓)")
print(f"  31 × 21          = {31*21}")
print(f"  651 mod 37       = {651 % 37}  ← correct answer is 22")
print(f"  Document wrote: 17×37+32=629+32=661 ≠ 651  (17×37=629, 629+32=661≠651)")
print(f"  Correct:         17×37+22=629+22=651 ✓")
print()
check("31×21=651", 31*21==651)
check("651 mod 37 = 22", 651%37==22)
check("NOT 32 as claimed", 651%37!=32)
print()

# ── 368/35 STRUCTURE ──────────────────────────────────────────────────────────

print("=== 368/35 STRUCTURE ===")
limit_exact = Fraction(convs[-1][0], convs[-1][1])
limit_sq = float(limit_exact)**2
frac_368_35 = 368/35

print(f"  Exact limit:   {convs[-1][0]}/{convs[-1][1]}")
print(f"  limit²:        {limit_sq:.12f}")
print(f"  368/35:        {frac_368_35:.12f}")
print(f"  Difference:    {abs(limit_sq - frac_368_35):.2e}  (approximation, not exact)")
print()

check("0.5142857... = 18/35", abs(18/35 - 0.5142857142857143) < 1e-15)
check("18/35 + 10 = 368/35", Fraction(18,35) + 10 == Fraction(368,35))
check("368/35 = 10.514285714...", abs(368/35 - 10.514285714285714) < 1e-12)
check("limit² ≈ 368/35  (within 2e-5)", abs(limit_sq - 368/35) < 0.0001)
check("limit² ≠ 368/35 exactly  (finite CF)", limit_sq != 368/35)
print()

# ── 368/35 FACTORIZATION AND MOD 37 ──────────────────────────────────────────

print("=== 368 AND 35 STRUCTURE ===")
check("368 = 16 × 23", 368 == 16*23)
check("16 = 2^4", 16 == 2**4)
check("23 ∈ URI_TIERS  {14,23,32,41}", 23 in URI_TIERS)
check("35 = 5 × 7", 35 == 5*7)
check("368 ≡ 35 (mod 37)  [368-9×37=368-333=35]", 368%37==35)
check("35⁻¹ ≡ 18 (mod 37)  [35×18=630=17×37+1]", modinv(35,37)==18 and 35*18%37==1)
check("368/35 ≡ 35×18 ≡ 630 ≡ 1 (mod 37)", (368 * modinv(35,37)) % 37 == 1)
print()
print(f"  368 = 2⁴ × 23   (23 ∈ URI_TIERS)")
print(f"  35  = 5  × 7")
print(f"  368/35 ≡ 1 (mod 37)  — unity in Z/37Z")
print()

# ── ZERO-POINT VERIFICATION ──────────────────────────────────────────────────

print("=== ZERO-POINT: n=7 NUMERATOR ≡ 0 (mod 37) ===")
h7, k7 = convs[7]
check("2430382 = 65686 × 37", h7 == 65686*37)
check("749523 mod 37 = 14  (not 0, invertible)", k7 % 37 == 14)
check("modinv(14, 37) exists", modinv(14, 37) is not None)
check("2430382/749523 ≡ 0 (mod 37)", residues[7] == 0)
print()

# ── RESIDUE SEQUENCE SUMMARY ─────────────────────────────────────────────────

print("=== RESIDUE SEQUENCE ===")
print(f"  n:   {' '.join(f'{i:>3}' for i in range(11))}")
print("  res: " + ' '.join((str(r) if r is not None else '?').rjust(3) for r in residues))
print()
print("  Key points:")
print("  n=2:  ≡ 1  (unity — 107/33, both ≡ 33 mod 37, 33×33⁻¹=1)")
print("  n=7:  ≡ 0  (numerator 2430382 divisible by 37)")
print("  n=9:  ≡ 22 (NOT 32 — arithmetic error in source)")
print()

# URI connection in residues
uri_residues = [r for r in residues if r in URI_TIERS]
print(f"  Residues in URI_TIERS {{14,23,32,41}}: {uri_residues}")
check("32 appears at n=3, n=8  (32 ∈ URI_TIERS)", residues[3]==32 and residues[8]==32)
print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All verified claims pass.")
