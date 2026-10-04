# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): digital roots of the primes from 11 to 107 -- "2-4-8"
blocks at 11,13,17 and 101,103,107, a "mirror" centred on 53, pair sums "all in the 5-7-9
family", an "inversion law of 90". Mathematics only.

CORRECT
  M1 Roots: 11,13,17 -> 2,4,8 and 101,103,107 -> 2,4,8; 101 - 11 = 90.
     The roots repeating is forced: 90 = 0 mod 9, so dr(p + 90) = dr(p) for every p.
     What is NOT forced is that 101, 103, 107 are all prime.
  M2 Roots 19..47 = 1,5,2,4,1,5,7,2; 53 -> 8; and the eight pair sums out from 53
     (47+59, 43+61, ..., 19+89) have roots 7,5,9,9,5,9,7,9.

WRONG
  M3 The halves are not equal: between 17 and 101 there are 8 primes below 53 and 9 above
     (59,61,67,71,73,79,83,89,97). The "upward slope" lists 8 roots and drops 97 (root 7).
     The interval 11..101 holds 22 primes, not 21.
  M4 "101 is the modular reflection of 11 across a base-90 grid": 101 = 11 + 90 is a
     TRANSLATION. The reflection of 11 mod 90 is -11 = 79.
  M5 "The second block is forced to appear at 101 ... infinite, self-correcting balance":
     the shifted triple survives once more (191, 193, 197 all prime) and fails at the next
     step (287 = 7 x 41). Primality is not forced by the 90-shift.
  M6 "Every pairing collapses into the 5-7-9 family" as a law: {5,7,9} is not a natural class
     (mod 3 they are 2, 1, 0). Tested against every centre prime below 2*10^6 with eight pairs
     each side: the pair sums use at most 3 distinct roots for 3,580 of 148,915 centres (2.4%);
     the other 97.6% use 4 to 8. 53 is one of the uncommon centres, picked after looking --
     not an instance of a law.
FALSIFICATION: any assertion failing.
"""
from collections import Counter

from sympy import isprime, primerange

dr = lambda n: 1 + (n - 1) % 9
P = list(primerange(11, 108))
assert [dr(p) for p in (11, 13, 17, 101, 103, 107)] == [2, 4, 8, 2, 4, 8] and 101 - 11 == 90   # M1
assert all(dr(n + 90) == dr(n) for n in range(1, 10000))
low = [p for p in P if 17 < p < 53]
high = [p for p in P if 53 < p < 101]
assert [dr(p) for p in low] == [1, 5, 2, 4, 1, 5, 7, 2] and dr(53) == 8                       # M2
pairs = list(zip(reversed(low), high))
assert [dr(a + b) for a, b in pairs] == [7, 5, 9, 9, 5, 9, 7, 9]
assert len(low) == 8 and len(high) == 9 and high[-1] == 97 and dr(97) == 7                     # M3
assert len([p for p in P if p <= 101]) == 22
assert (-11) % 90 == 79 and 101 % 90 == 11                                                     # M4
assert all(isprime(x) for x in (191, 193, 197)) and 287 == 7 * 41                              # M5

Q = list(primerange(5, 2 * 10 ** 6))                                                           # M6
sizes = Counter(len({dr(Q[c - i] + Q[c + i]) for i in range(1, 9)}) for c in range(8, len(Q) - 8))
few = sizes[1] + sizes[2] + sizes[3]
assert sum(sizes.values()) == 148915 and few == 3580 and few / 148915 < 0.025

if __name__ == "__main__":
    print("pair-sum roots around 53:", [dr(a + b) for a, b in pairs])
    print(f"centres with <= 3 distinct pair-sum roots: {few} of {sum(sizes.values())}")
