# math/theorems/matrix_m_mod37_audit.py
"""
Matrix M mod 37 — Fifth Submission Audit

Matrix presented alongside checkerboard parity patterns and 23/32 symmetry
claims.  Computational audit establishes that this is the SAME matrix as
PROVIDED_M (entry 80), submitted again under a new label.

─────────────────────────────────────────────────────────────────────────────
IDENTITY WITH ENTRY 80 (PROVIDED_M)
─────────────────────────────────────────────────────────────────────────────
  SNF       = [1, 9, 9, 9, 9, 9, 9, 9, 450]  (exact match)
  det       = 2 152 336 050                    (exact match)
  Rank Q    = 9                                (exact match)
  Kernel    = 0 over Z/26Z                     (exact match)
  Asymmetric pairs = 28                        (exact match)
  M[0,4]=2, M[4,0]=5                           (specific pair, exact match)

  All six independent identifiers agree: this is PROVIDED_M.

  The label "Matrix M mod 37" does not introduce a new matrix.
  Since all entries are < 37, M mod 37 = M.

─────────────────────────────────────────────────────────────────────────────
PARITY / CHECKERBOARD PATTERN — ANALYSIS
─────────────────────────────────────────────────────────────────────────────
Submitted alongside:
  1. Checkerboard of ■/□ symbols, rows 1-9, alternating by (i+j) mod 2.
  2. "9=■□■□■□■□■=1" row-reversal relabelling.
  3. "23/32 symmetry": 23 and 32 are decimal digit-reversals.
  4. Section 3 "deterministic shift" from 23 to 32 via operations
     (12-4=8, 21-3=18).

  What is mathematically content-free:
    - The checkerboard is position-index parity. No connection to M is
      stated or derivable; the same visual arises from ANY 9×9 grid.
    - Row-reversal of indices 1-9 → 9-1 is a trivial bijection.
    - 23 and 32 are digit-reversals; calling them "boundary gates" is
      informal language, not a definition of any map.
    - 23-8=15, 21-3=18 are arithmetic. The subtracted values (8, 3)
      and their relationship to the matrix are unspecified.

  No map from {■,□} patterns or from {23,32} to ker(M) or to Riemann zeros
  is defined.  These are descriptive labels on arithmetic, not theorems.

─────────────────────────────────────────────────────────────────────────────
MATRIX PROPERTIES (same as entry 80)
─────────────────────────────────────────────────────────────────────────────
  SNF = [1, 9, 9, 9, 9, 9, 9, 9, 450]
  gcd(d, 26) for each SNF entry: [1, 1, 1, 1, 1, 1, 1, 1, 2]
    → no entry divisible by 26 → kernel dim Z/26Z = 0
  gcd(450, 26) = 2 ≠ 26 → 450 contributes 0 to kernel
  gcd(9, 26)   = 1 → all seven 9s contribute 0

  Rank F_2:  8  (kernel mod 2 = 1)
  Rank F_13: 9  (kernel mod 13 = 0)
  Rank F_37: 9  (kernel mod 37 = 0; M already has entries < 37)

  Diagonal: [10,13,18,16,10,15,12,16,18]
    — entries exceed DR/T range (max 10) → NOT a pure DR/T-operator matrix
    — not equal to DR(k^2) for k=1..9 (those would be [1,4,9,7,7,9,4,1,9])

  Not symmetric: M[i,j] ≠ M[j,i] for 28 pairs, e.g. M[0,4]=2, M[4,0]=5.

Classification: Refutation (same matrix re-submitted; kernel remains 0)
"""

import numpy as np
from math import gcd
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from smith_normal_form_z26 import smith_normal_form_integer, kernel_dim_mod_n

M = np.array([
    [10,  2,  3,  4,  2,  4,  3,  2,  1],
    [ 2, 13,  6,  8,  4,  8,  6,  4,  2],
    [ 3,  6, 18,  3,  6,  3,  9,  6,  3],
    [ 4,  8,  3, 16,  8,  7,  3,  8,  4],
    [ 5,  1,  6,  2, 10,  2,  6,  1,  5],
    [ 6,  3,  9,  6,  3, 15,  9,  3,  6],
    [ 7,  5,  3,  1,  5,  1, 12,  5,  7],
    [ 8,  7,  6,  5,  7,  5,  6, 16,  8],
    [ 9,  9,  9,  9,  9,  9,  9,  9, 18],
], dtype=int)


