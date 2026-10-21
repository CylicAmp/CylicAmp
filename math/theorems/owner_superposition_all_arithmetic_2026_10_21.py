# CLASS: COMPUTATION
"""
The superposition: every basic sign at once, with each place -- left, yourself, right
(owner_work #407, 2026-10-21). Process entry: owner_work/PROCESS.md, #407.
Builds on owner_three_operations_neighbours_2026_10_21.py (#405, #406).

THE OWNER'S LINES, verbatim (#407):
    No, you do all basic arithmetic on, and that's the superposition of it. And then if you want
    to go down from there, like 1 plus 1 minus, you can do that.

CLEANED:
    superposition at n = all four signs at once, with every place n can reach:
        left       n + (n - 1)   n - (n - 1)   n x (n - 1)   n ÷ (n - 1)
        yourself   n + n         n - n         n x n         n ÷ n
        right      n + (n + 1)   n - (n + 1)   n x (n + 1)   n ÷ (n + 1)
    then "go down from there", like 1 plus 1 minus.

PROCESS: stand on a number; do + - x ÷ all together with each place; that set is the
superposition; then go down from it.

CHECKED:
    at 1 (yourself, right):      2 0 1 1  |  3 -1 2 0.5                    8 results, 6 different
    at 2 (left, yourself, right): 3 1 2 2  |  4 0 4 1  |  5 -1 6 0.666...   12 results, 9 different
    at 3:                         5 1 6 1.5 |  6 0 9 1  |  7 -1 12 0.75      12 results, 10 different
    from 4 on:                    12 results, 11 different, every time -- only 1 comes twice:
                                  n - (n - 1) = 1 and n ÷ n = 1
    where the rest of the repeats come from:
        2 + 2 = 2 x 2 = 4      x 1 and ÷ 1 give the same (1 x 1 = 1 ÷ 1, 2 x 1 = 2 ÷ 1)
        1 + 1 = 1 x 2 = 2      3 + 3 = 3 x 2 = 6
    why from 4 on: the x results n x n - n, n x n, n x n + n are above 2n + 1 (n x n - 3n - 1 > 0
    from n = 4); 0, 1, -1 are below 2n - 1; the two ÷ results n ÷ (n - 1) and n ÷ (n + 1) are not
    whole numbers (n shares no factor with n - 1 or n + 1) and are not equal.

    both ways, at 1 with zero (0 on the left): 12 slots, 1 ÷ 0 has no value -> 11 results,
        1+0 = 1, 1-0 = 1, 1x0 = 0 | 2 0 1 1 | 3 -1 2 0.5 -> 6 different, the same 6 as without zero.

    going down: from 4 signs, each next step gives 4 again -> 4, 16, 64, ... paths;
        up to 2 steps: 4 + 16 = 20; with zero (no step) 21.

Nothing is missing. "1 plus 1 minus" is the owner's example of an option ("if you want to go
down from there ... you can do that"); no check needs more than the message gives. A reply to
#407 labelled it missing and asked how it continues; that was wrong (#408), and is removed here.

RESIDUES mod 37: 1 IC, 2 DARK_A (#403).

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F


def superposition(n, start=1):
    """{(place, sign): value}; a ÷ by 0 has no value and is left out"""
    out = {}
    for place, m in [("left", n - 1), ("yourself", n), ("right", n + 1)]:
        if m < start:
            continue
        out[(place, "+")] = n + m
        out[(place, "-")] = n - m
        out[(place, "x")] = n * m
        if m != 0:
            out[(place, "÷")] = F(n, m)
    return out


def row(n, place, start=1):
    s = superposition(n, start)
    return [s[(place, g)] for g in "+-x÷" if (place, g) in s]


assert row(1, "yourself") == [2, 0, 1, 1] and row(1, "right") == [3, -1, 2, F(1, 2)]
assert "left" not in {p for p, _ in superposition(1)}
assert row(2, "left") == [3, 1, 2, 2] and row(2, "yourself") == [4, 0, 4, 1] and row(2, "right") == [5, -1, 6, F(2, 3)]
assert row(3, "left") == [5, 1, 6, F(3, 2)] and row(3, "yourself") == [6, 0, 9, 1] and row(3, "right") == [7, -1, 12, F(3, 4)]

counts = {n: (len(superposition(n)), len(set(superposition(n).values()))) for n in range(1, 5001)}
assert counts[1] == (8, 6) and counts[2] == (12, 9) and counts[3] == (12, 10)
assert all(counts[n] == (12, 11) for n in range(4, 5001))
for n in range(4, 5001):
    vals = list(superposition(n).values())
    assert [v for v in set(vals) if vals.count(v) > 1] == [1]
    assert n * n - 3 * n - 1 > 0 and F(n, n - 1).denominator > 1 and F(n, n + 1).denominator > 1

assert 2 + 2 == 2 * 2 == 4 and 1 * 1 == F(1, 1) and 2 * 1 == F(2, 1) and 1 + 1 == 1 * 2 and 3 + 3 == 3 * 2

z = superposition(1, start=0)
assert len(z) == 11 and [z[("left", g)] for g in "+-x"] == [1, 1, 0] and ("left", "÷") not in z
assert set(z.values()) == set(superposition(1).values()) and len(set(z.values())) == 6

paths = [4 ** k for k in range(1, 4)]
assert paths == [4, 16, 64] and 4 + 16 == 20 and 1 + 4 + 16 == 21

assert [x % 37 for x in (1, 2)] == [1, 2]

if __name__ == "__main__":
    print("superposition = + - x ÷ all at once with left, yourself, right: 8 results at 1 (6 different), "
          "12 at every n from 2 (9 at 2, 10 at 3, 11 from 4 on -- only 1 repeats: n-(n-1) = n÷n = 1)")
