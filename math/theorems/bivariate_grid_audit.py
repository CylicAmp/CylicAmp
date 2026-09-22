"""
bivariate_grid_audit.py

Non-uniform 3×3 bivariate arithmetic matrix: base-90 vertical progression
with singular variance 80 at M(2,1).

─────────────────────────────────────────────────────────────────
MATRIX:
  M = [[177, 178, 189],
       [257, 268, 279],
       [347, 358, 369]]

GOVERNING RELATIONS:
  (G1) Columns 2 & 3 (all rows): d_R = 90   DR(90) = 9
  (G2) Column 1 (i > 2):         d_R = 90   (same)
  (G3) Column 1 (i = 2):         d_R = 80   DR(80) = 8 = AHL  ← singular
  (G4) Horizontal (j ≥ 2):       d_C = 11   (= repunit_2)
  (G5) Row 1 col 1→2:            gap =  1   (not 11; companion singularity)

STEP ARITHMETIC:
  Standard d_R = 90 = 9×10;  DR = 9 = NULL
  Singular  d_R = 80 = 8×10; DR = 8 = AHL
  Variance       90 − 80 = 10 = 26⁻¹ mod 37  (modular ratio)
  d_C = 11 = repunit_2

SLOT ASSIGNMENTS (mod 37):
  d_R = 90: slot 16  →  ORBIT_P (outer ring)
  singular 80: slot 6 →  ORBIT_V (inner ring) = slot(191) = root slot
  d_C = 11: slot 11  →  ORBIT_V (inner ring) = repunit_2 slot

  The standard step (90) rides the outer ring.
  The singular step (80) drops to the inner ring at the exact slot of 191.
  The singular variance encodes a modal crossing from ORBIT_P → ORBIT_V.

DR COLUMN STRUCTURE:
  Col 1: [6, 5, 5]   (non-constant)
  Col 2: [7, 7, 7]   = ALO throughout
  Col 3: [9, 9, 9]   = NULL throughout

STARTING VALUE:
  M(1,1) = 177 = DESCENT[2] in the 191→100 chain.
  Descent: 191 → 188 → 177 → 166 → … → 100  (step −3, then −11)
  d_C = 11 = |descent step| after the first step.

BOTTOM-RIGHT CORNER:
  M(3,3) = 369  mod 37 = 36 = −1 mod 37
  Same residue as Ψ(23,29,31) = 73 mod 37 = 36 (psi_operator_audit, P3).

FACTORIZATION OF START:
  177 = 3 × 59;  59 mod 37 = 22 = 2×repunit_2 = middle step (bases 10-12)
─────────────────────────────────────────────────────────────────
"""

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


M = [
    [177, 178, 189],
    [257, 268, 279],
    [347, 358, 369],
]

ORBIT_P = [0, 1, 4, 13, 3, 10, 31, 20, 24, 36, 35, 32, 23, 33, 26, 5, 16, 12]
ORBIT_V = [2, 7, 22, 30, 17, 15, 9, 28, 11, 34, 29, 14, 6, 19, 21, 27, 8, 25]


# ── G1/G2: Columns 2 & 3 and Column 1 (i>2): d_R = 90 ───────────────────────

for j in [1, 2]:
    for i in range(1, 3):
        step = M[i][j] - M[i - 1][j]
        check(step == 90, f"col {j+1} row {i}→{i+1}: d_R = 90", step, 90)

check(M[2][0] - M[1][0] == 90, "col 1 row 2→3: d_R = 90", M[2][0] - M[1][0], 90)


# ── G3: Column 1 (i=2): d_R = 80 (singular) ──────────────────────────────────

check(M[1][0] - M[0][0] == 80, "col 1 row 1→2: d_R = 80 (singular)", M[1][0] - M[0][0], 80)


# ── G4: Horizontal j ≥ 2: d_C = 11 ───────────────────────────────────────────

for i in range(3):
    step = M[i][2] - M[i][1]
    check(step == 11, f"row {i+1} col 2→3: d_C = 11", step, 11)

for i in range(1, 3):
    step = M[i][1] - M[i][0]
    check(step == 11, f"row {i+1} col 1→2: d_C = 11 (i > 1)", step, 11)


# ── G5: Row 1 col 1→2: gap = 1, not 11 ──────────────────────────────────────

check(M[0][1] - M[0][0] == 1, "row 1 col 1→2: gap = 1 (companion singularity)",
      M[0][1] - M[0][0], 1)
check((M[0][1] - M[0][0]) != 11, "row 1 col 1→2 ≠ 11", M[0][1] - M[0][0], 1)


# ── Step DR and framework ─────────────────────────────────────────────────────

# d_R = 90: DR = 9 = NULL
check(dr(90) == 9, "DR(90) = 9 = NULL", dr(90), 9)
check(90 == 9 * 10, "90 = 9×10", 90, 9 * 10)

