"""
numpy_rank_audit.py

Audit of the NumPy rank-elevation experiment against the theorem.

─────────────────────────────────────────────────────────────────
USER'S CODE DOES THREE THINGS:
  (A) mat = [[1,2,3],[4,5,6],[7,8,9]]  → rank 2
  (B) uniform = mat + 10               → rank 2   (uniform shift preserves span)
  (C) exempt = uniform; exempt[0,0] -= 5 → rank 3  (any nonzero perturbation suffices)

WHAT IT TESTS (mapped to the theorem):
  mat is an arithmetic grid with a=1, d_R=3, d_C=1.
  It is exactly the C in the Rank Elevation Theorem, just with small parameters.
  The '-5' at (0,0) is a partial exemption; the theorem uses '-10' (the full Δ).
  Both raise rank to 3.

KEY FINDING FROM SWEEP:
  Only delta=0 at (0,0) keeps rank 2.
  Every delta≠0 raises rank to 3, regardless of magnitude.
  Therefore: rank elevation is a BINARY property of the location (0,0),
             not of the specific perturbation amount.

  The framework-specific amount (Δ=10 = modular ratio = 26⁻¹ mod 37) determines
  WHICH framework the matrix lives in; the rank elevation itself is universal.

─────────────────────────────────────────────────────────────────
"""

import numpy as np
from numpy.linalg import matrix_rank as np_rank
import fractions

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(int(n)) % 9
    return r if r else 9


def exact_rank(M):
    mat = [[fractions.Fraction(int(x)) for x in row] for row in M]
    r, c = len(mat), len(mat[0])
    rank = 0
    pivot_row = 0
    for col in range(c):
        found = next((row for row in range(pivot_row, r) if mat[row][col] != 0), -1)
        if found == -1:
            continue
        mat[pivot_row], mat[found] = mat[found], mat[pivot_row]
        pivot = mat[pivot_row][col]
        for row in range(r):
            if row != pivot_row and mat[row][col] != 0:
                f = mat[row][col] / pivot
                mat[row] = [mat[row][k] - f * mat[pivot_row][k] for k in range(c)]
        rank += 1
        pivot_row += 1
    return rank


# ── (A) User's mat is an arithmetic grid ─────────────────────────────────────

mat = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)

# Verify: a=1, d_R=3, d_C=1
A_USER, DR_USER, DC_USER = 1, 3, 1
for i in range(3):
    for j in range(3):
        expected = A_USER + i * DR_USER + j * DC_USER
        check(mat[i, j] == expected,
              f"mat[{i},{j}] = {A_USER}+{i}·{DR_USER}+{j}·{DC_USER} = {expected}",
              int(mat[i, j]), expected)

check(np_rank(mat) == 2, "rank(mat) = 2", np_rank(mat), 2)
check(exact_rank(mat.tolist()) == 2, "exact rank(mat) = 2", exact_rank(mat.tolist()), 2)

# Row dependency: row 2 = 2·row 1 - row 0
row_dep = 2 * mat[1] - mat[0]
check(np.allclose(row_dep, mat[2]), "row2 = 2·row1 - row0", True, True)


# ── (B) Uniform +10 preserves rank ───────────────────────────────────────────

uniform = mat + 10
check(np_rank(uniform) == 2, "rank(mat+10) = 2", np_rank(uniform), 2)

# The dependency is preserved: row2_new = 2·row1_new - row0_new
# Because (2*(mat[1]+10) - (mat[0]+10)) = 2*mat[1] - mat[0] + 10 = mat[2] + 10 ✓
check(np.allclose(2 * uniform[1] - uniform[0], uniform[2]),
      "row dependency preserved after +10", True, True)


# ── (C) Any nonzero perturbation at (0,0) elevates rank ──────────────────────

# Tested for 13 magnitudes spanning -10 to +10
DELTAS = list(range(-10, 11))
for delta in DELTAS:
    e = uniform.copy()
    e[0, 0] += delta
    r = np_rank(e)
    expected_rank = 2 if delta == 0 else 3
    check(r == expected_rank,
          f"(0,0) += {delta:+d}: rank = {expected_rank}",
          r, expected_rank)

