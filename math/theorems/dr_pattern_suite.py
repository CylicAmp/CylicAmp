"""
Digital-Root Pattern Suite

Covers ten verified findings from the pattern survey:

  A. Universal Collapse to S = {0,2,3,6,8,9}
  B. 1-9 Core: 27 digits, sum = 135, DR(135) = 9
  C. 9↔6 Flip via ±3 seed
  D. 5-Boundary: +9 spacing, period 9
  E. 123/321 Mirror: 444 = 12×37, 888 = 24×37
  F. 6×4 / 64→27 grid observation
  G. 7-Digit Matrix: center 28 = 2×(3+4+7)
  H. Tesla 4-bit bend → DR-3 class
  I. Date Coordinates: session date DR chain 2→7→1
  J. Cardano / ω: roots of x³ − 3x − 1 = 0 via cube root of unity
  K. DR=1 cluster: {c, 37, 73, 2701} and 11g ≡ 44g (mod 9) for 3∣g

DR convention used throughout: DR(n) = (n−1)%9+1 for n>0; DR(0)=0.
"""


def dr(n: int) -> int:
    """Digital root (1-based for n>0; 0 for n=0)."""
    if n == 0:
        return 0
    return (n - 1) % 9 + 1


# =============================================================================
# A. Universal Collapse to S = {0,2,3,6,8,9}
# =============================================================================
# Translation set M = {+2, -2, +3, 0} mod 9.
# Residues not in S: {1, 4, 5, 7}. Each maps into S in one step.
S = {0, 2, 3, 6, 8, 9}
outside_S = {r for r in range(10) if r not in S}  # {1,4,5,7}

collapse_map = {
    1: (1 + 2) % 9,   # 1 +2 → 3 ∈ S
    4: (4 + 2) % 9,   # 4 +2 → 6 ∈ S
    5: (5 + 3) % 9,   # 5 +3 → 8 ∈ S
    7: (7 + 2) % 9,   # 7 +2 → 0 ∈ S  (9 ≡ 0)
}

for r, image in collapse_map.items():
    assert r in outside_S
    assert image in S or image == 0, f"{r} → {image} not in S"

assert outside_S == {1, 4, 5, 7}

# =============================================================================
# B. 1-9 Core: 27 digits, sum 135 → DR 9
# =============================================================================
core_27 = list(range(1, 10)) * 3
assert len(core_27) == 27
assert sum(core_27) == 135
assert dr(135) == 9

# =============================================================================
# C. 9↔6 Flip via seed 3
# =============================================================================
# Subtracting 3 shifts DR: 9 → 6, 6 → 3.
# Adding 3 shifts DR:      6 → 9, 3 → 6.
# Representative pairs:
for n in range(9, 10000, 9):       # DR(n) = 9
    assert dr(n - 3) == 6, f"n={n}: expected DR(n-3)=6, got {dr(n-3)}"
for n in range(6, 10000, 9):       # DR(n) = 6
    assert dr(n + 3) == 9, f"n={n}: expected DR(n+3)=9, got {dr(n+3)}"

# =============================================================================
# D. 5-Boundary: +9 spacing, period 9
# =============================================================================
# DR(5 + 9k) = 5 for all k >= 0.
for k in range(1000):
    assert dr(5 + 9 * k) == 5, f"k={k}: DR(5+9k) != 5"

# The 1-9 digital-root grid has period 9: DR(n+9) = DR(n) for all n>0.
for n in range(1, 1000):
    assert dr(n + 9) == dr(n), f"period-9 fails at n={n}"

# =============================================================================
# E. 123/321 Mirror: 444 = 12×37, 888 = 24×37
# =============================================================================
assert 123 + 321 == 444
assert 444 == 12 * 37
assert 444 * 2 == 888
assert 888 == 24 * 37
assert dr(444) == 3   # 4+4+4=12, 1+2=3
assert dr(888) == 6

