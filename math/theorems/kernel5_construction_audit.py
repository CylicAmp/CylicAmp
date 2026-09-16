# math/theorems/kernel5_construction_audit.py
"""
Kernel-Dim-5 Construction Audit — {0,13} Matrix

The first matrix to achieve kernel dimension 5 over Z/26Z in this session.

Construction (from Python code provided):
  M = 13 × B  where B is a 0/1 matrix of rank 4 over Z/2Z.
  Base rows b₀,b₁,b₂,b₃ ∈ {0,1}^9;  rows 5-9 = pairwise sums mod 26.

Key algebraic facts:
  SNF(M) = 13 × SNF(B) = [13, 13, 13, 13, 26, 26, 26, 26, 0]
  - 13 × 1 = 13   (four times)
  - 13 × 2 = 26   (four times, from the 2s in SNF(B))
  - 13 × 0 = 0    (one zero, from rank deficit of B)

  Kernel over Z/26Z = #{d : gcd(d,26) = 26 OR d = 0}
    = #{26,26,26,26,0} = 5  ✓

  Rank over Z/2Z  = 4  (13 ≡ 1 mod 2; rank(M mod 2) = rank(B mod 2) = 4)
  Rank over Z/13Z = 0  (13 ≡ 0 mod 13; entire matrix vanishes)
  Rank over Q     = 8  (NOT 4; the code comment is wrong — one zero in SNF)

TABLE vs CODE discrepancy:
  R5 in the presented table = [13,13, 0,13, 0,13,13,13, 0]
  R5 from the Python code   = [13, 0,13, 0,13,13,13,13, 0]
  Columns 2 and 3 are transposed in the table.
  Table matrix gives rank 9 over Q, kernel Z/26Z = 4 (not 5).
  The CODE matrix is correct for the kernel-dim-5 claim.

IMPORTANT CONTEXT:
  This matrix is an artificially engineered {0,13} matrix.
  It has NO entries from DR, T operator, or any element of the framework.
  It is not the "Sovereign Matrix" — it is a rank-4 binary matrix scaled by 13.
  The kernel-dim-5 property follows trivially from M=13B:
    - 13 | all entries → M mod 13 = 0 → left kernel mod 13 = full space
    - CRT: kernel mod 26 ≥ kernel mod 13 contributions

Classification: Theorem (kernel-dim-5 first achieved); Refutation (not the framework matrix)
"""

import numpy as np
from math import gcd
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from smith_normal_form_z26 import smith_normal_form_integer, kernel_dim_mod_n


def _rank_mod_p(A, p):
    M = A % p; rows, cols = M.shape; pr = 0; r = 0
    for c in range(cols):
        if pr >= rows: break
        f = next((x for x in range(pr, rows) if M[x, c] % p), None)
        if f is None: continue
        M[[pr, f]] = M[[f, pr]]
        inv = pow(int(M[pr, c]), -1, p)
        M[pr] = M[pr] * inv % p
        for row in range(rows):
            if row != pr and M[row, c] % p:
                M[row] = (M[row] - M[row, c] * M[pr]) % p
        r += 1; pr += 1
    return r


# ── Code-generated matrix (correct version) ──────────────────────────────────

base = np.array([
    [13, 13,  0,  0, 13,  0, 13,  0,  0],
    [ 0, 13, 13,  0,  0, 13,  0, 13,  0],
    [ 0,  0, 13, 13,  0,  0, 13,  0, 13],
    [13,  0,  0, 13, 13,  0,  0, 13,  0],
], dtype=int)

KERNEL5_M = np.zeros((9, 9), dtype=int)
KERNEL5_M[0:4] = base
KERNEL5_M[4] = (base[0] + base[1]) % 26
KERNEL5_M[5] = (base[1] + base[2]) % 26
KERNEL5_M[6] = (base[2] + base[3]) % 26
KERNEL5_M[7] = (base[3] + base[0]) % 26
KERNEL5_M[8] = (base[0] + base[2]) % 26

