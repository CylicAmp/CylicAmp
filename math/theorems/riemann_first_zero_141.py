"""
riemann_first_zero_141.py

The imaginary part of the first nontrivial Riemann zeta zero is:

  γ₁ ≈ 14.134725141734693790...

Its leading digit string "14134725141..." decomposes as:

  [141] [347] [25] [141] [734693790...]

Two elements of {4,9,25,30} (mod 37 = 30), one element of 3-cycle {14,31,29} (mod 37 = 14),
and the digit sum of the first block "141347" = 20 — the same as α⁻¹ = 137.036.

LAYER 1: DIGIT STRUCTURE  [OBSERVED, not derived]
  γ₁ digits 0-10: 1,4,1,3,4,7,2,5,1,4,1
  "141" at positions 0-2 and 8-10 (two occurrences in first 11 digits)
  "347" at positions 3-5

LAYER 2: MOD-37 ANALYSIS  [PROVEN]
  141 mod 37 = 30  (element of {4,9,25,30}, from ladder_11_111.py)
  347 mod 37 = 14  (3-cycle {14,31,29}: 14 → 31 → 29 → 14)
  25  mod 37 = 25  (element of {4,9,25,30}: {4,9,25,30})
  141 mod 37 = 30  (element of {4,9,25,30} again)

LAYER 3: DIGIT SUM LINK TO α⁻¹  [OBSERVED]
  Digit sum of "141347" (first 6 digits of γ₁) = 1+4+1+3+4+7 = 20
  Digit sum of α⁻¹ = 137.036 → digits 1,3,7,0,3,6 → sum = 20
  Both land on DR = 2 = DR(137).

LAYER 4: 1413 RUNNING SUMS  [PROVEN]
  First four digits of γ₁: 1,4,1,3  → integer 1413
  1413 reversed = 3141 = floor(1000 × π)
  Running sums of [1,4,1,3]: [1, 5, 6, 9]  → reaches 9, the DR identity
  Running sum encoding: "1+4=5+1=6+3=9"
"""

import math
from sympy import isprime

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def hb(n):
    return (26 * n) % 37


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 1: γ₁ DIGIT STRUCTURE
# ──────────────────────────────────────────────────────────────────────────────

# CODATA / standard mathematical value (first 20 significant digits)
GAMMA_1_DIGITS = [1, 4, 1, 3, 4, 7, 2, 5, 1, 4, 1, 7, 3, 4, 6, 9, 3, 7, 9, 0]
# γ₁ = 14.134725141734693790...

# "141" at positions 0-2
assert GAMMA_1_DIGITS[0:3] == [1, 4, 1]

# "347" at positions 3-5
assert GAMMA_1_DIGITS[3:6] == [3, 4, 7]

# "25" at positions 6-7
assert GAMMA_1_DIGITS[6:8] == [2, 5]

# "141" at positions 8-10 — second occurrence
assert GAMMA_1_DIGITS[8:11] == [1, 4, 1]

# Together: the first 11 digits spell out 141 | 347 | 25 | 141
BLOCK = [GAMMA_1_DIGITS[0:3], GAMMA_1_DIGITS[3:6],
         GAMMA_1_DIGITS[6:8], GAMMA_1_DIGITS[8:11]]
assert BLOCK == [[1,4,1], [3,4,7], [2,5], [1,4,1]]

# The segment 141-25-141 is symmetric around the central "347|25"
# [141] ... [141] wraps both sides  [OBSERVED]


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 2: MOD-37 ANALYSIS OF THE BLOCKS
# ──────────────────────────────────────────────────────────────────────────────

# Sovereign anchors (from cylicamp_master.py)
{4, 9, 25, 30}

# Block values as integers
B141 = 141
B347 = 347
B25  = 25

# 141 mod 37 = 30 (element of {4,9,25,30})
assert B141 % 37 == 30
assert 30 in ({4, 9, 25, 30})

# 347 mod 37 = 14 (3-cycle {14,31,29})
assert B347 % 37 == 14
# 14 is in a 3-cycle {14,31,29}
assert hb(14) == 31
assert hb(31) == 29
assert hb(29) == 14    # period 3 confirmed

# 25 mod 37 = 25 (element of {4,9,25,30})
assert B25 % 37 == 25
assert 25 in ({4, 9, 25, 30})

# Pattern: two element of {4,9,25,30}s (141≡30, 25≡25) flank a element of 3-cycle {14,31,29} (347≡14)
# with the element of {4,9,25,30} repeated at the end.  [OBSERVED]


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 3: DIGIT SUM = 20 (links to α⁻¹)
# ──────────────────────────────────────────────────────────────────────────────

