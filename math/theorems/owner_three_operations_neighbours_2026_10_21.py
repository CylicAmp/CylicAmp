# CLASS: COMPUTATION
"""
The owner's three operations: a number with the one behind, with itself, with the one to its right
(owner_work #405, 2026-10-21). Process entry: owner_work/PROCESS.md, #405. Settles the two
readings asked in owner_three_neighbor_divisions_2026_10_21.py (#403).

THE OWNER'S LINES, verbatim (#405):
    There's three operations. If you're starting at the first number, you can only do two of those
    operations. One, use any arithmetic or math on yourself, the number you are at. And then you can
    do that to the number to your right, which for one would be the number two, because one only has
    two things that it can add up with, which is the two right by it. Now two, it can do three
    different things, because it can do now one, it can do itself, and now it can do three. Do you
    understand? Now, the reason why I say this, one, two, and three different operations, is because
    we can do each one by itself without the other. And this is where we get into more interesting
    things too. When we start mixing, like complex math, or multiplication, or division,

    (the message stops at "or division," -- the rest is missing, asked)

CLEANED (n is the number you are at; any arithmetic sign: + - x ÷):
    behind     n with n - 1
    yourself   n with n
    right      n with n + 1
    at 1:      yourself, right            (1 with 1, 1 with 2)        -> 2 operations
    at 2:      behind, yourself, right    (2 with 1, 2 with 2, 2 with 3) -> 3 operations
    each one can be done by itself, without the others; mixing comes after.

PROCESS: stand on a number; look at the places you can reach -- behind, yourself, right; the first
number has no one behind, so it has two; from 2 on there are three; do each one alone first.

SETTLED (#403 asked two readings):
    "you do" in 3 is n with each place, one at a time -- not one chain (n - 1) ÷ n ÷ (n + 1).
    The two-step is 1 and 2 by the same number: n ÷ (n + 1) and n ÷ (n - 1) (#403: "The number
    divides itself by the number in front of it ... The number divides itself by the number behind
    it. Then we combine those two"). The pasted pairing of #402, (n - 1) ÷ n and n ÷ (n - 1), is one
    pair of neighbours seen from both sides: 1's right (1 ÷ 2) and 2's behind (2 ÷ 1).

CHECKED, every sign, each operation by itself:
    at 1:   yourself  1+1 = 2   1-1 = 0   1x1 = 1   1÷1 = 1
            right     1+2 = 3   1-2 = -1  1x2 = 2   1÷2 = 0.5
    at 2:   behind    2+1 = 3   2-1 = 1   2x1 = 2   2÷1 = 2
            yourself  2+2 = 4   2-2 = 0   2x2 = 4   2÷2 = 1
            right     2+3 = 5   2-3 = -1  2x3 = 6   2÷3 = 0.666...

    for every n from 2 on (behind, yourself, right):
      +    2n - 1,  2n,  2n + 1          three numbers in a row, yourself in the middle
      -    1,  0,  -1                    the same three for every number
      x    n x n - n,  n x n,  n x n + n  steps of n, yourself in the middle
      ÷    n ÷ (n - 1),  1,  n ÷ (n + 1)  yourself is 1; the middle by flipping (#403)
    so with + - x, yourself sits exactly halfway between behind and right; with ÷ it does after a flip.

    adding: behind and right are the two odd numbers around 2n, so they are a twin pair when both
    are prime: 2 -> 3, 5   3 -> 5, 7   6 -> 11, 13   9 -> 17, 19 ... 69 -> 137, 139.
    From 2 to 99: 15 numbers give twin pairs.

COUNTS, both ways:
    operations at each place, line 1 to N:  1 -> 2,  2 to N - 1 -> 3,  N -> 2;  in all 3N - 2
      1 to 99: 2 + 97 x 3 + 2 = 295
    with zero (the line starts at 0): 0 -> 2, 1 -> 3 (0, itself, 2); 0 to 99: 3 x 100 - 2 = 298
      at 1 with zero, adding: 1+0 = 1, 1+1 = 2, 1+2 = 3 -> 1 2 3
    each by itself or mixed, choosing which operations to use:
      from 2 on   alone 3 + two at once 3 + all three 1 = 7;  with zero (choose none) 8
      at 1        alone 2 + both 1 = 3;                      with zero 4
    one sign for one operation: from 2 on 3 x 4 = 12 results; at 1 2 x 4 = 8.

RESIDUES mod 37 (gf37-audit): 1 IC, 2 DARK_A, 3 C3 (#403); 137 -> 26 IC, 139 -> 28 SA_ST_B.

MISSING: the rest of the message after "When we start mixing, like complex math, or
multiplication, or division," -- can I get it?

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F
from itertools import combinations
from sympy import isprime

SIGNS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "x": lambda a, b: a * b,
    "÷": lambda a, b: F(a, b),
}


def places(n, start=1, end=None):
    """the places n can reach on the line start .. end"""
    out = []
    if n - 1 >= start:
        out.append(("behind", n - 1))
    out.append(("yourself", n))
    if end is None or n + 1 <= end:
        out.append(("right", n + 1))
    return out


def results(n, start=1):
    return {(name, s): f(n, m) for name, m in places(n, start) for s, f in SIGNS.items()}


# --- at 1 and at 2 ---
assert [p for p, _ in places(1)] == ["yourself", "right"]
assert [p for p, _ in places(2)] == ["behind", "yourself", "right"] and [m for _, m in places(2)] == [1, 2, 3]
r1, r2 = results(1), results(2)
assert [r1[("yourself", s)] for s in "+-x÷"] == [2, 0, 1, 1]
assert [r1[("right", s)] for s in "+-x÷"] == [3, -1, 2, F(1, 2)]
assert [r2[("behind", s)] for s in "+-x÷"] == [3, 1, 2, 2]
assert [r2[("yourself", s)] for s in "+-x÷"] == [4, 0, 4, 1]
assert [r2[("right", s)] for s in "+-x÷"] == [5, -1, 6, F(2, 3)]
assert len(r1) == 8 and len(r2) == 12

# --- every n from 2 on ---
for n in range(2, 1000):
    r = results(n)
    b, y, rt = (lambda s: r[("behind", s)]), (lambda s: r[("yourself", s)]), (lambda s: r[("right", s)])
    assert (b("+"), y("+"), rt("+")) == (2 * n - 1, 2 * n, 2 * n + 1)
    assert (b("-"), y("-"), rt("-")) == (1, 0, -1)
    assert (b("x"), y("x"), rt("x")) == (n * n - n, n * n, n * n + n)
    assert (b("÷"), y("÷"), rt("÷")) == (F(n, n - 1), 1, F(n, n + 1))
    for s in "+-x":
        assert b(s) + rt(s) == 2 * y(s)                       # yourself exactly halfway
    assert 1 / b("÷") + 1 / rt("÷") == 2 * y("÷")              # halfway after a flip
    assert b("÷") + rt("÷") != 2 * y("÷")                      # not before

# --- the pasted pairing of #402 is one pair seen from both sides ---
assert all(results(n - 1)[("right", "÷")] * results(n)[("behind", "÷")] == 1 for n in range(3, 100))
assert results(1)[("right", "÷")] == F(1, 2) and results(2)[("behind", "÷")] == 2

# --- adding: twin pairs around 2n ---
twins = [n for n in range(2, 100) if isprime(2 * n - 1) and isprime(2 * n + 1)]
assert twins[:4] == [2, 3, 6, 9] and len(twins) == 15 and 69 in twins
assert (2 * 69 - 1, 2 * 69 + 1) == (137, 139)

# --- counts, both ways ---
def line_count(start, end):
    return sum(len(places(n, start, end)) for n in range(start, end + 1))


assert all(line_count(1, N) == 3 * N - 2 for N in range(2, 200))
assert line_count(1, 99) == 295 == 2 + 97 * 3 + 2
assert line_count(0, 99) == 298 == 3 * 100 - 2
assert [m for _, m in places(1, start=0)] == [0, 1, 2]
assert [1 + m for _, m in places(1, start=0)] == [1, 2, 3]

def mixes(k, with_zero):
    return sum(1 for r in range(0 if with_zero else 1, k + 1) for _ in combinations(range(k), r))


assert (mixes(3, False), mixes(3, True)) == (7, 8) and (mixes(2, False), mixes(2, True)) == (3, 4)
assert [sum(1 for _ in combinations(range(3), r)) for r in (1, 2, 3)] == [3, 3, 1]

# --- residues ---
assert [x % 37 for x in (1, 2, 3, 137, 139)] == [1, 2, 3, 26, 28]

if __name__ == "__main__":
    print("three operations: behind, yourself, right -- 2 at the first number, 3 from 2 on; "
          "+ gives 2n-1, 2n, 2n+1; - gives 1, 0, -1; x gives n²-n, n², n²+n; ÷ gives n/(n-1), 1, n/(n+1); "
          "yourself is halfway for + - x, and after a flip for ÷; line 1..N has 3N-2 operations; "
          "7 mixes from 2 on (8 with zero), 3 at 1 (4 with zero)")
