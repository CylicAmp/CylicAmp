# math/theorems/sovereign_matrix_v2_audit.py
"""
Sovereign Matrix V2 — SNF Audit

Matrix provided with rows {R1..R9} and T-operator entries (10 preserved literally).

Structural observations:
  - R4 == R5  (identical rows → rank deficit 1)
  - R7 == R8  (identical rows → rank deficit 1)
  - Rank over Q = 7  (two zero eigenvalues, not 5 as claimed for Theorem 9)
  - No entry equals 56.  Max entry = 10.

SNF diagonal: [1, 1, 9, 9, 9, 9, 9, 0, 0]
  - Two zeros → kernel dim = 2 over Q (and over any Z/nZ)
  - Over Z/26Z: gcd(9,26)=1 for all seven non-zero entries → rank=7, kernel=2

Kernel dimensions:
  Z/2Z:  2   (not 5)
  Z/13Z: 2   (not 5)
  Z/26Z: 2   (not 5)

Elementary divisors mod 26: [1,1,1,1,1,1,1,26,26]
  Two torsion elements of order 26; rest trivial.

Row structure:
  R2, R4/R5, R6, R7/R8, R9 are cyclic left-shifts (by 0,1,6,7,8 positions)
  of the base sequence [2,4,6,8,10,3,5,7,9] (arithmetic step=2 under T-operator).
  R3 = [3,6,9,3,6,9,3,6,9] (period-3 multiples of 3 under DR).
  R1 = [10,2,3,4,5,6,7,8,9] (row index 10: T(10j) for j=1..9).

Classification: Theorem (SNF infrastructure)
"""

import numpy as np
from math import gcd
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from smith_normal_form_z26 import (
    smith_normal_form_integer, kernel_dim_mod_n, elementary_divisors_mod_n
)

SOVEREIGN_M_V2 = np.array([
    [10, 2, 3, 4, 5, 6, 7, 8, 9],
    [ 2, 4, 6, 8,10, 3, 5, 7, 9],
    [ 3, 6, 9, 3, 6, 9, 3, 6, 9],
    [ 4, 6, 8,10, 3, 5, 7, 9, 2],
    [ 4, 6, 8,10, 3, 5, 7, 9, 2],
    [ 5, 7, 9, 2, 4, 6, 8,10, 3],
    [ 7, 9, 2, 4, 6, 8,10, 3, 5],
    [ 7, 9, 2, 4, 6, 8,10, 3, 5],
    [ 9, 2, 4, 6, 8,10, 3, 5, 7],
], dtype=int)

SNF_V2         = smith_normal_form_integer(SOVEREIGN_M_V2.astype(object))
RANK_Q         = int(np.linalg.matrix_rank(SOVEREIGN_M_V2))
KERNEL_DIM_2   = kernel_dim_mod_n(SOVEREIGN_M_V2, 2)
KERNEL_DIM_13  = kernel_dim_mod_n(SOVEREIGN_M_V2, 13)
KERNEL_DIM_26  = kernel_dim_mod_n(SOVEREIGN_M_V2, 26)
ELEM_DIVS_26   = [gcd(d, 26) for d in SNF_V2]

# ── Base sequence structure ───────────────────────────────────────────────────

BASE_SEQ = [2, 4, 6, 8, 10, 3, 5, 7, 9]   # step-2 T-sequence, period 9

def cyclic_shift(seq, k):
    return seq[k:] + seq[:k]


# ── Assertions ────────────────────────────────────────────────────────────────

# Duplicate rows
assert np.all(SOVEREIGN_M_V2[3] == SOVEREIGN_M_V2[4])   # R4 == R5
assert np.all(SOVEREIGN_M_V2[6] == SOVEREIGN_M_V2[7])   # R7 == R8

# No entry equals 56 (the claimed "Sovereign Knot at (7,8)")
assert SOVEREIGN_M_V2.max() == 10
assert not np.any(SOVEREIGN_M_V2 == 56)

# Rank over Q = 7 (two duplicate rows reduce rank by 2)
assert RANK_Q == 7

