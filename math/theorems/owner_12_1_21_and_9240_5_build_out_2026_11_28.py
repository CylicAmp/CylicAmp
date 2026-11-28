# CLASS: AUDIT
"""
The owner's lines of 2026-11-28, built out the way the owner taught the build out of 181 (#270: split it up and down,
add, take the root; halve the odd into equal halves, "equal odds compress", 1 / 2 = 0.5 + 0.5 = 1; read the mirror).

THE OWNER'S LINES, verbatim:
    1)12|1|21(8
    9240.5|5.0429
    build out how I taught

CLEANED (readings marked; each checked):
    1 → 12 | 1 | 21 → (8)        a number, a centre, its flip: 12 | 1 | 21 = 12121
    9240.5 | 5.0429             a number and its mirror (5.0429 is 9240.5 read backwards)

BUILD OUT, LINE 1:
    12 | 1 | 21 joined = 12121 = the owner's (1)2(1)2(1) of #259 = 17 x 23 x 31
    up:   12 + 1 + 21 = 34 → 3 + 4 = 7
    with the 1 in front: 1 + 12 + 1 + 21 = 35 → 3 + 5 = 8      (reading: the (8) is this result)
          digits 1 + 1 + 2 + 1 + 2 + 1 = 8 as well
    flip: 12 + 21 = 33 → 6;  21 - 12 = 9;  12 x 21 = 252 → 9;  3 x 7 = 21 and its flip 12 (#259 "(3x7=12 and 21)")
    halve the odd: 12121 = 6060.5 + 6060.5
    the ends: 1 + 8 = 9, the first 9-pair of #270 (124 + 875 = 999: 1+8, 2+7, 4+5)
BUILD OUT, LINE 2:
    9240.5 + 9240.5 = 18481: the odd number halved into two equal halves, the move of 1 / 2 = 0.5 + 0.5 = 1 (#270)
    18481 = 18 | 4 | 81, a palindrome and a prime -- 181 of #270 with 4 set in the centre    (reading, asked)
    digits: 9 + 2 + 4 + 0 + 5 = 20 → 2 on each side, 40 → 4 both sides; 18481 → 1 + 8 + 4 + 8 + 1 = 22 → 4
    both ways: 9240.5 has 5 digits with the zero, 4 without; the digit sum is 20 either way
    the whole part 9240 = 2^3 x 3 x 5 x 7 x 11
TIE: 12121 = (1)2(1)2(1) and 18481 = (1)8(4)8(1) are both five-digit palindromes a b c b a; 12121 = 17 x 23 x 31,
    18481 prime.
ASKED: is the (8) the total 1 + 12 + 1 + 21 = 35 → 8, and is 9240.5 the half of 18481 = 18 | 4 | 81 built out of 181?
Frameworks: records/gf37_audit_12_1_21_9240_2026_11_28.txt.

FALSIFICATION: any assertion failing.
"""
import pathlib
from fractions import Fraction as F

from sympy import factorint, isprime

TH = pathlib.Path(__file__).resolve().parent
dr = lambda n: 1 + (n - 1) % 9
assert int("12" + "1" + "21") == 12121 and "12" == "21"[::-1] and factorint(12121) == {17: 1, 23: 1, 31: 1}
assert 12 + 1 + 21 == 34 and dr(34) == 7 and 1 + 12 + 1 + 21 == 35 and dr(35) == 8 and sum(map(int, "112121")) == 8
assert 12 + 21 == 33 and dr(33) == 6 and 21 - 12 == 9 and 12 * 21 == 252 and dr(252) == 9 and 3 * 7 == 21
assert F(12121, 2) * 2 == 12121 and F(12121, 2) == F(60605, 10) and 1 + 8 == 9 and 124 + 875 == 999
assert "9240.5"[::-1] == "5.0429" and F(92405, 10) * 2 == 18481 and str(18481) == str(18481)[::-1] and isprime(18481)
assert int("18" + "4" + "81") == 18481 and "181" == "1" + "8" + "1"
assert sum(map(int, "92405")) == sum(map(int, "50429")) == 20 and dr(40) == 4 and sum(map(int, "18481")) == 22 and dr(22) == 4
assert len("92405") == 5 and len("9245") == 4 and factorint(9240) == {2: 3, 3: 1, 5: 1, 7: 1, 11: 1}
assert "12121" in (TH / "grid_split_23_over_6_2026_10_13.py").read_text()
assert "build out of 181" in (TH / "odd_even_doubling_181_2026_10_13.py").read_text()

if __name__ == "__main__":
    print("12|1|21 = 12121 (#259), 1+12+1+21 = 35 -> 8; 9240.5 x 2 = 18481 = 18|4|81, prime palindrome; mirror right")
