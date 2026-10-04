# CLASS: AUDIT
"""
Audit of a supplied survey (2026-10-04) of the six prime families audited in
prime_families_wikipedia_supplied_audit_2026_10_04.py. Mathematics only.

CORRECT
  S1 Definitions of all six families; Kummer's criterion (p irregular iff p divides the numerator
     of some B_2k, 2 <= 2k <= p-3); B_32 = 0 mod 37, so (37, 32) is an irregular pair and 37 a
     (p, p-5) prime; Wolstenholme's theorem mod p^3 for p >= 5; same-parity x, y make x^y + y^x
     even, so Leyland primes need opposite parity; isolated primes have relative density 1
     (Brun 1919: twin primes are a density-0 subset).
  S2 HP(8) is reached in 13 steps; 8 -> 222 -> 2337 -> 31941 is right; HP(4) = 211 in 2 steps.
  S3 (p, p-9) primes below 10^4: exactly 67 and 877; (p, p-3) below 2 x 10^4: 16843 only;
     (p, p-5) below 10^4: 37 only. (Test: p | num B_n  iff  sum_{j<p} j^n = 0 mod p^2.)

WRONG
  S4 "S(2) = {4, 6, 8}, |S(2)| = 3": 6 - phi(6) = 4 and 8 - phi(8) = 4. S(2) = {4}.
  S5 "Noncototients, e.g. 8, 10, 12, 14, 16, 20": of these only 10 is a noncototient.
     8 = 12 - 4 (3 solutions), 12 (3 solutions), 14 = 49 - 42 (1), 16 (3), 20 (1).
  S6 "31941 = 3 * 3 * 3549" is not a factorization into primes: 31941 = 3^3 x 7 x 13^2.
  S7 "HP(9) = 773 in 3 steps": HP(9) = 311 (9 -> 33 -> 311, 2 steps). "HP(10) = 11":
     HP(10) = 773 (10 -> 25 -> 55 -> 511 -> 773, 4 steps); 11 is HP(11).
NOT CHECKED HERE
  S8 The current state of the n = 49 home-prime search, the bound "no other Wolstenholme primes
     below 10^9", and "the largest known Leyland prime is 5122^6753 + 6753^5122" (a 2010 record;
     larger ones may have been found since).
CHECKED 2026-10-04 (S8):
  - HP(49): still unknown. Wikipedia "Home prime" (2026): the search is stuck on factoring a 251-digit
    composite in step 119 (since a December 2014 breakthrough at step 117) -- "well over 230 digits"
    and "over 115 iterations" are both consistent.
  - Wolstenholme primes: McIntosh and Roettger searched to 10^9 (2007), later to 10^10; Wikipedia
    reports none other below 10^11. "None other below 10^9" is CORRECT but understated.
  - Largest known Leyland prime: OUT OF DATE. 5122^6753 + 6753^5122 has 25,050 digits (computed
    below); the record is now 104824^5 + 5^104824, 73,269 digits, proved prime by ECPP in February
    2023 (Wikipedia "Leyland number").
FALSIFICATION: any assertion failing.
"""
from sympy import bernoulli, factorint, isprime, primerange, totient


def S(n):
    return [x for x in range(2, n * n + 2) if x - totient(x) == n]


def H(n):
    return int("".join(str(p) * e for p, e in sorted(factorint(n).items())))


def home(n):
    k = 0
    while not isprime(n):
        n, k = H(n), k + 1
    return n, k


def pair(p, m):
    n, p2 = p - m, p * p
    return sum(pow(j, n, p2) for j in range(1, p)) % p2 == 0


assert bernoulli(32).p % 37 == 0                                                         # S1
assert all((x ** y + y ** x) % 2 == 0 for x in range(2, 9) for y in range(2, 9) if x % 2 == y % 2)
assert home(8) == (3331113965338635107, 13) and [H(8), H(222), H(2337)] == [222, 2337, 31941]   # S2
assert home(4) == (211, 2)
assert [p for p in primerange(11, 10000) if pair(p, 9)] == [67, 877]                      # S3
assert [p for p in primerange(7, 20000) if pair(p, 3)] == [16843]
assert [p for p in primerange(7, 10000) if pair(p, 5)] == [37]
assert S(2) == [4] and 6 - totient(6) == 4 and 8 - totient(8) == 4                        # S4
assert {n: len(S(n)) for n in (8, 10, 12, 14, 16, 20)} == {8: 3, 10: 0, 12: 3, 14: 1, 16: 3, 20: 1}   # S5
assert factorint(31941) == {3: 3, 7: 1, 13: 2} and 31941 == 9 * 3549 and not isprime(3549)    # S6
assert home(9) == (311, 2) and home(10) == (773, 4) and home(11) == (11, 0)              # S7
import math                                                                                # S8 digit counts
assert math.floor(6753 * math.log10(5122)) + 1 == 25050
assert math.floor(104824 * math.log10(5)) + 1 == 73269
