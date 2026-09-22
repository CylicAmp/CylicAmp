"""
k5_shape_c_q3.py

Shape C of the k=5 ledger, reduced to its one live branch.

Shape C is {1, q, r, s, qr} with q < r < s. Song's mod-3 count lemma
(commit 02ae900) kills s=3, and r=3 needs r < q, so when 3 | n the only
survivor is q=3:

        prefix {1, 3, r, s, 3r},   3 < r < s,   n = 10(1+r^2) + s^2

STATUS: this branch is CLOSED. The ordering argument at the bottom of
this docstring proves it empty at Level 1, for every r and s.

SCOPE, precisely: what closes is the 3 | n branch of shape C, which is
exactly the branch that forces q = 3. The 3-does-NOT-divide-n branch of
shape C (all three primes above 3) is a DIFFERENT case and is UNTOUCHED
here -- with c = 0 the count lemma gives n = 5 = 2 (mod 3), consistent
with 3 not dividing n, so it yields no contradiction. Shape C as a whole
is therefore not yet closed.

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

--------------------------------------------------------------------
THE VIETA DESCENT DOES NOT CLOSE THIS -- tried, and why it fails
--------------------------------------------------------------------
m*r*t = r^2 + 10t^2 + 1 is not Vieta-symmetric as written: jumping in t
gives non-integers, because the quadratic in t has leading coefficient
10. Substituting T = 10t repairs it:

        10x^2 + y^2 + 10 = m*x*y            (E)

and (E) recovers the whole structure. For fixed x the two y-roots are
exactly 10t and s, since s + 10t = m*r and s*10t = 10(r^2+1). The known
pair appears as the two roots over x = 13: (13, 100) with t = 10, and
(13, 17) with s = 17, both giving m = 9.

Both jumps are then integral:

    y-jump   y' = m*x - y,      y*y'  = 10(x^2 + 1)   -- always
    x-jump   x' = m*y/10 - x,   x*x'  = (y^2 + 10)/10 -- only if 10 | y

TWO OBSTRUCTIONS, both fatal to the approach.

1. m is NOT pinned by the equation. Solutions exist for
   m in {9, 12, 15, 21, 33, 36, 51, 111, 132, 261, ...}. The Diophantine
   side of the problem does not single out 9 at all. What removes the
   other m is that r and s must be PRIME, that s > r, and that t is
   even -- arithmetic side conditions the Vieta structure cannot see.
   m = 15 is the sharpest case: (r, t, s) = (7, 10, 5) has all three of
   r, s prime and t even, and fails ONLY on s > r.

2. The descent has NO FINITE BASE. A solution descends in y when
   y^2 > 10(x^2+1), and in x only when 10 | y. So whenever 10 does not
   divide y, the x-jump is unavailable and minimality reduces to
   y^2 <= 10(x^2+1) -- satisfied by any small y beside a large x. The
   minimal set is therefore infinite: (1,1), (1,2), (1,4), (7,2), (7,5),
   (11,1), (13,4), (13,17), (127,25), (343,26), ... A Markov-style
   argument needs a finite set of descent roots to classify. There is
   none here.

So the closure, if it exists, is not a descent argument. That matches
what the sweeps already showed: both near-misses satisfy every
congruence and die on the PREFIX condition, which is a statement about
the ORDER of divisors, not about the equation.

--------------------------------------------------------------------
THE ORDERING ARGUMENT -- Level 1, closes the branch
--------------------------------------------------------------------
Write n = 3*r*s*m', so that m = 3m'.

(O1) 3 | m, because 3 | n and 3 divides neither r nor s. And 3 does not
     divide m', because 9 does not divide n by (C2).

(O2) EVERY PRIME FACTOR OF m' IS AT LEAST r. A prime p | n with
     p < max(prefix) is a divisor below the largest prefix element, so
     it must BE in the prefix, hence p is 3, r or s. Since 3 does not
     divide m', every prime factor of m' is r, s, or >= max(prefix) --
     and all three of those are >= r. So

         m' = 1   or   m' >= r.

(O3) SIZE BOUND. s and s' = 10(r^2+1)/s are the roots of
     X^2 - m*r*X + 10(r^2+1), so

         m = s/r + 10(r^2+1)/(r*s) =: f(s),

     convex in s with its minimum at s = sqrt(10(r^2+1)). The range of s
     is bounded on both sides: s > r, and s <= (r^2+1)/2, because r is
     odd so r^2+1 = 2u with u ODD, and s is an odd divisor of 2u, hence
     a divisor of u. A convex function on an interval is maximised at an
     endpoint, so

         m <= max( f(r), f((r^2+1)/2) )
            = max( 11 + 10/r^2,  (r^2+41)/(2r) ).

(O4) m' >= r IS IMPOSSIBLE. It would give m = 3m' >= 3r, but
       3r > 11 + 10/r^2     iff  3r^3 - 11r^2 - 10 > 0, true for r >= 4;
       3r > (r^2+41)/(2r)   iff  5r^2 > 41,             true for r >= 3.
     Both hold for every r >= 5, so 3r exceeds the bound in (O3).

(O5) Hence m' = 1 by (O2), i.e. m = 3. But then the quadratic
     X^2 - 3rX + 10(r^2+1) has discriminant

         9r^2 - 40(r^2+1) = -31r^2 - 40 < 0

     for every r, so no real s exists at all -- let alone a prime one.

CONTRADICTION in every case. The branch is empty.

This is why neither congruences nor the Vieta descent could finish it:
both are blind to the ORDER of the divisors, and (O2) -- the step that
does the work -- is purely a statement about which primes are allowed
to sit below the fifth-smallest divisor. The two near-misses are not
coincidences but the predicted shape of the failure: each sits in the
window where f forces m = 9, and 9 | m is exactly what the prefix
forbids.
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




# =====================================================================
# THE VIETA FORM (recorded as a ruled-out route, not a closure)
# =====================================================================

def vieta_m(x: int, y: int) -> int:
    """m for the substituted equation 10x^2 + y^2 + 10 = m*x*y, or 0."""
    num = 10 * x * x + y * y + 10
    return num // (x * y) if num % (x * y) == 0 else 0


def vieta_y_jump(x: int, y: int, m: int) -> int:
    """The other y-root. Always integral: y*y' = 10(x^2+1)."""
    return m * x - y


