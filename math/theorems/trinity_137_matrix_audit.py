#!/usr/bin/env python3
"""
trinity_137_matrix_audit.py

Arithmetic audit of five claimed constructions:
  1. 157/248/369 Trinity Matrix
  2. 137 Extraction from 3-Block Method
  3. 713 / 427 / 1140 / Fine-Structure
  4. 6×6 matrix (header claims twenty 7s, ten 8s)
  5. Checkerboard matrix
"""

FAIL = []

def dr(n):
    """Digital root: n%9, with convention 0→9 for multiples of 9 (except 0)."""
    if n == 0:
        return 0
    r = n % 9
    return r if r != 0 else 9

def check(cond, label, detail=""):
    if not cond:
        FAIL.append(label + (f": {detail}" if detail else ""))
    return cond

# ---------------------------------------------------------------------------
# Section 1: Trinity Matrix
# ---------------------------------------------------------------------------
print("=== Section 1: Trinity Matrix ===")

matrix = [
    [1, 5, 7],
    [2, 4, 8],
    [3, 6, 9],
]

row_sums = [13, 14, 18]
row_drs  = [4, 5, 9]
for i, (row, rs, rd) in enumerate(zip(matrix, row_sums, row_drs)):
    s = sum(row)
    check(s == rs,   f"row{i+1} sum",      f"{s} != {rs}")
    check(dr(s)==rd, f"row{i+1} DR",        f"DR({s})={dr(s)} != {rd}")

col_sums = [6, 15, 24]
col_drs  = [6, 6, 6]
for j, (cs, cd) in enumerate(zip(col_sums, col_drs)):
    s = sum(matrix[i][j] for i in range(3))
    check(s == cs,   f"col{j+1} sum",       f"{s} != {cs}")
    check(dr(s)==cd, f"col{j+1} DR",         f"DR({s})={dr(s)} != {cd}")

# Diagonals
diag_desc = [matrix[i][i]   for i in range(3)]   # (1,1),(2,2),(3,3) → 1,4,9
diag_asc  = [matrix[i][2-i] for i in range(3)]   # (1,3),(2,2),(3,1) → 7,4,3
check(diag_desc == [1,4,9], "descent diagonal", str(diag_desc))
check(diag_asc  == [7,4,3], "ascent diagonal",  str(diag_asc))
check(sum(diag_desc)==14 and dr(sum(diag_desc))==5, "descent sum=14 DR=5")
check(sum(diag_asc) ==14 and dr(sum(diag_asc)) ==5, "ascent  sum=14 DR=5")

# Row / col DR totals
row_dr_total = sum(row_drs)    # 4+5+9 = 18
col_dr_total = sum(col_drs)    # 6+6+6 = 18
check(row_dr_total==18 and dr(row_dr_total)==9, "row DR total=18 DR=9")
check(col_dr_total==18 and dr(col_dr_total)==9, "col DR total=18 DR=9")
print(f"  All Trinity Matrix checks: {'PASS' if not FAIL else 'see failures'}")


# ---------------------------------------------------------------------------
# Section 2: 137 Extraction — 3-Block Method
# ---------------------------------------------------------------------------
print("\n=== Section 2: 137 Extraction from 3-Block Method ===")

B1 = [[1,1,1],[1,3,7],[2,4,8]]

