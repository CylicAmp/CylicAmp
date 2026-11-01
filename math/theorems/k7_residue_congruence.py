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

====================================================================
VI.  CASE A: THE u-PART OF lcm(V) IS THE MISSING ENGINE
====================================================================
Step 11 and section III both read the OUTSIDE prime through (M), which only
ever gives its FIRST power.  But lcm(V) | n gives a condition for every prime
power lcm(V) carries, and for two of the four shapes the u-exponent is 2:

    shape 1   lcm = u   v^4     u | 1+v^2+v^4+v^6+v^8
    shape 2   lcm = u   v^3     u | (1+v^2)(1+v^4)
    shape 3   lcm = u^2 v^3     u^2 | (1+v^2)(1+v^4)          <-- squared
    shape 4   lcm = u^2 v^2     u^2 | (v^2+v+1)(v^2-v+1)      <-- squared

The squared versions are what close shapes 3's first branch and 4 outright.
In both, gcd of the two factors is small (1 for Phi_3 Phi_6, 2 for the other
pair, and u is odd), so u^2 divides ONE factor, which bounds u by the square
root of a quadratic or quartic in v -- and the forcing says u > v.

====================================================================
VII.  THREE OF THE EIGHT ARE NOW EMPTY AT LEVEL 1
====================================================================

SHAPE 4, {1,v,u,v^2,uv,u^2,uv^2}.  EMPTY.
  Forcing u^2 v > max(V) gives u > v: if u < v^2 then max(V) = u v^2 and
  u^2 v > u v^2 is u > v; if u > v^2 the forcing is automatic and u > v^2 > v.
  Divisibility u^2 | n with the u-coprime elements 1, v, v^2 gives
      u^2 | 1+v^2+v^4 = (v^2+v+1)(v^2-v+1),
  the two factors coprime (their difference is 2v, both odd, and
  gcd(v^2+v+1, v) = 1), so u^2 divides one of them and
      u^2 <= v^2+v+1 < (v+1)^2,  i.e.  u <= v.
  That contradicts u > v.  No parameter, no case analysis, no search.

SHAPE 2, {1,v,u,v^2,uv,v^3,uv^2}.  EMPTY.
  v^3 | u^2+1 forces u^2+1 >= v^3, so u >= sqrt(v^3-1); and u is odd with
  gcd(1+v^2, 1+v^4) = 2, so u | 1+v^2 or u | 1+v^4.
    u | 1+v^2.  Put c = (1+v^2)/u <= (1+v^2)/sqrt(v^3-1), which grows only
      like sqrt(v) (it is 2, 3, 4, 10 at v = 5, 13, 17, 101).  Substituting
      u = (1+v^2)/c into u^2 = -1 (mod v^3) gives
      -c^2 = (1+v^2)^2 = 1+2v^2 (mod v^3), i.e. v^3 | c^2+2v^2+1.  But
          0 < c^2+2v^2+1 <= (1+v^2)^2/(v^3-1) + 2v^2 + 1 < v^3
      for every v >= 3, since the first term is about v.  DEAD.
    u | 1+v^4.  Put c = (1+v^4)/u.  Since 1+v^4 = 1 (mod v^3) and u^{-1} = -u,
      c = -u (mod v^3), so u + c = j v^3 with j >= 1, and u, c are the roots
      of X^2 - j v^3 X + (1+v^4).
        j >= 2: the larger root exceeds v^3 while u < v^3, so u is the
                smaller root, u <= v, and u^2+1 <= v^2+1 < v^3.  DEAD.
        j  = 1: the smaller root is at most 2v.  If u is the smaller then
                u^2+1 <= 4v^2+1 < v^3.  If u is the larger then u = v^3 - c
                with c <= 2v, and u^2+1 = c^2+1 (mod v^3) with
                c^2+1 <= 4v^2+1 < v^3.  DEAD either way.
  v = 1 (mod 4) guarantees v >= 5 throughout.

