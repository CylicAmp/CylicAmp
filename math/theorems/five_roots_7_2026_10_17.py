# CLASS: AUDIT
"""
7, 43, 538, 61, 7 (owner_work #307, 2026-10-17).

THE OWNER'S LINES, verbatim:
    7
    43
    538
    61
    7

NO OPERATION OR SOURCE IS GIVEN with the five numbers, so nothing below says what they mean.

WHAT HOLDS
  All five have digital root 7: 7, 43 (4+3), 538 (5+3+8 = 16 -> 7), 61 (6+1), 7. So every difference between
  them is a multiple of 9 (forced: equal roots): 36, 495 = 55 x 9, -477 = -53 x 9, -54.
  The first and last are the same number, 7. 43 is also the first piece of the owner's 43|19|79 (#302-#303,
  roots 7, 1, 7; math/theorems/roots_43_19_79_2026_10_16.py).
  Sum 656 = 2^4 x 41, root 8. Concatenated 743538617, root 8 (forced: digital roots add).
  7, 43 and 61 are prime, and each is the upper member of a twin pair: (5, 7), (41, 43), (59, 61).
  538 = 2 x 269 (269 is prime; 271 is prime too, so 269 is the lower member of the twin pair (269, 271)).
  Reversals keep the root (forced): 34 (=7), 835 = 5 x 167 (=7), 16 (=7).

FRAMEWORKS (gf37-audit): 7 -> 7 D7, prime, safe prime (3 is Sophie Germain); 43 -> 6 TESLA; 538 = 2 x 269 -> 20 DARK_A;
  61 -> 24 SEED; 656 = 2^4 x 41 -> 27 NEG_H. 269 -> 10 IC.

FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


xs = [7, 43, 538, 61, 7]
assert [dr(n) for n in xs] == [7] * 5
assert [b - a for a, b in zip(xs, xs[1:])] == [36, 495, -477, -54] and all((b - a) % 9 == 0 for a, b in zip(xs, xs[1:]))
assert 495 == 55 * 9 and 477 == 53 * 9 and sum(xs) == 656 and factorint(656) == {2: 4, 41: 1} and dr(656) == 8
assert int("".join(map(str, xs))) == 743538617 and dr(743538617) == 8
assert all(isprime(n) and isprime(n - 2) for n in (7, 43, 61)) and not any(isprime(n + 2) for n in (7, 43, 61))
assert factorint(538) == {2: 1, 269: 1} and isprime(269) and isprime(271) and not isprime(267) and factorint(835) == {5: 1, 167: 1}
assert [int(str(n)[::-1]) for n in (43, 538, 61)] == [34, 835, 16] and [dr(n) for n in (34, 835, 16)] == [7, 7, 7]
assert [n % 37 for n in (7, 43, 538, 61, 656, 269)] == [7, 6, 20, 24, 27, 10]
assert isprime(3) and isprime(7) and 2 * 3 + 1 == 7

if __name__ == "__main__":
    print("7, 43, 538, 61, 7: all five have digital root 7; sum 656 = 2^4 x 41; source and operation not given")
