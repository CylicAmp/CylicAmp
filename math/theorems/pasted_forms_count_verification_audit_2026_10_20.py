# CLASS: AUDIT
"""
A pasted verification of the 0.125 form counts (owner_work #387, 2026-10-20). The message carries another tool's text ("That's symmetric! ... So the
column 3 is: k x C(7, k-1) for k = 1 to 8?"), a copy of an earlier CI line, its printed report and its two scripts. Nothing is put in the owner's mouth.
The counts it checks are owner_0125_all_forms_count_2026_10_20.py (column 2 = with zero, column 3 = without zero).

WRONG:
  1. Section [5] computes 9% x e^3.333 = 2.522005 and quotes the owner as "9% × e^3.333 = nothing". The owner wrote "9%×e^(3,333": the comma is the
     thousands comma, 3,333 = 3333. 9% x e^3333 = 2.8691330815 x 10^1446; a computer double stops near 1.8 x 10^308 (e^709.78), so that is the real
     overflow, and the pasted code never computes it.
  2. "9% × e^333 = 3.752364e+143 (overflow in standard float)": no overflow; 3.75 x 10^143 is far inside the double range. The code prints that label for any
     result above 10^100.
  3. "That's symmetric!": the binomials 1 7 21 35 35 21 7 1 are symmetric; column 3 (1 14 63 140 175 126 49 8) is not. What it has: the rows k and 9 - k
     share the same binomial C(7, k-1), with weights k and 9 - k.
RIGHT (re-run): the table, the cumulative column 1 18 135 660 2475 7722 21021 51480; column 3 = k x C(7, k-1) for k = 1..8; sum 576 = (7+2) x 2^6; every factorization
  of column 2 (17 ; 3x3x13 ; 3x5x5x7 ; 3x5x11x11 ; 3x3x11x53 ; 3x11x13x31 ; 3x11x13x71) ; 51480 = 72 x C(13,4) = 72 x 715 ; 51480/576 = 715/8 ;
  576 = 24 x 24 = 2^6 x 3^2 ; 51480 = 360 x 143 = 2^3 x 3^2 x 5 x 11 x 13, 11 and 13 twin primes ; 51480 = 13 mod 37 and 25 mod 41 ; 576 = 21 mod 37 ; 9 x 64 = 576 ;
  9% x e^3 = 1.8076983231 ; 9% x e^33 = 19,317,922,180,732.
ADDED HERE:
  Why 576 = 9 x 64: pair row k with row 9 - k; together k x C(7,k-1) + (9-k) x C(7,k-1) = 9 x C(7,k-1); the 8 rows make 4 pairs over the binomials
    1 7 21 35, and 9 x (1+7+21+35) = 9 x 64 = 576.
  Column 2 in one line: with zero, n digits give (9n - 1) x C(n+6, 7) / 8 forms. The factor 9n - 1 = 8 17 26 35 44 53 62 71 is where the primes 17, 53, 31 (62 = 2x31)
    and 71 of the factorizations come from. 51480 = 11440 + 40040 = 16 x 715 + 56 x 715 = 72 x 715 (the plain strings plus the extra point places).

FALSIFICATION: any assertion failing.
"""
import math
from fractions import Fraction
from math import comb

from mpmath import exp, log10, mp, mpf, nstr
from sympy import factorint, isprime

mp.dps = 40
col2 = [1, 17, 117, 525, 1815, 5247, 13299, 30459]
col3 = [1, 14, 63, 140, 175, 126, 49, 8]
cum = [sum(col2[:i + 1]) for i in range(8)]
assert cum == [1, 18, 135, 660, 2475, 7722, 21021, 51480]
assert col3 == [k * comb(7, k - 1) for k in range(1, 9)] and sum(col3) == 576 == (7 + 2) * 2 ** 6 == 7 * 2 ** 6 + 2 ** 7
assert [comb(7, j) for j in range(8)] == [1, 7, 21, 35, 35, 21, 7, 1] and col3 != col3[::-1]
assert all(col3[k - 1] + col3[8 - k] == 9 * comb(7, k - 1) for k in range(1, 9)) and 9 * (1 + 7 + 21 + 35) == 576
assert [factorint(c) for c in col2[1:]] == [{17: 1}, {3: 2, 13: 1}, {3: 1, 5: 2, 7: 1}, {3: 1, 5: 1, 11: 2}, {3: 2, 11: 1, 53: 1},
                                            {3: 1, 11: 1, 13: 1, 31: 1}, {3: 1, 11: 1, 13: 1, 71: 1}]
assert comb(13, 4) == 715 and 72 * 715 == 51480 and Fraction(51480, 576) == Fraction(715, 8)
assert 51480 == 360 * 143 and 143 == 11 * 13 and isprime(11) and isprime(13) and factorint(51480) == {2: 3, 3: 2, 5: 1, 11: 1, 13: 1}
assert (51480 % 37, 51480 % 41, 576 % 37, 576 % 9) == (13, 25, 21, 0) and 576 == 24 * 24 == 2 ** 6 * 3 ** 2

# column 2 in closed form
assert all(col2[n - 1] * 8 == (9 * n - 1) * comb(n + 6, 7) for n in range(1, 9))
assert [9 * n - 1 for n in range(1, 9)] == [8, 17, 26, 35, 44, 53, 62, 71] and 62 == 2 * 31
assert sum(comb(n + 7, 8) for n in range(1, 9)) == comb(16, 9) == 11440 == 16 * 715
assert sum((n - 1) * comb(n + 6, 7) for n in range(1, 9)) == 40040 == 56 * 715 and 11440 + 40040 == 51480

# the exponentials
assert nstr(mpf("0.09") * exp(3), 11) == "1.8076983231" and int(mpf("0.09") * exp(33)) == 19317922180732
assert abs(0.09 * math.exp(3.333) - 2.522005) < 1e-5                         # the pasted number, for 3.333
assert nstr(mpf("0.09") * exp(3333), 11) == "2.8691330815e+1446"             # the owner's 3,333
assert 0.09 * math.exp(333) < 1.7976931348623157e308                          # no overflow at 333
try:
    math.exp(3333)
    raise AssertionError("expected an overflow")
except OverflowError:
    pass
assert abs(math.log(1.7976931348623157e308) - 709.78) < 0.01

if __name__ == "__main__":
    print("pasted verification: counts right; e^(3,333) misread as e^3.333; e^333 is no overflow; column 3 is not symmetric, its pairs share C(7,k-1) -> 576 = 9 x 64")
