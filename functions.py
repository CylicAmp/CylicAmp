"""
functions.py -- the shared functions used across the repository.

Before this module existed, the same few functions were re-written from
scratch in hundreds of files (dr in 486 files, is_prime in 128, ...).
They are defined once here, and files import them.

The copies were NOT all identical. dr, for instance, was written with nine
different behaviours: 0 maps to 0 in some files and to 9 in others, and
negative inputs are handled four different ways. Each behaviour is kept
here as its own named function, so a file that imports one gets exactly the
behaviour its own copy had. The table in each docstring shows the difference.

    Behaviour on          0    9   -5   -9
    dr                    0    9    5    9    negatives by absolute value
    dr_signed             0    9    4    9    Python's (n-1) % 9 + 1 on n
    dr_pos                0    9    0    0    n <= 0 gives 0
    dr_strict            err   9  err  err    ValueError for n <= 0
    dr9                   9    9    5    9    0 gives 9, negatives by abs
    dr9_signed            9    9    4    9    (n-1) % 9 + 1, no special case
    dr9_pos               9    9    9    9    n <= 0 gives 9
    dr_iter               0    9   -5   -9    repeated digit sum; n < 10 returned as is
    dr9_iter              9    9   -5   -9    as dr_iter, but 0 gives 9

The 12 orbits of x -> 26x mod 37 are defined once below (ORBITS). The repo
used two naming schemes for the same 12 orbits; ORBIT_NAMES_V1 records the
earlier names, so both vocabularies are tied to one partition.

Built by tools/split_functions.py, which only swaps a file's copy for one of
these when the copy's behaviour matches exactly on the tested inputs and the
file's printed output is unchanged afterwards.
"""
import math


# -- digital root -------------------------------------------------------------

def dr(n):
    """Digital root; 0 -> 0; negative n uses |n|."""
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9


def dr_signed(n):
    """Digital root; 0 -> 0; negative n uses Python's modulo (dr(-5) = 4)."""
    return 0 if n == 0 else 1 + (n - 1) % 9


def dr_pos(n):
    """Digital root for n > 0; any n <= 0 gives 0."""
    return (n - 1) % 9 + 1 if n > 0 else 0


def dr_strict(n):
    """Digital root for n > 0; raises ValueError for n <= 0."""
    if n <= 0:
        raise ValueError
    return (n - 1) % 9 + 1


def dr9(n):
    """Digital root with 0 -> 9; negative n uses |n|."""
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def dr9_signed(n):
    """(n - 1) % 9 + 1 for every n: 0 -> 9, dr(-5) = 4."""
    return (n - 1) % 9 + 1


def dr9_pos(n):
    """Digital root for n > 0; any n <= 0 gives 9."""
    return 1 + (n - 1) % 9 if n > 0 else 9


def dr_iter(n):
    """Repeated decimal digit sum until below 10; n < 10 (incl. negatives) returned unchanged."""
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n


def dr9_iter(n):
    """As dr_iter, but a result of 0 becomes 9."""
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n if n != 0 else 9


# -- digit sum ----------------------------------------------------------------

def digit_sum(n):
    """Sum of decimal digits of n >= 0 (a minus sign raises ValueError)."""
    return sum(int(c) for c in str(n))


def digit_sum_abs(n):
    """Sum of decimal digits of |n|."""
    return sum(int(c) for c in str(abs(n)))


def digit_sum_str(s):
    """Sum of the digits in a digit string."""
    return sum(int(c) for c in s)


# -- primality ----------------------------------------------------------------