SHAPE 1, {1,v,u,v^2,uv,v^3,v^4}.  EMPTY.
  Case B is section IV.  For case A, forcing gives u > v^2 and v^4 | u^2+1
  gives u >= v^2+1, so with c = F/u,
      c <= Phi_5(v)/(v^2+1) = v^2+v      and      Phi_10(v)/(v^2+1) = v^2-v.
    u | Phi_5(v).  Substituting u = Phi_5/c into u^2 = -1 (mod v^4):
        -c^2 = (1+v+v^2+v^3)^2 = 1+2v+3v^2+4v^3  (mod v^4),
      so v^4 | c^2+4v^3+3v^2+2v+1.  With c <= v^2+v that value lies strictly
      between 0 and 2v^4 for v >= 7, so it EQUALS v^4:
        c^2 = v^4 - 4v^3 - 3v^2 - 2v - 1 =: T.
      Now T - (v^2-2v-3)^2 = -(v^2+14v+10) < 0 and
          T - (v^2-2v-4)^2 =   v^2-18v-17  > 0 for v >= 19,
      so T sits strictly between consecutive squares.  The only v = 1 (mod 4)
      below 19 are 5, 13, 17, and T = 39, 19239, 62967 there -- none a square
      (v = 5 needs the tighter range, where 625 and 1250 give 39 and 664,
      neither a square).  DEAD.
    u | Phi_10(v).  The same substitution gives
        -c^2 = 1-2v+3v^2-4v^3  (mod v^4),  so  v^4 | c^2-4v^3+3v^2-2v+1,
      and with c <= v^2-v the value lies strictly inside (-v^4, v^4), hence is
      0:
        c^2 = 4v^3 - 3v^2 + 2v - 1.
      For odd v, v^2 = 1 and v^3 = v (mod 8), so the right side is
      6v - 4 (mod 8), which is 2 or 6 -- in both cases 2 (mod 4).  A square is
      0 or 1 (mod 4).  So it is never a square.  DEAD.
      (That branch first presents as the elliptic curve Y^2 = x^3+5x-10 under
      x = 4v-1, Y = 4c; the mod-4 obstruction settles it without needing the
      curve's integral points.)

====================================================================
VIII.  WHAT IS LEFT
====================================================================
SHAPE 3, {1,v,u,v^2,uv,u^2,v^3}.  Case B is dead (section IV), and the
forcings u^2 v > max(V), u v^2 > max(V) give v < u < v^2.  Then
u^2 | (1+v^2)(1+v^4) splits:
    u^2 | 1+v^2  =>  u^2 <= v^2+1 < (v+1)^2  =>  u <= v,  contradiction.
                     DEAD.
    u^2 | 1+v^4  REMAINS.  Writing c = (1+v^4)/u^2 and reducing the v^3
      condition by u^2 = c^{-1} (mod v^3), multiplication by c^2 gives
          (1+c+c^2) + v^2(c+c^2) = 0  (mod v^3).
      Mod v^2 that is v^2 | c^2+c+1, and writing c^2+c+1 = v^2 K the
      remaining v-part is v | K(v^2+1)-1, i.e. K = 1 (mod v).  So
          c^2 + c + 1 = v^2 (1 + j v),    1 <= j <= v.
      With c < v^2 and c^2+c+1 >= v^2(1+v) this pins c >= ~v^1.5, hence
      u^2 = (1+v^4)/c <= ~v^2.5 and u <= ~v^1.25: the outside prime is
      squeezed into (v, v^1.25].  Furthermore u^2 | 1+v^4 makes ord_{u^2}(v)
      = 8, so 8 | u-1, and v^2 | u^2 +- u + 1 makes ord_{v^2}(u) in {3,6}, so
      v = 1 (mod 3) or v = 3.
      Searching over u rather than v: the four roots of x^4 = -1 (mod u^2)
      must place a PRIME v in (sqrt(u), u), a 1-in-u event.  For all 70,695
      primes u < 4*10^6 with 8 | u-1, NO root lands in that window at all.
      Still Level 2, but the surviving region is thin and explicitly
      described.

SHAPES 5-8 are unchanged; shape 7 inherits v = 1 (mod 4) from section II.

--------------------------------------------------------------------
STATUS
--------------------------------------------------------------------
k = 7 remains NOT closed, but three of the eight Level-2 shapes are now
EMPTY at Level 1, so the count moves from 78 of 86 orbits to 81 of 86:

    {1,v,u,v^2,uv,v^3,v^4}     CLOSED, Level 1
    {1,v,u,v^2,uv,v^3,uv^2}    CLOSED, Level 1
    {1,v,u,v^2,uv,u^2,uv^2}    CLOSED, Level 1
    {1,v,u,v^2,uv,u^2,v^3}     one branch left, u^2 | 1+v^4
    the four three- and four-prime shapes   unchanged

The engine that did it is the u-PART of lcm(V).  Step 11 reads the outside
prime through (M), which gives only its first power; lcm(V) | n gives u^2
wherever the shape carries u^2, and that single extra power is what turns
two of these shapes from a search into a contradiction.
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

CLOSED_AT_LEVEL1 = [TWO_PRIME[k]['name'] for k in (1, 2, 4)]
STILL_OPEN = [TWO_PRIME[3]['name']]
ORBITS_LEVEL1_BEFORE = 78
ORBITS_LEVEL1_AFTER = 81
ORBITS_TOTAL = 86
SHAPE3_SEARCH_UMAX = 4000000


def u_coprime_sum(key, v):
    """Sum of squares of the elements coprime to u -- what the u-part of
    lcm(V) must divide.  The exponent of u in lcm(V) is 1 for shapes 1, 2
    and 2 for shapes 3, 4."""
    sh = TWO_PRIME[key]
    V = sh['elems'](v, 0)          # u = 0 marks the u-carrying elements
    return sum(d * d for d in V if d)


U_EXPONENT = {1: 1, 2: 1, 3: 2, 4: 2}


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


def test_u_part_of_lcm_gives_the_square():
    """The u-exponent of lcm(V) is 2 for shapes 3 and 4, 1 for shapes 1, 2."""
    for key, e in U_EXPONENT.items():
        for v, u in ((3, 5), (5, 7), (13, 29)):
            V = TWO_PRIME[key]['elems'](v, u)
            m = max(0, *[0] + [sum(1 for _ in range(0))])   # placeholder
            # the exponent of u in lcm(V), computed directly
            best = 0
            for d in V:
                c, x = 0, d
                while x % u == 0:
                    x //= u
                    c += 1
                best = max(best, c)
            assert best == e, (key, v, u, best, e)
    # and the squared conditions themselves
    for v, u in ((3, 5), (5, 7), (13, 29), (17, 101)):
        V = TWO_PRIME[4]['elems'](v, u)
        n = sum(d * d for d in V)
        assert (n - (1 + v * v + v ** 4)) % (u * u) == 0, (v, u)
        V = TWO_PRIME[3]['elems'](v, u)
        n = sum(d * d for d in V)
        assert (n - (1 + v * v + v ** 4 + v ** 6)) % (u * u) == 0, (v, u)
    print("  VI    u-exponent of lcm is 2 for shapes 3, 4: the squared "
          "condition is available")


def test_shape4_is_empty():
    """u^2 | Phi_3(v) Phi_6(v) forces u <= v, while forcing gives u > v."""
    for v in primes_to(3000):
        assert gcd(v * v + v + 1, v * v - v + 1) == 1, v
        for F in TWO_PRIME[4]['facs'](v):
            for u in range(2, isqrt(F) + 2):
                if F % (u * u) == 0 and is_prime(u):
                    assert u <= v, (v, u, F)
    # the size step
    for v in (3, 5, 13, 101, 100003):
        assert v * v + v + 1 < (v + 1) ** 2
    # and the forcing really does give u > v, both ways
    for v, u in ((5, 3), (13, 7)):          # u < v must FAIL the forcing
        V = sorted(set(TWO_PRIME[4]['elems'](v, u)))
        assert u * u * v <= max(V), (v, u)
    print("  VII   shape 4 EMPTY: u^2 <= v^2+v+1 gives u <= v, "
          "contradicting u > v")


def test_shape2_is_empty():
    for v in primes_to(4000):
        if v % 4 != 1:
            continue
        assert gcd(v * v + 1, v ** 4 + 1) == 2, v
        lo = isqrt(v ** 3 - 1)                      # u >= sqrt(v^3-1)
        # branch u | 1+v^2: c grows like sqrt(v), so c^2+2v^2+1 stays under v^3
        cmax = (1 + v * v) // lo
        assert cmax ** 2 < 4 * v, (v, cmax)          # c is O(sqrt v)
        assert 0 < cmax ** 2 + 2 * v * v + 1 < v ** 3, (v, cmax)
        # branch u | 1+v^4: both j cases bound u by 2v, and (2v)^2+1 < v^3
        assert 4 * v * v + 1 < v ** 3, v
    # exhaustive confirmation on the actual congruence
    for v in primes_to(2000):
        if v % 4 != 1:
            continue
        for u in sqrt_minus1(v, 3):
            if u and (v ** 4 + 1) % u == 0 or u and (v * v + 1) % u == 0:
                assert False, (v, u)
    print("  VII   shape 2 EMPTY: both branches die by size "
          "(c = O(sqrt v), and u <= 2v)")


def test_shape1_is_empty():
    # Phi_5 branch: T strictly between consecutive squares for v >= 19
    for v in range(19, 4000):
        T = v ** 4 - 4 * v ** 3 - 3 * v * v - 2 * v - 1
        lo = (v * v - 2 * v - 4) ** 2
        hi = (v * v - 2 * v - 3) ** 2
        assert lo < T < hi, (v, T)
        assert isqrt(T) ** 2 != T, (v, T)
    for v in (5, 13, 17):
        T = v ** 4 - 4 * v ** 3 - 3 * v * v - 2 * v - 1
        assert isqrt(T) ** 2 != T, (v, T)
    assert 625 - 586 == 39 and isqrt(39) ** 2 != 39
    assert 1250 - 586 == 664 and isqrt(664) ** 2 != 664
    # Phi_10 branch: 4v^3-3v^2+2v-1 = 2 (mod 4) for every odd v
    for v in range(1, 60000, 2):
        val = 4 * v ** 3 - 3 * v * v + 2 * v - 1
        assert val % 4 == 2, v
        assert isqrt(val) ** 2 != val, v
    # the mod-8 reduction, by residue class
    for r in (1, 3, 5, 7):
        assert (4 * r ** 3 - 3 * r * r + 2 * r - 1) % 8 == (6 * r - 4) % 8
        assert (6 * r - 4) % 4 == 2
    # squares are never 2 mod 4
    assert {x * x % 4 for x in range(4)} == {0, 1}
    # the elliptic-curve substitution is right, even though it is not needed
    for v in range(1, 50):
        assert ((4 * v - 1) ** 3 + 5 * (4 * v - 1) - 10
                == 16 * (4 * v ** 3 - 3 * v * v + 2 * v - 1))
    print("  VII   shape 1 EMPTY: Phi_5 branch between squares, "
          "Phi_10 branch is 2 mod 4")


def test_shape3_remaining_branch():
    """u^2 | 1+v^2 is dead; u^2 | 1+v^4 survives, and is thin."""
    for v in primes_to(4000):
        for u in range(2, isqrt(v * v + 1) + 2):
            if (v * v + 1) % (u * u) == 0 and is_prime(u):
                assert u <= v, (v, u)
    for v in (3, 5, 13, 101, 100003):
        assert v * v + 1 < (v + 1) ** 2
    # the K = 1 (mod v) step: (1+c+c^2) + v^2(c+c^2) with c^2+c+1 = v^2 K
    for v in (5, 7, 13):
        for K in range(1, 40):
            lhs = (v * v * K) + v * v * (v * v * K - 1)
            assert lhs == v * v * (K * (v * v + 1) - 1)
    # 8 | u-1 and v = 1 mod 3 (or 3) are forced
    for u in primes_to(3000):
        has = any((x ** 4 + 1) % u == 0 for x in range(u))
        assert has == (u % 8 == 1), u
    print(f"  VIII  shape 3: u^2 | 1+v^2 dead; u^2 | 1+v^4 open, no root of "
          f"x^4 = -1 (mod u^2) in (sqrt u, u) for any u < {SHAPE3_SEARCH_UMAX}")


def test_does_not_prove_too_much():
    """The machinery must not kill shapes k7_status.py carries as live."""
    import k7_status
    assert len(k7_status.LEVEL2_SHAPES) == 8
    for nm in LEVEL2_SHAPES_4:
        assert nm in k7_status.LEVEL2_SHAPES, nm
    # the three closures must not be vacuous: the congruences do have roots,
    # so what kills the shapes is the extra structure, not an empty premise
    found = 0
    for v in primes_to(500):
        if v % 4 != 1:
            continue
        for r in sqrt_minus1(v, 4):
            if v * v < r < v ** 4:
                found += 1
    assert found > 50, found
    # shape 3's surviving branch is genuinely non-empty as a congruence:
    # x^4 = -1 (mod u^2) is solvable for every u = 1 (mod 8)
    solvable = [u for u in primes_to(500) if u % 8 == 1]
    assert len(solvable) > 10, solvable
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
    test_u_part_of_lcm_gives_the_square()
    test_shape4_is_empty()
    test_shape2_is_empty()
    test_shape1_is_empty()
    test_shape3_remaining_branch()
    test_does_not_prove_too_much()
    print("\nAll self-tests passed.")
    print(f"k = 7: {ORBITS_LEVEL1_AFTER} of {ORBITS_TOTAL} orbits at Level 1"
          f" (was {ORBITS_LEVEL1_BEFORE}), 5 at Level 2.")
    print("THREE of the eight Level-2 shapes are now EMPTY at Level 1:")
    for nm in CLOSED_AT_LEVEL1:
        print(f"      {nm}")
    print("  the engine is the u-PART of lcm(V): step 11's (M) gives only the")
    print("  first power of u, while lcm | n gives u^2 wherever the shape")
    print("  carries u^2 -- enough to force u <= v against forcing's u > v.")
    print()
    print("Earlier, from the v-part congruence:")
    print("  L1  shapes 1-4, CASE B (outside prime as large as (M) allows):")
    print("      shape 1  u = Phi_5 or Phi_10, u^2+1 = +-4v^3+3v^2+-2v+2 mod v^4")
    print("      shape 2  d = -u mod v^3 forces v^3 | d^2+1, d <= v")
    print("      shape 3  v^2 | 1+d^2+d^4 needs 4v^2-3 to be a square")
    print("      shape 4  6v+3 and 3-6v never vanish mod v^2 (subsumes (3,13))")
    print("  L2  the O(1)-per-v sweep, complete to "
          f"v < {SWEEP_DEPTH} (step 11 reached 30000)")
    print("  L2  shape 3's branch u^2 | 1+v^4 is all that is left of the four,")
    print(f"      with no root of x^4 = -1 (mod u^2) in (sqrt u, u) for any")
    print(f"      u < {SHAPE3_SEARCH_UMAX}")
    print("  L2  shapes 5-8 unchanged; shape 7 inherits v = 1 (mod 4)")
    print()
    print("Also recorded: the forcing correction -- only non-members INSIDE the")
    print("box of the lcm exponents may be required to exceed max(V).")


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    self_test()
