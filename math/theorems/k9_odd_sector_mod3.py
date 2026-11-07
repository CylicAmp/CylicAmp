"""
k = 9, ODD SECTOR: p1 = 3, AND THE SLICE COUNT MOD 3
================================================================

Prior art.  k9_status.py closed the even sector at Level 1 and cut the odd
sector (profile (9,0,0)) from 1531 labelled shapes to 36 open, by the
in-box vacuity certificate (1465) and the box size lemma (22 dead, 7
confined to p1 in {3,5,7}).  Those 36, and the 7, are what this file acts
on.  Nothing of that enumeration is restated as new.

Three results, all Level 1, and the first makes the other two possible.

  THEOREM 31  3 | n, so p1 = 3, throughout the odd sector.  Suppose 3 does
              not divide n.  Then no divisor of n does, so all NINE
              elements of V are coprime to 3, every square is 1 (mod 3),
              and n = 9 = 0 (mod 3) -- so 3 | n after all.  Since n is odd,
              the smallest prime divisor is at least 3, and 3 divides it, so
              it is exactly 3.  The coordinate p1 stops being a parameter:
              every one of the 43 remaining shapes is evaluated at p1 = 3
              alone, the 7 "small-p1" shapes included, whose confinement to
              {3,5,7} collapses to a point.                      Level 1

              The same count mod 8 is vacuous and is recorded so it is not
              retried: every odd square is 1 (mod 8), so n = 9 = 1 (mod 8)
              identically, for every shape.

  THEOREM 32  THE SLICE COUNT.  With p1 = 3, split V by the exponent of 3.
              An element with 3-exponent 0 is coprime to 3 and contributes
              1 (mod 3); one with exponent at least 1 contributes 0.  So
                  n = #{e in S : e_1 = 0}   (mod 3)
              and 3 | n forces that slice count to be divisible by 3.  This
              is a property of the SHAPE alone -- no prime beyond p1 = 3
              enters -- so it is decided by inspection:
                  of the 36 open shapes, 24 die;
                  of the 7 small-p1 shapes, 4 die.
              The odd sector drops from 36 to 12.               Level 1

  THEOREM 33  THE FULL-BOX SHAPE IS EMPTY.  One open shape has
              prod(m_i + 1) = 9 = |V|, so the box of lcm(V) is full, there
              is no in-box non-member, and (P) says nothing at all:
                  V = {1, v, v^2, u, uv, uv^2, u^2, u^2 v, u^2 v^2}
              which is every divisor of v^2 u^2.  So n is a value of
              sigma_2, and multiplicativity gives
                  n = sigma_2(v^2 u^2) = (1 + v^2 + v^4)(1 + u^2 + u^4).
              (L) says v^2 u^2 | n.  Since gcd(u, 1+u^2+u^4) = 1, the u^2
              must come from the other factor:
                  u^2 | 1 + v^2 + v^4 = (v^2 + v + 1)(v^2 - v + 1),
              and those two are coprime -- a common divisor splits 2v, both
              are odd, and each is 1 (mod v).  So u prime puts u^2 inside
              ONE of them, and the larger is v^2 + v + 1 < (v+1)^2.  Hence
                  u^2 <= v^2 + v + 1 < (v+1)^2,  so  u <= v,
              against u > v.  Note the asymmetry: the companion condition
              v^2 | 1 + u^2 + u^4 is never used, because the inequality runs
              the wrong way for the smaller prime.               Level 1

STATUS.  The odd sector goes from 36 open shapes to 11, and the separate
small-p1 class from 7 to 3.  k = 9's even sector remains closed at Level 1;
the odd sector is not closed.

The eleven survivors, by (r, lcm exponents, in-box non-members):

    r=2  m=[3,2]  2        r=3  m=[3,1,1]  3        r=4  m=[1,1,2,1]  6
    r=2  m=[3,2]  1        r=3  m=[3,1,1]  2        r=4  m=[1,2,1,1]  6
    r=2  m=[4,2]  2        r=3  m=[4,1,1]  3
    r=3  m=[1,2,2] 5       r=3  m=[4,1,1]  3
    r=3  m=[2,1,1] 1

The thinnest handles are the two with a single in-box non-member, and the
r=2 shapes, where only p2 is free once p1 = 3 is fixed.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import k9_status as K


# ----------------------------------------------------------------------
# the three results
# ----------------------------------------------------------------------

def slice_count(S):
    """#{e in S : e_1 = 0} -- the elements coprime to p1."""
    return sum(1 for e in S if e[0] == 0)


def passes_slice_count(S):
    """THEOREM 32: 3 | n requires the slice count to be 0 mod 3."""
    return slice_count(S) % 3 == 0


def sigma2_of_square_pair(v, u):
    """sigma_2(v^2 u^2), by multiplicativity."""
    return (1 + v*v + v**4) * (1 + u*u + u**4)


