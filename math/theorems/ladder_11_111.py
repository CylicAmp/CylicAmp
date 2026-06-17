"""
ladder_11_111.py

The +11 and +111 ladders from the two 37-hub pivots: 26 and 30.

PIVOT POINTS (mod 37):
  137 mod 37 = 26    (ord₃₇(26) = 3)
  30             (in the orbit 30→3→4→30 under x↦26x mod 37)

+111 LADDER (three-repunit steps = +3×37):
  26 + 111 = 137     α⁻¹ integer part
  30 + 111 = 141     floor(100√2); appears in π's decimal digits

+11 LADDER FROM 26 (to Eddington's number):
  26 + 11×10 = 136   Eddington's 1929 prediction (wrong)
  26 + 111   = 137   measured integer value of α⁻¹
  Gap: 111 − 110 = 1

THE 141 NODE:
  141 = 30 + 111   (+3×37 from 30)
  141 mod 37 = 30  (+3×37 is invisible mod 37)
  141 = 3 × 47,    DR(47) = 2, DR(141) = 6
  DR-track parallel: DR(137)=2, DR(411)=6 / DR(47)=2, DR(141)=6

π CONNECTION:
  π = 3.14159265...
  First three decimal digits are 1, 4, 1 → "141"
  141 = 30 + 111   [OBSERVED, structural meaning open]
"""

import math
from sympy import isprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ──────────────────────────────────────────────────────────────────────────────
# +111 LADDER
# ──────────────────────────────────────────────────────────────────────────────

assert 26 + 111 == 137
assert 30 + 111 == 141

# +111 = +3×37, so adding it leaves the value's residue mod 37 unchanged.
assert (26 + 111) % 37 == 26 % 37   # 137 mod 37 = 26
assert (30 + 111) % 37 == 30 % 37   # 141 mod 37 = 30


# ──────────────────────────────────────────────────────────────────────────────
# +11 LADDER FROM 26
# ──────────────────────────────────────────────────────────────────────────────

ladder_26 = [26 + 11 * k for k in range(1, 11)]
assert ladder_26 == [37, 48, 59, 70, 81, 92, 103, 114, 125, 136]
assert ladder_26[-1] == 136           # Eddington 1929

# The difference between +110 (step 10) and +111 (one repunit) is exactly 1.
assert 111 - 11 * 10 == 1
assert 137 - 136 == 1


# ──────────────────────────────────────────────────────────────────────────────
# 141 NODE
# ──────────────────────────────────────────────────────────────────────────────

assert 30 + 111 == 141
assert 141 % 37 == 30                 # orbit element 30 preserved
assert 141 == 3 * 47
assert isprime(47)
assert dr(47)  == 2
assert dr(141) == 6                   # 1+4+1 = 6

# DR parallel with the 137 family:
#   DR(137)=2, DR(411)=6    (3 × 137)
#   DR(47) =2, DR(141)=6    (3 × 47)
assert dr(137) == dr(47)  == 2
assert dr(411) == dr(141) == 6

# Triple of 141
assert 3 * 141 == 423
assert dr(423) == 9                   # 4+2+3 = 9


# ──────────────────────────────────────────────────────────────────────────────
# √2 CONNECTION
# ──────────────────────────────────────────────────────────────────────────────

SQRT2 = math.sqrt(2)                  # 1.41421356...
assert abs(SQRT2 - 1.41421356) < 1e-7
assert math.floor(100 * SQRT2) == 141  # floor(141.421...) = 141


# ──────────────────────────────────────────────────────────────────────────────
# π CONNECTION
# ──────────────────────────────────────────────────────────────────────────────

PI = math.pi   # 3.14159265358979...

assert math.floor(1000 * PI) == 3141   # 1000π ≈ 3141.59...
# → the decimal digits of π open with .141...
assert math.floor(100 * (PI - 3)) == 14   # first two decimal places: .14

# Running sums of the first 11 digits of π: 3,1,4,1,5,9,2,6,5,3,5
PI_DIGITS = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
running_pi = []
total = 0
for d in PI_DIGITS:
    total += d
    running_pi.append(total)
