# CLASS: AUDIT
"""
x^(x^x) = (1/2)^sqrt(2)  (Cliff Pickover's post, sent by the owner 2026-10-13 with "=7";
image at owner_work/images/2026-10-13_pickover_tetration.jpg)

SOLUTION  x = 1/4.
  x^x = (1/4)^(1/4) = 2^(-1/2);  x^(x^x) = (2^-2)^(2^-1/2) = 2^(-2/sqrt2) = 2^(-sqrt2) = (1/2)^sqrt2.
UNIQUE on x > 0:  f(x) = x^(x^x) = exp(x^x ln x).  On (0,1) the exponent's derivative is
  x^x [ (ln x)^2 + ln x + 1/x ] > 0, since (ln x)^2 + ln x >= -1/4 and 1/x > 1; so f increases
  from 0 to 1. For x >= 1, f(x) >= 1 > (1/2)^sqrt2 = 0.375... So x = 1/4 is the only positive root.
THE OWNER'S 7:  x = 0.25, and 2 + 5 = 7.
FRAMEWORKS (7):  7 -> D7 {7, 33, 34}, DR 7; prime, twin (5, 7), cousin, sexy; safe prime (3 -> 7,
  Sophie Germain chain); 1/4 = 28 (mod 37), SA_ST_B.

FALSIFICATION: any assertion failing.
"""
import math
from sympy import Rational, sqrt, simplify, nsimplify, log, symbols, diff, exp

x0 = Rational(1, 4)
assert simplify(x0 ** x0 - 2 ** Rational(-1, 2)) == 0
assert simplify(x0 ** (x0 ** x0) - Rational(1, 2) ** sqrt(2)) == 0
x = symbols("x", positive=True)
g = diff((x ** x) * log(x), x)
assert all(g.subs(x, Rational(k, 1000)).evalf() > 0 for k in range(1, 1000))      # f increasing on (0,1)
assert all((v / 100) ** ((v / 100) ** (v / 100)) >= 1 for v in range(100, 400))   # f >= 1 for x >= 1
assert abs(0.25 ** (0.25 ** 0.25) - 0.5 ** math.sqrt(2)) < 1e-15
assert sum(map(int, "25")) == 7                                                   # 0.25 -> 2 + 5 = 7
assert 7 % 37 in {7, 33, 34} and 4 * 28 % 37 == 1 and 28 in {21, 25, 28}
assert all(n % d for n in (5, 7) for d in range(2, n)) and all(n % d for n in (3,) for d in range(2, n))

if __name__ == "__main__":
    print("x = 1/4 (unique positive root); 0.25 -> 2+5 = 7; 7 in D7, twin prime, safe prime; 1/4 = 28 mod 37")
