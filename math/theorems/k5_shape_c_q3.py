"""
k5_shape_c_q3.py

Shape C of the k=5 ledger, reduced to its one live branch.

Shape C is {1, q, r, s, qr} with q < r < s. Song's mod-3 count lemma
(commit 02ae900) kills s=3, and r=3 needs r < q, so when 3 | n the only
survivor is q=3:

        prefix {1, 3, r, s, 3r},   3 < r < s,   n = 10(1+r^2) + s^2

STATUS: still OPEN. Everything below Level 1 is a reduction, not a
closure; the searches are Level 2 and exhaustive only to their stated
bounds. No proof of emptiness is claimed.

--------------------------------------------------------------------
LEVEL 1 REDUCTIONS
--------------------------------------------------------------------
(C1) 3 | n is AUTOMATIC. r, s > 3 give r^2 = s^2 = 1 (mod 3), so
     n = 1 + r^2 + s^2 = 0 (mod 3). The branch never has to assume it.

(C2) 9 does NOT divide n -- forced by the PREFIX, not by arithmetic.
     r >= 5 so max(prefix) = max(s, 3r) >= 15 > 9. If 9 | n then 9 is a
     divisor below the largest prefix element and would have to be in
     the prefix. It is not. So 9 | n refutes the shape.

(C3) s | r^2 + 1. From s | n and n = 10(1+r^2) + s^2 comes
     s | 10(1+r^2); s > r > 3 makes s >= 7, so s does not divide 10.
     This BOUNDS s by r^2+1, which is what makes the search finite.

(C4) r | s^2 + 10, since n = 10 + s^2 (mod r).

(C5) t is EVEN and t >= 2, where r^2+1 = s*t. r is odd so r^2+1 = 2
     (mod 8), i.e. r^2+1 = 2u with u odd; s is odd and divides r^2+1,
     so s | u and t = 2(u/s). In particular t = 1 never occurs, which
     is what rules out s = r^2+1 (even, hence not an odd prime).

(C6) THE IDENTITY. With r^2+1 = s*t,

         n = 10(r^2+1) + s^2 = 10st + s^2 = s(s + 10t).

     r | n and r does not divide s, so r | s + 10t. Writing
     s + 10t = r*m gives

         n = r * s * m,       m = (r^2 + 10t^2 + 1) / (r * t).

     Since 3 divides neither r nor s, (C2) becomes simply

         the shape requires 9 to NOT divide m.

     Equivalently m*r*t = r^2 + 10t^2 + 1: a Vieta-jumping form. For
     fixed m, r and r' = m*t - r are the two roots of
     X^2 - m*t*X + (10t^2+1), so r*r' = 10t^2 + 1. That descent is the
     likely route to a Level 1 closure and is NOT carried out here.

(C7) (C3) and (C4) collapse to r | 10t^2 + 1. From st = r^2+1 = 1
     (mod r) comes s = t^{-1} (mod r); substituting into s^2 = -10
     (mod r) gives 10t^2 = -1 (mod r). This is what makes the
     t-indexed search below possible.

--------------------------------------------------------------------
SEARCH RESULTS (Level 2)
--------------------------------------------------------------------
Two complementary sweeps, each COMPLETE in its own parameter:

  by r   for every prime r, (C3) bounds s to the prime divisors of
         r^2+1. Run to r <= 1000000.
  by t   for every even t, (C7) bounds r to the prime divisors of
         10t^2+1, and s = (r^2+1)/t. Run to t <= 300000.

The first reaches every small r at any t; the second reaches every
small t at any r. Both return THE SAME TWO PAIRS and nothing else:

    r=13      s=17      t=10      m=9    n = 1989        = 3^2 * 13 * 17
    r=53197   s=69073   t=40970   m=9    n = 33070287429 = 3^2 * 53197 * 69073

Both satisfy every congruence and both die on (C2): m = 9, so 9 | n,
so 9 is a divisor sitting below 3r that the prefix does not contain.
For r=13 that is 9 < 39, with the true five smallest divisors of 1989
being 1, 3, 9, 13, 17.

m = 9 is the ONLY value observed in either sweep. If m = 9 can be
forced, or 9 | m shown in general, the shape closes outright.
"""

from typing import List, Tuple, Dict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k5_odd_shapes import (is_prime, prime_divisors, primes_upto,
                           verify_prefix, first_k_divisors)

Pair = Tuple[int, int, int, int]        # (r, s, t, m)


def n_of(r: int, s: int) -> int:
    """The defining sum for prefix {1, 3, r, s, 3r}."""
    return 1 + 9 + r * r + s * s + 9 * r * r


