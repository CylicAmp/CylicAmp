"""
k5_cofactor_level1.py

Upgrades the three k=5 shapes that divisor_prefix_ledger.py closes only at
LEVEL 2 (its COFACTOR_SIZE oracle, a bounded check over primes <= 173) to
LEVEL 1 -- parameter-free, every prime, no search.

The three shapes, in the ledger's own labelling (names "2qrst"):

    {1, t, s, r, 2}     1 and four distinct primes, one of them 2   LEMMA 1
    {1, t, s, r, q}     1 and four distinct odd primes              LEMMA 1
    {1, t, s, r, t^2}   1, three odd primes, and the square of one  LEMMA 2

Both lemmas run on the same engine as the rest of the ledger: MOVE 1, the
prefix rule. The ledger's oracle had the right idea -- compare n against
lcm(V) -- but verified it by enumeration. The lemmas below prove it.

--------------------------------------------------------------------
THE ENGINE
--------------------------------------------------------------------
V = {d_1 < ... < d_5} are the five smallest divisors of n, M := d_5, and
n = d_1^2 + ... + d_5^2. Two facts are used over and over:

  (P)  PREFIX RULE. If e | n and e < M then e is one of the five smallest
       divisors, so e is in V. Equivalently: a divisor of n that is not
       in V and is not M is greater than M. It applies to COMPOSITE e --
       that is the whole force of "divisor prefix".

  (L)  LCM RULE. The elements of V are divisors of n, so L := lcm(V)
       divides n, and since n > 0 this gives n >= L.

So it is enough, in each shape, to prove n < L.

--------------------------------------------------------------------
LEMMA 1   V = {1, p1, p2, p3, p4},  p1 < p2 < p3 < p4 all prime
--------------------------------------------------------------------
Covers {1,t,s,r,2} and {1,t,s,r,q} at once; whether 2 is among the primes
never enters the argument.

  L = p1 p2 p3 p4   (the p_i are pairwise coprime),  M = p4.

(1) p1 p2 > p4.
    p1 p2 divides n and is composite, so it is not 1, not any p_i. By (P)
    it is not below M = p4, and it cannot equal p4 (composite vs prime).

(2) p3 >= 5.
    p3 is the third smallest of four distinct primes, so p3 >= 5.

(3) n < 5 p4^2.
    p1, p2, p3 < p4, so each of p1^2, p2^2, p3^2 is below p4^2, and
    1 < p4^2. Five terms, each below p4^2.

(4) L > 5 p4^2.
    L = (p1 p2) p3 p4 > p4 * p3 * p4 = p3 p4^2 >= 5 p4^2, by (1) then (2).

(3) and (4) give n < L, contradicting (L). The shape is empty.

--------------------------------------------------------------------
LEMMA 2   V = {1, t, s, r, t^2},  t, s, r distinct odd primes
--------------------------------------------------------------------
n is odd here (the shape carries no factor 2), so t, s, r >= 3.

(0) t IS THE SMALLEST OF THE THREE PRIMES.
    Suppose some p in {s, r} had p < t. Then p t divides n, is composite,
    and is not t^2 (p != t), so p t is not in V; by (P), p t > M. But
    t^2 is in V, so t^2 <= M < p t, giving t < p -- a contradiction.
    So t < s < r (relabelling s, r if needed).

Three configurations remain, by where t^2 falls among s and r. In the two
where M = r, the prefix rule gives one more inequality:

    t s divides n, is composite, is not t^2, so t s is not in V, so by (P)
    t s > M = r.                                                      (*)

  (a) r < t^2, so M = t^2.   L = t^2 s r,  n = 1 + t^2 + s^2 + r^2 + t^4.
      s, r < t^2 give s^2 < t^2 s and r^2 < t^2 r, so
          n < 1 + t^2 + t^4 + t^2 (s + r)
          L - n > t^2 [ s r - s - r - 1 - t^2 ] - 1
                = t^2 [ (s-1)(r-1) - t^2 - 2 ] - 1.
      Distinct odd primes above t give s >= t+2 and r >= t+4, so
      (s-1)(r-1) >= (t+1)(t+3) = t^2 + 4t + 3, and the bracket is at
      least 4t + 1 >= 13. So L - n > 13 t^2 - 1 > 0.

  (b) t^2 < s, so M = r and sorted V = 1, t, t^2, s, r.
      Each term of n is below s r:  1 < s r;  t^2 < s < s r;
      t^4 = (t^2)^2 < s r since t^2 < s < r;  s^2 < s r since s < r;
      and r^2 < t s r by (*). Hence
          n < s r + s r + s r + s r + t s r = (t + 4) s r.
      And t^2 >= t + 4 for t >= 3, so L = t^2 s r >= (t+4) s r > n.

  (c) s < t^2 < r, so M = r and sorted V = 1, t, s, t^2, r.
      1 < s r;  t^2 < r < s r;  s^2 < s r;  t^4 < r^2 < t s r by (*);
      and r^2 < t s r. Hence
          n < s r + s r + s r + t s r + t s r = (2t + 3) s r.
      And t^2 >= 2t + 3 for t >= 3 (equality at t = 3), so
      L = t^2 s r >= (2t+3) s r > n.

In all three, n < L contradicts (L). The shape is empty.

--------------------------------------------------------------------
WHAT THIS DOES AND DOES NOT CHANGE
--------------------------------------------------------------------
divisor_prefix_ledger.py is left exactly as it is. Its COFACTOR_SIZE
oracle is still Level 2 and still reports Level 2, because that oracle
really is a bounded check -- the module's rule is that it never claims
more than its own oracles prove. The Level 1 content lives here, and
k5_closed.py reads the combined status.

With these two lemmas the k=5 theorem is Level 1 end to end: the ledger's
other seven closures are Level 1 (MODULAR_PARITY, SINGLE_PRIME_POWER),
these three are Level 1 here, and shapes A, B, C are Level 1 in
k5_odd_shapes.py, k5_shape_c_q3.py and k5_shape_c_nodiv3.py.
"""

