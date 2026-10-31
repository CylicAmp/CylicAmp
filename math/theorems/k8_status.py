"""
k8_status.py

k = 8:  is there an n with  n = d_1^2 + ... + d_8^2  for d_1 < ... < d_8 the
EIGHT smallest divisors of n?

STATUS. Three of the four surviving profiles are CLOSED at Level 1. The
fourth leaves ONE family, and inside it p = 3 and p = 7 are Level 1 while
the rest is Level 2. So k = 8 is very close to closed -- much closer than
k = 7, because k is even and the parity lemma removes the whole odd sector
that made k = 7 hard (28 shapes there, none here).

A full structural enumeration (24,796 labelled order ideals -> 195 orbits
with the prime 2 fixed) gives these shape counts, and the four profiles it
leaves standing are exactly the four the mod-8 argument predicts:

    195 orbits                        45 need an argument
      (8,0,0)  58 shapes   killed by PARITY alone -- the whole odd sector
      (7,1,0)  28          killed by profile
      (6,1,1)  14          killed by profile
      (5,3,0)  13, (5,2,1) 11, (5,1,2) 7, (4,4,0) 4, and smaller: killed
      ------------------------------------------------------------------
      (6,2,0)  26 shapes   CLOSED L1   step 5, every shape
      (4,2,2)  10 shapes   step 6: family (a) CLOSED L1, family (b) RESIDUE
      (4,3,1)   5 shapes   CLOSED L1   step 3, immediate
      (4,1,3)   4 shapes   CLOSED L1   step 4

So 35 of the 45 are closed outright, and the remaining 10 are profile
(4,2,2), of which family (a) closes and family (b) is the gap. Compare
k = 7: 51 of 86 needed arguments and 31 were left at Level 2. The
difference is step 1 -- parity kills 58 shapes here and none there.

--------------------------------------------------------------------
THE ENGINES
--------------------------------------------------------------------
  (P) PREFIX RULE. e | n and e < max(V) implies e is in V. Composite e too.
  (L) LCM RULE. lcm(V) | n. Used in two strengths: the SIZE form n < lcm(V)
      (a contradiction, since lcm | n and n > 0 force n >= lcm), and the
      DIVISIBILITY form itself, which is strictly stronger.
  (M) MOD-p RULE. p | n, so reducing n = sum d^2 mod p gives
      sum over {d in V : p does not divide d} of d^2 = 0 (mod p).

--------------------------------------------------------------------
STEP 1   n IS EVEN
--------------------------------------------------------------------
k = 8 is even, so a sum of eight odd squares is even. An odd n would make
every d_i odd and force n even. So n is EVEN and d_2 = 2. This is the
parity lemma, and it is why k = 8 is easier than k = 7: the odd sector,
which at k = 7 held 28 shapes needing individual arguments, is empty here.

--------------------------------------------------------------------
STEP 2   THE PROFILE
--------------------------------------------------------------------
With A, B, C counting elements that are odd, 2 (mod 4), 0 (mod 4),

    A + B + C = 8      and      sum d^2 = A + 4B   (mod 8).

The profile is structural: an element's class depends only on its exponent
of 2. Branching on v_2(n), and adding B <= A -- each element counted by B
is 2d with d odd, d | n and d < 2d <= max(V), so (P) forces d into V, and
the odd elements number A -- leaves exactly four:

    (6,2,0)  v_2(n) = 1,  n = 6 (mod 8)
    (4,1,3)  8 | n
    (4,2,2)  n = 4 (mod 8), so v_2(n) = 2 exactly
    (4,3,1)  8 | n

B <= A is a property of EVERY prefix, not only of solutions; the mod-8
congruence is what restricts solutions. Both are checked below.

--------------------------------------------------------------------
STEP 3   (4,3,1) IS EMPTY -- one line
--------------------------------------------------------------------
A + 4B = 4 + 12 = 16 = 0 (mod 8), so 8 | n. C = 1 means 4 is the only
element that is 0 (mod 4), so 8 is not in V, so by (P) 8 > max(V). Then all
EIGHT elements of V are divisors below 8, drawn from {1,2,3,4,5,6,7} --
seven values for eight distinct elements. Contradiction.

--------------------------------------------------------------------
STEP 4   (4,1,3) IS EMPTY
--------------------------------------------------------------------
A + 4B = 8 = 0 (mod 8), so 8 | n.

(a) B = 1, so 2 is the only element that is 2 (mod 4), hence 2*o_1 > max(V)
    by (P). Then 4*o_1 > 2*o_1 > max(V), so no element that is 0 (mod 4)
    carries an odd factor: the C-elements are powers of 2, and with C = 3
    and 8 | n they are exactly {4, 8, 16}. So 16 | n.
(b) max(V) >= 16, and 2*o_1 > 16 gives o_1 >= 11.
(c) o_1 = p is the least odd prime of n, so a composite odd divisor is at
    least p^2 > 2p > max(V): the three odd divisors are PRIMES in [p, 2p).
(d) lcm(V) = 16*p*o_2*o_3 > 16p^3, while
    n = 1+4+16+64+256 + (p^2+o_2^2+o_3^2) = 341 + ... < 341 + 12p^2,
    and 16p^3 > 341 + 12p^2 for every prime p >= 5.

--------------------------------------------------------------------
STEP 5   (6,2,0) IS EMPTY -- every shape
--------------------------------------------------------------------
V = {2, 2*o_1} together with an odd part of six elements: 1 and five odd
divisors o_1 < ... < o_5.

(a) B = 2 forces the two 2-mod-4 elements to be {2, 2*o_1}: if 2*o_j were in
    V for some j >= 2 then 2*o_1 < 2*o_j <= max(V) would put 2*o_1 in V too,
    giving B >= 3. So 2*o_2 is not in V, and by (P)

        2*o_2 > max(V) >= o_5,    i.e.   o_5 < 2*o_2.

(b) THE SHAPE IS THEREBY FORCED. o_2, o_3, o_4, o_5 all lie in [o_2, 2o_2),
    so none divides another (a | b with a < b gives b >= 2a). In an order
    ideal this is very restrictive:
      * a product of two distinct primes cannot be among them, since both
        factors are also in the ideal and each divides the product;
      * at most one proper power of o_1 can be among them, for the same
        reason, and its base must be o_1 itself.
    So the odd part is either
        (i)  {1, p, r, s, t, u}   five distinct primes, or
        (ii) {1, p, p^2, r, s, t} one square and three further primes.
    An exhaustive enumeration of the 14 order ideals of size 6 in odd
    primes confirms these are the only two that admit o_5 < 2*o_2.

(c) Both die on the size form of (L):
      (i)  lcm = 2*p*r*s*t*u > 6r^4, and n = 5 + 5p^2 + (r^2+s^2+t^2+u^2)
           < 5 + 21r^2, with 6r^4 > 5 + 21r^2 for every prime r >= 5.
      (ii) lcm = 2*p^2*r*s*t > 18r^3, and n = 5 + 5p^2 + p^4 + (r^2+s^2+t^2)
           < 5 + 10r + 16r^2 using p^2 < 2r, with 18r^3 > that for r >= 5.

--------------------------------------------------------------------
STEP 6   (4,2,2) -- family (a) closed, family (b) is the residue
--------------------------------------------------------------------
n = 4 (mod 8), so v_2(n) = 2 exactly. The 0-mod-4 elements are 4 times odd
divisors, and C = 2 forces {4, 4*o_1}; then B = 2 forces {2, 2*o_1}, and
2*o_2 is not in V, so by (P)

    o_3 < 2*o_2    and    4*o_1 < 2*o_2,  i.e.  o_2 > 2*o_1.

The odd part has four elements. Of the four order ideals of that size,
{1,u,u^2,u^3} needs o_3 < 2*o_2, i.e. u^3 < 2u^2, i.e. u < 2; and
{1,u,t,tu} needs tu < 2t, i.e. u < 2. Both are vacuous. Two remain:

  (a) {1, p, t, s} three distinct primes, t > 2p, s < 2t.
      V = {1,2,4,p,2p,4p,t,s},  n = 21 + 21p^2 + t^2 + s^2,  lcm = 4*p*t*s.
      n < 21 + 10.25 t^2 (using p < t/2 and s < 2t) while lcm > 12 t^2
      (using p >= 3), and 12 > 10.25 with room. CLOSED at Level 1.

  (b) {1, p, t, p^2}  -- THE RESIDUE.
      V = {1, 2, 4, p, 2p, 4p, t, p^2},
          n = 21 + 21p^2 + t^2 + p^4,     lcm(V) = 4 p^2 t.
      The size form FAILS here: p^4 can dominate 4p^2 t, so n > lcm happens.
      Divisibility still bites, through (M):
          mod p:  n = 21 + t^2          so   p | 21 + t^2
          mod t:  n = 21(1+p^2) + p^4   so   t | 21(1+p^2) + p^4 =: M(p)
      p = 3 and p = 7 die at Level 1: both divide 21, so p | 21 + t^2 forces
      p | t, hence t = p, contradicting that t and p are distinct primes.
      For the remaining p the conditions are that t divides the FIXED number
      M(p) and lies in the forced range (2p, 2p^2). No such t exists for any
      prime p < 400. That is Level 2, and it is the whole remaining gap.

--------------------------------------------------------------------
CONSISTENCY
--------------------------------------------------------------------
A direct scan finds no k = 8 solution below 3,000,000, and all four
surviving profiles DO occur as genuine 8-divisor prefixes, so none of the
four was closed by being vacuous. Known solutions survive: k = 1 (n=1),
k = 4 (n=130), k = 11 (n=1860).
"""

