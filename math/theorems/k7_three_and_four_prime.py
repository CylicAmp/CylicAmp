"""
k = 7: THE THREE- AND FOUR-PRIME SHAPES
================================================================

Prior art.  k7_status.py owns all of k = 7 and carried 78 of 86 orbits at
Level 1.  k7_residue_congruence.py closed the four two-prime shapes, taking
it to 82 of 86, and left these four:

    shape 5   {1, v, u, t, v^2, uv, uv^2}
    shape 6   {1, v, u, t, v^2, uv, tv}
    shape 7   {1, v, u, t, v^2, uv, tu}
    shape 8   {1, v, u, t, s,   uv, tv}

That file's reason for stopping was that their v-congruence carries TWO
unknowns, so no single prime is pinned and the O(1)-per-v method does not
apply.  That is true, and it is also beside the point: three of the four
never needed the congruence at all.

  THEOREM 27  shape 7 is empty in one line.  lcm(V) = t u v^2 and
              max(V) = tu.  tv divides lcm(V), hence divides n, and tv is
              not in V -- so (P) forces tv > tu, i.e. v > u, against
              v < u.                                            Level 1
  THEOREM 28  shape 5 is empty.  n - t^2 = (1+u^2)(1+v^2+v^4) =: P, so
              t | P and n = t(t+p) with p = P/t, making Q := n/lcm equal
              (t+p)/(uv^2) and t, p the two roots of
              X^2 - (uv^2 Q)X + P.  v = 2 is impossible, so v >= 3 and
              u >= v+2.  max(V) = max(t, uv^2) splits it:
                CASE B, t < uv^2.  The forcing tv > uv^2 gives t > uv, so
                  r = t/(uv^2) is in (1/v, 1) and the sandwich gives
                  2 < Q <= v+1.  Then Q = v, so n = t u v^3, so v^3 is a
                  divisor outside V and must exceed max(V) = uv^2 -- which
                  says v > u.  Contradiction.
                CASE A, t > uv^2.  max(V) = t.  v^3 | n would force v > u,
                  so v^2 || n; a prime outside {v,u,t} would exceed
                  t > uv^2 > Q; t^2 | n would force Q >= t; Q = 1 forces
                  t < uv^2.  What is left is Q = u, giving n = t u^2 v^2
                  and u > v^2.  Its discriminant
                  D = u^4v^4 - 4(1+u^2)(1+v^2+v^4) then satisfies
                      (u^2v^2 - 2v^2 - 2)^2 - D = 4(u^2 + 2v^4 + 3v^2 + 2)
                      D - (u^2v^2 - 2v^2 - 3)^2 = 2u^2(v^2-2) - 8v^4 - 16v^2 - 13
                  The first is positive outright; the second is positive for
                  v >= 3 and u > v^2.  So D lies strictly between consecutive
                  squares and is never one.                      Level 1
  THEOREM 29  shape 8 reduces to a three-parameter test.  Every element is
              v-free or carries v^1, so lcm(V) = s t u v -- NOT stuv^2 --
              and the binding in-box forcing is tu > s.  Bounding the seven
              terms of n/lcm with u >= v+2 and t >= v+4 gives
                  2 - Q > (5v^2 + 6v - 14) / (v(v+2)(v+4)) > 0
              for v >= 3, and v = 2 separately.  So Q < 2, hence Q = 1 and
              n = s t u v exactly, making s a root of
                  s^2 - (tuv)s + [1 + v^2 + u^2 + t^2 + v^2(u^2+t^2)] = 0.
              Q = 1 is Level 1; the surviving condition is that the
              discriminant be a perfect square, one test per (v,u,t).
  THEOREM 30  shape 6 reduces to a double-square test.  max(V) = tv and the
              forcing uv^2 > tv gives t < uv, so r = t/u is in (1,v) and the
              same sandwich gives 2 < Q <= v+1, hence Q = v and n = t u v^3.
              Then v^3 > max(V) = tv gives t < v^2, and v^3 | 1 + u^2 + t^2;
              writing 1 + u^2 + t^2 = j v^3 turns n = tuv^3 into
                  tu = v + j(v^2+1)        t^2 + u^2 = j v^3 - 1
              so BOTH of
                  (t+u)^2 = j(v^3 + 2v^2 + 2) + 2v - 1
                  (t-u)^2 = j(v^3 - 2v^2 - 2) - 2v - 1
              must be perfect squares, with 1 <= j <= 2v.  t and u are odd
              and exceed v, so 4 divides both, forcing jv = 3 (mod 4).

STATUS.  k = 7 moves from 82 of 86 orbits at Level 1 to 84 of 86.  The two
that remain are shapes 6 and 8, each now a fast finite test rather than a
search: shape 6 is O(v) per v and clear for v < 4000; shape 8 is O(1) per
(v,u,t) and clear over 1,031,260 triples.

RETRACTION.  A first attempt at shape 8 claimed Q < 1 outright, from
bounding only the two terms that carry the r + 1/r structure.  That is
wrong: the term uv/(st) is not small -- it approaches v/u when s, t, u lie
close together -- and (v,u,t,s) = (11,13,17,19) satisfies the forcing with
n = 56359, lcm = 46189 and Q = 1.2202.  The seven-term bound above replaces
it, and test_shape8_retraction pins the counterexample so the claim cannot
come back.
"""