# =============================================================================
# F. 6×4 Grid / 64 → 27 = 3³  (consecutive perfect cubes)
# =============================================================================
# 4³ = 64, 3³ = 27.  The two consecutive perfect cubes bracket 37:  27 < 37 < 64.
# DR(64) = DR(6+4) = DR(10) = 1.
# DR(27) = DR(2+7) = DR(9) = 9.
assert 4 ** 3 == 64
assert 3 ** 3 == 27
assert 27 < 37 < 64
assert dr(64) == 1
assert dr(27) == 9
# Position 3: 27 = 3³ is the cube of 3, the third perfect cube (1,8,27).
cubes = [n ** 3 for n in range(1, 10)]
assert cubes.index(27) == 2   # 0-indexed → "position 3" in 1-indexed terms
assert cubes[2] == 27

# =============================================================================
# G. 7-Digit Matrix: center 28 = 2×(3+4+7)
# =============================================================================
anchor_digits = (3, 4, 7)
digit_sum = sum(anchor_digits)
center = 2 * digit_sum
assert digit_sum == 14
assert center == 28
assert center == 2 * 14
assert dr(28) == dr(2 + 8) == 1   # DR(28)=10→1

# =============================================================================
# H. Tesla {3,6,9}: 4-bit numbers — DR-3 subclass bends to 3
# =============================================================================
# 4-bit numbers: 1 through 15.
four_bit = list(range(1, 16))
tesla_class = [n for n in four_bit if dr(n) in {3, 6, 9}]  # {3,6,9,12,15}
assert set(tesla_class) == {3, 6, 9, 12, 15}

# DR-3 subclass (DR=3) within 4-bit range: {3, 12}
dr3_class = [n for n in four_bit if dr(n) == 3]
assert dr3_class == [3, 12]
# "4-bit bend → 3": 3 is the generator; 12 = 4×3 reduces back to DR=3.
assert dr(3) == 3
assert dr(12) == 3

# =============================================================================
# I. Date Coordinates: project session date 2026-04-11 → DR chain
# =============================================================================
# Session date: 2026-04-11
year, month, day = 2026, 4, 11
dr_year  = dr(sum(int(d) for d in str(year)))   # 2+0+2+6=10→1
dr_month = dr(month)                             # 4
dr_day   = dr(sum(int(d) for d in str(day)))     # 1+1=2
full_date_digits = sum(int(d) for d in "20260411")  # 2+0+2+6+0+4+1+1=16
dr_full = dr(full_date_digits)                   # 16→7

assert dr_year  == 1
assert dr_month == 4
assert dr_day   == 2
assert dr_full  == 7
# DR chain for the full date integer 20260411:
date_val = 20260411
assert dr(date_val) == 7

# =============================================================================
# J. Cardano / ω: roots of x³ − 3x − 1 = 0
# =============================================================================
# This cubic has discriminant Δ = 4p³ + 27q² with p=−3, q=−1:
# Δ = 4(−3)³ + 27(−1)² = −108 + 27 = ... use standard form Δ = −4(−3)³ − 27(−1)² = 108−27 = 81.
# Δ > 0: three distinct real roots (casus irreducibilis — requires ω to express via radicals).
# Roots: 2cos(2π/9), 2cos(8π/9), 2cos(14π/9).
# Connection to ω = e^(2πi/3): ω satisfies ω² + ω + 1 = 0 → ω = (−1 ± i√3)/2.
# DR(81) = 9; DR of discriminant = 9 (Tesla anchor).

import math

p_coeff, q_coeff = -3, -1
discriminant = -4 * p_coeff**3 - 27 * q_coeff**2   # 81
assert discriminant == 81
assert dr(discriminant) == 9

# Verify the three roots numerically
roots = [2 * math.cos(math.pi / 9 + 2 * math.pi * k / 3) for k in range(3)]
for r in roots:
    val = r**3 - 3*r - 1
    assert abs(val) < 1e-9, f"root {r:.6f} fails: x³−3x−1 = {val:.2e}"

# ω² + ω + 1 = 0; "3ω" refers to 3×ω (the Eisenstein unit scaled by 3).
omega = complex(-0.5, math.sqrt(3) / 2)   # e^(2πi/3)
assert abs(omega**2 + omega + 1) < 1e-12

# =============================================================================
# K. DR=1 cluster and multiplicative identity DR(11g) = DR(44g) for 3∣g
# =============================================================================
# DR=1 cluster: c (speed of light m/s), 37, 73, 2701 = 37×73
c_light = 299_792_458
assert dr(c_light) == 1   # digit sum 55→10→1
assert dr(37) == 1
assert dr(73) == 1
assert dr(2701) == 1
assert 37 * 73 == 2701

