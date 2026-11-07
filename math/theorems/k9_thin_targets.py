"""
k = 9 ODD SECTOR: THE FOUR THINNEST SHAPES
================================================================

Prior art.  k9_odd_sector_mod3.py forced p1 = 3 throughout the odd sector,
cut 36 open shapes to 12 by the slice count, and closed the full-box one,
leaving 11.  Of those, the thinnest are the three with only TWO primes --
where p1 = 3 leaves a single free prime -- and the one r = 3 shape carrying
a single in-box forcing.  Those are four distinct shapes, not five: one of
the two single-forcing shapes is itself an r = 2 shape, so the earlier count
double-counted it.

All four close, by two mechanisms, both Level 1.

  THEOREM 34  r = 2 COLLAPSES TO A DIVISIBILITY BY A CONSTANT.  With p1 = 3
              the only free prime is u, and n splits by the exponent of u:
                  n = C0 + C1 u^2 + C2 u^4
              where C0 sums 9^a over the elements that are powers of 3
              alone -- a base-9 repunit (9^k - 1)/8, a NUMBER with no
              parameter in it.  Since lcm(V) = 3^m1 u^2 divides n and u
              divides neither C1 u^2 nor... more simply, u^2 | n and
              u^2 | C1u^2 + C2u^4, so
                  u^2 | C0.
              That bounds u by sqrt(C0) and in fact pins it to the odd
              prime squares dividing C0 -- a finite explicit list.
                m = [3,2], both shapes:  C0 = 820 = 2^2 * 5 * 41.
                  Squarefree away from 2, so NO odd prime square divides
                  it.  Both shapes are empty immediately.
                m = [4,2]:  C0 = 7381 = 11^2 * 61, so u = 11 is the one
                  candidate.  It gives n = 33033 = 3 * 7 * 11^2 * 13, with
                  v_3(n) = 1, while lcm(V) = 3^4 * 11^2 needs v_3(n) >= 4.
                  Empty.                                         Level 1

  THEOREM 35  THE r = 3, m = [2,1,1] SHAPE HAS A PRIME IT CANNOT PLACE.
              V = {1, 3, 9, p2, p3, 3p2, 3p3, 9p2, 9p3}, so max(V) = 9p3 and
              n factors completely:
                  n = (1 + 9 + 81)(1 + p2^2 + p3^2) = 91 (1 + p2^2 + p3^2),
              and 91 = 7 * 13.  So 7 | n for EVERY assignment.  The single
              in-box forcing is p2 p3 > max(V) = 9 p3, i.e. p2 > 9, so
              p2 >= 11 and p3 > p2.  Then 7 is not in V -- V's only primes
              are 3, p2, p3 and none is 7 -- so (P) demands 7 > max(V)
              = 9 p3 >= 117.  Contradiction.                     Level 1

A NEGATIVE RESULT, recorded so the mechanism is not retried.  THEOREM 35
works because n happens to factor with a constant carrying a small prime.
Taking the gcd of n over many prime assignments, for every one of the 11
surviving shapes, returns:
    r=3 m=[2,1,1]   gcd = 273 = 3 * 7 * 13      <- the shape above
    every other     gcd = 3
and 3 is already in V.  So the forced-prime argument closes exactly one
shape and nothing more; the remaining seven need different tools.

STATUS.  Odd sector 11 -> 7 open.  The even sector stays closed at Level 1.
The odd sector is NOT closed.

The seven that remain:
    r=3  m=[1,2,2]  5 forcings        r=3  m=[4,1,1]  3 forcings
    r=3  m=[3,1,1]  3 forcings        r=4  m=[1,1,2,1] 6 forcings
    r=3  m=[3,1,1]  2 forcings        r=4  m=[1,2,1,1] 6 forcings
    r=3  m=[4,1,1]  3 forcings
Every one has r >= 3, so at least two free primes, and none has a forced
prime factor beyond 3.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from math import gcd, isqrt
import k9_status as K


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------

def value(e, ps):
    d = 1
    for i, x in enumerate(e):
        d *= ps[i] ** x
    return d


def n_of(S, ps):
    return sum(value(e, ps) ** 2 for e in S)


def repunit9(k):
    """(9^k - 1)/8 = 1 + 9 + ... + 9^(k-1)."""
    return (9 ** k - 1) // 8


def u_coefficients(S):
    """For r = 2 at p1 = 3: (C0, C1, C2) with n = C0 + C1 u^2 + C2 u^4."""
    C = [0, 0, 0]
    for e in S:
        C[e[1]] += 9 ** e[0]
    return tuple(C)


def odd_prime_squares_dividing(N):
    """Odd primes u != 3 with u^2 | N."""
    out = []
    for u in range(5, isqrt(N) + 1, 2):
        if N % (u * u):
            continue
        p = True
        d = 3
        while d * d <= u:
            if u % d == 0:
                p = False
                break
            d += 2
        if p:
            out.append(u)
    return out


def forced_gcd(S, r, samples=40):
    """gcd of n over many prime assignments: a divisor of n for every one."""
    from sympy import primerange
    small = [p for p in primerange(5, 200)]
    g = 0
    used = 0
    for i in range(len(small) - r + 2):
        ps = [3] + small[i:i + r - 1]
        if len(ps) != r or len(set(ps)) != r:
            continue
        g = gcd(g, n_of(S, ps))
        used += 1
        if used >= samples:
            break
    return g


def open_eleven():
    """The 11 shapes k9_odd_sector_mod3.py leaves open."""
    L = K.labelled_shapes(9)
    rest = [(r, S) for r, S in L if not K.vacuity_certificate(S)]
    left = [x for x in rest if K.box_size_lemma(x[1]) is None and x[0] > 1]
    return [(r, S) for r, S in left
            if sum(1 for e in S if e[0] == 0) % 3 == 0
            and len(K.box_nonmembers(S)) > 0]


C0_32 = 820                       # (9^4-1)/8
C0_42 = 7381                      # (9^5-1)/8
ONLY_CANDIDATE_42 = 11
N_AT_11 = 33033
FORCED_GCD_211 = 273              # 3 * 7 * 13
OPEN_BEFORE = 11
OPEN_AFTER = 7
CLOSED_HERE = 4


# ======================================================================
# tests
# ======================================================================

def test_the_targets_are_four_not_five():
    eleven = open_eleven()
    assert len(eleven) == OPEN_BEFORE == 11
    two = [x for x in eleven if x[0] == 2]
    one_forcing = [x for x in eleven if len(K.box_nonmembers(x[1])) == 1]
    assert len(two) == 3
    assert len(one_forcing) == 2
    # the overlap is exactly one shape, so the union is four
    overlap = [x for x in one_forcing if x[0] == 2]
    assert len(overlap) == 1
    union = two + [x for x in one_forcing if x[0] != 2]
    assert len(union) == 4 == CLOSED_HERE


def test_r2_coefficient_split():
    """THEOREM 34: n = C0 + C1 u^2 + C2 u^4, and C0 is a base-9 repunit."""
    from sympy import primerange
    eleven = open_eleven()
    two = [x for x in eleven if x[0] == 2]
    for r, S in two:
        C0, C1, C2 = u_coefficients(S)
        for u in primerange(5, 120):
            assert n_of(S, [3, u]) == C0 + C1*u*u + C2*u**4, (S, u)
        # C0 counts the pure powers of 3 in V
        k = sum(1 for e in S if e[1] == 0)
        assert C0 == repunit9(k), (C0, k)
        assert C0 in (C0_32, C0_42)
    assert repunit9(4) == C0_32 == 820
    assert repunit9(5) == C0_42 == 7381


def test_r2_shapes_are_empty():
    """THEOREM 34, the three closures."""
    eleven = open_eleven()
    two = [x for x in eleven if x[0] == 2]
    assert len(two) == 3
    closed = 0
    for r, S in two:
        m = K.lcm_exponents(S)
        C0, C1, C2 = u_coefficients(S)
        cands = odd_prime_squares_dividing(C0)
        if not cands:
            assert C0 == 820                      # the two m=[3,2] shapes
            closed += 1
            continue
        assert C0 == 7381 and cands == [ONLY_CANDIDATE_42]
        for u in cands:
            n = C0 + C1*u*u + C2*u**4
            assert n == N_AT_11 == 33033
            need = 3 ** m[0] * u * u
            assert n % need != 0                  # lcm does not divide n
            # precisely: v_3(n) = 1 but lcm wants 3^4
            v3 = 0
            x = n
            while x % 3 == 0:
                x //= 3
                v3 += 1
            assert v3 == 1 < m[0] == 4
        closed += 1
    assert closed == 3
    # 820 really has no odd prime square factor
    assert 820 == 2*2*5*41
    assert odd_prime_squares_dividing(820) == []
    # and 7381 has exactly one
    assert 7381 == 11*11*61
    assert odd_prime_squares_dividing(7381) == [11]
    # the u^2 | C0 step: u^2 divides n and divides C1u^2 + C2u^4
    from sympy import primerange
    for r, S in two:
        C0, C1, C2 = u_coefficients(S)
        for u in primerange(5, 60):
            n = C0 + C1*u*u + C2*u**4
            assert (n - C0) % (u*u) == 0           # the tail is divisible
            assert (n % (u*u) == 0) == (C0 % (u*u) == 0)


def test_the_211_shape_is_empty():
    """THEOREM 35."""
    from sympy import primerange
    eleven = open_eleven()
    tgt = [(r, S) for r, S in eleven
           if r == 3 and K.lcm_exponents(S) == (2, 1, 1)
           and len(K.box_nonmembers(S)) == 1]
    assert len(tgt) == 1
    r, S = tgt[0]
    # n factors completely
    for p2 in primerange(5, 120):
        for p3 in primerange(p2 + 2, 200):
            assert n_of(S, [3, p2, p3]) == 91 * (1 + p2*p2 + p3*p3)
    assert 91 == 7 * 13
    assert repunit9(3) == 91
    # the single forcing is p2 p3 > max(V) = 9 p3, so p2 > 9
    f = K.box_nonmembers(S)[0]
    assert f == (0, 1, 1), f                       # it is p2 p3
    for p2 in primerange(11, 80):
        for p3 in primerange(p2 + 2, 150):
            V = [value(e, [3, p2, p3]) for e in S]
            assert max(V) == 9 * p3
            assert p2 * p3 > max(V)                # the forcing holds
            assert 7 not in V                      # 7 cannot sit in V
            assert 7 < max(V)                      # yet (P) demands 7 > max(V)
            assert n_of(S, [3, p2, p3]) % 7 == 0   # and 7 divides n
    # p2 = 7 is excluded by the forcing itself
    for p3 in primerange(11, 100):
        assert not 7 * p3 > 9 * p3                 # p2 = 7 fails p2 > 9


def test_forced_gcd_is_a_dead_end_elsewhere():
    """The negative result: only one shape has a usable forced prime."""
    eleven = open_eleven()
    table = {}
    for r, S in eleven:
        g = forced_gcd(S, r)
        table[(r, K.lcm_exponents(S), len(K.box_nonmembers(S)))] = g
    has273 = [k for k, g in table.items() if g == FORCED_GCD_211]
    assert len(has273) == 1
    assert has273[0] == (3, (2, 1, 1), 1)
    others = [g for k, g in table.items() if k != has273[0]]
    assert set(others) == {3}, set(others)
    # and 3 is in V for every shape, so it forces nothing
    for r, S in eleven:
        e = tuple([1] + [0] * (r - 1))
        assert e in S


def test_seven_remain():
    eleven = open_eleven()
    two = [x for x in eleven if x[0] == 2]
    tgt = [(r, S) for r, S in eleven
           if r == 3 and K.lcm_exponents(S) == (2, 1, 1)
           and len(K.box_nonmembers(S)) == 1]
    rest = [x for x in eleven if x not in two and x not in tgt]
    assert len(rest) == OPEN_AFTER == 7
    assert all(r >= 3 for r, _ in rest)            # at least two free primes
    assert {r for r, _ in rest} == {3, 4}
    assert OPEN_BEFORE - CLOSED_HERE == OPEN_AFTER


def test_does_not_prove_too_much():
    # THEOREM 34 needs r = 2; with r >= 3 the "constant" carries primes
    eleven = open_eleven()
    three = [x for x in eleven if x[0] == 3][0]
    r, S = three
    C = {}
    for e in S:
        C.setdefault(tuple(e[1:]), 0)
        C[tuple(e[1:])] += 9 ** e[0]
    assert len(C) > 3                              # not a single quartic in u
    # THEOREM 35 needs the forcing to push p2 past 7; without it p2 = 7 would
    # place the 7 inside V and the argument would fail
    from sympy import primerange as _pr
    for p3 in _pr(11, 100):
        assert not (7 * p3 > 9 * p3)               # p2 = 7 fails p2 > 9
        V7 = [1, 3, 9, 7, p3, 21, 3*p3, 63, 9*p3]
        assert 7 in V7                             # and then 7 IS in V,
        assert n_of([(0,0,0)], [3, 7, p3]) == 1    # so nothing is forced
    # and the sector is not closed
    assert OPEN_AFTER > 0
    # the repunit identity is base 9, not base 10
    assert repunit9(3) == 91 != 111


def self_test():
    tests = [test_the_targets_are_four_not_five,
             test_r2_coefficient_split,
             test_r2_shapes_are_empty,
             test_the_211_shape_is_empty,
             test_forced_gcd_is_a_dead_end_elsewhere,
             test_seven_remain,
             test_does_not_prove_too_much]
    for t in tests:
        t()
        print(f'  ok  {t.__name__}')
    print()
    print(f'  THEOREM 34  r=2 at p1=3: u^2 | C0, a base-9 repunit.')
    print(f'              C0 = {C0_32} = 2^2*5*41 for both m=[3,2] shapes: no odd')
    print(f'              prime square divides it, so both are empty at once.')
    print(f'              C0 = {C0_42} = 11^2*61 for m=[4,2]: only u = 11, giving')
    print(f'              n = {N_AT_11} with v_3 = 1 against the 3^4 lcm needs.')
    print(f'  THEOREM 35  m=[2,1,1]: n = 91(1+p2^2+p3^2), the forcing gives')
    print(f'              p2 >= 11, so 7 | n cannot sit in V nor exceed 9 p3.')
    print(f'  negative    forced gcd over all 11: {FORCED_GCD_211} for that one shape,')
    print(f'              3 for every other -- and 3 is already in V.')
    print()
    print(f'  k = 9 odd sector:  {OPEN_BEFORE} open  ->  {OPEN_AFTER} open')


if __name__ == '__main__':
    self_test()
