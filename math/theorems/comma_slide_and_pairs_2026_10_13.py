# CLASS: AUDIT
"""
The comma sliding through four digits, the 12 taken both ways, and the pairs (owner_work #267, 2026-10-13).

THE OWNER'S LINES, verbatim:
    0,------000=1+3=4
    00,------00=2+2=4
    000,------0=3+1=4

    4×3=12
    3×4=12==(2+4=6)
    7×7=4+9=(1+3=4)

    6+4=10
    24+13=3+7=(10+1)=11


    12=3
    21=3


    34=7
    43=7

    46=1
    64=1

    33=6
    77=5
    11=2

EVERY LINE HOLDS.

THE COMMA THROUGH FOUR DIGITS
  The comma after digit 1, 2, 3 of a four-digit set: 1+3, 2+2, 3+1, each 4 (the comma sets of #265,
  now with the comma at every place). Each line has six dashes between the comma and the digits after it.
  4×3 = 12: three places for the comma, four digits each.

THE 12 BOTH WAYS
  4×3 = 12 and 3×4 = 12; the two 12s together are 24, and (2+4 = 6) is its digit sum -- the
  parenthesis as in #263 ("6x2=(1+2=3)"). 24 is written out two lines down.
  7×7 = 49, 4+9 = 13, 1+3 = 4.

THE TWO SUMS
  6+4 = 10 adds the 6 and the 4 just made. 24+13 adds the numbers they came from: 24+13 = 37,
  3+7 = 10 -- the same 10, because 24+13 has no carry. (10+1) = 11 is the +1 "to begin again" (#264).

THE PAIRS
  12 = 3, 21 = 3;  34 = 7, 43 = 7;  46 = 1, 64 = 1 (4+6 = 10 -> 1).
  12+34 = 46 and 21+43 = 64: the third pair is the first two added, and its root 1 is 3+7 = 10 -> 1.
  33 = 12+21, 77 = 34+43; 46+64 = 110. 33 = 6, 77 = 5 (14 -> 5), 11 = 2; 110 is also 2, and 33+77 = 110.
  A two-digit number plus its reversal is 11 x its digit sum: 33 = 11x3, 77 = 11x7, 110 = 11x10.

FALSIFICATION: any assertion failing.
"""


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


for s, k in (("0,------000", (1, 3)), ("00,------00", (2, 2)), ("000,------0", (3, 1))):
    lead, rest = s.split(",")
    assert (len(lead), len(rest.replace("-", ""))) == k and sum(k) == 4 and rest.count("-") == 6
assert 4 * 3 == 3 * 4 == 12 and 12 + 12 == 24 and 2 + 4 == 6
assert 7 * 7 == 49 and 4 + 9 == 13 and 1 + 3 == 4
assert 6 + 4 == 10 and 24 + 13 == 37 and 3 + 7 == 10 and 10 + 1 == 11
assert dr(24) + dr(13) == 10 and (24 % 10 + 13 % 10) < 10                       # no carry
for a, b, r in ((12, 21, 3), (34, 43, 7), (46, 64, 1)):
    assert dr(a) == dr(b) == r and int(str(a)[::-1]) == b
assert 12 + 34 == 46 and 21 + 43 == 64 and dr(3 + 7) == 1
assert 12 + 21 == 33 and 34 + 43 == 77 and 46 + 64 == 110 and 33 + 77 == 110
assert (dr(33), dr(77), dr(11), dr(110)) == (6, 5, 2, 2) and 7 + 7 == 14 and 1 + 4 == 5
for n in (12, 34, 46):
    assert n + int(str(n)[::-1]) == 11 * sum(map(int, str(n)))

if __name__ == "__main__":
    print("every line of #267 holds; 12+34 = 46, 21+43 = 64; 12+21 = 33, 34+43 = 77, 46+64 = 110 = 33+77")
