# CLASS: AUDIT
"""
Audit of supplied text (2026-10-03, another assistant): primes past 3 have digital root in
{1, 2, 4, 5, 7, 8}, "forever", with a table of large primes and a nonagon picture.

CORRECT
  D1 Every table row: 101 -> 2; 359 -> 17 -> 8; 541 (100th prime) -> 1; 7919 (1000th) ->
     26 -> 8; 104729 (10000th) -> 23 -> 5. Ranks and primality checked.
  D2 Primes p > 3 never have digital root 3, 6 or 9, for all p: dr(n) is n mod 9 (9 for 0),
     and dr in {3, 6, 9} <=> 3 | n. Forced, not a pattern found by looking.
  D3 3, 6, 9 on a 9-point wheel are equally spaced: an equilateral triangle.
PRIOR ART: math/primes/prime_engine.py already states it -- "DR filter is 6k+-1 wheel sieve":
  {n > 1 odd, dr(n) not in {3,6,9}} = {6k +- 1}.

OVERSTATED
  D4 "Primes are forced to bounce between 1, 2, 4, 5, 7, 8": so is EVERY number not divisible
     by 3 -- 25, 35, 49, 77, 91 included. The six roots carry no information about primality
     beyond "3 does not divide n".
  D5 "Instantly see its structural core: 104,729 belongs to the 5-family": the family is
     104729 mod 9. Primes split evenly among the six roots (Dirichlet; counted below up to
     10^6: each within 0.2% of 1/6), so the label does not single a prime out.
  D6 "You are completely right -- it never stops": the infinitude of primes (Euclid) and D2
     are both true, but neither is a discovery in this text; the opener agrees before checking.
FALSIFICATION: any assertion failing.
"""
from sympy import isprime, prime, primerange

dr = lambda n: 1 + (n - 1) % 9
ROWS = [(101, 2), (359, 8), (541, 1), (7919, 8), (104729, 5)]
assert all(isprime(p) and dr(p) == r for p, r in ROWS)                         # D1
assert (prime(100), prime(1000), prime(10000)) == (541, 7919, 104729)
assert all((dr(n) in (3, 6, 9)) == (n % 3 == 0) for n in range(1, 100000))      # D2
assert {(3 * k) % 9 for k in (1, 2, 3)} == {3, 6, 0}                            # D3: spacing 3
assert [n for n in (25, 35, 49, 77, 91) if dr(n) in (1, 2, 4, 5, 7, 8)] == [25, 35, 49, 77, 91]  # D4
counts = {r: 0 for r in (1, 2, 4, 5, 7, 8)}
for p in primerange(5, 10 ** 6):
    counts[dr(p)] += 1
total = sum(counts.values())
assert all(abs(c / total - 1 / 6) < 0.002 for c in counts.values()), counts    # D5

if __name__ == "__main__":
    print("table correct; roots 3,6,9 excluded <=> 3 does not divide n (forced)")
    print("primes 5..10^6 by root:", counts)
