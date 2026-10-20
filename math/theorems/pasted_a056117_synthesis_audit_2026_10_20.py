# CLASS: AUDIT
"""
A pasted "synthesis" of A056117 and the 9k - 1 steps (owner_work #398, 2026-10-20). Another tool's text. Nothing is put in the owner's mouth.

RIGHT (re-run):
  b_k = C(k+7, 8) + 8 C(k+6, 8) = (9k - 1) x C(k+6, 7)/8, by C(n, r) = n/r x C(n-1, r-1).
  The table: (9k - 1) = 8 17 26 35 44 53 62 71 ; C(k+6, 7)/8 = 1/8, 1, 9/2, 15, 165/4, 99, 429/2, 429 ; b_k = 1 17 117 525 1815 5247 13299 30459.
  Every 9k - 1 leaves 8 by 9.
  B(x) = A(x) x H(x) with A(x) = (1+x)^6 (1+8x) (column 3) and H(x) = 1/((1-x)^3 (1-x^2)^6): true, because (1-x^2)^6 = (1-x)^6 (1+x)^6, so the (1+x)^6 cancels and
    leaves (1+8x)/(1-x)^9. (The two columns' series are tied by H.)
  C(6 - k, 7) = -C(k, 7) for k at least 7 (the upper-negation identity).
  12 and 21 are 1 step of 9 apart, 14 and 41 three (27), 24 and 42 two (18), 37 and 73 four (36). Forced: a two-digit number and its flip always differ by
    9 x (the difference of the digits).
WRONG:
  1. Section 3: "The assertion failed because evaluating the analytic continuation ... involves sign changes from the binomial term (-1)^7" and "commit efee977
     passed with all 520 tests green". The assertion failed because the last expected value was typed wrong (11011; the value is 10791) -- the signs were already
     handled and every value was positive (8, 73, 369, 1365, 4125, 10791). The failing version was never committed (the commit step stops when a check fails);
     the fix is commit e1e49fb, CI run #521. efee977 is the commit before it. And 520 is the number of the CI run, not a count of tests: CI collects 571 tests.
  2. "Origin in Framework" column: the 53 as "Upper bound of Riemann zero cluster" and "the Riemann boundary 53" -- 53 is the edge of a window a pasted text drew
     around gamma_9..gamma_11 (#364); the nearest zero is gamma_11 = 52.970. "6+2 = 8", "7+1 = 8", "4+4 = 8" are not origins: every 9k - 1 adds up to 8 that way
     (forced), whatever k is.
MISSING (asked): "Matrix trace / odd root" (17), "UR Prefix sum (3 + 23 = 26)", and "Cascade state [4, 6, 8, 13, 24, 35]" -- none of the three is in the repository
  (searched: the cascade of the repository is {8, 13, 24}, cascade_8_13_24.py); the meaning of "8-cell geometry" is not given.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F
from math import comb

import sympy as sp

b = lambda k: comb(k + 7, 8) + 8 * comb(k + 6, 8)
for k in range(1, 30):
    assert comb(k + 7, 8) == F(k + 7, 8) * comb(k + 6, 7) and comb(k + 6, 8) == F(k - 1, 8) * comb(k + 6, 7)
    assert b(k) == F(9 * k - 1) * F(comb(k + 6, 7), 8)
assert [9 * k - 1 for k in range(1, 9)] == [8, 17, 26, 35, 44, 53, 62, 71]
assert [F(comb(k + 6, 7), 8) for k in range(1, 9)] == [F(1, 8), 1, F(9, 2), 15, F(165, 4), 99, F(429, 2), 429]
assert [b(k) for k in range(1, 9)] == [1, 17, 117, 525, 1815, 5247, 13299, 30459]
assert all((9 * k - 1) % 9 == 8 for k in range(1, 100))
chain = lambda n: n if n < 10 else chain(sum(map(int, str(n))))
assert all(chain(9 * k - 1) == 8 for k in range(1, 200)) and (6 + 2, 7 + 1, 4 + 4) == (8, 8, 8)

x = sp.symbols("x")
A = (1 + x) ** 6 * (1 + 8 * x)
H = 1 / ((1 - x) ** 3 * (1 - x ** 2) ** 6)
assert sp.simplify(A * H - (1 + 8 * x) / (1 - x) ** 9) == 0

kk = sp.symbols("k")
upper = lambda n, r: sp.prod([(n - j) for j in range(r)]) / sp.factorial(r)        # C(n, r) as a polynomial in n
assert all(upper(6 - k, 7) == -comb(k, 7) for k in range(7, 30))

assert [21 - 12, 41 - 14, 42 - 24, 73 - 37] == [9, 27, 18, 36]
assert all(abs(n - int(str(n)[::-1])) == 9 * abs(n // 10 - n % 10) for n in range(10, 100))

from math import factorial
def b_poly(k):
    p = 1
    for j in range(7):
        p *= (k + 6 - j)
    return F(9 * k - 1, 8) * F(p, factorial(7))
assert [b_poly(k) for k in range(-7, -13, -1)] == [8, 73, 369, 1365, 4125, 10791] and b_poly(-12) != 11011

if __name__ == "__main__":
    print("A056117 synthesis: factoring, table and B = A x H right; the failed assertion was a mistyped 10791 (not a sign), fixed in e1e49fb; 53 is a window edge")
