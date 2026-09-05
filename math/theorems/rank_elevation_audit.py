"""
rank_elevation_audit.py

Dimensionality and Rank Elevation Theorem

─────────────────────────────────────────────────────────────────
THEOREM:
  Let C be a uniform rank-2 arithmetic grid (n×3, n≥2) with
  C(i,j) = a + i·d_R + j·d_C  (d_R≠0, d_C≠0, 0-indexed).

  Let Δ be the correction matrix:
    Δ(i,j) = 0   if (i,j) = (0,0)
    Δ(i,j) = 10  otherwise.

  Let M = C - Δ. Then:

    rank(M) = rank(C) + 1 = 3.

PROOF SKETCH:
  (P1) col(C) = span{c₀, 𝟏}  where c₀ = column 0 of C (arithmetic seq.)
       and 𝟏 = [1,1,...,1]ᵀ.  dim(col(C)) = 2  (c₀ ∦ 𝟏 since d_R≠0).

  (P2) Column 0 of M:  m₀ = c₀ − 10·(𝟏 − e₁) = c₀ − 10·𝟏 + 10·e₁
       Columns 1,2 of M: mⱼ = (c₀ + j·d_C·𝟏) − 10·𝟏 = c₀ + (j·d_C−10)·𝟏
       So col(M) ⊆ span{c₀, 𝟏, e₁}.

  (P3) e₁ ∉ col(C):
       Any vector in col(C) has entries forming an arithmetic sequence:
         v = α·c₀ + β·𝟏  →  v_i = α(a + i·d_R) + β = (α·a+β) + i·(α·d_R).
       e₁ = [1,0,...,0]ᵀ has v₀=1, v₁=0: if arithmetic, d = v₁−v₀ = −1
       and v_i = 1−i for all i. But v₂=−1≠0 for n≥3.  Contradiction.
       Therefore e₁ ∉ col(C).

  (P4) m₀ = (c₀ − 10·𝟏) + 10·e₁ ∈ col(C) + span{e₁} but m₀ ∉ col(C)
       (because e₁ component is nonzero and e₁ ∉ col(C)).
       m₁, m₂ ∈ col(C)  (they are c₀ + const·𝟏).

  (P5) col(M) = col(C) + span{e₁} = span{c₀, 𝟏, e₁}.
       This has dimension 3 (three linearly independent vectors).
       Therefore rank(M) = 3 = rank(C) + 1.

COROLLARY:
  The rank elevation is caused solely by the anchor exemption.
  Without it (Δ≡10 everywhere), M = C − 10·J has the same column
  space as C (shifting by a constant doesn't change the span).
  With it (Δ(0,0)=0), the e₁ component enters and rank rises by 1.

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


def in_column_space(v, basis_cols):
    """Check if vector v is in the column space of the matrix formed by basis_cols."""
    n = len(v)
    m = len(basis_cols)
    # Augmented system: [basis_cols | v]
    aug = [[fractions.Fraction(basis_cols[j][i]) for j in range(m)] + [fractions.Fraction(v[i])]
           for i in range(n)]
    # Gaussian elimination
    rank_basis = 0
    pivot_row = 0
    for col in range(m + 1):
        found = next((row for row in range(pivot_row, n) if aug[row][col] != 0), -1)
        if found == -1:
            continue
        aug[pivot_row], aug[found] = aug[found], aug[pivot_row]
        pivot = aug[pivot_row][col]
        for row in range(n):
            if row != pivot_row and aug[row][col] != 0:
                f = aug[row][col] / pivot
                aug[row] = [aug[row][k] - f * aug[pivot_row][k] for k in range(m + 1)]
        if col < m:
            rank_basis += 1
        pivot_row += 1
    # Consistent iff rank of augmented = rank of basis part
    rank_aug = matrix_rank([[aug[i][j] for j in range(m + 1)] for i in range(n)])
    rank_bas = matrix_rank([[aug[i][j] for j in range(m)] for i in range(n)])
    return rank_aug == rank_bas


# ── Concrete 7×3 matrix ───────────────────────────────────────────────────────

ROWS, COLS = 7, 3
ANCHOR = 177
D_R, D_C = 90, 11

MATRIX = [
    [177, 178, 189],
    [257, 268, 279],
    [347, 358, 369],
    [437, 448, 459],
    [527, 538, 549],
    [617, 628, 639],
    [707, 718, 729],
]

C     = [[ANCHOR + i * D_R + j * D_C for j in range(COLS)] for i in range(ROWS)]
DELTA = [[0 if (i == 0 and j == 0) else 10 for j in range(COLS)] for i in range(ROWS)]


# ── P1: col(C) = span{c₀, 𝟏}, dim = 2 ───────────────────────────────────────

rank_C = matrix_rank(C)
check(rank_C == 2, "rank(C) = 2", rank_C, 2)

c0   = [C[i][0] for i in range(ROWS)]    # first column of C: arithmetic seq.
ones = [1] * ROWS

# c₀ is an arithmetic sequence with step d_R = 90
for i in range(1, ROWS):
    check(c0[i] - c0[i - 1] == D_R, f"c₀[{i}]-c₀[{i-1}] = d_R = {D_R}", c0[i]-c0[i-1], D_R)

# Every column of C is in span{c₀, 𝟏}
for j in range(COLS):
    col_j = [C[i][j] for i in range(ROWS)]
    in_span = in_column_space(col_j, [c0, ones])
    check(in_span, f"C col {j+1} ∈ span{{c₀,𝟏}}", in_span, True)


# ── P2: Column structure of M ─────────────────────────────────────────────────

e1 = [1 if i == 0 else 0 for i in range(ROWS)]   # standard basis vector

m0 = [MATRIX[i][0] for i in range(ROWS)]   # col 1 of M
m1 = [MATRIX[i][1] for i in range(ROWS)]   # col 2 of M
m2 = [MATRIX[i][2] for i in range(ROWS)]   # col 3 of M

# m₀ = c₀ - 10·𝟏 + 10·e₁  (verified elementwise)
for i in range(ROWS):
    expected = c0[i] - 10 * ones[i] + 10 * e1[i]
    check(m0[i] == expected, f"m₀[{i}] = c₀-10·𝟏+10·e₁", m0[i], expected)

# m₁ = c₀ + (d_C - 10)·𝟏 = c₀ + 1·𝟏  (d_C=11, 11-10=1)
coeff_1 = D_C - 10   # 11-10 = 1
for i in range(ROWS):
    expected = c0[i] + coeff_1 * ones[i]
    check(m1[i] == expected, f"m₁[{i}] = c₀ + {coeff_1}·𝟏", m1[i], expected)

# m₂ = c₀ + (2·d_C - 10)·𝟏 = c₀ + 12·𝟏
coeff_2 = 2 * D_C - 10   # 22-10 = 12
for i in range(ROWS):
    expected = c0[i] + coeff_2 * ones[i]
    check(m2[i] == expected, f"m₂[{i}] = c₀ + {coeff_2}·𝟏", m2[i], expected)

# m₁, m₂ ∈ col(C)  (they are c₀ + const·𝟏)
check(in_column_space(m1, [c0, ones]), "m₁ ∈ col(C) = span{c₀,𝟏}", True, True)
check(in_column_space(m2, [c0, ones]), "m₂ ∈ col(C) = span{c₀,𝟏}", True, True)


# ── P3: e₁ ∉ col(C) ──────────────────────────────────────────────────────────

e1_in_colC = in_column_space(e1, [c0, ones])
check(not e1_in_colC, "e₁ ∉ col(C)  (not an arithmetic sequence)", e1_in_colC, False)

# Explicit: if e₁ = α·c₀ + β·𝟏, then:
#   i=0: α·177 + β = 1
#   i=1: α·267 + β = 0
# Subtracting: α·90 = -1 → α = -1/90
# Then β = 1 - 177·α = 1 + 177/90 = 267/90
# Check at i=2: α·357 + β = -357/90 + 267/90 = -90/90 = -1 ≠ 0 = e₁[2]
alpha_e1 = fractions.Fraction(-1, D_R)
beta_e1  = 1 - fractions.Fraction(ANCHOR) * alpha_e1
val_at_2 = alpha_e1 * fractions.Fraction(c0[2]) + beta_e1
check(val_at_2 != 0, "if e₁ = α·c₀+β·𝟏, check at i=2 fails (≠0)", val_at_2, fractions.Fraction(-1))
check(val_at_2 == fractions.Fraction(-1), "e₁[2]=0 but α·c₀[2]+β = -1 ≠ 0", val_at_2, fractions.Fraction(-1))


# ── P4: m₀ ∉ col(C), m₀ ∈ col(C) + span{e₁} ────────────────────────────────

m0_in_colC = in_column_space(m0, [c0, ones])
check(not m0_in_colC, "m₀ ∉ col(C)  (has e₁ component)", m0_in_colC, False)

m0_in_extended = in_column_space(m0, [c0, ones, e1])
check(m0_in_extended, "m₀ ∈ span{c₀, 𝟏, e₁}", m0_in_extended, True)

# m₀ - (c₀ - 10·𝟏) = 10·e₁: e₁ component is exactly 10
residual = [m0[i] - (c0[i] - 10) for i in range(ROWS)]
check(residual == [10 * e1[i] for i in range(ROWS)],
      "m₀ - (c₀-10·𝟏) = 10·e₁", residual, [10 * v for v in e1])


# ── P5: rank(M) = rank(C) + 1 = 3 ───────────────────────────────────────────

rank_M = matrix_rank(MATRIX)
check(rank_M == rank_C + 1, "rank(M) = rank(C)+1", rank_M, rank_C + 1)
check(rank_M == 3, "rank(M) = 3", rank_M, 3)

# col(M) = span{c₀, 𝟏, e₁} (dimension 3)
rank_extended_basis = matrix_rank([[c0[i], ones[i], e1[i]] for i in range(ROWS)])
check(rank_extended_basis == 3, "rank[c₀|𝟏|e₁] = 3", rank_extended_basis, 3)

# Every column of M ∈ span{c₀, 𝟏, e₁}
for j, col in enumerate([m0, m1, m2]):
    check(in_column_space(col, [c0, ones, e1]),
          f"col {j+1} of M ∈ span{{c₀,𝟏,e₁}}", True, True)


# ── Corollary: without anchor exemption, rank stays 2 ────────────────────────

# M_uniform = C - 10·J  (Δ uniform, no exemption)
J10 = [[10] * COLS for _ in range(ROWS)]
M_uniform = [[C[i][j] - 10 for j in range(COLS)] for i in range(ROWS)]

rank_M_uniform = matrix_rank(M_uniform)
check(rank_M_uniform == 2, "rank(C - 10·J) = 2 (no exemption → rank unchanged)", rank_M_uniform, 2)

# All columns of M_uniform ∈ col(C) — shifting by constant preserves span
for j in range(COLS):
    col_j_unif = [M_uniform[i][j] for i in range(ROWS)]
    check(in_column_space(col_j_unif, [c0, ones]),
          f"(C-10J) col {j+1} ∈ col(C)", True, True)


# ── Generality: theorem holds for any arithmetic parameters ──────────────────

TEST_PARAMS = [
    (100, 45, 7, 5, 3),    # (anchor, d_R, d_C, rows, cols)
    (1,   90, 11, 7, 3),
    (167, 90, 11, 7, 3),
    (0,   1,  1,  4, 3),
]

for anchor, dR, dC, nrows, ncols in TEST_PARAMS:
    C_t = [[anchor + i * dR + j * dC for j in range(ncols)] for i in range(nrows)]
    D_t = [[0 if (i == 0 and j == 0) else 10 for j in range(ncols)] for i in range(nrows)]
    M_t = [[C_t[i][j] - D_t[i][j] for j in range(ncols)] for i in range(nrows)]

    rC = matrix_rank(C_t)
    rM = matrix_rank(M_t)
    check(rC == 2 and rM == 3,
          f"anchor={anchor},d_R={dR},d_C={dC}: rank(C)=2,rank(M)=3",
          (rC, rM), (2, 3))


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Rank Elevation Theorem Audit")
    print("=" * 66)

    print(f"\n── Theorem ──")
    print(f"  M = C - Δ  where rank(C)=2 and Δ exempts anchor (0,0) from -10")
    print(f"  ⟹  rank(M) = rank(C) + 1 = 3")

    print(f"\n── P1: col(C) = span{{c₀, 𝟏}}, dim=2 ──")
    print(f"  rank(C) = {rank_C}")
    print(f"  c₀ = {c0}  (arithmetic, step {D_R})")
    print(f"  Every column of C ∈ span{{c₀,𝟏}}: ✓")

    print(f"\n── P2: column structure of M ──")
    print(f"  m₀ = c₀ - 10·𝟏 + 10·e₁   (e₁ component appears via anchor exemption)")
    print(f"  m₁ = c₀ + {coeff_1}·𝟏   (d_C-10 = 11-10 = 1)")
    print(f"  m₂ = c₀ + {coeff_2}·𝟏   (2·d_C-10 = 22-10 = 12)")
    print(f"  m₁, m₂ ∈ col(C): ✓;   m₀ ∉ col(C): ✓")

    print(f"\n── P3: e₁ ∉ col(C) ──")
    print(f"  If e₁ = α·c₀+β·𝟏: α={alpha_e1}, β={beta_e1}")
    print(f"  Check at i=2: {alpha_e1}·{c0[2]}+{beta_e1} = {val_at_2} ≠ 0 = e₁[2]")
    print(f"  e₁ ∉ col(C): ✓")

    print(f"\n── P4: m₀ carries the new basis vector ──")
    print(f"  m₀ ∉ col(C): ✓")
    print(f"  m₀ - (c₀-10·𝟏) = {residual}  = 10·e₁")
    print(f"  m₀ ∈ span{{c₀,𝟏,e₁}}: ✓")

    print(f"\n── P5: rank(M) = {rank_M} = rank(C)+1 ──")
    print(f"  col(M) = span{{c₀, 𝟏, e₁}}  (3 linearly independent vectors)")
    print(f"  rank[c₀|𝟏|e₁] = {rank_extended_basis}")

    print(f"\n── Corollary: anchor exemption is necessary ──")
    print(f"  rank(C - 10·J) = {rank_M_uniform}  (uniform -10 preserves span)")
    print(f"  The rank elevation requires exactly the single-cell exemption at (0,0).")
    print(f"  Without it: rank stays {rank_M_uniform}.")
    print(f"  With it: rank rises to {rank_M}.")

    print(f"\n── Generality: verified for 4 parameter sets ──")
    for anchor, dR, dC, nrows, ncols in TEST_PARAMS:
        C_t = [[anchor + i * dR + j * dC for j in range(ncols)] for i in range(nrows)]
        D_t = [[0 if (i == 0 and j == 0) else 10 for j in range(ncols)] for i in range(nrows)]
        M_t = [[C_t[i][j] - D_t[i][j] for j in range(ncols)] for i in range(nrows)]
        print(f"  anchor={anchor}, d_R={dR}, d_C={dC}, {nrows}×{ncols}: "
              f"rank(C)={matrix_rank(C_t)}, rank(M)={matrix_rank(M_t)}")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
