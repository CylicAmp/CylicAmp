"""
k5_odd_shapes.py

The three k = 5 shapes left OPEN by divisor_prefix_ledger.

    A   {1, q, q^2, q^3, r}
    B   {1, q, q^2, r, qr}
    C   {1, q, r, s, qr}      q < r < s

All three are odd-sector, and the parity lemma is silent at k = 5 (a sum
of five odd squares is 5 mod 8, odd, so it can equal an odd n). Each is
reduced here to a divisibility condition that BOUNDS the larger prime in
terms of the smaller, which turns "search all n" into a search that is
COMPLETE for each value of the parameter.

STATUS:
  A  CLOSED at Level 1 -- see THE ORDERING ARGUMENT FOR SHAPE A below.
  B  CLOSED at Level 1 -- see THE ORDERING ARGUMENT FOR SHAPE B below.
  C  its 3|n branch (q=3) is closed in k5_shape_c_q3.py; the 3-does-not-
     divide-n branch is open.

--------------------------------------------------------------------
LEVEL 1 REDUCTIONS (proved; they make the search finite per parameter)
--------------------------------------------------------------------
Throughout n = sum of the squares of the five prefix elements.

Shape A  {1, q, q^2, q^3, r}
  (A1) Admissibility forces r > q^2. If r < q^2 then qr < q^3 = max(V),
       and qr | n (q, r coprime divisors), so qr would be a divisor
       below the top that is absent from the prefix.
  (A2) r | n = (1+q^2)(1+q^4). Combined with (A1), r | 1+q^2 would force
       r = q^2+1, which is EVEN. So r | q^4 + 1.
  (A3) q^3 | n and n = 1 + q^2 + r^2 mod q^3, so q^3 | 1 + q^2 + r^2,
       which gives q^2 | 1 + r^2 and hence q = 1 mod 4 (-1 must be a
       quadratic residue mod q).

Shape B  {1, q, q^2, r, qr}
  (B1) q^2 | n and n = 1 + r^2 mod q^2, so q^2 | 1 + r^2, q = 1 mod 4.
  (B2) r | n = 1 + q^2 + q^4 = (q^2+q+1)(q^2-q+1), so r <= q^2+q+1.
       Since (q^6-1)/(q^2-1) = 1+q^2+q^4, r has multiplicative order 3
       or 6 mod q, so r = 1 mod 3. In particular r != 3.

Shape C  {1, q, r, s, qr}
  (C1) The product in the prefix must be of the two SMALLEST primes.
       With primes a < b < c, a product ac or bc leaves ab strictly
       below the top and absent, which admissibility forbids.
  (C2) s | n = (1+q^2)(1+r^2), so s <= (1+q^2)(1+r^2): finite per (q,r).
  (C3) q | 1 + r^2 + s^2 and r | 1 + q^2 + s^2.

--------------------------------------------------------------------
SEARCH RESULTS (Level 2, recorded with their bounds)
--------------------------------------------------------------------
Bounds reached when this module was written:

  A   complete for every odd prime q <= 50000.
      3894 candidate r; ZERO reach even (A3)'s q^2 | 1+r^2.
  B   complete for every odd prime q <= 50000.
      29642 candidate r; exactly one pair survives the algebra,
      (q, r) = (5, 7), giving n = 1925 = 5^2 * 7 * 11, rejected because
      11 | n lies below max(V) = 35, so the prefix is wrong.
  C   complete for every prime pair q < r <= 5000.
      298436 candidate s; exactly one survives the algebra,
      (q, r, s) = (3, 13, 17), giving n = 1989 = 3^2 * 13 * 17, rejected
      because 9 | n lies below 17.

The two survivors are instructive: both satisfy every congruence and
die only on the PREFIX condition, i.e. on an unlisted small divisor.
That is the constraint no congruence oracle sees, and it is why these
shapes resist a purely modular argument.

--------------------------------------------------------------------
THE ORDERING ARGUMENT FOR SHAPE A -- Level 1, closes it
--------------------------------------------------------------------
Shape A is {1, q, q^2, q^3, r} with n = 1 + q^2 + q^4 + q^6 + r^2. Put
A = 1 + q^2 + q^4 + q^6, so n = A + r^2.

q^3 and r are coprime and both divide n, so q^3 r | n. Write

    n = q^3 * r * c.

(A-O1) EVERY PRIME FACTOR OF c IS q OR AT LEAST max(prefix). A prime
       p | n below max(prefix) is a divisor below the largest prefix
       element, so it must BE in the prefix, hence p is q or r. Taking
       out one factor of r leaves q and primes >= max(prefix).

(A-O2) c < q+2 IN BOTH CASES. Split c = A/(q^3 r) + r/q^3 and bound
       each term. (An earlier draft claimed n < 2q^6 in case A1; that is
       FALSE -- at q=3, r=26 it reads 1496 < 1458. A test caught it. The
       correct route bounds the two terms separately and happens to give
       the same constant in both cases.)
       case A1, q^2 < r < q^3, max = q^3:
         r/q^3 < 1, and A/(q^3 r) < A/q^5 = q + 1/q + 1/q^3 + 1/q^5,
         so c < q + 1 + 1/q + 1/q^3 + 1/q^5 < q + 2 for q >= 3.
       case A2, q^3 < r <= q^4+1, max = r:
         the proved r | q^4+1 gives r/q^3 <= q + 1/q^3, and r > q^3
         gives A/(q^3 r) < A/q^6 = 1 + 1/q^2 + 1/q^4 + 1/q^6,
         so c < q + 1 + 1/q^2 + 1/q^3 + 1/q^4 + 1/q^6 < q + 2.

(A-O3) c IS 1 OR q. By (A-O2) c < q+2 <= q^3, which is below both q^3
       and r, so by (A-O1) c has no prime factor other than q. And
       q^2 >= q+2 for q >= 2, so no higher power fits.

(A-O4) c = 1 IS IMPOSSIBLE. n = q^3 r reads r^2 - q^3 r + A = 0, with

           disc = q^6 - 4A = -3q^6 - 4q^4 - 4q^2 - 4 < 0

       for every q, so no real r exists. (This is exactly the
       polynomial the V5 kernel carried in PolynomialNegativityOracle
       -- the oracle that could never fire, because its pattern was a
       tuple of 3-tuples being compared against 5-tuples.)

(A-O5) c = q IS IMPOSSIBLE. n = q^4 r reads r^2 - q^4 r + A = 0, with
       disc = q^8 - 4q^6 - 4q^4 - 4q^2 - 4. Bracket it:

           (q^4-2q^2-5)^2 = q^8 - 4q^6 - 6q^4 + 20q^2 + 25
           (q^4-2q^2-4)^2 = q^8 - 4q^6 - 4q^4 + 16q^2 + 16

       disc - lower = 2q^4 - 24q^2 - 29, positive from q = 4 on;
       upper - disc = 20q^2 + 20, positive always. So for q >= 4 the
       discriminant lies STRICTLY BETWEEN THE SQUARES OF TWO
       CONSECUTIVE INTEGERS and cannot be a perfect square, so r is not
       an integer. q = 3 is checked directly: disc = 3281, between
       57^2 = 3249 and 58^2 = 3364.

No c remains. SHAPE A IS EMPTY.

Note both cases collapse to the same two equations, so the split on
where r sits relative to q^3 only affects which root would have been in
range -- and a non-square discriminant has no integer root at all.

--------------------------------------------------------------------
THE ORDERING ARGUMENT FOR SHAPE B -- Level 1, closes it
--------------------------------------------------------------------
Shape B is {1, q, q^2, r, qr} with

    n = 1 + q^2 + q^4 + r^2 + q^2 r^2 = (1+q^2)(1+r^2) + q^4.

q^2 and r are coprime and both divide n, so q^2 r | n. Write n = q^2 r c.

(B-O1) r > q ALWAYS, so the case r < q never arises. The proved
       q^2 | 1+r^2 makes 1+r^2 a POSITIVE multiple of q^2, hence
       1+r^2 >= q^2 and r^2 >= q^2-1. For integers that forces r >= q,
       since r = q-1 gives r^2 = q^2-2q+1 < q^2-1 for every q > 1; and
       r != q as distinct primes. So max(prefix) = qr throughout.

(B-O2) THE EXACT IDENTITY

           c = r + (r^2+1)/(q^2 r) + (1+q^2)/r.

       With r > q the last term is below (1+q^2)/q ~ q and the middle
       term below ~1+1/q, giving c <= r + q + 1. And c > r strictly,
       because n = q^2 r^2 + q^4 + q^2 + r^2 + 1 > q^2 r^2.

(B-O3) c = q^2 EXACTLY. Since c <= r+q+1 < qr, c has no prime factor at
       or above max(prefix), so c = q^a r^b. If b >= 1 then c >= r and
       c <= r+q+1 forces q^a <= 1 + (q+1)/r < 3, so a = 0 and c = r --
       contradicting c > r. Hence b = 0 and c = q^a. Then c > r > q
       gives a >= 2, and c <= r+q+1 <= q^2+2q+2 gives a <= 2.

(B-O4) c = q^2 means n = q^4 r, i.e.

           (q^2+1) r^2 - q^4 r + (q^4+q^2+1) = 0,
           D = q^8 - 4q^6 - 8q^4 - 8q^2 - 4.

       Bracket it:
           (q^4-2q^2-7)^2 = q^8-4q^6-10q^4+28q^2+49
           (q^4-2q^2-6)^2 = q^8-4q^6- 8q^4+24q^2+36
       D - lower = 2q^4-36q^2-53, positive for q >= 5; upper - D =
       32q^2+40, positive always. Two CONSECUTIVE squares, so D is never
       a perfect square and r is never an integer. q = 1 (mod 4) was
       already forced by q^2 | 1+r^2, so q >= 5 and no small case
       remains.

SHAPE B IS EMPTY. The same three ingredients as shape A -- prefix
ordering to bound the cofactor, the cofactor collapsing to a single
value, and a discriminant trapped between consecutive squares.
"""

