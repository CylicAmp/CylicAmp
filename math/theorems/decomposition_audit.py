"""
decomposition_audit.py

Structural matrix decomposition: M = C - Δ

─────────────────────────────────────────────────────────────────
CLAIM:
  M = C - Δ
  C(i,j) = 177 + 90i + 11j          (0-indexed; anchor = 177 = MATRIX[0,0])
  Δ(i,j) = 0 if (i,j)=(0,0), else 10
  rank(C) = 2,  rank(Δ) = 2,  rank(M) = 3

VERIFIED: M = C - Δ holds at all 21 cells.
  At (0,0): C=177, Δ=0 → 177-0=177 ✓
  At (i,j)≠(0,0): C gives M(i,j)+10; Δ=10 restores M(i,j) ✓

─────────────────────────────────────────────────────────────────
TWO EQUIVALENT DECOMPOSITIONS:
  (D1) M = C_177 - Δ    C_177 anchor=177, rank(Δ)=2  [this audit]
  (D2) M = C_167 + E    C_167 anchor=167, rank(E)=1  [closed_form_audit]

  Relation: C_167 = C_177 - 10·J  (all entries shifted -10)
            E = 10·e₁e₁ᵀ          (single +10 at anchor)
            Δ = 10·J - E           (complement: 10 everywhere except anchor)

RANK OF Δ:
  Δ = 10·(J - e₁e₁ᵀ)
  Row 0 of (J - e₁e₁ᵀ): [0,1,1]
  Row k>0 of (J - e₁e₁ᵀ): [1,1,1]
  Rows 0 and 1 are linearly independent → rank(Δ) = 2.

─────────────────────────────────────────────────────────────────
"""

import fractions

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


# ── Data ──────────────────────────────────────────────────────────────────────

ROWS, COLS = 7, 3
D_R = 90
D_C = 11

MATRIX = [
    [177, 178, 189],
    [257, 268, 279],
    [347, 358, 369],
    [437, 448, 459],
    [527, 538, 549],
    [617, 628, 639],
    [707, 718, 729],
]


def matrix_rank(M):
    mat = [[fractions.Fraction(x) for x in row] for row in M]
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


# ── Build C (anchor = 177) and Δ ─────────────────────────────────────────────

ANCHOR = MATRIX[0][0]   # 177

C = [[ANCHOR + i * D_R + j * D_C for j in range(COLS)] for i in range(ROWS)]
DELTA = [[0 if (i == 0 and j == 0) else 10 for j in range(COLS)] for i in range(ROWS)]


# ── Verify M = C - Δ at all cells ────────────────────────────────────────────

for i in range(ROWS):
    for j in range(COLS):
        check(C[i][j] - DELTA[i][j] == MATRIX[i][j],
              f"M({i+1},{j+1}) = C({i+1},{j+1})-Δ({i+1},{j+1}) = {C[i][j]}-{DELTA[i][j]}",
              C[i][j] - DELTA[i][j], MATRIX[i][j])

# Spot-checks from the problem statement
check(C[0][0] - DELTA[0][0] == 177, "anchor (1,1): 177-0=177", C[0][0]-DELTA[0][0], 177)
check(C[0][1] - DELTA[0][1] == 178, "(1,2): 188-10=178", C[0][1]-DELTA[0][1], 178)
check(C[1][0] - DELTA[1][0] == 257, "(2,1): 267-10=257", C[1][0]-DELTA[1][0], 257)
check(C[6][2] - DELTA[6][2] == 729, "(7,3): 739-10=729", C[6][2]-DELTA[6][2], 729)


# ── Rank structure ────────────────────────────────────────────────────────────

rank_C     = matrix_rank(C)
rank_DELTA = matrix_rank(DELTA)
rank_M     = matrix_rank(MATRIX)

check(rank_C == 2, "rank(C) = 2", rank_C, 2)
check(rank_DELTA == 2, "rank(Δ) = 2", rank_DELTA, 2)
check(rank_M == 3, "rank(M) = rank(C-Δ) = 3", rank_M, 3)

