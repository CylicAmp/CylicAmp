# math/theorems/sovereign_matrix_v3_audit.py
"""
Sovereign Matrix V3 — SNF Audit

Matrix: M[i,j] = DR(row_i × j), row indices {10,2,3,4,5,6,7,8,9}, cols 1–9.
Entries show literal '10' wherever the product equals 10; otherwise DR(product).

Structure:
  - No duplicate rows  → full rank possible
  - Last column: all 9s  (DR(row_i × 9) = 9 for all row_i coprime to 9)
  - Last row: all 9s   (DR(9 × j) = 9 for all j)
  - Rows 3,6 are period-3: [a,b,9,a,b,9,a,b,9]  (multiples of 3 in DR)

SNF:  [1, 9, 9, 9, 9, 9, 9, 9, 9]
  - One trivial factor + eight factors of 9
  - NO zero diagonal entries → rank = 9 over Q (invertible)

Kernel:
  Z/2Z:  0
  Z/13Z: 0
  Z/26Z: 0   (all SNF entries coprime to 26; gcd(9,26)=1; gcd(1,26)=1)

Elementary divisors mod 26: all 1 → trivial module, no torsion.

This matrix is full rank with trivial kernel over Z/26Z.
Theorem 9 (kernel dim 5) is not realised by this matrix.

Classification: Theorem (SNF infrastructure)
"""

import numpy as np
from math import gcd
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from smith_normal_form_z26 import smith_normal_form_integer, kernel_dim_mod_n

SOVEREIGN_M_V3 = np.array([
    [10, 2, 3, 4, 5, 6, 7, 8, 9],
    [ 2, 4, 6, 8,10, 3, 5, 7, 9],
    [ 3, 6, 9, 3, 6, 9, 3, 6, 9],
    [ 4, 8, 3, 7, 2, 6, 1, 5, 9],
    [ 5, 1, 6, 2, 7, 3, 8, 4, 9],
    [ 6, 3, 9, 6, 3, 9, 6, 3, 9],
    [ 7, 5, 3, 1, 8, 6, 4, 2, 9],
    [ 8, 7, 6, 5, 4, 3, 2, 1, 9],
    [ 9, 9, 9, 9, 9, 9, 9, 9, 9],
], dtype=int)

ROW_INDICES = [10, 2, 3, 4, 5, 6, 7, 8, 9]

def dr(n): return (n - 1) % 9 + 1 if n > 0 else 0

SNF_V3        = smith_normal_form_integer(SOVEREIGN_M_V3.astype(object))
RANK_Q        = int(np.linalg.matrix_rank(SOVEREIGN_M_V3))
KERNEL_DIM_26 = kernel_dim_mod_n(SOVEREIGN_M_V3, 26)
KERNEL_DIM_2  = kernel_dim_mod_n(SOVEREIGN_M_V3, 2)
KERNEL_DIM_13 = kernel_dim_mod_n(SOVEREIGN_M_V3, 13)
ELEM_DIVS_26  = [gcd(d, 26) for d in SNF_V3]

# ── Assertions ────────────────────────────────────────────────────────────────

# No duplicate rows
for i in range(9):
    for j in range(i + 1, 9):
        assert not np.all(SOVEREIGN_M_V3[i] == SOVEREIGN_M_V3[j]), f"R{i+1}==R{j+1}"

# Full rank
assert RANK_Q == 9

# SNF: one 1, eight 9s, no zeros
assert SNF_V3 == [1, 9, 9, 9, 9, 9, 9, 9, 9], f"Unexpected SNF: {SNF_V3}"

# Trivial kernel over all relevant moduli
assert KERNEL_DIM_26 == 0
assert KERNEL_DIM_2  == 0
assert KERNEL_DIM_13 == 0

# Elementary divisors mod 26: all 1 (gcd(9,26)=1)
assert all(d == 1 for d in ELEM_DIVS_26), f"Non-trivial divisors: {ELEM_DIVS_26}"
assert gcd(9, 26) == 1   # key: 9 and 26 coprime → no torsion mod 26

# Generation rule: M = DR(row_i × col_j), literal 10 where product = 10
M_test = SOVEREIGN_M_V3.copy(); M_test[M_test == 10] = 1
for i, ri in enumerate(ROW_INDICES):
    for j in range(1, 10):
        assert int(M_test[i, j - 1]) == dr(ri * j), \
            f"Rule mismatch at R{i+1},C{j}: dr({ri}*{j})={dr(ri*j)}, got {M_test[i,j-1]}"

# Last column all 9
assert np.all(SOVEREIGN_M_V3[:, 8] == 9)
# Last row all 9
assert np.all(SOVEREIGN_M_V3[8, :] == 9)
# Rows 3,6 period-3 (multiples of 3 in DR)
assert list(SOVEREIGN_M_V3[2]) == [3, 6, 9] * 3
assert list(SOVEREIGN_M_V3[5]) == [6, 3, 9] * 3

# Row sums: {45, 54, 81} only (from DR structure)
row_sums = list(map(int, SOVEREIGN_M_V3.sum(axis=1)))
assert set(row_sums) <= {45, 54, 81}


if __name__ == "__main__":
    print("Sovereign Matrix V3 — SNF Audit")
    print()
    print("  Generation rule: M[i,j] = DR(row_i × j),  row indices =", ROW_INDICES)
    print("  Literal '10' used where product = 10 (i*j=10, not where DR=1 generally)")
    print()
    print("  Matrix:")
    for i, row in enumerate(SOVEREIGN_M_V3):
        print(f"    R{i+1} (i={ROW_INDICES[i]:2d}): {list(map(int,row))}")
    print()
    print(f"  Rank over Q: {RANK_Q}  (no duplicate rows; invertible)")
    print(f"  SNF: {SNF_V3}")
    print(f"  gcd(9, 26) = {gcd(9,26)}  → all SNF factors coprime to 26")
    print()
    print(f"  Kernel dimensions:")
    print(f"    Z/2Z:  {KERNEL_DIM_2}   (no torsion at 2)")
    print(f"    Z/13Z: {KERNEL_DIM_13}  (no torsion at 13)")
    print(f"    Z/26Z: {KERNEL_DIM_26}  (no torsion; trivial module)")
    print()
    print(f"  Elementary divisors mod 26: {ELEM_DIVS_26}")
    print()
    eigs = sorted(np.linalg.eigvals(SOVEREIGN_M_V3).real, reverse=True)
    print(f"  Eigenvalues: {[round(e,4) for e in eigs]}")
    print(f"  Row sums: {list(map(int, SOVEREIGN_M_V3.sum(axis=1)))}")
    print()
    print("  Theorem 9 status:")
    print(f"    Kernel dim over Z/26Z = {KERNEL_DIM_26}  (Theorem 9 requires 5)")
    print(f"    This matrix does not realise the claimed kernel dimension.")
    print()
    print("All assertions passed.")