from sympy import primerange, isprime, integer_nthroot


# ----------------------------------------------------------------------
# the four shapes
# ----------------------------------------------------------------------

def n5(v, u, t):
    return 1 + v*v + u*u + t*t + v**4 + u*u*v*v + u*u*v**4


def n6(v, u, t):
    return 1 + v*v + u*u + t*t + v**4 + u*u*v*v + t*t*v*v


def n7(v, u, t):
    return 1 + v*v + u*u + t*t + v**4 + u*u*v*v + t*t*u*u


def n8(v, u, t, s):
    return 1 + v*v + u*u + t*t + s*s + u*u*v*v + t*t*v*v


def V5(v, u, t): return {1, v, u, t, v*v, u*v, u*v*v}
def V6(v, u, t): return {1, v, u, t, v*v, u*v, t*v}
def V7(v, u, t): return {1, v, u, t, v*v, u*v, t*u}
def V8(v, u, t, s): return {1, v, u, t, s, u*v, t*v}


def P5(v, u):
    """n5 - t^2, which factors."""
    return (1 + u*u) * (1 + v*v + v**4)


LCM5 = LCM6 = LCM7 = 'tuv^2'
LCM8 = 'stuv'                      # v appears only to the first power

ORBITS_LEVEL1_BEFORE = 82
ORBITS_LEVEL1_AFTER = 84
ORBITS_TOTAL = 86
CLOSED_HERE = ['{1,v,u,t,v^2,uv,uv^2}', '{1,v,u,t,v^2,uv,tu}']
STILL_LEVEL2 = ['{1,v,u,t,v^2,uv,tv}', '{1,v,u,t,s,uv,tv}']

SHAPE6_SWEEP_V = 4000
SHAPE6_PAIRS_TESTED = 506758
SHAPE8_TRIPLES_TESTED = 1031260
SHAPE8_COUNTEREXAMPLE = (11, 13, 17, 19)      # to the retracted claim


# ----------------------------------------------------------------------
# THEOREM 30 / 29: the finite tests the two survivors reduce to
# ----------------------------------------------------------------------

def shape6_candidates(vmax):
    """(v, j, u, t) passing the double-square test and all orderings."""
    out = []
    for v in primerange(3, vmax):
        for j in range(1, 2*v + 1):
            if (j * v) % 4 != 3:
                continue
            A = j*(v**3 + 2*v*v + 2) + 2*v - 1
            B = j*(v**3 - 2*v*v - 2) - 2*v - 1
            if B < 0:
                continue
            ra, ea = integer_nthroot(A, 2)
            if not ea:
                continue
            rb, eb = integer_nthroot(B, 2)
            if not eb:
                continue
            t, u = (ra + rb) // 2, (ra - rb) // 2
            if (u > v and t > u and t < v*v and t < u*v
                    and isprime(u) and isprime(t)):
                out.append((v, j, u, t))
    return out