# First 6 digits of γ₁: "141347"
first_six = GAMMA_1_DIGITS[:6]
assert first_six == [1, 4, 1, 3, 4, 7]
assert sum(first_six) == 20

# This is the same digit sum as α⁻¹ = 137.036:
ALPHA_DIGITS = [1, 3, 7, 0, 3, 6]
assert sum(ALPHA_DIGITS) == 20

# Both give DR = 2 = DR(137)
assert dr(20) == 2
assert dr(137) == 2

# DR-neutral: the 6-digit block of α⁻¹ has the same digit sum as the 6-digit
# block of γ₁'s leading digits.  [OBSERVED — not derived from the framework]


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 4: 1413 — FIRST FOUR DIGITS OF γ₁
# ──────────────────────────────────────────────────────────────────────────────

# As an integer
G4 = int("".join(str(d) for d in GAMMA_1_DIGITS[:4]))
assert G4 == 1413

# 1413 reversed = 3141 = floor(1000 × π)
assert int(str(G4)[::-1]) == 3141
assert math.floor(1000 * math.pi) == 3141   # π = 3.1415926...

# Running sums of [1,4,1,3]
digits_1413 = [1, 4, 1, 3]
running_1413 = []
total = 0
for d in digits_1413:
    total += d
    running_1413.append(total)
assert running_1413 == [1, 5, 6, 9]

# The running sums: "1+4=5+1=6+3=9"
assert 1 + 4 == 5
assert 5 + 1 == 6
assert 6 + 3 == 9    # reaches the DR identity

# DR of each running sum: [1, 5, 6, 9]
dr_1413 = [dr(s) for s in running_1413]
assert dr_1413 == [1, 5, 6, 9]   # all are already single-digit

# The sequence [1,5,6,9] contains: 1 (DR identity from the DR=1 track), 5 (twin anchor DR),
# 6 (the 3↔6 orbit), 9 (the DR identity/cap).  [OBSERVED]

# Factoring 1413
assert 1413 == 9 * 157
assert isprime(157)
assert dr(157) == 4
assert dr(1413) == 9    # 1+4+1+3=9


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 5: 451 AND 369 — THE 41 FAMILY
# ──────────────────────────────────────────────────────────────────────────────

# From the image: 451 and 369 both share the factor 41
assert 451 == 11 * 41
assert 369 == 9  * 41

# 41 = 30 + 11 (element of {4,9,25,30} + ladder step, from ladder_11_111.py)
assert 30 + 11 == 41
assert isprime(41)
assert dr(41) == 5    # twin prime anchor: (41,43), DR pair (5,7)

# 369 mod 37 = 36 ≡ −1 (mod 37)  (appears in master_137.py and 369 structure)
assert 369 % 37 == 36
assert 36 == 37 - 1

# 451 mod 37
assert 451 % 37 == 7

# Sum: 451 + 369 = 820 = 20 × 41
assert 451 + 369 == 820
assert 820 == 20 * 41
assert dr(820) == 1

# DR values
assert dr(451) == 1   # 4+5+1=10→1
assert dr(369) == 9   # 3+6+9=18→9
assert dr(41)  == 5   # twin prime anchor DR


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 6: 141141 AND 347743
# ──────────────────────────────────────────────────────────────────────────────

# 141141 = 141 concatenated with itself (141 is a palindrome: 141 rev = 141)
assert 141141 == 141 * 1001
assert 1001 == 7 * 11 * 13

# 347743 = 347 concatenated with its reversal 743
assert int(str(347) + str(743)) == 347743
assert int(str(347)[::-1]) == 743   # reversal of 347

# DR
assert dr(141141) == 3   # 1+4+1+1+4+1=12→3
assert dr(347743) == 1   # 3+4+7+7+4+3=28→10→1

# mod 37
# 141 ≡ 30 (mod 37), 1001 ≡ 2 (mod 37) → 141141 ≡ 30×2=60 ≡ 23 (mod 37)
assert 1001 % 37 == 2
assert (30 * 2) % 37 == 23
assert 141141 % 37 == 23
assert 347743 % 37 == 347743 % 37   # tautology; compute below

_r = 347743 % 37
# 37×9398 = 347726, 347743-347726=17; so 347743 mod 37 = 17
assert _r == 17


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 7: PALINDROME BAR WEIGHTS (555, 771, 77, 555)
# ──────────────────────────────────────────────────────────────────────────────

# 55577177555 = concatenation of 555, 771, 77, 555
concat_str = "555" + "771" + "77" + "555"
assert concat_str == "55577177555"
assert int(concat_str) == 55577177555