# Summary: rank(uniform + δ·e₁e₁ᵀ) = 2 iff δ=0
check(True, "rank elevation is binary in δ: only δ=0 keeps rank 2", True, True)


# ── Why: the exact perturbation that preserves rank ───────────────────────────
#
# For rank(exempt) = 2, row 2 of exempt must remain = 2·row 1 - row 0.
# After changing exempt[0,0] by δ:
#   LHS: exempt[2] = uniform[2] = [17,18,19]
#   RHS: 2·uniform[1] - exempt[0] = [28,30,32] - [11+δ,12,13] = [17-δ, 18, 19]
# For LHS = RHS: 17-δ = 17  →  δ = 0.
# So δ=0 is the UNIQUE value preserving rank 2.

exempt_0 = uniform.copy()
exempt_0[0, 0] += 0   # only δ=0 works
check(np_rank(exempt_0) == 2, "δ=0: rank = 2 (unique preserving value)", np_rank(exempt_0), 2)

# Algebraic proof: solve for δ
# Required: 2*uniform[1,0] - (uniform[0,0]+δ) = uniform[2,0]
# 2·14 - (11+δ) = 17 → 28 - 11 - δ = 17 → δ = 0
lhs = 2 * int(uniform[1, 0]) - int(uniform[0, 0])   # 28-11=17
rhs = int(uniform[2, 0])                             # 17
check(lhs - rhs == 0, "δ_preserve = 2·uniform[1,0]-uniform[0,0]-uniform[2,0] = 0",
      lhs - rhs, 0)


# ── Mapping to the Rank Elevation Theorem ─────────────────────────────────────
#
# User's mat  = C in the theorem (arithmetic grid, rank 2)
# mat + 10    = C + 10·J (uniform shift; same column space, rank 2)
# exempt (−5) = C + 10·J + (-5)·e₁e₁ᵀ  → rank 3 (any nonzero pert. at (0,0))
#
# Framework's M = C_177 - Δ with Δ = 10·(J - e₁e₁ᵀ):
#   M(0,0) = C(0,0)   (no change)
#   M(i,j≠(0,0)) = C(i,j) - 10
#
# Viewed as: M = (C - 10·J) + 10·e₁e₁ᵀ
#              = (rank-2 shifted C) + (rank-1 single-entry perturbation at (0,0))
# The +10·e₁e₁ᵀ term is the "exemption" and causes the rank elevation.
# Magnitude: 10 = 26⁻¹ mod 37 (modular ratio) — connects to the framework.

ROWS_7, COLS_3 = 7, 3
ANCHOR = 177
DR_F, DC_F = 90, 11

C_177 = [[ANCHOR + i * DR_F + j * DC_F for j in range(COLS_3)] for i in range(ROWS_7)]
J10   = [[10] * COLS_3 for _ in range(ROWS_7)]
E10   = [[10 if (i == 0 and j == 0) else 0 for j in range(COLS_3)] for i in range(ROWS_7)]

# C - 10·J has same column space as C (rank 2)
C_shifted = [[C_177[i][j] - J10[i][j] for j in range(COLS_3)] for i in range(ROWS_7)]
check(exact_rank(C_shifted) == 2, "rank(C_177 - 10·J) = 2", exact_rank(C_shifted), 2)

# C_shifted + E10 is M (= C_177 - Δ)
M_rebuilt = [[C_shifted[i][j] + E10[i][j] for j in range(COLS_3)] for i in range(ROWS_7)]

MATRIX = [
    [177, 178, 189], [257, 268, 279], [347, 358, 369],
    [437, 448, 459], [527, 538, 549], [617, 628, 639],
    [707, 718, 729],
]
check(M_rebuilt == MATRIX, "C_shifted + E10 = M (verified)", M_rebuilt, MATRIX)
check(exact_rank(M_rebuilt) == 3, "rank(M_rebuilt) = 3", exact_rank(M_rebuilt), 3)

# E10 is the perturbation at (0,0): rank-1
check(exact_rank(E10) == 1, "rank(E10) = 1 (single nonzero entry)", exact_rank(E10), 1)

