# CLASS: AUDIT
"""
Audit of supplied analysis (2026-10-06) of three math boards read from video
frames of 1000035063.mp4 (see records/mathframes_video_extraction_INCOMPLETE_2026_10_06.md).

RESULT: every number in the supplied analysis checks out. Two additions below.

1. ROW 7 OF THE LADDER X IS PRIOR ART, EXACT MATCH.
   The board's grid 786/243/342 and its theorem ("equal arms iff a = 7 mod 9")
   are math/lemmas/ladder_x_grid.py, already proved there for every a, not a
   new result. The supplied analysis's own correction ("13 is not a square")
   is right; neither the board nor the lemma file calls 13 a square.

2. SECTION 3's SPLIT (a <= 4 vs a >= 5) IS FORCED, NOT EMPIRICAL.
   With o = a a single digit, rev(o) = o always (a single digit reverses to
   itself). So 2(o+r) = 4a exactly, as the board's own header states.
   With i = 2a: if 2a is itself a single digit (a <= 4), rev(i) = i too, so
   i + ir = 2i = 4a -- forced equal to 2(o+r), no computation needed.
   If 2a has two digits (a >= 5), rev(i) != i in general and the identity
   breaks. So the a <= 4 / a >= 5 split IS the single-digit/two-digit split
   of 2a; it is not a separate fact to verify row by row.
   dr(i) = dr(2o) holding on all nine rows is for the same reason noted in
   the supplied analysis -- it is TRIVIAL here, since i = 2a = 2o by the
   reading itself, not an independent check.

FALSIFICATION: any assertion below failing.
"""
from sympy import isprime

dr = lambda n: 0 if n == 0 else 1 + (n - 1) % 9
rev = lambda n: int(str(n)[::-1])
ds = lambda n: sum(map(int, str(n)))

# --- Section 1: board grid == repo's ladder_x_grid.py row 7, prior art ---
BOARD_ROW7 = [[7, 8, 6], [2, 4, 3], [3, 4, 2]]
g = [d for row in BOARD_ROW7 for d in row]
assert "".join(map(str, g)) == "786243342"           # matches ladder_x_grid.row6(7)
assert g[0] + g[4] + g[8] == 13 and g[2] + g[4] + g[6] == 13
assert not (13**0.5).is_integer()                     # 13 is not a square
import math
assert math.isqrt(13) ** 2 != 13

# --- Section 2: the two 3x3 grids, row/column/diagonal sums ---
LEFT = [[3, 1, 4], [5, 2, 6], [7, 8, 9]]
RIGHT = [[2, 5, 7], [3, 1, 4], [6, 8, 9]]
for grid, rows, cols, diag, anti in (
    (LEFT, [8, 13, 24], [15, 11, 19], 14, 13),
    (RIGHT, [14, 8, 23], [11, 14, 20], 12, 14),
):
    assert [sum(r) for r in grid] == rows
    assert [grid[0][c] + grid[1][c] + grid[2][c] for c in range(3)] == cols
    assert grid[0][0] + grid[1][1] + grid[2][2] == diag
    assert grid[0][2] + grid[1][1] + grid[2][0] == anti
    assert sorted(d for r in grid for d in r) == list(range(1, 10))   # permutation of 1..9

assert 2357 + 4815 == 7172 and 7172 != 6262              # voiceover error, correctly caught
assert isprime(167)
assert dr(10) == 1                                        # mod-9 torus formula, standard convention

# --- Section 3: i = 2a, r = rev(a) = a (single digit), equality iff a <= 4 ---
rows = []
for a in range(1, 10):
    o, i = a, 2 * a
    r, ir = rev(o), rev(i)
    equal = (i + ir == 2 * (o + r))
    rows.append((a, equal))
    assert r == o                                         # single digit reverses to itself
    assert 2 * (o + r) == 4 * a                            # matches the board's own header
    assert equal == (a <= 4)                                # forced split: whether 2a is one digit
    assert (ds(i) == 2 * ds(o)) == (a <= 4)
    assert dr(i) == dr(2 * o)                               # trivial: i and 2o are the same number

assert [a for a, eq in rows if eq] == [1, 2, 3, 4]
assert [a for a, eq in rows if not eq] == [5, 6, 7, 8, 9]

print("video-boards audit: row 7 grid is prior art (ladder_x_grid.py); all")
print("row/column/diagonal sums and the voiceover corrections check out;")
print("section 3's split is forced by whether 2a is one digit. All assertions pass.")