def is_prime(n):
    """Trial division. True iff n is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    r = math.isqrt(n) if isinstance(n, int) else int(n ** 0.5)
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True


# -- the 12 orbits of x -> 26x on GF(37)* ------------------------------------
#
# The same partition appears under two naming schemes in the repo. ORBITS uses
# the current names; ORBIT_NAMES_V1 gives the earlier name for each orbit.

ORBITS = {
    'IC':      {1, 10, 26},
    'DARK_A':  {2, 15, 20},
    'C3':      {3, 4, 30},
    'CAS_EXT': {5, 13, 19},
    'TESLA':   {6, 8, 23},
    'D7':      {7, 33, 34},
    'SA_ST_A': {9, 12, 16},
    'NEG_H':   {11, 27, 36},
    'C9':      {14, 29, 31},
    'NQR17':   {17, 22, 35},
    'SEED':    {18, 24, 32},
    'SA_ST_B': {21, 25, 28},
}

ORBIT_NAMES_V1 = {
    'IC': 'IC', 'DARK_A': 'DARK_A', 'C3': 'SOVEREIGN_SPIRAL', 'CAS_EXT': 'NQR_5',
    'TESLA': 'TESLA_ORB', 'D7': 'D7', 'SA_ST_A': 'SA_ORB', 'NEG_H': 'ORBIT_11',
    'C9': 'NQR_14', 'NQR17': 'NQR_17', 'SEED': 'SEED_ORB', 'SA_ST_B': 'OUTLIER_ORB',
}

_ORBIT_OF_RESIDUE = {r: name for name, s in ORBITS.items() for r in s}


def _orbit(x, missing, names=None):
    r = x % 37
    if r == 0:
        return 'SEAM'
    name = _ORBIT_OF_RESIDUE.get(r)
    if name is None:                       # only for inputs like 3.5
        return missing(x, r)
    return names[name] if names else name


def _raise(exc):
    def f(x, r):
        raise exc(x)
    return f


# The variants differ only on inputs that are not whole numbers (e.g. 3.5);
# on integers they all agree. Each keeps the fallback its source copies had.

def orbit_of(x):
    """Orbit name of x mod 37 ('SEAM' for 0); ValueError if unclassifiable."""
    return _orbit(x, _raise(ValueError))


def orbit_of_next(x):
    """As orbit_of; StopIteration if unclassifiable."""
    return _orbit(x, _raise(StopIteration))


def orbit_of_assert(x):
    """As orbit_of; AssertionError if unclassifiable."""
    return _orbit(x, _raise(AssertionError))


def orbit_of_key(x):
    """As orbit_of; KeyError if unclassifiable."""
    return _orbit(x, _raise(KeyError))


def orbit_of_unknown(x):
    """As orbit_of; 'UNKNOWN' if unclassifiable."""
    return _orbit(x, lambda x, r: 'UNKNOWN')


def orbit_of_q(x):
    """As orbit_of; '?' if unclassifiable."""
    return _orbit(x, lambda x, r: '?')


def orbit_of_v1(x):
    """Earlier orbit names (ORBIT_NAMES_V1); '?' if unclassifiable."""
    return _orbit(x, lambda x, r: '?', ORBIT_NAMES_V1)


# -- quadratic character ------------------------------------------------------
#
# Two different functions were both called `legendre` in the repo:
#   * Euler's criterion as a raw residue: a^((p-1)/2) mod p, i.e. 0, 1 or p-1
#     (NOT -1: a non-residue gives p-1);
#   * the Legendre symbol itself: 0, 1 or -1.
# Each comes with p required or p defaulting to 37, as the source copies had.

def euler_criterion(a, p):
    """a^((p-1)/2) mod p: 0, 1, or p-1 for prime p."""
    return pow(a, (p - 1) // 2, p)


def euler_criterion37(a, p=37):
    """As euler_criterion, p defaulting to 37."""
    return pow(a, (p - 1) // 2, p)


def legendre(a, p):
    """Legendre symbol (a/p): 0 if p | a, else 1 or -1 by Euler's criterion."""
    if a % p == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def legendre37(a, p=37):
    """As legendre, p defaulting to 37."""
    if a % p == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def legendre_by_residue(a, p):
    """0 if a^((p-1)/2) = 0, -1 if it is p-1, else 1 (agrees with legendre for prime p)."""
    r = pow(a, (p - 1) // 2, p)
    return 0 if r == 0 else -1 if r == p - 1 else 1


# -- sieve of Eratosthenes ------------------------------------------------------
#
# The copies named `sieve` returned three different things; each is kept.

def sieve_flags(n):
    """bytearray f of length n+1 with f[k] = 1 iff k is prime."""
    is_p = bytearray([1]) * (n + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i::i] = bytearray(len(is_p[i * i::i]))
    return is_p


def primes_upto(n):
    """List of primes <= n, ascending."""
    f = sieve_flags(n)
    return [i for i in range(2, n + 1) if f[i]]


def primes_upto_set(n):
    """Set of primes <= n."""
    return set(primes_upto(n))


# -- Rule 30 ------------------------------------------------------------------
#
# new[i] = left XOR (center OR right). The copies named rule30 were three
# different things; each is kept.

def rule30_step(n):
    """One Rule 30 step on the binary string of n (width = bit length, zero outside)."""
    bits = list(map(int, bin(n)[2:]))
    padded = [0] + bits + [0]
    out = [padded[i - 1] ^ (padded[i] | padded[i + 1]) for i in range(1, len(padded) - 1)]
    return int(''.join(map(str, out)), 2)


def rule30_ring(n, bits=8):
    """One Rule 30 step on n as a cyclic string of `bits` cells."""
    s = format(n % (1 << bits), f'0{bits}b')
    out = ''
    for i in range(bits):
        L, C, R = int(s[(i - 1) % bits]), int(s[i]), int(s[(i + 1) % bits])
        out += str(L ^ (C | R))
    return int(out, 2)


def rule30_cell(l, c, r):
    """New value of one cell from its neighbourhood, read off the rule number: (30 >> (4l+2c+r)) & 1."""
    return 30 >> 4 * l + 2 * c + r & 1


def rule30_cell_xor(l, c, r):
    """l XOR (c OR r); equals rule30_cell on 0/1 inputs."""
    return l ^ (c | r)
