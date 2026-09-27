"""
cascade_dr_audit.py

DR cascade structure of the non-uniform 3×3 matrix.

─────────────────────────────────────────────────────────────────
CORRECTED DR TABLE (user's labels corrected):

  i    M(i,1)  DR   M(i,2)  DR   M(i,3)  DR
  1     177     6    178     7    189     9
  2     257     5    268     7    279     9
  3     347     5    358     7    369     9

Column DR patterns:
  Col 1: [6, 5, 5]   anchor has DR=6; rows 2-3 have DR=5
  Col 2: [7, 7, 7]   ALO throughout  (not 5 as stated)
  Col 3: [9, 9, 9]   NULL throughout ✓

User's labeling corrections:
  177 → DR=6  (stated as 3=TRIAD; correct label is cascade-product or AHL+ALO)
  178 → DR=7  (stated as 5=MEDIATOR; correct label is ALO)
  268 → DR=7  (stated as 5=MEDIATOR; correct label is ALO)
  358 → DR=7  (stated as 5=MEDIATOR; correct label is ALO)

─────────────────────────────────────────────────────────────────
ACTUAL CASCADE STRUCTURE:

  Row 1:    6 → 7 → 9    (anchor-DR → ALO → NULL)
  Row 2:    5 → 7 → 9    (prime-admissible → ALO → NULL)
  Row 3:    5 → 7 → 9    (prime-admissible → ALO → NULL)

  Every row terminates at DR=9=NULL. ✓
  Col 3 is the NULL column; col 2 is the ALO column.

TERMINAL CELL:
  369: digits 3,6,9; sum = 18 = GATE = (37-1)/2; DR(18) = 9 = NULL ✓

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


# ── Matrix and DR values ──────────────────────────────────────────────────────

MATRIX = [
    [177, 178, 189],
    [257, 268, 279],
    [347, 358, 369],
]

DR_TABLE = [[dr(MATRIX[i][j]) for j in range(3)] for i in range(3)]

EXPECTED_DR = [
    [6, 7, 9],
    [5, 7, 9],
    [5, 7, 9],
]

for i in range(3):
    for j in range(3):
        check(DR_TABLE[i][j] == EXPECTED_DR[i][j],
              f"DR(M({i+1},{j+1})) = DR({MATRIX[i][j]})",
              DR_TABLE[i][j], EXPECTED_DR[i][j])


# ── Column patterns ───────────────────────────────────────────────────────────

COL_DR = [[DR_TABLE[i][j] for i in range(3)] for j in range(3)]

check(COL_DR[0] == [6, 5, 5], "col 1 DR = [6,5,5]", COL_DR[0], [6, 5, 5])
check(COL_DR[1] == [7, 7, 7], "col 2 DR = [7,7,7] = ALO throughout", COL_DR[1], [7, 7, 7])
check(COL_DR[2] == [9, 9, 9], "col 3 DR = [9,9,9] = NULL throughout", COL_DR[2], [9, 9, 9])

# DR=7 is ALO, not MEDIATOR (DR=5)
AHL, ALO = 8, 7
check(COL_DR[1][0] == ALO, "col 2 rows have DR=ALO=7 (not 5)", COL_DR[1][0], ALO)

# DR=6 at anchor (177), not TRIAD (DR=3)
check(DR_TABLE[0][0] == 6, "DR(177) = 6 (not 3=TRIAD)", DR_TABLE[0][0], 6)
check(6 == dr(AHL + ALO), "6 = DR(AHL+ALO) = DR(8+7) = DR(15)", dr(AHL + ALO), 6)
check(6 == 1 * 2 * 3, "6 = cascade product (1×2×3)", 1 * 2 * 3, 6)

# DR=5 in col 1 (rows 2-3): prime-admissible residue
PRIME_RESIDUES_MOD9 = {1, 2, 4, 5, 7, 8}
check(5 in PRIME_RESIDUES_MOD9, "DR=5 is prime-admissible mod 9", 5 in PRIME_RESIDUES_MOD9, True)
check(7 in PRIME_RESIDUES_MOD9, "DR=7 (ALO) is prime-admissible mod 9", 7 in PRIME_RESIDUES_MOD9, True)
check(9 not in PRIME_RESIDUES_MOD9, "DR=9 (NULL) is NOT prime-admissible", 9 not in PRIME_RESIDUES_MOD9, True)


# ── Row cascade: every row terminates at NULL ─────────────────────────────────

for i in range(3):
    check(DR_TABLE[i][2] == 9,
          f"row {i+1} terminates at DR=9=NULL", DR_TABLE[i][2], 9)

# Row 1 cascade: 6 → 7 → 9
check(DR_TABLE[0] == [6, 7, 9], "row 1 cascade: 6→7→9 (anchor-DR→ALO→NULL)",
      DR_TABLE[0], [6, 7, 9])

# Rows 2-3 cascade: 5 → 7 → 9
check(DR_TABLE[1] == [5, 7, 9], "row 2 cascade: 5→7→9 (prime-residue→ALO→NULL)",
      DR_TABLE[1], [5, 7, 9])
check(DR_TABLE[2] == [5, 7, 9], "row 3 cascade: 5→7→9 (prime-residue→ALO→NULL)",
      DR_TABLE[2], [5, 7, 9])

# DR increases along each row: col1 < col2 < col3 (for rows 2-3)
# Row 1: 6 < 7 < 9; Rows 2-3: 5 < 7 < 9
for i in range(3):
    check(DR_TABLE[i][0] < DR_TABLE[i][1] < DR_TABLE[i][2],
          f"row {i+1}: DR strictly increases left→right",
          (DR_TABLE[i][0], DR_TABLE[i][1], DR_TABLE[i][2]),
          (DR_TABLE[i][0], DR_TABLE[i][1], DR_TABLE[i][2]))


# ── Terminal cell: 369 ────────────────────────────────────────────────────────

TERMINAL = MATRIX[2][2]   # 369
check(TERMINAL == 369, "terminal cell M(3,3) = 369", TERMINAL, 369)

TERMINAL_DIGITS = [3, 6, 9]
check(list(map(int, str(TERMINAL))) == TERMINAL_DIGITS,
      "digits(369) = [3,6,9]", list(map(int, str(TERMINAL))), TERMINAL_DIGITS)

DIGIT_SUM = sum(TERMINAL_DIGITS)   # 18
check(DIGIT_SUM == 18, "3+6+9 = 18 = GATE", DIGIT_SUM, 18)

GATE = (37 - 1) // 2
check(GATE == 18, "GATE = (37-1)/2 = 18", GATE, 18)
check(dr(DIGIT_SUM) == 9, "DR(18) = 9 = NULL", dr(DIGIT_SUM), 9)
check(dr(TERMINAL) == 9, "DR(369) = 9 = NULL", dr(TERMINAL), 9)

# 369 = 9 × 41; both factors are significant
check(369 == 9 * 41, "369 = 9×41", 9 * 41, 369)
check(dr(9) == 9, "DR(9) = 9 = NULL (nine-principle fixed point)", dr(9), 9)
check(41 % 37 == 4, "41 mod 37 = 4 ∈ ORBIT_P", 41 % 37, 4)


# ── Base-90 preservation ──────────────────────────────────────────────────────

D_R = 90
check(D_R % 9 == 0, "d_R=90 ≡ 0 mod 9 → NULL-preserving", D_R % 9, 0)
check(dr(D_R) == 9, "DR(90) = 9 = NULL", dr(D_R), 9)

# Adding 90 does not change DR of any cell
for i in range(3):
    for j in range(3):
        v = MATRIX[i][j]
        check(dr(v + D_R) == dr(v), f"DR({v}+90) = DR({v}) = {dr(v)}",
              dr(v + D_R), dr(v))

# The singular variance: 80 vs 90; difference = 10
D_R2 = 80   # singular step
check(D_R - D_R2 == 10, "singular variance = 90-80 = 10 = modular ratio", D_R - D_R2, 10)
check(dr(D_R2) == 8, "DR(80) = 8 = AHL (singular step has AHL as DR)", dr(D_R2), 8)

# The singular step introduces DR=6 at anchor (not 5 like uniform rows)
# DR(177) = 6; if step were 90 (uniform), anchor would be 167: DR(167)=5
check(dr(167) == 5, "DR(ideal anchor 167) = 5 (uniform would give DR=5)", dr(167), 5)
check(dr(177) == 6, "DR(actual anchor 177) = 6 (singular step gives DR=6)", dr(177), 6)
# The singular step (80 vs 90) shifts anchor DR from 5 to 6


# ── DR=3 (TRIAD) does not appear in this matrix ──────────────────────────────

all_dr_values = {dr(MATRIX[i][j]) for i in range(3) for j in range(3)}
check(3 not in all_dr_values,
      "DR=3 (TRIAD) does not appear in the matrix", 3 not in all_dr_values, True)
check(all_dr_values == {5, 6, 7, 9},
      "DR values in matrix = {5,6,7,9}", all_dr_values, {5, 6, 7, 9})


# ── Output ────────────────────────────────────────────────────────────────────

LABEL = {5: "prime-residue", 6: "cascade-product", 7: "ALO", 9: "NULL"}

if __name__ == "__main__":
    print("Cascade DR Audit (corrected)")
    print("=" * 66)

    print(f"\n── DR table ──")
    print(f"  {'i':>2}  {'M(i,1)':>8} DR  {'M(i,2)':>8} DR  {'M(i,3)':>8} DR")
    for i in range(3):
        row = MATRIX[i]
        drs = DR_TABLE[i]
        print(f"  {i+1:>2}  {row[0]:>8}  {drs[0]}  {row[1]:>8}  {drs[1]}  {row[2]:>8}  {drs[2]}")

    print(f"\n── Column DR patterns ──")
    print(f"  Col 1: {COL_DR[0]}  ({LABEL[COL_DR[0][0]]} → {LABEL[COL_DR[0][1]]} → {LABEL[COL_DR[0][2]]})")
    print(f"  Col 2: {COL_DR[1]}  ALO={ALO} throughout")
    print(f"  Col 3: {COL_DR[2]}  NULL throughout")

    print(f"\n── Corrections to user's table ──")
    corrections = [
        (177, 3, 6, "TRIAD",    "cascade-product = DR(AHL+ALO)"),
        (178, 5, 7, "MEDIATOR", "ALO"),
        (268, 5, 7, "MEDIATOR", "ALO"),
        (358, 5, 7, "MEDIATOR", "ALO"),
    ]
    for val, wrong, right, wrong_label, right_label in corrections:
        print(f"  {val}: stated DR={wrong} ({wrong_label}) → actual DR={right} ({right_label})")

    print(f"\n── Row cascade ──")
    print(f"  Row 1: {DR_TABLE[0][0]}→{DR_TABLE[0][1]}→{DR_TABLE[0][2]}  "
          f"({LABEL[DR_TABLE[0][0]]}→{LABEL[DR_TABLE[0][1]]}→{LABEL[DR_TABLE[0][2]]})")
    for i in [1, 2]:
        print(f"  Row {i+1}: {DR_TABLE[i][0]}→{DR_TABLE[i][1]}→{DR_TABLE[i][2]}  "
              f"({LABEL[DR_TABLE[i][0]]}→{LABEL[DR_TABLE[i][1]]}→{LABEL[DR_TABLE[i][2]]})")
    print(f"  All rows terminate at DR=9=NULL: ✓")

    print(f"\n── Terminal cell 369 ──")
    print(f"  digits: {TERMINAL_DIGITS};  sum = {DIGIT_SUM} = GATE = (37-1)/2")
    print(f"  DR(18) = {dr(DIGIT_SUM)} = NULL;  DR(369) = {dr(TERMINAL)} = NULL")
    print(f"  369 = 9×41;  41 mod 37 = {41%37} ∈ ORBIT_P")

    print(f"\n── Singular variance ──")
    print(f"  d_R = {D_R}: DR({D_R}) = {dr(D_R)} = NULL (preserves all column DRs)")
    print(f"  Singular step = {D_R2}: DR({D_R2}) = {dr(D_R2)} = AHL (step carries AHL signature)")
    print(f"  Variance = {D_R}-{D_R2} = {D_R-D_R2} = modular ratio")
    print(f"  Effect on anchor DR: ideal 167→DR=5, actual 177→DR=6 (singular step shifts anchor)")

    print(f"\n── DR=3 (TRIAD) ──")
    print(f"  DR values present: {sorted(all_dr_values)}")
    print(f"  DR=3 is NOT in this matrix.")
    print(f"  The cascade runs 5(or 6) → 7 → 9, not 3 → 5 → 9.")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
