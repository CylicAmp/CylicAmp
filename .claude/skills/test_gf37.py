#!/usr/bin/env python3
"""
Regression tests for the shared gf37 library.

Written after two bugs of the same shape were found in consecutive turns
by feeding in a single negative number:

    dr(-8)     returned 8   (abs applied, disagreed with -8 = 1 mod 9)
    factor(-8) returned {2:3}  (product 8, not -8)

Both were silent abs(). The rule these tests enforce: a function must not
return something that disagrees with its input, and it must refuse rather
than guess when the input is outside its domain.

    python3 test_gf37.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gf37 as G

FAILS = []


def check(name, cond, detail=''):
    if cond:
        print(f"  ok    {name}")
    else:
        print(f"  FAIL  {name}   {detail}")
        FAILS.append(name)


# ── domain discipline: the two bugs that motivated this file ────────────

def test_dr_domain():
    print("dr / mod9 domain")
    try:
        G.dr(-8)
        check("dr rejects negatives", False, "did not raise")
    except ValueError as e:
        check("dr rejects negatives", "mod9" in str(e),
              "error message should name mod9 as the alternative")
    check("mod9 accepts signed", G.mod9(-8) == 1 and G.mod9(8) == 8)
    check("dr matches formula on 0..1999",
          all(G.dr(n) == (9 if n and n % 9 == 0 else n % 9)
              for n in range(2000)))
    check("dr(0)=0, dr(9)=9, dr(37)=1",
          (G.dr(0), G.dr(9), G.dr(37)) == (0, 9, 1))


def test_factor_roundtrip():
    print("factor round-trip")
    bad = [n for n in list(range(-500, 0)) + list(range(1, 500))
           if G.factor_product(G.factor(n)) != n]
    check("factor(n) multiplies back to n over -500..499", bad == [], f"{bad[:5]}")
    check("factor(-8) carries the sign", G.factor(-8) == {-1: 1, 2: 3})
    check("factor(8) has no -1 key", -1 not in G.factor(8))
    try:
        G.factor(0)
        check("factor(0) raises", False, "did not raise")
    except ValueError:
        check("factor(0) raises", True)


def test_return_types():
    """dr_basin returns a NAME. Misread once as a repeated DR."""
    print("return types")
    check("dr_basin returns a string",
          all(isinstance(G.dr_basin(n), str) for n in (1, 3, 5, 246, 137)))
    check("basin names are the three expected",
          {G.dr_basin(n) for n in range(1, 200)} ==
          {'Trinity', 'Basin', 'Valve'})
    check("known basins",
          [(n, G.dr(n), G.dr_basin(n)) for n in (1, 3, 5, 246, 137)] ==
          [(1, 1, 'Basin'), (3, 3, 'Trinity'), (5, 5, 'Valve'),
           (246, 3, 'Trinity'), (137, 2, 'Valve')])


# ── framework invariants that later theorems depend on ─────────────────

def test_orbits():
    print("orbit structure")
    allelems = set().union(*G.ORBITS.values())
    check("12 orbits partition the 36 nonzero residues",
          len(G.ORBITS) == 12 and allelems == set(range(1, 37)))
    check("every orbit has size 3", all(len(s) == 3 for s in G.ORBITS.values()))
    check("orbit(x) = {x,10x,100x}  (T302)",
          all({min(s) % 37, (10 * min(s)) % 37, (100 * min(s)) % 37} == s
              for s in G.ORBITS.values()))
    check("137 = 26 = 10^2 mod 37", 137 % 37 == 26 == pow(10, 2, 37))
    check("ord_37(10) = 3", G.order_mod(10, 37) == 3)
    check("SEAM for multiples of 37",
          all(G.orbit(37 * k) == 'SEAM' for k in range(1, 30)))


def test_antipodal():
    print("antipodal structure")
    check("6 pairs, all distinct orbits", len(G.ANTIPODAL) == 6 and
          len({o for p in G.ANTIPODAL for o in p}) == 12)
    check("antipode is negation",
          all(G.orbit(-x) == G.antipode(G.orbit(x)) for x in range(1, 37)))
    check("antipode is an involution",
          all(G.antipode(G.antipode(o)) == o for o in G.ORBITS))
    check("class distance is always 6",
          all((G.cls(min(G.ORBITS[b])) - G.cls(min(G.ORBITS[a]))) % 12 == 6
              for a, b in G.ANTIPODAL))


def test_blocks():
    print("decimal blocks (T302/T303)")
    check("block(k) = 27k for all k",
          all(G.block(k) == f"{27*k:03d}" for k in range(1, 37)))
    check("block depends only on k mod 37",
          all(G.block(k) == G.block(k % 37) for k in range(1, 400)))
    check("antipodal blocks sum to 999",
          all(int(G.block(k)) + int(G.block(-k)) == 999 for k in range(1, 37)))
    # T303: x27 cycles are the cosets of <11>
    seen, cycles = set(), []
    for s in range(1, 37):
        if s in seen:
            continue
        c, x = [s], (27 * s) % 37
        while x != s:
            c.append(x)
            x = (27 * x) % 37
        seen |= set(c)
        cycles.append(sorted(c))
    og = {1, 10, 11, 26, 27, 36}
    cos, cov = [], set()
    for a in range(1, 37):
        if a in cov:
            continue
        s = sorted({(a * g) % 37 for g in og})
        cos.append(s)
        cov |= set(s)
    check("block-map cycles are the cosets of <11> (T303)",
          sorted(cycles) == sorted(cos))


def test_homomorphisms():
    print("homomorphisms (the forced facts)")
    check("class is a homomorphism to Z/12Z (T285)",
          all((G.cls(a) + G.cls(b)) % 12 == G.cls(a * b)
              for a in range(1, 37) for b in range(1, 37)))
    check("DR is a homomorphism to Z/9Z",
          all(G.dr(G.dr(a) * G.dr(b)) == G.dr(a * b)
              for a in range(1, 200) for b in range(1, 50)))


def test_primes():
    print("prime profile")
    p = G.prime_profile(5)
    check("5 is SG and safe", p['sophie_germain'] and p['safe'])
    check("13 is not SG (2*13+1 = 27)",
          not G.prime_profile(13)['sophie_germain'])
    check("11 twin/cousin/sexy all true",
          all(G.prime_profile(11)[k] for k in ('twin', 'cousin', 'sexy')))
    check("negatives are not prime", not G.is_prime(-7))


if __name__ == '__main__':
    for t in (test_dr_domain, test_factor_roundtrip, test_return_types,
              test_orbits, test_antipodal, test_blocks,
              test_homomorphisms, test_primes):
        t()
    print()
    if FAILS:
        print(f"{len(FAILS)} FAILURES: {FAILS}")
        sys.exit(1)
    print("all gf37 tests passed")