# SNF: two zeros (rank deficit = kernel dim over Q = 2)
assert SNF_V2 == [1, 1, 9, 9, 9, 9, 9, 0, 0], f"Unexpected SNF: {SNF_V2}"

# Kernel dimensions
assert KERNEL_DIM_26 == 2    # NOT 5
assert KERNEL_DIM_2  == 2
assert KERNEL_DIM_13 == 2

# Elementary divisors mod 26: seven trivial + two full (order-26 torsion)
assert ELEM_DIVS_26 == [1, 1, 1, 1, 1, 1, 1, 26, 26]

# Row structure: R2,R4,R6,R7,R9 are shifts of base sequence
assert list(SOVEREIGN_M_V2[1]) == cyclic_shift(BASE_SEQ, 0)   # R2 shift=0
assert list(SOVEREIGN_M_V2[3]) == cyclic_shift(BASE_SEQ, 1)   # R4 shift=1
assert list(SOVEREIGN_M_V2[5]) == cyclic_shift(BASE_SEQ, 6)   # R6 shift=6
assert list(SOVEREIGN_M_V2[6]) == cyclic_shift(BASE_SEQ, 7)   # R7 shift=7
assert list(SOVEREIGN_M_V2[8]) == cyclic_shift(BASE_SEQ, 8)   # R9 shift=8

# R3 is period-3 (multiples of 3 mod 9)
assert list(SOVEREIGN_M_V2[2]) == [3, 6, 9] * 3

# Missing shifts (2, 3, 4, 5) explain the rank deficit:
# only 7 distinct rows occupy the orbit of base_seq (R2,R4=R5,R6,R7=R8,R9 = 5 shifts×, 2 duplicated)
distinct_rows = {tuple(r) for r in SOVEREIGN_M_V2}
assert len(distinct_rows) == 7   # 9 rows but only 7 distinct


if __name__ == "__main__":
    print("Sovereign Matrix V2 — SNF Audit")
    print()
    print("  Matrix:")
    for i, row in enumerate(SOVEREIGN_M_V2):
        dup = " ← DUPLICATE of R4" if i == 4 else (" ← DUPLICATE of R7" if i == 7 else "")
        print(f"    R{i+1}: {list(row)}{dup}")
    print()
    print(f"  Max entry: {SOVEREIGN_M_V2.max()}   Any entry == 56: {bool(np.any(SOVEREIGN_M_V2 == 56))}")
    print()
    print(f"  Rank over Q: {RANK_Q}  (7 distinct rows: R4=R5, R7=R8)")
    print(f"  SNF diagonal: {SNF_V2}")
    print()
    print(f"  Kernel dimensions:")
    print(f"    Z/2Z:  {KERNEL_DIM_2}   (NOT 5)")
    print(f"    Z/13Z: {KERNEL_DIM_13}  (NOT 5)")
    print(f"    Z/26Z: {KERNEL_DIM_26}  (NOT 5)")
    print()
    print(f"  Elementary divisors mod 26: {ELEM_DIVS_26}")
    print(f"  Two torsion elements of order 26; rest trivial.")
    print()
    print("  Row structure (base = [2,4,6,8,10,3,5,7,9], step-2 T-sequence):")
    for row_idx, shift in [(1,0),(3,1),(5,6),(6,7),(8,8)]:
        match = list(SOVEREIGN_M_V2[row_idx]) == cyclic_shift(BASE_SEQ, shift)
        print(f"    R{row_idx+1} = base shifted by {shift}  ({'✓' if match else '✗'})")
    print(f"    R3 = [3,6,9]×3 (period-3 DR multiples)")
    print(f"    R1 = T(10·j) for j=1..9 (row index = 10)")
    print()
    print("  Summary vs claimed 'Theorem 9' (kernel dim 5):")
    print(f"    Actual kernel dim over Z/26Z = {KERNEL_DIM_26}")
    print(f"    Actual rank over Q           = {RANK_Q}")
    print(f"    Entry at (7,8): {SOVEREIGN_M_V2[6,7]}  (claimed: 56)")
    print()
    print("All assertions passed.")
