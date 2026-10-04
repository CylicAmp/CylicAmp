# CLASS: LEMMA
"""
Owner, 2026-10-04:
    23+6=2+9=11+5=16+16=3+2=5
    24+8=3+2=5+11=16+7=2+3=5

DECODED -- two lines run side by side and feed each other:
    step                         line 1             line 2
    start                        23                 24
    + product of its digits      23+2x3 = 29        24+2x4 = 32
    digit sum                    2+9 = 11           3+2 = 5
    add the other line           11+5 = 16          5+11 = 16
    line 1 doubles, line 2 adds its digit sum
                                 16+16 = 32         16+(1+6) = 23
    digit sum                    3+2 = 5            2+3 = 5
  (Reading "16+7" as 16 plus its own digit sum, 1+6 = 7.)

FORCED: the two lines always end on the same digital root. After meeting at
z, line 1 gives 2z and line 2 gives z + DS(z), and DS(z) = z mod 9. Checked on
every consecutive pair n, n+1 from 11 to 98 with no zero digit: 72 of 72.

SPECIAL TO 23, 24: line 2 ends on 23 -- line 1's own start -- for this pair
only, among all 72 pairs: the two lines close into a loop, 23 -> ... -> 23, like
the 832 chain closing on 8. Ending on the reversal pair 32 / 23 is common
(any pair whose lines meet at 16: 13/14, 26/27, 33/34, 43/44, ...); coming
back to the starting number is not.
23 and 29 are prime; (29, 31) is a twin-prime pair.

FALSIFICATION: any assertion below failing.
"""
from math import prod
from sympy import isprime

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def ds(n):
    return sum(map(int, str(n)))

def lines(n):
    m = n + 1
    x1, x2 = n + prod(map(int, str(n))), m + prod(map(int, str(m)))
    y1, y2 = ds(x1), ds(x2)
    z = y1 + y2
    return (x1, y1, z, 2 * z, ds(2 * z)), (x2, y2, z, z + ds(z), ds(z + ds(z)))

L1, L2 = lines(23)
assert L1 == (29, 11, 16, 32, 5) and L2 == (32, 5, 16, 23, 5)
PAIRS = [n for n in range(11, 99) if "0" not in str(n) + str(n + 1)]
assert len(PAIRS) == 72
assert all(dr(lines(n)[0][3]) == dr(lines(n)[1][3]) for n in PAIRS)
assert [n for n in PAIRS if lines(n)[1][3] == n] == [23]
assert isprime(23) and isprime(29) and isprime(31)

if __name__ == "__main__":
    print(L1, L2)
    print("all assertions pass")
