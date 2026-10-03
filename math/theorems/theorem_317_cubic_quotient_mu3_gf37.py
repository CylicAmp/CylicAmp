# CLASS: THEOREM
"""
Theorem 317: the cubic T(x)=x^3+33 descends to a 12-point graph on F_37*/mu_3,
and the (X,Y,Z) layout is a drawing of that quotient
Author: Michael Warren Song (CyclicAmp)

Advances T268's cubic (theorem_268_cubic_k3_33_gf37.py) one layer down.

=== THE RESULT ===

    T(x) = x^3 + 33 (mod 37).

    T(x) = T(y)  <=>  x^3 = y^3  <=>  x/y in mu_3 = {1, 10, 26}

    So the twelve mu_3-cosets ARE the fibres of T, and Y = T(x) is a COMPLETE
    INVARIANT of the coset. Cubing has image of size 36/gcd(3,36) = 12, so the
    twelve shelves are that image translated by 33:

        I = {cubes} + 33 = {2, 4, 6, 7, 10, 19, 22, 23, 25, 27, 32, 34}

    I is forward-invariant. The dynamics of all 36 units are T restricted to I,
    plus the fibre sitting over each shelf.

=== THE INDUCED MAP ON THE TWELVE SHELVES ===

    Two tails of length 3, one 6-cycle:

        2 -> 4 -> 23 -> 27
       22 -> 25 ->  7 ->  6
        6 -> 27 -> 32 -> 19 -> 10 -> 34 -> 6

    The cycle on I is the SAME C_6 as on the field -- not a smaller shadow of
    it. The six "deep" cosets are exactly the six tail shelves; the six
    "intersecting" cosets are exactly the six cycle shelves.

=== DEPTH IS GRAPH DISTANCE ===

    For any unit x NOT on the cycle:

        depth(x) = 1 + dist( T(x), C_6 )

    Zero exceptions over all 30 off-cycle units. Shelf 2 is three steps from
    the cycle, so its fibre {14, 29, 31} sits at X = 4 -- the maximum
    transient. Intersecting cosets hold one point already on C_6 (X=0) and two
    one step out (X=1), sharing one Y.

=== WHAT THIS EXPLAINS ===

    An injective (X, Y, Z) layout of all 36 units is a DRAWING of this
    quotient, not extra dynamics:

        Y  labels the 12-point graph          (the shelf)
        X  is graph-distance to C_6, plus one for the fibre
        Z  splits a fibre

    The layout's two collision shapes -- [0,1,1] needing a cycle-point rule,
    and [d,d,d] needing a {-delta, 0, +delta} split -- exist only downstairs.
    Upstairs there is one node per class and nothing to disambiguate. The
    layout convention and the quotient are ALTERNATIVES, not companions: the
    36-point picture carries strictly more information (it distinguishes a
    cycle point from its two preimages) at the cost of three arbitrary drawing
    choices to render it.

=== WHY THE DESCENT IS CLEAN ===

    Two conditions, both hold:
      1. T is constant on each coset -- shown above.
      2. [T(x)] is always defined: T(x) = 0 would need x^3 = -33 = 4, and 4 is
         NOT a cube mod 37 (the cubes are the index-3 subgroup of order 12).
         So T never lands on 0 and the quotient graph has no hole.

    0 itself is outside the map: T(0) = 33, and 33 is not one of the twelve
    shelves.

=== DEPTH COMPRESSION, AND WHY IT IS EXACTLY ONE ===

        downstairs [0,1,1] -> upstairs 0   (drop 0)
        downstairs [2,2,2] -> upstairs 1   (drop 1)
        downstairs [3,3,3] -> upstairs 2   (drop 1)
        downstairs [4,4,4] -> upstairs 3   (drop 1)
        max transient 4 -> 3

    The intersecting cosets lose nothing: their cycle point is already at
    depth 0, so merging it with its two depth-1 preimages leaves the class
    minimum at 0. Every deep coset drops exactly 1, because that same merge
    shortens every path running through the cycle point by one step.

=== SCOPE ===

    T|_I is forward-invariant but NOT a bijection on I (the two tails feed in;
    12 shelves have 10 distinct images). Nothing here claims it is.

    mu_3 in C and mu_3 in GF(37) share a cyclic group of order 3, and Z/3 is
    ubiquitous; that alone is a level-1 correspondence. What is specific is
    that GF(37)'s mu_3 is {1, 10, 26} = IC -- identity, base (10 = 26^-1), and
    26 = 137 mod 37 -- which follows from ord_37(26) = 3, the same fact that
    makes every 137-orbit a 3-cycle. The mu_3-cosets ARE the 137-orbits:
    orbit(x) = {x, 26x, 26^2 x} = x*mu_3. Shelf, coset and orbit are one
    partition seen three ways, which is why CLAUDE.md lists exactly 12 orbits.

=== FALSIFICATION ===
    Any assert below failing. In particular: a second cycle, a shelf outside
    I, an off-cycle unit whose depth is not 1 + dist(T(x), C_6), or T(0) != 33.
"""

P = 37
SHIFT = 33
MU3 = {1, 10, 26}
C6 = [6, 27, 32, 19, 10, 34]
I = [2, 4, 6, 7, 10, 19, 22, 23, 25, 27, 32, 34]


def T(x):
    return (pow(x, 3, P) + SHIFT) % P


def cosets():
    seen, out = set(), []
    for x in range(1, P):
        if x in seen:
            continue
        c = tuple(sorted(x * m % P for m in MU3))
        seen.update(c)
        out.append(c)
    return sorted(out)


def dist_to_cycle(y, cyc):
    d = 0
    while y not in cyc:
        y = T(y)
        d += 1
    return d


