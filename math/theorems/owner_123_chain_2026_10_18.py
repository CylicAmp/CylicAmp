# CLASS: AUDIT
"""
(1)23 chain (owner_work #328, 2026-10-18).

THE OWNER'S LINE, verbatim:
    (1)23=6+3=9+2=2+1=(3)

READING: (1)23 is 123 with its first digit in brackets (the 1 of "123=1" in the owner's seven rows, owner_work 2026-10-17). Each "=" is the next
  addition, written with its running digital root: 1+2+3 = 6; 6+3 = 9; 9+2 = 11, root 2; 2+1 = 3. The numbers added, 3, 2, 1, are the digits of 123
  read backwards -- and they are the digits moved to the front by the three rotations of the seven rows: 123 -> 312 moves the 3, 312 -> 231
  moves the 2, 231 -> 123 moves the 1. Every step holds; the line ends at (3).
  Forced part: 6 + (3 + 2 + 1) = 12 -> 3, the same as 123 + its reversal 321 = 444 -> 12 -> 3 (digit sums add).
  Forced means true for every number (digital roots add), nothing special to this line. Chosen by the owner, not forced: the order 3, 2, 1 and the
  bracket around the 1. No other person's work is involved; none was found. NOT SETTLED: whether the final (3) is meant as the 3 of "123 = 3" (the third
  turn of the rows); the line does not say.

FRAMEWORKS (gf37-audit): 123 SA_ST_A (12 mod 37); 444 = 12 x 37 -> 0, the SEAM; 321 SA_ST_A ... see the assertions.
FALSIFICATION: any assertion failing.
"""


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


digits = [1, 2, 3]
values = [sum(digits)]
for d in reversed(digits):
    values.append(dr(values[-1] + d))
assert values == [6, 9, 2, 3] and 6 + 3 == 9 and 9 + 2 == 11 and dr(11) == 2 and 2 + 1 == 3
rows = ["123", "312", "231", "123"]
assert [int(b[0]) for b in rows[1:]] == [3, 2, 1] and all(b == a[-1] + a[:-1] for a, b in zip(rows, rows[1:]))   # the digit moved to the front
assert [int(a[-1]) for a in rows[:3]] == list(reversed(digits)) == [3, 2, 1]
assert dr(6 + 3 + 2 + 1) == 3 and 123 + 321 == 444 and dr(444) == 3 and 444 == 12 * 37
assert 123 % 37 == 12 and 321 % 37 == 25 and 444 % 37 == 0

if __name__ == "__main__":
    print("(1)23 = 6, +3 = 9, +2 = 11 -> 2, +1 = (3): the added 3, 2, 1 are the digits moved by the three rotations of 123")
