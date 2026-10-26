# CLASS: AUDIT
"""
The pasted 12 x 12 and 12 x 24 lattices (2026-10-26): rows A = 420244442024, B = 525735537525, C = 405515515504, in the
cycle A B C B three times; the 12 x 24 rows are each row written twice. Text from another tool, relayed by the owner.
Audit on arrival.

RIGHT, every layout: 12 rows; A, B, C have 12 digits; the cycle A B C B three times; the 12 x 24 rows are H H; the
  grid views carry the same digits as the strings.

NEW LINES:
  each row reads the same both ways: 420244 | 442024, 525735 | 537525, 405515 | 515504 -- a half and its flip
  (so H H is also H and its flip, and every 24-digit row reads the same both ways too)
  digit totals: A 32 -> 5, B 54 -> 9, C 40 -> 4; the 12 x 12 adds to 3 x 32 + 6 x 54 + 3 x 40 = 540 -> 9;
    the 12 x 24 to 1080 -> 9
  column totals of the 12 x 12: 54 18 45 63 33 57 57 33 63 45 18 54 -- the same both ways, all multiples of 3
    (each column is 3 A + 6 B + 3 C); roots 9 9 9 9 6 3 3 6 9 9 9 9
  each 12-digit row reads the same both ways with an even number of digits, so 11 divides it (the mirror rule, #374)
  by 37 (gf37-audit): A -> 20 DARK_A, B -> 28 SA_ST_B, C -> 15 DARK_A
  every 24-digit row H H = H x (10^12 + 1), and 10^12 + 1 = 73 x 137 x 99990001: so every row of the 12 x 24 is a
    multiple of 137 (and of 73) -- forced by writing the row twice (10001 = 73 x 137 is already in the repo)

FALSIFICATION: any assertion failing.
"""
from sympy import factorint

A, B, C = "420244442024", "525735537525", "405515515504"
rows12 = [A, B, C, B] * 3
rows24 = [h + h for h in rows12]
assert len(rows12) == 12 and all(len(r) == 12 for r in rows12) and all(len(r) == 24 for r in rows24)
grid = {"A": "4 2 0 2 4 4 4 4 2 0 2 4", "B": "5 2 5 7 3 5 5 3 7 5 2 5", "C": "4 0 5 5 1 5 5 1 5 5 0 4"}
assert grid["A"].replace(" ", "") == A and grid["B"].replace(" ", "") == B and grid["C"].replace(" ", "") == C
assert all(r == r[::-1] for r in rows12 + rows24)
assert [(h[:6], h[6:]) for h in (A, B, C)] == [("420244", "442024"), ("525735", "537525"), ("405515", "515504")]
digit = lambda s: sum(map(int, s))
root = lambda m: (m - 1) % 9 + 1
assert [digit(h) for h in (A, B, C)] == [32, 54, 40] and [root(digit(h)) for h in (A, B, C)] == [5, 9, 4]
assert sum(digit(r) for r in rows12) == 540 and sum(digit(r) for r in rows24) == 1080
cols = [sum(int(r[j]) for r in rows12) for j in range(12)]
assert cols == [54, 18, 45, 63, 33, 57, 57, 33, 63, 45, 18, 54] and cols == cols[::-1] and all(c % 3 == 0 for c in cols)
assert [root(c) for c in cols] == [9, 9, 9, 9, 6, 3, 3, 6, 9, 9, 9, 9]
assert all(int(h) % 11 == 0 for h in (A, B, C))
assert [int(h) % 37 for h in (A, B, C)] == [20, 28, 15]
assert factorint(10 ** 12 + 1) == {73: 1, 137: 1, 99990001: 1} and 10001 == 73 * 137
assert all(int(r) == int(r[:12]) * (10 ** 12 + 1) and int(r) % 137 == 0 and int(r) % 73 == 0 for r in rows24)

if __name__ == "__main__":
    print("lattice: every layout right; rows read the same both ways; totals 540 / 1080; every 24-digit row is 137 x ...")