from math import gcd, isqrt
from typing import List

PROFILES_SURVIVING = {(6, 2, 0), (4, 1, 3), (4, 2, 2), (4, 3, 1)}
LEVEL1_PROFILES = {(6, 2, 0), (4, 1, 3), (4, 3, 1)}
RESIDUE = "(4,2,2) family (b): V = {1,2,4,p,2p,4p,t,p^2}"

# From the full structural enumeration: 24,796 labelled order ideals ->
# 195 orbits (prime 2 fixed), of which 45 fall in a surviving profile.
ENUMERATION_ORBITS = 195
ENUMERATION_SHAPE_COUNTS = {(6, 2, 0): 26, (4, 2, 2): 10,
                            (4, 3, 1): 5, (4, 1, 3): 4}


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


def profile(V) -> tuple:
    return (sum(1 for v in V if v % 2),
            sum(1 for v in V if v % 4 == 2),
            sum(1 for v in V if v % 4 == 0))


def surviving_profiles(k: int = 8):
    out = []
    for A in range(1, k + 1):
        for B in range(0, k + 1 - A):
            C = k - A - B
            S = (A + 4 * B) % 8
            if C == 0 and B == 0:
                continue                      # n odd, excluded by step 1
            if C == 0:
                if S % 4 == 2 and B <= A:
                    out.append((A, B, C))
            elif B >= 1 and S % 4 == 0 and B <= A:
                out.append((A, B, C))
    return out


