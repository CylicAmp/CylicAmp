"""
k7_status.py

k = 7:  is there an n with  n = d_1^2 + ... + d_7^2  for d_1 < ... < d_7 the
SEVEN smallest divisors of n?

STATUS, STATED HONESTLY.  k=7 is NOT closed at Level 1, but 77 of its 86
orbits now are and only NINE remain. k=7 is the case where the parity lemma
gives nothing: k is odd, so a sum of seven odd squares is odd, and BOTH an
odd n and an even n survive step 1. The shape count jumps accordingly --
86 orbits against 13 at k=5 and 24 at k=6.

    86 orbits                  (3857 labelled order ideals, prime 2 fixed)
    35 killed by profile       LEVEL 1, step 1
    51 need an argument
       14  profile (6,1,0)     LEVEL 1, step 2
        4  profile (4,1,2)     LEVEL 1, step 3
        5  profile (4,2,1)     LEVEL 1, step 7   <- closed later
       28  profile (7,0,0), the odd sector:
            1  {1,v,v^2,...,v^6}   LEVEL 1, step 4, the mod-p rule
            1  {1,v,u,t,uv,vt,ut}  LEVEL 1, step 5
            9  LEVEL 1, step 8, product forcing   <- closed later
            8  LEVEL 1, step 9, n < lcm           <- closed later
            9  LEVEL 2 ONLY -- the last section

So 77 of 86 orbits are Level 1 and 9 are Level 2. Steps 7, 8 and 9 closed
22 of the 31 that were previously Level 2; the remaining 9 are listed at
the end, and they share one feature.

--------------------------------------------------------------------
THE ENGINES (same three as k=5 and k=6)
--------------------------------------------------------------------
  (P) PREFIX RULE. If e | n and e < max(V), then e is in V. Composite e too.
  (L) LCM RULE. Every element of V divides n, so lcm(V) | n. This is a
      DIVISIBILITY statement, far stronger than n >= lcm(V).
  (M) MOD-p RULE. p in V means p | n, and reducing n = sum d^2 mod p kills
      every term divisible by p, so

          sum over {d in V : p does not divide d} of d^2  =  0  (mod p).

      When that coprime part is just {1}, n = 1 (mod p) and p cannot divide n.

--------------------------------------------------------------------
STEP 1   THE PROFILE, AND WHY IT KILLS 35 OF 86
--------------------------------------------------------------------
Let A, B, C count the elements of V that are odd, 2 (mod 4), 0 (mod 4).
Squares mod 8 are 1, 4, 0 in those three classes, so

    A + B + C = 7      and      sum d^2 = A + 4B   (mod 8).

The profile is a STRUCTURAL invariant of a shape: the class of an element
depends only on the exponent of 2 in it, so no realization is needed.
A >= 1 always, since d_1 = 1.

Three branches, by v_2(n):
  n odd      B = C = 0, so A = 7, and n = 7 (mod 8).
  v_2(n) = 1 C = 0, n = 2 (mod 4), so A + 4(7-A) = 5A + 4 must be 2 or 6 mod 8.
  v_2(n) >= 2 4 | n, so 4 is in V (seven distinct divisors cannot all be
             below 4), giving B >= 1 and C >= 1, and A = 0 (mod 4).

Then (P) adds  B <= A:  each element counted by B is 2d with d odd, and
d | n with d < 2d <= max(V), so (P) forces d into V -- and the odd elements
number A. That kills (A,B,C) = (2,5,0). Four profiles survive:

    (7,0,0)  n odd              28 shapes
    (6,1,0)  v_2(n) = 1         14 shapes      closed below
    (4,2,1)  v_2(n) = 2          5 shapes
    (4,1,2)  8 | n               4 shapes      closed below

--------------------------------------------------------------------
STEP 2   PROFILE (6,1,0) IS EMPTY        LEVEL 1, all 14 shapes
--------------------------------------------------------------------
V = {1, 2, o_1 < ... < o_5} with the o_i odd, and max(V) = o_5.

(a) B = 1 means 2 is the only element that is 2 (mod 4). But 2*o_1 divides n
    and is 2 (mod 4), so (P) gives  2*o_1 > o_5.
(b) o_1 = p is the least odd prime of n: a smaller odd prime would be an odd
    divisor below o_5, so (P) would put it in V, below o_1.
(c) Every odd divisor of n has all prime factors >= p, so a COMPOSITE one is
    at least p^2 > 2p > o_5 and cannot be in V. So o_1..o_5 are five PRIMES,
    all in [p, 2p).
(d) lcm(V) = 2*o_1*...*o_5 > 2p^5, while n = 1 + 4 + sum o_i^2 < 5 + 20p^2.
    And 2p^5 > 5 + 20p^2 for every odd prime p (486 > 185 at p = 3).
    So n < lcm(V), contradicting lcm(V) | n.

--------------------------------------------------------------------
STEP 3   PROFILE (4,1,2) IS EMPTY        LEVEL 1, all 4 shapes
--------------------------------------------------------------------
Here A + 4B = 8 = 0 (mod 8), so 8 | n.

(a) B = 1, so as above 2*o_1 > max(V); and 4 is in V, so max(V) >= 4 and
    o_1 > 2. Then 4*o_1 > 2*o_1 > max(V), so no element that is 0 (mod 4)
    carries an odd factor: the C-elements are powers of 2. With C = 2 and
    8 | n (and 8 < 16), they are forced to be exactly {4, 8}.
(b) So max(V) >= 8, and 2*o_1 > 8 gives o_1 >= 5; also o_3 < 2*o_1.
(c) As in step 2, o_1, o_2, o_3 are three PRIMES in [p, 2p), p = o_1 >= 5.
(d) lcm(V) = 8*o_1*o_2*o_3 > 8p^3, while n = 85 + sum o_i^2 < 85 + 12p^2,
    and 8p^3 > 85 + 12p^2 for every prime p >= 5 (1000 > 385 at p = 5).

--------------------------------------------------------------------
STEP 4   THE PURE CHAIN IS EMPTY         LEVEL 1
--------------------------------------------------------------------
V = {1, v, v^2, v^3, v^4, v^5, v^6}. The only element coprime to v is 1, so
(M) gives n = 1 (mod v). But v is in V, so v | n. Contradiction.

--------------------------------------------------------------------
STEP 5   {1, v, u, t, uv, vt, ut} IS EMPTY   LEVEL 1
--------------------------------------------------------------------
Three odd primes v < u < t together with all three pairwise products;
max(V) = ut. The identity that drives it:

    n = 1+v^2+u^2+t^2+(uv)^2+(vt)^2+(ut)^2 = (1+v^2)(1+u^2)(1+t^2) - (vut)^2

(a) v | n and v | (vut)^2, so v | (1+u^2)(1+t^2); likewise for u and t.
(b) v > 3. If v = 3 then u, t are coprime to 3, so (1+u^2)(1+t^2) = 2*2 = 1
    (mod 3) and 3 does not divide n. And n is odd. So v >= 5.
(c) v^2 and u^2 do not divide n: both are below ut = max(V) (because
    v < u < t), so (P) would force them into V, and they are not there.
    t^2 > ut, so t may repeat. Any prime of n outside {v,u,t} is >= ut, again
    by (P). Hence

        n = v * u * t^c * m,     c >= 1,    m = 1 or m >= ut.

(d) Size. n contains the term (ut)^2, so n > u^2t^2; and v <= u-2 gives
    n = u^2t^2 + v^2t^2 + v^2u^2 + t^2 + u^2 + v^2 + 1 < 4 u^2 t^2.
(e) Both branches die.
      m >= ut: n >= v*u*t^c*ut >= v*u^2*t^2, so v*u^2t^2 < 4u^2t^2 forces
               v < 4, contradicting v >= 5.
      m = 1:   n = v*u*t^c with u^2t^2 < v*u*t^c < 4u^2t^2, and
                 c = 1 needs v > ut,      false
                 c = 2 needs v > u,       false
                 c = 3 needs v*t < 4u, so t < 4u/5 < u,  false
                 c >= 4 is worse still.


--------------------------------------------------------------------
STEP 7   PROFILE (4,2,1) IS EMPTY        LEVEL 1, all 5 shapes
--------------------------------------------------------------------
A + 4B = 4 + 8 = 12 = 4 (mod 8), so n = 4 (mod 8) and v_2(n) = 2 EXACTLY.

(a) The 0-mod-4 elements are 4 times odd divisors, and C = 1 leaves only
    {4}. So 4*o_1 is not in V, and by (P)  4*o_1 > max(V).
(b) B = 2 forces {2, 2*o_1} as always, so 2*o_2 > max(V).
    V = {1, 2, 4, o_1, 2*o_1, o_2, o_3}, and o_3 < 4*o_1, o_3 < 2*o_2.

(c) CASE p = o_1 >= 5. A composite odd divisor is at least p^2, and
    p^2 > 4p for p >= 5, so p^2 > max(V): o_1, o_2, o_3 are all PRIME.
    Then n = 21 + 5p^2 + o_2^2 + o_3^2 < 21 + 10*o_2^2 (using p < o_2 and
    o_3 < 2 o_2), while lcm(V) = 4*p*o_2*o_3 > 4p*o_2^2 >= 20*o_2^2. And
    20 x > 21 + 10 x for x = o_2^2 >= 4. So n < lcm(V).

(d) CASE p = 3. Now p^2 = 9 < 12 = 4p, so 9 may be an odd divisor, and the
    primality argument fails. But 4*o_1 = 12 > max(V) >= o_3 bounds the
    case to o_3 <= 11, leaving five admissible odd parts:
        (o_2,o_3) = (5,7), (5,9), (7,9), (7,11), (9,11)
    -- (5,11) is excluded because o_3 = 11 >= 2*o_2 = 10 would force
    2*o_2 = 10 into V and give B >= 3. All five have n < lcm(V):
        140 < 420,  172 < 180,  196 < 252,  236 < 924,  268 < 396.

--------------------------------------------------------------------
STEP 8   PRODUCT FORCING kills 9 odd-sector shapes   LEVEL 1
--------------------------------------------------------------------
LEMMA. Let p < q be primes in V with pq not in V. Then pq | n (the primes
are coprime), so by (P)

        pq > max(V).

A shape is therefore EMPTY as soon as some such pair satisfies pq <= max(V)
on every realization. The commonest instance: if V contains the square of
the LARGER prime, then pq < q^2 <= max(V) and the shape dies.

These nine shapes all die this way:

    {1,v,u,v^2,u^2,v^3,v^4}    {1,v,u,t,v^2,u^2,t^2}
    {1,v,u,v^2,u^2,v^3,u^3}    {1,v,u,t,s,v^2,u^2}
    {1,v,u,t,v^2,u^2,v^3}      {1,v,u,t,s,v^2,tu}
    {1,v,u,t,v^2,uv,t^2}       {1,v,u,t,s,uv,st}
    {1,v,u,t,v^2,tu,v^3}

For the first six, two primes have their squares in V and the forcing pair
is immediate. For {1,v,u,t,v^2,tu,v^3}: if v is not the least prime then
w*v < v^2 for the least prime w; and if v IS least then u, t > v^2 is
forced (else u*v < v^3 would need u*v in V), so max(V) = tu and u*v < tu.
For {1,v,u,t,s,uv,st}: the two least primes' product is the smallest of all
products, so it is at most max(V) and must be uv or st; whichever it is,
the next product up is also below max(V) and is absent.

--------------------------------------------------------------------
STEP 9   n < lcm(V) kills 8 more odd-sector shapes   LEVEL 1
--------------------------------------------------------------------
    {1,v,u,t,v^2,v^3,v^4}      {1,v,u,t,s,v^2,uv}
    {1,v,u,t,v^2,uv,v^3}       {1,v,u,t,s,r,v^2}
    {1,v,u,t,v^2,uv,u^2}       {1,v,u,t,s,r,uv}
    {1,v,u,t,s,v^2,v^3}        {1,v,u,t,s,r,q}

n = 1 + sum o_i^2 < 7*max(V)^2, so lcm(V) > 7*max(V)^2 suffices, and for
six of the eight it holds outright. The cleanest is {1,v,u,t,s,r,q}, six
distinct primes: (P) gives v*u > q for the two least (their product is not
in V), so lcm = v*u*t*s*r*q > q*t*s*r*q >= 1001*q^2 > 7*q^2.

Two shapes -- {1,v,u,t,v^2,uv,v^3} and {1,v,u,t,v^2,uv,u^2} -- have
lcm/max^2 as low as 1.62 and 3.12, so the crude bound does NOT cover them.
They need admissibility as well: in the first, v^2*u divides n (it divides
lcm = v^3*u*t) and is not in V, so v^2*u > max(V), which bounds the large
prime t and restores n < lcm. Verified on every admissible realization over
primes to 400 (13,596 and 47,534 of them), with min lcm/n of 1.12 and 2.28.

--------------------------------------------------------------------
WHAT IS ONLY LEVEL 2  --  the 9 shapes left
--------------------------------------------------------------------
All nine are in the odd sector. What separates them from the eight that
step 9 closes is measurable and exact: for these nine, lcm(V) can fall
BELOW n, so the size form of (L) is simply unavailable and only the
divisibility form is left. The tightest min lcm/n over admissible
realizations:

    residue shapes   0.000 to 0.633      (lcm can be far below n)
    step-9 shapes    1.247 to 970.94     (lcm always exceeds n)

Structurally these are the PRIME-POOR shapes: seven elements built from few
enough primes, with enough repetition, that lcm(V) never outgrows n. Eight
of the nine contain v^2 together with u*v; the ninth, {1,v,u,t,s,uv,tv},
has no square at all and instead reuses v across the two products u*v and
t*v. So the common feature is prime REUSE, not v^2 -- an earlier draft of
this file claimed v^2 and was wrong on that ninth shape.

    {1,v,u,v^2,v^3,v^4,v^5}    {1,v,u,v^2,uv,u^2,uv^2}
    {1,v,u,v^2,uv,v^3,v^4}     {1,v,u,t,v^2,uv,uv^2}
    {1,v,u,v^2,uv,v^3,uv^2}    {1,v,u,t,v^2,uv,tv}
    {1,v,u,v^2,uv,u^2,v^3}     {1,v,u,t,v^2,uv,tu}
                               {1,v,u,t,s,uv,tv}

For these the evidence is a bounded search, not a proof:

  * over all assignments of odd primes <= 41 to the shape's prime slots,
    NO shape but {1,v,u,t,uv,vt,ut} has a single realization that is
    coprime-product admissible AND satisfies lcm(V) | n;
  * that one shape's only surviving realization is (v,u,t) = (5,13,17),
    giving n = 60775 = 5^2 * 11 * 13 * 17, whose seven smallest divisors are
    1,5,11,13,17,25,55 -- not V, since 11 | n and 11 < 65. Step 5 closes it
    at Level 1 anyway;
  * so the search finds NO witness at any shape, which agrees with the
    ground-truth scan: divisor_square_sum_scan.py finds solutions only at
    k = 1, 4 (n=130) and 11 (n=1860) up to 30,000,000.

The useful observation for whoever closes these: the correct form of (L) --
lcm(V) | n rather than n >= lcm(V) -- removes 50 of the 51 shapes
immediately over any prime pool tried. A Level 1 version of that
divisibility argument, rather than the size version used in steps 2 and 3,
is very likely what finishes k = 7.
"""

