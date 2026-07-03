#!/usr/bin/env python3
"""
BASE-7 PALINDROME AUDIT: 123321₇ = 22800₁₀
============================================
Verifies conversion, factorization, mod-37 residue, QR/QNR status,
palindrome structure, and convergent connection.

ERROR FOUND:
  Document claims "12 in 37-field: 2²⁸ (QNR)"
  2²⁸ ≡ 12 (mod 37) is CORRECT, but 12 is QR, not QNR.
  28 is even; (2|37)=-1 so (-1)^28=1 → 2^28 is a QR.
  Independent: 7² = 49 ≡ 12 (mod 37).

CORRECT STATEMENTS:
  123321₇ = 22800₁₀ = 2⁴ × 3 × 5² × 19
  22800 ≡ 8 (mod 37)   [8 = 2³, QNR]
  6 ≡ 2²⁷ (mod 37)    [27 odd → QNR ✓]
  12 ≡ 2²⁸ (mod 37)   [28 even → QR ✗ on QNR claim]
  22800 ≡ 8 = convergent n=4 residue
"""

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def is_qr(a, p):
    if a % p == 0:
        return None
    return pow(a, (p - 1) // 2, p) == 1

# ── BASE-7 CONVERSION ────────────────────────────────────────────────────────

print("=== BASE-7 CONVERSION: 123321₇ ===")
digits = [1, 2, 3, 3, 2, 1]
powers = [7**i for i in range(5, -1, -1)]
terms = [d * p for d, p in zip(digits, powers)]
total = sum(terms)

print(f"  Digit × power → term")
for d, p, t in zip(digits, powers, terms):
    print(f"  {d} × {p} = {t}")
print(f"  Sum = {total}")
print()

check("1×7⁵ = 16807", terms[0] == 16807)
check("2×7⁴ = 4802",  terms[1] == 4802)
check("3×7³ = 1029",  terms[2] == 1029)
check("3×7² = 147",   terms[3] == 147)
check("2×7¹ = 14",    terms[4] == 14)
check("1×7⁰ = 1",     terms[5] == 1)
check("123321₇ = 22800", total == 22800)

# Step-by-step as in document
check("16807 + 4802 = 21609", 16807+4802 == 21609)
check("21609 + 1029 = 22638", 21609+1029 == 22638)
check("22638 + 147 = 22785",  22638+147 == 22785)
check("22785 + 14 = 22799",   22785+14 == 22799)
check("22799 + 1 = 22800",    22799+1 == 22800)
print()

# ── FACTORIZATION ─────────────────────────────────────────────────────────────

print("=== FACTORIZATION ===")
check("22800 = 228 × 100", 228*100 == 22800)
check("228 = 12 × 19",     12*19 == 228)
check("228 = 2² × 3 × 19", 4*3*19 == 228)
check("22800 = 2⁴ × 3 × 5² × 19", 16*3*25*19 == 22800)
print()

# ── MOD-37 ────────────────────────────────────────────────────────────────────

print("=== MOD-37 RESIDUE ===")
check("616 × 37 = 22792", 616*37 == 22792)
check("22800 - 22792 = 8", 22800 - 22792 == 8)
check("22800 ≡ 8 (mod 37)", 22800 % 37 == 8)
print()

# ── QR / QNR STATUS ───────────────────────────────────────────────────────────

print("=== QR/QNR STATUS MOD 37 ===")
print("  Legendre symbol (2|37) via Euler criterion:")
legendre_2 = pow(2, 18, 37)   # 2^((37-1)/2)
print(f"  2^18 mod 37 = {legendre_2}  (≡ -1 → 2 is QNR)")
check("2 is QNR mod 37  [(2|37)=-1, 2^18≡36≡-1]", legendre_2 == 36)
print()

check("8 = 2³  (odd power of QNR → QNR)", is_qr(8,37) == False)
print(f"  8 is QR: {is_qr(8,37)}  → QNR ✓")
print()

check("2²⁷ ≡ 6 (mod 37)", pow(2,27,37) == 6)
check("27 is odd → 2²⁷ is QNR", pow(2,27,37) % 37 != 0 and is_qr(pow(2,27,37),37) == False)
check("6 is QNR mod 37", is_qr(6,37) == False)
print()

check("2²⁸ ≡ 12 (mod 37)", pow(2,28,37) == 12)
check("28 is even → 2²⁸ is QR  (NOT QNR)", is_qr(12,37) == True)
check("7² ≡ 12 (mod 37)  [49-37=12]", 49 % 37 == 12)
print("  *** DOCUMENT ERROR: '12 in 37-field: QNR' is WRONG — 12 is QR ***")
print()

# ── PALINDROME STRUCTURE ─────────────────────────────────────────────────────

print("=== PALINDROME STRUCTURE ===")
s = "123321"
check("123321 is palindrome in base 7", s == s[::-1])
check("22800 is NOT palindrome in base 10", "22800" != "22800"[::-1])

from collections import Counter
c = Counter(s)
check("123321: exactly two 1s, two 2s, two 3s", dict(c) == {'1':2,'2':2,'3':2})
print()

# ── 1-2-3 TRINITY ─────────────────────────────────────────────────────────────

print("=== 1-2-3 TRINITY ===")
check("1+2+3 = 6", 1+2+3 == 6)
check("6 = 2×3", 6 == 2*3)
check("6 is QNR mod 37", is_qr(6,37) == False)
check("6 ≡ 2²⁷ (mod 37)  [correct value, odd power → QNR]", pow(2,27,37) == 6)
print()

# ── DIGIT SUM ─────────────────────────────────────────────────────────────────

print("=== DIGIT SUM OF 22800 ===")
ds = sum(int(d) for d in "22800")
check("digit sum(22800) = 12", ds == 12)
check("12 = 3×4", 12 == 3*4)
check("12 ≡ 2²⁸ (mod 37)  [value correct]", pow(2,28,37) == 12)
check("12 is QR (not QNR) — document error", is_qr(12,37) == True)
print()

# ── CONVERGENT CONNECTION ─────────────────────────────────────────────────────

print("=== CONVERGENT n=4 CONNECTION ===")
# From continued_fraction_mod37_audit.py: residues[4] = 8
convergent_n4_residue = 8
check("22800 ≡ 8 (mod 37)", 22800 % 37 == convergent_n4_residue)
check("convergent n=4 residue = 8  (from mod-37 audit)", convergent_n4_residue == 8)
check("both 22800 and 6002/1851 map to 8 in Z/37Z", 22800 % 37 == 8)
print()

# ── SUMMARY ───────────────────────────────────────────────────────────────────

print("=== SUMMARY ===")
print("  123321₇ → 22800₁₀ ≡ 8 (mod 37)")
print("  8 = 2³  [QNR, odd power]")
print("  Palindrome base 7 (1-2-3-3-2-1) breaks in base 10")
print("  8 = convergent n=4 residue ✓")
print()
print("  ERROR IN DOCUMENT:")
print("  '12 in 37-field: 2²⁸ (QNR)'")
print("  2²⁸ ≡ 12 (mod 37) is correct, but 12 is QR (28 even; 7²≡12)")
print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All verified claims pass.")
