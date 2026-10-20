# CLASS: AUDIT
"""
Odds making evens, halves, and "20 equal 5555, that's 8 sevens" (owner_work #382, 2026-10-20). Process entry: owner_work/PROCESS.md, #382.

THE OWNER'S LINES, verbatim:
    2 made from odd odd =even
    or 4 odds even

    1÷2=0.5 +0.5
    2=1+1=0.5×4=2.0 or 0.20 im not sure
    4 × 5 =20
    5=2 number sevens
    because
    5÷2=2.5+2.5

    so 20 equal 5555
    thats 8 sevens

CLEANED AND CHECKED:
  1 + 1 = 2 : two odds make an even                                             right
  four odds make an even (5 + 5 + 5 + 5 = 20)                                   right
  1 ÷ 2 = 0.5 → 0.5 + 0.5 = 1                                                    right
  2 = 1 + 1 = 0.5 x 4 = 2.0                                                      right
  "or 0.20": wrong -- 0.5 x 4 = 2.0 ; 0.20 is 0.5 x 0.4, a tenth of 2. With zero and without: 2.0 = 2 (a 0 at the end after the point changes nothing),
    0.20 = 0.2 (a 0 in front moves the 2 one place to the right).
  4 x 5 = 20                                                                     right
  5 ÷ 2 = 2.5 → 2.5 + 2.5 = 5 ; 2.5 → 2 + 5 = 7 : 5 is two numbers that are each a 7 ("2 number sevens") ; 7 + 7 = 14 → 1 + 4 = 5, back to 5   right
  20 = 5 + 5 + 5 + 5 ("5555") = 8 x 2.5 → 8 sevens ; 8 x 7 = 56 → 5 + 6 = 11 → 1 + 1 = 2, the same as 20 → 2 + 0 = 2                      right
THE PATTERN UNDER IT: halving walks the owner's doubling roots 1 2 4 8 7 5 backwards. 5 → 2.5 (7) → 1.25 (8) → 0.625 (13 → 4) → 0.3125 (11 → 2)
  → 0.15625 (19 → 1) → 0.078125 (23 → 5): 5 7 8 4 2 1 5, six steps and round again (halving is x5 on roots: 5 x 5 = 25 → 7).
FRAMEWORKS (gf37-audit): 20 DARK_A ; 25 SA_ST_B ; 5555 = 5x11x101 = 5 CAS_EXT ; 56 = 19 CAS_EXT ; 7 D7 ; 8 TESLA.

#383 (2026-10-20), verbatim:
    20 is made from 55|55 even odds
    20 is made from 77|77|77|77

    7÷2=3.5+3.5=7

    so
    8 sevens =
    7 × 3.5+3.5
    or 7x7=4+9=1-3=4
  Cleaned and checked:
    20 = 5+5 | 5+5 : four odds, an even number of them                                                   right
    20 = 77 | 77 | 77 | 77 : eight halves of 5 (2.5 each, each read 2+5 = 7) ; 8 x 2.5 = 20 ; 8 x 7 = 56 → 5+6 = 11 → 1+1 = 2 = the root of 20   right
    7 ÷ 2 = 3.5 → 3.5 + 3.5 = 7 ; 3.5 → 3+5 = 8, so 7 halves into two 8s, and 8+8 = 16 → 1+6 = 7, back to 7   right
    "8 sevens = 7 × 3.5+3.5", two readings:
      as written, 7 x 3.5 + 3.5 = 24.5 + 3.5 = 28 = 8 x 3.5 : eight halves of 7 ; 28 → 2+8 = 10 → 1            right
      with brackets, 7 x (3.5 + 3.5) = 7 x 7 = 49 → 4+9 = 13 → 1+3 = 4 (the "or 7x7" line)                      right as arithmetic
    8 sevens as whole 7s is 8 x 7 = 56 → 2 ; 7 x 7 = 49 → 4 is seven sevens. If the 7 in front was meant as 8 (the key next to it):
      8 x (3.5 + 3.5) = 8 x 7 = 56 → 2, the root of 20. Which reading is meant is asked in the reply.

#384 (2026-10-20), verbatim:
    3.5=8
    3.5=8+8=(1+6=7)
    6=6.1=1
    8=3.5=8
    8=5.3=8
    1=1.6=6
  Cleaned and checked:
    3.5 → 3+5 = 8                                                                 right
    3.5 + 3.5 → 8 + 8 = 16 → 1+6 = 7 (the 7 the halves came from: 3.5 + 3.5 = 7)    right
    8 → 3.5 → 3+5 = 8 ; 8 → 5.3 → 5+3 = 8 (the flip keeps the 8)                    right
    16 → 1.6 and its flip 6.1 ; "6=6.1=1" and "1=1.6=6" name the two digits of each (6 then 1, 1 then 6) ; added, each is 7 (6+1, 1+6).
      Which the two lines mean -- the two digits, or the 7 like the 8 lines -- is asked in the reply.
  Forced (true every time): doubling a half's digit root gives back the whole's root (8+8 = 16 → 7 for 7 ; 7+7 = 14 → 5 for 5), because halving is x5
    on roots and doubling is x2, and 2 x 5 = 10 → 1. A flip of two digits changes the number by a multiple of 9: 53 − 35 = 18, 61 − 16 = 45.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as Q

from sympy import factorint


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def digit_root_of_decimal(q):
    s = str(float(q)) if q.denominator != 1 else str(q)
    return dr(sum(int(c) for c in s if c.isdigit()))


assert 1 + 1 == 2 and (1 % 2, 1 % 2, 2 % 2) == (1, 1, 0) and (5 + 5 + 5 + 5) % 2 == 0
assert all((a + b + c + d) % 2 == 0 for a in range(1, 20, 2) for b in range(1, 20, 2) for c in range(1, 8, 2) for d in range(1, 8, 2))
assert Q(1, 2) == Q(5, 10) and Q(5, 10) + Q(5, 10) == 1
assert 1 + 1 == Q(5, 10) * 4 == 2 and Q(20, 100) == Q(5, 10) * Q(4, 10) and Q(20, 100) * 10 == 2
assert 4 * 5 == 20 and Q(5, 2) == Q(25, 10) and Q(25, 10) + Q(25, 10) == 5 and 2 + 5 == 7 and 7 + 7 == 14 and 1 + 4 == 5
assert 5 + 5 + 5 + 5 == 20 == 8 * Q(25, 10) and 8 * 7 == 56 and 5 + 6 == 11 and dr(56) == dr(20) == 2

halves, x = [], Q(5)
for _ in range(7):
    halves.append(digit_root_of_decimal(x))
    x = x / 2
assert halves == [5, 7, 8, 4, 2, 1, 5] and [str(float(Q(5, 2 ** k))) for k in range(1, 7)] == ["2.5", "1.25", "0.625", "0.3125", "0.15625", "0.078125"]
assert [pow(2, k, 9) for k in range(6)] == [1, 2, 4, 8, 7, 5] and halves[:6] == [5, 7, 8, 4, 2, 1] and (5 * 5) % 9 == 7

assert (20 % 37, 25 % 37, 5555 % 37, 56 % 37) == (20, 25, 5, 19) and factorint(5555) == {5: 1, 11: 1, 101: 1}

# #383
assert 5 + 5 + 5 + 5 == 20 and 4 % 2 == 0 and 8 * Q(25, 10) == 20 and 8 * 7 == 56 and dr(56) == dr(20) == 2
assert Q(7, 2) == Q(35, 10) and Q(35, 10) * 2 == 7 and 3 + 5 == 8 and 8 + 8 == 16 and 1 + 6 == 7
assert 7 * Q(35, 10) + Q(35, 10) == 28 == 8 * Q(35, 10) and dr(28) == 1
assert 7 * (Q(35, 10) + Q(35, 10)) == 49 == 7 * 7 and 4 + 9 == 13 and 1 + 3 == 4 and dr(49) == 4
assert 8 * (Q(35, 10) + Q(35, 10)) == 56 and dr(56) == 2 != dr(49)

# #384
assert 3 + 5 == 8 == 5 + 3 and 8 + 8 == 16 and 1 + 6 == 7 and Q(35, 10) + Q(35, 10) == 7
assert 6 + 1 == 1 + 6 == 7 and 61 - 16 == 45 == 9 * 5 and 53 - 35 == 18 == 9 * 2
for whole in range(1, 200):
    half = Q(whole, 2)
    assert dr(2 * digit_root_of_decimal(half)) == dr(whole)

if __name__ == "__main__":
    print("#382: 1+1 = 2, 0.5x4 = 2.0 (0.20 wrong), 5 = 2.5+2.5 = two 7s, 20 = 5555 = 8 x 2.5 = 8 sevens; halving walks 1 2 4 8 7 5 backwards")