def functional_graph():
    succ = {x: T(x) for x in range(P)}
    cyc = set()
    for x in range(P):
        seen, y = [], x
        while y not in seen:
            seen.append(y)
            y = succ[y]
        cyc.update(seen[seen.index(y):])
    dep = {}
    for x in range(P):
        d, y = 0, x
        while y not in cyc:
            y = succ[y]
            d += 1
        dep[x] = d
    return succ, cyc, dep


def run():
    cs = cosets()
    succ, fcyc, fdep = functional_graph()

    # --- mu_3, and cosets = 137-orbits ---
    assert MU3 == {x for x in range(1, P) if pow(x, 3, P) == 1}
    assert 26 == 137 % P and 26 * 10 % P == 1
    assert len(cs) == 12 == (P - 1) // 3
    for c in cs:
        assert set(c) == {c[0] * m % P for m in MU3}
        assert set(c) == {c[0], 26 * c[0] % P, 26 * 26 * c[0] % P}   # 137-orbit

    # --- fibres of T are exactly the cosets; Y is a complete invariant ---
    for c in cs:
        assert len({T(x) for x in c}) == 1
    assert len({T(c[0]) for c in cs}) == 12
    for x in range(1, P):
        for y in range(1, P):
            assert (T(x) == T(y)) == (x * pow(y, P - 2, P) % P in MU3)

    # --- I = cubes + 33, forward-invariant, not a bijection ---
    cubes = {pow(x, 3, P) for x in range(1, P)}
    assert len(cubes) == 12 == (P - 1) // 3
    assert sorted((c + SHIFT) % P for c in cubes) == I
    assert sorted({T(c[0]) for c in cs}) == I
    assert {T(y) for y in I} <= set(I)
    assert len({T(y) for y in I}) == 10 < 12          # forward-inv, not bijective

    # --- the induced map: two tails of 3, one C_6 ---
    for tail in ([2, 4, 23, 27], [22, 25, 7, 6]):
        for a, b in zip(tail, tail[1:]):
            assert T(a) == b, (a, b)
    for i, v in enumerate(C6):
        assert T(v) == C6[(i + 1) % 6]
    assert set(C6) == fcyc                            # same C_6 as on the field
    assert len(fcyc) == 6

    # --- deep cosets are the tail shelves, intersecting are the cycle shelves
    deep = {c for c in cs if min(fdep[x] for x in c) >= 2}
    inter = {c for c in cs if sorted(fdep[x] for x in c) == [0, 1, 1]}
    assert len(deep) == len(inter) == 6
    assert deep | inter == set(cs)
    assert {T(c[0]) for c in inter} == set(C6)
    assert {T(c[0]) for c in deep} == set(I) - set(C6)

    # --- depth = 1 + dist(T(x), C_6), off the cycle. zero exceptions ---
    off = [x for x in range(1, P) if x not in fcyc]
    assert len(off) == 30
    for x in off:
        assert fdep[x] == 1 + dist_to_cycle(T(x), set(C6)), x
    assert dist_to_cycle(2, set(C6)) == 3
    assert sorted(x for x in range(1, P) if T(x) == 2) == [14, 29, 31]
    assert all(fdep[x] == 4 for x in (14, 29, 31))
    assert max(fdep[x] for x in range(1, P)) == 4

    # --- clean descent ---
    assert 4 not in cubes                              # x^3 = -33 = 4 unsolvable
    assert (-SHIFT) % P == 4
    assert not [x for x in range(1, P) if T(x) == 0]
    assert T(0) == SHIFT == 33 and 33 not in I         # 0 sits outside

    # --- the quotient graph, and one-level compression ---
    of = {x: c for c in cs for x in c}
    Tbar = {c: of[T(c[0])] for c in cs}
    qcyc = set()
    for c in cs:
        seen, y = [], c
        while y not in seen:
            seen.append(y)
            y = Tbar[y]
        qcyc.update(seen[seen.index(y):])
    qdep = {}
    for c in cs:
        d, y = 0, c
        while y not in qcyc:
            y = Tbar[y]
            d += 1
        qdep[c] = d
    assert len(qcyc) == 6
    assert max(qdep.values()) == 3 == max(fdep.values()) - 1
    for c in cs:
        lo = min(fdep[x] for x in c)
        assert qdep[c] == (0 if lo == 0 else lo - 1), c

    print("All assertions passed.\n")
    print(f"T(x) = x^3 + {SHIFT} mod {P}       fibres of T = mu_3-cosets = 137-orbits")
    print(f"I = cubes + {SHIFT} = {I}")
    print(f"  forward-invariant, |T(I)| = {len({T(y) for y in I})} < 12 "
          f"(not a bijection)\n")
    print("INDUCED MAP ON THE TWELVE SHELVES")
    print("   2 ->  4 -> 23 -> 27")
    print("  22 -> 25 ->  7 ->  6")
    print("   6 -> 27 -> 32 -> 19 -> 10 -> 34 -> 6   (the same C_6)\n")
    print(f"  {'coset':<16} {'Y':>3} {'X down':>10} {'X up':>5}  kind")
    for c in sorted(cs, key=lambda c: (qdep[c], T(c[0]))):
        ds = sorted(fdep[x] for x in c)
        kind = "intersecting" if c in inter else "deep"
        print(f"  {str(list(c)):<16} {T(c[0]):>3} {str(ds):>10} {qdep[c]:>5}  {kind}")
    print(f"\n  depth(x) = 1 + dist(T(x), C_6) for all {len(off)} off-cycle units,"
          f" 0 exceptions")
    print(f"  max transient 4 downstairs -> 3 upstairs; deep cosets drop 1,")
    print(f"  intersecting drop 0 (their cycle point already sits at 0)")


if __name__ == "__main__":
    run()