# Δ = 10·(J - e₁e₁ᵀ); rank of each factor
J_matrix   = [[10] * COLS for _ in range(ROWS)]      # 10·J
e1e1       = [[10 if (i==0 and j==0) else 0 for j in range(COLS)] for i in range(ROWS)]

rank_J     = matrix_rank(J_matrix)
rank_e1e1  = matrix_rank(e1e1)
rank_J_minus_e1e1 = matrix_rank([[J_matrix[i][j] - e1e1[i][j]
                                   for j in range(COLS)] for i in range(ROWS)])

check(rank_J == 1, "rank(10·J) = 1", rank_J, 1)
check(rank_e1e1 == 1, "rank(10·e₁e₁ᵀ) = 1", rank_e1e1, 1)
check(rank_J_minus_e1e1 == 2, "rank(10·J - 10·e₁e₁ᵀ) = 2 = rank(Δ)", rank_J_minus_e1e1, 2)

# Verify Δ = 10·J - 10·e₁e₁ᵀ
for i in range(ROWS):
    for j in range(COLS):
        check(J_matrix[i][j] - e1e1[i][j] == DELTA[i][j],
              f"Δ({i+1},{j+1}) = 10·J - 10·e₁e₁ᵀ",
              J_matrix[i][j] - e1e1[i][j], DELTA[i][j])

# rank(M) ≤ rank(C) + rank(Δ) = 4, but column count caps at 3, so rank(M) ≤ 3
# rank(M) = 3 (full column rank): the rows of M span all of ℝ³
check(rank_M <= min(ROWS, COLS), "rank(M) ≤ min(7,3) = 3", rank_M <= 3, True)
check(rank_M == COLS, "rank(M) = 3 = column count (full column rank)", rank_M, COLS)


# ── Two decompositions: D1 and D2 ────────────────────────────────────────────

# D2: M = C_167 + E   (closed_form_audit decomposition)
A_167 = 167
C_167 = [[A_167 + i * D_R + j * D_C for j in range(COLS)] for i in range(ROWS)]
E     = [[MATRIX[i][j] - C_167[i][j] for j in range(COLS)] for i in range(ROWS)]

check(E[0][0] == 10, "E(1,1) = +10", E[0][0], 10)
check(all(E[i][j] == 0 for i in range(ROWS) for j in range(COLS) if not (i==0 and j==0)),
      "E = 0 everywhere except (1,1)", True, True)

rank_C_167 = matrix_rank(C_167)
rank_E     = matrix_rank(E)
check(rank_C_167 == 2, "rank(C_167) = 2", rank_C_167, 2)
check(rank_E == 1, "rank(E) = 1", rank_E, 1)

# Relation between D1 and D2:
# C_167 = C_177 - 10·J  (anchor shifts all entries by -10)
# E = 10·e₁e₁ᵀ
# Δ = 10·J - E
for i in range(ROWS):
    for j in range(COLS):
        check(C[i][j] - 10 == C_167[i][j],
              f"C_177({i+1},{j+1}) - 10 = C_167({i+1},{j+1})",
              C[i][j] - 10, C_167[i][j])
        check(J_matrix[i][j] - e1e1[i][j] == DELTA[i][j],
              f"Δ = 10·J - E at ({i+1},{j+1})",
              J_matrix[i][j] - e1e1[i][j], DELTA[i][j])


# ── Modular content ───────────────────────────────────────────────────────────

# The modular ratio 10 = 26⁻¹ mod 37 appears as:
#   - The uniform correction applied by Δ to all off-anchor cells
#   - The ε deviation at the anchor (E(1,1))
# Both corrections have the same magnitude because they're complementary:
# Δ shifts everything except the anchor; E shifts only the anchor.
# Together they account for the same total quantity: 10 per cell.

check(26 * 10 % 37 == 1, "10 = 26⁻¹ mod 37 (modular ratio = correction magnitude)",
      26 * 10 % 37, 1)