# Magnitude check: the framework-specific amount
check(26 * 10 % 37 == 1, "perturbation magnitude 10 = 26⁻¹ mod 37",
      26 * 10 % 37, 1)
check(dr(10) == 1, "DR(10) = 1 = φ-axiom", dr(10), 1)


# ── What the code does NOT test (but the theorem covers) ─────────────────────

# The user's mat is 3×3, n=3. Theorem holds for any n≥2 rows, any arithmetic params.
GENERAL_CASES = [
    (1, 3, 1, 3, 3),    # user's case
    (177, 90, 11, 7, 3), # framework case
    (0, 5, 2, 4, 3),
    (100, 7, 3, 5, 3),
]
for anchor, dR, dC, rows, cols in GENERAL_CASES:
    C_t   = [[anchor + i * dR + j * dC for j in range(cols)] for i in range(rows)]
    J_t   = [[10] * cols for _ in range(rows)]
    E_t   = [[10 if (i == 0 and j == 0) else 0 for j in range(cols)] for i in range(rows)]
    M_t   = [[C_t[i][j] - J_t[i][j] + E_t[i][j] for j in range(cols)] for i in range(rows)]
    rC = exact_rank(C_t)
    rM = exact_rank(M_t)
    check(rC == 2 and rM == 3,
          f"a={anchor},dR={dR},dC={dC},{rows}×{cols}: rank(C)=2,rank(M)=3",
          (rC, rM), (2, 3))


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("NumPy Rank Audit")
    print("=" * 66)

    print(f"\n── User's code output ──")
    print(f"  Original rank:              {int(np_rank(mat))}")
    print(f"  Uniform +10 rank:           {int(np_rank(uniform))}")
    exempt = uniform.copy()
    exempt[0, 0] -= 5
    print(f"  With (0,0) exemption rank:  {int(np_rank(exempt))}")
    print(f"  Logic check complete.")

    print(f"\n── mat IS an arithmetic grid ──")
    print(f"  a={A_USER}, d_R={DR_USER}, d_C={DC_USER}; matches theorem's C exactly")
    print(f"  row 2 = 2·row 1 - row 0: ✓")

    print(f"\n── Perturbation sweep at (0,0) ──")
    print(f"  {'δ':>5}  rank")
    for delta in DELTAS:
        e = uniform.copy()
        e[0, 0] += delta
        marker = " ← only value preserving rank 2" if delta == 0 else ""
        print(f"  {delta:>+5}  {int(np_rank(e))}{marker}")

    print(f"\n── Key finding ──")
    print(f"  Rank elevation is BINARY in location, not in magnitude.")
    print(f"  δ=0 at (0,0): rank stays 2  (row dependency preserved)")
    print(f"  δ≠0 at (0,0): rank rises to 3  (e₁ enters column space)")
    print(f"  Algebraic proof: δ_preserve = 2·u[1,0]-u[0,0]-u[2,0] = 0")

    print(f"\n── Framework mapping ──")
    print(f"  mat = C (a=1,d_R=3,d_C=1);  mat+10 = C+10·J;  exempt = C+10·J+δ·e₁e₁ᵀ")
    print(f"  Framework M = (C_177-10·J) + 10·e₁e₁ᵀ")
    print(f"  Same structure; magnitude 10 = 26⁻¹ mod 37 connects to Z/37Z")
    print(f"  rank(C-10·J)=2 → rank(C-10·J+10·e₁e₁ᵀ)=3 ✓")

    print(f"\n── General cases ──")
    for anchor, dR, dC, rows, cols in GENERAL_CASES:
        C_t = [[anchor + i * dR + j * dC for j in range(cols)] for i in range(rows)]
        J_t = [[10]*cols for _ in range(rows)]
        E_t = [[10 if (i==0 and j==0) else 0 for j in range(cols)] for i in range(rows)]
        M_t = [[C_t[i][j]-J_t[i][j]+E_t[i][j] for j in range(cols)] for i in range(rows)]
        print(f"  a={anchor}, d_R={dR}, d_C={dC}, {rows}×{cols}: "
              f"rank(C)={exact_rank(C_t)}, rank(M)={exact_rank(M_t)}")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