B = KERNEL5_M // 13   # 0/1 matrix

SNF_K5    = smith_normal_form_integer(KERNEL5_M.astype(object))
SNF_B     = smith_normal_form_integer(B.astype(object))
RANK_Q    = int(np.linalg.matrix_rank(KERNEL5_M.astype(float)))
RANK_2    = _rank_mod_p(KERNEL5_M.copy(), 2)
RANK_13   = _rank_mod_p(KERNEL5_M.copy(), 13)
KERNEL_26 = kernel_dim_mod_n(KERNEL5_M, 26)
KERNEL_2  = 9 - RANK_2
KERNEL_13 = 9 - RANK_13

# ── Table matrix (R5 transposed — incorrect) ─────────────────────────────────

TABLE_R5_WRONG = [13, 13, 0, 13, 0, 13, 13, 13, 0]   # as written in message
TABLE_R5_RIGHT = list(map(int, KERNEL5_M[4]))          # from code


# ── Assertions ────────────────────────────────────────────────────────────────

# R5 discrepancy
assert TABLE_R5_WRONG != TABLE_R5_RIGHT

# Code matrix: kernel dim 5 achieved
assert KERNEL_26 == 5
assert KERNEL_2  == 5
assert KERNEL_13 == 9   # 13 vanishes mod 13 → full kernel

# SNF structure: M = 13 * B, SNF(M) = 13 * SNF(B)
assert SNF_B == [1, 1, 1, 1, 2, 2, 2, 2, 0]
assert SNF_K5 == [13, 13, 13, 13, 26, 26, 26, 26, 0]
assert [13 * d for d in SNF_B] == SNF_K5

# Rank over Q = 8 (NOT 4 as code comment claims)
assert RANK_Q == 8
assert RANK_2 == 4

# All entries in {0, 13}
assert set(int(x) for x in KERNEL5_M.flatten()) == {0, 13}

# Not related to DR or T: no entry in 1..9 range
assert KERNEL5_M.max() == 13
assert 1 not in KERNEL5_M and 9 not in KERNEL5_M


if __name__ == "__main__":
    print("Kernel-Dim-5 Construction Audit — {0,13} Matrix")
    print()
    print("  Matrix (code-generated, correct):")
    for i, row in enumerate(KERNEL5_M):
        src = "base" if i < 4 else f"base[{[0,1,2,3,0,1,2][i-4:i-3+1][0]}]+base[{[1,2,3,0,2][i-4]}] mod 26"
        print(f"    R{i+1}: {list(map(int,row))}")
    print()
    print(f"  B = M/13 entries: {set(int(x) for x in B.flatten())}")
    print(f"  SNF(B)   = {SNF_B}")
    print(f"  SNF(M)   = {SNF_K5}  = 13 × SNF(B)  ✓")
    print()
    print(f"  Rank over Q   = {RANK_Q}   (code comment says 4 — WRONG)")
    print(f"  Rank over Z/2Z = {RANK_2}   kernel={KERNEL_2}")
    print(f"  Rank over Z/13Z= {RANK_13}  kernel={KERNEL_13}  (13≡0 mod 13 → all zero)")
    print(f"  Kernel Z/26Z  = {KERNEL_26}  ✓  (first matrix to achieve this)")
    print()
    print("  R5 discrepancy:")
    print(f"    Table: {TABLE_R5_WRONG}")
    print(f"    Code:  {TABLE_R5_RIGHT}  ← correct (cols 2,3 transposed in table)")
    print()
    print("  Context:")
    print("  This matrix is 13 × (rank-4 binary matrix).")
    print("  It contains no DR, T-operator, or framework entries (1–9).")
    print("  Kernel=5 follows from: 13|all entries → M≡0 mod 13 → large mod-13 kernel.")
    print("  The SNF structure [13^4, 26^4, 0] is entirely determined by the")
    print("  binary rank structure, not by any property of the Sovereign Matrix.")
    print()
    print("All assertions passed.")
