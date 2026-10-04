# CLASS: AUDIT
"""
Audit of supplied blocks (2026-10-04): the 8-column engine, the 2x2 prime-digit grips 23 / 32,
and the rotated 8x8 parity field. (The "PR #8 sync" block restates
eight_column_ceiling_supplied_audit_2026_10_04.py correctly.) Mathematics only.

8-COLUMN ENGINE -- runs, and every check is CORRECT but empty
  C1 It scans an 8x8 grid of all 9s: every line is 72 and the total 576 (root 9) because the
     grid is constant. A constant grid gives the same sum in every direction, so the scan
     carries no information. Its mod-5 counts are copied from the earlier audit, not computed.
2x2 PRIME-DIGIT GRIPS -- arithmetic CORRECT
  C2 [[2,3],[3,2]] and [[3,2],[2,3]]: every row and column 5; diagonals 4 and 6 (and 6 and 4);
     each grid totals 10.
  C3 WRONG: "2 is a composite digit" -- 2 is prime (the text also calls it prime one clause
     earlier). The script does not run: `assert ... == ` with nothing after it is a SyntaxError.
ROTATED 8x8 PARITY FIELD -- internally inconsistent
  C4 The script lost its rows (SyntaxError). Its comments give row 4 twice, differently:
     "o e o o o o e o" (6 odd) and "1 0 0 1 1 0 0 1" (4 odd).
  C5 With the binary rows given (rows 5-8 mirroring 1-4), the odd total is 28, so the script's
     `assert total_odd_nodes == 32` FAILS; the 32 needs the token-string version of row 4.
  C6 The printed rotated rows do not follow its own rule (shift row r by r): row 4 shifted by 3
     is 1 1 0 0 1 1 0 0 = "o o e e o o e e", not the printed "o o o e o e o o"; rows 5-8 are
     printed with mismatched binary and token strings.
  C7 CORRECT in principle: rotating a row never changes how many odd entries it has, so row
     totals (and the grand total) are conserved; only the column and diagonal sums move.
FALSIFICATION: any assertion failing.
"""
grid = [[9] * 8 for _ in range(8)]                                                       # C1
assert {sum(r) for r in grid} == {72} == {sum(c) for c in zip(*grid)} and sum(map(sum, grid)) == 576
assert sum(grid[i][i] for i in range(8)) == sum(grid[i][7 - i] for i in range(8)) == 72

for g, d in (([[2, 3], [3, 2]], (4, 6)), ([[3, 2], [2, 3]], (6, 4))):                   # C2
    assert {sum(r) for r in g} == {5} == {sum(c) for c in zip(*g)}
    assert (g[0][0] + g[1][1], g[0][1] + g[1][0]) == d and sum(map(sum, g)) == 10
assert 2 in (2, 3, 5, 7)                                                                 # C3

tok = lambda s: [1 if c == "o" else 0 for c in s.split()]
assert sum(tok("o e o o o o e o")) == 6 and sum([1, 0, 0, 1, 1, 0, 0, 1]) == 4           # C4
top = [[1, 1, 0, 1, 1, 0, 1, 1], [0, 0, 1, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0, 0, 1]]
field = top + top[::-1]
assert sum(map(sum, field)) == 28 != 32                                                  # C5
alt = top[:3] + [tok("o e o o o o e o")]
assert sum(map(sum, alt + alt[::-1])) == 32
row4 = top[3][3:] + top[3][:3]                                                           # C6
assert row4 == [1, 1, 0, 0, 1, 1, 0, 0] and row4 != tok("o o o e o e o o")
rot = [r[i % 8:] + r[:i % 8] for i, r in enumerate(field)]                               # C7
assert [sum(r) for r in rot] == [sum(r) for r in field]
