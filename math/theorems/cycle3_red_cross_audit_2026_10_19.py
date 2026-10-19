# CLASS: AUDIT
"""
"Cycle 3" with the red cross drawn over it: the pasted description audited against the owner's picture
(owner_work/images/2026-10-19_cycle3_red_cross.jpg, 2026-10-19; the paste is another tool's text, relayed
by the owner, in the same message as the picture).

THE OWNER'S PICTURE: the title "Cycle 3" over seven rows
    213312 / 221331 / 122133 / 312213 / 331221 / 133122 / 213312
with FOUR red lines through one point: a vertical line between the 3rd and 4th digit, a horizontal line
through row 3 (312213), and two diagonals corner to corner. The point is the middle of the twin 2s of row 3.
The paste describes only the two diagonals.

PRIOR ART (read before writing): math/lemmas/rotation_grids_x.py, owner 2026-10-04 -- the seam line
  "21331(22)13312" (213 turned and mirrored, written twice, the repdigit 22 at the seam) and the
  balanced X ("balances exactly when the repeated diagonal digit is the middle value").
  The rows of Cycle 3 are the six turns of 213312; row 3 is the six digits around the (22) of that line.

RIGHT:
  213312=2+1+3+3+1+2=12, every row is 12, 7x12=84
  row 3 across: 3+1=4, 2+2=4, 1+3=4
  \\ diagonal: 2 2 2 2 2 2 2 (seven 2s)
WRONG (pasted line / fixed line):
  / diagonal from bottom-left   2 1 3 2 1 3 2   |   2 3 1 2 1 3 2   (231, 2, 132: it does not repeat)
  top part                      8+4+1=13        |   8+4+0=12   (the 1 is a cut cell; rows 0 and 1 leave theirs out)
  bottom part                   1+4+8=13        |   0+4+8=12
  row 4 marks                   3 [3] 1 2 [2] 1 |   3 3 [1] [2] 2 1   (the lines pass the 1 and the 2 of row 4; the paste copied row 5's marks)
  "33 -> 13, 43 -> 13"          33 stays 33, 43-37=6, 13 stays 13   (neither 33 nor 43 gives 13)
  wings "18, 1+8=9"             left of both lines 16, right 16 (1+6=7); the paste lists no cells for 18
I CAN'T CHECK: "9-Spine Triad anchor" (no definition in the paste).

THE MISSING LINES (the vertical and the horizontal of the picture):
  vertical: 6+5+5+6+7+7+6=42 | 6+7+7+6+5+5+6=42, 42+42=84
  horizontal: 12+12+12=36 | 12 | 36, 36+12+36=84
  four quarters (row 3 left out): 6+5+5=16, 6+7+7=20, 7+7+6=20, 5+5+6=16, 72+12=84
  all four lines: wedges top 5+7=12, bottom 7+5=12, left 12, right 12; 48 + diagonal cells 24 + row 3 12 = 84
  cells struck by a line: 18, their sum 36; cells not struck: 24, their sum 48; 36+48=84

FORCED OR DEPENDS ON THE ORDER (the six orders of 1 2 3 each turned the same way, run below):
  every row 12, left wing 12, right wing 12: true for all six orders.
  top 12 and bottom 12, both diagonals 14=14: only for the orders that start with 2 (213, 231) --
  the owner's balanced X of 2026-10-04 (the repeated digit is the middle value). 123 gives top 15, diagonals 7 and 13.

FALSIFICATION: any assertion failing.
"""
from itertools import permutations


def build(row):
    rows, r = [], list(row)
    for _ in range(7):
        rows.append(r[:])
        r = [r[-1]] + r[:-1]
    return rows


def cross(g):
    A = {(r, round(2.5 + 6 / 7 * (r - 3))) for r in range(7)}
    B = {(r, round(5 - (2.5 + 6 / 7 * (r - 3)))) for r in range(7)}
    cut = {c for c in A | B if c[0] != 3}
    reg = {}
    for r in range(7):
        if r == 3:
            continue
        a = 2.5 + 6 / 7 * (r - 3)
        lo, hi = sorted((round(a), round(5 - a)))
        for c in range(6):
            if (r, c) in cut:
                continue
            side = ("T" if r < 3 else "B") if lo < c < hi else ("L" if c <= lo else "R")
            key = side + ("l" if c <= 2 else "r")
            reg[key] = reg.get(key, 0) + g[r][c]
    return sorted(A), sorted(B), cut, reg


g = build([2, 1, 3, 3, 1, 2])
assert g == [[2, 1, 3, 3, 1, 2], [2, 2, 1, 3, 3, 1], [1, 2, 2, 1, 3, 3], [3, 1, 2, 2, 1, 3],
             [3, 3, 1, 2, 2, 1], [1, 3, 3, 1, 2, 2], [2, 1, 3, 3, 1, 2]]
