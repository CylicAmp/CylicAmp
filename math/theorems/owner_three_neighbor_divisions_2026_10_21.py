# CLASS: COMPUTATION
"""
The owner's 1, 2 and 3: a number divided by its neighbours (owner_work #403, 2026-10-21).
Process entry: owner_work/PROCESS.md, #403. Follows the pasted squeeze (#402,
pasted_neighbor_division_squeeze_audit_2026_10_21.py).

THE OWNER'S LINES, verbatim (#403):
    Actually I have 1 2 and 3

    One being the number just divides itself by the number in front of it. Or simply as its own
    other operation, the opposite. The number divides itself by the number behind it. Then we
    combine those two and we get the two-step. But there's a third. And a third one works like
    this, and it's important. You do the one behind you, you do yourself, and then you do the one
    to your right.

CLEANED (n is the number; in front = to the right = n + 1, behind = n - 1):
    1          n ÷ (n + 1)                          2 ÷ 3 = 0.666...
    2          n ÷ (n - 1)                          2 ÷ 1 = 2
    two-step   1 and 2 together
    3          behind, yourself, right:  n - 1, n, n + 1

PROCESS: take a number; divide it by the one in front (1); divide it by the one behind (2);
put 1 and 2 together (the two-step); then take all three places -- behind, yourself, right (3).

TWO PAIRINGS OF THE TWO-STEP (both computed; which one is the owner's is asked):
    1 and 2 by the same number n:      n ÷ (n + 1) and n ÷ (n - 1)      at 2: 0.666... and 2
    the paste's (#402): 1 by the number behind, 2 by n:
                                        (n - 1) ÷ n and n ÷ (n - 1)      at 2: 0.5 and 2
    the paste's pair multiplies to 1; the same-number pair multiplies to n x n ÷ (n x n - 1).

3, READ THE SAME WAY AS 1 AND 2 (you ÷ each of the three):
    n ÷ (n - 1),  n ÷ n = 1,  n ÷ (n + 1)
      2 -> 2,    1, 0.666...
      3 -> 1.5,  1, 0.75
      4 -> 1.333..., 1, 0.8
    "you do yourself" is n ÷ n = 1 -- the 1 sits inside 3 as its own step.
    The outer two multiply to n x n ÷ (n x n - 1) = 1 + 1 ÷ (n x n - 1), and their average is the
    same number (they always are: the flips of the outer two add to 2).
      2 -> 4/3 = 1.333...    3 -> 9/8 = 1.125    4 -> 16/15 = 1.0666...
      5 -> 25/24 = 1.041666...    9 -> 81/80 = 1.0125    10 -> 100/99 = 1.0101...
    3 -> 3 ÷ 2 x 3 ÷ 4 = 9 ÷ 8 = 1.125: the owner's 1.125 of #368 (9 ÷ 2 ÷ 2 ÷ 2 = 1.125).
    5 -> 1 + 1/24: the /24 of #386 (1% ÷ 4 ÷ 3 ÷ 2 ÷ 1 = 1/2400).
    10 -> 1 + 1/99: 1 ÷ 99 = 0.0101..., the product of every step of the squeeze (#402).
    The product ends (no loop) at 3 and 9 only -- 1.125 and 1.0125 -- for every number, not just to 99
      (proof below: n x n - 1 = (n - 1)(n + 1) must be made of 2s and 5s only).
    All of 3 multiplied from 2 to 99: 2 x 99 ÷ 100 = 1.98.

3, FLIPPED (each of the three ÷ you):
    (n - 1) ÷ n,  n ÷ n = 1,  (n + 1) ÷ n   =   1 - 1/n,  1,  1 + 1/n
      2 -> 0.5, 1, 1.5      3 -> 0.666..., 1, 1.333...     4 -> 0.75, 1, 1.25
    equal steps of 1/n, and 1 is exactly the middle by adding: (n - 1) + (n + 1) = 2n.
    This is where 1 is the center that the paste (#402) claimed and did not have: the paste used
    behind and yourself only; with the one to the right as well, 1 is dead center.

3, READ AS ONE CHAIN: (n - 1) ÷ n ÷ (n + 1)
      2 -> 1 ÷ 2 ÷ 3 = 1/6     3 -> 2 ÷ 3 ÷ 4 = 1/6     4 -> 3 ÷ 4 ÷ 5 = 3/20 = 0.15

BOTH WAYS (with zero and without):
    n = 1, the same way as 1 and 2:  1 ÷ 0 (no value), 1 ÷ 1 = 1, 1 ÷ 2 = 0.5 -> 3 starts at 2
    n = 1, flipped:                  0 ÷ 1 = 0, 1, 2 ÷ 1 = 2 -> 0 1 2, steps of 1, 1 in the middle
    n = 1, one chain:                0 ÷ 1 ÷ 2 = 0
    n = 2 to 99 (98 numbers), the same way as 1 and 2:
      n ÷ (n - 1) loops 84, ends 14     n ÷ (n + 1) loops 85, ends 13
      n ÷ n = 1 never loops             the product loops 96, ends 2 (n = 3, 9)

PROOF that the product ends only at 3 and 9: n x n ÷ (n x n - 1) is in lowest terms, so it ends
exactly when n - 1 and n + 1 are made of 2s and 5s only. If n is even both are odd, so both are
powers of 5 two apart: impossible (1 and 3, 5 and 7, ...: 3 is not a power of 5, and two powers
of 5 above 1 differ by at least 20). If n is odd, m = (n - 1) ÷ 2 and m + 1 are next to each
other and made of 2s and 5s; they share no factor, so one is a power of 2 and the other a power
of 5:  2^b - 5^a = 1 gives 2^b = 5^a + 1, which leaves 2 by 4, so b = 1, a = 0: m = 1, n = 3;
5^a - 2^b = 1: by 3, 5^a leaves 1 or 2 and 2^b leaves 2 or 1, so a is odd and b is even; if
b >= 3 then 5^a leaves 1 by 8, so a is even -- a clash; so b = 2, a = 1: m = 4, n = 9.

RESIDUES mod 37 (gf37-audit): 1 IC, 2 DARK_A (Sophie Germain: 5), 3 C3 (twin with 5, Sophie
Germain: 7).

MISSING (asked): which reading of "you do": you ÷ each (as in 1 and 2), each ÷ you, or one chain;
and whether the two-step is 1 and 2 by the same number or the paste's pairing.
SETTLED in #405 (owner_three_operations_neighbours_2026_10_21.py): 3 is n with each place, one at
a time (the chain reading drops); the two-step is 1 and 2 by the same number.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F
from math import prod


def ends(q):
    """a fraction's decimal ends exactly when its bottom is made of 2s and 5s only"""
    d = F(q).denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def op1(n):
    return F(n, n + 1)


