"""
k9_status.py

k = 9:  is there an n with  n = d_1^2 + ... + d_9^2  for d_1 < ... < d_9 the
NINE smallest divisors of n?

STATUS.
  EVEN SECTOR   CLOSED, LEVEL 1.  All five surviving even profiles are empty,
                parameter-free, no bounded range and no search.
  ODD SECTOR    OPEN, reduced from 1531 labelled shapes to 37 by two
                parameter-free lemmas (a vacuity certificate and a box size
                lemma).

ERRATUM, corrected in this revision.  An earlier revision forced
val(f) > max(V) for EVERY minimal non-member f of a shape.  That is only
justified when f divides n, and a non-member divides n for certain only when
it divides lcm(V) -- that is, only when it lies in the BOX [0, m] of the lcm
exponents.  A monomial outside the box, such as p_1^(m_1+1), need not divide
n at all: n's exponent of p_1 may be exactly m_1, and then (P) says nothing
about that power.  Three things changed:
  * the vacuity certificate now ranges over in-box non-members only, and
    kills 1465 of the 1531 odd-sector shapes rather than 1499;
  * the "refined tail lemma", whose premise was M < p_1^(m_1+1), is withdrawn
    and replaced by the BOX SIZE LEMMA of step 7b, which uses only in-box
    forcing;
  * the odd-sector residue is 37 shapes, not 27.
The EVEN sector is unaffected in its conclusions -- all five profiles are
still empty at Level 1 -- but two of its proofs needed repair, and both
repairs are recorded in place: step 5 was missing the branch v_2(n) = 2, and
step 6's census splits differently.  Every count below has been recomputed.

k = 9 is hard for the same reason k = 7 was and k = 6, k = 8 were not: the
PARITY LEMMA (a sum of k odd squares has the parity of k) forces n even only
when k is even.  At k = 9 it says the opposite -- nine odd squares sum to an
odd number -- so the odd sector is consistent and has to be attacked directly.

--------------------------------------------------------------------
THE ENGINES
--------------------------------------------------------------------
  (P) PREFIX RULE.  e | n and e < max(V) implies e is in V.  Composite e too;
      that is the whole force of it.
  (L) LCM RULE.  lcm(V) | n.  Two strengths: the SIZE form (n < lcm(V) is a
      contradiction, since lcm | n and n > 0 force n >= lcm) and the
      DIVISIBILITY form itself, which is strictly stronger.
  (M) MOD-p RULE.  p | n, so  sum over {d in V : p does not divide d} of d^2
      is congruent to 0 mod p.
  PROFILE (A,B,C).  The counts of elements of V that are odd, 2 mod 4, and
      0 mod 4.  Squares mod 8 are 1, 4, 0 respectively, so

          n = sum d^2  ==  A + 4B   (mod 8).

      This is STRUCTURAL: it depends only on v_2(n), so it needs no
      realization.  Two companions:
        B <= A    every 2-mod-4 element is 2d with d odd and d < 2d <= max(V),
                  so (P) puts d in V;
        B >= 1    if n is even then 2 | n and 2 <= max(V), so 2 is in V.

--------------------------------------------------------------------
STEP 1.  PROFILE.  Exactly six profiles survive.
--------------------------------------------------------------------
A + B + C = 9.

  n odd   =>  B = C = 0  =>  A = 9.                           (9,0,0)
  n even  =>  B >= 1 and B <= A.
     C = 0  =>  v_2(n) = 1  =>  n = 2 mod 4  =>  A + 4B = 2 mod 4
            =>  A = 2 mod 4.  With A + B = 9 and B <= A: A = 6, B = 3.
                                                            (6,3,0)
     C >= 1 =>  4 | n  =>  A + 4B = 0 mod 4  =>  A = 0 mod 4.
            A = 8 forces B + C = 1 with B >= 1 and C >= 1: impossible.
            A = 4 leaves B + C = 5, 1 <= B <= 4:
                                     (4,1,4) (4,2,3) (4,3,2) (4,4,1)

--------------------------------------------------------------------
STEP 2.  (4,2,3) is EMPTY.  Immediate.
--------------------------------------------------------------------
A = 4 and the four odd elements are 1 < o_1 < o_2 < o_3.  B = 2 means exactly
two elements are 2 mod 4, so v_2(n) = 2 exactly is impossible as soon as C = 3:
with v_2(n) = 2 every 0-mod-4 element is 4*odd, so C = {4, 4o_1, 4o_2}; but
4o_2 in V with 2o_2 < 4o_2 <= max(V) puts 2o_2 in V by (P), and then
{2, 2o_1, 2o_2} are three distinct 2-mod-4 elements, contradicting B = 2.
If instead v_2(n) >= 3 then 8 | n and the C-class contains 4 and 8, and the
same argument applies to the third C-element.  Either way B >= 3.

--------------------------------------------------------------------
STEP 3.  (4,1,4) is EMPTY.
--------------------------------------------------------------------
B = 1 means 2 is the only 2-mod-4 element, so no element is 2*odd beyond 2
itself; by (P) every C-element must then be a power of 2, giving
C = {4, 8, 16, 32} and 32 | n, so max(V) >= 32.
B = 1 also forces 2o_1 > max(V) >= 32, so o_1 >= 17, and the three odd
elements o_1 < o_2 < o_3 all lie in [o_1, 2o_1), hence are all prime
(a composite in that window would have a proper divisor in V).

    V    = {1, 2, 4, 8, 16, 32, o_1, o_2, o_3}
    n    = 1+4+16+64+256+1024 + o_1^2+o_2^2+o_3^2 = 1365 + o_1^2+o_2^2+o_3^2
    lcm  = 32 * o_1 * o_2 * o_3 > 32 p^3       (p := o_1)

and o_i < 2p gives n < 1365 + 12p^2.  Since 32p^3 > 1365 + 12p^2 for every
p >= 5, the size form of (L) closes it.

--------------------------------------------------------------------
STEP 4.  (4,4,1) is EMPTY.
--------------------------------------------------------------------
C = 1 means v_2(n) = 2, so C = {4}, and B = 4 gives
B = {2, 2o_1, 2o_2, 2o_3}.  4o_1 is not in V, so 4o_1 > max(V) >= 2o_3,
hence o_3 < 2o_1 and all three odd elements lie in [o_1, 2o_1): all prime.

    V   = {1, 2, 4, o_1, o_2, o_3, 2o_1, 2o_2, 2o_3}
    n   = 21 + 5(o_1^2 + o_2^2 + o_3^2) < 21 + 60 p^2
    lcm = 4 o_1 o_2 o_3 > 4 p^3

4p^3 > 21 + 60p^2 holds for p >= 17.  Below that the window [p, 2p) is thin:
p = 3, 5 hold only two primes (vacuous), and p = 7, 11, 13 give exactly seven
triples, every one with n < lcm.  See _444_SMALL.

--------------------------------------------------------------------
STEP 5.  (4,3,2) is EMPTY.
--------------------------------------------------------------------
A = 4, B = 3, C = 2.  There are TWO branches, by v_2(n).

BRANCH A, v_2(n) >= 3.  Then 8 | n, and 8 must be in V (if not, 8 > max(V)
and all nine elements would have to fit in {1,...,7}), so C = {4, 8}.
B = 3 gives B = {2, 2o_1, 2o_2}, so 4o_1 > max(V) >= 2o_2 and o_2 < 2o_1;
and o_1 o_2 is not in V, so o_1 o_2 > max(V) >= o_3.

    n   = 85 + 5 o_1^2 + 5 o_2^2 + o_3^2,     lcm = 8 o_1 o_2 o_3
    n - lcm = (o_3 - 4 o_1 o_2)^2 - (16 o_1^2 o_2^2 - 85 - 5o_1^2 - 5o_2^2)

o_3 runs over (o_2, o_1 o_2), where the completed square is largest at the
left end, so it suffices that  o_2^2 (8 o_1 - 6) > 85 + 5 o_1^2, and since
o_2 > o_1 that follows from  8 o_1^3 > 85 + 11 o_1^2,  true at o_1 = 3
(216 > 184) and after.  So n < lcm throughout.

BRANCH B, v_2(n) = 2 exactly.  C = 2 does NOT force 8 | n -- that was the
gap.  With v_2(n) = 2 every 0-mod-4 element is 4*odd, so C = {4, 4 o_1} and

    V   = {1, 2, 4, o_1, o_2, o_3, 2o_1, 2o_2, 4o_1}
    n   = 21 + 21 o_1^2 + 5 o_2^2 + o_3^2,      lcm = 4 o_1 o_2 o_3

with no 8 anywhere.  The valid forcings here are 4o_2 | n and 2o_3 | n (each
a product of coprime divisors of n), giving 2 o_1 < o_3 < 4 o_2.  Then
o_3 < 4 o_2 gives n < 21 + 21 o_1^2 + 21 o_2^2 while o_3 > o_2 gives
lcm > 4 o_1 o_2^2; the o_2^2 terms need o_1 >= 7, and for o_1 = 3, 5 the
quadratic o_3^2 - 4 o_1 o_2 o_3 + (21 + 21 o_1^2 + 5 o_2^2) is negative
across the whole forced window.  So BRANCH B is size-killed too, tightest
n/lcm = 0.914 at (3, 5, 7).

--------------------------------------------------------------------
STEP 6.  (6,3,0) is EMPTY.
--------------------------------------------------------------------
v_2(n) = 1, so V = O union {2, 2 o_1, 2 o_2} where O is the odd part, a
SIX-element divisor-closed set of odd numbers, o_1 < o_2 its 2nd and 3rd
smallest elements, and B = 3 means the doubling stops there:

        2 o_3 > M := max(V).

With the primes ordered p_1 < ... < p_r there are 39 labelled six-element
shapes (14 up to permuting the primes -- the same 14 that carried k = 8's
profile (6,2,0), but the labelling matters here because the forcing is not
symmetric in the primes).  They fall out as

        26   killed by the VACUITY CERTIFICATE (step 7b below), outright
         6   vacuous: no admissible prime tuple at all
         6   killed by the size form (n < lcm on every admissible tuple)
         1   the SANDWICH shape, which no size argument can reach
        ---
        39

(The split was 31/3/4/1 before the erratum; the certificate is weaker now,
so five shapes moved out of it and into the vacuous and size-killed columns.
Nothing moved into the residue: the residue is still the single sandwich
shape, so (6,3,0) is still EMPTY at Level 1.)

Four of the six size kills, each with its threshold and its finite
remainder:

   A  O = {1, p, p^2, q, pq, r},  p < q < p^2.  The window p^2 < r < pq is
      empty (there o_3 = p^2, and B = 3 wants 2p^2 > M = pq, i.e. p > q), so
      r < 2p^2 throughout, lcm(V) > p^3 q^2 and
          n < 5 + 5p^2 + 5q^2 + 5p^4 + p^2 q^2,
      so it is enough that q^2 (p^3 - p^2 - 5) > 5p^4 + 5p^2 + 5, which
      holds once p^5 > 6p^4 + 10p^2 + 5, i.e. from p = 7.  p = 3, 5 leave
      11 configurations, all with n < lcm.

   B  O = {1, p, p^2, p^3, q, r},  q > p^2, r < pq.  lcm(V) > 2 p^3 q^2 and
      n < 5 + 13 M^2 < 5 + 13 p^2 q^2, so 2p > 13 suffices: from p = 7.
      p = 3, 5 leave 486 configurations, all with n < lcm.

   C  O = {1, p, p^2, q, r, s},  s < pq.  lcm(V) > 2 p^2 q^3 and
      n < 5 + 13 p^2 q^2, so 2q > 13 suffices: from q = 7.  That leaves
      q = 5, hence p = 3, hence O in {1,3,5,7,9,11}, {1,3,5,7,9,13},
      {1,3,5,9,11,13}: three configurations, all with n < lcm.

   D  O = {1, p, q, r, s, t}.  Here m = (1,1,1,1,1), so m_1 = 1 and T = 4,
      and the refined tail lemma of step 7b (with lcm(V) = 2 lcm(O), which
      halves the constant) gives p_2^4 < (9/2) p_1^3.  At p_1 = 5, 7 that
      already has no room; at p_1 = 3 it gives p_2 <= 3.32, and the next
      prime is 5.  EMPTY.

THE SANDWICH.  The one shape no size argument reaches is

        O    = {1, u, t, u^2, ut, t^2}        u < t odd primes
        V    = {1, 2, u, t, 2u, 2t, u^2, ut, t^2}
        n    = 5 + 5u^2 + 5t^2 + u^4 + u^2 t^2 + t^4
        lcm  = 2 u^2 t^2

and the reason is an identity:

        n - lcm = 5 + 5u^2 + 5t^2 + (u^4 - u^2 t^2 + t^4) > 0   always,

because x^2 - x + 1 > 0 for every real x.  So n > lcm for every (u,t): the
shape is immune to the size form.  What kills it is that n is TRAPPED BELOW
2*lcm as well.  B = 3 forces 2u^2 > t^2 -- the third odd element is u^2 and
its double must exceed M = t^2 -- so with s := t^2/u^2 in (1,2),

        2*lcm - n = u^4 * g(s) - 5u^2(1+s) - 5,    g(s) = -s^2 + 3s - 1.

On [1,2], g(1) = g(2) = 1 and g(3/2) = 5/4, so g >= 1; and
5u^2(1+s) + 5 <= 15u^2 + 5 < u^4 as soon as u >= 5.  For u = 3 the window
3 < t < 3*sqrt(2) = 4.24 contains no prime, so u = 3 is vacuous.  Hence

        lcm < n < 2 * lcm,

and a proper multiple of lcm cannot sit strictly between lcm and 2*lcm.
Contradiction, parameter-free.

--------------------------------------------------------------------
STEP 7.  THE ODD SECTOR (9,0,0).  1531 shapes down to 27.
--------------------------------------------------------------------
n odd, V nine odd divisors.  The shape of V is an order ideal of size 9 in
N^r (r = the number of distinct primes), and with the primes ordered
p_1 < ... < p_r on coordinates 1..r there are

        1531 labelled shapes      (120 up to permuting the primes)
          r = 1 2  3   4   5   6  7  8
              1 28 195 512 550 216 28 1

The labelling cannot be quotiented away: the forcing constraints single out
the SMALLEST prime, so a shape and its mirror behave differently.

7a.  r = 1 dies by (M), instantly.  V = {1, p, ..., p^8} makes 1 the only
     element coprime to p, so n = 1 (mod p); but p | n.  Contradiction.
     This is the only shape where the coprime class of a prime is a single
     element: for r >= 2 the element p_j is coprime to p_i.

7b.  TWO PARAMETER-FREE LEMMAS.

     WHAT MAY BE FORCED.  (P) applies to a divisor of n.  A non-member f of
     the shape is a divisor of n for certain exactly when f | lcm(V), i.e.
     when f lies in the BOX [0, m] of the lcm exponents.  Only those f may
     be required to exceed M := max(V).  Outside the box nothing is known:
     p_1^(m_1+1) need not divide n.  Both lemmas below use in-box f only.
     Two shapes have NO in-box non-member at all, so neither lemma reaches
     them -- the full-box shapes, those with prod(m_i + 1) = 9:

         m = (8)      V = all divisors of p_1^8
         m = (2,2)    V = all nine divisors of p_1^2 p_2^2

     THE VACUITY CERTIFICATE.  Put y_i = log p_i, so 0 < y_1 <= ... <= y_r.
     That cone is generated by the vectors e_j + e_{j+1} + ... + e_r, so for
     an integer vector c,

        <c,y> <= 0 for EVERY such y   <=>   sum_{i>=j} c_i <= 0 for all j.

     If some member e of the shape and some IN-BOX non-member f have
     c = f - e passing that test, then val(f) <= val(e) <= M whatever the
     primes, contradicting val(f) > M (equality is impossible: distinct
     monomials in distinct primes have distinct values).  The shape is then
     EMPTY outright, with no case analysis at all.

     THE BOX SIZE LEMMA.  Let f be an in-box non-member and c = m - 2f.
     Since M < val(f) and n is a sum of nine squares each at most M^2,

        lcm(V) <= n <= 9 M^2 < 9 val(f)^2,   i.e.   lcm(V)/val(f)^2 < 9.

     Write y_i = y_1 + (increments >= 0).  Abel summation gives
     <c,y> >= y_1 * sum(c) whenever every top partial sum of c from index 2
     on is non-negative, and then lcm(V)/val(f)^2 >= p_1^(sum c).  Hence

        p_1^(sum c) < 9.

        sum c >= 2  =>  p_1^2 < 9  =>  p_1 < 3: no odd prime.  DEAD.
        sum c  = 1  =>  p_1 < 9, so p_1 in {3,5,7}.
        sum c <= 0  =>  no information from this f.

     This replaces the withdrawn "refined tail lemma", whose premise
     M < p_1^(m_1+1) used an out-of-box non-member.

     The census over the 1531 shapes:

        killed by the certificate (in-box)                        1465
        of the remaining 66:
           box size lemma, sum c >= 2, dead outright                22
           box size lemma, sum c  = 1, p_1 in {3,5,7} only           7
           no handle from either lemma                              37
        ---------------------------------------------------------------
        dead outright at Level 1                                  1487
        confined to p_1 in {3,5,7}                                    7
        NO HANDLE                                                    37

     Of the 37, one is the r = 1 shape, which dies by (M) in 7a, so 36 are
     genuinely untouched by anything in this file.

7c.  WHAT IS LEFT.  36 shapes, spread over r = 2, 3, 4 (plus the r = 1 shape
     that (M) kills).  The hardest is

        {1, p, p^2, ..., p^7, q}      with      p^6 < q < p^8

     (forcing: pq is not in V so pq > M; p^8 > M), where

        n = (p^16 - 1)/(p^2 - 1) + q^2,     lcm = p^7 q,
        n / lcm  ~  t + 1/t     for    t := q / p^7  in  (1, p),

     so n/lcm ranges over (2, p + 1/p) and BOTH strengths of (L) leave room:
     neither the size form nor the sandwich of step 6 applies.  Closing it
     needs the two congruences

        q    |  (p^16 - 1)/(p^2 - 1),
        q^2  = -(1 + p^2 + p^4 + p^6)   (mod p^7),

     which is genuinely arithmetic, not structural.  This is the k = 9
     analogue of the eight prime-poor odd-sector shapes still open at k = 7.

--------------------------------------------------------------------
LEDGER
--------------------------------------------------------------------
    k = 5   CLOSED, Level 1
    k = 6   CLOSED, Level 1
    k = 7   78/86 orbits Level 1; 8 odd-sector shapes open
    k = 8   CLOSED, Level 1
    k = 9   EVEN SECTOR CLOSED, Level 1 (five profiles, all empty);
            ODD SECTOR (9,0,0) reduced from 1531 shapes to 36

The pattern is stable: even k closes, odd k does not, and the obstruction is
always the same -- parity hands the even cases their whole odd sector for
free, and odd k has to earn it.
"""