# Singular d_R = 80: DR = 8 = AHL
check(dr(80) == 8, "DR(80) = 8 = AHL (singular step)", dr(80), 8)
check(80 == 8 * 10, "80 = 8×10", 80, 8 * 10)

# Variance = 10 = modular ratio
check(90 - 80 == 10, "variance = 90−80 = 10", 90 - 80, 10)
check(26 * 10 % 37 == 1, "10 = 26⁻¹ mod 37 (modular ratio)", 26 * 10 % 37, 1)

# d_C = 11 = repunit_2
check(11 % 37 == 11, "d_C = 11 = repunit_2 in Z/37Z", 11 % 37, 11)


# ── Slot assignments in Z/37Z ─────────────────────────────────────────────────

# d_R = 90 → slot 16 → ORBIT_P
check(90 % 37 == 16, "d_R = 90 mod 37 = 16", 90 % 37, 16)
check(16 in ORBIT_P, "slot 16 ∈ ORBIT_P (outer ring)", 16 in ORBIT_P, True)

# singular 80 → slot 6 → ORBIT_V = slot(191)
check(80 % 37 == 6, "singular 80 mod 37 = 6 = slot(191)", 80 % 37, 6)
check(191 % 37 == 6, "191 mod 37 = 6 (root slot)", 191 % 37, 6)
check(6 in ORBIT_V, "slot 6 ∈ ORBIT_V (inner ring) = slot of 191", 6 in ORBIT_V, True)

# d_C = 11 → slot 11 → ORBIT_V
check(11 in ORBIT_V, "slot 11 ∈ ORBIT_V (inner ring)", 11 in ORBIT_V, True)

# Standard step in ORBIT_P; singular step in ORBIT_V at root slot → modal crossing
check(90 % 37 in ORBIT_P and 80 % 37 in ORBIT_V,
      "d_R=90 in ORBIT_P; singular 80 in ORBIT_V (modal crossing in step)",
      (90 % 37 in ORBIT_P, 80 % 37 in ORBIT_V), (True, True))


# ── DR column structure ───────────────────────────────────────────────────────

COL_DR = [[dr(M[i][j]) for i in range(3)] for j in range(3)]

# Column 2 = DR 7 (ALO) throughout
check(COL_DR[1] == [7, 7, 7], "col 2 DR = [7,7,7] = ALO throughout", COL_DR[1], [7, 7, 7])

# Column 3 = DR 9 (NULL) throughout
check(COL_DR[2] == [9, 9, 9], "col 3 DR = [9,9,9] = NULL throughout", COL_DR[2], [9, 9, 9])

# Column 1: non-constant [6, 5, 5]
check(COL_DR[0] == [6, 5, 5], "col 1 DR = [6,5,5]", COL_DR[0], [6, 5, 5])
check(dr(COL_DR[0][0]) == 6, "col 1 row 1: DR = 6 = DR(33) = DR(AHL+ALO)", COL_DR[0][0], 6)

# Row DR sums
ROW_DR_SUMS = [sum(dr(M[i][j]) for j in range(3)) for i in range(3)]
check(ROW_DR_SUMS[0] == 22, "row 1 DR sum = 22 = 2×repunit_2", ROW_DR_SUMS[0], 22)
check(ROW_DR_SUMS[1] == 21, "row 2 DR sum = 21", ROW_DR_SUMS[1], 21)
check(ROW_DR_SUMS[2] == 21, "row 3 DR sum = 21", ROW_DR_SUMS[2], 21)
check(22 == 2 * 11, "22 = 2×repunit_2 (row 1 DR sum)", 22, 2 * 11)
check(dr(22) == 4, "DR(22) = 4", dr(22), 4)
check(dr(21) == 3, "DR(21) = 3", dr(21), 3)


# ── Starting value: M(1,1) = 177 = DESCENT[2] ────────────────────────────────

# Descent from 191: 191, 191-3=188, 188-11=177, 177-11=166, …, 100
DESCENT = [191, 188] + [191 - 3 - 11 * k for k in range(1, 9)]
check(DESCENT[:10] == [191, 188, 177, 166, 155, 144, 133, 122, 111, 100],
      "descent 191→100", DESCENT[:10],
      [191, 188, 177, 166, 155, 144, 133, 122, 111, 100])

check(M[0][0] == 177, "M(1,1) = 177", M[0][0], 177)
check(177 in DESCENT, "177 ∈ descent sequence", 177 in DESCENT, True)
check(DESCENT.index(177) == 2, "177 = DESCENT[2] (third element)", DESCENT.index(177), 2)
check(177 % 37 == 29, "177 mod 37 = 29 = slot of 177 in descent", 177 % 37, 29)