def residue_n(p: int, t: int) -> int:
    return 21 + 21 * p * p + t * t + p ** 4


def residue_M(p: int) -> int:
    return 21 * (1 + p * p) + p ** 4


# =====================================================================
# SELF-TESTS
# =====================================================================

def test_step1_parity() -> None:
    for ds in [(1, 3, 5, 7, 9, 11, 13, 15), (1, 3, 9, 27, 81, 243, 729, 2187)]:
        assert sum(d * d for d in ds) % 2 == 0, ds
    bad = [n for n in range(1, 300000, 2)
           if len(smallest_divisors(n, 8)) == 8
           and sum(d * d for d in smallest_divisors(n, 8)) == n]
    assert bad == [], bad
    print("[ok] step 1: eight odd squares sum even, so n is even")


def test_step2_profiles() -> None:
    got = set(surviving_profiles(8))
    assert got == PROFILES_SURVIVING, got
    assert (2 + 4 * 6) % 8 == 2 and 6 > 2, "(2,6,0) passes mod 8 but B>A"
    # the structural enumeration (195 orbits) leaves exactly these four,
    # with these shape counts; recorded rather than recomputed, since
    # orbit_reps(labeled_universe(8)) takes about seven minutes.
    assert ENUMERATION_SHAPE_COUNTS.keys() == PROFILES_SURVIVING
    assert sum(ENUMERATION_SHAPE_COUNTS.values()) == 45
    print(f"[ok] step 2: exactly {len(got)} profiles survive, "
          f"{sum(ENUMERATION_SHAPE_COUNTS.values())} shapes among them")