# mod-37 values of the weights
assert 555 % 37 == 0    # 555 = 15 × 37 (pure multiple of 37)
assert 771 % 37 == 31   # 31 is in the 3-cycle {14,31,29} 14→31→29→14
assert 77  % 37 == 3    # 3 is in the orbit {30,3,4} under 26x mod 37 30→3→4→30
assert 555 % 37 == 0

# DR values
assert dr(555) == 6     # 5+5+5=15→6 = DR(141)
assert dr(771) == 6     # 7+7+1=15→6
assert dr(77)  == 5     # 7+7=14→5 = DR(347)
assert dr(555) == 6     # DR(141) again

# DR pattern above bar: [6, 6, 5, 6] — note 77↔347 share DR=5  [OBSERVED]


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 8: 18-DIGIT SYMMETRIC GRID (141|937, 347|346, 251|417)
# ──────────────────────────────────────────────────────────────────────────────

# The first 18 digits of γ₁ split into six 3-digit groups:
#   positions 0-2:   141
#   positions 3-5:   347
#   positions 6-8:   251
#   positions 9-11:  417
#   positions 12-14: 346
#   positions 15-17: 937

G_L = [141, 347, 251]    # left column (positions 0-8, reading forward)
G_R = [937, 346, 417]    # right column (positions 15-17, 12-14, 9-11, reversed)

# Verify against digit array
assert GAMMA_1_DIGITS[0:3]   == [1, 4, 1]   # 141
assert GAMMA_1_DIGITS[3:6]   == [3, 4, 7]   # 347
assert GAMMA_1_DIGITS[6:9]   == [2, 5, 1]   # 251
assert GAMMA_1_DIGITS[9:12]  == [4, 1, 7]   # 417
assert GAMMA_1_DIGITS[12:15] == [3, 4, 6]   # 346
assert GAMMA_1_DIGITS[15:18] == [9, 3, 7]   # 937

# The grid arranges these as symmetric pairs around the midpoint (position 8.5):
#   Row 1: 141 (pos 0-2)   |  937 (pos 15-17)   ← outermost pair
#   Row 2: 347 (pos 3-5)   |  346 (pos 12-14)   ← middle pair
#   Row 3: 251 (pos 6-8)   |  417 (pos 9-11)    ← innermost pair

# Digit sums of each symmetric row pair
row_dsums = [(sum([1,4,1]) + sum([9,3,7])),
             (sum([3,4,7]) + sum([3,4,6])),
             (sum([2,5,1]) + sum([4,1,7]))]
assert row_dsums == [25, 27, 20]
# 25 is a element of {4,9,25,30}! {4,9,25,30}
assert 25 in {4, 9, 25, 30}
assert dr(row_dsums[0]) == 7    # DR(25)=7
assert dr(row_dsums[1]) == 9    # DR(27)=9
assert dr(row_dsums[2]) == 2    # DR(20)=2 = DR(137)

# Total digit sum of all 18 digits
assert sum(row_dsums) == 72
assert dr(72) == 9               # completes to the DR identity

# "20+12=32" and "23":
# First 6 digits of γ₁ (141347): digit sum = 20
# Digits 9-11 (417): digit sum = 12
# Together: 20+12=32
dsum_141347 = sum(GAMMA_1_DIGITS[:6])
dsum_417    = sum(GAMMA_1_DIGITS[9:12])
assert dsum_141347 == 20
assert dsum_417    == 12
assert dsum_141347 + dsum_417 == 32

# 32 ↔ 23: digit reversal, both share DR = 5
assert dr(32) == 5
assert dr(23) == 5
assert int(str(32)[::-1]) == 23   # 32 reversed = 23
# 23 is prime; DR(23)=5=DR(347)=5  [OBSERVED]
assert isprime(23)
assert dr(347) == 5