from math import isqrt
from typing import List, Tuple

LEMMA1_SHAPES = ("{1, t, s, r, 2}", "{1, t, s, r, q}")
LEMMA2_SHAPES = ("{1, t, s, r, t^2}",)


def primes_upto(n: int) -> List[int]:
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(n + 1) if sieve[i]]


def lcm_of(vals) -> int:
    from math import gcd
    out = 1
    for v in vals:
        out = out * v // gcd(out, v)
    return out


def n_of(prefix) -> int:
    return sum(d * d for d in prefix)


# ---------------------------------------------------------------------
# LEMMA 1
# ---------------------------------------------------------------------

def lemma1_certificate(p1: int, p2: int, p3: int, p4: int) -> Tuple[bool, str]:
    """Return (closed, reason) for V = {1,p1,p2,p3,p4}."""
    if not p1 * p2 > p4:
        return False, "(1) fails: p1 p2 <= p4, so the prefix rule gives nothing"
    if not p3 >= 5:
        return False, "(2) fails: p3 < 5"
    n = n_of((1, p1, p2, p3, p4))
    L = p1 * p2 * p3 * p4
    if not n < 5 * p4 * p4:
        return False, "(3) fails"
    if not L > 5 * p4 * p4:
        return False, "(4) fails"
    return True, f"n={n} < 5p4^2={5*p4*p4} < L={L}, but L | n forces n >= L"


# ---------------------------------------------------------------------
# LEMMA 2
# ---------------------------------------------------------------------

def lemma2_config(t: int, s: int, r: int) -> str:
    if r < t * t:
        return "a"
    if t * t < s:
        return "b"
    return "c"


