# CLASS: AUDIT
"""
Audit of the pasted text "The operational mechanics behind these sequences, folds, and cyclic shifts" (owner_work #331, 2026-10-18).
Another tool's text, relayed by the owner with no words of their own. The owner's own lines it analyses (544/554/455, 188/277/772, 811/118,
4551|1554, 112(2)34|3, "121 drip 010", 101+131) are NOT in the record (it starts 2026-10-05): they came from sessions that were never recorded
or from another tool, and the paste does not quote them. So what follows checks the paste's arithmetic, not its reading of the owner.

FAULTS FIRST
  F1  "The outcome row 1, 1, 2, 2, 3, 4, 3 acts as an accumulator": no operation turning the column pairs (1,2) (3,1) (2,3) (1,2) (3,1) (2,3) (1,2)
      into that row is given (the formulas were lost in the paste), and the row is not non-decreasing (4 then 3), so it is not a running total
      of nonnegative terms. Not reproduced.
  F2  "121 -drip-> 010": 121 - 111 = 010 is right, but 010 is not "a flat repunit" (the repunit is the 111 that was subtracted), and "drip" here
      is not the owner's drip cycle as recorded (#228: each digit against every ordering of the digits).
  F3  "101 + 131 -> 3": 101 + 131 = 232, digit sum 7, 232 - 111 = 121, root 4 all hold; "7 = 3 (mod 4)" is true, but digital roots work mod 9,
      not mod 4, and the 3 is not derived from anything shown.
  F4  "confirming the algebraic stability of the 4551 | 1554 fold" overstates. What holds: 4551 = 37 x 123 and 1554 = 37 x 42, and since the
      middle digits are equal, 4551 - 1554 = 999 x 3 = 81 x 37, so one being a multiple of 37 forces the other. 4551 being one is the fact.

HOLDS
  Pair columns: the seven pairs are two period-3 rows, 1 3 2 1 3 2 1 over 2 1 3 2 1 3 2.
  544 -> 13 -> 4; 455 -> 14 -> 5; 554 - 455 = 99 = 9 x 11. 188 -> 17 -> 8; 277 -> 16 -> 7; 772 - 277 = 495 = 5 x 99. 811 - 118 = 693 = 7 x 99.
  Every such difference is a multiple of 99 -- FORCED: (100a + 10b + c) - (100c + 10b + a) = 99 (a - c). 9 x 99 = 891 is the case a - c = 9 (900 - 009).
  121 -> 4 after 232 - 111; 112(2)34 are the digits 1, 1, 2, 2, 3, 4, and with the 3 after the bar the row 1, 1, 2, 2, 3, 4, 3 (digit sum 16 -> 7).

COINCIDENCES (recorded, not claimed): 4551 = 3 x 37 x 41 = 37 x 123 and 1554 = 2 x 3 x 7 x 37 = 37 x 42, the owner's 123 and 42; 1122343 (the seven-digit
  row read as a number) = 43^2 x 607, the owner's 43. Which numbers count as the owner's is chosen after the fact.

FRAMEWORKS (gf37-audit): 4551, 1554 and 2997 are multiples of 37 (the seam); 891 C3; 232 IC; 1122343 NQR17.
FALSIFICATION: any assertion failing.
"""
from sympy import factorint


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


top, bottom = [1, 3, 2] * 2 + [1], [2, 1, 3] * 2 + [2]
assert list(zip(top, bottom)) == [(1, 2), (3, 1), (2, 3), (1, 2), (3, 1), (2, 3), (1, 2)]
row = [1, 1, 2, 2, 3, 4, 3]
assert any(b < a for a, b in zip(row, row[1:])) and sum(row) == 16 and dr(16) == 7
assert 121 - 111 == 10 and 111 == 3 * 37 and 101 + 131 == 232 and sum(map(int, "232")) == 7 and 232 - 111 == 121 and dr(121) == 4 and 7 % 4 == 3
assert [dr(n) for n in (544, 455, 188, 277)] == [4, 5, 8, 7] and [sum(map(int, str(n))) for n in (544, 455, 188, 277)] == [13, 14, 17, 16]
assert 554 - 455 == 99 == 9 * 11 and 772 - 277 == 495 == 5 * 99 and 811 - 118 == 693 == 7 * 99
assert all((100 * a + 10 * b + c) - (100 * c + 10 * b + a) == 99 * (a - c) for a in range(10) for b in range(10) for c in range(10))
assert 900 - 9 == 891 == 9 * 99 and 891 % 37 == 3
assert factorint(4551) == {3: 1, 37: 1, 41: 1} and 4551 == 37 * 123 and factorint(1554) == {2: 1, 3: 1, 7: 1, 37: 1} and 1554 == 37 * 42
assert 4551 - 1554 == 2997 == 81 * 37 == 3 * 999 and 4551 % 37 == 0 and 1554 % 37 == 0 and int("4551"[::-1]) == 1554
assert all((1000 * a + 100 * b + 10 * b + d) - (1000 * d + 100 * b + 10 * b + a) == 999 * (a - d) and 999 % 37 == 0 for a in range(1, 10) for b in range(10) for d in range(10))
assert factorint(1122343) == {43: 2, 607: 1} and 1122343 == 43 ** 2 * 607 and 1122343 % 37 == 22
assert int("".join(map(str, row))) == 1122343

if __name__ == "__main__":
    print("pasted folds audited: abc - cba = 99(a-c) is forced; 4551 = 37 x 123, 1554 = 37 x 42; the accumulator row, 'drip' and 'mod 4' claims are not supported")
