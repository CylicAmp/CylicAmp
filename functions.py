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