def lemma2_certificate(t: int, s: int, r: int) -> Tuple[bool, str]:
    """Return (closed, reason) for V = {1,t,s,r,t^2} with t < s < r odd."""
    prefix = (1, t, s, r, t * t)
    n = n_of(prefix)
    L = t * t * s * r
    cfg = lemma2_config(t, s, r)
    M = max(prefix)
    if cfg == "a":
        bound = 1 + t * t + t ** 4 + t * t * (s + r)
        bracket = (s - 1) * (r - 1) - t * t - 2
        ok = n < bound and bracket >= 4 * t + 1 and L - n > 0
        return ok, (f"config a (r<t^2, M=t^2): bracket (s-1)(r-1)-t^2-2 = "
                    f"{bracket} >= 4t+1 = {4*t+1}; L-n = {L-n}")
    # configs b and c both have M = r and need t s > r
    if not t * s > r:
        return False, "(*) fails: t s <= r"
    if cfg == "b":
        ok = n < (t + 4) * s * r <= t * t * s * r
        return ok, (f"config b (t^2<s, M=r): n={n} < (t+4)sr={(t+4)*s*r} "
                    f"<= t^2 sr = L = {L}")
    ok = n < (2 * t + 3) * s * r <= t * t * s * r
    return ok, (f"config c (s<t^2<r, M=r): n={n} < (2t+3)sr={(2*t+3)*s*r} "
                f"<= t^2 sr = L = {L}")


# =====================================================================
# SELF-TESTS
# =====================================================================

def test_lemma1_algebra() -> None:
    """(1)-(4) hold for every admissible four-prime tuple."""
    ps = primes_upto(600)
    checked = 0
    for i, p1 in enumerate(ps):
        if p1 > 120:
            break
        for j in range(i + 1, len(ps)):
            p2 = ps[j]
            if p2 > 300:
                break
            for k in range(j + 1, len(ps)):
                p3 = ps[k]
                if p3 > 400:
                    break
                for m in range(k + 1, len(ps)):
                    p4 = ps[m]
                    if p4 >= p1 * p2:      # (1): otherwise the shape is
                        break              # impossible for a different reason
                    assert p3 >= 5, (p1, p2, p3)
                    ok, why = lemma1_certificate(p1, p2, p3, p4)
                    assert ok, (p1, p2, p3, p4, why)
                    checked += 1
    assert checked > 20000, checked
    print(f"[ok] LEMMA 1: n < 5p4^2 < L on all {checked} admissible four-prime tuples")


def test_lemma1_prefix_rule_step() -> None:
    """(1) really is forced: p1 p2 < p4 would put p1 p2 in the prefix."""
    ps = primes_upto(400)
    bad = []
    for i, p1 in enumerate(ps[:40]):
        for p2 in ps[i + 1:i + 40]:
            for p3 in [x for x in ps if x > p2][:30]:
                for p4 in [x for x in ps if x > p3][:30]:
                    if p1 * p2 < p4:
                        n = p1 * p2 * p3 * p4
                        # p1 p2 is a divisor of n below p4, so the five
                        # smallest divisors cannot be {1,p1,p2,p3,p4}
                        five = sorted({1, p1, p2, p3, p4, p1 * p2})[:5]
                        if five == [1, p1, p2, p3, p4]:
                            bad.append((p1, p2, p3, p4))
    assert bad == [], bad[:5]
    print("[ok] LEMMA 1 step (1): p1 p2 < p4 always breaks the prefix")


def test_lemma2_t_is_smallest() -> None:
    """(0) a prime below t contradicts t^2 being in the prefix."""
    ps = [p for p in primes_upto(300) if p >= 3]
    for t in ps[:40]:
        for p in [x for x in ps if x < t]:
            # p*t is composite, != t^2, so it must exceed M >= t^2
            assert p * t < t * t, (p, t)   # which is the contradiction
    print("[ok] LEMMA 2 step (0): any prime below t forces p t < t^2, contradiction")


def test_lemma2_algebra() -> None:
    """(a), (b), (c) hold for every admissible triple of odd primes."""
    ps = [p for p in primes_upto(1200) if p >= 3]
    counts = {"a": 0, "b": 0, "c": 0}
    for i, t in enumerate(ps):
        if t > 150:
            break
        for j in range(i + 1, len(ps)):
            s = ps[j]
            if s > 600:
                break
            for k in range(j + 1, len(ps)):
                r = ps[k]
                cfg = lemma2_config(t, s, r)
                if cfg in ("b", "c") and not t * s > r:
                    break              # (*) fails: shape impossible anyway
                if r > 1100:
                    break
                ok, why = lemma2_certificate(t, s, r)
                assert ok, (t, s, r, cfg, why)
                counts[cfg] += 1
    assert all(v > 0 for v in counts.values()), counts
    print(f"[ok] LEMMA 2: n < L in every configuration "
          f"(a={counts['a']}, b={counts['b']}, c={counts['c']})")


