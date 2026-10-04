# CLASS: AUDIT
"""
Audit of supplied text (2026-10-03): "This is the Green-Tao theorem ..." with its
statement, condition, method, asymptotic, and a claimed link to this repo.

CORRECT
  G1 Statement: the primes contain k-term arithmetic progressions for every k
     (Green & Tao, Annals of Math. 167 (2008); arXiv 2004).
  G2 Condition: any subset of the primes with positive upper relative density contains
     k-term APs for every k. That is the theorem's actual form.
  G3 Method: a relative ("transference") Szemeredi theorem -- the primes sit with positive
     density inside a pseudorandom majorant built from Goldston-Yildirim sieve weights.
  G4 Asymptotic: #k-term prime APs up to N ~ S_k N^2 / (log N)^k. Green-Tao "Linear
     equations in primes" (2010) proved it conditional on two conjectures, proved in 2012
     (Mobius-nilsequences by Green-Tao; inverse Gowers by Green-Tao-Ziegler). Unconditional.

INCOMPLETE
  G5 "Local factors (p/(p-1))^(k-1)": that is only part of each factor. The full local
     factor, derived and checked below by counting (a, d) mod p:
        p <  k:  (1/p)         * (p/(p-1))^(k-1)
        p >= k:  (1 - (k-1)/p) * (p/(p-1))^(k-1)
     The p < k case says d must be 0 mod p -- the same fact that forces 23# | d in the
     AP-27 record (ap27_record_audit_2026_10_03.py).

NOT ESTABLISHED
  G6 "Connects to the divisor work ... exactly the kind of arithmetic function your divisor
     machinery handles": the singular series is an Euler product over primes; the T245
     divisor work is about the smallest divisors of one n. An analogy, not a link.
  G7 "Filed as reference ... verified": nothing was in the repo. This file is the first.

PRIOR USE IN THIS REPO, CORRECTED
  math/theorems/goldbach_proof_attempt_gf37.py line 69 says "By the Green-Tao / Dirichlet
  density argument, this covers 'most' n" for n - 37 prime. Green-Tao says nothing about
  that: n - 37 is prime for a density-zero set of n (prime number theorem), so it covers
  almost no n. Checked below for n <= 10^5: 19.2% of EVEN n (the Goldbach case).
  (A first version of this file counted all n, odd included, and reported 9.6%; odd n
  make n - 37 even, so that figure was diluted. The even-n share is the right one.)
FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F
from sympy import isprime


def local_count(p, k):
    """Proportion of (a, d) mod p with a + j d != 0 mod p for j = 0..k-1."""
    good = sum(1 for a in range(p) for d in range(p) if all((a + j * d) % p for j in range(k)))
    return F(good, p * p)


def local_factor(p, k):
    return local_count(p, k) / F(p - 1, p) ** k


def formula(p, k):
    base = F(p, p - 1) ** (k - 1)
    return base * (F(1, p) if p < k else 1 - F(k - 1, p))


for k in range(2, 9):                                                   # G5
    for p in (2, 3, 5, 7, 11, 13):
        assert local_factor(p, k) == formula(p, k), (p, k)
assert local_factor(5, 3) != F(5, 4) ** 2                                # bare (p/(p-1))^(k-1) is not it
# p < k forces d = 0 mod p: every surviving (a, d) has d = 0
assert all(d == 0 for a in range(5) for d in range(5) if all((a + j * d) % 5 for j in range(7)))

N = 10 ** 5                                                             # goldbach file, line 69
evens = range(40, N + 1, 2)
share = sum(1 for n in evens if isprime(n - 37)) / len(evens)
assert 0.19 < share < 0.2, share

if __name__ == "__main__":
    print("G5 local factors verified for k = 2..8, p <= 13")
    print(f"goldbach file: n - 37 prime for {share:.1%} of even n <= {N} -- not 'most'")