def vieta_x_jump(x: int, y: int, m: int) -> int:
    """The other x-root. Integral only when 10 | y."""
    if y % 10:
        return 0
    return m * y // 10 - x


def vieta_is_minimal(x: int, y: int, m: int) -> bool:
    """No available jump decreases. Note this set is INFINITE."""
    if vieta_y_jump(x, y, m) < y:
        return False
    if y % 10 == 0 and vieta_x_jump(x, y, m) < x:
        return False
    return True


def test_vieta_substitution() -> None:
    """T = 10t turns the form Vieta-symmetric and recovers the known pair."""
    r, t, s = 13, 10, 17
    assert vieta_m(r, 10 * t) == 9 and vieta_m(r, s) == 9
    # the two y-roots over x=r are exactly 10t and s
    assert vieta_y_jump(r, 10 * t, 9) == s
    assert vieta_y_jump(r, s, 9) == 10 * t
    assert s * (10 * t) == 10 * (r * r + 1)
    assert s + 10 * t == 9 * r
    # the x-jump needs 10 | y
    assert vieta_x_jump(r, s, 9) == 0
    assert vieta_x_jump(r, 10 * t, 9) == (10 * t * t + 1) // r == 77
    print("[ok] Vieta form: 10x^2+y^2+10 = mxy, roots over x=13 are 100 and 17")