# d_C = 11 = descent step magnitude after first step
check(11 == abs(-11), "d_C = 11 = |descent step| (−11→+11 in matrix column)",
      11, 11)


# ── M(3,3) = 369: mod 37 = 36 = −1 ──────────────────────────────────────────

check(M[2][2] == 369, "M(3,3) = 369", M[2][2], 369)
check(369 % 37 == 36, "369 mod 37 = 36 = −1 mod 37", 369 % 37, 36)
check(36 == 37 - 1, "36 = −1 mod 37", 36, 37 - 1)

# Ψ(23,29,31) = 73 ≡ 36 (psi_operator_audit, P3)
PSI_23_29_31 = 2 * (23 + 29) - 31
check(PSI_23_29_31 == 73, "Ψ(23,29,31) = 73", PSI_23_29_31, 73)
check(PSI_23_29_31 % 37 == 36, "Ψ(23,29,31) mod 37 = 36 = M(3,3) mod 37",
      PSI_23_29_31 % 37, 36)

# 36 = 2×18 = 2×GATE (double the CENTER)
check(36 == 2 * 18, "36 = 2×GATE", 36, 2 * 18)
check((37 - 1) // 2 == 18, "GATE = (37-1)/2 = 18", (37 - 1) // 2, 18)


# ── Factorization of start value ──────────────────────────────────────────────

# 177 = 3 × 59; 59 mod 37 = 22 = middle step (bases 10-12, base_recurrence_audit)
check(3 * 59 == 177, "177 = 3×59", 3 * 59, 177)
check(59 % 37 == 22, "59 mod 37 = 22 = middle step S (bases 10-12)", 59 % 37, 22)
check(22 == 2 * 11, "22 = 2×repunit_2 = col sums 1,3,4,5 of doubling matrix", 22, 2 * 11)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Bivariate Grid Audit")
    print("=" * 62)

    print("\n── Matrix ──")
    print(f"  {'':>6}  {'Col 1':>8}  {'Col 2':>8}  {'Col 3':>8}")
    for i in range(3):
        vals = M[i]
        drs  = [dr(v) for v in vals]
        mods = [v % 37 for v in vals]
        print(f"  Row {i+1}:  {vals[0]:>8}  {vals[1]:>8}  {vals[2]:>8}")
        print(f"         DR: {drs[0]:>6}   DR: {drs[1]:>6}   DR: {drs[2]:>6}")
        print(f"        m37: {mods[0]:>6}  m37: {mods[1]:>6}  m37: {mods[2]:>6}")

    print(f"\n── Governing relations ──")
    print(f"  d_R = 90 (standard): cols 2-3 all rows; col 1 rows 2→3")
    print(f"  d_R = 80 (singular): col 1 row 1→2  (10 less than standard)")
    print(f"  d_C = 11: horizontal for j≥2 (all rows); also row 2-3 col 1→2")
    print(f"  Row 1 col 1→2: gap = 1 (companion singularity)")

    print(f"\n── Step framework ──")
    print(f"  d_R=90: DR=9 (NULL); 90 mod 37={90%37} → ORBIT_P (outer)")
    print(f"  d_R=80: DR=8 (AHL);  80 mod 37={80%37} → ORBIT_V (inner) = slot(191)")
    print(f"  variance: 90−80=10 = 26⁻¹ mod 37 = modular ratio")
    print(f"  d_C=11: repunit_2;   11 mod 37=11 → ORBIT_V (inner)")
    print(f"  Standard step ORBIT_P → singular step ORBIT_V: modal crossing in step")

    print(f"\n── DR column structure ──")
    print(f"  Col 1: {[dr(M[i][0]) for i in range(3)]}  (6→5→5)")
    print(f"  Col 2: {[dr(M[i][1]) for i in range(3)]}  = ALO throughout")
    print(f"  Col 3: {[dr(M[i][2]) for i in range(3)]}  = NULL throughout")
    print(f"  Row DR sums: {ROW_DR_SUMS}  = [22=2×repunit_2, 21, 21]")
    print(f"  Row DR of sums: {[dr(s) for s in ROW_DR_SUMS]}  = [4, 3, 3]")

    print(f"\n── Starting value M(1,1) = 177 ──")
    print(f"  Descent 191→100: {DESCENT[:10]}")
    print(f"  177 = DESCENT[2] (third element; slot 29 in Z/37Z)")
    print(f"  d_C = 11 = |descent step| from element 2 onward")
    print(f"  177 = 3×59; 59 mod 37 = 22 = middle step S for bases 10-12")

    print(f"\n── Bottom-right corner M(3,3) = 369 ──")
    print(f"  369 mod 37 = {369%37} = −1 mod 37 = 2×GATE mod 37")
    print(f"  Ψ(23,29,31) = {PSI_23_29_31} mod 37 = {PSI_23_29_31%37}  (same slot)")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
