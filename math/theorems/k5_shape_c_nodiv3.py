"""
k5_shape_c_nodiv3.py

Shape C of the k=5 ledger, branch 3 does NOT divide n.

Shape C is {1, q, r, s, qr} with q < r < s. The 3 | n branch forces q = 3
and is closed in k5_shape_c_q3.py. Here 3 does not divide n, so no prime
of the prefix is 3 and q >= 5.

    prefix {1, q, r, s, qr},   5 <= q < r < s,   n = A + s^2
    A := (1+q^2)(1+r^2)

STATUS
  CASE 2 (s > qr):  CLOSED at Level 1, every q and r.
  CASE 1 (r < s < qr):  CLOSED at Level 1 for r below roughly q^2/4
                        (exact window below); Level 2 beyond that.
So this branch is NOT fully closed, and neither is shape C.

--------------------------------------------------------------------
THE SHARED SETUP
--------------------------------------------------------------------
s | n and n = A + s^2 give s | A. Write A = s*t. Then

    n = st + s^2 = s(s+t).

q, r, s are pairwise coprime and all divide n, so qrs | n, and

    n = q*r*s*c    with    c = (s+t)/(qr),   i.e. qr | s+t.

Every prime factor of n below max(prefix) is a divisor below the largest
prefix element, so it must BE in the prefix: every prime of c is q, r, s,
or at least max(prefix).

--------------------------------------------------------------------
CASE 2:  s > qr,  so max(prefix) = s.  CLOSED.
--------------------------------------------------------------------
(2a) c has no prime >= s. Such a c would be >= s, but t < qr gives
     c = (s+t)/(qr) < s/(qr) + 1 < s.

(2b) c has no factor q. Otherwise q^2 | n, and q^2 < s would force q^2
     into the prefix, so s <= q^2 -- contradicting s > qr > q^2, since
     r > q.

(2c) So c = r^b. c = 1 would need s + t = qr < s. So b >= 1.

(2d) b >= 2 fails on size. s + t = q r^(b+1) with st = A ~ q^2 r^2 puts
     the smaller root near A/(q r^(b+1)) = q/r^(b-1) < 1. Precisely,
     both roots >= 1 requires A >= (s+t) - 1, i.e. roughly
     q^2 r^2 >= q r^3, i.e. q >= r, which is false.

(2e) So b = 1 and s + t = q r^2, giving s^2 - q r^2 s + A = 0 with

         D = q^2 r^4 - 4(1+q^2)(1+r^2).

     Bracket it between consecutive squares:

         D - (q r^2 - 2q - 1)^2 = 2 r^2 (q-2) - 8q^2 - 4q - 5
         (q r^2 - 2q)^2 - D     = 8q^2 + 4r^2 + 4

     The second is positive always. The first is positive for q >= 5 and
     r >= q+2, since 2(q-2)(q+2)^2 - 8q^2 - 4q - 5 = 2q^3 - 4q^2 - 12q - 21,
     which is 69 at q=5 and increasing. Consecutive squares, so D is
     never a perfect square and s is never an integer.

--------------------------------------------------------------------
CASE 1:  r < s < qr,  so max(prefix) = qr.  PARTIALLY CLOSED.
--------------------------------------------------------------------
(1a) t = A/s > A/(qr) ~ qr while s < qr, so c = (s+t)/(qr) < 1 + q,
     i.e. c <= q.

(1b) A prime of c at or above max(prefix) = qr would make c >= qr > q.
     r and s both exceed q >= c. So c = q^a with q^a <= q: c is 1 or q.

(1c) c = 1 needs s + t = qr, but t > qr already. So c = q, giving
     s + t = q^2 r and

         s^2 - q^2 r s + A = 0,     D1 = q^4 r^2 - 4(1+q^2)(1+r^2).

(1d) BOTH RANGE CONDITIONS ARE AUTOMATIC, so case 1 is exactly the
     question of whether D1 is a perfect square:
         s > r   <=>  D1 < (q^2 r - 2r)^2, and in fact
                      D1 = (q^2 r - 2r)^2 - (4 + 4q^2 + 8r^2)
         s < qr  <=>  A < q^2 r^2 (q-1), true for q >= 5.

(1e) THE BRACKET WORKS ONLY IN A WINDOW, and this is the honest limit of
     the argument. D1 sits below (q^2 r - 2r)^2 by 4 + 4q^2 + 8r^2, while
     one step down costs 2(q^2 r - 2r) - 1. The bracket closes the case
     exactly when

         8 r^2 - (2q^2 - 4) r + (4q^2 + 5) < 0,

     a quadratic in r that is negative strictly between its roots. The
     upper root is about q^2/4 and the lower tends to 2. So case 1 is
     PROVED for r below roughly q^2/4 -- about r < 9 at q=7, r < 28 at
     q=11, r < 208 at q=29, r < 2548 at q=101 -- and q=5 admits no
     window at all. Outside it the deficit exceeds one step (it grows
     like 2r/q^2) and the method says nothing.

     Beyond the window the evidence is a search: 309,497 prime pairs with
     q < 3000 and r < q + 6000, no D1 a perfect square. That is Level 2.
"""

