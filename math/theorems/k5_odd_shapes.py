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

STATUS: these shapes are NOT closed. Everything below is Level 2 --
exhaustive only up to the stated parameter bound. No Level 1 argument
for them is known to this module, and it does not pretend otherwise.

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

def self_test() -> None:
    test_reduction_A2()
    test_reduction_C1()
    test_near_misses_die_on_the_prefix()
    test_bounded_searches()
    print("\nAll self-tests passed.")
    print("NOTE: shapes A, B and C remain OPEN. The searches are exhaustive "
          "only\n      up to their parameter bounds; no Level 1 closure is claimed.")

if __name__ == "__main__":
    self_test()