assert [sum(r) for r in g] == [12] * 7 and 7 * 12 == 84 and sum(map(sum, g)) == 84
assert g[3][0] + g[3][1] == g[3][2] + g[3][3] == g[3][4] + g[3][5] == 4
doubled = "21331" + "22" + "13312"                    # the owner's seam line of 2026-10-04
assert doubled == "213312" * 2 and doubled[3:9] == "312213" == "".join(map(str, g[3]))
assert ["".join(map(str, r)) for r in g] == [("213312" * 2)[(6 - i) % 6:(6 - i) % 6 + 6] for i in range(7)]   # six turns, then back

A, B, cut, reg = cross(g)
assert [g[r][c] for r, c in A] == [2] * 7
assert [g[r][c] for r, c in sorted(B, reverse=True)] == [2, 3, 1, 2, 1, 3, 2]      # bottom-left to top-right
assert [g[r][c] for r, c in sorted(B, reverse=True)] != [2, 1, 3, 2, 1, 3, 2]      # the pasted line
assert sum(g[r][c] for r, c in A) == sum(g[r][c] for r, c in B) == 14

# the pasted wedges: cells between the two cut cells of each row, cut cells left out
assert sum(g[0][1:5]) + sum(g[1][2:4]) + 0 == 12 and 8 + 4 + 1 == 13 and g[2][3] == 1
assert 0 + sum(g[5][2:4]) + sum(g[6][1:5]) == 12 and (g[4][2], g[4][3]) == (1, 2)
assert (g[4][1], g[4][4]) == (3, 2)                                                  # what the pasted row 4 marks
assert (33 % 37, 43 % 37, 43 - 37, 13 % 37) == (33, 6, 6, 13)
assert reg["Ll"] == reg["Rr"] == 12 and 12 + 4 == 16                                 # wings: 12 with the horizontal line, 16 with row 3's flank
assert sum(g[r][c] for r in range(1, 6) for c in range(6)
           if c < min(x for rr, x in cut | {(3, 2)} if rr == r)) == 16 == 2 + 3 + 4 + 6 + 1

# the vertical and the horizontal
left = [sum(r[:3]) for r in g]
right = [sum(r[3:]) for r in g]
assert left == [6, 5, 5, 6, 7, 7, 6] and right == [6, 7, 7, 6, 5, 5, 6] and sum(left) == sum(right) == 42
assert sum(map(sum, g[:3])) == sum(map(sum, g[4:])) == 36 and sum(g[3]) == 12
q = [sum(left[:3]), sum(right[:3]), sum(left[4:]), sum(right[4:])]
assert q == [16, 20, 20, 16] and sum(q) == 72 and sum(q) + 12 == 84
assert reg == {"Tl": 5, "Tr": 7, "Ll": 12, "Rr": 12, "Bl": 7, "Br": 5}
assert reg["Tl"] + reg["Tr"] == reg["Bl"] + reg["Br"] == 12 and sum(reg.values()) == 48
assert sum(g[r][c] for r, c in cut) == 24 and len(cut) == 12 and 48 + 24 + 12 == 84
struck = cut | {(3, c) for c in range(6)}
assert len(struck) == 18 and sum(g[r][c] for r, c in struck) == 36 and 36 + 48 == 84

# forced or depends on the order
for p in permutations((1, 2, 3)):
    h = build(list(p) + list(p)[::-1])
    a, b, ct, rg = cross(h)
    da, db = sum(h[r][c] for r, c in a), sum(h[r][c] for r, c in b)
    assert rg["Ll"] == rg["Rr"] == 12 and all(sum(r) == 12 for r in h)
    balanced = (rg["Tl"] + rg["Tr"] == 12 and da == db == 14)
    assert balanced == (p[0] == 2)
h = build([1, 2, 3, 3, 2, 1])
a, b, ct, rg = cross(h)
assert rg["Tl"] + rg["Tr"] == 15 and sum(h[r][c] for r, c in a) == 7 and sum(h[r][c] for r, c in b) == 13

ORB = {"IC": {1, 10, 26}, "NEG_H": {11, 27, 36}, "SA_ST_A": {9, 12, 16}, "C3": {3, 4, 30}, "D7": {7, 33, 34},
       "SEED": {18, 24, 32}, "TESLA": {6, 8, 23}, "CAS_EXT": {5, 13, 19}, "NQR17": {17, 22, 35},
       "DARK_A": {2, 15, 20}, "SA_ST_B": {21, 25, 28}, "C9": {14, 29, 31}}


def orbit(n):
    return next(k for k, v in ORB.items() if n % 37 in v)


assert [orbit(n) for n in (84, 36, 48, 12, 24, 42, 14, 16, 20, 13, 5, 7, 18)] == [
    "IC", "NEG_H", "NEG_H", "SA_ST_A", "SEED", "CAS_EXT", "C9", "SA_ST_A", "DARK_A", "CAS_EXT", "CAS_EXT", "D7", "SEED"]

if __name__ == "__main__":
    print("Cycle 3: rows 12 each, 84; / diagonal is 2 3 1 2 1 3 2 (pasted 2 1 3 2 1 3 2 wrong); wedges 12 not 13; "
          "vertical 42|42, horizontal 36|12|36, wedges 12 each; 12 for top/bottom only for orders starting with 2")
