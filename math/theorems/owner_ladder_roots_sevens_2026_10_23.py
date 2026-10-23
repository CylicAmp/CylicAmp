# CLASS: COMPUTATION
"""
The owner's ladder 11 12 22 23 33 34 44 45 against the count 11 .. 18, the halves, and how many 7s reach 1+2=3
(owner_work #430, 2026-10-23). Process entry: owner_work/PROCESS.md, #430.

THE OWNER'S LINES, verbatim (#430):
    09=9
    1+0=10+1=11
    11=2=11+1=12
    12=3=12+1=
    22=4=13
    23=5=14
    33=6=15
    34=7=16
    44=8=17
    45=9=18


    09=9
    1+0=10÷2=5÷2=2.55.2
    11=2=11=2=20÷2÷10+10=2
    12=3=12=3=30
    22=4=13=4=40
    23=5=14=5=50
    33=6=15=6=60
    34=7=16=7=70
    44=8=17=8=80
    45=9=18=9=90



    5÷2=2.5
    2÷5=0.4
    7+7=14
    7×7=49


    7+7+7+7=2+8====1
    14+14+14+14=5+6=11

    21+21+21+21=
    28+28+28+28=
    35+35+35+35=

    lol how many 7s can I get at  count 1+2=3 exactly

    1=7777
    11=7777|7777

CLEANED:
    09 -> 0 + 9 = 9;   10 -> 10 + 1 = 11;   11 -> 2, 11 + 1 = 12;   12 -> 3, 12 + 1 = 13
    the ladder and the count, side by side, with their root:
      22 -> 4 = 13 -> 4    23 -> 5 = 14 -> 5    33 -> 6 = 15 -> 6    34 -> 7 = 16 -> 7
      44 -> 8 = 17 -> 8    45 -> 9 = 18 -> 9
    then each root with a 0 after it: 3 -> 30, 4 -> 40, ... 9 -> 90
    10 ÷ 2 = 5 -> 5 ÷ 2 = 2.5 -> 2.5 and 5.2 (written together as 2.55.2)
    11 -> 2 -> 20 -> 20 ÷ 2 = 10 -> 10 ÷ 10 = 1 -> 1 + 10 = 11 -> 2
    5 ÷ 2 = 2.5    2 ÷ 5 = 0.4    7 + 7 = 14    7 x 7 = 49
    7 + 7 + 7 + 7 = 28 -> 2 + 8 = 10 -> 1
    14 + 14 + 14 + 14 = 56 -> 5 + 6 = 11
    21 + 21 + 21 + 21 =        28 + 28 + 28 + 28 =        35 + 35 + 35 + 35 =
    1 = 7777        11 = 7777 | 7777        how many 7s reach 1 + 2 = 3 exactly?

PROCESS: count up from 09; next to the count, climb the ladder 11 12 | 22 23 | 33 34 | 44 45 (each double digit, then
one more); match each ladder step to the count with the same root; write the root with a 0; halve 10 twice; add 7s
four at a time and fold; ask how many 7s land on 1 + 2 = 3.

CHECKED:
    every line of the two ladders: right. The ladder and the count share the root because they are 9s apart:
      22 - 13 = 9, 23 - 14 = 9, 33 - 15 = 18, 34 - 16 = 18, 44 - 17 = 27, 45 - 18 = 27  (11 - 11 = 0, 12 - 12 = 0)
    roots with a 0 after them: 30 -> 3 ... 90 -> 9, right (a 0 adds nothing; with zero and without, the same root)
    10 ÷ 2 = 5, 5 ÷ 2 = 2.5 right; 2.5 read backwards is 5.2
    20 ÷ 2 = 10, 10 ÷ 10 = 1, 1 + 10 = 11 -> 2: right
    5 ÷ 2 = 2.5, 2 ÷ 5 = 0.4, 7 + 7 = 14, 7 x 7 = 49: right
    7 + 7 + 7 + 7 = 28 -> 10 -> 1 right;  14 + 14 + 14 + 14 = 56 -> 11 right
    the open lines:  21 x 4 = 84 -> 8 + 4 = 12 -> 1 + 2 = 3     28 x 4 = 112 -> 4     35 x 4 = 140 -> 5
      four of anything takes the root of 28 = 4 x 7 -> 1 each time: the k-th line lands on k (1, 2, 3, 4, 5)
    1 = 7777 (28 -> 10 -> 1) right; 11 = 7777|7777 (56 -> 5 + 6 = 11) right

THE QUESTION: twelve 7s, 7777|7777|7777 = 84 -> 8 + 4 = 12 -> 1 + 2 = 3 -- the next step after 1 = 7777 and
  11 = 7777|7777, and the first number of 7s whose total folds to exactly 12. Both ways:
    total exactly 12 (1 + 2):  12, 21, 39, 48, 66, ... sevens  (84, 147, 273, 336, 462, ...)
    root 3 (any total):        3, 12, 21, 30, 39, ... sevens -- every 9 more 7s from 3 (777 = 21 -> 3)

FRAMEWORKS (gf37-audit, 1/137): eight 7s, 77777777 = 7 x 11 x 73 x 101 x 137 = 137 x 567721: 137 divides every
  8-digit repdigit, because 1 ÷ 137 repeats every 8 digits (99999999 = 137 x 729927, repetend_998001_audit).
  7777 -> 7 D7 (= 7 x 11 x 101); 77777777 -> 3 C3; twelve 7s = 3 x 7 x 7 x 11 x 13 x 37 x 101 x 9901 -> 0;
  28 SA_ST_B, 56 -> 19 CAS_EXT, 84 -> 10 IC.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F

from sympy import factorint


def root(m):
    while m > 9:
        m = sum(map(int, str(m)))
    return m


assert root(9) == 9 and 10 + 1 == 11 and root(11) == 2 and 11 + 1 == 12 and root(12) == 3
ladder = [11, 12, 22, 23, 33, 34, 44, 45]
count = [11, 12, 13, 14, 15, 16, 17, 18]
assert [root(x) for x in ladder] == [root(x) for x in count] == [2, 3, 4, 5, 6, 7, 8, 9]
assert [a - b for a, b in zip(ladder, count)] == [0, 0, 9, 9, 18, 18, 27, 27]
assert all(root(10 * r) == r for r in range(1, 10))
assert F(10, 2) == 5 and F(5, 2) == F(5, 2) == F(25, 10) and str(2.5)[::-1] == "5.2"
assert F(20, 2) / 10 + 10 == 11 and root(11) == 2
assert (F(5, 2), F(2, 5), 7 + 7, 7 * 7) == (F(5, 2), F(2, 5), 14, 49)
assert 4 * 7 == 28 and root(28) == 1 and 4 * 14 == 56 and 5 + 6 == 11
fours = [4 * x for x in (7, 14, 21, 28, 35)]
assert fours == [28, 56, 84, 112, 140] and [root(v) for v in fours] == [1, 2, 3, 4, 5]
assert 8 + 4 == 12 and 1 + 2 == 3
assert root(int("7777")) == root(28) == 1 and sum(map(int, str(7 * 8))) == 11
assert 7 * 12 == 84 and sum(map(int, "84")) == 12
assert [k for k in range(1, 70) if sum(map(int, str(7 * k))) == 12] == [12, 21, 39, 48, 66]
assert [k for k in range(1, 40) if root(7 * k) == 3] == [3, 12, 21, 30, 39]
assert factorint(77777777) == {7: 1, 11: 1, 73: 1, 101: 1, 137: 1} and 77777777 == 137 * 567721
assert all(int(str(d) * 8) % 137 == 0 for d in range(1, 10)) and 99999999 == 137 * 729927
assert factorint(int("7" * 12)) == {3: 1, 7: 2, 11: 1, 13: 1, 37: 1, 101: 1, 9901: 1}
assert [x % 37 for x in (7777, 77777777, int("7" * 12), 28, 56, 84)] == [7, 3, 0, 28, 19, 10]

if __name__ == "__main__":
    print("#430: ladder and count share their roots (9s apart: 0 0 9 9 18 18 27 27); 4 x (7k) lands on k; "
          "twelve 7s = 84 -> 12 -> 1+2 = 3; eight 7s = 137 x 567721")
