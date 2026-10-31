"""
k5_shape_c_nodiv3.py

Shape C of the k=5 ledger, branch 3 does NOT divide n.

Shape C is {1, q, r, s, qr} with q < r < s. The 3 | n branch forces q = 3
and is closed in k5_shape_c_q3.py. Here 3 does not divide n, so no prime
of the prefix is 3 and q >= 5.

    prefix {1, q, r, s, qr},   5 <= q < r < s,   n = A + s^2
    A := (1+q^2)(1+r^2)

STATUS
  CASE 2 (s > qr):      CLOSED at Level 1, every q and r.
  CASE 1 (r < s < qr):  CLOSED at Level 1, every q and r.
So this branch is closed, and with k5_shape_c_q3.py shape C is closed.

--------------------------------------------------------------------
THE SHARED SETUP
--------------------------------------------------------------------
s | n and n = A + s^2 give s | A. Write A = s*t. Then

    n = st + s^2 = s(s+t).

q, r, s are pairwise coprime and all divide n, so qrs | n, and

    n = q*r*s*c    with    c = (s+t)/(qr),   i.e. qr | s+t.

THE PREFIX RULE, used throughout: if d | n and d < max(prefix), then d is
a divisor of n below the fifth-smallest divisor, so d must BE one of the
five smallest, i.e. d is in {1, q, r, s, qr}. It applies to composite d,
not only to primes -- that is the whole content of "divisor prefix", and
it is what closes case 1.

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
CASE 1:  r < s < qr,  so max(prefix) = qr.  CLOSED.
--------------------------------------------------------------------
Case 1 closes on the prefix rule applied to the composite divisor q^2.
It needs no discriminant and no range at all.

(1a) c <= q+1, on size. s < qr and s > r give t = A/s < A/r, so

         c = (s+t)/(qr) < (qr + A/r)/(qr) = 1 + (q + 1/q)(1 + 1/r^2),

     and for 5 <= q < r the correction 1/q + q/r^2 + 1/(q r^2) is below
     1/5 + 5/49 + 1/245 < 0.31. So c < q + 1.31, hence c <= q+1.

(1b) c is 1 or q. Every prime p | c divides n. If p < qr the prefix rule
     puts p in {q, r, s}; and c <= q+1 < r, so p is neither r nor s. A
     prime p >= qr would give c >= qr > q+1. So c is a power of q, and
     q^a <= q+1 < q^2 forces a <= 1.
     (c = q+1 is independently impossible: q+1 is even, so 2 | n, and
     2 < q would have to be in the prefix. The two routes agree.)

(1c) c = 1 is impossible. It needs s + t = qr, but A > q^2 r^2 gives
     t = A/s > A/(qr) > qr already.

(1d) So c = q, and therefore

         n = q*r*s*c = q^2 * r * s,      so   q^2 | n.

(1e) THE CONTRADICTION. r > q gives q^2 < qr = max(prefix). So q^2 is a
     divisor of n strictly below the largest prefix element, and the
     prefix rule forces q^2 into {1, q, r, s, qr}. But q^2 != 1 and
     q^2 != q (q >= 5); q^2 is composite while r and s are prime; and
     q^2 = qr would force q = r. Every option fails.

     CASE 1 IS EMPTY -- every q, every r. No window, no search.

--------------------------------------------------------------------
RULED-OUT ROUTE: the discriminant bracket (recorded, with a witness)
--------------------------------------------------------------------
Case 1 does also reduce to a discriminant, and the earlier version of
this file tried to close it that way. That route cannot work, and the
reason is worth keeping so it is not attempted again.

From c = q one gets s + t = q^2 r, so s^2 - q^2 r s + A = 0 with

    D1 = q^4 r^2 - 4(1+q^2)(1+r^2) = (q^2 r - 2r)^2 - (4 + 4q^2 + 8r^2),

s = (q^2 r - m)/2 and t = (q^2 r + m)/2 for m = sqrt(D1). Both range
conditions are automatic:

    s > r   <=>  D1 < (q^2 r - 2r)^2        identically true
    s < qr  <=>  A < q^2 r^2 (q-1)          true for q >= 5

so on that route case 1 becomes exactly "is D1 a perfect square". The
consecutive-square bracket closes it only where

    8 r^2 - (2q^2 - 4) r + (4q^2 + 5) < 0,

whose upper root is about q^2/4 -- and q=5 has no window at all, since
the deficit 4 + 4q^2 + 8r^2 outgrows one step 2(q^2 r - 2r) - 1 like
2r/q^2.

WHY THE ROUTE IS DEAD, not merely incomplete. "D1 is a perfect square"
is the Pell-type equation

    m^2 - a r^2 = -b,    a = q^4 - 4q^2 - 4,    b = 4q^2 + 4,

and a = (q^2-2)^2 - 8 is never a perfect square (X^2 - Y^2 = 8 forces
X=3, Y=1, i.e. q^2=5). So the equation is a genuine Pell equation and,
where solvable, has infinitely many solutions. Solving it by
Lagrange-Matthews-Mollin gives an explicit counterexample to the whole
approach: at q = 17 the prime

    r = CASE1_WITNESS_R  (110 digits, defined below)

is prime, coprime to 3, and makes D1 an exact perfect square, with
s = (q^2 r - m)/2 an integer satisfying r < s < qr. It passes every
condition the discriminant argument tracks. It dies only on (1e), on
q^2 | n. So no bracket, no sieve and no search on D1 could ever have
closed case 1 -- the squares are really there.

A SECONDARY FACT, true and cheap, kept because it is independent of all
of the above: in this branch 3 divides D1 always, and

    r^2 = 1 mod 9  ->  D1 = 3 mod 9     never a square
    r^2 = 4 mod 9  ->  D1 = 0 mod 9     open
    r^2 = 7 mod 9  ->  D1 = 6 mod 9     never a square

independently of q. So a square D1 forces r = +-2 (mod 9). The witness
above satisfies it. The 3-adic density of solutions decays (1/3, 2/9,
4/27, 11/81, 31/243, ...) but is nonzero at every level, so by
compactness Z_3 solutions exist and no power of 3 closes the case
either. This is further confirmation that (1e), not the discriminant,
is the real obstruction.
"""