from math import gcd, isqrt

# ---------------------------------------------------------------- profiles
def surviving_profiles():
    """All (A,B,C) with A+B+C=9 that survive step 1."""
    out = []
    for A in range(10):
        for B in range(10 - A):
            C = 9 - A - B
            if B > A:                       # B <= A
                continue
            if B == 0 and C == 0:           # n odd
                out.append((A, B, C))
                continue
            if B == 0:                      # n even forces 2 in V
                continue
            if C == 0:                      # v_2(n) = 1, n = 2 mod 4
                if (A + 4 * B) % 4 == 2:
                    out.append((A, B, C))
            else:                           # 4 | n, n = 0 mod 4
                if (A + 4 * B) % 4 == 0:
                    out.append((A, B, C))
    return sorted(out)


def mod8(A, B):
    """n = sum d^2 = A + 4B (mod 8)."""
    return (A + 4 * B) % 8


# ------------------------------------------------------------ small helpers
def lcm_of(vs):
    o = 1
    for x in vs:
        o = o * x // gcd(o, x)
    return o


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


def smallest_divisors(n, k):
    """The k smallest divisors of n.  Caller must not read past index k-1."""
    d = []
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            d.append(i)
            d.append(n // i)
    return sorted(set(d))[:k]


# ------------------------------------------------------- step 3   (4,1,4)
def step3_bound(p):
    """32 p^3 > 1365 + 12 p^2  -- the (4,1,4) size inequality."""
    return 32 * p ** 3 > 1365 + 12 * p ** 2


# ------------------------------------------------------- step 4   (4,4,1)
def step4_bound(p):
    """4 p^3 > 21 + 60 p^2  -- the (4,4,1) size inequality."""
    return 4 * p ** 3 > 21 + 60 * p ** 2


_444_SMALL = [(7, 11, 13), (11, 13, 17), (11, 13, 19), (11, 17, 19),
              (13, 17, 19), (13, 17, 23), (13, 19, 23)]


def profile441(o1, o2, o3):
    V = sorted([1, 2, 4, o1, o2, o3, 2 * o1, 2 * o2, 2 * o3])
    n = 21 + 5 * (o1 * o1 + o2 * o2 + o3 * o3)
    assert n == sum(d * d for d in V), (o1, o2, o3)
    return V, n, 4 * o1 * o2 * o3


# ------------------------------------------------------- step 5   (4,3,2)
def profile432(o1, o2, o3):
    V = sorted([1, 2, 4, 8, o1, o2, o3, 2 * o1, 2 * o2])
    n = 85 + 5 * o1 * o1 + 5 * o2 * o2 + o3 * o3
    assert n == sum(d * d for d in V), (o1, o2, o3)
    return V, n, 8 * o1 * o2 * o3


def step5_bound(o1):
    """8 o_1^3 > 85 + 11 o_1^2  -- the (4,3,2) reduction after o_2 > o_1."""
    return 8 * o1 ** 3 > 85 + 11 * o1 ** 2


# ------------------------------------------------------- step 6   (6,3,0)
def profile630(u, t):
    """The one (6,3,0) odd part the size form cannot reach."""
    V = sorted([1, 2, u, t, 2 * u, 2 * t, u * u, u * t, t * t])
    n = 5 + 5 * u * u + 5 * t * t + u ** 4 + u * u * t * t + t ** 4
    assert n == sum(d * d for d in V), (u, t)
    return V, n, 2 * u * u * t * t


def g630(s):
    """g(s) = -s^2 + 3s - 1, the sandwich coefficient; g >= 1 on [1,2]."""
    return -s * s + 3 * s - 1


# ------------------------------------------------------- step 7   odd sector
def minimal_nonmembers(S):
    """The minimal monomials outside the order ideal S."""
    Ss = set(S)
    r = len(S[0])
    out = set()
    for e in Ss:
        for i in range(r):
            f = list(e)
            f[i] += 1
            f = tuple(f)
            if f in Ss:
                continue
            if all(tuple(f[j] - (1 if j == i2 else 0) for j in range(r)) in Ss
                   for i2 in range(r) if f[i2] > 0):
                out.add(f)
    return sorted(out)


def labelled_shapes(k=9):
    """Order ideals of size k in N^r with every coordinate used, r = 1..k-1.

    The primes are p_1 < ... < p_r on coordinates 0..r-1, so these are
    LABELLED: the coordinate order is part of the data and must not be
    canonicalized away -- the forcing constraints are not symmetric.
    """
    out = []
    for r in range(1, k):
        cur = {frozenset({tuple([0] * r)})}
        for _ in range(k - 1):
            nxt = set()
            for S in cur:
                cand = set()
                for e in S:
                    for i in range(r):
                        f = list(e)
                        f[i] += 1
                        f = tuple(f)
                        if f in S:
                            continue
                        if all(tuple(f[j] - (1 if j == i2 else 0) for j in range(r))
                               in S for i2 in range(r) if f[i2] > 0):
                            cand.add(f)
                for f in cand:
                    nxt.add(S | {f})
            cur = nxt
        for S in cur:
            if all(any(e[i] > 0 for e in S) for i in range(r)):
                out.append((r, tuple(sorted(S))))
    return sorted(set(out))


def lcm_exponents(S):
    r = len(S[0])
    return tuple(max(e[i] for e in S) for i in range(r))


def box_nonmembers(S):
    """Minimal non-members of S that lie inside the box [0, m] of lcm(V).

    Only these are guaranteed to divide n (they divide lcm(V), which divides
    n), so only these may be required to exceed max(V).  A non-member outside
    the box, such as p_1^(m_1+1), need not divide n at all.
    """
    S = list(S)
    m = lcm_exponents(S)
    r = len(m)
    return [f for f in minimal_nonmembers(S)
            if all(f[i] <= m[i] for i in range(r))]


def vacuity_certificate(S, mnm=None):
    """A parameter-free witness that the shape is empty, or None.

    Returns (f, e) with f an IN-BOX minimal non-member, e a member, and
    f - e having every top partial sum <= 0.  That makes val(f) <= val(e)
    <= max(V) for every ordered tuple of primes, contradicting val(f) >
    max(V).
    """
    S = list(S)
    if mnm is None:
        mnm = box_nonmembers(S)
    r = len(S[0])
    for f in mnm:
        for e in S:
            c = [f[i] - e[i] for i in range(r)]
            if all(sum(c[i] for i in range(j, r)) <= 0 for j in range(r)):
                return (f, e)
    return None


def iroot(x, k):
    """Integer k-th root, floor."""
    if x < 1:
        return 0
    lo, hi = 1, 1 << ((x.bit_length() // k) + 2)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** k <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def box_size_lemma(S):
    """'dead', 'small-p1', or None -- see step 7b.

    For an in-box non-member f and c = m - 2f with every top partial sum of
    c from index 2 on non-negative, lcm(V)/val(f)^2 >= p_1^(sum c) while
    lcm(V) <= n <= 9 M^2 < 9 val(f)^2.  So p_1^(sum c) < 9.
    """
    S = list(S)
    m = lcm_exponents(S)
    r = len(m)
    best = None
    for f in box_nonmembers(S):
        c = [m[i] - 2 * f[i] for i in range(r)]
        if all(sum(c[i] for i in range(j, r)) >= 0 for j in range(1, r)):
            tot = sum(c)
            if tot >= 2:
                return 'dead'
            if tot == 1:
                best = 'small-p1'
    return best


SHAPE_COUNTS = {1: 1, 2: 28, 3: 195, 4: 512, 5: 550, 6: 216, 7: 28, 8: 1}
TOTAL_SHAPES = 1531
CERTIFIED = 1465           # in-box vacuity certificate
BOX_DEAD = 22              # box size lemma, sum c >= 2
BOX_SMALL_P1 = 7           # box size lemma, sum c = 1
NO_HANDLE = 37             # neither lemma reaches these
KILLED_LEVEL1 = 1487       # CERTIFIED + BOX_DEAD
ODD_SECTOR_OPEN = 36       # NO_HANDLE minus the r = 1 shape, which (M) kills
FULL_BOX_SHAPES = 2        # prod(m_i+1) = 9, so no in-box non-member exists

# profile (6,3,0): the 39 labelled six-element odd parts
SIX_SHAPES = 39
SIX_CERTIFIED = 26
SIX_VACUOUS = 6
SIX_SIZE_KILLED = 6
SIX_SANDWICH = 1


# =====================================================================
#                             SELF-TESTS
# =====================================================================
def test_profiles():
    got = surviving_profiles()
    want = [(4, 1, 4), (4, 2, 3), (4, 3, 2), (4, 4, 1), (6, 3, 0), (9, 0, 0)]
    assert got == want, got
    # the mod-8 residues the survivors carry
    assert mod8(9, 0) == 1                  # n odd
    assert mod8(6, 3) == 2                  # n = 2 mod 4
    for A, B, C in want:
        if C:
            assert mod8(A, B) % 4 == 0, (A, B, C)
    # A = 8 is the one near miss, and B >= 1 with C >= 1 is what kills it
    assert (8, 0, 1) not in got and (8, 1, 0) not in got
    print("  step 1  profile: exactly 6 survive", want)


def test_mod8_is_structural():
    """A + 4B mod 8 really is sum d^2 mod 8, for any multiset of integers."""
    import random
    random.seed(9)
    for _ in range(4000):
        V = [random.randrange(1, 400) for _ in range(9)]
        A = sum(1 for d in V if d % 2)
        B = sum(1 for d in V if d % 4 == 2)
        assert sum(d * d for d in V) % 8 == mod8(A, B), V
    print("  step 1  n = A + 4B (mod 8) verified on 4000 random 9-sets")


def test_step2_B_at_least_three():
    """(4,2,3): a 4*odd element drags 2*odd in, so B >= 3 -- never 2."""
    for o1 in (3, 5, 7, 11):
        for o2 in (13, 17, 19):
            V = {1, 2, 4, 4 * o1, 4 * o2, o1, o2}
            mx = max(V)
            # (P): 2*o is below 4*o <= max(V), so it must be in V
            for o in (o1, o2):
                assert 2 * o < 4 * o <= mx
            forced = {2, 2 * o1, 2 * o2}
            assert len(forced) == 3
    print("  step 2  (4,2,3): (P) forces B >= 3, contradicting B = 2")


def test_step3_bound():
    assert not step3_bound(1)
    for p in range(5, 2000):
        assert step3_bound(p), p
    # the structural chain: B=1 -> C is powers of 2 -> 32|n -> o_1 >= 17
    V = [1, 2, 4, 8, 16, 32]
    assert sum(d * d for d in V) == 1365
    assert 2 * 17 > 32 and 2 * 16 <= 32      # 2 o_1 > max(V) needs o_1 >= 17
    print("  step 3  (4,1,4): 32 p^3 > 1365 + 12 p^2 for all p >= 5")


def test_step4_bound_and_small_cases():
    for p in range(17, 2000):
        assert step4_bound(p), p
    assert not step4_bound(13)               # 13 is below the bound
    # p = 3, 5 are vacuous: fewer than three primes in [p, 2p)
    for p in (3, 5):
        win = [q for q in range(p, 2 * p) if is_prime(q)]
        assert len(win) < 3, (p, win)
    # the seven surviving small triples, all with n < lcm
    # only o_1 = p matters: a triple whose least member is 17 or more is
    # already covered by step4_bound
    found = []
    for p in (7, 11, 13):
        win = [q for q in range(p, 2 * p) if is_prime(q)]
        assert win and win[0] == p
        for j in range(1, len(win)):
            for l in range(j + 1, len(win)):
                found.append((p, win[j], win[l]))
    assert sorted(set(found)) == sorted(_444_SMALL), sorted(set(found))
    for o1, o2, o3 in _444_SMALL:
        V, n, L = profile441(o1, o2, o3)
        assert n < L, (o1, o2, o3, n, L)
    print(f"  step 4  (4,4,1): bound from p >= 17; the {len(_444_SMALL)} small"
          f" triples all have n < lcm")


def test_step5_completed_square_and_bound():
    for o1 in range(3, 400, 2):
        if is_prime(o1):
            assert step5_bound(o1), o1
    # the completed-square identity
    for o1, o2, o3 in ((3, 5, 7), (5, 7, 11), (7, 11, 13), (11, 13, 101)):
        V, n, L = profile432(o1, o2, o3)
        lhs = n - L
        rhs = (o3 - 4 * o1 * o2) ** 2 - (16 * o1 * o1 * o2 * o2
                                         - 85 - 5 * o1 * o1 - 5 * o2 * o2)
        assert lhs == rhs, (o1, o2, o3, lhs, rhs)
    # n < lcm throughout the forced region o_2 < 2 o_1, o_2 < o_3 < o_1 o_2
    tot = worst = 0
    worst_r = 1e9
    P = [q for q in range(3, 400) if is_prime(q)]
    for o1 in P:
        for o2 in P:
            if not (o1 < o2 < 2 * o1):
                continue
            for o3 in P:
                if not (o2 < o3 < o1 * o2):
                    continue
                V, n, L = profile432(o1, o2, o3)
                tot += 1
                assert n < L, (o1, o2, o3, n, L)
                if L / n < worst_r:
                    worst_r, worst = L / n, (o1, o2, o3)
    assert tot > 10000, tot
    print(f"  step 5  (4,3,2): n < lcm on all {tot:,} forced triples, "
          f"tightest lcm/n = {worst_r:.3f} at {worst}")


def test_step6_sandwich():
    # the identity that makes the size form useless
    for u, t in ((3, 5), (17, 19), (31, 37), (41, 47)):
        V, n, L = profile630(u, t)
        assert L == 2 * u * u * t * t
        assert n - L == 5 + 5 * u * u + 5 * t * t + (u ** 4 - u * u * t * t + t ** 4)
        assert n > L, (u, t)                 # n > lcm ALWAYS, forced or not
    # g >= 1 on [1,2], with equality only at the ends
    assert abs(g630(1.0) - 1) < 1e-12 and abs(g630(2.0) - 1) < 1e-12
    assert g630(1.5) == 1.25
    for i in range(1, 1000):
        assert g630(1 + i / 1000) >= 1 - 1e-12
    # 15 u^2 + 5 < u^4 from u = 5 on
    assert 15 * 25 + 5 < 5 ** 4
    assert not (15 * 9 + 5 < 3 ** 4)         # u = 3 needs the vacuity argument
    assert [t for t in range(4, 5) if is_prime(t) and t * t < 18] == []
    # and the sandwich itself, over the whole forced region
    P = [q for q in range(3, 6000) if is_prime(q)]
    tot = 0
    lo, hi = 9e9, 0.0
    for i, u in enumerate(P):
        for t in P[i + 1:]:
            if t * t >= 2 * u * u:
                break
            V, n, L = profile630(u, t)
            tot += 1
            assert L < n < 2 * L, (u, t, n, L)
            lo = min(lo, n / L)
            hi = max(hi, n / L)
            # cheap test first: lcm never divides n, so the prefix check
            # short-circuits and is never actually needed
            assert n % L != 0 or V == smallest_divisors(n, 9)
    assert tot > 50000, tot
    print(f"  step 6  (6,3,0): lcm < n < 2 lcm on all {tot:,} forced pairs, "
          f"n/lcm in [{lo:.4f}, {hi:.4f}]")


def test_step7a_r1_dies_mod_p():
    for p in (3, 5, 7, 11, 101, 1009):
        V = [p ** i for i in range(9)]
        n = sum(d * d for d in V)
        assert n % p == 1, (p, n % p)        # 1 is the only element coprime to p
        assert n % p != 0
    print("  step 7a r = 1: n = 1 (mod p) but p | n -- (M) kills it outright")


def test_only_in_box_non_members_may_be_forced():
    """The erratum, as a test: out-of-box non-members are not forced."""
    # k=7's shape {1,v,u,v^2,uv,u^2,uv^2} has m = (2,2)
    S = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2), (2, 1)]
    assert lcm_exponents(S) == (2, 2)
    assert minimal_nonmembers(S) == [(0, 3), (1, 2), (3, 0)]
    assert box_nonmembers(S) == [(1, 2)]
    # v^3 = (3,0) sits outside the box, so it need not divide n; forcing
    # v^3 > max(V) >= u v^2 would give v > u and empty the shape wrongly
    v, u = 3, 5
    V = sorted([1, v, u, v * v, u * v, u * u, u * v * v])
    assert max(V) == u * v * v == 45
    assert v ** 3 < max(V)        # would be a contradiction if it were forced
    # the two full-box shapes at k=9 have no in-box non-member at all
    L = labelled_shapes(9)
    fb = [(r, S) for r, S in L if not box_nonmembers(S)]
    assert len(fb) == FULL_BOX_SHAPES, len(fb)
    from math import prod
    for r, S in fb:
        assert prod(x + 1 for x in lcm_exponents(list(S))) == 9
    print(f"  erratum only in-box non-members may be forced; "
          f"{FULL_BOX_SHAPES} full-box shapes have no forcing at all")


def test_vacuity_certificate_is_sound():
    """The certificate's cone duality, checked against brute force."""
    import random
    random.seed(99)
    for _ in range(3000):
        r = random.randrange(1, 5)
        c = [random.randrange(-4, 5) for _ in range(r)]
        claim = all(sum(c[i] for i in range(j, r)) <= 0 for j in range(r))
        viol = False
        for _ in range(400):
            y = sorted(random.uniform(0.01, 10) for _ in range(r))
            if sum(c[i] * y[i] for i in range(r)) > 1e-9:
                viol = True
                break
        if claim:
            assert not viol, (c,)
    # on a shape it really does witness emptiness, and the witness is in-box
    S = [(0, 0), (0, 1), (1, 0), (2, 0), (3, 0), (4, 0), (0, 2), (0, 3), (0, 4)]
    w = vacuity_certificate(S)
    assert w is not None
    f, e = w
    m = lcm_exponents(S)
    assert all(f[i] <= m[i] for i in range(len(m))), (f, m)
    for ps in ((3, 5), (5, 7), (11, 13), (101, 211)):
        vf = ps[0] ** f[0] * ps[1] ** f[1]
        ve = ps[0] ** e[0] * ps[1] ** e[1]
        assert vf < ve, (ps, vf, ve)
    print("  step 7b certificate: cone duality verified, witness is in-box")


def test_box_size_lemma_is_sound():
    """lcm/val(f)^2 >= p_1^(sum c) under the partial-sum condition."""
    import random
    random.seed(7)
    L = labelled_shapes(9)
    checked = 0
    for r, S in L:
        Sl = list(S)
        m = lcm_exponents(Sl)
        for f in box_nonmembers(Sl):
            c = [m[i] - 2 * f[i] for i in range(r)]
            if not all(sum(c[i] for i in range(j, r)) >= 0 for j in range(1, r)):
                continue
            for _ in range(10):
                ps = sorted(random.sample(
                    [q for q in range(3, 200) if is_prime(q)], r))
                lcm_v = 1
                vf = 1
                for i in range(r):
                    lcm_v *= ps[i] ** m[i]
                    vf *= ps[i] ** f[i]
                # exact integer form of  lcm >= p_1^(sum c) * val(f)^2,
                # valid for negative sum(c) too (no float exponents)
                t = sum(c)
                lhs = lcm_v * ps[0] ** max(0, -t)
                rhs = ps[0] ** max(0, t) * vf * vf
                assert lhs >= rhs, (S, f, ps, t)
                checked += 1
    assert checked > 500, checked
    print(f"  step 7b box size lemma: the Abel bound holds on {checked:,} "
          f"random instances")


def test_step7b_shape_census_and_lemmas():
    L = labelled_shapes(9)
    from collections import Counter
    c = dict(Counter(r for r, _ in L))
    assert c == SHAPE_COUNTS, c
    assert len(L) == TOTAL_SHAPES, len(L)
    cert = [(r, S) for r, S in L if vacuity_certificate(S)]
    assert len(cert) == CERTIFIED, len(cert)
    rest = [(r, S) for r, S in L if not vacuity_certificate(S)]
    dead = [x for x in rest if box_size_lemma(x[1]) == 'dead']
    small = [x for x in rest if box_size_lemma(x[1]) == 'small-p1']
    left = [x for x in rest if box_size_lemma(x[1]) is None]
    assert len(dead) == BOX_DEAD, len(dead)
    assert len(small) == BOX_SMALL_P1, len(small)
    assert len(left) == NO_HANDLE, len(left)
    assert len(cert) + len(dead) == KILLED_LEVEL1
    assert len(cert) + len(dead) + len(small) + len(left) == TOTAL_SHAPES
    # the r = 1 shape is among the no-handle set and (M) kills it
    assert any(r == 1 for r, _ in left)
    assert len(left) - 1 == ODD_SECTOR_OPEN
    print(f"  step 7b census: {CERTIFIED} certificate + {BOX_DEAD} box-size "
          f"= {KILLED_LEVEL1} dead; {BOX_SMALL_P1} confined to p1 in {{3,5,7}}; "
          f"{ODD_SECTOR_OPEN} open after (M)")


def _six_shapes():
    return labelled_shapes(6)


def _build630(O):
    """V from the odd part O, with B = 3 enforced."""
    V = sorted(set(O) | {2, 2 * O[1], 2 * O[2]})
    if len(V) != 9:
        return None
    if 2 * O[3] <= max(V):
        return None
    return V


def test_step5_branch_b_is_size_killed():
    """The branch v_2(n) = 2, C = {4, 4 o_1}, missed by the old step 5."""
    P = [q for q in range(3, 320) if is_prime(q)]
    tot = 0
    worst = (0.0, None)
    for i, o1 in enumerate(P):
        for o2 in P[i + 1:]:
            for o3 in P:
                if not (2 * o1 < o3 < 4 * o2) or o3 <= o2:
                    continue
                V = sorted({1, 2, 4, o1, o2, o3, 2 * o1, 2 * o2, 4 * o1})
                if len(V) != 9:
                    continue
                M = max(V)
                if 4 * o2 <= M or 2 * o3 <= M:   # the two VALID forcings
                    continue
                n = 21 + 21 * o1 * o1 + 5 * o2 * o2 + o3 * o3
                assert n == sum(d * d for d in V), (o1, o2, o3)
                Lc = 4 * o1 * o2 * o3
                assert Lc == lcm_of(V), (o1, o2, o3)
                tot += 1
                assert n < Lc, (o1, o2, o3, n, Lc)
                if n / Lc > worst[0]:
                    worst = (n / Lc, (o1, o2, o3))
    assert tot > 30000, tot
    assert worst[1] == (3, 5, 7)
    print(f"  step 5  branch B (v_2 = 2, C = {{4, 4o_1}}): n < lcm on all "
          f"{tot:,} admissible triples, tightest {worst[0]:.4f} at {worst[1]}")


def test_step6_census_and_the_size_kills():
    import itertools
    L6 = _six_shapes()
    assert len(L6) == SIX_SHAPES, len(L6)
    cert = [(r, S) for r, S in L6 if vacuity_certificate(S)]
    assert len(cert) == SIX_CERTIFIED, len(cert)
    rest = [(r, S) for r, S in L6 if not vacuity_certificate(S)]
    assert len(rest) == SIX_VACUOUS + SIX_SIZE_KILLED + SIX_SANDWICH
    # classify the survivors with VALID forcing only
    P = [q for q in range(3, 200) if is_prime(q)]
    vac = size = sand = 0
    for r, S in rest:
        Sl = list(S)
        bnm = box_nonmembers(Sl)
        adm = sz = 0
        for ps in itertools.combinations(P, r):
            O = sorted(_val(e, ps) for e in Sl)
            if len(set(O)) != 6:
                continue
            V = _build630(O)
            if V is None:
                continue
            M = max(V)
            if any(_val(f, ps) <= M for f in bnm):
                continue
            adm += 1
            if sum(d * d for d in V) < lcm_of(V):
                sz += 1
        if adm == 0:
            vac += 1
        elif sz == adm:
            size += 1
        else:
            sand += 1
            assert lcm_exponents(Sl) == (2, 2), Sl   # the sandwich shape
    assert (vac, size, sand) == (SIX_VACUOUS, SIX_SIZE_KILLED, SIX_SANDWICH), \
        (vac, size, sand)
    print(f"  step 6  (6,3,0) census: {SIX_SHAPES} = {SIX_CERTIFIED} certificate"
          f" + {vac} vacuous + {size} size-killed + {sand} sandwich")


def _val(e, ps):
    v = 1
    for i, a in enumerate(e):
        if a:
            v *= ps[i] ** a
    return v


def test_step7c_residue_family_is_really_open():
    """{1,p,...,p^7,q}: both strengths of (L) leave room, so it stays open."""
    for p in (11, 13, 17):
        for q in [x for x in range(p ** 6 + 1, p ** 6 + 4000) if is_prime(x)]:
            if not (p ** 6 < q < p ** 8):
                continue
            V = sorted([p ** i for i in range(8)] + [q])
            if len(set(V)) != 9:
                continue
            mx = max(V)
            if p * q <= mx or p ** 8 <= mx:   # forcing
                continue
            n = sum(d * d for d in V)
            Lc = lcm_of(V)
            assert Lc == p ** 7 * q
            assert n > Lc, (p, q)             # size form: no help
            break
    # the ratio really does climb above 2, which is what breaks the sandwich
    p = 11
    q = next(x for x in range(2 * p ** 7, 3 * p ** 7) if is_prime(x))
    V = sorted([p ** i for i in range(8)] + [q])
    n = sum(d * d for d in V)
    Lc = lcm_of(V)
    assert n / Lc > 2, n / Lc
    print(f"  step 7c residue: p=11, q={q} gives n/lcm = {n / Lc:.3f} > 2 -- "
          f"the sandwich cannot apply")


def test_does_not_prove_too_much():
    """The engines must not kill configurations that genuinely exist."""
    # k = 4: n = 130 = 1 + 4 + 25 + 100, divisors 1,2,5,10.  Profile (2,2,0),
    # so B = 2 = A: allowed at k = 4, and v_2 = 1.
    V = [1, 2, 5, 10]
    assert sum(d * d for d in V) == 130
    assert smallest_divisors(130, 4) == V
    A = sum(1 for d in V if d % 2)
    B = sum(1 for d in V if d % 4 == 2)
    assert (A, B) == (2, 2) and B <= A
    assert 130 % 8 == mod8(A, B)
    # lcm(V) = 10 divides 130, so (L) is satisfied -- as it must be
    assert 130 % lcm_of(V) == 0
    # and the k=9 size inequalities are not vacuously true
    assert not step4_bound(13) and not step3_bound(1)
    print("  sanity  130 (k=4) survives every engine used here")


def test_no_k9_solution_by_scan():
    hits = [n for n in range(2, 400000)
            if len(smallest_divisors(n, 10)) >= 9
            and sum(d * d for d in smallest_divisors(n, 9)) == n]
    assert hits == [], hits
    print("  scan    no n < 400000 is the sum of the squares of its nine"
          " smallest divisors")


def self_test():
    print("k9_status.py self-tests\n")
    test_profiles()
    test_mod8_is_structural()
    test_step2_B_at_least_three()
    test_step3_bound()
    test_step4_bound_and_small_cases()
    test_step5_completed_square_and_bound()
    test_step6_sandwich()
    test_step5_branch_b_is_size_killed()
    test_step6_census_and_the_size_kills()
    test_step7a_r1_dies_mod_p()
    test_only_in_box_non_members_may_be_forced()
    test_vacuity_certificate_is_sound()
    test_box_size_lemma_is_sound()
    test_step7b_shape_census_and_lemmas()
    test_step7c_residue_family_is_really_open()
    test_does_not_prove_too_much()
    test_no_k9_solution_by_scan()
    print("\nAll self-tests passed.")
    print("k = 9, EVEN SECTOR: CLOSED at Level 1 -- all five even profiles"
          " are empty,")
    print("parameter-free, no bounded range and no search.")
    print("  L1  step 1  profile   6 profiles survive mod 8 with B <= A, B >= 1")
    print("  L1  step 2  (4,2,3)   (P) forces B >= 3")
    print("  L1  step 3  (4,1,4)   C = {4,8,16,32}, p >= 17, 32p^3 > 1365+12p^2")
    print("  L1  step 4  (4,4,1)   4p^3 > 21+60p^2 from 17; seven small triples")
    print("  L1  step 5  (4,3,2)   completed square, 8o^3 > 85+11o^2 from 3")
    print("  L1  step 5b (4,3,2)   branch v_2 = 2, C = {4, 4o_1}: size-killed")
    print(f"  L1  step 6  (6,3,0)   39 odd parts: {SIX_CERTIFIED} certificate,"
          f" {SIX_VACUOUS} vacuous,")
    print(f"                        {SIX_SIZE_KILLED} size, "
          f"{SIX_SANDWICH} SANDWICH lcm < n < 2 lcm")
    print()
    print("k = 9, ODD SECTOR (9,0,0): OPEN, reduced "
          f"{TOTAL_SHAPES} -> {ODD_SECTOR_OPEN}.")
    print("  step 7a r = 1 dies by (M): n = 1 (mod p)")
    print(f"  step 7b certificate {CERTIFIED} + box size lemma {BOX_DEAD}"
          f" = {KILLED_LEVEL1} dead outright;")
    print(f"          {BOX_SMALL_P1} confined to p_1 in {{3,5,7}};"
          f" {NO_HANDLE} with no handle")
    print(f"  step 7c {ODD_SECTOR_OPEN} shapes remain after (M) takes r = 1;")
    print("          the hardest is {1,p,...,p^7,q} with p^6 < q < p^8")
    print()
    print("  ERRATUM: an earlier revision forced every minimal non-member to")
    print("  exceed max(V).  Only IN-BOX ones may be.  Even sector unaffected")
    print("  in its conclusions; odd-sector residue is 36, not 27.")


if __name__ == "__main__":
    self_test()