check(dr(10) == 1, "DR(10) = 1 = φ-axiom (UNIT)", dr(10), 1)

# Sum of all Δ entries = 10 × (ROWS×COLS - 1) = 10×20 = 200
delta_sum = sum(DELTA[i][j] for i in range(ROWS) for j in range(COLS))
check(delta_sum == 10 * (ROWS * COLS - 1), "sum(Δ) = 10×20 = 200", delta_sum, 200)
check(delta_sum == 200, "sum(Δ) = 200", delta_sum, 200)
check(dr(200) == 2, "DR(sum(Δ)) = DR(200) = 2 = e-axiom", dr(200), 2)

# Sum of all E entries = 10 (single nonzero)
e_sum = sum(E[i][j] for i in range(ROWS) for j in range(COLS))
check(e_sum == 10, "sum(E) = 10 (single nonzero)", e_sum, 10)
check(delta_sum + e_sum == 210, "sum(Δ)+sum(E) = 200+10 = 210 = 21×10", delta_sum + e_sum, 210)
check(210 == ROWS * COLS * 10, "21×10 = ROWS×COLS×10", 210, ROWS * COLS * 10)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Decomposition Audit: M = C - Δ")
    print("=" * 66)

    print(f"\n── Matrices (first 3 rows shown) ──")
    print(f"  {'':4}  {'C':>20}  {'Δ':>20}  {'C-Δ = M':>20}")
    for i in range(ROWS):
        c_row = C[i]
        d_row = DELTA[i]
        m_row = MATRIX[i]
        print(f"  i={i+1}  {str(c_row):>20}  {str(d_row):>20}  {str(m_row):>20}")

    print(f"\n── Decomposition M = C - Δ ──")
    print(f"  C(i,j) = {ANCHOR} + {D_R}·i + {D_C}·j   (anchor = MATRIX[1,1] = {ANCHOR})")
    print(f"  Δ(i,j) = 0 if (i,j)=(1,1), else 10")
    print(f"  C(1,1)-Δ(1,1) = {ANCHOR}-0 = {ANCHOR} = M(1,1) ✓")
    print(f"  C(i,j)-Δ(i,j) = [C(i,j)+10]-10 = M(i,j) for (i,j)≠(1,1) ✓")

    print(f"\n── Rank summary ──")
    print(f"  rank(C) = {rank_C}  (separable: u·𝟏ᵀ + 𝟏·vᵀ, anchor=177)")
    print(f"  rank(Δ) = {rank_DELTA}  (Δ = 10·J - 10·e₁e₁ᵀ; rows [0,1,1] and [1,1,1] lin. indep.)")
    print(f"  rank(M) = {rank_M}  = full column rank (cols of M span ℝ³)")
    print(f"  rank(M) ≤ rank(C)+rank(Δ) = {rank_C}+{rank_DELTA} = 4; column cap binds at 3")

    print(f"\n── Two equivalent decompositions ──")
    print(f"  (D1) M = C_177 - Δ   rank(C_177)={rank_C}, rank(Δ)={rank_DELTA}")
    print(f"  (D2) M = C_167 + E   rank(C_167)={rank_C_167}, rank(E)={rank_E}")
    print(f"  Δ = 10·J - E;   C_167 = C_177 - 10·J")
    print(f"  Same matrix M; D1 anchors at 177, D2 anchors at 167.")

    print(f"\n── Correction magnitude = 10 = modular ratio ──")
    print(f"  26×10 mod 37 = {26*10%37}  (10 = 26⁻¹ mod 37)")
    print(f"  DR(10) = {dr(10)} = φ-axiom = UNIT")
    print(f"  Δ applies -10 to {ROWS*COLS-1} cells; E applies +10 to 1 cell")
    print(f"  sum(Δ) = {delta_sum};  sum(E) = {e_sum};  total = {delta_sum+e_sum} = {ROWS*COLS}×10")
    print(f"  DR(sum(Δ)) = DR({delta_sum}) = {dr(delta_sum)} = e-axiom")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
