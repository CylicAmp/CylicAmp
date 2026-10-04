# math/theorems/triangular_partition_audit.py
"""
Triangular Partition Diagram — Ordered 2-Compositions of 5

Pattern submitted:
  0(5-----1-1-1-1-1      row 0: sum=0, complement=5, 5 right-ones
  0+1(4----1-1-1-1       row 1: sum=1, complement=4, 4 right-ones
  1+1=2(3---1-1-1        row 2: sum=2, complement=3, 3 right-ones
  1+1+1=3(2- -1-1        row 3: sum=3, complement=2, 2 right-ones
  1+1+1+1=4(-1-1         row 4: sum=4, complement=1, 1 right-one (*)
  1+1+1+1+1=5(0          row 5: sum=5, complement=0, 0 right-ones

(*) Row 4 is formatted as "(-1-1"; reading "(−" as the separator-dash and
    "1" as the single right-one, the complement is 1 consistent with 4+1=5.
    The trailing "-1" appears to be a character-alignment artifact.

─────────────────────────────────────────────────────────────────────────────
MATHEMATICAL CONTENT
─────────────────────────────────────────────────────────────────────────────
  The diagram shows the 6 ordered compositions of 5 into two non-negative
  integer parts: {(n, 5-n) : n ∈ {0,1,2,3,4,5}}.

  Left column  = n (accumulated by successive +1 additions)
  Right column = 5-n (shown as (5-n) unit steps "1")
  Sum          = n + (5-n) = 5 for all rows  ✓

  This is equivalent to the 6 lattice points on the simplex:
    {(a,b) ∈ ℤ_≥0² : a + b = 5}

─────────────────────────────────────────────────────────────────────────────
WHAT THIS DOES NOT ESTABLISH
─────────────────────────────────────────────────────────────────────────────
  1. Kernel dimension.
       "There are 5 ones in row 0" does not mean ker(M) over Z/26Z has dim 5.
       Kernel dimension is determined by SNF — specifically the count of SNF
       diagonal entries d with gcd(d,26)=26 or d=0.
       For PROVIDED_M: SNF=[1,9,9,9,9,9,9,9,450], kernel Z/26Z=0.

  2. Linear independence.
       In Z/26Z (or any ring), 1+1+1+1+1 = 5 is a single scalar, not a
       collection of 5 linearly independent vectors.
       To span a 5-dimensional kernel one needs 5 vectors in (Z/26Z)^9,
       each annihilated by M, that are linearly independent over Z/26Z.
       These were computed (entry 88) for the {0,13} construction only.

  3. Any map to Riemann zeros.
       Lattice points (n, 5-n) ∈ ℤ² are pairs of non-negative integers.
       Riemann zero imaginary parts are transcendental reals.
       No injection from ℤ² to the zero sequence is defined.

  4. Connection to the 1/137 framework.
       The pattern 0+1+1+...+1=n is the successor function on ℕ.
       It generates no DR, T-operator, or Z/26Z structure.

─────────────────────────────────────────────────────────────────────────────
NOTE ON PREVIOUS "ZERO" PATTERN
─────────────────────────────────────────────────────────────────────────────
  Presented in same session:
    0         → 1 zero
    00        → 2 zeros
    000       → 3 zeros
    0,000     → 4 zeros (1 before comma + 3 after → ratio 1/4)
    00,000    → 5 zeros (2 before + 3 after → ratio 2/3 "~")
    000,000   → 6 zeros (3 before + 3 after → ratio 3/3 = 1 = 2×3)

  This is a decimal place-value notation for groupings of zeros (thousands
  separator convention).  "1/4", "2/3~" are the ratios of pre-comma zeros
  to post-comma zeros — not fractions in any algebraic structure.
  "2×3" = 6 = total zeros in the last row, a count identity.
  No algebraic claim follows from these ratio observations.

Classification: Observation (counting pattern); Refutation (kernel-dim claim)
"""

# ── Verify the combinatorial structure ────────────────────────────────────────

