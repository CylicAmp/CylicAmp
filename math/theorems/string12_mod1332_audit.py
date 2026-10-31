#!/usr/bin/env python3
"""
string12_mod1332_audit.py

Modular analysis of the repeated-"12" digit string.

STRING FAMILY:
  N(n, t) = the number formed by n pairs of "12" followed by optional trailing "1" (t=True)
  N(n, False) = "1212...12"  (2n digits)
  N(n, True)  = "1212...121" (2n+1 digits)

KEY STRUCTURAL DRIVER:
  100 ≡ 26 (mod 37)   — the two-digit positional base equals MULT, the 137-map multiplier
  ord₃₇(26) = 3       — established throughout this repo
  → N(n, False) ≡ 0 (mod 37) iff 3 | n  (period 3 pairs = 6 digits)

  1332 = 36 × 37.  "LOCKED" states:
    N ≡ 0 (mod 1332): zero lock
    N ≡ 1 (mod 1332): unit lock

VERIFIED:
  N(3,False)  = 121212    ≡ 0 (mod 1332)  [6 digits, n=3, 3|3]
  N(3,True)   = 1212121   ≡ 1 (mod 1332)  [7 digits]
  N(6,False)  = period hit ≡ 0 (mod 1332)  [12 digits]
  N(45,False) = 90-digit string ≡ 0 (mod 1332)  [45=15×3, 3|45]
  N(45,True)  = 91-digit string ≡ 1 (mod 1332)  [+trailing 1]

  FRAME DUALITY:
    Left-anchored (×12 stride): 45 pairs "12" + trailing "1"
    Right-anchored (×21 stride): leading "1" + 45 pairs "21"

  PURE "21" CONTRAST:
    212121 ≡ 9 (mod 36), ≡ 0 (mod 37) → ≡ 333 (mod 1332)
    Breaking the double-zero: "21" endings are ≡ 1 (mod 4), not 0.

CONNECTION TO GF(37):
  100 ≡ 26 = MULT (mod 37)  [137 mod 37 = 26]
  ord₃₇(100) = ord₃₇(26) = 3  [the 137-map orbit order]
  N(n,False) = 12 × (100ⁿ − 1)/99;  100ⁿ ≡ 1 (mod 37) ⟺ 3|n
  The "12" repetition inherits the same period-3 that governs all 137-map orbits.
"""

import math
errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def make_N(n_pairs, trailing=False):
    s = "12" * n_pairs + ("1" if trailing else "")
    return int(s)

M = 1332   # = 36 × 37

# ── STRUCTURAL CONSTANTS ─────────────────────────────────────────────────────

print("=== STRUCTURAL CONSTANTS ===")
check("1332 = 36 × 37", M == 36 * 37)
check("100 ≡ 26 (mod 37)  [= MULT, the 137-map multiplier]", 100 % 37 == 26)
check("ord₃₇(26) = 3: 26^3 ≡ 1 (mod 37)", pow(26,3,37)==1 and all(pow(26,k,37)!=1 for k in [1,2]))
check("100^3 ≡ 1 (mod 37)  [same, via 100≡26]", pow(100,3,37) == 1)
check("333 = 9 × 37  (pure-21 lock value)", 333 == 9*37)
print()

# ── PERIOD-6 PATTERN ─────────────────────────────────────────────────────────

print("=== PERIOD-6 LOCK PATTERN ===")
for n, t, expect_mod_M in [(3,False,0),(3,True,1),(6,False,0),(6,True,1)]:
    N = make_N(n, t)
    label = f"N({n},{'T' if t else 'F'}) = {str(N)[:12]}{'...' if len(str(N))>12 else ''}, mod 1332 = {N%M}"
    check(label, N % M == expect_mod_M)
print()

# ── 90-DIGIT AND 91-DIGIT STRINGS ────────────────────────────────────────────

print("=== N90 AND N91 ===")
N90 = make_N(45)
N91 = make_N(45, True)

check("N90 has 90 digits  (45 pairs of '12')", len(str(N90)) == 90)
check("N91 has 91 digits  (45 pairs + '1')", len(str(N91)) == 91)
check("N91 == N90 × 10 + 1", N91 == N90 * 10 + 1)
print()

check("N90 ≡ 0 (mod 36)", N90 % 36 == 0)
check("N90 ≡ 0 (mod 37)", N90 % 37 == 0)
check("N90 ≡ 0 (mod 1332)  [ZERO LOCK]", N90 % M == 0)
print()

check("N91 ≡ 1 (mod 36)", N91 % 36 == 1)
check("N91 ≡ 1 (mod 37)", N91 % 37 == 1)
check("N91 ≡ 1 (mod 1332)  [UNIT LOCK]", N91 % M == 1)
print()

# ── WHY N90 ≡ 0 (mod 37) ─────────────────────────────────────────────────────

print("=== WHY N90 ≡ 0 (mod 37): ord₃₇(100)=3 AND 3|45 ===")
check("45 = 3 × 15", 45 == 3 * 15)
check("100^45 ≡ 1 (mod 37)  [45 = 15 × ord₃₇(26)]", pow(100,45,37) == 1)
check("N90 = 12 × (100^45 − 1)/99, and 100^45≡1 → numerator ≡ 0 (mod 37)",
      N90 % 37 == 0)
