"""
Prime splitting in Z[omega], omega = e^(2*pi*i/3) = (-1 + sqrt(-3)) / 2.

Eisenstein norm:  N(a, b) = a^2 - a*b + b^2       (norm of a + b*omega)
Loeschian form:   L(x, y) = x^2 + x*y + y^2       (= N(x, -y))

Every rational prime p satisfies exactly one:
  p = 3           ramified   chi_-3(p) =  0
  p ≡ 1 mod 3    split       chi_-3(p) = +1  =>  p = N(a,b) for some a,b in Z
  p ≡ 2 mod 3    inert       chi_-3(p) = -1  =>  p*Z[omega] remains prime

Representation count:
  r(p) = #{(a,b) in Z^2 : N(a,b) = p}
  r(p) = 12 if split, 0 if inert, 6 if p=3.

Sign fix: if L(x,y)=p (x,y found by Loeschian search), then N(x,-y)=p.

Cross-checked against sympy.isprime; pi(x) verified at x=10^3,10^4,10^5.
Counts below 5000: split=330, inert=338, ramified=1.
Dirichlet balance below 10^5: split=4784, inert=4807 (including p=2).
"""

from sympy import isprime as sympy_isprime, primerange


def norm_e(a: int, b: int) -> int:
    """Eisenstein norm N(a + b*omega) = a^2 - a*b + b^2."""
    return a * a - a * b + b * b


def loeschian(x: int, y: int) -> int:
    """L(x,y) = x^2 + x*y + y^2 = N(x, -y)."""
    return x * x + x * y + y * y


def chi_minus3(p: int) -> int:
    """
    Kronecker character (-3 | p).
    0 if p=3, +1 if p≡1 mod 3, -1 if p≡2 mod 3.
    """
    if p == 3:
        return 0
    return 1 if p % 3 == 1 else -1


def split_class(p: int) -> str:
    c = chi_minus3(p)
    if c == 0:
        return "ramified"
    return "split" if c == 1 else "inert"


def norm_witness(p: int):
    """
    Return (a, b) with N(a,b)=p and a,b != both 0, or None if inert/not prime.
    Searches the Eisenstein norm form directly (not Loeschian).
    """
    bound = int(p ** 0.5) + 2
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            if (a, b) != (0, 0) and norm_e(a, b) == p:
                return (a, b)
    return None


def rep_count(p: int) -> int:
    """#{(a,b) in Z^2 : N(a,b) = p}."""
    bound = int(p ** 0.5) + 2
    return sum(
        1
        for a in range(-bound, bound + 1)
        for b in range(-bound, bound + 1)
        if norm_e(a, b) == p
    )


def splitting_table(bound: int = 5000) -> dict:
    """
    For all primes p <= bound, classify and (for split) record a norm witness.
    Returns {"split": [...], "inert": [...], "ramified": [...]}
    with each entry (p, witness_or_None).
    """
    result = {"split": [], "inert": [], "ramified": []}
    for p in primerange(2, bound + 1):
        cls = split_class(p)
        w = norm_witness(p) if cls == "split" else None
        result[cls].append((p, w))
    return result


def verify_primality_crosscheck(limit: int = 20000) -> int:
    """
    Compare own trial-division against sympy.isprime for all n in [2, limit].
    Returns count of mismatches (0 expected).
    """
    def own_is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        return all(n % i for i in range(3, int(n ** 0.5) + 1, 2))

    return sum(
        1 for n in range(2, limit + 1)
        if own_is_prime(n) != sympy_isprime(n)
    )


def verify_prime_counts() -> list:
    """
    Cross-check pi(x) against known values.
    Returns list of (x, computed, known, ok).
    """
    known = {1000: 168, 10_000: 1229, 100_000: 9592}
    results = []
    for x, k in sorted(known.items()):
        c = sum(1 for _ in primerange(2, x + 1))
        results.append((x, c, k, c == k))
    return results


SPLIT_INERT_BELOW_5000 = {"split": 330, "inert": 338, "ramified": 1}
DIRICHLET_BELOW_100000 = {"split": 4784, "inert": 4807}
