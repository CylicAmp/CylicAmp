# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): primes as a spectrum (Mazur & Stein), Gaussian primes on
the 2D grid, and a "geyser" Green's function. Mathematics only.

CORRECT
  G1 Chebyshev's psi(x) jumps by log p at every prime POWER p^k (not only at primes); the
     explicit formula ties those jumps to the zeta zeros -- the duality Mazur & Stein's
     "Prime Numbers and the Riemann Hypothesis" (2016) is built around.
  G2 Odd primes p = 1 mod 4 are sums of two squares: 5 = 1+4, 13 = 4+9, 17 = 1+16, 29 = 4+25;
     primes p = 3 mod 4 (3, 7, 11, 19, 23) are not. Checked for every prime below 10^4.
CORRECTED
  G3 "The norm a^2 + b^2 determines whether a grid point is prime" is incomplete. a + bi is a
     Gaussian prime exactly when (i) its norm is a rational prime (the split primes, and 1 + i),
     or (ii) it is a unit times an inert prime p = 3 mod 4 -- whose norm is p^2, NOT prime.
     So 3 = 3 + 0i is a Gaussian prime with norm 9. Checked against direct factor search.
  G4 2 is neither: it ramifies, 2 = -i(1+i)^2.
NOT ESTABLISHED
  G5 "These act as diagonal vectors on the 3x3 grid" and "this is why {1,2,3} and {1,6,7} have
     different rotational constraints": 5 = (1, 2) is not a diagonal, and no link from Gaussian
     splitting to those triples is given.
  G6 The geyser: an impulse on a graph spreading by the graph Laplacian is the standard heat /
     wave kernel; but the "phase shifts {2,...,9}" are asserted, not derived.
  G7 Whether the Mazur & Stein book itself ends with Gaussian primes was not checked here.
FALSIFICATION: any assertion failing.
"""
from sympy import isprime, primerange

def two_squares(p):
    return any(int((p - a * a) ** 0.5) ** 2 == p - a * a for a in range(int(p ** 0.5) + 1))

for p in primerange(3, 10 ** 4):                                                       # G2
    assert two_squares(p) == (p % 4 == 1)
assert [(1, 2), (2, 3), (1, 4), (2, 5)] == [(a, b) for p in (5, 13, 17, 29)
        for a in range(1, 6) for b in range(a, 6) if a * a + b * b == p]


def gauss_prime_direct(a, b):
    """a+bi is prime iff no factorization into two non-units (search by norm)."""
    n = a * a + b * b
    if n <= 1:
        return False
    for c in range(-int(n ** 0.5) - 1, int(n ** 0.5) + 2):
        for d in range(-int(n ** 0.5) - 1, int(n ** 0.5) + 2):
            m = c * c + d * d
            if 1 < m < n and n % m == 0:
                # (a+bi)/(c+di) = (a+bi)(c-di)/m
                re, im = a * c + b * d, b * c - a * d
                if re % m == 0 and im % m == 0:
                    return False
    return True


def gauss_prime_rule(a, b):
    n = a * a + b * b
    if isprime(n):
        return True
    if a == 0 or b == 0:
        q = abs(a + b)
        return isprime(q) and q % 4 == 3
    return False


for a in range(-12, 13):                                                                # G3
    for b in range(-12, 13):
        assert gauss_prime_direct(a, b) == gauss_prime_rule(a, b), (a, b)
assert gauss_prime_direct(3, 0) and not isprime(9)
assert not gauss_prime_direct(2, 0) and gauss_prime_direct(1, 1)                         # G4
