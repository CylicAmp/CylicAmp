# CLASS: COMPUTATION
"""
67(7)76: the owner's chains on 6 7 7 7 6, and the pasted analysis of it (owner_work #429, 2026-10-23).
Process entry: owner_work/PROCESS.md, #429.

THE OWNER'S LINES, verbatim (#429, after the pasted block; the "now tie back to" lines come twice in the message):
    now tie back to

    67(7)76=

    6+7=1+3=4+7=1+1=2+7=9+6=1+5=6

    or
    1+3=4+7=1+1=2+1=3+3=6

    (2+7)+6=2+(7+6).

    6|777|6
    6+21=2+7=9+6=1+5=6

    13+7=20+13=3+3=6

    434

CLEANED:
    6 + 7 = 13 -> 1 + 3 = 4 -> 4 + 7 = 11 -> 1 + 1 = 2 -> 2 + 7 = 9 -> 9 + 6 = 15 -> 1 + 5 = 6
    13 -> 1 + 3 = 4 -> 4 + 7 = 11 -> 1 + 1 = 2 -> 2 + 1 = 3 -> 3 + 3 = 6      (the second 13 taken as its digits 1, 3)
    (2 + 7) + 6 = 2 + (7 + 6)
    6 | 777 | 6:  7 + 7 + 7 = 21;  6 + 21 = 27 -> 2 + 7 = 9 -> 9 + 6 = 15 -> 1 + 5 = 6
    13 + 7 = 20 -> 20 + 13 = 33 -> 3 + 3 = 6
    434

PROCESS: read 67(7)76 digit by digit and fold after every step; read it again as 13 | 7 | 13 with the second 13 split
into its digits; check that the grouping of the last steps does not matter; read it as 6 | 777 | 6; read it as
13 + 7 + 13.

CHECKED:
    6 7 7 7 6, folded at every step: 6 -> 4 -> 2 -> 9 -> 6   right
    13 | 7 | 13 with the second 13 as 1, 3: 4 -> 2 -> 3 -> 6   right
    (2 + 7) + 6 = 9 + 6 = 15 and 2 + (7 + 6) = 2 + 13 = 15: right -- the same 15, both -> 6
    6 | 777 | 6: 6 + 21 = 27 -> 9, 9 + 6 = 15 -> 6   right
    13 + 7 + 13 = 33 -> 6   right
    every path ends on 6, because all of them add the same five digits: 6 + 7 + 7 + 7 + 6 = 33 -> 6
    434: 4 + 3 + 4 = 11 -> 2; it reads the same both ways like 67776. What 434 is taken from is not in the lines.

TIED TO THE WORK:
    67 and 76 are flips (#358): a flip moves a number by a multiple of 9 (76 - 67 = 9), so both have the same total,
      13 -> 4. That is why the mirror half adds the same as the first half.
    67(7)76 is the mirror of #374 with a center: 67, then 7, then 67 read backwards.
    6|777|6 is in the bars of #427: 5 digits, an odd length, so a digit sits in the center -- 7.
    the chains use "=" to carry forward (#410): 6+21=2+7 is 6 + 21 = 27 written as its digits.

THE PASTE, re-run: 67776 as a number; the running sums 6 13 20 27 33; the folded path 6 4 2 9 6; 13 + 7 + 13 = 33;
  outside in 6 + 6 = 12 -> 3, 7 + 7 = 14 -> 5, 3 + 5 + 7 = 15 -> 6; every grouping ends on 6 -- all right.
  (Its "Earlier, you had forms such as 141(777)141, 14516(21)14516, 56(3)56, 2(3)2" refers to work that is not in
  owner_work/ before this message.)

RESIDUES mod 37 (gf37-audit): 67776 -> 29 C9 (= 2^6 x 3 x 353); 67 -> 30 C3 (prime); 76 -> 2 DARK_A; 33 D7;
  434 -> 27 NEG_H (= 2 x 7 x 31).

FALSIFICATION: any assertion failing.
"""
from itertools import accumulate

from sympy import factorint, isprime


def root(m):
    while m > 9:
        m = sum(map(int, str(m)))
    return m


def fold_each(steps):
    out, cur = [], 0
    for s in steps:
        cur = root(cur + s)
        out.append(cur)
    return out


d = [6, 7, 7, 7, 6]
assert int("".join(map(str, d))) == 67776 and str(67776) == str(67776)[::-1]
assert fold_each(d) == [6, 4, 2, 9, 6]
assert list(accumulate(d)) == [6, 13, 20, 27, 33] and root(33) == 6
assert fold_each([13, 7, 1, 3]) == [4, 2, 3, 6]
assert (2 + 7) + 6 == 2 + (7 + 6) == 15 and root(15) == 6
assert 7 + 7 + 7 == 21 and 6 + 21 == 27 and root(27) == 9 and 9 + 6 == 15 and root(15) == 6
assert 13 + 7 == 20 and 20 + 13 == 33 and root(33) == 6
assert root(6 + 6) == 3 and root(7 + 7) == 5 and root(3 + 5 + 7) == 6
assert 4 + 3 + 4 == 11 and root(11) == 2 and str(434) == str(434)[::-1]
assert 76 - 67 == 9 and sum(map(int, "67")) == sum(map(int, "76")) == 13 and root(13) == 4
assert "67" + "7" + "67"[::-1] == "67776"
assert factorint(67776) == {2: 6, 3: 1, 353: 1} and factorint(434) == {2: 1, 7: 1, 31: 1} and isprime(67)
assert [x % 37 for x in (67776, 67, 76, 33, 434)] == [29, 30, 2, 33, 27]

if __name__ == "__main__":
    print("#429: every chain right -- 6 4 2 9 6, 4 2 3 6, (2+7)+6 = 2+(7+6) = 15, 6|777|6 -> 6, 13+7+13 = 33 -> 6; "
          "all add the same five digits (33); 67 and 76 are flips, 9 apart, both 13")