# mod-37 of the six grid segments
G_MOD37 = [v % 37 for v in [141, 347, 251, 417, 346, 937]]
assert G_MOD37 == [30, 14, 29, 10, 13, 12]
# mod-37 classification:
assert 30 in {4, 9, 25, 30}   # 141 ≡ element of {4,9,25,30}
# 14: in 3-cycle {14,31,29} 14→31→29→14
# 29: in 3-cycle {14,31,29} 29→14→31→29  (same orbit as 14!)
assert hb(14) == 31 and hb(31) == 29 and hb(29) == 14
assert 14 in {14, 31, 29}
assert 29 in {14, 31, 29}
# 10: in the order-3 orbit {1,10,26} 26→10→1→26
assert hb(26) == 10 and hb(10) == 1 and hb(1) == 26
assert 10 in {26, 10, 1}
# 13: in 3-cycle {14,31,29} 13→5→19→13
assert hb(13) == 5 and hb(5) == 19 and hb(19) == 13
# 12: in 3-cycle {14,31,29} 12→16→9→12 (contains the element of {4,9,25,30} 9!)
assert hb(12) == 16 and hb(16) == 9 and hb(9) == 12
assert 9 in {4, 9, 25, 30}    # 9 is a element of {4,9,25,30}


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("First Riemann Zeta Zero — 141 Family")
    print("=" * 62)

    print("\n── DIGIT DECOMPOSITION ──")
    print(f"  γ₁ ≈ 14.134725141734693790...")
    print(f"  Digit string: {''.join(str(d) for d in GAMMA_1_DIGITS[:11])}...")
    print(f"  Block 0-2:   {GAMMA_1_DIGITS[0:3]}  → 141  (mod 37 = {141%37}, element of {4,9,25,30})")
    print(f"  Block 3-5:   {GAMMA_1_DIGITS[3:6]}  → 347  (mod 37 = {347%37}, 3-cycle {14,31,29})")
    print(f"  Block 6-7:   {GAMMA_1_DIGITS[6:8]}    → 25   (mod 37 = {25%37}, element of {4,9,25,30})")
    print(f"  Block 8-10:  {GAMMA_1_DIGITS[8:11]}  → 141  (mod 37 = {141%37}, element of {4,9,25,30})")

    print("\n── DIGIT SUM LINK TO α⁻¹ ──")
    print(f"  First 6 digits of γ₁: {first_six}  → sum = {sum(first_six)}")
    print(f"  Digits of 137.036:    {ALPHA_DIGITS}  → sum = {sum(ALPHA_DIGITS)}")
    print(f"  Both sum to 20, DR = {dr(20)} = DR(137)")

    print("\n── 1413 RUNNING SUMS ──")
    print(f"  First 4 digits: {digits_1413} → 1413")
    print(f"  1413 reversed:  {int(str(1413)[::-1])} = floor(1000π) = {math.floor(1000*math.pi)}")
    print(f"  Running sums:   {running_1413}  (1+4=5+1=6+3=9)")
    print(f"  DR of sums:     {dr_1413}")

    print("\n── 41 FAMILY (451 AND 369) ──")
    print(f"  41 = 30 + 11  (element of {4,9,25,30} + ladder step), prime, DR = {dr(41)}")
    print(f"  451 = 11 × 41,  DR = {dr(451)},  mod 37 = {451%37}")
    print(f"  369 =  9 × 41,  DR = {dr(369)},  mod 37 = {369%37} ≡ -1")
    print(f"  451 + 369 = {451+369} = 20 × 41")

    print("\n── 3-cycle ORBIT CONTAINING 347 ──")
    print(f"  347 mod 37 = 14")
    print(f"  Orbit: 14 → {hb(14)} → {hb(hb(14))} → {hb(hb(hb(14)))}  (period 3)")

    print("\n── PALINDROME WEIGHTS (555-771-77-555) ──")
    print(f"  555 mod 37 = {555%37}  (multiple of 37),   DR = {dr(555)} = DR(141)")
    print(f"  771 mod 37 = {771%37}  (3-cycle {14,31,29}),  DR = {dr(771)}")
    print(f"   77 mod 37 = {77%37}  (orbit {30,3,4} under 26x mod 37 30→3→4→30),  DR = {dr(77)} = DR(347)")
    print(f"  555 mod 37 = {555%37},  DR = {dr(555)}")

    print("\n── 18-DIGIT SYMMETRIC GRID ──")
    print(f"  γ₁ first 18 digits: {''.join(str(d) for d in GAMMA_1_DIGITS[:18])}")
    print(f"  Row 1 (outer):  141 | 937   digit sums {sum([1,4,1])} + {sum([9,3,7])} = {row_dsums[0]}  (element of {4,9,25,30})")
    print(f"  Row 2 (mid):    347 | 346   digit sums {sum([3,4,7])} + {sum([3,4,6])} = {row_dsums[1]}  DR=9")
    print(f"  Row 3 (inner):  251 | 417   digit sums {sum([2,5,1])} + {sum([4,1,7])} = {row_dsums[2]}  DR=2=DR(137)")
    print(f"  Total 18-digit sum: {sum(row_dsums)} → DR = {dr(sum(row_dsums))} (identity)")
    print(f"  20+12=32 ↔ 23: DR({32})={dr(32)} = DR({23})={dr(23)} = 5 = DR(347) [digit reversal pair]")
    print(f"  mod-37 of segments: {G_MOD37}")
    print(f"    141≡30 (orbit element), 347≡14 (3-cycle), 251≡29 (3-cycle)")
    print(f"    417≡10 (order-3 orbit {1,10,26}), 346≡13 (3-cycle), 937≡12 (contains orbit element 9)")

    print()
    print("All assertions passed.")