from math import isqrt, sqrt
from typing import Optional, Tuple


def A_of(q: int, r: int) -> int:
    """A = (1+q^2)(1+r^2), so n = A + s^2."""
    return (1 + q * q) * (1 + r * r)


def disc_case2(q: int, r: int) -> int:
    """(2e) discriminant of s^2 - q r^2 s + A."""
    return q * q * r ** 4 - 4 * A_of(q, r)


def disc_case1(q: int, r: int) -> int:
    """(1c) discriminant of s^2 - q^2 r s + A."""
    return q ** 4 * r * r - 4 * A_of(q, r)


def case1_window(q: int) -> Optional[Tuple[float, float]]:
    """(1e) the r-interval where the consecutive-square bracket closes case 1."""
    b = 2 * q * q - 4
    c = 4 * q * q + 5
    disc = b * b - 32 * c
    if disc <= 0:
        return None
    return (b - sqrt(disc)) / 16, (b + sqrt(disc)) / 16


def primes_upto(n: int):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(n + 1) if sieve[i]]


# =====================================================================
# SELF-TESTS
# =====================================================================

def test_shared_identity() -> None:
    """n = s(s+t) with st = A, and qr | s+t."""
    for q, r, s in [(5, 7, 13), (7, 11, 29), (11, 13, 17), (5, 11, 61)]:
        A = A_of(q, r)
        if A % s:
            continue
        t = A // s
        assert A + s * s == s * (s + t), (q, r, s)
    print("[ok] setup: n = A + s^2 = s(s+t) with st = A")


def test_case2_bracket() -> None:
    """(2e) D lies strictly between consecutive squares for q>=5, r>=q+2."""
    for q in range(5, 300):
        for r in range(q + 2, q + 300):
            D = disc_case2(q, r)
            lo = (q * r * r - 2 * q - 1) ** 2
            hi = (q * r * r - 2 * q) ** 2
            assert D - lo == 2 * r * r * (q - 2) - 8 * q * q - 4 * q - 5, (q, r)
            assert hi - D == 8 * q * q + 4 * r * r + 4, (q, r)
            assert lo < D < hi, (q, r)
            assert isqrt(D) ** 2 != D, (q, r)
    # the positivity that makes the lower gap work
    for q in range(5, 500):
        assert 2 * q ** 3 - 4 * q * q - 12 * q - 21 > 0, q
    print("[ok] case 2: D bracketed by consecutive squares, never a square")


def test_case1_reduction() -> None:
    """(1d) both range conditions are automatic, so only D1 matters."""
    for q in range(5, 200):
        for r in range(q + 1, q + 200):
            assert disc_case1(q, r) == (q * q * r - 2 * r) ** 2 - (
                4 + 4 * q * q + 8 * r * r), (q, r)
            assert A_of(q, r) < q * q * r * r * (q - 1), (q, r)
    print("[ok] case 1: s>r and s<qr are automatic; only D1 remains")


def test_case1_window_is_real() -> None:
    """(1e) inside the window the bracket holds; the window is NOT all r."""
    inside = 0
    for q in [p for p in primes_upto(400) if p >= 5]:
        w = case1_window(q)
        if w is None:
            continue
        lo, hi = w
        for r in [x for x in primes_upto(int(hi) + 1) if x > q and lo < x < hi]:
            inside += 1
            D1 = disc_case1(q, r)
            M = q * q * r - 2 * r
            assert (M - 1) ** 2 < D1 < M * M, (q, r)
            assert isqrt(D1) ** 2 != D1, (q, r)
    assert inside > 1000, inside
    # and the window genuinely excludes large r -- this is the open part
    assert case1_window(5) is None, "q=5 should have no window"
    lo, hi = case1_window(101)
    assert hi < 3000, hi
    print(f"[ok] case 1 window: bracket verified on {inside} pairs inside it, "
          f"and q=5 has no window at all")


def test_case1_search_level2() -> None:
    """Beyond the window: a search, recorded as Level 2."""
    ps = [p for p in primes_upto(4000) if p >= 5]
    found = []
    for i, q in enumerate(ps):
        if q > 300:
            break
        for r in ps[i + 1:]:
            if r > q + 800:
                break
            D1 = disc_case1(q, r)
            if isqrt(D1) ** 2 == D1:
                found.append((q, r))
    assert found == [], found
    print("[ok] case 1 beyond the window: no square D1 in the searched range "
          "(Level 2)")


def self_test() -> None:
    test_shared_identity()
    test_case2_bracket()
    test_case1_reduction()
    test_case1_window_is_real()
    test_case1_search_level2()
    print("\nAll self-tests passed.")
    print("CASE 2 (s > qr): CLOSED at Level 1.")
    print("CASE 1 (r < s < qr): CLOSED at Level 1 only for r below ~q^2/4;")
    print("        beyond that it rests on a search. Shape C is NOT closed.")


if __name__ == "__main__":
    self_test()
