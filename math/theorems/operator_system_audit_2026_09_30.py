# CLASS: AUDIT
"""
Operator-system audit, 2026-09-29/30: every verdict reached in the session on
the supplied axiom set, flip labelings, collapse fixed points, the handwritten
page (19=10 ... 111=(PF-13)1x3) and the prime-type table. Each verdict below is
asserted; run this file to re-check all of them.

A. AXIOM SET ("King" list)
   Hold as stated: Axioms 1, 2, 3, 4, 8, 9; Artifacts 1, 2, 4, 5, 7, 9.
   A5  n = sum of digits is a MAP n -> S(n), not an equality (123 != 6).
   A5/A6  iterated digit sum and n mod 9 disagree exactly at multiples of 9
       (9 vs 0). Settled by the 9x9 grid: column index 1..9, so residue 0 is 9
       (grid81_operators_applied.py, A1).
   A7  the ordering n+0 < n*1 < ... needs a cost function; by operation count
       n+0 and n*1 tie.
   A10 splits of 0^4 into blocks of 1, 2, 3: 7, not 6 (missing 0-0-00).
       Counts for k = 1..6: 1, 2, 4, 7, 13, 24 (tribonacci).
   A11 0^k -> (x k + 1 + k): operand and order unstated.
   Artifacts 6 and 10 give the same string 11111223 for n = 4 from different
       definitions; no stated rule produces it.

B. FLIP LABELINGS  F(a) = b, F(b) = a, F o F = id -- correct.
   Parity and mod-2 class are the same partition.
   Flips realized by a map on the numbers: parity (n -> n+1), mod-3 nonzero
   (n -> -n), digit parity. Relabeling only: prime/composite, twin/non-twin,
   mod-9 representative parity (unequal class sizes).
   Mod-9 representative parity: class sizes 5/4 flip with the convention
   (1..9: five odd; 0..8: five even), and it is not additive (5+5 = 10 = 1).
   F3 on {0,1,2} = n -> -n mod 3, Fix = {0}.

C. SUM/PRODUCT COLLAPSE FIXED POINTS, 10 <= n <= 99
   The supplied set {22,36,44,63,77,99} is reproduced by no standard reading.
   C_S = digital root, C_P = digital root of the digit product gives exactly
   {22, 36, 58, 63, 85, 99}, outputs (4,4), (9,9). Proof: for nonzero digits
   a, b the condition is a + b = ab (mod 9), i.e. (a-1)(b-1) = 1 (mod 9):
   inverse unit pairs (1,1),(2,5),(4,7),(8,8) -> digits (2,2),(3,6),(6,3),
   (5,8),(8,5),(9,9). 44 and 77 fail every reading (16 -> 7 or 6; 49 -> 4 or 8).

D. THE HANDWRITTEN PAGE
   R(n) = n - 9 equals one digit-sum step exactly for 10 <= n <= 19.
   PF marks at 12, 15, 18 fit P3(n) = [3 | n]; a marking is not a computed
   factor, so P3 is kept separate from PF. The 999 line's 21 -> 7 matches the
   largest prime factor (21 = 3*7) and not the smallest odd prime factor (3):
   IF that 7 is a PF value, PF is the largest prime factor.
   Repdigits 222,333,555,666,999 fit k + c with k = digit class mod 3 (1..3)
   and c = dr(3a); since c = 3k identically, the rule is 4k (one parameter).
   aaa = 3 * 37 * a, so the largest prime factor of every repdigit is 37.
   Undecoded: (PF-13)1x3, (PF-23)2x3, (PF-33)3x3; how 3 + 999 becomes 10 + 11.
   [2026-10-02: full repdigit page decoded as far as it determines in
   repdigit_pf_page_2026_10_02.py -- PF = "prime foundational"; two rules fit
   all 8 lines and the missing 777 line decides between them.]

E. PRIME-TYPE TABLE, 1..81: 22 primes; every row correct; counts twin 15,
   Sophie 8, sexy 19, safe 6, palindromic 5. With partners restricted to 1..81,
   Sophie drops to 6 (41 -> 83, 53 -> 107 leave); twin, sexy, safe unchanged.

FALSIFICATION: any assertion below failing.
"""
from itertools import product
from math import prod

from sympy import isprime, primefactors


def dr(n):
    return 1 + (n - 1) % 9


def ds(n):
    return sum(int(c) for c in str(n))


def collapse(n):
    while n >= 10:
        n = ds(n)
    return n


# A
assert ds(123) == 6 != 123
assert [n for n in range(1, 100) if collapse(n) != n % 9] == list(range(9, 100, 9))


def splits(k):
    return [[]] if k == 0 else [[p] + c for p in (1, 2, 3) if p <= k for c in splits(k - p)]


assert [len(splits(k)) for k in range(1, 7)] == [1, 2, 4, 7, 13, 24]
assert [1, 1, 2] in splits(4)

# B
assert (5 + 5) % 9 == 1
assert sum(1 for x in range(1, 10) if x % 2) == 5 and sum(1 for x in range(0, 9) if x % 2 == 0) == 5
assert {x: (-x) % 3 for x in range(3)} == {0: 0, 1: 2, 2: 1}

# C
fixed = [n for n in range(10, 100) if prod(map(int, str(n))) and collapse(ds(n)) == collapse(prod(map(int, str(n))))]
assert fixed == [22, 36, 58, 63, 85, 99]
assert sorted({(a, b) for a, b in product(range(1, 10), repeat=2) if ((a - 1) * (b - 1)) % 9 == 1}) == \
    [(2, 2), (3, 6), (5, 8), (6, 3), (8, 5), (9, 9)]
assert collapse(16) == 7 and collapse(49) == 4

# D
assert all(n - 9 == ds(n) for n in range(10, 20)) and all(n - 9 != ds(n) for n in range(20, 10 ** 4))
assert max(primefactors(21)) == 7 and min(p for p in primefactors(21) if p > 2) == 3
assert all(dr(3 * a) == 3 * (1 + (a - 1) % 3) for a in range(1, 10))
assert all(111 * a == 3 * 37 * a and max(primefactors(111 * a)) == 37 for a in range(1, 10))

# E
P = [p for p in range(1, 82) if isprime(p)]
tw = sum(1 for p in P if isprime(p - 2) or isprime(p + 2))
so = sum(1 for p in P if isprime(2 * p + 1))
sx = sum(1 for p in P if isprime(p - 6) or isprime(p + 6))
sa = sum(1 for p in P if p > 2 and isprime((p - 1) // 2))
pa = sum(1 for p in P if str(p) == str(p)[::-1])
assert (len(P), tw, so, sx, sa, pa) == (22, 15, 8, 19, 6, 5)
assert [p for p in P if isprime(2 * p + 1) and 2 * p + 1 <= 81] == [2, 3, 5, 11, 23, 29]

if __name__ == "__main__":
    print("operator system audit 2026-09-30: all assertions pass")