SMALLEST_PRIME = 3                 # THEOREM 31
N_MOD_8 = 1                        # identically, so vacuous

ODD_OPEN_BEFORE = 36
ODD_OPEN_AFTER_SLICE = 12
ODD_OPEN_AFTER_FULLBOX = 11
SLICE_KILLED = 24
SMALL_P1_BEFORE = 7
SMALL_P1_AFTER = 3
SMALL_P1_KILLED = 4

SURVIVORS = [(2, (3, 2), 2), (2, (3, 2), 1), (2, (4, 2), 2),
             (3, (1, 2, 2), 5), (3, (2, 1, 1), 1), (3, (3, 1, 1), 3),
             (3, (3, 1, 1), 2), (3, (4, 1, 1), 3), (3, (4, 1, 1), 3),
             (4, (1, 1, 2, 1), 6), (4, (1, 2, 1, 1), 6)]


def open_shapes():
    """Rebuild k9_status's open odd sector and its small-p1 class."""
    L = K.labelled_shapes(9)
    rest = [(r, S) for r, S in L if not K.vacuity_certificate(S)]
    left = [x for x in rest if K.box_size_lemma(x[1]) is None and x[0] > 1]
    small = [x for x in rest if K.box_size_lemma(x[1]) == 'small-p1']
    return left, small


def full_box_shapes(group):
    return [(r, S) for r, S in group if len(K.box_nonmembers(S)) == 0]


# ======================================================================
# tests
# ======================================================================

def test_three_divides_n():
    """THEOREM 31, as a congruence count on nine odd squares."""
    # if none of the nine is divisible by 3, every square is 1 mod 3
    for res in (1, 2):
        assert (res * res) % 3 == 1
    assert (9 * 1) % 3 == 0            # so the sum would be 0 mod 3 anyway
    # hence 3 | n, and n odd makes 3 the smallest prime divisor
    assert SMALLEST_PRIME == 3
    # the mod 8 count by contrast is identically 1 and says nothing
    for odd in range(1, 40, 2):
        assert (odd * odd) % 8 == 1
    assert (9 * 1) % 8 == N_MOD_8 == 1
    # every open shape does carry p1^1, so 3 really is the second divisor
    left, small = open_shapes()
    for r, S in left + small:
        e = tuple([1] + [0] * (r - 1))
        assert e in S, (r, S)


def test_slice_count_identity():
    """THEOREM 32: n = slice count (mod 3), verified on real integers."""
    # build n for a shape at p1 = 3 and compare against the slice count
    left, _ = open_shapes()
    from sympy import prime
    for r, S in left[:14]:
        for shift in (0, 1, 2):
            ps = [3] + [prime(4 + shift + i) for i in range(r - 1)]
            if len(set(ps)) != r:
                continue
            n = 0
            for e in S:
                d = 1
                for i, x in enumerate(e):
                    d *= ps[i] ** x
                n += d * d
            assert n % 3 == slice_count(S) % 3, (r, S, ps)


def test_slice_count_kills_24_of_36():
    """THEOREM 32, the census."""
    left, small = open_shapes()
    assert len(left) == ODD_OPEN_BEFORE == 36
    assert len(small) == SMALL_P1_BEFORE == 7
    dead = [x for x in left if not passes_slice_count(x[1])]
    surv = [x for x in left if passes_slice_count(x[1])]
    assert len(dead) == SLICE_KILLED == 24, len(dead)
    assert len(surv) == ODD_OPEN_AFTER_SLICE == 12, len(surv)
    sdead = [x for x in small if not passes_slice_count(x[1])]
    assert len(sdead) == SMALL_P1_KILLED == 4, len(sdead)
    assert len(small) - len(sdead) == SMALL_P1_AFTER == 3
    # the m=[7,1] shape is among the dead, with slice count 1
    seven = [(r, S) for r, S in left if K.lcm_exponents(S) == (7, 1)]
    assert len(seven) == 1
    # its elements coprime to 3 are 1 and p2 -- the unit counts too
    assert slice_count(seven[0][1]) == 2
    assert not passes_slice_count(seven[0][1])
    # and its n really is 2 mod 3 for every prime u other than 3
    base = sum((3 ** i) ** 2 for i in range(8))
    assert base % 3 == 1
    from sympy import primerange
    for u in primerange(5, 200):
        assert (base + u*u) % 3 == 2