print("  The '12' repetition inherits period 3 from ord₃₇(MULT)=3.")
print()

# ── WHY N90 ≡ 0 (mod 36) ─────────────────────────────────────────────────────

print("=== WHY N90 ≡ 0 (mod 36 = 4 × 9) ===")
check("Last two digits of N90 = '12' → 12 mod 4 = 0  [N90 ≡ 0 mod 4]",
      N90 % 4 == 0)
digit_sum_90 = 45 * 3   # 3 per pair (1+2=3)
check("Digit sum of N90 = 45×3 = 135 ≡ 0 (mod 9)  [N90 ≡ 0 mod 9]",
      digit_sum_90 == 135 and 135 % 9 == 0)
check("N90 ≡ 0 (mod 4) and ≡ 0 (mod 9)  → ≡ 0 (mod 36)", N90 % 36 == 0)
print()

# ── N91 = N90 × 10 + 1 ───────────────────────────────────────────────────────

print("=== N91 = N90 × 10 + 1 ===")
check("N90 ≡ 0 (mod 1332)  → N91 = 0×10+1 ≡ 1 (mod 1332)", N91 % M == 1)
print()

# ── FRAME DUALITY ─────────────────────────────────────────────────────────────

print("=== FRAME DUALITY: 91-DIGIT STRING ===")
s91 = str(N91)
check("First digit = '1'", s91[0] == '1')
check("Digits [1:] start '212121...'  (right-anchor: 1 + 45×'21')",
      s91[1:7] == '212121')
# Verify 45 '21' pairs from position 1
tail = s91[1:]
check("s91[1:] == '21' × 45", tail == '21' * 45)
check("s91 == '1' + '21' × 45", s91 == '1' + '21' * 45)
print("  Left-anchored:  45×'12' + '1'")
print("  Right-anchored: '1' + 45×'21'")
print("  Same string, two valid framings.")
print()

# ── PREVIOUS STRING: N89 ─────────────────────────────────────────────────────

print("=== N89: PREVIOUS STRING (44 PAIRS + '1') ===")
N89 = make_N(44, True)
check("N89 has 89 digits", len(str(N89)) == 89)
check("N89 mod 36 = 25", N89 % 36 == 25)
check("N89 mod 37 = 22", N89 % 37 == 22)
check("N89 mod 1332 = 133", N89 % M == 133)
check("N89 × 100 + 21 = N91  [appending '21' to get the 91-digit string]",
      N89 * 100 + 21 == N91)
check("(N89×100 + 21) mod 37 = 1  [22×26 + 21 ≡ 572+21=593≡1 mod 37]",
      (N89 * 100 + 21) % 37 == 1)
check("(N89×100 + 21) mod 36 = 1  [25×28 + 21 = 721 ≡ 1 mod 36]",
      (N89 * 100 + 21) % 36 == 1)
print()

# ── PURE '21' CONTRAST ────────────────────────────────────────────────────────

print("=== PURE '21' FRAME: 212121 ===")
N21_6 = int('212121')
check("212121 mod 36 = 9   [last two '21' → 21 mod 4=1; digit sum 9 → mod 9=0; CRT→9]",
      N21_6 % 36 == 9)
check("212121 mod 37 = 0   [100≡26 mod 37, ord=3, 3|3 pairs → same zero mod 37]",
      N21_6 % 37 == 0)
check("212121 mod 1332 = 333", N21_6 % M == 333)
check("333 = 9 × 37  [hits zero mod 37 but 9 mod 36, not 0]", 333 == 9*37)
print("  Pure '21' breaks the double-zero because '21' ends in odd two-digit tail (21 mod 4=1).")
print("  '12' ends in 12 ≡ 0 mod 4; '21' ends in 21 ≡ 1 mod 4.")
print()

# ── THE PERIOD TABLE ─────────────────────────────────────────────────────────

print("=== PERIOD TABLE: N(n, False) mod 1332 for n=0..9 ===")
for n in range(10):
    N = make_N(n) if n > 0 else 0
    locked = " ← LOCKED" if (N % M == 0 and n > 0) else ""
    print(f"  n={n:2d}: {N % M:4d} (mod 1332){locked}")
print("  Period = 3 pairs = 6 digits. Lock fires at n=3,6,9,...")
print()

# ── SUMMARY ──────────────────────────────────────────────────────────────────

print("=== SUMMARY ===")
print("  100 ≡ 26 = MULT (mod 37);  ord₃₇(26) = 3")
print("  → '12'×n string: N ≡ 0 (mod 37) iff 3|n  (period 6 digits)")
print("  '12' ends in 12 ≡ 0 (mod 4);  digit sum = 3n ≡ 0 (mod 9) iff 3|n")
print("  → N ≡ 0 (mod 1332) iff 3|n  (zero lock)")
print()
print("  45 = 15×3 → N90 ≡ 0 (mod 1332)  [zero lock]")
print("  N91 = N90×10+1 ≡ 1 (mod 1332)  [unit lock]")
print()
print("  '21' frame (212121): 21 mod 4=1 → breaks mod-4 zero → lands at 333 mod 1332")
print("  333 = 9×37;  '21' reaches 37-zero but misses 4-zero")
print()

if errors:
    print(f"FAILURES ({len(errors)}):")
    for e in errors:
        print(f"  - {e}")
else:
    print("All verified claims pass.")