from math import isqrt, sqrt
from typing import Optional, Tuple

# The q=17 witness: prime, coprime to 3, D1 an exact square, r < s < qr.
# It exists to prove the discriminant route cannot close case 1.
CASE1_WITNESS_Q = 17
CASE1_WITNESS_R = 14813867252907869619135619827383423192199756439309170279811117063533804572327116347480246551610245030837262053


def A_of(q: int, r: int) -> int:
    """A = (1+q^2)(1+r^2), so n = A + s^2."""
    return (1 + q * q) * (1 + r * r)


def disc_case2(q: int, r: int) -> int:
    """(2e) discriminant of s^2 - q r^2 s + A."""
    return q * q * r ** 4 - 4 * A_of(q, r)


def disc_case1(q: int, r: int) -> int:
    """discriminant of s^2 - q^2 r s + A (ruled-out route, kept for the record)."""
    return q ** 4 * r * r - 4 * A_of(q, r)


def case1_cofactor_bound(q: int, r: int) -> float:
    """(1a) the size bound forcing c <= q+1."""
    return (q * r + A_of(q, r) / r) / (q * r)


def case1_is_empty(q: int, r: int) -> bool:
    """(1d)-(1e) c=q makes n = q^2 r s, and q^2 < qr is a divisor not in the
    prefix. True means case 1 is impossible for this (q, r)."""
    return q * q < q * r and q * q not in (1, q, q * r)


def case1_window(q: int) -> Optional[Tuple[float, float]]:
    """the r-interval where the (abandoned) bracket would have closed case 1."""
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


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def smallest_divisors(n: int, k: int = 5):
    out = []
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            out.append(i)
            if len(out) > k + 2:
                break
    return sorted(out)[:k]


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
    for q in range(5, 500):
        assert 2 * q ** 3 - 4 * q * q - 12 * q - 21 > 0, q
    print("[ok] case 2: D bracketed by consecutive squares, never a square")


def test_case1_cofactor_bound() -> None:
    """(1a) c < q+2 over every prime pair, so c <= q+1."""
    ps = [p for p in primes_upto(600) if p >= 5 and p % 3]
    worst = 0.0
    for i, q in enumerate(ps[:60]):
        for r in ps[i + 1:][:400]:
            bnd = case1_cofactor_bound(q, r)
            assert bnd < q + 2, (q, r, bnd)
            worst = max(worst, bnd - q)
    assert worst < 1.5, worst
    print(f"[ok] case 1 (1a): c <= q+1 on every pair (sup of bound-q = {worst:.4f})")


def test_case1_cofactor_is_one_or_q() -> None:
    """(1c) c=1 is impossible because A > q^2 r^2 forces t > qr."""
    ps = [p for p in primes_upto(600) if p >= 5 and p % 3]
    for i, q in enumerate(ps[:60]):
        for r in ps[i + 1:][:400]:
            assert A_of(q, r) > q * q * r * r, (q, r)
    print("[ok] case 1 (1c): A > q^2 r^2, so t > qr and c = 1 is impossible")


