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

if __name__ == "__main__":
    print("#382: 1+1 = 2, 0.5x4 = 2.0 (0.20 wrong), 5 = 2.5+2.5 = two 7s, 20 = 5555 = 8 x 2.5 = 8 sevens; halving walks 1 2 4 8 7 5 backwards")
