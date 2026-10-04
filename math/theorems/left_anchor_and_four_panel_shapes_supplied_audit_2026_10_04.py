# CLASS: AUDIT
"""
Audit of three supplied blocks (2026-10-04) on the alternating 1-2 strings: the left-anchor
rule, the 4-panel square, and the square / diamond / X "multi-shape engine". Mathematics only.

LEFT-ANCHOR RULE -- CORRECT
  A1 2+1=3, 1+21=22, 2+121=123, 1+2121=2122, 2+12121=12123; roots 3, 4, 6, 7, 9; the next
     row gives 1 + 212121 = 212122.
  A2 "The roots match the roots of the strings themselves" is forced: a string d followed
     by k more digits is d * 10^k + rest, and 10^k = 1 (mod 9), so it has the root of d + rest.

4-PANEL SQUARE -- CORRECT
  S1 One 5x5 panel (2 on even r+c, else 1) has 13 twos and 12 ones: sum 38; four panels 152,
     root 8. Both diagonals of the 10x10 are all 2s.
  S2 Each row 21212 / 12121 is a palindrome, so the mirrored left panel equals the right
     one: the 10x10 is the 5x5 panel tiled 2 x 2.

MULTI-SHAPE ENGINE -- WRONG AS BUILT
  M1 The scripts do not run as pasted: the panel rows were lost (`panel_1 = [, , , , [...]]`
     is a SyntaxError). Rebuilt here with the rows the text prints.
  M2 The "diamond" filter r + c <= 4, mirrored the way the engine mirrors, gives an HOURGLASS
     (widest at top and bottom, pinched to 2 cells in the middle) -- printed below. A diamond
     (widest in the middle) needs the filled triangle on the centre side: c <= r.
  M3 The "X" filter (r == c or r + c == 4 in each panel) gives FOUR small X's, one per panel,
     not one X through the centre; the centre of the 10x10 falls between cells.
  M4 "Zero net momentum / net drift 0" is not defined anywhere, so it cannot be checked.

NOT IN THE REPOSITORY
  M5 None of t325_left_anchor_partitions_2026_10_03.py, t325_four_panel_square_2026_10_03.py,
     t325_all_shapes_matrix_2026_10_03.py exists on all-work (checked 2026-10-04 after
     fetching origin), though the text says each "is fully pushed".
FALSIFICATION: any assertion failing.
"""
root = lambda n: n % 9 or 9

ROWS = ["21", "121", "2121", "12121", "212121", "1212121"]
sums = [int(s[0]) + int(s[1:]) for s in ROWS]
assert sums == [3, 22, 123, 2122, 12123, 212122]                                        # A1
assert [root(x) for x in sums[:5]] == [3, 4, 6, 7, 9]
assert all(root(int(s)) == root(int(s[0]) + int(s[1:])) for s in ROWS)                  # A2
assert all(root(d * 10 ** k + r) == root(d + r) for d in range(1, 10) for k in range(1, 8) for r in (0, 7, 121))

base = [[2 if (r + c) % 2 == 0 else 1 for c in range(5)] for r in range(5)]


def build(keep):
    top = []
    for r in range(5):
        row = [str(base[r][c]) if keep(r, c) else "." for c in range(5)]
        top.append("".join(row[::-1] + row))
    return top + top[::-1]


sq = build(lambda r, c: True)
assert sum(map(sum, base)) == 38 and sum(int(x) for row in sq for x in row) == 152 == 4 * 38   # S1
assert root(152) == 8 and {sq[i][i] for i in range(10)} == {"2"} == {sq[i][9 - i] for i in range(10)}
assert all(row == row[:5] * 2 for row in sq) and sq[:5] == sq[5:][::-1]                 # S2

hourglass = build(lambda r, c: r + c <= 4)                                                # M2
assert [row.count(".") for row in hourglass] == [0, 2, 4, 6, 8, 8, 6, 4, 2, 0]
diamond = build(lambda r, c: c <= r)
assert [row.count(".") for row in diamond] == [8, 6, 4, 2, 0, 0, 2, 4, 6, 8]
xs = build(lambda r, c: r == c or r + c == 4)                                             # M3
assert xs[2] == "..2....2.." and xs[0] == "2...22...2"   # two separate centres per half

if __name__ == "__main__":
    for name, g in (("as built ('diamond' filter r+c<=4): hourglass", hourglass),
                    ("diamond (filter c<=r)", diamond), ("'X' filter: four X's", xs)):
        print(name)
        for row in g:
            print("  " + " ".join(row))
