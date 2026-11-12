# CLASS: COMPUTATION
"""
The safe prime generator (exports/safe_primes.py), built 2026-11-12: the second of the applications offered on
2026-10-28 (check character, safe primes, Rule 30).

A Sophie Germain prime p has 2p + 1 prime; 2p + 1 is a safe prime -- what Diffie-Hellman key exchange runs on
(RFC 3526, RFC 7919). The list is read off the walk's table: entry k says whether 2k + 1 is prime, and 2p + 1 for
p = 2k + 1 is entry 2k + 1, so a Sophie Germain prime is entries k and 2k + 1 both prime.

CHECKED HERE (CI): the program's own --test --
  counts below 10 .. 10^7 = OEIS A092816 (3, 10, 37, 190, 1171, 7746, 56032); first 40 of A005384 and A005385;
  forced: above 3 every p leaves 2 by 3 (root 2, 5 or 8), every safe prime above 7 leaves 11 by 12;
  the Pocklington step is right on 10,421 cases; the Miller-Rabin trap 318665857834031151167461 (bases 2 .. 37
  fooled, 2 .. 41 not); five RFC Diffie-Hellman primes are safe primes; made safe primes of 16, 64, 128, 256 bits --
and against sympy here: every Sophie Germain prime below 10^6, and the made primes.

CHECKED OUTSIDE CI (2026-11-12): fresh 512-, 1024- and 2048-bit safe primes made in 0.3 s, 8.8 s and 146.7 s;
  p and q prime by sympy and by OpenSSL (openssl prime) for all three. The RFC 3526 hex values were read from the RFC
  and matched against its own formulas (2^b - 2^(b-64) - 1 + 2^64 x ([2^e pi] + c)) for all six sizes.
  q leaves 3 or 7 by 8 about equally: 3833 / 3911 below 10^6, 140 / 160 over 300 made 96-bit ones.

FALSIFICATION: any assertion failing.
"""
import pathlib
import random
import sys

import sympy

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "exports"))
import safe_primes as S  # noqa: E402

assert S.run_tests()

sg = S.sophie_germain_list(10 ** 6)
brute = [p for p in sympy.primerange(2, 10 ** 6) if sympy.isprime(2 * p + 1)]
assert sg == brute and len(sg) == 7746

for bits, seed in ((96, 11), (160, 12), (200, 13)):
    q, p = S.safe_prime(bits, rng=random.Random(seed))
    assert q.bit_length() == bits and q == 2 * p + 1 and sympy.isprime(p) and sympy.isprime(q)

for n in (25, 49, 341, 561, 1105, 1729, 2465, 2821, 6601, 8911, 318665857834031151167461):
    assert S.is_prime(n) == sympy.isprime(n) is False

if __name__ == "__main__":
    print("safe primes: OEIS counts to 10^7, five RFC groups, made primes confirmed by sympy")