# Multiplicative identity: 44 − 11 = 33 = 9×(11/3); more directly:
#   11·3k ≡ 6k (mod 9)  and  44·3k ≡ 6k (mod 9)
# so 11g ≡ 44g (mod 9) whenever g = 3k.
# Cycle of 6k mod 9: 6, 3, 9, 6, 3, 9, …  (period 3)
assert 11 % 9 == 2
assert 44 % 9 == 8
assert (11 * 3) % 9 == (44 * 3) % 9 == 6

for k in range(1, 1000):
    g = 3 * k
    assert dr(11 * g) == dr(44 * g), f"identity fails at g={g}"

# The 6k mod 9 cycle: 6,3,0,6,3,0,… but DR maps 0→9, giving 6,3,9,6,3,9,…
expected_dr_cycle = [6, 3, 9]
for k in range(1, 100):
    raw = (6 * k) % 9
    expected = expected_dr_cycle[(k - 1) % 3]
    actual = raw if raw != 0 else 9
    assert actual == expected, f"cycle fails at k={k}: got {actual}"


if __name__ == "__main__":
    print("Digital-Root Pattern Suite")
    print()

    print("A. Universal Collapse — S = {0,2,3,6,8,9}")
    for r, img in collapse_map.items():
        print(f"   {r} + delta → {img} ∈ S")
    print(f"   Residues outside S: {sorted(outside_S)} — all reach S in 1 step")
    print()

    print("B. 1-9 Core (×3 = 27 digits)")
    print(f"   sum = {sum(core_27)},  DR(135) = {dr(135)}")
    print()

    print("C. 9↔6 Flip via seed 3")
    print(f"   DR(9−3) = DR(6) = {dr(6)};  DR(6+3) = DR(9) = {dr(9)}")
    print()

    print("D. 5-Boundary: DR(5+9k)=5, period 9  (verified for k=0..999)")
    print()

    print("E. 123/321 Mirror")
    print(f"   123 + 321 = {123+321} = 12×37  ✓")
    print(f"   888 = 24×37  ✓;  DR(444)={dr(444)}, DR(888)={dr(888)}")
    print()

    print("F. 6×4 Grid / 64→27")
    print(f"   4³=64, DR(64)={dr(64)};  3³=27, DR(27)={dr(27)};  27<37<64  ✓")
    print()

    print("G. 7-Digit Matrix Center")
    print(f"   3+4+7={digit_sum};  center=2×{digit_sum}={center};  DR(28)={dr(28)}")
    print()

    print("H. Tesla 4-bit bend → 3")
    print(f"   Tesla class (DR∈{{3,6,9}}): {tesla_class}")
    print(f"   DR-3 subclass: {dr3_class}")
    print()

    print("I. Date Coordinates (2026-04-11)")
    print(f"   DR(year)={dr_year}, DR(month)={dr_month}, DR(day)={dr_day}, DR(full)={dr_full}")
    print()

    print("J. Cardano / ω  (x³−3x−1=0)")
    print(f"   Discriminant = {discriminant},  DR({discriminant}) = {dr(discriminant)}")
    print(f"   Roots: {[f'{r:.6f}' for r in roots]}")
    print(f"   ω = e^(2πi/3) satisfies ω²+ω+1=0  ✓")
    print()

    print("K. DR=1 cluster and 11g ≡ 44g (mod 9) for 3∣g")
    print(f"   DR(c=299792458)={dr(c_light)}, DR(37)={dr(37)}, DR(73)={dr(73)}, DR(2701)={dr(2701)}")
    print(f"   37 × 73 = {37*73}  ✓")
    print(f"   11 mod 9 = {11%9},  44 mod 9 = {44%9};  11·3k ≡ 44·3k ≡ 6k (mod 9)")
    print(f"   DR(11g)=DR(44g) verified for g=3k, k=1..999")
    print(f"   6k DR cycle: {[expected_dr_cycle[(k-1)%3] for k in range(1,10)]}…")
    print()

    print("All assertions passed.")