from typing import List, Tuple, Optional, Dict
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# =====================================================================
# 1. NUMBER-THEORETIC PRIMITIVES
# =====================================================================

def is_prime(n: int) -> bool:
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
    for a in small:                       # deterministic below 3.3 * 10^24
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

def _rho(n: int) -> int:
    from math import gcd
    if n % 2 == 0:
        return 2
    while True:
        x = random.randrange(2, n)
        y, c, d = x, random.randrange(1, n), 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d

def factor(n: int, out: Optional[Dict[int, int]] = None) -> Dict[int, int]:
    if out is None:
        out = {}
    if n == 1:
        return out
    if is_prime(n):
        out[n] = out.get(n, 0) + 1
        return out
    d = _rho(n)
    factor(d, out)
    factor(n // d, out)
    return out

def prime_divisors(n: int) -> List[int]:
    return sorted(factor(n))

def primes_upto(N: int) -> List[int]:
    sieve = bytearray([1]) * (N + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(N + 1) if sieve[i]]

# =====================================================================
# 2. THE PREFIX ORACLE (independent of every congruence above)
# =====================================================================

def first_k_divisors(n: int, k: int, cap: int) -> List[int]:
    out = []
    for d in range(1, cap + 1):
        if n % d == 0:
            out.append(d)
            if len(out) == k:
                return out
    return out

def verify_prefix(vals: Tuple[int, ...], k: int = 5) -> Optional[int]:
    """Independent check: are `vals` really the k smallest divisors of
    n = sum of their squares? This is what both near-misses fail."""
    vals = tuple(sorted(vals))
    if len(set(vals)) != k:
        return None
    n = sum(v * v for v in vals)
    if any(n % v for v in vals):
        return None
    if tuple(first_k_divisors(n, k, max(vals))) != vals:
        return None
    return n

# =====================================================================
# 3. COMPLETE PARAMETRIC SEARCHES
# =====================================================================

def search_A(qmax: int):
    """{1, q, q^2, q^3, r}. Complete for every odd prime q <= qmax."""
    cand = surv = 0
    hits = []
    for q in primes_upto(qmax):
        if q == 2:
            continue
        for r in prime_divisors(1 + q ** 4):           # (A2)
            if r == q or r <= q * q:                   # (A1)
                continue
            cand += 1
            if (1 + r * r) % (q * q):                  # (A3)
                continue
            surv += 1
            if (1 + q * q + r * r) % q ** 3:
                continue
            if verify_prefix((1, q, q * q, q ** 3, r)):
                hits.append((q, r))
    return {"candidates": cand, "survive_congruences": surv, "witnesses": hits}

def search_B(qmax: int):
    """{1, q, q^2, r, qr}. Complete for every odd prime q <= qmax."""
    cand = surv = 0
    hits, near = [], []
    for q in primes_upto(qmax):
        if q == 2:
            continue
        rs = set(prime_divisors(q * q + q + 1)) | set(prime_divisors(q * q - q + 1))
        for r in rs:                                   # (B2)
            if r == q:
                continue
            cand += 1
            if (1 + r * r) % (q * q):                  # (B1)
                continue
            surv += 1
            near.append((q, r))
            if verify_prefix((1, q, q * q, r, q * r)):
                hits.append((q, r))
    return {"candidates": cand, "survive_congruences": surv,
            "near_misses": near, "witnesses": hits}

def search_C(pmax: int):
    """{1, q, r, s, qr}, q < r < s. Complete for every pair q < r <= pmax."""
    ps = [p for p in primes_upto(pmax) if p != 2]
    pd = {p: prime_divisors(1 + p * p) for p in ps}
    cand = surv = 0
    hits, near = [], []
    for i, q in enumerate(ps):
        for r in ps[i + 1:]:
            for s in set(pd[q]) | set(pd[r]):          # (C2)
                if s <= r or s == q:
                    continue
                cand += 1
                if (1 + r * r + s * s) % q:            # (C3)
                    continue
                if (1 + q * q + s * s) % r:            # (C3)
                    continue
                surv += 1
                near.append((q, r, s))
                if verify_prefix((1, q, r, s, q * r)):
                    hits.append((q, r, s))
    return {"candidates": cand, "survive_congruences": surv,
            "near_misses": near, "witnesses": hits}

# =====================================================================
# 4. SELF-TESTS
# =====================================================================

def test_reduction_A2() -> None:
    """r > q^2 and r | (1+q^2)(1+q^4) really does imply r | q^4+1."""
    for q in primes_upto(300):
        if q == 2:
            continue
        full = prime_divisors((1 + q * q) * (1 + q ** 4))
        reduced = set(prime_divisors(1 + q ** 4))
        for r in full:
            if r != q and r > q * q:
                assert r in reduced, f"(A2) fails at q={q}, r={r}"
    print("[ok] (A2) r > q^2 forces r | q^4+1, checked against the full product")

def test_reduction_C1() -> None:
    """The prefix product must join the two SMALLEST primes."""
    from math import gcd
    from itertools import combinations
    def admissible(vals):
        top, S = max(vals), set(vals)
        return all(not (gcd(x, y) == 1 and x * y < top and x * y not in S)
                   for x, y in combinations(sorted(S), 2))
    for a, b, c in [(3,5,7), (3,5,11), (5,7,11), (3,7,11), (5,11,13), (3,11,101)]:
        assert admissible((1, a, b, c, a * b)), (a, b, c)
        assert not admissible((1, a, b, c, a * c)), (a, b, c)
        assert not admissible((1, a, b, c, b * c)), (a, b, c)
    print("[ok] (C1) only the product of the two smallest primes is admissible")

def test_near_misses_die_on_the_prefix() -> None:
    """Both survivors satisfy every congruence and fail only the prefix."""
    for vals, n_expected, intruder in [((1, 5, 7, 25, 35), 1925, 11),
                                       ((1, 3, 13, 17, 39), 1989, 9)]:
        n = sum(v * v for v in vals)
        assert n == n_expected, (n, n_expected)
        assert all(n % v == 0 for v in vals), "should divide n"
        assert n % intruder == 0 and intruder < max(vals)
        assert verify_prefix(vals) is None, "prefix check must reject"
    print("[ok] near misses: congruences all pass, prefix condition rejects")

def test_bounded_searches() -> None:
    a = search_A(3000)
    b = search_B(3000)
    c = search_C(500)
    assert a["witnesses"] == [], a
    assert b["witnesses"] == [], b
    assert c["witnesses"] == [], c
    assert a["survive_congruences"] == 0
    assert (5, 7) in b["near_misses"]
    assert (3, 13, 17) in c["near_misses"]
    print(f"[ok] searches: A q<=3000 ({a['candidates']} cand), "
          f"B q<=3000 ({b['candidates']} cand), "
          f"C q<r<=500 ({c['candidates']} cand) -- no witnesses [Level 2]")



# =====================================================================
# SHAPE A: the Level 1 closure
# =====================================================================

def shape_a_constant(q: int) -> int:
    """A = 1 + q^2 + q^4 + q^6, so that n = A + r^2."""
    return 1 + q * q + q ** 4 + q ** 6


def disc_c_equals_one(q: int) -> int:
    """(A-O4) discriminant of r^2 - q^3 r + A."""
    return q ** 6 - 4 * shape_a_constant(q)


def disc_c_equals_q(q: int) -> int:
    """(A-O5) discriminant of r^2 - q^4 r + A."""
    return q ** 8 - 4 * shape_a_constant(q)


def test_shape_a_c_is_one_or_q() -> None:
    """(A-O2)+(A-O3): the size bound leaves only c = 1 and c = q."""
    for q in range(3, 500):
        A = shape_a_constant(q)
        # case A1: q^2 < r < q^3.  max(prefix) = q^3
        for r in (q * q + 1, (q * q + q ** 3) // 2, q ** 3 - 1):
            if not (q * q < r < q ** 3):
                continue
            assert (A + r * r) / (q ** 3 * r) < q + 2, (q, r)
        # case A2: q^3 < r <= q^4+1.  max(prefix) = r
        for r in (q ** 3 + 1, q ** 4, q ** 4 + 1):
            assert (A + r * r) / (q ** 3 * r) < q + 2, (q, r)
        assert q * q >= q + 2                      # no higher power of q fits
        assert q + 2 <= q ** 3                     # c below every non-q prime
    print("[ok] (A-O2,3): size bound forces c in {1, q} in both cases")


def test_shape_a_c_one_impossible() -> None:
    """(A-O4): identity and negativity of the c = 1 discriminant."""
    for q in range(2, 2000):
        d = disc_c_equals_one(q)
        assert d == -3 * q ** 6 - 4 * q ** 4 - 4 * q * q - 4, q
        assert d < 0, q
    print("[ok] (A-O4): c=1 discriminant is -3q^6-4q^4-4q^2-4 < 0 always")


def test_shape_a_c_q_impossible() -> None:
    """(A-O5): the c = q discriminant sits between consecutive squares."""
    import math
    for q in range(3, 2000):
        d = disc_c_equals_q(q)
        lo = (q ** 4 - 2 * q * q - 5) ** 2
        hi = (q ** 4 - 2 * q * q - 4) ** 2
        assert d - lo == 2 * q ** 4 - 24 * q * q - 29, q
        assert hi - d == 20 * q * q + 20, q
        if q >= 4:
            assert lo < d < hi, q                  # consecutive squares
        assert math.isqrt(d) ** 2 != d, q          # hence never a square
    assert disc_c_equals_q(3) == 3281 and 57 ** 2 < 3281 < 58 ** 2
    print("[ok] (A-O5): c=q discriminant strictly between consecutive squares")


def test_shape_a_search_agrees() -> None:
    """The bounded search must find nothing, as the proof now requires."""
    assert search_A(20000)["witnesses"] == []
    print("[ok] shape A: proof and search agree -- empty")


def self_test_shape_a() -> None:
    test_shape_a_c_is_one_or_q()
    test_shape_a_c_one_impossible()
    test_shape_a_c_q_impossible()
    test_shape_a_search_agrees()




# =====================================================================
# SHAPE B: the Level 1 closure
# =====================================================================

def disc_shape_b(q: int) -> int:
    """(B-O4) discriminant of (q^2+1)r^2 - q^4 r + (q^4+q^2+1)."""
    return q ** 8 - 4 * (q * q + 1) * (q ** 4 + q * q + 1)


def test_shape_b_r_exceeds_q() -> None:
    """(B-O1): q^2 | 1+r^2 makes r < q impossible."""
    for q in [p for p in primes_upto(1500) if p > 2]:
        for r in range(3, q):
            assert (1 + r * r) % (q * q) != 0, (q, r)
        assert (q - 1) ** 2 < q * q - 1
    print("[ok] (B-O1): no r < q satisfies q^2 | 1+r^2; r > q always")


def test_shape_b_cofactor_identity() -> None:
    """(B-O2): the exact expression for c, and r < c <= r+q+1."""
    for q in [p for p in primes_upto(400) if p % 4 == 1]:
        for r in (q + 2, 2 * q, q * q, q * q + q + 1):
            n = (1 + q * q) * (1 + r * r) + q ** 4
            c = n / (q * q * r)
            assert abs(c - (r + (r*r+1)/(q*q*r) + (1+q*q)/r)) < 1e-6 * c
            assert r < c <= r + q + 1 + 1e-9, (q, r, c)
    print("[ok] (B-O2): identity holds and r < c <= r+q+1")


def test_shape_b_disc_never_square() -> None:
    """(B-O4): D sits strictly between consecutive squares."""
    import math
    for q in range(5, 3000):
        d = disc_shape_b(q)
        assert d == q**8 - 4*q**6 - 8*q**4 - 8*q*q - 4, q
        lo = (q**4 - 2*q*q - 7) ** 2
        hi = (q**4 - 2*q*q - 6) ** 2
        assert d - lo == 2*q**4 - 36*q*q - 53, q
        assert hi - d == 32*q*q + 40, q
        assert lo < d < hi, q
        assert math.isqrt(d) ** 2 != d, q
    print("[ok] (B-O4): D bracketed by consecutive squares, never a square")


def test_shape_b_search_agrees() -> None:
    assert search_B(20000)["witnesses"] == []
    print("[ok] shape B: proof and search agree -- empty")


def self_test_shape_b() -> None:
    test_shape_b_r_exceeds_q()
    test_shape_b_cofactor_identity()
    test_shape_b_disc_never_square()
    test_shape_b_search_agrees()


def self_test() -> None:
    test_reduction_A2()
    test_reduction_C1()
    test_near_misses_die_on_the_prefix()
    test_bounded_searches()
    self_test_shape_a()
    self_test_shape_b()
    print("\nAll self-tests passed.")
    print("SHAPE A: CLOSED at Level 1 -- c must be 1 or q, and both give a")
    print("         discriminant with no integer root.")
    print("SHAPE B: CLOSED at Level 1 -- r > q is forced, c = q^2 is forced,")
    print("         and its discriminant is never a perfect square.")
    print("SHAPE C: q=3 branch closed in k5_shape_c_q3.py; 3-does-not-divide-n open.")

if __name__ == "__main__":
    self_test()
