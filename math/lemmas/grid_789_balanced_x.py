# CLASS: LEMMA
"""
Owner, 2026-10-04:
    2+4=6   2+3=5   2+1=3      2+2=(4+2=6)   22,426
    grids   134    124    135
            256    653    426
            789    789    789
Context: the X on a 3x3 grid (ladder_x_grid.py): the two diagonals cross at the
centre at right angles, so the X is "square" when its arms have equal sums.

THE +2 RULE (proved): for a grid of 1..9 with 7 8 9 along the bottom, the arms
are top-left + centre + 9 and top-right + centre + 7, so they are equal exactly
when top-right = top-left + 2. The possible corner pairs are
    (1, 3), (2, 4), (3, 5), (4, 6)
-- the owner's 2+1 = 3, 2+2 = 4, 2+3 = 5, 2+4 = 6. Of the 720 grids with 789 on
the bottom, 96 have a balanced X. The plain grid 123/456/789 is one: 1+5+9 =
3+5+7 = 15.

THE THREE GRIDS:
    134/256/789: rows 8, 13, 24; columns 10, 16, 19; X arms 15, 16 (corners 1, 4)
    124/653/789: rows 7, 14, 24; columns 14, 15, 16; X arms 15, 16 (corners 1, 4)
        top + middle in every column is 7 (1+6, 2+5, 4+3), and the middle row
        653 is 2+4, 2+3, 2+1 in order.
    135/426/789: rows 9, 12, 24; columns 12, 13, 20; X arms 12, 14 (corners 1, 5)
        426 is "22,426": 2+2 = 4, then 2, then 4+2 = 6; 135 steps by 2.
  None of the three has corners 2 apart, so none has a balanced X as written.
  Every grid of 1..9 totals 45 and its bottom row 789 sums to 24.

FALSIFICATION: any assertion below failing.
"""
from itertools import permutations

def arms(g):
    return g[0][0] + g[1][1] + g[2][2], g[0][2] + g[1][1] + g[2][0]

BAL, PAIRS = 0, set()
for p in permutations(range(1, 7)):
    g = [list(p[:3]), list(p[3:]), [7, 8, 9]]
    a, b = arms(g)
    assert (a == b) == (g[0][2] == g[0][0] + 2)
    if a == b:
        BAL += 1
        PAIRS.add((g[0][0], g[0][2]))
assert BAL == 96 and sorted(PAIRS) == [(1, 3), (2, 4), (3, 5), (4, 6)]
assert [2 + 1, 2 + 2, 2 + 3, 2 + 4] == [3, 4, 5, 6]
assert arms([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == (15, 15)

A = [[1, 3, 4], [2, 5, 6], [7, 8, 9]]
B = [[1, 2, 4], [6, 5, 3], [7, 8, 9]]
C = [[1, 3, 5], [4, 2, 6], [7, 8, 9]]
assert [arms(g) for g in (A, B, C)] == [(15, 16), (15, 16), (12, 14)]
assert [sum(c) for c in zip(*B)] == [14, 15, 16] and [B[0][i] + B[1][i] for i in range(3)] == [7, 7, 7]
assert B[1] == [2 + 4, 2 + 3, 2 + 1] and C[1] == [2 + 2, 2, (2 + 2) + 2] and C[0] == [1, 3, 5]
assert all(sum(map(sum, g)) == 45 for g in (A, B, C))

if __name__ == "__main__":
    print("balanced X grids with 789 bottom:", BAL, sorted(PAIRS))
    print("all assertions pass")