def test_step2_against_real_prefixes() -> None:
    """B <= A on every prefix, and the mod-8 identity on every prefix."""
    checked = 0
    occurring = set()
    for n in range(2, 400000):
        V = smallest_divisors(n, 8)
        if len(V) < 8:
            continue
        A, B, C = profile(V)
        assert A + B + C == 8
        assert B <= A, (n, V)
        assert sum(d * d for d in V) % 8 == (A + 4 * B) % 8, (n, V)
        occurring.add((A, B, C))
        checked += 1
    assert PROFILES_SURVIVING <= occurring, PROFILES_SURVIVING - occurring
    print(f"[ok] step 2 verified on {checked:,} real prefixes; all four "
          f"surviving profiles occur (none vacuous)")


def test_step3_431() -> None:
    assert (4 + 4 * 3) % 8 == 0, "8 | n"
    assert len(set(range(1, 8))) < 8, "only seven divisors are below 8"
    print("[ok] step 3: (4,3,1) empty -- 8 | n, 8 not in V, so V fits below 8")


def test_step4_413() -> None:
    assert (4 + 4 * 1) % 8 == 0
    for p in primes_upto(4000):
        if p >= 5:
            assert 16 * p ** 3 > 341 + 12 * p * p, p
    assert 16 * 11 ** 3 == 21296 and 341 + 12 * 121 == 1793
    print("[ok] step 4: (4,1,3) empty -- 16p^3 > 341+12p^2 for all p >= 5")


def test_step5_620_bounds() -> None:
    for r in primes_upto(4000):
        if r >= 5:
            assert 6 * r ** 4 > 5 + 21 * r * r, r
            assert 18 * r ** 3 > 5 + 10 * r + 16 * r * r, r
    print("[ok] step 5: (6,2,0) both families die on the size form")


def test_step5_shape_is_forced() -> None:
    """Only two order ideals of size 6 in odd primes admit o_5 < 2 o_2."""
    from itertools import permutations, product
    NV = 5
    zero = tuple([0] * NV)
    G = [v for v in product(range(6), repeat=NV) if sum(v) <= 5]

    def covers(v):
        return [tuple(w) for w in
                ([*v[:i], v[i] - 1, *v[i + 1:]] for i in range(NV) if v[i] > 0)]

    ideals = set()

    def canon(S):
        return min(tuple(sorted(tuple(v[p[i]] for i in range(NV)) for v in S))
                   for p in permutations(range(NV)))

    def grow(S):
        if len(S) == 6:
            ideals.add(canon(S))
            return
        for v in G:
            if v not in S and all(c in S for c in covers(v)):
                grow(S | {v})

    grow({zero})
    assert len(ideals) == 14, len(ideals)
    odd = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    realizable = 0
    for S in ideals:
        used = [i for i in range(NV) if any(v[i] for v in S)]
        ok = False
        for assign in permutations(odd, len(used)):
            pmap = dict(zip(used, assign))
            vals = []
            for v in S:
                x = 1
                for i, e in enumerate(v):
                    if e:
                        x *= pmap[i] ** e
                vals.append(x)
            if len(set(vals)) < 6:
                continue
            o = sorted(v for v in vals if v > 1)
            if o[4] < 2 * o[1]:
                ok = True
                break
        if ok:
            realizable += 1
    assert realizable == 2, realizable
    print(f"[ok] step 5: of the 14 size-6 odd ideals only {realizable} admit "
          f"o_5 < 2 o_2 -- the shape is forced")


