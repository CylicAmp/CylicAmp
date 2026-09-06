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


def ok(name):
    """Report a test whose work was done by bare asserts above it. The
    assert is the test; this only prints. Never use it to stand in for a
    condition — a printer that always passes is not a check."""
    print(f"  ok    {name}")


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


# ── invariants that later theorems depend on ─────────────────

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



# ── cyclotomic / decimal-period primitives (T301-T304) ─────────────────────

def test_cyclotomic():
    assert G.phi_d(1, 137) == 136
    assert G.phi_d(3, 137) == 18907 == 7 * 37 * 73
    assert G.phi_d(3, 10) == 111 == 3 * 37
    assert G.phi_d(6, 10) == 91 == 7 * 13
    assert G.phi_d(8, 10) == 10001 == 73 * 137
    for d in range(1, 13):                      # x^d-1 = prod_{e|d} Phi_e(x)
        prod = 1
        for e in range(1, d + 1):
            if d % e == 0:
                prod *= G.phi_d(e, 10)
        assert prod == 10 ** d - 1, d
    ok("cyclotomic values and the x^d-1 product identity")


def test_order_slot():
    assert G.order_slot(10, 3) == [37]          # the L3 singleton
    assert G.order_slot(137, 3) == [7, 37, 73]  # L1, complete
    assert G.order_slot(10, 6) == [7, 13]
    assert G.order_slot(10, 8) == [73, 137]
    # every prime in a slot really has that order; the p | d case is excluded
    for d in range(1, 10):
        for p in G.order_slot(10, d):
            assert G.order_mod(10, p) == d and d % p != 0
    ok("order slots: primes with ord_p(a) = d")


def test_period():
    assert G.period(37, 10) == (0, 3)           # 1/37 = 0.027027...
    assert G.period(137, 10) == (0, 8)
    assert G.period(7, 10) == (0, 6)
    assert G.period(8, 10) == (3, 0)            # terminates
    assert G.period(8, 2) == (3, 0)
    assert G.period(8, 100) == (2, 0)           # pre = ceil(v_2(8)/v_2(100))
    assert G.period(1, 10) == (0, 0)
    # the stated rule against the observed expansion
    from fractions import Fraction
    for base in (2, 3, 10, 12, 100):
        for d in range(1, 60):
            f = Fraction(1, d)
            seen, r, i = {}, f.numerator % f.denominator, 0
            while r not in seen and r != 0:
                seen[r] = i
                r = r * base % f.denominator
                i += 1
            obs = (i, 0) if r == 0 else (seen[r], i - seen[r])
            assert G.period(d, base) == obs, (d, base, G.period(d, base), obs)
    ok("period(n, base) matches the observed expansion, 5 bases x 59 n")


def test_repetend():
    assert G.repetend(1, 37, 10) == '027'
    assert G.repetend(1, 7, 10) == '142857'
    assert G.repetend(1, 17, 2) == '00001111'
    assert G.repetend(8, 17, 2) == '01111000'
    assert G.repetend(10, 33, 2) == '0100110110'
    assert len(G.repetend(1, 69, 2)) == 22
    assert G.repetend(1, 8, 10) == ''           # terminates
    # a repetend must reproduce its own number
    from fractions import Fraction
    for a, b, base in ((1, 37, 10), (1, 7, 10), (8, 17, 2), (10, 33, 2)):
        r = G.repetend(a, b, base)
        assert Fraction(int(r, base), base ** len(r) - 1) == Fraction(a, b)
    ok("repetends, and each reproduces its own fraction")


def test_complement_halves():
    assert G.complement_halves(1, 17, 2) is True     # 2^4 = -1 mod 17
    assert G.complement_halves(8, 17, 2) is True
    assert G.complement_halves(10, 33, 2) is True    # 2^5 = -1 mod 33
    assert G.complement_halves(1, 69, 2) is False    # 2^11 != -1 mod 69
    assert G.complement_halves(1, 37, 10) is False   # period 3, odd
    assert G.complement_halves(1, 37, 2) is True     # 2 is a primitive root
    assert G.complement_halves(1, 8, 2) is None      # terminates
    ok("complement-halves test tracks base^(L/2) = -1")


def test_lists():
    assert G.L1_ORD137 == [7, 37, 73]
    assert G.L2_CM == [5, 17, 37]
    assert G.L3_ORD10 == [37]
    assert G.lists_containing(37) == ['L1', 'L2', 'L3']
    assert G.lists_containing(73) == ['L1']
    assert G.lists_containing(5) == ['L2']
    assert G.lists_containing(11) == []
    # each list agrees with the computation it claims to record
    assert G.order_slot(137, 3) == G.L1_ORD137
    assert G.order_slot(10, 3) == G.L3_ORD10
    assert G.L2_CM == [n * n + 1 for n in (2, 4, 6)]
    ok("the three complete lists, and each matches its own derivation")


def test_factor_str():
    assert G.factor_str(111) == '3 x 37'
    assert G.factor_str(999) == '3^3 x 37'
    assert G.factor_str(18907) == '7 x 37 x 73'
    assert G.factor_str(1) == '1'
    ok("factor_str renders factorizations")


def test_guards_refuse_rather_than_hang():
    """Every unbounded search in this library must have a stated bound.

    Found by auditing 233, then 9999991, then 2^31-1: each hung in a
    different place — order_slot factoring a 112-digit Phi, repetend
    building a 1.6-million-digit string, order_mod looping toward n-1.
    A silent hang is worse than a stated refusal.
    """
    import time
    t0 = time.time()
    assert G.order_slot(10, 232) is None          # Phi_232(10) has 112 digits
    assert G.order_slot(10, 1666665) is None      # degree 622080
    assert G.order_slot(10, 3) == [37]            # small ones still work
    assert G.repetend(1, 9999991, 10) is None     # period 1666665
    assert G.repetend(1, 37, 10) == '027'
    assert G.order_mod(10, 2 ** 31 - 1, max_steps=10 ** 5) is None
    assert G.order_mod(2, 2 ** 31 - 1) == 31      # unbounded default is fine
    assert G.period(2 ** 31 - 1, 10)[1] == -1     # -1 = unknown, not 0
    assert G.period(2 ** 31 - 1, 2) == (0, 31)
    assert time.time() - t0 < 10, "a guard is not firing"
    ok("guards return None/-1 instead of hanging (233, 9999991, 2^31-1)")


def test_period_zero_vs_unknown():
    """0 means terminates, -1 means unknown. They must not be confused."""
    assert G.period(8, 10) == (3, 0)              # terminates
    assert G.period(37, 10) == (0, 3)
    assert G.period(2 ** 31 - 1, 10)[1] == -1     # unknown
    assert G.period(8, 10)[1] != G.period(2 ** 31 - 1, 10)[1]
    ok("period 0 (terminates) is distinct from -1 (unknown)")


def test_totient():
    assert G.totient(1666665) == 622080
    for n, t in ((1, 1), (2, 1), (12, 4), (37, 36), (1369, 37 * 36)):
        assert G.totient(n) == t, n
    ok("totient from the factorization")

if __name__ == '__main__':
    # every test defined in this module runs; an unregistered test is a
    # test that silently never ran, which is worse than no test.
    tests = [v for k, v in sorted(globals().items())
             if k.startswith('test_') and callable(v)]
    for t in tests:
        t()
    print()
    if FAILS:
        print(f"{len(FAILS)} FAILURES: {FAILS}")
        sys.exit(1)
    print("all gf37 tests passed")
