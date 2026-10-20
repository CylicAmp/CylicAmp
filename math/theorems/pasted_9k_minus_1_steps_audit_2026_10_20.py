# CLASS: AUDIT
"""
Stepping the lead factor 9k - 1 of A056117 by +9 and -9 (owner_work #397, 2026-10-20). A pasted script with comments; run as given it prints
k=0..-5: -1, -10, -19, -28, -37, -46. Nothing is put in the owner's mouth.

RIGHT (re-run): 9k - 1 for k = 0..12: -1 8 17 26 35 44 53 62 71 80 89 98 107 ; for k = 0..-12: -1 -10 -19 -28 -37 -46 -55 -64 -73 -82 -91 -100 -109.
  "37 appears" at k = -4: 9 x (-4) - 1 = -37. It comes back every 37 steps: 9 x 33 = 297 = 8 x 37 + 1, so 37 divides 9k - 1 exactly when k = -4, 33, 70, ...
  (forced: a step of 9 hits every remainder by 37 once in 37 steps).
NOT RIGHT AS WRITTEN: "53 <- 53 from Riemann zero interval!" -- the interval [48, 53] was the window a pasted text (#364) drew around gamma_9..gamma_11; 53 is its
  edge, not a zero. The zero nearest 53 is gamma_11 = 52.970 (0.030 below).
WHAT THE STEPS SHOW, in the owner's chain:
  every 9k - 1 from 8 on chains to 8 (8, 17 → 8, 26 → 8, ...): adding 9 changes nothing. The negative side has sizes 10, 19, 28, 37, ... = 9k + 1, chaining to 1.
  Primes among them: 17 53 71 89 107 on the + side ; 19 37 73 109 on the − side (sizes).
THE SEQUENCE ITSELF AT NEGATIVE k (the "and in our sequences" part): b(k) = (9k - 1)/8 x C(k+6, 7), read as a polynomial in k:
  b(0) = b(-1) = ... = b(-6) = 0 ; then b(-7) = 8, b(-8) = 73, b(-9) = 369, b(-10) = 1365, b(-11) = 4125, b(-12) = 10791.
  These are the terms of (8 + x)/(1 - x)^9 -- the numerator 1 + 8x of A056117 read backwards (8 + x). Forced: a series p(x)/(1 - x)^9 always continues to negative
  k this way (the reversal rule for such series). 369 is the owner's 369 = 9 x 41 = 3 x 123 (#268), and 73 the 73 of 10001 = 73 x 137 (#368).

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F
from math import factorial

import sympy as sp
from sympy import isprime

assert [9 * k - 1 for k in range(13)] == [-1, 8, 17, 26, 35, 44, 53, 62, 71, 80, 89, 98, 107]
assert [9 * k - 1 for k in range(0, -13, -1)] == [-1, -10, -19, -28, -37, -46, -55, -64, -73, -82, -91, -100, -109]
assert [k for k in range(-40, 80) if (9 * k - 1) % 37 == 0] == [-4, 33, 70] and 9 * 33 == 297 == 8 * 37 + 1
assert all((9 * k - 1) % 9 == 8 for k in range(1, 200)) and all((9 * k + 1) % 9 == 1 for k in range(1, 200))
assert [9 * k - 1 for k in range(1, 13) if isprime(9 * k - 1)] == [17, 53, 71, 89, 107]
assert [9 * k + 1 for k in range(1, 13) if isprime(9 * k + 1)] == [19, 37, 73, 109]


def b(k):                                  # (9k-1)/8 x C(k+6, 7) as a polynomial in k
    prod = 1
    for j in range(7):
        prod *= (k + 6 - j)
    return F(9 * k - 1, 8) * F(prod, factorial(7))


assert [b(k) for k in range(1, 9)] == [1, 17, 117, 525, 1815, 5247, 13299, 30459]
assert [b(k) for k in range(0, -7, -1)] == [0] * 7
neg = [b(k) for k in range(-7, -13, -1)]
assert neg == [8, 73, 369, 1365, 4125, 10791]
x = sp.symbols("x")
rev = sp.series((8 + x) / (1 - x) ** 9, x, 0, 6).removeO()
assert [rev.coeff(x, j) for j in range(6)] == neg
assert 369 == 9 * 41 == 3 * 123 and 10001 == 73 * 137

import json, pathlib
G = json.load(open(pathlib.Path(__file__).resolve().parents[2] / "math" / "lemmas" / "data" / "zeta_zeros_gamma_1_1000.json"))
nearest = min(G, key=lambda g: abs(g - 53))
assert round(nearest, 3) == 52.970 and G.index(nearest) == 10 and round(53 - nearest, 3) == 0.030

if __name__ == "__main__":
    print("9k-1 steps right; 37 at k=-4 (every 37 steps); 53 is a window edge, nearest zero 52.970; the counts at negative k are 8, 73, 369, ... = (8+x)/(1-x)^9")