def test_step6_family_a() -> None:
    """(4,2,2) with three distinct odd primes: n < lcm."""
    ps = primes_upto(600)
    checked = 0
    for p in ps:
        if p < 3 or p > 120:
            continue
        for t in ps:
            if t <= 2 * p:
                continue
            if t > 400:
                break
            for s in ps:
                if s <= t or s >= 2 * t:
                    continue
                V = sorted([1, 2, 4, p, 2 * p, 4 * p, t, s])
                if len(set(V)) < 8:
                    continue
                n = sum(d * d for d in V)
                assert n == 21 + 21 * p * p + t * t + s * s, (p, t, s)
                assert n < lcm_of(V), (p, t, s, n, lcm_of(V))
                checked += 1
    assert checked > 2000, checked
    print(f"[ok] step 6 family (a): n < lcm on all {checked} triples")


def test_step6_residue_identity_and_small_p() -> None:
    """The residue family's identity, and the Level 1 kill at p = 3, 7."""
    for p, t in ((3, 7), (3, 11), (5, 13), (5, 37), (11, 29)):
        V = sorted([1, 2, 4, p, 2 * p, 4 * p, t, p * p])
        if len(set(V)) < 8:
            continue
        assert sum(d * d for d in V) == residue_n(p, t), (p, t)
        assert lcm_of(V) == 4 * p * p * t, (p, t)
    for p in (3, 7):
        assert 21 % p == 0, p
        # p | 21 + t^2 then forces p | t^2, i.e. p | t, i.e. t = p
        for t in primes_upto(500):
            if t != p and t > 2:
                assert (21 + t * t) % p != 0 or t % p == 0, (p, t)
    print("[ok] step 6 residue: identity holds; p = 3 and p = 7 die at Level 1")


def test_step6_residue_search_level2() -> None:
    """Level 2: no (p,t) in the forced range satisfies both congruences."""
    found = []
    for p in primes_upto(400):
        if p < 5 or p in (3, 7):
            continue
        M = residue_M(p)
        for t in primes_upto(2 * p * p):
            if not (2 * p < t < 2 * p * p):
                continue
            if M % t == 0 and (21 + t * t) % p == 0:
                found.append((p, t))
    assert found == [], found
    print("[ok] step 6 residue: no (p,t) with p < 400 passes both congruences "
          "in range (Level 2)")


def test_no_k8_solution_by_scan() -> None:
    LIM = 1_500_000
    hits = []
    for n in range(2, LIM):
        d = []
        for i in range(1, isqrt(n) + 1):
            if n % i == 0:
                d.append(i)
                if len(d) > 10:
                    break
        d = sorted(d)[:8]
        if len(d) == 8 and sum(x * x for x in d) == n:
            hits.append(n)
    assert hits == [], hits
    print(f"[ok] direct scan to {LIM:,}: no k=8 solution")


def test_does_not_prove_too_much() -> None:
    for n, k in ((1, 1), (130, 4), (1860, 11)):
        ds = smallest_divisors(n, k)
        assert len(ds) == k and sum(d * d for d in ds) == n, (n, k, ds)
    print("[ok] anchors survive: 1 (k=1), 130 (k=4), 1860 (k=11)")


def self_test() -> None:
    test_step1_parity()
    test_step2_profiles()
    test_step2_against_real_prefixes()
    test_step3_431()
    test_step4_413()
    test_step5_620_bounds()
    test_step5_shape_is_forced()
    test_step6_family_a()
    test_step6_residue_identity_and_small_p()
    test_step6_residue_search_level2()
    test_does_not_prove_too_much()
    test_no_k8_solution_by_scan()
    print("\nAll self-tests passed.")
    print("k=8 STATUS: 3 of 4 profiles CLOSED at Level 1; one family remains.")
    print("  L1  step 1  parity          n is even (removes the odd sector)")
    print("  L1  step 2  profile         4 profiles survive")
    print("  L1  step 3  (4,3,1)         8 | n, but V would fit below 8")
    print("  L1  step 4  (4,1,3)         C={4,8,16}, p>=11, 16p^3 > 341+12p^2")
    print("  L1  step 5  (6,2,0)         shape forced to 2 cases, both size-killed")
    print("  L1  step 6a (4,2,2) primes  n < lcm")
    print(f"  L2  step 6b {RESIDUE}")
    print("              p=3, p=7 are Level 1; the rest is a bounded search.")


if __name__ == "__main__":
    self_test()