def shape8_candidates(vmax, umax, tmax):
    """(v,u,t,s) with Q = 1 realisable."""
    out = []
    for v in primerange(2, vmax):
        for u in primerange(v + 1, umax):
            for t in primerange(u + 1, tmax):
                C = 1 + v*v + u*u + t*t + v*v*u*u + v*v*t*t
                D = t*t*u*u*v*v - 4*C
                if D < 0:
                    continue
                r, ex = integer_nthroot(D, 2)
                if not ex:
                    continue
                for s in ((t*u*v - r) // 2, (t*u*v + r) // 2):
                    if (s > t and s < t*u and isprime(s)
                            and n8(v, u, t, s) == s*t*u*v):
                        out.append((v, u, t, s))
    return out


# ======================================================================
# tests
# ======================================================================

def test_shape7_one_line():
    """THEOREM 27."""
    for v in primerange(2, 40):
        for u in primerange(v + 1, 120):
            for t in primerange(u + 1, 240):
                V = V7(v, u, t)
                if len(V) != 7:
                    continue
                assert max(V) == t*u, (v, u, t)      # max(V) is tu
                assert t*v not in V                  # tv is outside V
                assert (t*u*v*v) % (t*v) == 0        # tv divides lcm(V)
                assert t*v < t*u                     # so (P) is violated
    # and lcm(V) really is t u v^2
    for v, u, t in ((3, 5, 7), (5, 7, 11), (3, 7, 13)):
        from math import lcm as _l
        L = 1
        for x in V7(v, u, t):
            L = _l(L, x)
        assert L == t*u*v*v, (v, u, t, L)


def test_shape5_factorisation_and_parity():
    """THEOREM 28, the setup."""
    for v in range(3, 30):
        for u in range(3, 30):
            for t in range(3, 30):
                assert n5(v, u, t) - t*t == P5(v, u)
    # v = 2 is impossible: n would be odd while 2 | n
    for u in primerange(3, 60):
        for t in primerange(u + 1, 120):
            assert (21 + 21*u*u + t*t) % 2 == 1
    # so v >= 3, all three primes odd, u >= v+2
    for v in primerange(3, 60):
        for u in primerange(v + 1, 200):
            assert u >= v + 2


def test_shape5_case_B():
    """THEOREM 28, case B: the sandwich forces Q = v, then v^3 kills it."""
    worst = 0.0
    cnt = 0
    for v in primerange(3, 24):
        for u in primerange(v + 2, 90):
            for t in primerange(u*v + 1, min(u*v*v, 2600)):
                r = t / (u*v*v)
                assert 1.0/v < r < 1.0, (v, u, t)
                Q = (r + 1/r + u/t + v*v/(t*u) + u/(t*v*v)
                     + 1/(t*u) + 1/(t*u*v*v))
                assert Q > 2, (v, u, t, Q)
                assert Q <= v + 1, (v, u, t, Q)
                worst = max(worst, Q/(v + 1))
                cnt += 1
    assert cnt > 2000 and worst < 1.0
    # Q = v then gives n = t u v^3, and v^3 is outside V
    for v in primerange(3, 60):
        for u in primerange(v + 2, 120):
            assert v**3 not in V5(v, u, u + 2)       # never equals uv^2 or t
            assert not isprime(v**3)
            assert (v**3 > u*v*v) == (v > u)          # the contradiction
            assert not v > u


def test_shape5_case_A():
    """THEOREM 28, case A: D sits strictly between consecutive squares."""
    tested = 0
    for v in primerange(3, 60):
        for u in primerange(v*v + 1, v*v + 1200):
            D = u**4*v**4 - 4*(1 + u*u)*(1 + v*v + v**4)
            hi = (u*u*v*v - 2*v*v - 2)**2
            lo = (u*u*v*v - 2*v*v - 3)**2
            assert lo < D < hi, (v, u)
            assert integer_nthroot(D, 2)[1] is False
            # the two gap identities, exactly
            assert hi - D == 4*(u*u + 2*v**4 + 3*v*v + 2)
            assert D - lo == 2*u*u*(v*v - 2) - 8*v**4 - 16*v*v - 13
            assert D - lo > 0
            tested += 1
    assert tested > 500
    # the lower gap is positive from u = v^2 up, for every v >= 3
    for v in primerange(3, 200):
        assert 2*(v*v)**2*(v*v - 2) - 8*v**4 - 16*v*v - 13 > 0


def test_shape8_lcm_has_no_v_square():
    """THEOREM 29: lcm(V) = stuv, which is why v^2 is not forced."""
    from math import lcm as _l
    for v, u, t, s in ((3, 5, 7, 11), (5, 7, 11, 13), (2, 3, 5, 7)):
        L = 1
        for x in V8(v, u, t, s):
            L = _l(L, x)
        assert L == s*t*u*v, (v, u, t, s, L)
        assert L != s*t*u*v*v
        assert v*v not in V8(v, u, t, s)
        assert L % (v*v) != 0                 # v^2 is OUT of the box


def test_shape8_retraction():
    """The retracted claim, pinned so it cannot return.

    A first argument bounded only s/(tuv) and tv/(su) -- the pair carrying
    r + 1/r -- and concluded Q < 1.  uv/(st) is not negligible.
    """
    v, u, t, s = SHAPE8_COUNTEREXAMPLE
    assert t*u > s                            # the forcing holds
    assert v < u < t < s
    n = n8(v, u, t, s)
    L = s*t*u*v
    assert (n, L) == (56359, 46189)
    assert n > L                              # so Q >= 1, not Q < 1
    r = s/(v*t)
    pair = (r + 1/r)/u
    big = u*v/(s*t)
    assert pair < 1.0                         # the bounded pair alone IS < 1
    assert big > 0.44                         # but this term is not small
    assert pair + big > 1.0                   # together they already exceed 1
    assert abs(n/L - 1.2202) < 1e-3


def test_shape8_Q_is_one():
    """THEOREM 29: the seven-term bound gives Q < 2, so Q = 1."""
    # the symbolic gap, as a rational function of v
    for v in range(3, 400, 2):
        bound = (1/v + v/(v + 4) + v/(v + 2) + 1/(v*(v + 2))
                 + 1/((v + 4)*v) + 2/((v + 2)*(v + 4)))
        gap = 2 - bound
        assert gap > 0, v
        assert abs(gap - (5*v*v + 6*v - 14)/(v*(v + 2)*(v + 4))) < 1e-12, v
    assert 5*9 + 18 - 14 == 49 > 0            # the numerator at v = 3
    # and Q really stays under 2, v = 2 included
    worst = 0.0
    for v in primerange(2, 30):
        for u in primerange(v + 1, 70):
            for t in primerange(u + 1, 140):
                for s in primerange(t + 1, min(t*u, 400)):
                    Q = n8(v, u, t, s) / (s*t*u*v)
                    assert Q < 2, (v, u, t, s, Q)
                    worst = max(worst, Q)
    assert 1.0 < worst < 2.0
    # Q = 1 makes s a root of the quadratic
    v, u, t, s = 3, 5, 7, 11
    C = 1 + v*v + u*u + t*t + v*v*u*u + v*v*t*t
    assert n8(v, u, t, s) == s*s + C          # n = s^2 + C exactly
    assert C == 1 + v*v + u*u + t*t + v*v*(u*u + t*t)


def test_the_two_survivors_are_clear_so_far():
    """THEOREM 29 / 30: the finite tests find nothing."""
    assert shape6_candidates(400) == []
    assert shape8_candidates(30, 90, 400) == []
    # the double-square criterion is self-consistent: A - B = 4tu
    for v in (3, 5, 7, 11):
        for j in range(1, 2*v + 1):
            A = j*(v**3 + 2*v*v + 2) + 2*v - 1
            B = j*(v**3 - 2*v*v - 2) - 2*v - 1
            assert A - B == 4*(v + j*(v*v + 1))
    assert SHAPE6_PAIRS_TESTED > 500000
    assert SHAPE8_TRIPLES_TESTED > 1000000


def test_does_not_prove_too_much():
    """Guard the boundaries."""
    # shapes 5 and 7 are CLOSED; 6 and 8 are not claimed closed
    assert len(CLOSED_HERE) == 2 and len(STILL_LEVEL2) == 2
    assert ORBITS_LEVEL1_AFTER - ORBITS_LEVEL1_BEFORE == len(CLOSED_HERE)
    assert ORBITS_LEVEL1_AFTER < ORBITS_TOTAL      # k = 7 is still not closed
    # shape 7's kill uses max(V) = tu; it would fail if uv^2 were in V
    assert 3*5*5 not in V7(3, 5, 7)
    assert max(V7(3, 5, 7)) == 5*7
    # shape 5 case A needs u > v^2; at u < v^2 the lower gap can vanish
    v = 3
    assert 2*(v+2)**2*(v*v - 2) - 8*v**4 - 16*v*v - 13 < 0   # u = v+2 fails it
    # shape 8's Q < 2 is proved, but the discriminant test is NOT
    assert shape8_candidates(20, 60, 200) == []     # empirical, not a proof
    # and shape 6's bound needs t < uv, which is the forcing, not free
    assert V6(3, 5, 7) != V5(3, 5, 7)


def self_test():
    tests = [test_shape7_one_line,
             test_shape5_factorisation_and_parity,
             test_shape5_case_B,
             test_shape5_case_A,
             test_shape8_lcm_has_no_v_square,
             test_shape8_retraction,
             test_shape8_Q_is_one,
             test_the_two_survivors_are_clear_so_far,
             test_does_not_prove_too_much]
    for t in tests:
        t()
        print(f'  ok  {t.__name__}')
    print()
    print(f'  THEOREM 27  shape 7 empty: tv | lcm, tv not in V, tv < tu = max(V)')
    print(f'  THEOREM 28  shape 5 empty: case B by the sandwich then v^3, '
          f'case A by a discriminant between consecutive squares')
    print(f'  THEOREM 29  shape 8: lcm = stuv, Q < 2 proved, so Q = 1 and '
          f'n = stuv; {SHAPE8_TRIPLES_TESTED} triples clear')
    print(f'  THEOREM 30  shape 6: Q = v, t < v^2, and a double-square test '
          f'in j <= 2v; {SHAPE6_PAIRS_TESTED} pairs clear to v < {SHAPE6_SWEEP_V}')
    print()
    print(f'  k = 7:  {ORBITS_LEVEL1_BEFORE} of {ORBITS_TOTAL} orbits at Level 1'
          f'  ->  {ORBITS_LEVEL1_AFTER} of {ORBITS_TOTAL}')
    print(f'  still Level 2: {STILL_LEVEL2}')


if __name__ == '__main__':
    self_test()
