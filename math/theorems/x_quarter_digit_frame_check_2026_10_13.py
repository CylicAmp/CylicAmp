# CLASS: AUDIT
"""
Check of the "rational -> algebraic -> transcendental" summary (owner_work #256, 2026-10-13),
built on x^(x^x) = (1/2)^sqrt2, x = 1/4 (pickover_tetration_x_quarter_2026_10_13.py) and the
0.25 drip cycle (owner_work/drip_cycle.md).

HOLDS
  x = 0.25 -> 2+5 = 7.  232 -> 7.  6+1 = 7.  3+4 = 7.  7x3 = 21, 3x4 = 12, 9+12 = 21,
  12+21 = 33 -> 6.  171 = 9 x 19 = 3^2 x 19; (1)+71 = 72 -> 9 and 17+1 = 18 -> 9 (forced: 171 is a
  multiple of 9, so every split of its digits sums to a multiple of 9).  23/6 = 3.8333...
  Table rows: 5,7,9,11 = [0,23,6] (0+2+3+6 = 11); 6,8,10,17,19,21 = [0,1]; 16,18,20 = [0,36],
  [0,66], [0,99] (9, 12, 18); 22 = [12] (3); [6,1,7] sums to 14.
NEEDS A STATED CUT
  x^x = 1/sqrt2 = 0.70710678... and x^(x^x) = 2^-sqrt2 = 0.37521422... are irrational: their digits
  never end, so they have no single digit sum. The stated 6 and 8 hold at 4 decimal places
  (0.7071 -> 15 -> 6; 0.3752 -> 17 -> 8) and change at other lengths (1/sqrt2: 7,7,5,6,6,3,1,9,...;
  2^-sqrt2: 3,1,6,8,9,4,6,8,...). Same 4-place cut for both, so the climb 7 -> 6 -> 8 is
  consistent at that cut.
CORRECTIONS
  "Rows 25, 26 carry [6,1,7]": rows 25, 26 AND 27 -- the owner wrote 6+1=7 three times.
  "23/6 four times, then +1": the lines alternate -- 01, then 00=23/6 four times with 0=+1
  between them (three +1 lines), not +1 after the fourth.
  "growth table": these rows are plug.py's "numbers in each line" table for message #255 (row =
  line number), not the growth run; and its 0 entries are the owner's 00, read as 0.
NOT IN THE RECORD
  232 and 171 appear in no owner message before #256; the arithmetic on them holds.
FOUND WHILE CHECKING
  23/6 = 3.8333...: the digital roots of its truncations run 3, 2, 5, 8, 2, 5, 8, ... -- the repeating
  3 adds 3 each digit, so they cycle through {2, 5, 8}; +1 sends {2, 5, 8} to {3, 6, 9}.

FALSIFICATION: any assertion failing.
"""
from decimal import Decimal, getcontext

getcontext().prec = 60


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def droots(v, k):
    s = format(v, "f").replace(".", "")[1:] if v < 1 else format(v, "f").replace(".", "")
    return [dr(sum(map(int, s[:j]))) for j in range(1, k + 1)]


assert sum(map(int, "25")) == 7 and sum(map(int, "232")) == 7 and 6 + 1 == 7 == 3 + 4
assert 7 * 3 == 21 and 3 * 4 == 12 and 9 + 12 == 21 and dr(12 + 21) == 6
assert 171 == 9 * 19 == 3 ** 2 * 19 and dr(1 + 71) == 9 == dr(17 + 1)
assert all((int("171"[:i]) + int("171"[i:])) % 9 == 0 for i in (1, 2))
r2, t = Decimal(1) / Decimal(2).sqrt(), Decimal(2) ** (-Decimal(2).sqrt())
assert str(r2)[:6] == "0.7071" and str(t)[:6] == "0.3752"
assert droots(r2, 8) == [7, 7, 5, 6, 6, 3, 1, 9] and droots(t, 8) == [3, 1, 6, 8, 9, 4, 6, 8]
assert droots(r2, 4)[-1] == 6 and droots(t, 4)[-1] == 8                     # the 4-place cut
q = Decimal(23) / Decimal(6)
lad = droots(q, 11)
assert lad[:2] == [3, 2] and lad[2:] == [5, 8, 2, 5, 8, 2, 5, 8, 2]           # cycle {2,5,8}
assert {dr(v + 1) for v in (2, 5, 8)} == {3, 6, 9}
assert sum([0, 23, 6], 0) == 29 and sum(map(int, "0236")) == 11 and 6 + 1 + 7 == 14

if __name__ == "__main__":
    print("holds; 6 and 8 need the 4-place cut; rows 25-27; 23/6 roots cycle 2,5,8 -> +1 -> 3,6,9")