assert running_pi == [3, 4, 8, 9, 14, 23, 25, 31, 36, 39, 44]

# DR of each running sum
dr_running_pi = [dr(s) for s in running_pi]
assert dr_running_pi == [3, 4, 8, 9, 5, 5, 7, 4, 9, 3, 8]

# First running sum ≡ −1 (mod 37): at position 9 (0-indexed: 8), value 36
assert running_pi[8] == 36
assert 36 % 37 == 36   # 36 ≡ −1 (mod 37), same as 369 mod 37

# The running sum skips 37 entirely (goes 36 → 39) because the next digit is 3.


# ──────────────────────────────────────────────────────────────────────────────
# 141 + 111k PALINDROME FAMILY  (k = 0 .. 5)
# ──────────────────────────────────────────────────────────────────────────────

PALETTE = [141 + 111 * k for k in range(6)]
assert PALETTE == [141, 252, 363, 474, 585, 696]

for v in PALETTE:
    assert v % 37 == 30    # orbit element 30 is invariant: +111 = +3×37

DR_PALETTE = [dr(v) for v in PALETTE]
assert DR_PALETTE == [6, 9, 3, 6, 9, 3]   # cycle 6→9→3 repeating

# Verify the cycle rule explicitly
NEXT_DR = {6: 9, 9: 3, 3: 6}
for i in range(len(DR_PALETTE) - 1):
    assert DR_PALETTE[i + 1] == NEXT_DR[DR_PALETTE[i]]

# {3,6,9} = complement of prime DR set {1,2,4,5,7,8}  (proven in prime_dr_unification.py)
# The entire palindrome family lives inside {3,6,9}.


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Ladder +11 / +111 from 37-hub Pivots")
    print("=" * 62)

    print("\n── +111 LADDER ──")
    print(f"  26 ({26}) + 111 = {26+111}   α⁻¹ integer")
    print(f"  30  ({30}) + 111 = {30+111}   π/√2 integer")
    print(f"  Rule: +111 = +3×37, so mod 37 is unchanged.")

    print("\n── +11 LADDER FROM 26 ──")
    for i, v in enumerate(ladder_26, 1):
        tag = "  ← Eddington 1929 (wrong)" if v == 136 else ""
        print(f"  26 + 11×{i:2d} = {v:3d}{tag}")
    print(f"  26 + 111   = 137  ← correct α⁻¹ integer")
    print(f"  Gap: 137 − 136 = {137-136}  (111 − 110 = {111-110})")

    print("\n── 141 NODE ──")
    print(f"  141 = 30 + 111  (30 + 3×37)")
    print(f"  141 mod 37      = {141%37}  (orbit element 30 preserved)")
    print(f"  141 = 3 × 47,   DR(47) = {dr(47)},  DR(141) = {dr(141)}")
    print(f"  Parallel:  DR(137)={dr(137)}, DR(411)={dr(411)}  vs  DR(47)={dr(47)}, DR(141)={dr(141)}")
    print(f"  floor(100√2)    = {math.floor(100*SQRT2)}")

    print("\n── π CONNECTION ──")
    print(f"  π = {PI:.10f}...")
    print(f"  floor(1000π)    = {math.floor(1000*PI)}  → decimal opens .141...")
    print(f"  π digits:          {PI_DIGITS}")
    print(f"  Running sums:      {running_pi}")
    print(f"  DR running sums:   {dr_running_pi}")
    print(f"  Sum[9] = {running_pi[8]} ≡ −1 (mod 37)  [same as 369 mod 37]")
    print(f"  Running sum never hits 37: goes 36 → 39 (next digit = 3)")

    print("\n── 141+111k FAMILY ──")
    print(f"  {PALETTE}")
    print(f"  All mod 37 = 30  (orbit element 30 invariant)")
    print(f"  DR:  {DR_PALETTE}  (6→9→3→6 cycle, entirely within {{3,6,9}})")

    print()
    print("All assertions passed.")