def op2(n):
    return F(n, n - 1)


def three(n):                 # read the same way as 1 and 2
    return op2(n), F(n, n), op1(n)


def three_flipped(n):
    return F(n - 1, n), F(n, n), F(n + 1, n)


def three_chain(n):
    return F(n - 1, n) / (n + 1)


N = range(2, 100)

# --- 1, 2 and the two pairings ---
assert op1(2) == F(2, 3) and op2(2) == 2
assert all(op1(n) < 1 < op2(n) for n in N)
assert all(op1(n - 1) * op2(n) == 1 for n in N)                      # the paste's pairing
assert all(op1(n) * op2(n) == F(n * n, n * n - 1) for n in N)         # same-number pairing
assert op1(1) == F(1, 2)                                             # 1 by the number behind 2

# --- 3, the same way as 1 and 2 ---
assert three(2) == (2, 1, F(2, 3)) and three(3) == (F(3, 2), 1, F(3, 4)) and three(4) == (F(4, 3), 1, F(4, 5))
outer = {n: three(n)[0] * three(n)[2] for n in N}
assert all(outer[n] == (three(n)[0] + three(n)[2]) / 2 == 1 + F(1, n * n - 1) for n in N)
assert all(1 / three(n)[0] + 1 / three(n)[2] == 2 for n in N)
assert [outer[n] for n in (2, 3, 4, 5, 9, 10)] == [F(4, 3), F(9, 8), F(16, 15), F(25, 24), F(81, 80), F(100, 99)]
assert outer[3] == F(9, 2 * 2 * 2) == F(1125, 1000)                  # #368: 9 ÷ 2 ÷ 2 ÷ 2 = 1.125
assert outer[5] - 1 == F(1, 24) and F(1, 100) / 4 / 3 / 2 / 1 == F(1, 2400)   # #386
assert outer[10] - 1 == F(1, 99) == prod(F(n - 1, n) for n in N)     # #402
assert [n for n in N if ends(outer[n])] == [3, 9] and outer[9] == F(10125, 10000)
assert [n for n in range(2, 200000) if ends(F(n * n, n * n - 1))] == [3, 9]
assert prod(outer[n] for n in N) == F(99, 50) == F(2 * 99, 100)

# --- 3 flipped: 1 is the middle by adding ---
assert three_flipped(2) == (F(1, 2), 1, F(3, 2)) and three_flipped(4) == (F(3, 4), 1, F(5, 4))
assert all(three_flipped(n)[0] + three_flipped(n)[2] == 2 for n in N)
assert all(three_flipped(n)[1] - three_flipped(n)[0] == three_flipped(n)[2] - three_flipped(n)[1] == F(1, n) for n in N)

# --- 3 as one chain ---
assert [three_chain(n) for n in (2, 3, 4)] == [F(1, 6), F(1, 6), F(3, 20)]

# --- both ways ---
assert three_flipped(1) == (0, 1, 2) and three_chain(1) == 0 and op1(1) == F(1, 2)
try:
    op2(1)
    raise AssertionError("1 ÷ 0 must have no value")
except ZeroDivisionError:
    pass
assert sum(not ends(op2(n)) for n in N) == 84 and sum(not ends(op1(n)) for n in N) == 85
assert sum(not ends(outer[n]) for n in N) == 96

# --- the proof, step by step, checked on small powers ---
assert all(2 ** b - 5 ** a != 1 for a in range(0, 30) for b in range(2, 80))      # b = 1 only
assert [(a, b) for a in range(0, 30) for b in range(0, 80) if 5 ** a - 2 ** b == 1] == [(1, 2)]
assert [(a, b) for a in range(0, 30) for b in range(0, 80) if 2 ** b - 5 ** a == 1] == [(0, 1)]
assert all((5 ** a) % 8 == 1 for a in range(0, 30, 2)) and all((5 ** a) % 8 == 5 for a in range(1, 30, 2))

# --- residues ---
assert [x % 37 for x in (1, 2, 3)] == [1, 2, 3]

if __name__ == "__main__":
    print("1: n ÷ (n+1); 2: n ÷ (n-1); 3 (you ÷ behind, yourself, right): n/(n-1), 1, n/(n+1); the outer two "
          "multiply and average to n²/(n²-1): 3 -> 9/8 = 1.125 (#368), 5 -> 1 + 1/24 (#386), 10 -> 1 + 1/99; "
          "ends only at 3 and 9; flipped, 1 - 1/n, 1, 1 + 1/n puts 1 exactly in the middle")
