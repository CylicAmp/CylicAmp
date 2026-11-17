# CLASS: COMPUTATION
"""
The owner's lines (2026-11-17), quoted as written:

    "0|505|150|150|
     continue if
     15+15=6,6,12,30
     5151        5151        5151
     1515        1515        1515
     6666        5151        5151
                 2727        1515
                             3333 or 12121212=4+6=10
     01
     005
     01"

CLEANED, each step checked:
    blocks 0 | 505 | 150 | 150 : roots 0, 1, 6, 6
    15 + 15 = 30;  15 -> 6, 15 -> 6, 6 + 6 = 12;  12 -> 3 and 30 -> 3 agree, so continue      right
    add the rows down each column, keeping the column's root:
      5151 + 1515                  columns 6 6 6 6        -> 6666                            right
      5151 + 1515 + 5151           columns 11 7 11 7      -> 2 7 2 7 = 2727                  right
      5151 + 1515 + 5151 + 1515    columns 12 12 12 12    -> 3333, or unreduced 12121212     right
      "12121212 = 4 + 6 = 10": which numbers 4 and 6 are is not in the lines (the digits of 12121212 add to 12:
        four 1s and four 2s) -- missing, asked
    01 / 005 / 01: the zero frame 0, 00, 0 with 1, 5, 1 -- 151, prime (the V6 ledger's lemma 4)

BOTH WAYS: 0|505|150|150| has 10 digits with the zeros, 6 without; its digits add to 22 -> 4 either way; 4 blocks
  with the 0 block, 3 without; the blocks add to 805 -> 13 -> 4 either way.

CONTINUED (the owner's "continue"): 5 rows -> 8484, 6 rows -> 9999, 7 rows -> 5151 again: the stack repeats every 6
  rows, because each pair of rows adds 6 to every column and three pairs add 18 (root 9). The even stacks give
  6666, 3333, 9999 -- the owner's 6, 3, 9.

FORCED: every four-digit row is ab x 101 (5151 = 51 x 101, 1515, 6666, 2727, 3333 all multiples of 101); and
  12121212 = 12 x 1010101 = 2^2 x 3 x 73 x 101 x 137 (1010101 = 101 x 10001, 10001 = 73 x 137, already in the repo).
gf37-audit: 5151 -> 8 by 37 (TESLA), 2727 -> 26 (IC), 3333 -> 3 (C3), 12121212 -> 12 (SA_ST_A); 151 -> 3.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime


def root(n):
    return 1 + (n - 1) % 9 if n else 0


def stack(r):
    rows = ["5151" if i % 2 == 0 else "1515" for i in range(r)]
    cols = [sum(int(row[c]) for row in rows) for c in range(4)]
    return cols, "".join(str(root(c)) for c in cols)


assert [root(b) for b in (0, 505, 150, 150)] == [0, 1, 6, 6]
assert 15 + 15 == 30 and root(15) == 6 and 6 + 6 == 12 and root(12) == root(30) == 3

assert stack(2) == ([6, 6, 6, 6], "6666") and 5151 + 1515 == 6666
assert stack(3) == ([11, 7, 11, 7], "2727")
assert stack(4) == ([12, 12, 12, 12], "3333") and "".join(map(str, stack(4)[0])) == "12121212"
assert sum(map(int, "12121212")) == 12 and "12121212".count("1") == "12121212".count("2") == 4

assert isprime(151) and int("1" + "5" + "1") == 151

s = "0505150150"
assert len(s) == 10 and len(s.replace("0", "")) == 6 and sum(map(int, s)) == 22 and root(22) == 4
assert 0 + 505 + 150 + 150 == 805 and root(805) == 4

assert [stack(r)[1] for r in range(1, 13)] == ["5151", "6666", "2727", "3333", "8484", "9999"] * 2
assert [stack(r)[1] for r in (2, 4, 6)] == ["6666", "3333", "9999"]

for n in (5151, 1515, 6666, 2727, 3333):
    assert n % 101 == 0
assert 12121212 == 12 * 1010101 and factorint(12121212) == {2: 2, 3: 1, 73: 1, 101: 1, 137: 1}
assert (5151 % 37, 2727 % 37, 3333 % 37, 12121212 % 37, 151 % 37) == (8, 26, 3, 12, 3)

if __name__ == "__main__":
    print("6666, 2727, 3333 / 12121212 right; the stack repeats every 6 rows: 5151 6666 2727 3333 8484 9999")
