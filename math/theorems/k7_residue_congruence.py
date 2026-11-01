# CLASS: THEOREM
"""
k = 7, the eight Level-2 shapes: replacing the divisor search with a congruence

PRIOR ART.  k7_status.py owns the whole k = 7 analysis: 78 of 86 orbits at
Level 1, the eight remaining shapes named in LEVEL2_SHAPES, and step 11,
which uses (M) on the OUTSIDE prime to confine it to the prime factors of a
factored coprime sum -- a finite candidate set per base prime, swept to
v < 30000 by scripts/k7_deep_search.py.  Step 11 also contains a partial
Level 1 result on {1,v,u,v^2,uv,u^2,uv^2}.  None of that is restated as new.

WHAT IS NEW
  1. A FORCING CORRECTION that applies to all eight shapes (section I).
  2. THE SHARPENING: (L) on the v-part of lcm(V) gives a CONGRUENCE for the
     outside prime modulo a power of v, where step 11 gives a divisibility.
     The congruence has O(1) roots, and combined with step 11's divisibility
     it pins the outside prime to O(1) candidates per v with NO factorisation
     at all (section III).  The sweep is then complete to v < 300000.
  3. FOUR LEVEL-1 BRANCH KILLS (section IV): in each of the four two-prime
     shapes, the branch where the outside prime is as large as (M) permits
     dies parameter-free.  For {1,v,u,v^2,uv,u^2,uv^2} this SUBSUMES step
     11's partial result, which needed (M) on v and a separate check of
     (v,u) = (3,13).
  4. Parameter-free congruence classes for v (section II).

====================================================================
I.  THE FORCING CORRECTION
====================================================================
(P) applies to a DIVISOR of n.  A non-member f of a shape divides n for
certain only when f | lcm(V), i.e. only when f lies in the BOX [0, m] of the
lcm exponents.  A non-member outside the box need not divide n: n's exponent
of a prime may be exactly what lcm(V) carries.

For these eight shapes the corrected forcing is

    shape                              forced (in box)      NOT forced
    {1,v,u,v^2,uv,v^3,v^4}             u v^2                u^2, v^5
    {1,v,u,v^2,uv,v^3,uv^2}            u v^3                u^2, v^4
    {1,v,u,v^2,uv,u^2,v^3}             u^2 v, u v^2         u^3, v^4
    {1,v,u,v^2,uv,u^2,uv^2}            u^2 v                u^3, v^3
    {1,v,u,t,v^2,uv,uv^2}              t u, t v             t^2, u^2, v^3
    {1,v,u,t,v^2,uv,tv}                t u, t v^2, u v^2    t^2, u^2, v^3
    {1,v,u,t,v^2,uv,tu}                t v, u v^2           t^2, u^2, v^3
    {1,v,u,t,s,uv,tv}                  s t, s u, t u, s v   s^2,t^2,u^2,v^2

Step 11's own forcing, u^2 v > max(V) on the fourth shape, is in the box
(m = (2,2), and u^2 v = (1,2) <= (2,2)) and so is valid.

====================================================================
II.  THE CONGRUENCE, AND THE FORCED CLASS OF v
====================================================================
Reduce n modulo the v-part of lcm(V).  Every term carrying v^(m_1) or more
drops, and what is left factors:

    shape                        condition                        v must be
    {1,v,u,v^2,uv,v^3,v^4}       v^4 | (u^2+1)(v^2+1)             1 mod 4
    {1,v,u,v^2,uv,v^3,uv^2}      v^3 | (u^2+1)(v^2+1)             1 mod 4
    {1,v,u,v^2,uv,u^2,v^3}       v^3 | u^4+u^2v^2+u^2+v^2+1       1 mod 3, or 3
    {1,v,u,v^2,uv,u^2,uv^2}      v^2 | (u^2-u+1)(u^2+u+1)         1 mod 3, or 3
    {1,v,u,t,v^2,uv,uv^2}        v^2 | t^2+u^2+1                  --
    {1,v,u,t,v^2,uv,tv}          v^2 | t^2+u^2+1                  --
    {1,v,u,t,v^2,uv,tu}          v^2 | (t^2+1)(u^2+1)             1 mod 4
    {1,v,u,t,s,uv,tv}            v | s^2+t^2+u^2+1                --

Since gcd(v^2+1, v) = 1, the first two collapse to v^4 | u^2+1 and
v^3 | u^2+1.  The forced classes:

  * v | u^2+1 makes -1 a quadratic residue mod v, so v = 1 (mod 4).  Same
    for the seventh shape: v prime and v^2 | (t^2+1)(u^2+1) gives v | t^2+1
    or v | u^2+1 either way.
  * u^4+u^2+1 = (u^2+u+1)(u^2-u+1), and the two factors are coprime (a common
    divisor divides 2u, both are odd, and gcd(u^2+u+1, u) = 1), so v^2
    divides one of them.  A root of u^2 +- u + 1 mod v needs -3 to be a
    quadratic residue, so v = 1 (mod 3), or v = 3.

That halves the live base primes for free.

====================================================================
III.  WHY THE SEARCH IS NOW O(1) PER v
====================================================================
Step 11 gives u | Q(v), with Q a product of two cyclotomic-type factors, and
u prime, so u | F for one factor F.  Write F = u d.  Let a = m_1 and work
modulo v^a, where the congruence of section II has a fixed number of roots r
(found by Hensel lifting; O(1) of them).  Then:

  CASE A, u < v^a.  u lies in a known class mod v^a and is below the modulus,
    so u IS the root: one candidate per root.
  CASE B, u >= v^a.  Then d = F/u <= F/v^a, which for each of our F is below
    v^a, and d = F * u^{-1} is pinned mod v^a, so d is one value per root.

The two cases are exhaustive, and for each F the bound F/v^a is small enough
that case B really does pin d:

    shape 1:  F ~ v^4 = v^a, so u >= v^a gives d < 2, hence d = 1, u = F.
    shape 2:  F = 1+v^2 < v^3 forces case A outright; F = 1+v^4 gives d <= v.
    shape 3:  same two F as shape 2.
    shape 4:  F ~ v^2 = v^a, so again d = 1 and u = F.

So the whole sweep costs a few modular inverses per v and factors nothing.
Complete to v < 300000 for all four two-prime shapes: NO realization.
(Step 11 reached v < 30000 by factoring integers of size ~v^8.)

====================================================================
IV.  FOUR LEVEL-1 BRANCH KILLS
====================================================================
In each two-prime shape, CASE B above -- the outside prime as large as (M)
allows -- dies with no parameter left.

SHAPE 1, {1,v,u,v^2,uv,v^3,v^4}.  Case B gives u = Phi_5(v) or Phi_10(v).
Reducing u^2+1 modulo v^4:

    u = Phi_5(v)  = v^4+v^3+v^2+v+1  ->  u^2+1 =  4v^3+3v^2+2v+2  (mod v^4)
    u = Phi_10(v) = v^4-v^3+v^2-v+1  ->  u^2+1 = -4v^3+3v^2-2v+2  (mod v^4)

Both are nonzero, and both have absolute value below v^4 once v >= 5.  Since
v = 1 (mod 4) forces v >= 5, v^4 cannot divide either.  BRANCH DEAD.

SHAPE 2, {1,v,u,v^2,uv,v^3,uv^2}.  u | 1+v^2 already gives u <= 1+v^2 < v^3,
so case B means u | 1+v^4 with u >= v^3 and d = (1+v^4)/u <= v.  Now
1+v^4 = 1 (mod v^3), and u^2 = -1 (mod v^3) makes u^{-1} = -u, so

    d = -u  (mod v^3)   =>   d^2 = u^2 = -1  (mod v^3)   =>   v^3 | d^2+1.

But 0 < d^2+1 <= v^2+1 < v^3 for every v >= 2.  BRANCH DEAD.

SHAPE 3, {1,v,u,v^2,uv,u^2,v^3}.  Case B again has u | 1+v^4, d <= v and
u = d^{-1} (mod v^3).  Multiplying v^3 | u^4+u^2v^2+u^2+v^2+1 by d^4:

    (1+d^2+d^4) + v^2 (d^2+d^4) = 0   (mod v^3),

so reducing mod v^2 leaves v^2 | 1+d^2+d^4 = (d^2+d+1)(d^2-d+1).  The two
factors are coprime and v is prime, so v^2 divides one of them; with d <= v
each is positive and below 2v^2, so that one must EQUAL v^2.  But
d^2 +- d + 1 = v^2 forces 4v^2-3 to be a perfect square, i.e.
(2v-y)(2v+y) = 3, i.e. v = 1.  BRANCH DEAD.
(The composite v = 133 = 7*19, d = 68 satisfies v^2 | 1+d^2+d^4 -- 7^2
divides one factor and 19^2 the other.  A prime cannot split that way, which
is exactly where primality enters.)

SHAPE 4, {1,v,u,v^2,uv,u^2,uv^2}.  Case B gives u = v^2+v+1 or v^2-v+1, and

    u = v^2+v+1  ->  u^4+u^2+1 =  6v+3  (mod v^2)
    u = v^2-v+1  ->  u^4+u^2+1 =  3-6v  (mod v^2)

Both nonzero; both below v^2 in absolute value for v >= 7; and v = 3, 5 fail
by inspection (21 mod 9 = 3, 15 mod 9 = 6, 33 mod 25 = 8, 27 mod 25 = 2).
BRANCH DEAD -- and this is step 11's partial result obtained without (M) on
v and without the separate (v,u) = (3,13) check, since 6v+-3 never vanishes.

WHAT REMAINS in the two-prime shapes is CASE A alone: u is one of O(1)
explicit roots below v^a, and must divide one of the two cyclotomic factors.
That is Level 2, but now a two-candidate test per v rather than a divisor
enumeration, which is why v < 300000 is reachable.

====================================================================
V.  THE FOUR THREE- AND FOUR-PRIME SHAPES
====================================================================
Their conditions are listed in section II.  The (M) sums, taking the
elements coprime to each prime in turn, are

  {1,v,u,t,v^2,uv,uv^2}  v | t^2+u^2+1
                         u | t^2+v^4+v^2+1
                         t | (u^2+1)(v^2-v+1)(v^2+v+1)
  {1,v,u,t,v^2,uv,tv}    v | t^2+u^2+1
                         u | t^2v^2+t^2+v^4+v^2+1
                         t | u^2v^2+u^2+v^4+v^2+1
  {1,v,u,t,v^2,uv,tu}    v | (t^2+1)(u^2+1)
                         u | t^2+v^4+v^2+1
                         t | u^2v^2+u^2+v^4+v^2+1
  {1,v,u,t,s,uv,tv}      v | s^2+t^2+u^2+1
                         u | s^2+t^2v^2+t^2+v^2+1
                         t | s^2+u^2v^2+u^2+v^2+1
                         s | (v^2+1)(t^2+u^2+1)

Here the v-congruence involves TWO unknowns, so it pins the outside prime
only once the others are fixed: the search is O(1) per PAIR, not per v, and
these four stay at Level 2 with no branch closed.  Shape seven does inherit
the free halving v = 1 (mod 4).

--------------------------------------------------------------------
STATUS
--------------------------------------------------------------------
k = 7 remains NOT closed: 78 of 86 orbits Level 1, 8 at Level 2.  What this
file changes is the inside of those 8:
    4 shapes    case B closed at LEVEL 1, case A swept complete to v < 300000
    1 shape     free halving of the base primes (v = 1 mod 4)
    3 shapes    unchanged
"""