def test_case1_is_empty() -> None:
    """(1e) THE CLOSURE: c=q gives n=q^2 r s, and q^2 < qr is a divisor
    of n that cannot sit in the prefix {1,q,r,s,qr}."""
    ps = [p for p in primes_upto(2000) if p >= 5 and p % 3]
    checked = 0
    for i, q in enumerate(ps):
        for r in ps[i + 1:]:
            assert q * q < q * r, (q, r)
            assert q * q != 1 and q * q != q
            assert not _is_prime(q * q)
            assert q * q != q * r
            assert case1_is_empty(q, r), (q, r)
            checked += 1
            if checked > 200000:
                break
        if checked > 200000:
            break
    print(f"[ok] case 1 (1e) CLOSED: q^2 | n, q^2 < qr, q^2 not in prefix "
          f"({checked} pairs)")


def test_case1_witness_kills_discriminant_route() -> None:
    """The q=17 witness passes every discriminant-side condition and dies
    only on (1e). This is why the bracket route is recorded as dead."""
    q, r = CASE1_WITNESS_Q, CASE1_WITNESS_R
    assert _is_prime(q) and _is_prime(r), "witness primes"
    assert r > q and r % 3 and q % 3, "witness is in the 3-does-not-divide branch"
    D1 = disc_case1(q, r)
    m = isqrt(D1)
    assert m * m == D1, "witness makes D1 an exact perfect square"
    assert (q * q * r - m) % 2 == 0, "s is an integer"
    s = (q * q * r - m) // 2
    assert r < s < q * r, "witness satisfies BOTH case-1 range conditions"
    assert r % 9 in (2, 7), "witness obeys the mod-9 condition"
    n = A_of(q, r) + s * s
    assert n % (q * q) == 0, "but q^2 | n ..."
    assert q * q < q * r, "... and q^2 < qr, so (1e) kills it"
    assert case1_is_empty(q, r), "and (1e) applies to the witness too"
    print(f"[ok] witness q=17, r={len(str(r))} digits: D1 IS a perfect square, "
          f"ranges hold, dies only on q^2 | n")


def test_mod9_condition() -> None:
    """A square D1 forces r = +-2 mod 9, independently of q."""
    squares9 = {(x * x) % 9 for x in range(9)}
    for X in (1, 4, 7):
        a9 = (X * X - 4 * X - 4) % 9
        b9 = (4 * X + 4) % 9
        assert (a9 * 1 - b9) % 9 == 3 and 3 not in squares9
        assert (a9 * 4 - b9) % 9 == 0
        assert (a9 * 7 - b9) % 9 == 6 and 6 not in squares9
    for q in range(5, 150):
        if q % 3 == 0:
            continue
        for r in range(5, 2000):
            if r % 3 == 0:
                continue
            D1 = disc_case1(q, r)
            if D1 >= 0 and isqrt(D1) ** 2 == D1:
                assert r % 9 in (2, 7), (q, r)
    print("[ok] mod 9: a square D1 forces r = +-2 (mod 9), for every q")


def test_brute_force_no_case1_n() -> None:
    """Independent check: no n at all has prefix [1,q,r,s,qr] with
    n = q^2 r s and r < s < qr."""
    ps = [p for p in primes_upto(3000) if p >= 5 and p % 3]
    LIM = 4_000_000
    found = []
    for i, q in enumerate(ps):
        if q * q * q > LIM:
            break
        for r in ps[i + 1:]:
            if q * q * r > LIM:
                break
            for s in ps:
                if s <= r:
                    continue
                if s >= q * r:
                    break
                n = q * q * r * s
                if n > LIM:
                    break
                if smallest_divisors(n) == [1, q, r, s, q * r]:
                    found.append((q, r, s, n))
    assert found == [], found
    print(f"[ok] brute force to {LIM:,}: no case-1 n exists")


def self_test() -> None:
    test_shared_identity()
    test_case2_bracket()
    test_case1_cofactor_bound()
    test_case1_cofactor_is_one_or_q()
    test_case1_is_empty()
    test_case1_witness_kills_discriminant_route()
    test_mod9_condition()
    test_brute_force_no_case1_n()
    print("\nAll self-tests passed.")
    print("CASE 2 (s > qr):     CLOSED at Level 1.")
    print("CASE 1 (r < s < qr): CLOSED at Level 1, via q^2 | n and q^2 < qr.")
    print("Branch 3-does-not-divide-n is CLOSED, so shape C is CLOSED.")


if __name__ == "__main__":
    self_test()
