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

THE WINDOW LINES (owner, 2026-10-04):
    24~62 = 6+8 = (1+(4 = 5) = 10 = 1
    46~24 = (1+(6 = 7) = 1+6 = 7+7 = 1+4 = 5
    62~46 = (8+(1 = 9) = 8+1+9 = 1+8 = 9
    795 new set of 3 / 861 / 618
  Reading 246 round its circle gives the two-digit windows 24, 46, 62 (digit
  sums 6, 10 -> 1, 8). Each line pairs a window with the one before it, adds
  the digit sums and reduces, then doubles:
    24~62: 6+8 = 14 -> 5, doubled 10 -> 1       (24 + 62 = 86 -> 5)
    46~24: 10+6 = 16 -> 7, doubled 14 -> 5      (46 + 24 = 70 -> 7)
    62~46: 8+10 = 18 -> 9, doubled 18 -> 9      (62 + 46 = 108 -> 9)
  New sets of three: the pair values 5, 7, 9 (795 is a rotation of 579) and the
  window roots 8, 6, 1 (861, 618: rotations of 186).
  5, 7, 9 is evenly spaced, so its rotation grid balances (centre 7, every line
  21). 1, 6, 8 is not, so no stacking of its rotations balances -- but 1+6+8 =
  15 and {1, 6, 8} is a line of the Lo Shu, the 3x3 magic square of 1..9
  (492/357/816), as is the doubled set {1, 5, 9}. The Lo Shu has 8 lines out of
  84 possible triples, so a triple landing on one is about 1 in 10.

MIXING (owner, 2026-10-04, first example): 33+53 = 8+6 = 1+4 = 5 -- the same
  5 as 24~62. 33 = 24 + 9 and 53 = 62 - 9: moving 9 from one number to the
  other keeps each digit sum (6 and 8) and the total (86), so the result is
  forced to repeat. (Owner's fuller account of mixing, "instead of 246 ...",
  still to come.)
  Owner's lists are both circles of each set: 795 -> 579 -> 957, and
  861 -> 186 -> 618 with the mirror circle 168 -> 816 -> 681 -- all six orders.

MIXING, THE OWNER'S RULE (2026-10-04): take 1 from one digit and give it to
  another. From 246: 156, 147 (from the 2); 336, 237 (from the 4); 345, 255
  (from the 6 -- written 346, 256: the 6 not lowered, a slip).
  KEPT: the digit sum, 12 -> 3, in every mix.
  THE NEW SET IS DIGITS + 3 (proved for every triple abc): the window-pair
  values are DR(digit sum + a), DR(digit sum + b), DR(digit sum + c), because
  ab + ca = 11a + b + 10c reduces to 2a + b + c. For 246 the sum is 12 -> 3, so
  2, 4, 6 become 5, 7, 9 -- the owner's 795. Mixing keeps the sum, so every mix
  of 246 also shifts by 3: 156 -> 4, 8, 9; 147 -> 4, 7, 1; 336 -> 6, 6, 9;
  237 -> 5, 6, 1; 345 -> 6, 7, 8; 255 -> 5, 8, 8.
  EVENLY SPACED SURVIVES ONLY END-TO-END: moving 1 between the two ends keeps
  the middle 4 and changes the step by one -- 147 (step 3) and 345 (step 1)
  stay evenly spaced, so their rotation grids still balance (centre 4, every
  line 12). Moving to or from the middle breaks it (156, 336, 237, 255).

MIX TO ONE NUMBER (owner: "we can do this until we only have 1 number left ...
  my way of showing why 2+4=6+6=(1+2=3)"): keep mixing until every slot but
  one is 0. Each move keeps the total, so the last slot always holds 12, and
  12 -> 1+2 = 3, whichever slot and in whatever order (2000 random routes: only
  0 0 12, 0 12 0, 12 0 0). It takes 6 moves into the 6's slot (2+4 units), 8
  into the 4's, 10 into the 2's. The owner's line is the route into the 6:
  2 goes into 4 -> 6, then 6 + 6 = 12 -> 3. This is why adding the digits and
  reducing gives the same answer as any amount of mixing: the total is the
  one thing mixing cannot change.

SIX AS FACTOR PAIRS (owner, 2026-10-04):
    6 = 33, 222, 111111   "two 3s, three 2s, six 1s"
    6 = 321, 123, 213     (3+2+1 = 6; 321 and 213 share a circle, 123 is in
                           the mirror circle -- all are orders of 1, 2, 3)
    2332 + (61 = 7) / 3223 / 2332 ;  3223 + (6+1 = 7) / 2332 / 3223
    167 / 716 / 671
  Each equal split of 6 is a count and a value with count x value = 6:
  two 3s = 23, three 2s = 32, six 1s = 61 (and one 6 = 16). Swapping count
  and value reverses the pair: 23 <-> 32, 61 <-> 16. 2332 and 3223 are a pair
  followed by its reverse -- even-length palindromes, so both divisible by 11
  (2332 = 11 x 212, 3223 = 11 x 293).
  61 -> 6+1 = 7: x 11 puts the digit sum in the middle, 61 x 11 = 671 = 6|7|1,
  and 16 x 11 = 176. 167, 671, 716 is one circle (the owner's list), and its
  mirror circle is 761, 617, 176. 167, 761 and 617 are prime. 167 is also the
  first value of prime_insertion_sequence_audit.py (1, 7 with 6 inserted).

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

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def ds(n):
    return sum(map(int, str(n)))

W = [int(w) for w in ("24", "46", "62")]
assert [ds(w) for w in W] == [6, 10, 8] and [dr(w) for w in W] == [6, 1, 8]
PAIRS = [(24, 62), (46, 24), (62, 46)]
V = [dr(ds(a) + ds(b)) for a, b in PAIRS]
assert V == [5, 7, 9] == [dr(a + b) for a, b in PAIRS]
assert [dr(2 * v) for v in V] == [1, 5, 9]
assert "795" in cycle("579", rot_r) and "861" in cycle("186", rot_r) and "618" in cycle("186", rot_r)
assert has_magic_rotation("579") and not has_magic_rotation("168")
LS = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
assert magic(LS)
LINES = [set(r) for r in LS] + [set(c) for c in zip(*LS)] + [{4, 5, 6}, {2, 5, 8}]
assert {1, 6, 8} in LINES and {1, 5, 9} in LINES and {5, 7, 9} not in LINES

assert (24 + 9, 62 - 9) == (33, 53) and 33 + 53 == 24 + 62 == 86
assert (ds(33), ds(53)) == (ds(24), ds(62)) == (6, 8) and dr(6 + 8) == 5
assert cycle("795", rot_l) == ["795", "957", "579"] and set(cycle("795", rot_r)) == {"795", "579", "957"}
assert set(cycle("861", rot_r)) | set(cycle("168", rot_r)) == {"".join(p) for p in permutations("168")}

def mixes(t):
    out = []
    for i in range(3):
        for j in range(3):
            if i != j:
                d = list(map(int, t))
                d[i] -= 1
                d[j] += 1
                out.append("".join(map(str, d)))
    return out

MIX = mixes("246")
assert MIX == ["156", "147", "336", "237", "345", "255"]
assert all(sum(map(int, m)) == 12 for m in MIX)
def new_set(t):
    a, b, c = map(int, t)
    return [dr((10 * a + b) + (10 * c + a)), dr((10 * b + c) + (10 * a + b)), dr((10 * c + a) + (10 * b + c))]
assert new_set("246") == [5, 7, 9]
for m in MIX:
    assert new_set(m) == [dr(int(x) + 3) for x in m]
from itertools import product
for a, b, c in product(range(10), repeat=3):
    t = f"{a}{b}{c}"
    assert new_set(t) == [dr(a + b + c + x) for x in (a, b, c)]
assert [m for m in MIX if has_magic_rotation(m)] == ["147", "345"]

import random
_rng = random.Random(5)
ENDS = set()
for _ in range(2000):
    d, tgt, n = [2, 4, 6], _rng.randrange(3), 0
    while sum(x > 0 for x in d) > 1:
        i = _rng.choice([k for k in range(3) if k != tgt and d[k] > 0])
        d[i] -= 1
        d[tgt] += 1
        n += 1
        assert sum(d) == 12
    assert n == 12 - [2, 4, 6][tgt]
    ENDS.add(tuple(d))
assert ENDS == {(0, 0, 12), (0, 12, 0), (12, 0, 0)} and dr(12) == 3 == dr(2 + 4 + 6)

from sympy import isprime
assert sorted([("321" in cycle("123", rot_r)), ("213" in cycle("321", rot_r))]) == [False, True]
assert [(c, 6 // c) for c in (1, 2, 3, 6)] == [(1, 6), (2, 3), (3, 2), (6, 1)]
assert 2332 == 11 * 212 and 3223 == 11 * 293 and "2332" == "23" + "32" and "3223" == "32" + "23"
assert 61 * 11 == 671 and 16 * 11 == 176 and 6 + 1 == 7
assert set(cycle("167", rot_r)) == {"167", "716", "671"} and set(cycle("761", rot_r)) == {"761", "617", "176"}
assert [x for x in (167, 716, 671, 761, 617, 176) if isprime(x)] == [167, 761, 617]

if __name__ == "__main__":
    for m in MAGIC:
        print(" / ".join(m))
    print("all assertions pass")