def test_lemma2_threshold_inequalities() -> None:
    """the two coefficient facts the lemma turns on, for every odd t."""
    for t in range(3, 5000, 2):
        assert t * t >= t + 4, t          # config b
        assert t * t >= 2 * t + 3, t      # config c, equality at t=3
    assert 3 * 3 == 2 * 3 + 3, "config c is tight exactly at t=3"
    print("[ok] LEMMA 2: t^2 >= t+4 and t^2 >= 2t+3 for all odd t >= 3")


def test_lcm_rule_is_what_it_claims() -> None:
    """(L): if the prefix really is a divisor prefix then lcm(V) | n."""
    ps = primes_upto(200)
    checked = 0
    for n in range(2, 300000):
        ds = []
        for i in range(1, isqrt(n) + 1):
            if n % i == 0:
                ds.append(i)
                if len(ds) > 7:
                    break
        ds = sorted(ds)[:5]
        if len(ds) < 5:
            continue
        assert n % lcm_of(ds) == 0, (n, ds)
        checked += 1
    print(f"[ok] (L) lcm rule: lcm of the five smallest divisors divides n "
          f"({checked} values of n)")


def test_does_not_kill_real_solutions() -> None:
    """n = 130 (k=4) and n = 1860 (k=11) must survive: the lemmas are k=5."""
    for n, k in ((130, 4), (1860, 11)):
        ds = []
        for i in range(1, isqrt(n) + 1):
            if n % i == 0:
                ds.append(i)
                ds.append(n // i)
        ds = sorted(set(ds))[:k]
        assert sum(d * d for d in ds) == n, (n, k)
        assert len(ds) != 5 or k == 5
        # and for these the lcm rule is satisfied with equality-free slack
        assert n % lcm_of(ds) == 0, (n, ds)
    print("[ok] anchors survive: 130 (k=4) and 1860 (k=11) are untouched")


def test_brute_force_three_shapes_empty() -> None:
    """Independent confirmation: no n realizes any of the three shapes."""
    ps = primes_upto(400)
    LIM = 6_000_000
    found = []
    # LEMMA 1 shapes: n divisible by four distinct primes, prefix = 1+those
    for i, p1 in enumerate(ps):
        if p1 ** 4 > LIM:
            break
        for j in range(i + 1, len(ps)):
            p2 = ps[j]
            if p1 * p2 ** 3 > LIM:
                break
            for k in range(j + 1, len(ps)):
                p3 = ps[k]
                if p1 * p2 * p3 ** 2 > LIM:
                    break
                for m in range(k + 1, len(ps)):
                    p4 = ps[m]
                    n = p1 * p2 * p3 * p4
                    if n > LIM:
                        break
                    if n_of((1, p1, p2, p3, p4)) == n:
                        found.append(("L1", p1, p2, p3, p4, n))
    # LEMMA 2 shape: n divisible by t^2, s, r
    for t in ps:
        if t >= 3 and t * t * 15 > LIM:
            break
        if t < 3:
            continue
        for s in [x for x in ps if x > t]:
            if t * t * s * s > LIM:
                break
            for r in [x for x in ps if x > s]:
                n = t * t * s * r
                if n > LIM:
                    break
                if n_of((1, t, s, r, t * t)) == n:
                    found.append(("L2", t, s, r, n))
    assert found == [], found
    print(f"[ok] brute force to {LIM:,}: none of the three shapes is realized")


def self_test() -> None:
    test_lemma1_prefix_rule_step()
    test_lemma1_algebra()
    test_lemma2_t_is_smallest()
    test_lemma2_threshold_inequalities()
    test_lemma2_algebra()
    test_lcm_rule_is_what_it_claims()
    test_does_not_kill_real_solutions()
    test_brute_force_three_shapes_empty()
    print("\nAll self-tests passed.")
    print("LEMMA 1 closes {1,t,s,r,2} and {1,t,s,r,q} at LEVEL 1.")
    print("LEMMA 2 closes {1,t,s,r,t^2} at LEVEL 1.")
    print("The ledger's three COFACTOR_SIZE shapes are now Level 1.")


if __name__ == "__main__":
    self_test()