ROWS = [
    (0, 5, 5),   # (left_sum, complement, right_ones_count)
    (1, 4, 4),
    (2, 3, 3),
    (3, 2, 2),
    (4, 1, 1),   # row 4: complement=1, ONE right-one (formatting artifact noted)
    (5, 0, 0),
]

# Sum invariant: left + complement = 5 for all rows
for left, comp, _ in ROWS:
    assert left + comp == 5, f"Sum invariant broken: {left} + {comp} ≠ 5"

# Number of compositions: C(5+1, 1) = 6 (ordered 2-compositions of 5)
assert len(ROWS) == 6

# Left sums are 0,1,2,3,4,5 (strictly increasing)
assert [r[0] for r in ROWS] == list(range(6))

# Complements are 5,4,3,2,1,0 (strictly decreasing)
assert [r[1] for r in ROWS] == list(range(5, -1, -1))

# Right-one counts equal complements (visual representation)
assert all(right == comp for _, comp, right in ROWS)

# ── Kernel dimension is NOT derivable from this pattern ───────────────────────

# PROVIDED_M kernel Z/26Z = 0, not 5:
from math import gcd
SNF_PROVIDED_M = [1, 9, 9, 9, 9, 9, 9, 9, 450]
kernel_provided = sum(1 for d in SNF_PROVIDED_M if d == 0 or gcd(d, 26) == 26)
assert kernel_provided == 0   # not 5

# The {0,13} matrix (entry 86) has kernel=5, but from M=13B structure:
SNF_K5 = [13, 13, 13, 13, 26, 26, 26, 26, 0]
kernel_k5 = sum(1 for d in SNF_K5 if d == 0 or gcd(d, 26) == 26)
assert kernel_k5 == 5   # correct, but from SNF — not from counting pattern

# 5 as a scalar in Z/26Z: gcd(5,26)=1 → 5 is a unit → spans all of Z/26Z
# "5 ones" is one element (= 5), not a 5-dimensional structure
assert gcd(5, 26) == 1   # 5 is a unit; no torsion

# Zero-comma pattern: ratio counts
zero_groups = [(1, 3), (2, 3), (3, 3)]   # (before-comma, after-comma) for 4,5,6 zeros
for before, after in zero_groups:
    total = before + after
    ratio_num = before
    ratio_den = after
    # These are just integer ratios, not elements of any algebraic structure
    assert total in (4, 5, 6)


if __name__ == "__main__":
    print("Triangular Partition Diagram — Ordered 2-Compositions of 5")
    print()
    print("  Pattern: {(n, 5-n) : n = 0, 1, 2, 3, 4, 5}")
    print()
    print(f"  {'Row':>3}  {'Left (sum)':>12}  {'Complement':>10}  {'Right ones':>10}  {'Total':>5}")
    print("  " + "-" * 50)
    for i, (left, comp, right) in enumerate(ROWS):
        left_str = "+".join(["1"]*left) if left > 0 else "0"
        print(f"  {i:>3}  {left_str:>12} = {left}  ({comp:>8})  {'1-'*(right-1)+'1' if right>0 else '':>10}  {left+comp:>5}")
    print()
    print("  Sum invariant: n + (5-n) = 5 for all rows  ✓")
    print("  6 rows = 6 ordered 2-compositions of 5")
    print()
    print("  What this establishes: a counting diagram for ℤ_≥0 pairs summing to 5.")
    print()
    print("  What this does NOT establish:")
    print("    Kernel dimension: determined by SNF, not by counting 1s.")
    print(f"    PROVIDED_M SNF={SNF_PROVIDED_M}")
    print(f"    → kernel Z/26Z = {kernel_provided}  (not 5)")
    print()
    print("    'Five 1s' in Z/26Z: 1+1+1+1+1 = 5, a unit (gcd(5,26)=1).")
    print("    This is a single element of Z/26Z, not a 5-dim module.")
    print()
    print("  Zero-comma pattern:")
    print("    0,000 / 00,000 / 000,000 = place-value zero-grouping")
    print("    Ratios 1/4, 2/3, 3/3 are pre/post-comma zero counts.")
    print("    These are counting observations, not algebraic claims.")
    print()
    print("All assertions passed.")
