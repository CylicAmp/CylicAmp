# CLASS: LEMMA
"""
The owner's infinite growth cycle and "forever numbers" (2026-10-04):
    "I continuously add the missing numbers in between that create a space for
     new gaps that need to be filled in"
    246
    23456
    213141516        "after 3 we get ones"
    2123213431454156 "make sure I did right"
    0 / 00 / 000 / 0000 = double
    "forever numbers that never stop but create patterns we can reflect":
    8+8 = 1+6 = 7
Prior work nearby (different operations): zero_fill_bridge_audit.py (filling
0-spaces), prime_insertion_sequence_audit.py (inserting into the 1-7 gap),
open_closed_grid_theorem.py (sequential filling), palindrome_diamond_audit.py.

THE TWO MOVES (decoded from the owner's lines, and they reproduce them exactly):
  FILL: in every gap of 2 or more between neighbours, put the number next to
        the larger end:   2 4 6 -> 2 3 4 5 6;
        2 1 3 1 4 1 5 1 6 -> 2 1 2 3 2 1 3 4 3 1 4 5 4 1 5 6   (the owner's line: CORRECT)
  ONES: when no gaps are left, put a 1 between every pair:
        2 3 4 5 6 -> 2 1 3 1 4 1 5 1 6   ("after 3 we get ones")
  The ones open new gaps (1 next to 3, 4, 5, 6), FILL closes them, ONES opens
  more -- the cycle never ends. FILL repeated until no gaps gives the full
  staircase 2123212343212345432123456 (the same as inserting every missing
  number at once), then ONES doubles it (length L -> 2L - 1).

GROWTH -> DOUBLING ("= double"): gap-free lengths after each cycle
    5, 25, 93, 281, 741, 1785, 4045, 8793, 18581, 38521
  ratios 5.0, 3.72, 3.02, 2.64, 2.41, 2.27, 2.17, 2.11, 2.07 -> approaching 2.
  L(next) - 2L = 15, 43, 95, 179, 303, 475, 703, 995, 1359: its third
  differences are constant (8) over these nine cycles, so the excess over
  doubling grows only like a cubic while the length doubles -- the ratio
  tends to 2. (Computed for nine cycles; the limit is read from the
  pattern, not proved.)

FOREVER NUMBERS: 8+8 = 16 -> 1+6 = 7 is one step of doubling under the
digital root: 1 -> 2 -> 4 -> 8 -> 7 -> 5 -> 1, repeating every 6 forever and
never touching 3, 6, 9 (the doubling set {1,2,4,5,7,8} of cipher_123_1234.py).
Run backwards it is halving: 7 -> 8 -> 4 -> 2 -> 1 -> 5 -> 7 (halving is x5 mod 9).

FALSIFICATION: any assertion below failing.
"""
def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def fill(s):
    out = [s[0]]
    for a, b in zip(s, s[1:]):
        if abs(a - b) >= 2:
            out.append(max(a, b) - 1)
        out.append(b)
    return out

def fill_all(s):
    out = [s[0]]
    for a, b in zip(s, s[1:]):
        st = 1 if b > a else -1
        out += list(range(a + st, b, st))
        out.append(b)
    return out

def ones(s):
    out = [s[0]]
    for b in s[1:]:
        out += [1, b]
    return out

def show(s):
    return "".join(map(str, s))

s1 = fill([2, 4, 6])
s2 = ones(s1)
s3 = fill(s2)
assert (show(s1), show(s2), show(s3)) == ("23456", "213141516", "2123213431454156")

s = s3
while fill(s) != s:
    s = fill(s)
assert show(s) == show(fill_all(s2)) == "2123212343212345432123456"

s, done = [2, 3, 4, 5, 6], [5]
for _ in range(9):
    t = ones(s)
    assert len(t) == 2 * len(s) - 1
    s = t
    while fill(s) != s:
        s = fill(s)
    done.append(len(s))
assert done == [5, 25, 93, 281, 741, 1785, 4045, 8793, 18581, 38521]
ex = [done[i + 1] - 2 * done[i] for i in range(len(done) - 1)]
d = ex
for _ in range(3):
    d = [d[i + 1] - d[i] for i in range(len(d) - 1)]
assert d == [8] * len(d)
assert [round(done[i + 1] / done[i], 2) for i in range(len(done) - 1)][-1] == 2.07

assert 8 + 8 == 16 and dr(16) == 7
assert [dr(2 ** k) for k in range(7)] == [1, 2, 4, 8, 7, 5, 1]
assert all(dr(2 * x) in (1, 2, 4, 5, 7, 8) for x in (1, 2, 4, 5, 7, 8))
assert [dr(5 * x) for x in (7, 8, 4, 2, 1, 5)] == [8, 4, 2, 1, 5, 7]

if __name__ == "__main__":
    print(show(s1), show(s2), show(s3))
    print("gap-free lengths:", done)
    print("all assertions pass")
