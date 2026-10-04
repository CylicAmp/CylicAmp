# CLASS: AUDIT
"""
Audit of supplied lists (2026-10-04, Wikipedia "List of prime numbers"): highly cototient,
home, irregular, (p, p-3) / (p, p-5) / (p, p-9) irregular, isolated, Leyland primes. Every list
recomputed from its definition. Mathematics only.

ALL CORRECT
  F1 Highly cototient primes <= 2000: 2 23 47 59 83 89 113 167 269 389 419 509 659 839 1049 1259
     1889 (A105440). Cototient counts over all x <= 2000^2, which covers every x with
     x - phi(x) <= 2000 (a composite x has x - phi(x) >= sqrt x).
  F2 Home primes HP(2) .. HP(48): all 47 values match (A037274), including HP(8) =
     3331113965338635107 and HP(48) = 6161791591356884791277.
  F3 Irregular primes up to 613 match (p divides the numerator of some B_k, k = 2..p-3). The list
     stops at 613 by truncation; 617 and 619 are next.
  F4 (p, p-3): 16843 and 2124679 -- checked through Wolstenholme's criterion
     C(2p-1, p-1) = 1 (mod p^4), which is equivalent to p | B_{p-3}. (Only these two are known.)
     (p, p-5): 37 divides B_32. (p, p-9): 67 divides B_58 and 877 divides B_868.
  F5 Isolated primes below 1000 match (A007510; 2 included, as neither 0 nor 4 is prime).
  F6 Leyland primes up to 4.3 x 10^37 match and the list is complete in that range
     (a^b + b^a, a >= b >= 2, enumerated up to the bound).

ALREADY IN THE REPO (the list itself involves 37)
  37 is the first irregular prime and (37, 32) its irregular pair: theorem_365_37_first_irregular_
  prime.py; theorem_366 records that "cyclotomic membership" of 37 is vacuous as a distinction.
FALSIFICATION: any assertion failing.
"""
import numpy as np
from sympy import bernoulli, factorint, isprime, primerange

N = 2000                                                                                  # F1
X = N * N + 10
phi = np.arange(X, dtype=np.int64)
for p in primerange(2, X):
    phi[p::p] -= phi[p::p] // p
cot = np.arange(X) - phi
cnt = np.bincount(cot[2:][cot[2:] <= N], minlength=N + 1)
best, hc = 0, []
for k in range(2, N + 1):
    if cnt[k] > best:
        best, hc = cnt[k], hc + [k]
assert [k for k in hc if isprime(k)] == [2, 23, 47, 59, 83, 89, 113, 167, 269, 389, 419, 509, 659, 839, 1049, 1259, 1889]


def hp(n):                                                                                # F2
    while not isprime(n):
        n = int("".join(str(p) * e for p, e in sorted(factorint(n).items())))
    return n


HP = [2, 3, 211, 5, 23, 7, 3331113965338635107, 311, 773, 11, 223, 13, 13367, 1129, 31636373, 17, 233, 19,
      3318308475676071413, 37, 211, 23, 331319, 773, 3251, 13367, 227, 29, 547, 31, 241271, 311, 31397, 1129,
      71129, 37, 373, 313, 3314192745739, 41, 379, 43, 22815088913, 3411949, 223, 47, 6161791591356884791277]
assert [hp(n) for n in range(2, 49)] == HP

IRR = [37, 59, 67, 101, 103, 131, 149, 157, 233, 257, 263, 271, 283, 293, 307, 311, 347, 353, 379, 389, 401, 409,
       421, 433, 461, 463, 467, 491, 523, 541, 547, 557, 577, 587, 593, 607, 613]
irr = [p for p in primerange(3, 620) if any(bernoulli(k).p % p == 0 for k in range(2, p - 2, 2))]
assert irr == IRR + [617, 619]                                                            # F3


def wolstenholme(p):
    m, num, den = p ** 4, 1, 1
    for i in range(1, p):
        num, den = num * (p + i) % m, den * i % m
    return num * pow(den, -1, m) % m == 1


assert wolstenholme(16843) and wolstenholme(2124679)                                     # F4
assert bernoulli(32).p % 37 == 0 and bernoulli(58).p % 67 == 0 and bernoulli(868).p % 877 == 0

iso = [p for p in primerange(2, 1000) if not isprime(p - 2) and not isprime(p + 2)]      # F5
assert iso[:6] == [2, 23, 37, 47, 53, 67] and iso[-3:] == [983, 991, 997] and len(iso) == 99

TOP = 43143988327398957279342419750374600193                                              # F6
ley = sorted({a ** b + b ** a for a in range(2, 130) for b in range(2, a + 1)
              if a ** b + b ** a <= TOP and isprime(a ** b + b ** a)})
assert ley == [17, 593, 32993, 2097593, 8589935681, 59604644783353249,
               523347633027360537213687137, TOP]
