# CLASS: AUDIT
"""
Audit of supplied code and text (2026-10-04): digital roots of 246, 248, 485, 369, 469 and
a claimed link to the roots of the primes 11..101. Mathematics only. (The "mirror at 53"
part repeats text audited in prime_root_mirror_53_supplied_audit_2026_10_04.py.)

CORRECT
  N1 Roots: 246 -> 3, 248 -> 5, 485 -> 8, 369 -> 9, 469 -> 1 (the code's dr is right).
  N2 The 21 roots listed are exactly the roots of the 21 primes 11..97.

WRONG
  N3 Their sum is 98 (root 8), not 93 (root 3). Including 101 (22 primes, "11 to 101"):
     100, root 1. Either way the "base-3 framework" match with 246 fails.
  N4 "248 -> 485: the values swap positions and shift": digits 2,4,8 -> 4,8,5 is not a swap.
  N5 "246 at the front charts the shift out of the 3-6-9 exclusion zone into the active
     5 and 8 tracks": none of the five numbers is prime (factorizations below), so none
     sits on any prime track; root 5 and 8 are shared by every number = 5 or 8 mod 9.
  N6 369 and 469 are in the code but not mentioned in the text.

CONNECTION ALREADY IN THE REPO (forced)
  246 = 2 x 123 and 369 = 3 x 123: two rows of the T327 counting stack 123 / 246 / 369
  (theorem_327_counting_stack_123_246_369_gf37.py). 248 has digits 2, 4, 8 -- the root
  pattern of 11, 13, 17.
FALSIFICATION: any assertion failing.
"""
from sympy import factorint, isprime, primerange

dr = lambda n: 9 if n % 9 == 0 else n % 9
assert [dr(n) for n in (246, 248, 485, 369, 469)] == [3, 5, 8, 9, 1]                     # N1
L = [2, 4, 8, 1, 5, 2, 4, 1, 5, 7, 2, 8, 5, 7, 4, 8, 1, 7, 2, 8, 7]
assert L == [dr(p) for p in primerange(11, 98)] and len(L) == 21                          # N2
assert sum(L) == 98 != 93 and dr(98) == 8                                                 # N3
assert sum(dr(p) for p in primerange(11, 102)) == 100 and len(list(primerange(11, 102))) == 22
assert sorted("248") != sorted("485")                                                      # N4
assert not any(isprime(n) for n in (246, 248, 485, 369, 469))                             # N5
assert [factorint(n) for n in (246, 248, 485, 369, 469)] == [
    {2: 1, 3: 1, 41: 1}, {2: 3, 31: 1}, {5: 1, 97: 1}, {3: 2, 41: 1}, {7: 1, 67: 1}]
assert 246 == 2 * 123 and 369 == 3 * 123                                                  # T327 rows
