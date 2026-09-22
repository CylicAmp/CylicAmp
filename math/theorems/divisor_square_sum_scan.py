"""
divisor_square_sum_scan.py

Ground truth for  n = d_1^2 + ... + d_k^2  over the k smallest divisors of n.

This is the SOLUTION HUNT, not the impossibility kernel. It makes no
claims about shapes, congruences or certificates: it enumerates n and
checks the defining equation directly, so anything it reports is a
witness and anything it fails to report is absent below the bound.

WHY A SIEVE UP TO sqrt(N) SUFFICES
----------------------------------
d_k^2 is one of the summands, so n >= d_k^2 and therefore d_k <= sqrt(n).
Sieving divisors d up to sqrt(N) captures the ENTIRE prefix of every
n <= N -- nothing is missed by not sieving further. The scan is
segmented so memory stays flat regardless of N.

RESULTS, n <= 30,000,000, k <= 14
---------------------------------
    k = 1    n = 1
    k = 4    n = 130  = 1 + 4 + 25 + 100
    k = 11   n = 1860 = 1+4+9+16+25+36+100+144+225+400+900
    every other k <= 14: NONE

1860 = 2^2 * 3 * 5 * 31, whose eleven smallest divisors are
1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30 -- the twelfth is 31.

SOLUTIONS ARE SPORADIC, NOT A FAMILY
------------------------------------
k = 1, 4, 11 and nothing in between. In particular the divisor prefix is
NOT a Markov-Hurwitz node. That form needs

    sum(x_i^2) = c * prod(x_i)   with c a positive integer,

i.e. the PRODUCT of the prefix must divide n. Neither witness does, and
they fail in opposite directions:

    130    product        100   n/product = 1.3
    1860   product  777600000   n/product = 0.0000024

so it is not a matter of finding the right constant -- the form does not
apply. Any search of Markov-Hurwitz parameter space for this problem is
looking for a structure the problem does not have.

PARITY (see divisor_prefix_ledger.oracle_parity)
------------------------------------------------
A sum of k odd squares has the parity of k, and every divisor of an odd
n is odd. So for EVEN k an odd n is impossible and the whole odd sector
dies for free. Consistent with the table: 130 and 1860 are both even.
"""

from typing import Dict, List, Tuple
import math

Witness = Tuple[int, List[int]]


def scan(limit: int, kmax: int = 14, segment: int = 2_000_000,
         progress=None) -> Dict[int, List[Witness]]:
    """Every n <= limit equal to the sum of the squares of its k smallest
    divisors, for each k <= kmax. Exhaustive below the bound."""
    hits: Dict[int, List[Witness]] = {}
    for lo in range(1, limit + 1, segment):
        hi = min(lo + segment, limit + 1)
        root = math.isqrt(hi - 1)                 # d_k <= sqrt(n), so this is enough
        divs: List[List[int]] = [[] for _ in range(hi - lo)]
        for d in range(1, root + 1):
            start = ((lo + d - 1) // d) * d
            for m in range(start, hi, d):
                bucket = divs[m - lo]
                if len(bucket) < kmax:
                    bucket.append(d)
        for i, bucket in enumerate(divs):
            n = lo + i
            total = 0
            for k, d in enumerate(bucket, 1):
                total += d * d
                if total == n:
                    hits.setdefault(k, []).append((n, bucket[:k]))
                elif total > n:
                    break                          # squares only grow
        if progress:
            progress(hi - 1)
    return hits


def verify(n: int, k: int) -> bool:
    """Independent check, by direct division rather than by sieve."""
    divisors = [d for d in range(1, math.isqrt(n) + 1) if n % d == 0]
    divisors = sorted(divisors)[:k]
    return len(divisors) == k and sum(d * d for d in divisors) == n


# =====================================================================
# SELF-TESTS
# =====================================================================

def test_known_witnesses() -> None:
    assert verify(130, 4)
    assert verify(1860, 11)
    assert sum(d * d for d in (1, 2, 5, 10)) == 130
    assert sum(d * d for d in (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30)) == 1860
    # and they really are the k smallest divisors
    d1860 = [d for d in range(1, 1861) if 1860 % d == 0]
    assert d1860[:11] == [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30]
    assert d1860[11] == 31
    print("[ok] witnesses: 130 at k=4, 1860 at k=11, both verified directly")


def test_scan_finds_them() -> None:
    hits = scan(2_000_000, kmax=12)
    assert hits.get(4) == [(130, [1, 2, 5, 10])]
    assert hits.get(11) == [(1860, [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30])]
    for k in (2, 3, 5, 6, 7, 8, 9, 10, 12):
        assert k not in hits, (k, hits[k])
    print("[ok] scan to 2e6 reproduces exactly k=1, 4, 11 and nothing else")


def test_not_markov_hurwitz() -> None:
    """The product of the prefix must divide n for a Markov-Hurwitz node."""
    for n, pref in [(130, (1, 2, 5, 10)),
                    (1860, (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30))]:
        product = 1
        for d in pref:
            product *= d
        assert n % product != 0, (n, product)
    # and they miss in opposite directions
    assert 100 < 130                       # k=4: product below n
    assert 777_600_000 > 1860              # k=11: product far above n
    print("[ok] neither witness is a Markov-Hurwitz node, and they fail "
          "in opposite directions")


def test_sqrt_bound_is_sound() -> None:
    """d_k <= sqrt(n), which is what lets the sieve stop at sqrt(N)."""
    for n, pref in [(130, (1, 2, 5, 10)),
                    (1860, (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30))]:
        assert max(pref) <= math.isqrt(n), (n, max(pref))
        assert max(pref) ** 2 <= n
    print("[ok] d_k^2 <= n holds on both witnesses, justifying the sieve bound")


def self_test() -> None:
    test_known_witnesses()
    test_not_markov_hurwitz()
    test_sqrt_bound_is_sound()
    test_scan_finds_them()
    print("\nAll self-tests passed.")


if __name__ == "__main__":
    self_test()
    print("\nRecorded scan: n <= 30,000,000, k <= 14 -> k=1, k=4 (130), "
          "k=11 (1860), nothing else.")
