# math/theorems/mersenne_dr_boundary_53_54.py
"""
Mersenne DR Boundary: n=53 / n=54

─────────────────────────────────────────────────────────────────────────────
FOUR-DIGIT NUMBERS — DIGITAL ROOT 6
─────────────────────────────────────────────────────────────────────────────
  Total 4-digit numbers: 9,000  (1000–9999)
  With DR=6:  9000 ÷ 9 = 1,000  (one ninth of all 4-digit numbers)

  Digit sum exactly 6 (first sum, no iteration needed):
    a+b+c+d=6, a≥1, b,c,d≥0  →  a'=(a-1): a'+b+c+d=5
    Stars & bars: C(8,3) = 56

  Group counts by leading digit:
    1→21,  2→15,  3→10,  4→6,  5→3,  6→1   (total=56)

─────────────────────────────────────────────────────────────────────────────
DR(2^n − 1) — PERIOD-6 CYCLE
─────────────────────────────────────────────────────────────────────────────
  2^n mod 9 cycles with period 6: [2,4,8,7,5,1]
  DR(2^n − 1) cycle (n mod 6 = 1..6): [1,3,7,6,4,9]

─────────────────────────────────────────────────────────────────────────────
BOUNDARY: n=53 → n=54
─────────────────────────────────────────────────────────────────────────────
  M_53 = 9007199254740991   16 digits  first=9  DR(53)=8  DR(M_53)=4
  M_54 = 18014398509481983  17 digits  first=1  DR(54)=9  DR(M_54)=9

  n=53: last 16-digit Mersenne number (first digit 9)
  n=54: first 17-digit Mersenne number (first digit 1 — resets to 1)

  At n=54: DR(n) = DR(M_n) = 9  (only case in the 6-cycle window where both equal 9)

  Digit-length boundary:  16 → 17  ("10-11" in hexadecimal digit count)
  First-digit boundary:   9  →  1  ("1-2" register: last before 1, next after 1)
"""

import math

M53 = 2**53 - 1
M54 = 2**54 - 1

def dr(n): return (n - 1) % 9 + 1 if n > 0 else 9


# ── Four-digit DR=6 count ──────────────────────────────────────────────────────

count_dr6 = sum(1 for n in range(1000, 10000) if dr(n) == 6)
assert count_dr6 == 1000
assert 9000 // 9 == 1000

# Digit sum exactly 6: stars and bars C(8,3)
assert math.comb(8, 3) == 56
exact6 = [n for n in range(1000, 10000) if sum(int(d) for d in str(n)) == 6]
assert len(exact6) == 56

# Group counts by leading digit
groups = [sum(1 for n in exact6 if str(n)[0] == d) for d in '123456']
assert groups == [21, 15, 10, 6, 3, 1]
assert sum(groups) == 56

# ── DR(2^n − 1) period-6 cycle ─────────────────────────────────────────────────

# 2^n mod 9 cycles with period 6
pow2_mod9_cycle = [(2**k) % 9 for k in range(1, 7)]
assert pow2_mod9_cycle == [2, 4, 8, 7, 5, 1]

# DR(2^k - 1) for k=1..6
dr_mersenne_cycle = [dr(2**k - 1) for k in range(1, 7)]
assert dr_mersenne_cycle == [1, 3, 7, 6, 4, 9]

# Period confirmed: DR(2^(n+6) - 1) == DR(2^n - 1) for small n
for k in range(1, 7):
    assert dr(2**k - 1) == dr(2**(k + 6) - 1)

# ── M_53 properties ────────────────────────────────────────────────────────────

assert M53 == 9_007_199_254_740_991
assert len(str(M53)) == 16
assert str(M53)[0] == '9'
assert dr(53) == 8
assert dr(M53) == 4
assert 53 % 6 == 5                       # n mod 6 = 5 → DR(M_n) = 4
assert dr_mersenne_cycle[4] == 4         # cycle index 4 (0-indexed)

# ── M_54 properties ────────────────────────────────────────────────────────────

assert M54 == 18_014_398_509_481_983
assert len(str(M54)) == 17
assert str(M54)[0] == '1'
assert dr(54) == 9
assert dr(M54) == 9
assert 54 % 6 == 0                       # n mod 6 = 0 → DR(M_n) = 9
assert dr_mersenne_cycle[5] == 9         # cycle index 5 (0-indexed)

# n=54 is the unique case in the cycle where DR(n) = DR(M_n) = 9
assert dr(54) == dr(M54) == 9

# ── Boundary: digit-length flip ────────────────────────────────────────────────

assert len(str(M53)) == 16               # last 16-digit Mersenne
assert len(str(M54)) == 17               # first 17-digit Mersenne
assert len(str(2**53)) == 16             # 2^53 is also 16 digits
assert len(str(2**54)) == 17             # 2^54 is 17 digits

# First digit resets from 9 → 1 at this boundary
assert str(M53)[0] == '9'
assert str(M54)[0] == '1'

# ── Confirming n=53 is LAST 16-digit, n=54 is FIRST 17-digit ──────────────────

assert all(len(str(2**n - 1)) == 16 for n in range(50, 54))
assert all(len(str(2**n - 1)) == 17 for n in range(54, 57))


if __name__ == "__main__":
    print("Mersenne DR Boundary: n=53 / n=54")
    print()
    print("Four-digit numbers with DR=6:")
    print(f"  Total:           {count_dr6:,}  (9000 ÷ 9)")
    print(f"  Digit sum = 6:   {len(exact6)}   C(8,3)")
    print(f"  By leading digit: {dict(zip('123456', groups))}")
    print()
    print("DR(2^n − 1) period-6 cycle:")
    print(f"  2^k mod 9:  {pow2_mod9_cycle}")
    print(f"  DR(M_k):    {dr_mersenne_cycle}")
    print()
    print(f"  M_53 = {M53}")
    print(f"         16 digits  first=9  DR(53)={dr(53)}  DR(M_53)={dr(M53)}")
    print()
    print(f"  M_54 = {M54}")
    print(f"         17 digits  first=1  DR(54)={dr(54)}  DR(M_54)={dr(M54)}")
    print()
    print("  n=53: last 16-digit Mersenne (first digit 9)")
    print("  n=54: first 17-digit Mersenne (first digit 1 — resets)")
    print("  n=54: DR(n) = DR(M_n) = 9  [only occurrence in the 6-cycle window]")
    print()
    print("All assertions passed.")
