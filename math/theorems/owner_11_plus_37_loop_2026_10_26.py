# CLASS: COMPUTATION
"""
1|1 + 37 and the loop 1)(1 + 3 + 7 (owner_work #442, 2026-10-26). Process entry: owner_work/PROCESS.md, #442.

THE OWNER'S LINES, verbatim (#442):
    1|1+37=4+8=1+2=3

    1)(1+3=4+7=1)(1+3=4+7=1)(1+3=4+7=1)(1

CLEANED:
    11 + 37 = 48 -> 4 + 8 = 12 -> 1 + 2 = 3
    1)(1 -> 1 + 3 = 4 -> 4 + 7 = 11 = 1)(1 -> 1 + 3 = 4 -> 4 + 7 = 11 = 1)(1 -> 1 + 3 = 4 -> 4 + 7 = 11 = 1)(1
    (here 1|1 and 1)(1 are both 11 written with a mark between its two 1s)

PROCESS: add 37 to 11 and fold; then add 37 digit by digit -- the 3, then the 7 -- to 1, reach 11, split it into its
two 1s at the bracket, and start again from the second 1; three times.

CHECKED:
    11 + 37 = 48 -> 12 -> 3: right
    1 + 3 = 4, 4 + 7 = 11: right, every loop; 3 + 7 = 10, so each loop is 1 -> 1 + 10 = 11
    the two lines are one move: +37 in line 1, +3 then +7 in line 2 (37's digits)
    adding 37 adds 1 to the root (37 -> 3 + 7 = 10 -> 1): 11 (root 2) + 37 = 48 (root 3)
    both ways: starting again from the second 1 each loop (the owner's way): 1 -> 4 -> 11, three times;
      carrying the whole total instead: 1 -> 4 -> 11 -> 14 -> 21 -> 24 -> 31, roots 1 4 2 5 3 6 4 --
      each full loop adds 10, one more on the root
    the line holds 4 brackets )( and 3 loops

RESIDUES (gf37-audit): adding 37 leaves the remainder by 37 the same: 11 -> 11 and 48 -> 11, both NEG_H; 11 is prime,
  twin with 13.

FALSIFICATION: any assertion failing.
"""


def root(m):
    while m > 9:
        m = sum(map(int, str(m)))
    return m


assert 11 + 37 == 48 and 4 + 8 == 12 and 1 + 2 == 3 and root(48) == 3
assert 1 + 3 == 4 and 4 + 7 == 11 and 3 + 7 == 10
line = "1)(1+3=4+7=1)(1+3=4+7=1)(1+3=4+7=1)(1"
assert line.count(")(") == 4 and line.count("+3=4+7=") == 3
assert root(37) == 1 and root(11) == 2 and all(root(n + 37) == root(n) % 9 + 1 for n in range(1, 2000))
carry = [1]
for step in (3, 7, 3, 7, 3, 7):
    carry.append(carry[-1] + step)
assert carry == [1, 4, 11, 14, 21, 24, 31] and [root(v) for v in carry] == [1, 4, 2, 5, 3, 6, 4]
assert 11 % 37 == 48 % 37 == 11

if __name__ == "__main__":
    print("11 + 37 = 48 -> 3 right; 1 + 3 + 7 = 11 each loop right; +37 adds 1 to the root and nothing by 37")
