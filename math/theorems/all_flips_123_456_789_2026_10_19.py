# CLASS: AUDIT
"""
All the flips of 123/456/789 (owner_work #359, 2026-10-19).

THE OWNER'S LINES, verbatim:
    123 / 456 / 789        123 / 654 / 789        123 / 654 / 987        331 / 654 / 987
    do all flips counting by 3 +1
TYPO: 331 for 321 (the fourth grid is all three rows flipped). The intended value is used.
Reading used: the four grids are 0, 1, 2 and 3 flips (3 flips + the unflipped grid = "3 +1"); the chain of #357 and #358 is run
on each; then all 8 choices of flipped rows are counted (1 + 3 + 3 + 1); then the places where this grid "counts by 3 and +1" (the
rows count +1 across, the columns count 3 down, the middle digits 2, 5, 8 count by 3). Nothing is asked.

IN THE OWNER'S NOTATION (rows ; row residues mod 37 ; sum ; root ; residue of the sum):
  123/456/789   6,6,6 ; 12,12,12 ; 1368=18=9 ; 12+12+12=36=-1
  123/654/789   6,6,6 ; 12,25,12 ; 1566=18=9 ; 12+25+12=49=12
  123/654/987   6,6,6 ; 12,25,25 ; 1764=18=9 ; 12+25+25=62=25
  321/654/987   6,6,6 ; 25,25,25 ; 1962=18=9 ; 25+25+25=75=1
  Every flip turns a row's 12 into 25 = -12. Forced for a row whose digits satisfy a+c=2b (the owner's diamond rule):
  abc + cba = 101(a+c) + 20b = 222b = 6b x 37.   123+321=444=12x37 ; 456+654=1110=30x37 ; 789+987=1776=48x37.
  The middle digits 2, 5, 8 count by 3, so 12, 30, 48 count by 18 and 444+1110+1776 = 3330 = 90x37 = 30x111.
ALL 8 CHOICES OF FLIPPED ROWS: 0 flips 1 grid, 1 flip 3 grids, 2 flips 3 grids, 3 flips 1 grid (1+3+3+1=8). The sum depends only on
  how many: 1368, 1566, 1764, 1962 (each flip +198=2x99 ; 198=13 mod 37 ; 198=9x22, so the root stays 9).
  1368+1962=3330 and 1566+1764=3330.  1368=37x37-1 ; 1566=2x3x3x3x29 ; 1764=42x42 ; 1962=2x3x3x109.
COLUMNS (read downward): 0 flips 147, 258, 369 step 111 ; 1 flip 167, 258, 349 step 91 ; 2 flips 169, 258, 347 step 89 ;
  3 flips 369, 258, 147 step -111 (the columns of the first grid in the other order).
  The unflipped grid counts +1 across each row and +3 down each column (1,4,7 / 2,5,8 / 3,6,9); a flipped row counts -1.
  Three flips is the owner's mirror (each row reversed, rotation_grids_x.py); 987/654/321 (also turned over) has the same sum 1962.

FALSIFICATION: any assertion failing.
"""
from itertools import combinations, product

from sympy import factorint


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


flip = lambda n: int(str(n)[::-1])
rows = [123, 456, 789]
grids = [[123, 456, 789], [123, 654, 789], [123, 654, 987], [321, 654, 987]]
assert [[flip(n) if flip(n) != n and i in c else n for i, n in enumerate(rows)] for c in [(), (1,), (1, 2), (0, 1, 2)]] == grids
assert 331 != 321 and flip(123) == 321

expect = {0: ([12, 12, 12], 1368, 36), 1: ([12, 25, 12], 1566, 12), 2: ([12, 25, 25], 1764, 25), 3: ([25, 25, 25], 1962, 1)}
for k, g in enumerate(grids):
    res, total, tr = expect[k]
    assert [dr(n) for n in g] == [6, 6, 6] and [n % 37 for n in g] == res
    assert sum(g) == total and dr(total) == 9 and total % 37 == tr == sum(res) % 37
assert [sum(expect[k][0]) for k in range(4)] == [36, 49, 62, 75] and [x % 37 for x in (36, 49, 62, 75)] == [36, 12, 25, 1]
assert 12 + 25 == 37 and all(flip(n) % 37 == (-n) % 37 for n in rows)

# forced for a + c = 2b
for a in range(1, 10):
    for b in range(10):
        c = 2 * b - a
        if 0 <= c <= 9:
            x, y = 100 * a + 10 * b + c, 100 * c + 10 * b + a
            assert x + y == 222 * b == 6 * b * 37 and (x + y) % 37 == 0
assert [123 + 321, 456 + 654, 789 + 987] == [444, 1110, 1776] == [12 * 37, 30 * 37, 48 * 37]
assert [12, 30, 48] == [6 * b for b in (2, 5, 8)] and [30 - 12, 48 - 30] == [18, 18]
assert 444 + 1110 + 1776 == 3330 == 90 * 37 == 30 * 111 == 222 * (2 + 5 + 8)

# all 8 choices
bycount = {}
for pick in product((0, 1), repeat=3):
    g = [flip(n) if p else n for p, n in zip(pick, rows)]
    bycount.setdefault(sum(pick), []).append(sum(g))
assert {k: len(v) for k, v in bycount.items()} == {0: 1, 1: 3, 2: 3, 3: 1} and 1 + 3 + 3 + 1 == 8
assert {k: set(v) for k, v in bycount.items()} == {0: {1368}, 1: {1566}, 2: {1764}, 3: {1962}}
assert all(b - a == 198 for a, b in ((1368, 1566), (1566, 1764), (1764, 1962))) and 198 == 2 * 99 == 9 * 22 and 198 % 37 == 13
assert 1368 + 1962 == 3330 == 1566 + 1764 and 1368 == 37 * 37 - 1
assert factorint(1566) == {2: 1, 3: 3, 29: 1} and 1764 == 42 * 42 and factorint(1962) == {2: 1, 3: 2, 109: 1}

# columns
digits = lambda ns: [[int(c) for c in str(n)] for n in ns]
col = lambda g: [100 * g[0][j] + 10 * g[1][j] + g[2][j] for j in range(3)]
assert [col(digits(g)) for g in grids] == [[147, 258, 369], [167, 258, 349], [169, 258, 347], [369, 258, 147]]
assert [(c[1] - c[0], c[2] - c[1]) for c in (col(digits(g)) for g in grids)] == [(111, 111), (91, 91), (89, 89), (-111, -111)]
g0 = digits(rows)
assert [[g0[i][j] for i in range(3)] for j in range(3)] == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
assert all(g0[i][j + 1] - g0[i][j] == 1 for i in range(3) for j in range(2)) and all(g0[i + 1][j] - g0[i][j] == 3 for i in range(2) for j in range(3))
assert flip(654) == 456 and [int(c) for c in "654"] == [6, 5, 4] and sum(grids[3]) == sum([987, 654, 321]) == 1962

if __name__ == "__main__":
    print("all flips: sums 1368, 1566, 1764, 1962 (36, 12, 25, 1 mod 37) in 1+3+3+1 grids; each flip +198; a flipped row is minus the row mod 37; "
          "row pairs 444, 1110, 1776 = 37 x 12, 30, 48")
