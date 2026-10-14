# CLASS: AUDIT
"""
Audit of the pasted block "The Next Direct Computation: Continuing the Multiples of 9 Sequence"
(owner_work #291, 2026-10-14): n = 342, 351, ..., 441 with factorizations and links.

HOLDS
  All twelve factorizations are right, and every n has digital root 9 (forced: 9 | n, n > 0).
  333 = 3^2 x 37.  19 = 2^-1 mod 37 (2 x 19 = 38).  351 = 3^3 x 13, 369 = 3^2 x 41, 369 - 351 = 18.
  det [8 1 6; 3 5 7; 4 9 2] = -360 (the Lo Shu square).  378 = 370 + 8.  387 = 10 x 37 + 17.
  396 = 36 x 11.  405 = 45 x 9.  23 divides 133,860 (= 23 x 5820).  441 = 21^2.  1+7+7+6 = 21.

WRONG
  "432 ... Highly composite": 432 has 20 divisors; 360, which is smaller, has 24. A highly composite
  number has more divisors than every smaller number, so 432 is not one. 360 is.
  "zero information loss between steps": every positive multiple of 9 has digital root 9, so the
  digital root is the same constant at every step -- it keeps none of the information about n.

NOT DEFINED IN THE PASTE (and not found in the repo under these names)
  N(a, b), "N(1,7) = 4 x 13 x 37" (= 1924), "N(5,6) = 2 x 41 x 37" (= 3034), "isotropic class",
  "Sigma N = 133,860", "ray multiplicity", "the 37-horizon", "1776 -> 21 anchor". The numbers stated
  for them are arithmetically right; what N(a, b) is, the block does not say. (Not a^2 + ab + b^2:
  that gives 57 and 91.) Several formulas were lost in the paste (blank lines after "first
  isotropic class", "second isotropic class", "primary reduction", "projection satisfies").

FRAMEWORKS (gf37-audit): 342 SA_ST_A; 351 SEED; 360 NEG_H; 369 NEG_H; 378 TESLA; 387 NQR17; 396 IC;
  405 NQR17; 414 D7; 423 SA_ST_A; 432 SA_ST_B; 441 D7.
  369 is the owner's "this section goes by 369" (#268) = 3 x 123 (comma_slide_and_pairs_2026_10_13.py).

FALSIFICATION: any assertion failing.
"""
from sympy import Matrix, divisor_count, factorint


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


CLAIMED = {342: {2: 1, 3: 2, 19: 1}, 351: {3: 3, 13: 1}, 360: {2: 3, 3: 2, 5: 1}, 369: {3: 2, 41: 1},
           378: {2: 1, 3: 3, 7: 1}, 387: {3: 2, 43: 1}, 396: {2: 2, 3: 2, 11: 1}, 405: {3: 4, 5: 1},
           414: {2: 1, 3: 2, 23: 1}, 423: {3: 2, 47: 1}, 432: {2: 4, 3: 3}, 441: {3: 2, 7: 2}}
assert list(CLAIMED) == list(range(342, 442, 9))
assert all(factorint(n) == f for n, f in CLAIMED.items()) and all(dr(n) == 9 for n in CLAIMED)
assert 333 == 9 * 37 and 2 * 19 % 37 == 1 and 369 - 351 == 18
assert Matrix([[8, 1, 6], [3, 5, 7], [4, 9, 2]]).det() == -360
assert 370 + 8 == 378 and 10 * 37 + 17 == 387 and 36 * 11 == 396 and 45 * 9 == 405
assert 133860 == 23 * 5820 and 21 ** 2 == 441 and 1 + 7 + 7 + 6 == 21
assert 4 * 13 * 37 == 1924 and 2 * 41 * 37 == 3034 and (1 + 7 + 49, 25 + 30 + 36) == (57, 91)
# WRONG: 432 is not highly composite; 360 is
assert divisor_count(432) == 20 and divisor_count(360) == 24
assert not all(divisor_count(m) < divisor_count(432) for m in range(1, 432))
assert all(divisor_count(m) < divisor_count(360) for m in range(1, 360))
# WRONG: the digital root is constant on multiples of 9, so it carries no information about n
assert len({dr(9 * k) for k in range(1, 10000)}) == 1

if __name__ == "__main__":
    print("12 factorizations hold; 432 is not highly composite (360 is); dr = 9 is constant, so it keeps no information")
