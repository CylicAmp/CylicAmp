# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): prime endings (1, 3, 7, 9) against digital-root
columns (1, 2, 4, 5, 7, 8), and "the roots are forced to alternate / constantly jump across
the even-odd column divide". Mathematics only.

CORRECT
  E1 Every prime > 5 ends in 1, 3, 7 or 9 (otherwise 2 or 5 divides it). Forced.
  E2 Every prime > 3 has root 1, 2, 4, 5, 7 or 8 (otherwise 3 divides it). Forced; filed in
     prime_digital_root_supplied_audit_2026_10_03.py and prime_engine.py.
  E3 The table: 7->7, 11->2, 13->4, 17->8, 19->1, 23->5, 29->2, 31->4.
  E4 Roots split about evenly between the "even" columns {2, 4, 8} and the "odd" columns
     {1, 5, 7}: 50.0% / 50.0% of primes 7..10^6 (to within 0.1%).

WRONG
  E5 "Forced to alternate" / "constantly jump back and forth": the table itself has 11, 13,
     17 all in even columns and 19, 23 both odd. Over consecutive primes 7..10^6 the root
     parity changes on 55.3% of steps and stays on 44.7% -- not an alternation (that would be
     100%). The excess over 50% is real and known: consecutive primes avoid repeating their
     residue class (Lemke Oliver & Soundararajan, "Unexpected biases in the distribution of
     consecutive primes", PNAS 2016). (A first draft of this file guessed 49.5%; the
     assertion caught it.)

ADDED
  E6 Ending and root together fix the prime mod 90 (lcm(10, 9) = 90). The 4 endings x 6 roots
     = 24 combinations are exactly the 24 = phi(90) classes coprime to 90, and the primes
     fill them evenly (Dirichlet): each between 4.13% and 4.21% up to 10^6 (1/24 = 4.17%).
     So ending and root are independent -- neither "locks" the other.
FALSIFICATION: any assertion failing.
"""
from collections import Counter
from math import gcd

from sympy import primerange

dr = lambda n: 1 + (n - 1) % 9
P = list(primerange(7, 10 ** 6))
assert {p % 10 for p in P} == {1, 3, 7, 9}                                                 # E1
assert {dr(p) for p in P} == {1, 2, 4, 5, 7, 8}                                            # E2
assert [dr(p) for p in (7, 11, 13, 17, 19, 23, 29, 31)] == [7, 2, 4, 8, 1, 5, 2, 4]       # E3
even = lambda p: dr(p) in (2, 4, 8)
share_even = sum(map(even, P)) / len(P)
assert abs(share_even - 0.5) < 0.001                                                       # E4
flips = sum(even(a) != even(b) for a, b in zip(P, P[1:])) / (len(P) - 1)
assert 0.55 < flips < 0.56 and [even(p) for p in (11, 13, 17)] == [True] * 3               # E5
cells = Counter((p % 10, dr(p)) for p in P)                                                # E6
assert len(cells) == 24 == sum(1 for r in range(90) if gcd(r, 90) == 1)
assert all(0.0413 < c / len(P) < 0.0421 for c in cells.values())

if __name__ == "__main__":
    print(f"even-column share {share_even:.4f}; parity changes on {flips:.4f} of steps")
