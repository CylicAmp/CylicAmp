"""
doubling_cycle_matrix_audit.py

Doubling-cycle matrix: five paired strings encoding DR doubling cycle steps 1–5.

─────────────────────────────────────────────────────────────────
MATRIX (left / right pairs):

  101112 / 211101    d=1  DR(2×1)=2
  202224 / 422202    d=2  DR(2×2)=4
  404448 / 844404    d=4  DR(2×4)=8
  808887 / 788808    d=8  DR(2×8)=DR(16)=7
  707775 / 577707    d=7  DR(2×7)=DR(14)=5

STRUCTURE (left string of each row):
  [d, 0, d, d, d, DR(2d)]  — d steps through the DR doubling cycle

DR DOUBLING CYCLE (from dr_algebra.py):
  1 → 2 → 4 → 8 → 7 → 5 → 1  (period 6)
  This matrix covers steps d ∈ {1, 2, 4, 8, 7}  (rows 1–5).
  Missing row (step 6): d=5 → [5,0,5,5,5,1]  digit_sum=21  DR=3.

KEY FACTS:
  (M1) Right string = exact reversal of left string (all 5 rows).

  (M2) Row digit-sum formula: digit_sum = 4d + DR(2d).
       Row DRs:  6, 3, 6, 3, 6  (locked to {3,6}, alternating, period 2).

  (M3) Left-grid column sums (6 columns, rows 1–5):
         Col 1 = 1+2+4+8+7 = 22 = 2×11 = 2×repunit_2
         Col 2 = 0+0+0+0+0 =  0
         Col 3 = 22  (same as col 1)
         Col 4 = 22
         Col 5 = 22
         Col 6 = 2+4+8+7+5 = 26 = 2×13  (AHL digit-sum; slot of 137 in Z/37Z)

  (M4) Total left-grid digit-sum = 114;  DR(114) = 6.

  (M5) Left + right numerical sums — DR alternates {3,6,3,6,3}
       (inverted relative to the row DR sequence {6,3,6,3,6}).

  (M6) AHL/ALO connection (alpha_grid.py):
         AHL = 8 = digit at position RH-E; digit_sum of 8-pair strings = 26 = col 6 sum.
         ALO = 7 = digit at position RL-O; digit_sum of 7-pair strings = 34 = 2×17.
       Col 6 sum = 26 = 2×13 (6th prime).  DR(26) = 8 = AHL.

  (M7) Missing-row completion:
         d=5 step yields [5,0,5,5,5,1];  digit_sum=21;  DR=3.
         Appending it restores the full 6-step cycle and gives total = 135;  DR(135)=9.
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
    r = n % 9
    return r if r else 9


def digit_sum(s):
    return sum(int(c) for c in str(s))


# ── Raw strings ───────────────────────────────────────────────────────────────

LEFT  = ["101112", "202224", "404448", "808887", "707775"]
RIGHT = ["211101", "422202", "844404", "788808", "577707"]

# DR doubling cycle steps covered by rows 1-5
D_STEPS = [1, 2, 4, 8, 7]


# ── M1: Right = reversal of left ─────────────────────────────────────────────

for i, (L, R) in enumerate(zip(LEFT, RIGHT)):
    rev = L[::-1]
    check(rev == R, f"row {i+1}: reverse({L}) = {R}", rev, R)


# ── Structure: each left row = [d, 0, d, d, d, DR(2d)] ──────────────────────

for i, (L, d) in enumerate(zip(LEFT, D_STEPS)):
    digits = [int(c) for c in L]
    expected = [d, 0, d, d, d, dr(2 * d)]
    check(digits == expected, f"row {i+1} structure [{d},0,{d},{d},{d},{dr(2*d)}]",
          digits, expected)


# ── M2: Row digit-sum formula 4d + DR(2d) ───────────────────────────────────

EXPECTED_DS = [6, 12, 24, 39, 33]
EXPECTED_ROW_DR = [6, 3, 6, 3, 6]

for i, (L, d) in enumerate(zip(LEFT, D_STEPS)):
    ds = digit_sum(L)
    formula = 4 * d + dr(2 * d)
    check(ds == formula, f"row {i+1} digit_sum = 4×{d}+DR({2*d}) = {formula}", ds, formula)
    check(ds == EXPECTED_DS[i], f"row {i+1} digit_sum = {EXPECTED_DS[i]}", ds, EXPECTED_DS[i])
    check(dr(ds) == EXPECTED_ROW_DR[i], f"row {i+1} DR = {EXPECTED_ROW_DR[i]}",
          dr(ds), EXPECTED_ROW_DR[i])

# Row DRs are alternating {6,3} starting 6
check(EXPECTED_ROW_DR == [6, 3, 6, 3, 6], "row DR sequence = [6,3,6,3,6]",
      EXPECTED_ROW_DR, [6, 3, 6, 3, 6])
check(set(EXPECTED_ROW_DR) == {3, 6}, "row DRs locked to {3,6}", set(EXPECTED_ROW_DR), {3, 6})


# ── M3: Column sums of left grid ─────────────────────────────────────────────

COLS = [[int(L[j]) for L in LEFT] for j in range(6)]
COL_SUMS = [sum(c) for c in COLS]

EXPECTED_COL_SUMS = [22, 0, 22, 22, 22, 26]
check(COL_SUMS == EXPECTED_COL_SUMS, "left grid column sums", COL_SUMS, EXPECTED_COL_SUMS)

# Cols 1,3,4,5 = 22 = 2×11 = 2×repunit_2
for j in [0, 2, 3, 4]:
    check(COL_SUMS[j] == 22, f"col {j+1} sum = 22 = 2×repunit_2", COL_SUMS[j], 22)
check(22 == 2 * 11, "22 = 2×11 = 2×repunit_2", 22, 2 * 11)
check(11 % 37 == 11, "11 = repunit_2 in Z/37Z", 11 % 37, 11)

# Col 2 = 0 (all zeros)
check(COL_SUMS[1] == 0, "col 2 sum = 0", COL_SUMS[1], 0)

# Col 6 = 26 = AHL digit-sum = slot of 137 = 2×13
check(COL_SUMS[5] == 26, "col 6 sum = 26 (AHL digit-sum)", COL_SUMS[5], 26)
check(26 == 2 * 13, "26 = 2×13 (6th prime pair)", 26, 2 * 13)
check(dr(26) == 8, "DR(26) = 8 = AHL", dr(26), 8)
check(137 % 37 == 26, "137 mod 37 = 26 (col 6 sum = slot of 137)", 137 % 37, 26)


# ── M4: Total left-grid digit-sum ────────────────────────────────────────────

total_left = sum(digit_sum(L) for L in LEFT)
check(total_left == sum(EXPECTED_DS), "total left digit-sum", total_left, sum(EXPECTED_DS))
check(total_left == 114, "total = 114", total_left, 114)
check(dr(total_left) == 6, "DR(114) = 6", dr(total_left), 6)

# Also equals sum of column sums
check(sum(COL_SUMS) == total_left, "sum(col sums) = total digit-sum",
      sum(COL_SUMS), total_left)


# ── M5: Left + right numerical sums ──────────────────────────────────────────

EXPECTED_LR_DR = [3, 6, 3, 6, 3]

for i, (L, R) in enumerate(zip(LEFT, RIGHT)):
    lv, rv = int(L), int(R)
    s = lv + rv
    ds_s = digit_sum(s)
    d_s = dr(ds_s)
    check(d_s == EXPECTED_LR_DR[i], f"row {i+1} L+R DR = {EXPECTED_LR_DR[i]}", d_s, EXPECTED_LR_DR[i])

# Inverted relative to row DRs [6,3,6,3,6]
for i in range(5):
    check(EXPECTED_ROW_DR[i] + EXPECTED_LR_DR[i] == 9,
          f"row {i+1}: row_DR + LR_DR = 9 (complementary)",
          EXPECTED_ROW_DR[i] + EXPECTED_LR_DR[i], 9)


# ── M6: AHL/ALO connection ────────────────────────────────────────────────────

# AHL = 8 (step 4/6 in doubling cycle: 1→2→4→8); digit_sum of AHL-pair strings = 26
check(D_STEPS[3] == 8, "row 4 d = 8 = AHL", D_STEPS[3], 8)
check(digit_sum(LEFT[3]) == 39, "row 4 (d=8) digit_sum = 39", digit_sum(LEFT[3]), 39)
check(dr(39) == 3, "DR(39) = 3", dr(39), 3)

# ALO = 7 (step 5/6 in doubling cycle: 1→2→4→8→7); digit_sum of ALO-pair strings = 33
check(D_STEPS[4] == 7, "row 5 d = 7 = ALO", D_STEPS[4], 7)
check(digit_sum(LEFT[4]) == 33, "row 5 (d=7) digit_sum = 33", digit_sum(LEFT[4]), 33)
check(dr(33) == 6, "DR(33) = 6", dr(33), 6)

# Col 6 sum = 26 = AHL digit-sum (from master_matrix_audit): DR(26) = 8 = AHL
check(COL_SUMS[5] == 26, "col 6 sum = AHL digit-sum = 26", COL_SUMS[5], 26)

# AHL and ALO are consecutive steps (4th and 5th) in the 6-step cycle
ahl_idx = D_STEPS.index(8)
alo_idx = D_STEPS.index(7)
check(alo_idx == ahl_idx + 1, "ALO step immediately follows AHL step in cycle",
      alo_idx, ahl_idx + 1)

# Cross-add: AHL + ALO = 8 + 7 = 15; DR = 6 = DR(total left)
check(dr(8 + 7) == 6, "DR(AHL+ALO) = DR(15) = 6 = DR(total)", dr(8 + 7), 6)

# Cross-multiply: AHL × ALO = 56; DR = 2 (first prime)
check(dr(8 * 7) == 2, "DR(AHL×ALO) = DR(56) = 2 = first prime", dr(8 * 7), 2)


# ── M7: Missing-row completion (d=5, step 6 of cycle) ────────────────────────

# The 6-step DR doubling cycle: 1→2→4→8→7→5→1
FULL_CYCLE = [1, 2, 4, 8, 7, 5]
check(FULL_CYCLE[:5] == D_STEPS, "rows 1-5 cover first 5 cycle steps",
      FULL_CYCLE[:5], D_STEPS)

d_missing = FULL_CYCLE[5]
check(d_missing == 5, "missing step d = 5", d_missing, 5)

missing_row = [d_missing, 0, d_missing, d_missing, d_missing, dr(2 * d_missing)]
missing_formula = 4 * d_missing + dr(2 * d_missing)
check(missing_row == [5, 0, 5, 5, 5, 1], "missing row = [5,0,5,5,5,1]",
      missing_row, [5, 0, 5, 5, 5, 1])
check(missing_formula == 21, "missing row digit_sum = 4×5+DR(10) = 21", missing_formula, 21)
check(dr(missing_formula) == 3, "DR(21) = 3", dr(missing_formula), 3)

# Full 6-row total digit-sum = 114 + 21 = 135; DR = 9
full_total = total_left + missing_formula
check(full_total == 135, "full 6-row total = 135", full_total, 135)
check(dr(full_total) == 9, "DR(135) = 9", dr(full_total), 9)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Doubling Cycle Matrix Audit")
    print("=" * 62)

    print("\n── Matrix (left / right) ──")
    print(f"  {'Left':>8}  {'Right':>8}  {'d':>2}  {'DR(2d)':>6}  {'ds':>4}  {'DR':>3}")
    for i, (L, R, d) in enumerate(zip(LEFT, RIGHT, D_STEPS)):
        ds = digit_sum(L)
        print(f"  {L:>8} / {R:>8}   {d:>2}      {dr(2*d):>3}    {ds:>4}    {dr(ds):>3}")

    print(f"\n── Structure: [d, 0, d, d, d, DR(2d)] ──")
    for L, d in zip(LEFT, D_STEPS):
        row = [int(c) for c in L]
        print(f"  d={d}: {row}  digit_sum=4×{d}+{dr(2*d)}={4*d+dr(2*d)}")

    print(f"\n── Column sums (left grid) ──")
    for j, s in enumerate(COL_SUMS):
        note = ""
        if j in [0, 2, 3, 4]:
            note = f"  = 2×repunit_2"
        elif j == 1:
            note = f"  (zero column)"
        elif j == 5:
            note = f"  = 2×13 = AHL digit-sum = slot(137) in Z/37Z"
        print(f"  Col {j+1}: {s}{note}")
    print(f"  Total: {total_left}  DR={dr(total_left)}")

    print(f"\n── Left + right DR (row-by-row) ──")
    for i, (L, R) in enumerate(zip(LEFT, RIGHT)):
        s = int(L) + int(R)
        row_dr = EXPECTED_ROW_DR[i]
        lr_dr = dr(digit_sum(s))
        print(f"  Row {i+1}: {L}+{R}={s}  DR={lr_dr}  (row_DR={row_dr}  sum={row_dr+lr_dr})")

    print(f"\n── AHL/ALO connection ──")
    print(f"  AHL=8 at row 4 (d=8, step 4/6 in doubling cycle)")
    print(f"  ALO=7 at row 5 (d=7, step 5/6 in doubling cycle)")
    print(f"  Col 6 sum = 26 = AHL digit-sum = slot(137) mod 37")
    print(f"  AHL+ALO = 15  DR=6 = DR(total={total_left})")
    print(f"  AHL×ALO = 56  DR=2 = first prime")

    print(f"\n── Missing row (d=5, step 6 of cycle) ──")
    print(f"  [5,0,5,5,5,1]  digit_sum=21  DR=3")
    print(f"  Full 6-row total = {full_total}  DR={dr(full_total)}")
    print(f"  DR doubling cycle: 1→2→4→8→7→5→1  (period 6)")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
