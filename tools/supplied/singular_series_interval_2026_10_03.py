# Supplied code, 2026-10-03, verbatim (from a pasted correction of an earlier draft).
# Audited in math/primes/singular_series_supplied_audit_2026_10_03.py.
from decimal import Decimal, getcontext, localcontext
from fractions import Fraction
import math


# Extra guard digits are used internally.  The returned interval is
# subsequently rounded to the requested number of decimal places.
getcontext().prec = 80


def fast_prime_sieve(limit: int):
    """Return the exact list of primes <= limit."""
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * (
                (limit - start) // p + 1
            )

    return [n for n, is_prime in enumerate(sieve) if is_prime]


def primorial(k: int) -> int:
    """Return k# = product of primes p <= k."""
    result = 1

    for p in fast_prime_sieve(k):
        result *= p

    return result


def exact_head(k: int):
    """
    Exact finite prefactor

        1/(2(k-1)) *
        product_{p <= k} [ 1/p * (p/(p-1))^(k-1) ]

    for the primorial-step arithmetic progression.
    """
    if k < 3:
        raise ValueError("This implementation is intended for k >= 3.")

    m = k - 1
    head = Fraction(1, 2 * m)

    for p in fast_prime_sieve(k):
        local_factor = (
            Fraction(1, p)
            * Fraction(p, p - 1) ** m
        )
        head *= local_factor

    return head


def finite_euler_product(k: int, B: int, precision: int = 80):
    """
    Compute

        product_{k < p <= B}
        (1 - (k-1)/p) * (p/(p-1))^(k-1)

    using Decimal arithmetic.

    No binary floating-point values are introduced.
    """
    if B <= k:
        raise ValueError("B must be larger than k.")

    m = k - 1
    product = Decimal(1)

    with localcontext() as ctx:
        ctx.prec = precision

        dm = Decimal(m)
        one = Decimal(1)

        for p in fast_prime_sieve(B):
            if p <= k:
                continue

            dp = Decimal(p)

            factor = (
                one - dm / dp
            ) * (
                dp / (dp - one)
            ) ** m

            product *= factor

    return +product


def rigorous_tail_interval(k: int, B: int, precision: int = 80):
    """
    Return a rigorous enclosure [lower, upper] for

        product_{p > B} f_k(p)

    where

        f_k(p) =
            (1 - (k-1)/p) * (p/(p-1))^(k-1).

    For k >= 3 and B >= k, every tail factor lies in (0, 1).

    The bound uses

        -log f_k(p)
        <= A/p^2 + C/p^3

    together with

        sum_{p>B} 1/p^2 < 1/B
        sum_{p>B} 1/p^3 < 1/(2B^2).

    No prime-number-theorem approximation is used.
    """
    if k < 3:
        raise ValueError("k must be >= 3.")

    if B < k:
        raise ValueError("B must be >= k.")

    m = k - 1

    with localcontext() as ctx:
        ctx.prec = precision

        dm = Decimal(m)
        dB = Decimal(B)
        one = Decimal(1)

        # Exact leading coefficient:
        #
        # (m^2 - m)/2 = m(m-1)/2
        A = dm * (dm - one) / Decimal(2)

        # Bound on the r >= 3 part.
        #
        # sum_{r>=3} m^r/(r p^r)
        # <= m^3/(3 p^3 (1-m/p))
        #
        # and p >= B+1.
        denominator = (
            Decimal(1)
            - dm / Decimal(B + 1)
        )

        C = dm ** 3 / (
            Decimal(3) * denominator
        )

        # Sum_{n>B} 1/n^2 < 1/B
        # Sum_{n>B} 1/n^3 < 1/(2B^2)
        error_exponent = (
            A / dB
            + C / (Decimal(2) * dB ** 2)
        )

        lower = (-error_exponent).exp()
        upper = one

    return lower, upper


def compute_singular_series_interval(
    k: int,
    B: int = 2_000_000,
    precision: int = 80
):
    """
    Compute a certified interval containing the primorial-step
    singular series

        S_k =
            1/(2(k-1))
            * P1(k)
            * P2(k,B)
            * Tail(k,B).

    P1 is exact rational arithmetic.
    P2 is evaluated with Decimal guard precision.
    Tail is enclosed rigorously rather than replaced by an
    asymptotic estimate.
    """
    if k < 3:
        raise ValueError("k must be >= 3.")

    if B <= k:
        raise ValueError("B must be greater than k.")

    head = exact_head(k)
    p2 = finite_euler_product(k, B, precision)
    tail_lo, tail_hi = rigorous_tail_interval(
        k, B, precision
    )

    with localcontext() as ctx:
        ctx.prec = precision

        head_dec = (
            Decimal(head.numerator)
            / Decimal(head.denominator)
        )

        finite_value = head_dec * p2

        lower = finite_value * tail_lo
        upper = finite_value * tail_hi

    return head, lower, upper


def format_interval(lower, upper, places=15):
    """
    Display the certified interval without pretending that
    every displayed digit is independently certified.
    """
    quantum = Decimal(1).scaleb(-places)

    lo = lower.quantize(quantum)
    hi = upper.quantize(quantum)

    return f"[{lo}, {hi}]"


if __name__ == "__main__":
    B = 2_000_000
    PRECISION = 80

    print(
        f"{'k':<3} | "
        f"{'Exact head':<30} | "
        f"{'Certified interval':<50}"
    )
    print("-" * 90)

    for k in range(3, 11):
        head, lower, upper = compute_singular_series_interval(
            k,
            B=B,
            precision=PRECISION
        )

        print(
            f"{k:<3} | "
            f"{str(head):<30} | "
            f"{format_interval(lower, upper, 15)}"
        )
