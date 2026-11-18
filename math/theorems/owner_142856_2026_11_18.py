# CLASS: COMPUTATION
"""
The owner's message (2026-11-18): "142856 / work i did". The owner's work on 142856 is not in the repository, the
removed message record, or the owner's Google Drive (searched 2026-11-18) -- asked for. Recorded here: the number
itself, through the frameworks.

    142856 = 142857 - 1 = 2^3 x 7 x 2551          (142857 is the repeating block of 1/7)
    7 x 142856 = 999992                            (7 x 142857 = 999999)
    digits 1 + 4 + 2 + 8 + 5 + 6 = 26 -> 8
    by 37: 142857 is a multiple of 37, so 142856 leaves 36 (that is -1), orbit NEG_H
    reversed: 658241 = 71 x 73 x 127
    1/142856: 3 digits before the repeat (from 2^3), then a period of 2550 = lcm(6, 425) -- 6 from the 7,
      425 from 2551

FALSIFICATION: any assertion failing.
"""
from math import lcm

from sympy import factorint, isprime, n_order

n = 142856
assert n == 142857 - 1 and factorint(n) == {2: 3, 7: 1, 2551: 1} and isprime(2551)
assert 7 * n == 999992 and 7 * 142857 == 999999
assert sum(map(int, str(n))) == 26 and 1 + (n - 1) % 9 == 8
assert 142857 % 37 == 0 and n % 37 == 36
assert int(str(n)[::-1]) == 658241 == 71 * 73 * 127
assert n_order(10, 7) == 6 and n_order(10, 2551) == 425 and lcm(6, 425) == 2550

if __name__ == "__main__":
    print("142856 = 142857 - 1 = 2^3 x 7 x 2551; 7 x 142856 = 999992; root 8; leaves 36 by 37; reversed 71 x 73 x 127")