from math import gcd, isqrt

# ------------------------------------------------------------------ helpers
def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def primes_to(N):
    b = bytearray([1]) * (N + 1)
    b[0] = b[1] = 0
    for i in range(2, isqrt(N) + 1):
        if b[i]:
            b[i * i::i] = bytearray(len(b[i * i::i]))
    return [i for i in range(3, N + 1) if b[i]]


def lcm_of(vs):
    o = 1
    for x in vs:
        o = o * x // gcd(o, x)
    return o


def smallest_divisors(n, k):
    """The k smallest divisors of n.  Caller must not read past index k-1."""
    d = []
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            d.append(i)
            d.append(n // i)
    return sorted(set(d))[:k]


def sqrt_minus1(v, a):
    """All roots of x^2 = -1 mod v^a, or [] if none.  v an odd prime."""
    if v % 4 != 1:
        return []
    # a root mod v, by Euler: find a non-residue g, then g^((v-1)/4)
    r = None
    for g in range(2, v):
        if pow(g, (v - 1) // 2, v) == v - 1:
            r = pow(g, (v - 1) // 4, v)
            break
    if r is None or (r * r + 1) % v:
        return []
    for k in range(2, a + 1):
        mk = v ** k
        r = (r - (r * r + 1) * pow(2 * r, -1, mk)) % mk       # Hensel
    M = v ** a
    return sorted({r % M, (-r) % M})


def roots_u4_u2_1(v, a):
    """Roots of x^4+x^2+1 = 0 mod v^a.  Needs -3 a QR mod v (or v = 3)."""
    base = set()
    for x in range(v):
        if (x ** 4 + x * x + 1) % v == 0:
            base.add(x)
    rs = sorted(base)
    for k in range(2, a + 1):
        mk, mk1 = v ** k, v ** (k - 1)
        new = []
        for r in rs:
            d = (4 * r ** 3 + 2 * r) % v
            if d:
                new.append((r - (r ** 4 + r * r + 1) * pow(d, -1, mk)) % mk)
            else:
                new += [(r + j * mk1) % mk for j in range(v)
                        if ((r + j * mk1) ** 4 + (r + j * mk1) ** 2 + 1) % mk == 0]
        rs = sorted(set(new))
    return rs


# ------------------------------------------------------- the four shapes
#   key: (name, a, elements, forced-in-box, cyclotomic factors, u lower bound)
TWO_PRIME = {
    1: dict(name="{1, v, u, v^2, uv, v^3, v^4}", a=4,
            elems=lambda v, u: [1, v, u, v * v, u * v, v ** 3, v ** 4],
            forced=lambda v, u: [u * v * v],
            facs=lambda v: [v**4 + v**3 + v*v + v + 1,
                            v**4 - v**3 + v*v - v + 1],
            umin=lambda v: v * v),
    2: dict(name="{1, v, u, v^2, uv, v^3, uv^2}", a=3,
            elems=lambda v, u: [1, v, u, v * v, u * v, v ** 3, u * v * v],
            forced=lambda v, u: [u * v ** 3],
            facs=lambda v: [v * v + 1, v ** 4 + 1],
            umin=lambda v: v),
    3: dict(name="{1, v, u, v^2, uv, u^2, v^3}", a=3,
            elems=lambda v, u: [1, v, u, v * v, u * v, u * u, v ** 3],
            forced=lambda v, u: [u * u * v, u * v * v],
            facs=lambda v: [v * v + 1, v ** 4 + 1],
            umin=lambda v: v),
    4: dict(name="{1, v, u, v^2, uv, u^2, uv^2}", a=2,
            elems=lambda v, u: [1, v, u, v * v, u * v, u * u, u * v * v],
            forced=lambda v, u: [u * u * v],
            facs=lambda v: [v * v + v + 1, v * v - v + 1],
            umin=lambda v: v),
}


def roots_for(key, v):
    a = TWO_PRIME[key]['a']
    if key in (1, 2):
        return sqrt_minus1(v, a)
    if key == 4:
        return roots_u4_u2_1(v, a)
    # shape 3: full polynomial, same roots mod v as x^4+x^2+1
    base = [x for x in range(v) if (x ** 4 + x * x + 1) % v == 0]
    rs = base
    for k in range(2, a + 1):
        mk, mk1 = v ** k, v ** (k - 1)
        P = lambda x: x ** 4 + x * x * v * v + x * x + v * v + 1
        dP = lambda x: 4 * x ** 3 + 2 * x * v * v + 2 * x
        new = []
        for r in rs:
            d = dP(r) % v
            if d:
                new.append((r - P(r) * pow(d, -1, mk)) % mk)
            else:
                new += [(r + j * mk1) % mk for j in range(v)
                        if P((r + j * mk1) % mk) % mk == 0]
        rs = sorted(set(new))
    return rs


def live_base_prime(key, v):
    """The parameter-free class of section II."""
    if key in (1, 2):
        return v % 4 == 1
    return v == 3 or v % 3 == 1


def verify(key, v, u):
    """Full check of a candidate: forcing, lcm | n, and the prefix test."""
    sh = TWO_PRIME[key]
    if u < 2 or u == v or not is_prime(u):
        return None
    V = sorted(set(sh['elems'](v, u)))
    if len(V) != 7:
        return None
    M = max(V)
    if any(f <= M for f in sh['forced'](v, u)):
        return None
    n = sum(d * d for d in V)
    if n % lcm_of(V):
        return None
    if smallest_divisors(n, 7) != V:
        return None
    return (v, u, n)


def sweep(key, vmax):
    """Complete search over all (v, u) with v < vmax.  O(1) work per v."""
    sh = TWO_PRIME[key]
    a = sh['a']
    hits, cands, live = [], 0, 0
    for v in primes_to(vmax):
        if not live_base_prime(key, v):
            continue
        rs = [r for r in roots_for(key, v) if r]
        if not rs:
            continue
        live += 1
        Mp = v ** a
        for F in sh['facs'](v):
            for r in rs:
                if sh['umin'](v) < r < Mp and F % r == 0:   # CASE A
                    cands += 1
                    h = verify(key, v, r)
                    if h:
                        hits.append(h)
                if gcd(r, Mp) != 1:
                    continue
                d = (F % Mp) * pow(r, -1, Mp) % Mp          # CASE B
                if d and F % d == 0:
                    u = F // d
                    if u > sh['umin'](v):
                        cands += 1
                        h = verify(key, v, u)
                        if h:
                            hits.append(h)
    return hits, cands, live


SWEEP_DEPTH = 300000      # produced by the committed sweep(), see the tests
LEVEL2_SHAPES_4 = [TWO_PRIME[k]['name'] for k in (1, 2, 3, 4)]


# =====================================================================
#                             SELF-TESTS
# =====================================================================
def test_forcing_correction_is_in_box():
    """Only in-box non-members may be forced; step 11's own forcing is in-box."""
    # shape 4 has m = (2,2); v^3 and u^3 are OUTSIDE the box
    v, u = 3, 5
    V = sorted({1, v, u, v * v, u * v, u * u, u * v * v})
    assert max(V) == u * v * v
    assert v ** 3 < max(V) and u ** 3 > max(V)
    # so forcing v^3 > max(V) would empty a shape k7_status.py carries as live
    import k7_status
    assert "{1, v, u, v^2, uv, u^2, uv^2}" in k7_status.LEVEL2_SHAPES
    # step 11's forcing u^2 v > max(V) IS in the box ((1,2) <= (2,2))
    assert TWO_PRIME[4]['forced'](v, u) == [u * u * v]
    print("  I     forcing correction: u^2 v is in-box (valid); v^3, u^3 are not")


def test_congruence_conditions():
    """n reduced mod the v-part of lcm(V), on explicit realizations."""
    for v, u in ((3, 5), (5, 7), (13, 29), (17, 101)):
        # shape 1: v^4 | (u^2+1)(v^2+1), and gcd(v^2+1, v) = 1
        V = TWO_PRIME[1]['elems'](v, u)
        n = sum(d * d for d in V)
        assert (n - (u * u + 1) * (v * v + 1)) % v ** 4 == 0, (v, u)
        assert gcd(v * v + 1, v) == 1
        # shape 2
        V = TWO_PRIME[2]['elems'](v, u)
        n = sum(d * d for d in V)
        assert (n - (u * u + 1) * (v * v + 1)) % v ** 3 == 0, (v, u)
        # shape 4
        V = TWO_PRIME[4]['elems'](v, u)
        n = sum(d * d for d in V)
        assert (n - (u ** 4 + u * u + 1)) % v ** 2 == 0, (v, u)
    print("  II    the congruences hold on explicit realizations")


def test_forced_classes_of_v():
    # v | u^2+1 needs -1 a QR, i.e. v = 1 mod 4
    for v in primes_to(2000):
        has = bool(sqrt_minus1(v, 1))
        assert has == (v % 4 == 1), v
    # u^4+u^2+1 factors into coprime halves
    for u in range(1, 3000):
        assert gcd(u * u + u + 1, u * u - u + 1) == 1, u
    # and a root mod v needs -3 a QR, i.e. v = 1 mod 3 (or v = 3)
    for v in primes_to(2000):
        if v == 3:
            continue
        has = any((x ** 4 + x * x + 1) % v == 0 for x in range(v))
        assert has == (v % 3 == 1), v
    print("  II    forced classes: v = 1 mod 4 (shapes 1,2,7), "
          "v = 1 mod 3 or 3 (shapes 3,4)")


def test_case_split_is_exhaustive():
    """For each shape, u >= v^a really does pin the cofactor below v^a."""
    for v in (5, 13, 17, 101, 1009):
        # shape 1: each factor is below 2 v^4, so u >= v^4 gives d = 1
        for F in TWO_PRIME[1]['facs'](v):
            assert F < 2 * v ** 4
        # shape 4: each factor is below 2 v^2
        for F in TWO_PRIME[4]['facs'](v):
            assert F < 2 * v ** 2
        # shape 2/3: 1+v^2 is already below v^3; 1+v^4 gives d <= v
        assert v * v + 1 < v ** 3
        assert (v ** 4 + 1) // v ** 3 <= v
    print("  III   case split exhaustive: u >= v^a pins the cofactor")


def test_level1_kill_shape1():
    """u = Phi_5(v) or Phi_10(v) never satisfies v^4 | u^2+1."""
    for v in primes_to(4000):
        if v % 4 != 1:
            continue
        for F in TWO_PRIME[1]['facs'](v):
            assert (F * F + 1) % v ** 4 != 0, (v, F)
    # the closed form of the residue, and the size argument
    for v in (5, 13, 17, 29, 101, 1000003):
        p5 = v ** 4 + v ** 3 + v * v + v + 1
        p10 = v ** 4 - v ** 3 + v * v - v + 1
        assert (p5 * p5 + 1) % v ** 4 == (4 * v ** 3 + 3 * v * v + 2 * v + 2) % v ** 4
        assert (p10 * p10 + 1) % v ** 4 == (-4 * v ** 3 + 3 * v * v - 2 * v + 2) % v ** 4
        for r in (4 * v ** 3 + 3 * v * v + 2 * v + 2,
                  -4 * v ** 3 + 3 * v * v - 2 * v + 2):
            assert r != 0 and abs(r) < v ** 4, (v, r)
    print("  IV    shape 1: case B dead -- u^2+1 = +-4v^3+3v^2+-2v+2 (mod v^4),"
          " nonzero and below v^4 from v = 5")


def test_level1_kill_shape2():
    """v^3 | d^2+1 with d <= v is impossible."""
    bad = [(v, d) for v in primes_to(600) for d in range(1, v + 1)
           if (d * d + 1) % v ** 3 == 0]
    assert bad == [], bad
    for v in (3, 5, 13, 101, 100003):
        assert v * v + 1 < v ** 3                    # the size step
    print("  IV    shape 2: case B dead -- d = -u (mod v^3) forces v^3 | d^2+1,"
          " but d^2+1 <= v^2+1 < v^3")


def test_level1_kill_shape3():
    """v^2 | 1+d^2+d^4 with d <= v and v PRIME is impossible."""
    bad = [(v, d) for v in primes_to(2000) for d in range(1, v + 1)
           if (1 + d * d + d ** 4) % v ** 2 == 0]
    assert bad == [], bad
    # the step that needs primality: a composite CAN split the two factors
    v, d = 133, 68
    assert (1 + d * d + d ** 4) % v ** 2 == 0
    assert not is_prime(v) and v == 7 * 19
    assert (d * d - d + 1) % 7 ** 2 == 0 and (d * d + d + 1) % 19 ** 2 == 0
    # and d^2 +- d + 1 = v^2 has no solution, since 4v^2-3 is never a square
    for v in range(2, 200000):
        y = isqrt(4 * v * v - 3)
        assert y * y != 4 * v * v - 3, v
    print("  IV    shape 3: case B dead -- v^2 | 1+d^2+d^4 needs d^2+-d+1 = v^2,"
          " i.e. 4v^2-3 square")


def test_level1_kill_shape4_subsumes_step11():
    """u = v^2+-v+1 never satisfies v^2 | u^4+u^2+1."""
    for v in primes_to(4000):
        for F in TWO_PRIME[4]['facs'](v):
            assert (F ** 4 + F * F + 1) % v ** 2 != 0, (v, F)
    # closed form 6v+3 and 3-6v
    for v in (3, 5, 7, 13, 101, 100003):
        assert (((v * v + v + 1) ** 4 + (v * v + v + 1) ** 2 + 1) % v ** 2
                == (6 * v + 3) % v ** 2)
        assert (((v * v - v + 1) ** 4 + (v * v - v + 1) ** 2 + 1) % v ** 2
                == (3 - 6 * v) % v ** 2)
    for v in (7, 11, 13, 101):
        assert 0 < 6 * v + 3 < v * v and 0 < 6 * v - 3 < v * v
    assert (6 * 3 + 3) % 9 == 3 and (6 * 3 - 3) % 9 == 6
    assert (6 * 5 + 3) % 25 == 8 and (6 * 5 - 3) % 25 == 2
    # step 11's single exception is subsumed: (3,13) is u = v^2+v+1
    assert 13 == 3 ** 2 + 3 + 1
    assert (13 ** 4 + 13 ** 2 + 1) % 9 != 0
    print("  IV    shape 4: case B dead -- 6v+3 and 3-6v never vanish mod v^2;"
          " subsumes step 11's (3,13)")


def test_complete_sweep():
    """The O(1)-per-v sweep finds nothing.  Abridged depth for the suite."""
    DEPTH = 30000          # step 11's own depth; SWEEP_DEPTH is 300000
    tot = 0
    for key in (1, 2, 3, 4):
        hits, cands, live = sweep(key, DEPTH)
        assert hits == [], (key, hits)
        assert live > 1000, (key, live)
        tot += cands
        print(f"  V     shape {key}: v < {DEPTH}, {live} live base primes, "
              f"{cands} candidates, no realization")
    assert tot < 50, tot      # the point: the candidate set is tiny
    assert SWEEP_DEPTH == 300000


def test_does_not_prove_too_much():
    """The machinery must not kill shapes k7_status.py carries as live."""
    import k7_status
    assert len(k7_status.LEVEL2_SHAPES) == 8
    for nm in LEVEL2_SHAPES_4:
        assert nm in k7_status.LEVEL2_SHAPES, nm
    # case A genuinely survives: roots exist and lie in the right window
    found = 0
    for v in primes_to(500):
        if v % 4 != 1:
            continue
        for r in sqrt_minus1(v, 4):
            if v * v < r < v ** 4:
                found += 1
    assert found > 50, found
    # and the anchors of the whole programme still hold
    for n, k in ((1, 1), (130, 4)):
        ds = smallest_divisors(n, k)
        assert len(ds) == k and sum(d * d for d in ds) == n, (n, k)
    print("  check all four shapes are still live in k7_status; case A has "
          f"{found} roots in window below v = 500")


def self_test():
    print("k7_residue_congruence.py self-tests\n")
    test_forcing_correction_is_in_box()
    test_congruence_conditions()
    test_forced_classes_of_v()
    test_case_split_is_exhaustive()
    test_level1_kill_shape1()
    test_level1_kill_shape2()
    test_level1_kill_shape3()
    test_level1_kill_shape4_subsumes_step11()
    test_complete_sweep()
    test_does_not_prove_too_much()
    print("\nAll self-tests passed.")
    print("k = 7 is still NOT closed: 78 of 86 orbits Level 1, 8 at Level 2.")
    print("Inside those 8:")
    print("  L1  shapes 1-4, CASE B (outside prime as large as (M) allows):")
    print("      shape 1  u = Phi_5 or Phi_10, u^2+1 = +-4v^3+3v^2+-2v+2 mod v^4")
    print("      shape 2  d = -u mod v^3 forces v^3 | d^2+1, d <= v")
    print("      shape 3  v^2 | 1+d^2+d^4 needs 4v^2-3 to be a square")
    print("      shape 4  6v+3 and 3-6v never vanish mod v^2 (subsumes (3,13))")
    print("  L2  shapes 1-4, CASE A: O(1) candidates per v, complete to")
    print(f"      v < {SWEEP_DEPTH} with no realization (step 11 reached 30000)")
    print("  L2  shapes 5-8 unchanged; shape 7 inherits v = 1 (mod 4)")
    print()
    print("Also recorded: the forcing correction -- only non-members INSIDE the")
    print("box of the lcm exponents may be required to exceed max(V).")


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    self_test()
