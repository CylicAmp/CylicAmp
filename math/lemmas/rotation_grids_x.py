# CLASS: LEMMA
"""
Owner, 2026-10-04: "any row of 3 numbers I always find its rotational
sequences ... also there is its mirror and then double mirror that create
x and diamond like before". Examples given:
    426 -> 642 -> 264 -> 426   (=1, =2, =3: back on the third turn)
    246 -> 624 -> 462 -> 246
    642 -> 264 -> 426 -> 642
    "the flow above going to the left; here to the right": 246 -> 462 -> 624 -> 246
Builds on ladder_x_grid.py and grid_789_balanced_x.py (the X on a 3x3 grid
balances when its two arms have equal sums).

ROTATION AND MIRROR: three different digits turn round in a cycle of 3, in
either direction (the two flows are the same cycle walked both ways). The
mirror of a row (246 -> 642) lies in the OTHER cycle, so a row's rotations
plus its mirror's rotations are all 3! = 6 orders: {246, 462, 624} and
{426, 642, 264}.

ROTATION GRIDS: stack a cycle as a 3x3 grid (e.g. 246/624/462). Every row and
every column holds 2, 4, 6 once (a Latin square), so all sum to 12. One
diagonal repeats one digit; the other holds all three (sum 12).
THE BALANCED X: the repeated diagonal sums to 3 x its digit, so the X balances
exactly when that digit is the middle value 4 (3 x 4 = 2 + 4 + 6). Then every
row, column and both diagonals are 12 -- a magic square. Of the 12 stackings
(6 starts x 2 flows), exactly 4 do it:
    462/246/624    264/642/426    624/246/462    426/642/264
  and they are ONE grid with its mirror (each row reversed), its flip (rows in
  reverse order) and its double mirror (both = turned 180 degrees). The centre
  is 4 in all four.
WHEN IT WORKS: it needs 3 x middle = sum, i.e. the three numbers evenly
spaced (a+c = 2b). 246, 135 and 789 (the owner's grid rows) are evenly spaced,
and so are 123, 456, 789; 134 and 256 are not, and give no balanced X.

FALSIFICATION: any assertion below failing.
"""
from itertools import permutations

def rot_r(s):
    return s[-1] + s[:-1]

def rot_l(s):
    return s[1:] + s[0]

def cycle(s, f):
    out = [s]
    while f(out[-1]) != s:
        out.append(f(out[-1]))
    return out

def grid(rows):
    return [[int(c) for c in r] for r in rows]

def magic(g):
    lines = [sum(r) for r in g] + [sum(c) for c in zip(*g)]
    lines += [g[0][0] + g[1][1] + g[2][2], g[0][2] + g[1][1] + g[2][0]]
    return len(set(lines)) == 1

assert cycle("426", rot_r) == ["426", "642", "264"]
assert cycle("246", rot_r) == ["246", "624", "462"]
assert cycle("642", rot_r) == ["642", "264", "426"]
assert cycle("246", rot_l) == ["246", "462", "624"]
assert "246"[::-1] in cycle("426", rot_r)
assert set(cycle("246", rot_r)) | set(cycle("426", rot_r)) == {"".join(p) for p in permutations("246")}

MAGIC = []
for start in ("246", "462", "624", "426", "642", "264"):
    for f in (rot_r, rot_l):
        g = grid(cycle(start, f))
        assert all(sum(r) == 12 for r in g) and all(sum(c) == 12 for c in zip(*g))
        if magic(g):
            MAGIC.append(cycle(start, f))
assert sorted(MAGIC) == sorted([["462", "246", "624"], ["264", "642", "426"],
                                ["624", "246", "462"], ["426", "642", "264"]])
G = ["462", "246", "624"]
mirror = [r[::-1] for r in G]
flip = G[::-1]
double = [r[::-1] for r in G[::-1]]
assert sorted([G, mirror, flip, double]) == sorted(MAGIC)
assert all(grid(m)[1][1] == 4 for m in MAGIC)

def has_magic_rotation(t):
    return any(magic(grid(cycle("".join(p), f))) for p in permutations(t) for f in (rot_r, rot_l))
for t in ("246", "135", "789", "123", "456"):
    assert has_magic_rotation(t)
for t in ("134", "256", "124", "653"):
    assert not has_magic_rotation(t)
for a in range(1, 10):
    for b in range(a + 1, 10):
        for c in range(b + 1, 10):
            assert has_magic_rotation(f"{a}{b}{c}") == (a + c == 2 * b)

if __name__ == "__main__":
    for m in MAGIC:
        print(" / ".join(m))
    print("all assertions pass")
