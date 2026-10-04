# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): "mechanical counter law" -- adding 1 to 9, 99, 999,
9999 flushes every column to 0; "the input needed is 1/k of k". Mathematics only.

CORRECT
  C1 (10^k - 1) + 1 = 10^k: one unit clears k nines, for every k, with k carries; the
     digit sum drops from 9k to 1.
  C2 The exact law behind it is already filed: T432 (theorem_432_carry_map_digital_root_
     rings_gf37.py), Kummer's identity C(x, y) = (s(x) + s(y) - s(x+y)) / 9. With y = 1:
        s(n + 1) = s(n) + 1 - 9t,   t = number of trailing nines of n
     (checked below for every n < 10^6). At n = 10^k - 1, t = k.

NOT ESTABLISHED / WRONG
  C3 "To reach the next clean state (2 0) from 18 you needed 2 units": 18 is the DIGIT SUM
     of 99, not a state of the counter; 99 + 1 = 100, not 20. Likewise "from 27 you would
     need 3 ones" mixes the digit sum 27 of 999 with the number itself.
  C4 "You only need 1/k of the effort because k counters work together": the input is 1
     for every k, so "1/k of k" is the identity 1 = k / k, not a fraction of work saved.
     What grows with k is the number of carries (k), which T432 counts exactly.
FALSIFICATION: any assertion failing.
"""
s = lambda n: sum(map(int, str(n)))


def trailing_nines(n):
    t = 0
    while n % 10 == 9:
        n //= 10
        t += 1
    return t


for k in range(1, 12):                                                    # C1
    n = 10 ** k - 1
    assert n + 1 == 10 ** k and s(n) == 9 * k and s(n + 1) == 1 and trailing_nines(n) == k
assert all(s(n + 1) == s(n) + 1 - 9 * trailing_nines(n) for n in range(10 ** 6))     # C2
assert s(99) == 18 and 99 + 1 == 100 != 20 and s(999) == 27                           # C3
assert all(k / k == 1 for k in range(1, 20))                                           # C4