def m_of(r: int, t: int) -> int:
    """m = (r^2 + 10t^2 + 1) / (r*t), from the (C6) identity."""
    num = r * r + 10 * t * t + 1
    assert num % (r * t) == 0, (r, t)
    return num // (r * t)


def search_by_r(rmax: int) -> List[Pair]:
    """COMPLETE for every prime r <= rmax. (C3) bounds s."""
    out = []
    for r in primes_upto(rmax):
        if r <= 3:
            continue
        for s in prime_divisors(r * r + 1):          # (C3)
            if s <= r:
                continue
            if (s * s + 10) % r:                     # (C4)
                continue
            t = (r * r + 1) // s
            out.append((r, s, t, m_of(r, t)))
    return out


def search_by_t(tmax: int) -> List[Pair]:
    """COMPLETE for every even t <= tmax. (C7) bounds r."""
    out = []
    for t in range(2, tmax + 1, 2):                  # (C5): t is even
        for r in prime_divisors(10 * t * t + 1):     # (C7)
            if r <= 3 or (r * r + 1) % t:
                continue
            s = (r * r + 1) // t
            if s <= r or not is_prime(s):
                continue
            out.append((r, s, t, m_of(r, t)))
    return out


def surviving_witnesses(pairs: List[Pair]) -> List[Tuple[int, int, int]]:
    """Pairs that also pass (C2) and the full prefix check."""
    out = []
    for r, s, t, m in pairs:
        n = n_of(r, s)
        if n % 9 == 0:                               # (C2)
            continue
        if verify_prefix((1, 3, r, s, 3 * r)):
            out.append((r, s, n))
    return out


# =====================================================================
# SELF-TESTS
# =====================================================================

def test_reductions() -> None:
    small = [p for p in primes_upto(400) if p > 3]
    # (C1)
    assert all(n_of(r, s) % 3 == 0 for r in small[:12] for s in small[:12])
    # (C5)
    for r in small[:40]:
        for s in prime_divisors(r * r + 1):
            if s > r:
                assert ((r * r + 1) // s) % 2 == 0, (r, s)
    # (C7) equivalence
    for r in small[:40]:
        for t in range(2, r + 2, 2):
            if (r * r + 1) % t:
                continue
            s = (r * r + 1) // t
            if s <= r:
                continue
            assert ((s * s + 10) % r == 0) == ((10 * t * t + 1) % r == 0), (r, t)
    print("[ok] reductions: 3|n automatic, t even, and (C3)+(C4) == (C7)")


def test_identity() -> None:
    """n = r*s*m must reproduce the defining sum exactly."""
    for r, s, t, m in search_by_r(20000):
        assert r * s * m == n_of(r, s), (r, s, t, m)
        assert (r * r + 1) == s * t
        assert (n_of(r, s) % 9 == 0) == (m % 9 == 0)   # 9|n iff 9|m
    print("[ok] identity: n = r*s*m, and 9|n iff 9|m")


def test_both_sweeps_agree() -> None:
    by_r = {(r, s) for r, s, _, _ in search_by_r(60000)}
    by_t = {(r, s) for r, s, _, _ in search_by_t(50000)}
    assert (13, 17) in by_r and (13, 17) in by_t
    # the two sweeps are complete in different parameters; each must
    # contain every pair the other finds within the overlap r <= 60000
    assert {p for p in by_t if p[0] <= 60000} <= by_r
    print(f"[ok] sweeps agree: by_r found {len(by_r)}, by_t found {len(by_t)}")


def test_known_pair_dies_on_nine() -> None:
    r, s = 13, 17
    n = n_of(r, s)
    assert n == 1989 and n % 9 == 0
    assert m_of(r, (r * r + 1) // s) == 9
    assert 9 < 3 * r                       # 9 sits below max(prefix)
    assert first_k_divisors(n, 5, 3 * r) == [1, 3, 9, 13, 17]
    assert verify_prefix((1, 3, r, s, 3 * r)) is None
    print("[ok] r=13,s=17: m=9 so 9|n, and 9 < 39 breaks the prefix")


def test_no_witnesses() -> None:
    pairs = search_by_r(60000) + search_by_t(50000)
    assert surviving_witnesses(pairs) == []
    assert {m for _, _, _, m in pairs} == {9}, "m other than 9 appeared"
    print("[ok] no witnesses in range; every surviving pair has m = 9")


def self_test() -> None:
    test_reductions()
    test_identity()
    test_both_sweeps_agree()
    test_known_pair_dies_on_nine()
    test_no_witnesses()
    print("\nAll self-tests passed.")
    print("NOTE: shape C q=3 remains OPEN. The sweeps are exhaustive only to")
    print("      their bounds. Forcing m = 9 in general would close it.")


if __name__ == "__main__":
    self_test()