def _rank_mod_p(A, p):
    M2 = A % p; rows, cols = M2.shape; r = 0; pr = 0
    for c in range(cols):
        if pr >= rows: break
        f = next((x for x in range(pr, rows) if M2[x, c] % p), None)
        if f is None: continue
        M2[[pr, f]] = M2[[f, pr]]
        inv = pow(int(M2[pr, c]), -1, p)
        M2[pr] = M2[pr] * inv % p
        for row in range(rows):
            if row != pr and M2[row, c] % p:
                M2[row] = (M2[row] - M2[row, c] * M2[pr]) % p
        r += 1; pr += 1
    return r


RANK_Q    = int(np.linalg.matrix_rank(M.astype(float)))
RANK_2    = _rank_mod_p(M.copy(), 2)
RANK_13   = _rank_mod_p(M.copy(), 13)
RANK_37   = _rank_mod_p(M.copy(), 37)
KERNEL_26 = kernel_dim_mod_n(M, 26)
KERNEL_2  = 9 - RANK_2
KERNEL_13 = 9 - RANK_13
KERNEL_37 = 9 - RANK_37
SNF_M     = smith_normal_form_integer(M.astype(object))
ASYM_PAIRS = [(i, j) for i in range(9) for j in range(i+1,9)
              if int(M[i,j]) != int(M[j,i])]
DIAG = [int(M[i,i]) for i in range(9)]


# ── Assertions ────────────────────────────────────────────────────────────────

# Identity with entry 80 (PROVIDED_M)
assert SNF_M == [1, 9, 9, 9, 9, 9, 9, 9, 450], f"SNF mismatch: {SNF_M}"
assert RANK_Q == 9
assert KERNEL_26 == 0
assert len(ASYM_PAIRS) == 28
assert int(M[0, 4]) == 2 and int(M[4, 0]) == 5   # the identifying pair

# No entry ≡ 0 (mod 26) and no SNF factor divisible by 26
assert all(gcd(int(d), 26) < 26 and int(d) != 0 for d in SNF_M)

# Diagonal exceeds DR range
assert max(DIAG) == 18 and any(d > 10 for d in DIAG)

# Not symmetric
assert len(ASYM_PAIRS) > 0

# Kernel over Z/37Z = 0 (rank = 9 over F_37)
assert KERNEL_37 == 0

# gcd(450, 26) = 2 ≠ 26 → 450 does not contribute to kernel
assert gcd(450, 26) == 2

# DR(k^2) for k=1..9: all in {1,...,9}, none match diagonal
DR = lambda n: (n - 1) % 9 + 1 if n > 0 else 0
dr_sq = [DR(k*k) for k in range(1, 10)]
assert dr_sq == [1, 4, 9, 7, 7, 9, 4, 1, 9]
assert DIAG != dr_sq   # diagonal is NOT DR(k^2)


if __name__ == "__main__":
    print("Matrix M mod 37 — Fifth Submission Audit")
    print()
    print("  RESULT: This is the same matrix as PROVIDED_M (entry 80).")
    print()
    print("  Six identifiers — all match entry 80:")
    print(f"    SNF          = {SNF_M}")
    print(f"    Rank Q       = {RANK_Q}")
    print(f"    Kernel Z/26Z = {KERNEL_26}")
    print(f"    Asym. pairs  = {len(ASYM_PAIRS)}")
    print(f"    M[0,4]={M[0,4]}, M[4,0]={M[4,0]}  (identifying asymmetric pair)")
    print(f"    det ≈ {round(float(np.linalg.det(M.astype(float))))}")
    print()
    print("  Since all entries < 37: 'M mod 37' = M.  Label adds no new information.")
    print()
    print("  Kernel Z/26Z = 0. gcd structure of SNF factors:")
    for d in SNF_M:
        g = gcd(int(d), 26)
        print(f"    d={d:>4}  gcd(d,26)={g}  {'→ no torsion' if g < 26 else '→ TORSION'}")
    print()
    print("  Rank breakdown:")
    print(f"    Over Q:   {RANK_Q}   (full rank — invertible)")
    print(f"    Over F_2: {RANK_2}   (kernel mod 2 = {KERNEL_2})")
    print(f"    Over F_13:{RANK_13}  (kernel mod 13 = {KERNEL_13})")
    print(f"    Over F_37:{RANK_37}  (kernel mod 37 = {KERNEL_37})")
    print()
    print("  Parity / checkerboard pattern:")
    print("    Checkerboard ■/□ = position parity (i+j) mod 2.")
    print("    Applies identically to every 9×9 grid; no connection to M.")
    print("    '23/32 symmetry' = decimal digit reversal of 23 → 32.")
    print("    '23-8=15, 21-3=18' = arithmetic; subtracted values unexplained.")
    print("    None of these constitute a mathematical definition or theorem.")
    print()
    print("  Diagonal (NOT DR(k^2) values):", DIAG)
    print("    DR(k^2) for k=1..9 would be:", dr_sq)
    print()
    print("All assertions passed.")