def test_vieta_does_not_force_m() -> None:
    """Obstruction 1: many m admit solutions, so the equation alone is silent."""
    found = {vieta_m(x, y) for x in range(1, 1200) for y in range(1, 1200)}
    found.discard(0)
    for expected in (9, 12, 15, 21, 33, 36, 111):
        assert expected in found, expected
    assert len(found) > 1, "m would be pinned, which it is not"
    # the sharpest near-case: r,s prime and t even, failing only on s > r
    assert vieta_m(7, 100) == 15 and vieta_m(7, 5) == 15
    assert is_prime(7) and is_prime(5) and (100 // 10) % 2 == 0
    assert 5 < 7, "m=15 is excluded by s > r alone"
    print("[ok] obstruction 1: m is not pinned; m=15 dies only on s > r")


def test_vieta_has_no_finite_base() -> None:
    """Obstruction 2: the minimal set is infinite, so there is nothing to classify."""
    mins = []
    for x in range(1, 4000):
        for y in range(1, 40):
            m = vieta_m(x, y)
            if m and y % 10 and vieta_is_minimal(x, y, m):
                mins.append((x, y))
    assert len(mins) >= 8, mins
    # they keep appearing as x grows, because 10 does not divide y
    assert max(x for x, _ in mins) > 100
    print(f"[ok] obstruction 2: {len(mins)} minimal solutions with y < 40; "
          f"largest x = {max(x for x, _ in mins)}")




# =====================================================================
# THE ORDERING ARGUMENT (Level 1 closure of this branch)
# =====================================================================

def f_bound(s: float, r: int) -> float:
    """m as a function of s: f(s) = s/r + 10(r^2+1)/(r s), convex in s."""
    return s / r + 10 * (r * r + 1) / (r * s)


def m_upper_bound(r: int) -> float:
    """(O3). f is convex, so its max over r < s <= (r^2+1)/2 is at an endpoint."""
    return max(f_bound(r, r), f_bound((r * r + 1) / 2, r))


def test_s_upper_bound() -> None:
    """(O3): r odd makes r^2+1 = 2u with u odd, so an odd s divides u."""
    for r in [p for p in primes_upto(1500) if p > 3]:
        u = (r * r + 1) // 2
        assert u % 2 == 1, r                      # r^2+1 = 2 (mod 8)
        for s in prime_divisors(r * r + 1):
            if s == 2:
                continue
            assert u % s == 0 and s <= u, (r, s)
    print("[ok] (O3): every odd s dividing r^2+1 satisfies s <= (r^2+1)/2")


def test_m_prime_bound() -> None:
    """(O4): 3r always exceeds the (O3) bound, so m' >= r is impossible."""
    for r in range(5, 5000):
        assert 3 * r > m_upper_bound(r), r
        assert 3 * r ** 3 - 11 * r * r - 10 > 0, r      # 3r > 11 + 10/r^2
        assert 5 * r * r > 41, r                        # 3r > (r^2+41)/(2r)
    print("[ok] (O4): 3r > max(f(r), f((r^2+1)/2)) for every r >= 5")


def test_m_equals_three_impossible() -> None:
    """(O5): m = 3 leaves the quadratic with a negative discriminant."""
    for r in range(1, 20000):
        assert 9 * r * r - 40 * (r * r + 1) < 0, r
    print("[ok] (O5): m = 3 gives discriminant -31r^2-40 < 0, no real s")


def test_branch_is_empty() -> None:
    """The chain (O2)+(O4)+(O5) leaves no case, and the sweeps agree."""
    for r, s, t, m in search_by_r(60000):
        # every surviving pair must land on the forced value m = 9
        assert m == 9, (r, s, m)
        assert m <= m_upper_bound(r) + 1e-9, (r, m)
        assert n_of(r, s) % 9 == 0                  # so the prefix breaks
    assert surviving_witnesses(search_by_r(60000)) == []
    print("[ok] branch empty: m' = 1 forces m = 3, which has no real s")


def self_test_ordering() -> None:
    test_s_upper_bound()
    test_m_prime_bound()
    test_m_equals_three_impossible()
    test_branch_is_empty()


def self_test() -> None:
    test_reductions()
    test_identity()
    test_both_sweeps_agree()
    test_known_pair_dies_on_nine()
    test_no_witnesses()
    test_vieta_substitution()
    test_vieta_does_not_force_m()
    test_vieta_has_no_finite_base()
    self_test_ordering()
    print("\nAll self-tests passed.")
    print("RESULT: the q=3 branch of shape C is CLOSED at Level 1 by the")
    print("        ordering argument (O1)-(O5).")
    print("SCOPE:  shape C's 3-does-not-divide-n branch (q > 3) is untouched,")
    print("        so shape C as a whole is not yet closed.")


if __name__ == "__main__":
    self_test()