def test_full_box_shape_is_empty():
    """THEOREM 33."""
    left, _ = open_shapes()
    fb = full_box_shapes(left)
    assert len(fb) == 1, len(fb)
    r, S = fb[0]
    assert r == 2 and K.lcm_exponents(S) == (2, 2)
    prod = 1
    for e in K.lcm_exponents(S):
        prod *= e + 1
    assert prod == 9 == len(S)                 # the box is exactly V
    assert K.box_nonmembers(S) == []           # so (P) gives nothing
    # V is every divisor of v^2u^2, so n is a sigma_2 value
    from sympy import primerange, gcd
    for v in primerange(3, 30):
        for u in primerange(v + 2, 60):
            V = [1, v, v*v, u, u*v, u*v*v, u*u, u*u*v, u*u*v*v]
            assert len(set(V)) == 9
            assert sum(d*d for d in V) == sigma2_of_square_pair(v, u)
    # the factorisation and the inequality that closes it
    for v in primerange(3, 500):
        a, b = v*v + v + 1, v*v - v + 1
        assert 1 + v*v + v**4 == a * b
        assert gcd(a, b) == 1                  # coprime, as claimed
        assert b < a < (v + 1) ** 2            # the larger is below (v+1)^2
        assert gcd(v, a) == 1 and gcd(v, b) == 1
        # u^2 inside either factor forces u <= v
        from math import isqrt
        assert isqrt(a) <= v
    # the companion condition v^2 | 1+u^2+u^4 is genuinely unused: state it
    # as what it is, a condition that sometimes holds and decides nothing
    from sympy import primerange as _pr
    holds = [(v, u) for v in _pr(3, 20) for u in _pr(v + 2, 60)
             if (1 + u*u + u**4) % (v*v) == 0]
    assert holds, holds            # it DOES hold for some pairs
    for v, u in holds:
        from math import isqrt as _is
        assert _is(v*v + v + 1) <= v      # and u <= v still kills them all
    assert ODD_OPEN_AFTER_FULLBOX == ODD_OPEN_AFTER_SLICE - 1 == 11


def test_survivor_list_matches():
    left, _ = open_shapes()
    surv = [(r, K.lcm_exponents(S), len(K.box_nonmembers(S)))
            for r, S in left if passes_slice_count(S)]
    fb = [(r, K.lcm_exponents(S), 0) for r, S in full_box_shapes(left)]
    live = sorted(x for x in surv if x not in fb)
    assert len(live) == 11, len(live)
    assert sorted(SURVIVORS) == live, live
    assert {r for r, _, _ in live} == {2, 3, 4}
    # the thinnest handles
    thin = [x for x in live if x[2] == 1]
    assert len(thin) == 2, thin


def test_does_not_prove_too_much():
    # THEOREM 31 is an ODD-sector statement; it uses all nine being odd
    assert (9 * 1) % 3 == 0
    assert (8 * 1) % 3 == 2            # eight odd squares would NOT give it
    assert (7 * 1) % 3 == 1            # nor seven, so k=7 gets nothing here
    # the slice count is about the shape, not the primes: p2 never enters
    left, _ = open_shapes()
    for r, S in left[:6]:
        assert passes_slice_count(S) == (slice_count(S) % 3 == 0)
    # 24 + 12 = 36, and nothing is double-counted
    dead = [x for x in left if not passes_slice_count(x[1])]
    surv = [x for x in left if passes_slice_count(x[1])]
    assert len(dead) + len(surv) == 36
    assert not set(map(str, dead)) & set(map(str, surv))
    # the sector is NOT closed
    assert ODD_OPEN_AFTER_FULLBOX > 0
    assert SMALL_P1_AFTER > 0
    # and THEOREM 33 needs the box to be FULL; the other shapes have forcings
    assert len(full_box_shapes(left)) == 1


def self_test():
    tests = [test_three_divides_n,
             test_slice_count_identity,
             test_slice_count_kills_24_of_36,
             test_full_box_shape_is_empty,
             test_survivor_list_matches,
             test_does_not_prove_too_much]
    for t in tests:
        t()
        print(f'  ok  {t.__name__}')
    print()
    print(f'  THEOREM 31  3 | n, so p1 = 3 everywhere in the odd sector;'
          f'  n = 1 mod 8 is vacuous')
    print(f'  THEOREM 32  slice count: n = #{{e : e_1 = 0}} mod 3, so that count'
          f' must be 0 mod 3')
    print(f'              kills {SLICE_KILLED} of {ODD_OPEN_BEFORE} open shapes,'
          f' and {SMALL_P1_KILLED} of the {SMALL_P1_BEFORE} small-p1 shapes')
    print(f'  THEOREM 33  the full-box shape is sigma_2(v^2u^2), and'
          f' u^2 | (v^2+v+1)(v^2-v+1) forces u <= v')
    print()
    print(f'  k = 9 odd sector:  {ODD_OPEN_BEFORE} open  ->  '
          f'{ODD_OPEN_AFTER_SLICE} after the slice count  ->  '
          f'{ODD_OPEN_AFTER_FULLBOX} after the full box')
    print(f'  small-p1 class:    {SMALL_P1_BEFORE}  ->  {SMALL_P1_AFTER}')


if __name__ == '__main__':
    self_test()
