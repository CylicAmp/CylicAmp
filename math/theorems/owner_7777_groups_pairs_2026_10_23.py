# CLASS: COMPUTATION
"""
Groups of 7777, pairs folded to their roots, ways to write 4, counting to 7 by 2, and 148 split two ways
(owner_work #431, 2026-10-23). Process entry: owner_work/PROCESS.md, #431. The message repeats the lines of #430
first (owner_ladder_roots_sevens_2026_10_23.py); the new lines are below.

THE OWNER'S NEW LINES, verbatim (#431):
    1=7777
    11=7777|7777
    111=7777|7777|7777
    1111=7777|7777|7777|7777=3+1



    1=7777=55
    11=7777|7777=5555
    1=1414=55
    11=7777|7777=5555
    1=2828=11
    11=7777/7777=5555
    1=3535=88
    11=7777/7777=5555

    55+55=110+11=121+88=20+9=2+9=2


    1111=7777|7777|7777|7777=3+1
    or 2/2
    or 0.5×4×2=4
    or 43=7
    or 34=7


    counting to 7 by 2
    12
    34
    56
    7=at 7 in 4 count

    12+34+46+56=148=
    1+48=4+9=1+3=4
    14+8=2+2=4=3+1=4

CLEANED:
    1 -> 7777 (28 -> 1)        11 -> 7777 | 7777 (56 -> 11)        111 -> three groups (84 -> 12 -> 3)
    1111 -> four groups (112 -> 1 + 1 + 2 = 4 = 3 + 1)
    each pair folded to its root:  7777 -> 77 77 -> 14 14 -> 5 5 -> 55     7777|7777 -> 5555
                                   1414 -> 14 14 -> 5 5 -> 55     2828 -> 28 28 -> 10 10 -> 1 1 -> 11
                                   3535 -> 35 35 -> 8 8 -> 88
    55 + 55 = 110 -> 110 + 11 = 121 -> 121 + 88 = 209 -> 20 + 9 = 29 -> 2 + 9 = 11 -> 2
    4 = 3 + 1;  2/2;  0.5 x 4 x 2 = 4;  4 3 -> 4 + 3 = 7;  3 4 -> 3 + 4 = 7
    counting to 7 by 2: 1 2 -> 3 4 -> 5 6 -> 7: at 7 in 4 counts
    12 + 34 + 46 + 56 = 148 -> 1 | 48: 1 + 48 = 49 -> 4 + 9 = 13 -> 1 + 3 = 4
                            -> 14 | 8: 14 + 8 = 22 -> 2 + 2 = 4 = 3 + 1

PROCESS: count groups of four 7s with 1s (1, 11, 111, 1111); fold each group's pairs to their roots; add the folded
numbers; write 4 several ways; count to 7 in pairs; add, then split 148 two ways.

CHECKED:
    the groups: four 7s = 28 -> 1, eight = 56 -> 11 (-> 2), twelve = 84 -> 12 -> 3, sixteen = 112 -> 4 = 3 + 1: right.
      The k-th group lands on k, because four 7s = 28 -> 1.
    the folded pairs: 7777 -> 55, 7777|7777 -> 5555, 1414 -> 55, 2828 -> 11, 3535 -> 88: right
      (each pair to its root: 77 -> 14 -> 5, 14 -> 5, 28 -> 10 -> 1, 35 -> 8). Every one of these is a pair written
      twice, ab ab = ab x 101 (7777 = 77 x 101, 1414 = 14 x 101, ...), so its root is twice the pair's root.
    55 + 55 = 110, + 11 = 121, + 88 = 209 -> 2 + 0 + 9 = 11 -> 2: right (20 + 9 = 29 -> 11 -> 2 the same).
    3 + 1 = 4, 0.5 x 4 x 2 = 4, 4 + 3 = 7, 3 + 4 = 7: right.  2/2 as a division is 1; as 2|2 in the bars of #427 its
      total is 2 + 2 = 4 (both ways).
    counting to 7 by 2: 4 counts (1 2, 3 4, 5 6, 7): right.
    12 + 34 + 46 + 56 = 148: right as written; both splits fold to 4, and 148 -> 1 + 4 + 8 = 13 -> 4 (splitting
      changes nothing, #372). The pairs of the count to 7 are 12, 34, 56, 7: 46 is 12 + 34, the running total; with
      the pairs themselves 12 + 34 + 56 + 7 = 109 -> 10 -> 1.

FRAMEWORKS (gf37-audit): 148 = 4 x 37 -> 0 (the seam); 209 = 11 x 19 -> 24 SEED; 121 = 11 x 11 -> 10 IC;
  sixteen 7s = 7 x 11 x 17 x 73 x 101 x 137 x 5882353 -- 137 divides it (16 is two loops of 1 ÷ 137's 8).

FALSIFICATION: any assertion failing.
"""
from sympy import factorint


def root(m):
    while m > 9:
        m = sum(map(int, str(m)))
    return m


def fold_pairs(s):
    return "".join(str(root(int(s[i:i + 2]))) for i in range(0, len(s), 2))


groups = {g: int("7" * (4 * g)) for g in range(1, 5)}
assert [sum(map(int, str(v))) for v in groups.values()] == [28, 56, 84, 112]
assert [root(v) for v in groups.values()] == [1, 2, 3, 4] and 1 + 1 + 2 == 4 == 3 + 1
assert all(root(7 * 4 * g) == g for g in range(1, 9))
assert fold_pairs("7777") == "55" and fold_pairs("77777777") == "5555" and fold_pairs("1414") == "55"
assert fold_pairs("2828") == "11" and fold_pairs("3535") == "88"
assert all(int(ab * 2) == int(ab) * 101 and root(int(ab * 2)) == root(2 * root(int(ab))) for ab in ("77", "14", "28", "35"))
assert 55 + 55 == 110 and 110 + 11 == 121 and 121 + 88 == 209 and root(209) == 2 and 20 + 9 == 29 and root(29) == 2
assert 3 + 1 == 4 and 0.5 * 4 * 2 == 4 and 4 + 3 == 7 == 3 + 4 and 2 / 2 == 1 and 2 + 2 == 4
assert len(["12", "34", "56", "7"]) == 4
assert 12 + 34 + 46 + 56 == 148 and 1 + 48 == 49 and root(49) == 4 and 14 + 8 == 22 and root(22) == 4 == root(148)
assert 12 + 34 == 46 and 12 + 34 + 56 + 7 == 109 and root(109) == 1
assert 148 == 4 * 37 and 209 == 11 * 19 and 209 % 37 == 24 and 121 % 37 == 10
assert factorint(int("7" * 16)) == {7: 1, 11: 1, 17: 1, 73: 1, 101: 1, 137: 1, 5882353: 1}

if __name__ == "__main__":
    print("#431: groups of 7777 land on 1 2 3 4; pairs fold to 55 5555 55 11 88 (ab ab = ab x 101); 209 -> 2; "
          "148 = 4 x 37, both splits -> 4; with the count pairs 12+34+56+7 = 109 -> 1")
