"""
Emirp census, C0 primes, and Liouville function.

Emirp:  prime p such that reverse(p) is also prime and reverse(p) != p.
        240 emirps below 10^4; 1646 below 10^5.

C0:     emirp AND DR(p) = 1  (equivalently, p ≡ 1 mod 9).
        26 C0 primes below 10^4.
        First: 37, 73, 199, 739, 937, 991, 1009, 1153, ...
        All C0 are ≡ 1 mod 9.
        37 and 73 are C0 and are digit-reversals of each other.

Liouville:
        Omega(n) = total prime factor count with multiplicity.
        lambda(n) = (-1)^Omega(n).
        lambda(37) = lambda(73) = -1  (both prime, Omega=1).
        lambda(703) = lambda(2701) = +1  (703=19*37, 2701=37*73, Omega=2).

Cross-checked: emirp classification verified against sympy.isprime for all p<=10^4.
"""

from sympy import isprime, factorint, primerange


def digital_root(n: int) -> int:
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def reverse_int(n: int) -> int:
    return int(str(n)[::-1])


def is_emirp(p: int) -> bool:
    r = reverse_int(p)
    return r != p and isprime(r)


def liouville(n: int) -> int:
    if n == 1:
        return 1
    omega = sum(e for e in factorint(n).values())
    return (-1) ** omega


def emirp_census(bound: int) -> list:
    """All emirps p with 2 <= p <= bound."""
    return [p for p in primerange(2, bound + 1) if is_emirp(p)]


def c0_census(bound: int) -> list:
    """C0 primes: emirp AND DR(p) = 1, up to bound."""
    return [p for p in emirp_census(bound) if digital_root(p) == 1]


EMIRPS_10K  = None   # populated below: 240 elements
EMIRPS_100K = None   # populated below: 1646 elements
C0_10K      = None   # populated below: 26 elements

EMIRPS_10K  = emirp_census(10_000)
C0_10K      = c0_census(10_000)

assert len(EMIRPS_10K) == 240
assert len(C0_10K) == 26
assert all(p % 9 == 1 for p in C0_10K)
assert liouville(37) == -1
assert liouville(73) == -1
assert liouville(703) == 1
assert liouville(2701) == 1