# B1 row sums
b1_row_sums = [sum(r) for r in B1]   # [3, 11, 14]
check(b1_row_sums == [3, 11, 14], "B1 row sums", str(b1_row_sums))
check(14 // 2 == 7, "14/2 = 7")

# B2 col sums (labeled "B2 row sums" in document)
b2 = [sum(B1[i][j] for i in range(3)) for j in range(3)]  # col sums of B1
check(b2 == [4, 8, 16], "B2 (B1 col sums)", str(b2))
check(dr(16) == 7, "DR(16)=7")

# Dashboard columns
dash_col1 = [3, 4, 3]
dash_col2 = [2, 8, 2]
dash_col3 = [7, 7, 7]

check(sum(dash_col1)==10 and dr(sum(dash_col1))==1, "dash col1 sum=10 DR=1",
      f"sum={sum(dash_col1)} DR={dr(sum(dash_col1))}")
check(sum(dash_col2)==12 and dr(sum(dash_col2))==3, "dash col2 sum=12 DR=3",
      f"sum={sum(dash_col2)} DR={dr(sum(dash_col2))}")
check(sum(dash_col3)==21 and dr(sum(dash_col3))==3, "dash col3 sum=21 DR=3",
      f"sum={sum(dash_col3)} DR={dr(sum(dash_col3))}")

# Extraction claim: DRs → 1, 3, 7 → 137
extracted_drs = [dr(sum(dash_col1)), dr(sum(dash_col2)), dr(sum(dash_col3))]
print(f"  Dashboard col DRs: {extracted_drs}  (claimed: [1, 3, 7])")
check(extracted_drs == [1, 3, 3],
      "CONFIRM: col DRs are [1,3,3] not [1,3,7]",
      "the document's extraction is correct for the first two columns")

# The third extracted value (7) comes from cell values, not from DR(col3 sum)
# DR(col3 sum) = DR(21) = 3; cell values are all 7
col3_cell_value = dash_col3[0]  # 7
print(f"  col3 sum DR = {dr(21)}  (= 3, not 7)")
print(f"  col3 cell value = {col3_cell_value}  (= 7)")
print(f"  NOTE: 'Extracted: 1, 3, 7' uses DR(sum) for cols 1-2 but CELL VALUE for col 3.")
print(f"  The third extracted digit is 7 because all three cells ARE 7, not because DR(21)=7.")
print(f"  DR(21) = {dr(21)}. Extraction rule is inconsistent across columns.")
print(f"  Alternate read: B1 row 2 = [1,3,7] = 137 directly; the dashboard is a visual echo.")


# ---------------------------------------------------------------------------
# Section 3: 713 / 427 / 1140 / Fine-Structure
# ---------------------------------------------------------------------------
print("\n=== Section 3: 713 / 427 / 1140 ===")

check(713 + 427 == 1140, "713 + 427 = 1140")
check(713 - 427 == 286,  "713 - 427 = 286")
check(713 * 427 == 304451, "713 × 427 = 304451", f"actual={713*427}")
check(713**2 == 508369, "713² = 508369",        f"actual={713**2}")
check(508 + 369 == 877, "508 + 369 = 877")
check(508 - 369 == 139, "508 - 369 = 139")

# Fine-structure claim: n / 137.035999177 = 1140811334612.7932
# n is not specified in the document.
alpha_inv = 137.035999177
claimed_quotient = 1140811334612.7932
n_implied = alpha_inv * claimed_quotient
print(f"  α⁻¹ = {alpha_inv}")
print(f"  claimed: n / {alpha_inv} = {claimed_quotient:.4f}")
print(f"  implied n = α⁻¹ × {claimed_quotient:.4f} = {n_implied:.4e}")
print(f"  n is NOT specified in the document.")
print(f"  The 'first digits 1140' observation: the quotient begins with 1140 → matches 713+427.")
print(f"  Without specifying n, this is unverifiable.")
# Check: does 1140 × α⁻¹ have any special significance?
x = 1140 * alpha_inv
print(f"  1140 × α⁻¹ = {x:.6f}  (not a special constant)")
print(f"  NOTE: any n can be divided by α⁻¹; choosing n to produce leading digits 1140")
print(f"  does not demonstrate a relationship between 713+427 and the fine-structure constant.")


# ---------------------------------------------------------------------------
# Section 4: 6×6 Matrix
# ---------------------------------------------------------------------------
print("\n=== Section 4: 6×6 Matrix ===")

matrix_6x6 = [
    [8, 7, 7, 7, 7, 8],
    [7, 8, 7, 7, 8, 7],
    [7, 7, 8, 8, 7, 7],
    [7, 7, 8, 8, 7, 7],
    [7, 8, 7, 7, 8, 7],
    [8, 7, 7, 7, 7, 8],
]

# Row sums
for i, row in enumerate(matrix_6x6):
    s = sum(row)
    check(s == 44,       f"6×6 row{i+1} sum=44",  f"got {s}")
    check(dr(s) == 8,    f"6×6 row{i+1} DR=8",    f"DR({s})={dr(s)}")

# Column sums
for j in range(6):
    col = [matrix_6x6[i][j] for i in range(6)]
    s = sum(col)
    check(s == 44, f"6×6 col{j+1} sum=44", f"got {s}")

# Count 7s and 8s
count_7 = sum(row.count(7) for row in matrix_6x6)
count_8 = sum(row.count(8) for row in matrix_6x6)
total   = count_7 + count_8

check(count_7 == 24, "total 7s = 24", f"got {count_7}")
check(count_8 == 12, "total 8s = 12", f"got {count_8}")
check(total   == 36, "total cells = 36", f"got {total}")

print(f"  7s: {count_7}  8s: {count_8}  total: {total}")
print(f"  NOTE: Document header says 'twenty 7s, ten 8s'.")
print(f"  Actual matrix has {count_7} sevens and {count_8} eights — NOT 20 and 10.")
print(f"  The tabulated totals (Total 7s: 24, Total 8s: 12) inside the section ARE correct.")
print(f"  The section HEADER is wrong: should read 'twenty-four 7s, twelve 8s'.")
# Verify 20+10=30 would give 30 cells, not 36
print(f"  20+10=30 cells ≠ 6×6=36 cells (30 is a 5×6 grid, not 6×6).")


# ---------------------------------------------------------------------------
# Section 5: Checkerboard Matrix
# ---------------------------------------------------------------------------
print("\n=== Section 5: Checkerboard Matrix ===")

checker = [
    [7, 8, 7, 8, 7, 8],
    [8, 7, 8, 7, 8, 7],
    [7, 8, 7, 8, 7, 8],
    [8, 7, 8, 7, 8, 7],
    [7, 8, 7, 8, 7, 8],
]

for i, row in enumerate(checker):
    s = sum(row)
    check(s == 45,    f"checker row{i+1} sum=45", f"got {s}")
    check(dr(s) == 9, f"checker row{i+1} DR=9",   f"DR({s})={dr(s)}")

c7 = sum(r.count(7) for r in checker)
c8 = sum(r.count(8) for r in checker)
check(c7 == 15, "checker 7s=15", f"got {c7}")
check(c8 == 15, "checker 8s=15", f"got {c8}")
check(c7+c8 == 30, "checker total=30 (5×6)", f"{c7+c8}")
print(f"  7s: {c7}  8s: {c8}  (5×6=30 cells) — all correct ✓")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
if FAIL:
    print(f"FAILED ({len(FAIL)}):")
    for f in FAIL:
        print(f"  ✗ {f}")
    import sys; sys.exit(1)
else:
    print("AUDIT COMPLETE — all arithmetic PASS")
    print()
    print("  Section 1 (Trinity Matrix): all row/col/diagonal sums correct ✓")
    print()
    print("  Section 2 (137 Extraction):")
    print("    All B1/B2 arithmetic correct ✓")
    print("    Dashboard col DRs: [1, 3, 3] — NOT [1, 3, 7]")
    print("    The '7' in the extraction comes from cell values in col 3,")
    print("    not from DR(col3 sum)=DR(21)=3.")
    print("    Simplest read: 137 is B1 row 2 = [1,3,7] directly;")
    print("    the dashboard construction cannot derive 7 from column DRs.")
    print()
    print("  Section 3 (713/427/1140):")
    print("    All integer arithmetic correct ✓")
    print("    Fine-structure quotient unverifiable: n is unspecified.")
    print("    Leading-digit 1140 observation: depends on choice of n.")
    print()
    print("  Section 4 (6×6 Matrix):")
    print("    All row/column sums = 44, DR = 8 ✓")
    print("    HEADER ERROR: says 'twenty 7s, ten 8s'")
    print("    Actual: 24 sevens, 12 eights (20+10=30 ≠ 6×6=36)")
    print("    Internal tabulated counts (24, 12) are correct.")
    print()
    print("  Section 5 (Checkerboard):")
    print("    All row sums = 45, DR = 9 ✓")
    print("    15 sevens, 15 eights, 30 cells ✓")
    print()
    print("  Section 6 (0,000 Origin): conceptual, no arithmetic content.")