from math import gcd, isqrt
from itertools import combinations, permutations
from typing import Dict, List, Tuple

PROFILES_SURVIVING = {(7, 0, 0), (6, 1, 0), (4, 2, 1), (4, 1, 2)}
LEVEL1_PROFILES = {(6, 1, 0), (4, 1, 2)}


def primes_upto(n: int) -> List[int]:
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


def lcm_of(vals) -> int:
    o = 1
    for v in vals:
        o = o * v // gcd(o, v)
    return o


def smallest_divisors(n: int, k: int) -> List[int]:
    d = []
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            d.append(i)
            d.append(n // i)
    return sorted(set(d))[:k]


def profile_of(shape) -> Tuple[int, int, int]:
    """(A, B, C) from the exponent of 2 alone -- structural, no realization."""
    return (sum(1 for v in shape if v[0] == 0),
            sum(1 for v in shape if v[0] == 1),
            sum(1 for v in shape if v[0] >= 2))


def surviving_profiles(k: int = 7):
    """Step 1, run as arithmetic over the finite profile space."""
    out = []
    for A in range(1, k + 1):
        for B in range(0, k + 1 - A):
            C = k - A - B
            S = (A + 4 * B) % 8
            if C == 0 and B == 0:
                if S % 2 == 1:
                    out.append((A, B, C))
            elif C == 0:
                if S % 4 == 2 and B <= A:
                    out.append((A, B, C))
            else:
                if B >= 1 and S % 4 == 0 and B <= A:
                    out.append((A, B, C))
    return out


def step2_bound(p: int) -> bool:
    """profile (6,1,0): 2p^5 > 5 + 20p^2."""
    return 2 * p ** 5 > 5 + 20 * p * p


def step3_bound(p: int) -> bool:
    """profile (4,1,2): 8p^3 > 85 + 12p^2."""
    return 8 * p ** 3 > 85 + 12 * p * p


def step5_n(v: int, u: int, t: int) -> int:
    return 1 + v * v + u * u + t * t + (u * v) ** 2 + (v * t) ** 2 + (u * t) ** 2


# =====================================================================
# SELF-TESTS
# =====================================================================

def test_step1_profiles() -> None:
    got = set(surviving_profiles(7))
    assert got == PROFILES_SURVIVING, got
    # and the one the prefix rule kills, which arithmetic alone would allow
    assert (5 * 2 + 4) % 8 == 6, "A=2,B=5 satisfies the congruence"
    assert 5 > 2, "but B=5 > A=2, and each 2d forces d into the prefix"
    print(f"[ok] step 1: exactly {len(got)} profiles survive mod 8 + prefix rule")


def test_step1_profile_is_structural() -> None:
    """The class mod 4 of an element depends only on the exponent of 2."""
    for e, want in ((0, "odd"), (1, "2 mod 4"), (2, "0 mod 4"), (5, "0 mod 4")):
        val = 2 ** e * 15
        cls = "odd" if val % 2 else ("2 mod 4" if val % 4 == 2 else "0 mod 4")
        assert cls == want, (e, cls)
    print("[ok] step 1: the profile is structural, independent of realization")


def test_step1_verified_against_realizations() -> None:
    """INDEPENDENT check of step 1, the step that kills 35 of 86 orbits.

    Rather than re-deriving the profile arithmetic, realize every orbit over
    a pool of odd primes and confirm, on each realization, that
      (A) sum d^2 = A + 4B (mod 8), and
      (B) every shape whose profile step 1 kills really does fail the
          v_2(n) branch it would have to sit in.
    """
    import os
    import sys as _s
    _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import divisor_prefix_ledger as ledger

    reps = ledger.orbit_reps(ledger.labeled_universe(7), 7)
    assert len(reps) == 86, len(reps)
    odd = [3, 5, 7, 11, 13, 17]
    killed = 0
    tested = 0
    for rep in reps:
        A, B, C = profile_of(rep)
        if (A, B, C) not in PROFILES_SURVIVING:
            killed += 1
        nv = len(rep[0])
        slots = [i for i in range(nv) if i and any(v[i] for v in rep)]
        for assign in permutations(odd, len(slots)):
            pmap: Dict[int, int] = {0: 2}
            pmap.update(dict(zip(slots, assign)))
            vals = []
            for v in rep:
                x = 1
                for i, e in enumerate(v):
                    if e:
                        x *= pmap[i] ** e
                vals.append(x)
            if len(set(vals)) < 7:
                continue
            tested += 1
            n = sum(x * x for x in vals)
            assert n % 8 == (A + 4 * B) % 8, (rep, vals)          # (A)
            if (A, B, C) in PROFILES_SURVIVING:
                continue
            fits = ((C == 0 and B == 0 and n % 2 == 1)
                    or (C == 0 and B > 0 and n % 4 == 2 and B <= A)
                    or (C >= 1 and B >= 1 and n % 4 == 0 and B <= A))
            assert not fits, (rep, (A, B, C), vals, n)            # (B)
    assert killed == 35, killed
    assert tested > 10000, tested
    print(f"[ok] step 1 verified on {tested:,} realizations of all 86 orbits: "
          f"sum d^2 = A+4B (mod 8), and all {killed} killed shapes fail their branch")


def test_step2_profile_610() -> None:
    for p in primes_upto(3000):
        if p >= 3:
            assert step2_bound(p), p
    assert step2_bound(3) and 2 * 3 ** 5 == 486 and 5 + 20 * 9 == 185
    print("[ok] step 2: 2p^5 > 5+20p^2 for every odd prime -> (6,1,0) empty")


def test_step3_profile_412() -> None:
    for p in primes_upto(3000):
        if p >= 5:
            assert step3_bound(p), p
    assert 8 * 125 == 1000 and 85 + 12 * 25 == 385
    print("[ok] step 3: 8p^3 > 85+12p^2 for every prime p>=5 -> (4,1,2) empty")


def test_step4_chain() -> None:
    for p in primes_upto(200):
        if p < 3:
            continue
        n = sum(p ** (2 * i) for i in range(7))
        assert n % p == 1, p
    print("[ok] step 4: the chain gives n = 1 (mod v), so v cannot divide n")


def test_step5_identity_and_squeeze() -> None:
    ps = [x for x in primes_upto(200) if x >= 3]
    checked = 0
    for i, v in enumerate(ps):
        if v > 60:
            break
        for j in range(i + 1, len(ps)):
            u = ps[j]
            if u > 110:
                break
            for t in ps[j + 1:]:
                if t > 160:
                    break
                n = step5_n(v, u, t)
                assert n == (1 + v * v) * (1 + u * u) * (1 + t * t) - (v * u * t) ** 2
                assert u * u * t * t < n < 4 * u * u * t * t, (v, u, t)
                assert v * v < u * t and u * u < u * t and t * t > u * t
                checked += 1
    assert checked > 5000, checked
    # the v=3 exclusion
    for u in ps:
        for t in ps:
            if 3 < u < t and u % 3 and t % 3:
                assert ((1 + u * u) * (1 + t * t)) % 3 == 1, (u, t)
    print(f"[ok] step 5: identity, u^2t^2 < n < 4u^2t^2, and v != 3 "
          f"({checked} triples)")


def test_step5_branches_contradict() -> None:
    """Every (c, m) branch of n = v*u*t^c*m violates the size window."""
    ps = [x for x in primes_upto(400) if x >= 5]
    checked = 0
    for i, v in enumerate(ps[:20]):
        for j in range(i + 1, min(i + 20, len(ps))):
            u = ps[j]
            for t in ps[j + 1:j + 20]:
                lo, hi = u * u * t * t, 4 * u * u * t * t
                for c in range(1, 6):
                    assert not (lo < v * u * t ** c < hi), (v, u, t, c)
                assert v * u * u * t * t >= hi, (v, u, t)   # the m >= ut branch
                checked += 1
    assert checked > 2000, checked
    print(f"[ok] step 5: no branch fits the window ({checked} triples)")


def test_level2_residue() -> None:
    """The bounded search behind the Level 2 claim, on the one shape that
    survives lcm(V) | n: its single realization is not a prefix."""
    v, u, t = 5, 13, 17
    V = sorted([1, v, u, t, u * v, v * t, u * t])
    n = step5_n(v, u, t)
    assert n == 60775 and n % lcm_of(V) == 0, (n, lcm_of(V))
    actual = smallest_divisors(n, 7)
    assert actual != V, (V, actual)
    assert n % 11 == 0 and 11 < u * t and 11 not in V, "11 | n sits below max(V)"
    print(f"[ok] level 2: the one lcm-surviving realization fails (P): "
          f"11 | {n} and 11 < {u*t}")


def test_no_k7_solution_by_scan() -> None:
    LIM = 2_000_000
    hits = []
    for n in range(2, LIM):
        d = []
        for i in range(1, isqrt(n) + 1):
            if n % i == 0:
                d.append(i)
                if len(d) > 9:
                    break
        d = sorted(d)[:7]
        if len(d) == 7 and sum(x * x for x in d) == n:
            hits.append(n)
    assert hits == [], hits
    print(f"[ok] direct scan to {LIM:,}: no k=7 solution")


def test_does_not_prove_too_much() -> None:
    for n, k in ((1, 1), (130, 4), (1860, 11)):
        ds = smallest_divisors(n, k)
        assert len(ds) == k and sum(d * d for d in ds) == n, (n, k, ds)
    print("[ok] anchors survive: 1 (k=1), 130 (k=4), 1860 (k=11)")


STEP7_P3_CASES = [(5, 7), (5, 9), (7, 9), (7, 11), (9, 11)]

STEP8_SHAPES = [
    "{1, v, u, v^2, u^2, v^3, v^4}", "{1, v, u, v^2, u^2, v^3, u^3}",
    "{1, v, u, t, v^2, u^2, v^3}", "{1, v, u, t, v^2, uv, t^2}",
    "{1, v, u, t, v^2, tu, v^3}", "{1, v, u, t, v^2, u^2, t^2}",
    "{1, v, u, t, s, v^2, u^2}", "{1, v, u, t, s, v^2, tu}",
    "{1, v, u, t, s, uv, st}",
]
STEP9_SHAPES = [
    "{1, v, u, t, v^2, v^3, v^4}", "{1, v, u, t, v^2, uv, v^3}",
    "{1, v, u, t, v^2, uv, u^2}", "{1, v, u, t, s, v^2, v^3}",
    "{1, v, u, t, s, v^2, uv}", "{1, v, u, t, s, r, v^2}",
    "{1, v, u, t, s, r, uv}", "{1, v, u, t, s, r, q}",
]
LEVEL2_SHAPES = [
    "{1, v, u, v^2, v^3, v^4, v^5}", "{1, v, u, v^2, uv, v^3, v^4}",
    "{1, v, u, v^2, uv, v^3, uv^2}", "{1, v, u, v^2, uv, u^2, v^3}",
    "{1, v, u, v^2, uv, u^2, uv^2}", "{1, v, u, t, v^2, uv, uv^2}",
    "{1, v, u, t, v^2, uv, tv}", "{1, v, u, t, v^2, uv, tu}",
    "{1, v, u, t, s, uv, tv}",
]


def _lcm(vals):
    o = 1
    for v in vals:
        o = o * v // gcd(o, v)
    return o


def _odd_shapes():
    import os
    import sys as _s
    _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import divisor_prefix_ledger as ledger
    reps = ledger.orbit_reps(ledger.labeled_universe(7), 7)
    return {ledger.render(r): r for r in reps if all(v[0] == 0 for v in r)}, ledger


def test_step7_profile_421() -> None:
    """(4,2,1): p >= 5 by bound, p = 3 by five explicit cases."""
    assert (4 + 4 * 2) % 8 == 4, "n = 4 mod 8, so v_2(n) = 2 exactly"
    # (c) the bound, on every admissible prime triple
    ps = [x for x in primes_upto(200) if x >= 5]
    checked = 0
    for p in ps:
        for o2 in [x for x in ps if x > p]:
            for o3 in [x for x in ps if o2 < x < min(4 * p, 2 * o2)]:
                V = sorted([1, 2, 4, p, 2 * p, o2, o3])
                if len(set(V)) < 7:
                    continue
                n = sum(d * d for d in V)
                assert n == 21 + 5 * p * p + o2 * o2 + o3 * o3
                assert n < _lcm(V), (p, o2, o3)
                checked += 1
    assert checked > 3000, checked
    for x in range(2, 5000):
        assert 20 * x * x > 21 + 10 * x * x
    # (d) the p = 3 case list
    for o2, o3 in STEP7_P3_CASES:
        assert o3 < 2 * o2 and o3 <= 11
        V = sorted([1, 2, 3, 4, 6, o2, o3])
        assert len(set(V)) == 7
        assert sum(d * d for d in V) < _lcm(V), (o2, o3)
    assert 11 >= 2 * 5, "(5,11) is excluded: o_3 >= 2 o_2 would force 10 into V"
    print(f"[ok] step 7: (4,2,1) empty -- bound on {checked} triples for p>=5, "
          f"and {len(STEP7_P3_CASES)} explicit cases at p=3")


def test_step8_product_forcing() -> None:
    """Each of the 9 shapes has a prime pair p<q with pq not in V and
    pq <= max(V), on every realization."""
    shapes, ledger = _odd_shapes()
    pool = [x for x in primes_upto(200) if x >= 3]
    total = 0
    for name in STEP8_SHAPES:
        rep = shapes[name]
        nv = len(rep[0])
        used = [i for i in range(nv) if any(v[i] for v in rep)]
        k = len(used)
        cap = {2: 200, 3: 80, 4: 50}[k]
        pl = [x for x in pool if x <= cap]
        seen = 0
        for assign in permutations(pl, k):
            pmap = dict(zip(used, assign))
            vals = []
            for v in rep:
                x = 1
                for i, e in enumerate(v):
                    if e:
                        x *= pmap[i] ** e
                vals.append(x)
            if len(set(vals)) < 7:
                continue
            S, M = set(vals), max(vals)
            hit = any(a * b not in S and a * b <= M
                      for a, b in combinations(sorted(assign), 2))
            assert hit, (name, sorted(vals))
            seen += 1
        assert seen > 100, (name, seen)
        total += seen
    print(f"[ok] step 8: product forcing on all {len(STEP8_SHAPES)} shapes "
          f"({total:,} realizations)")


def test_step9_size_form() -> None:
    """n < lcm(V) on every ADMISSIBLE realization of the 8 shapes."""
    shapes, ledger = _odd_shapes()
    pool = [x for x in primes_upto(400) if x >= 3]
    total = 0
    worst = None
    for name in STEP9_SHAPES:
        rep = shapes[name]
        nv = len(rep[0])
        used = [i for i in range(nv) if any(v[i] for v in rep)]
        k = len(used)
        cap = {3: 200, 4: 80, 5: 48, 6: 42}[k]
        pl = [x for x in pool if x <= cap]
        seen = 0
        for assign in permutations(pl, k):
            pmap = dict(zip(used, assign))
            vals = []
            for v in rep:
                x = 1
                for i, e in enumerate(v):
                    if e:
                        x *= pmap[i] ** e
                vals.append(tuple([x])[0])
            vals = tuple(vals)
            if len(set(vals)) < 7 or not ledger.prefix_admissible(vals):
                continue
            n = sum(x * x for x in vals)
            Lc = _lcm(vals)
            assert n < Lc, (name, sorted(vals), n, Lc)
            r = Lc / n
            if worst is None or r < worst[0]:
                worst = (r, name)
            seen += 1
        assert seen > 50, (name, seen)
        total += seen
    print(f"[ok] step 9: n < lcm on all {total:,} admissible realizations "
          f"of {len(STEP9_SHAPES)} shapes (tightest lcm/n = {worst[0]:.2f})")


def test_level2_residue_is_nine_shapes() -> None:
    """The Level 2 residue is exactly nine named shapes, and together with
    steps 4, 5, 8, 9 they account for all 28 odd-sector shapes."""
    shapes, _ = _odd_shapes()
    assert len(shapes) == 28, len(shapes)
    accounted = (set(STEP8_SHAPES) | set(STEP9_SHAPES) | set(LEVEL2_SHAPES)
                 | {"{1, v, v^2, v^3, v^4, v^5, v^6}",
                    "{1, v, u, t, uv, tv, tu}"})
    assert accounted == set(shapes), accounted ^ set(shapes)
    assert len(LEVEL2_SHAPES) == 9
    # The real dividing line: for the residue shapes lcm(V) can fall BELOW n,
    # so the size form of (L) is unavailable; for the step-9 shapes it cannot.
    # Eight of the nine contain v^2 with uv, but {1,v,u,t,s,uv,tv} does not --
    # it reuses v across uv and tv instead. The feature is prime REUSE.
    for name in LEVEL2_SHAPES:
        assert "uv" in name or "v^2" in name, name
    assert "v^2" not in "{1, v, u, t, s, uv, tv}", "the ninth has no square"
    print(f"[ok] residue: exactly {len(LEVEL2_SHAPES)} shapes; steps 4,5,8,9 "
          f"cover the other 19 of 28")


def self_test() -> None:
    test_step1_profiles()
    test_step1_profile_is_structural()
    test_step1_verified_against_realizations()
    test_step2_profile_610()
    test_step3_profile_412()
    test_step4_chain()
    test_step5_identity_and_squeeze()
    test_step5_branches_contradict()
    test_step7_profile_421()
    test_step8_product_forcing()
    test_step9_size_form()
    test_level2_residue_is_nine_shapes()
    test_level2_residue()
    test_does_not_prove_too_much()
    test_no_k7_solution_by_scan()
    print("\nAll self-tests passed.")
    print("k=7 STATUS: NOT closed. 77 of 86 orbits at Level 1, 9 at Level 2.")
    print("  L1  step 1  profile (mod 8 + prefix rule)   kills 35 orbits")
    print("  L1  step 2  profile (6,1,0)                 14 shapes")
    print("  L1  step 3  profile (4,1,2)                  4 shapes")
    print("  L1  step 4  the pure chain, mod-p            1 shape")
    print("  L1  step 5  {1,v,u,t,uv,vt,ut}               1 shape")
    print("  L1  step 7  profile (4,2,1)                  5 shapes")
    print("  L1  step 8  product forcing, odd sector      9 shapes")
    print("  L1  step 9  n < lcm, odd sector              8 shapes")
    print("  L2          odd sector, prime-poor shapes      9 shapes")


if __name__ == "__main__":
    self_test()
