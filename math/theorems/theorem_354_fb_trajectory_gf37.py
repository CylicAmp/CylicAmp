# CLASS: THEOREM
"""
Theorem 354: the f_b orbit of 18 is the f_a orbit pushed through C, term by
term -- because 18 is C's fixed point
Author: Michael Warren Song (CyclicAmp)

T353 corrected the f_a trajectory from 18.  The same computation for
f_b = C o T does not need to be run independently: the conjugacy determines
it, and the reason 18 is the convenient starting point is that C fixes it.

=== THE ORBIT ===

    f_a: 18 -> 19 ->  7 -> 25 ->  4 -> [10 ->  2 ->  6] -> ...
    f_b: 18 -> 21 -> 22 ->  2 -> 13 -> [31 ->  7 -> 19] -> ...

    f_b: PREPERIOD 5 INTO THE 3-CYCLE (31, 7, 19).

    Same preperiod, same cycle length as f_a.  That is forced, not
    observed: conjugate maps have identical orbit shape.

=== WHY IT IS THE SAME ORBIT PUSHED THROUGH C ===

    From T353, f_b = C o f_a o C^-1, hence f_b^n = C o f_a^n o C^-1 for
    every n.  So

        f_b^n(18) = C( f_a^n( C^-1(18) ) ).

    And C(18) = 3(18) + 1 = 55 == 18, so 18 is the fixed point of C and
    C^-1(18) = 18 as well.  The formula collapses to

        f_b^n(18) = C( f_a^n(18) )

    -- the f_b orbit of 18 is the f_a orbit of 18, mapped term by term
    through C.  Verified over thirteen terms:

        C[18, 19, 7, 25, 4, 10, 2, 6, ...]
          = [18, 21, 22, 2, 13, 31, 7, 19, ...]

    and the cycles correspond: C{10, 2, 6} = {31, 7, 19}.

    18 is the only starting point where the two orbits share a first term,
    precisely because it is the unique fixed point of C.

=== THE TWO MAPS HAVE IDENTICAL GLOBAL SHAPE ===

        map    cycle lengths      cycles                basins   max pre
        f_a    3 (x31), 1 (x6)    (2,6,10) and (27)     31, 6    5
        f_b    3 (x31), 1 (x6)    (7,19,31) and (8)     31, 6    5

    Every invariant agrees, and the two cycle sets correspond under C:
    C{2,6,10} = {7,19,31} and C(27) = 8.  Conjugacy guarantees all of it in
    advance; the table is a check, not a discovery.

=== WHAT WOULD HAVE BEEN A REAL FINDING ===

    Any difference between these two tables.  There is none, and there
    cannot be, so the f_b computation carries no information beyond f_a's.
    Recorded so it is not later cited as independent corroboration of the
    f_a result -- it is the same result in different coordinates.

=== FALSIFICATION ===
    A term where f_b^n(18) != C(f_a^n(18)); or any invariant above
    differing between the two maps.
"""

P = 37
T = lambda x: (pow(x, 3, P) + 33) % P
C = lambda x: (3 * x + 1) % P
Ci = lambda y: (25 * (y - 1)) % P
FA = lambda x: T(C(x))
FB = lambda x: C(T(x))


def census(f):
    info = {}
    for x in range(P):
        o = [x]
        for _ in range(40):
            o.append(f(o[-1]))
        seen = {}
        for i, v in enumerate(o):
            if v in seen:
                info[x] = (seen[v], i - seen[v], tuple(sorted(o[seen[v]:i])))
                break
            seen[v] = i
    return info


def orbit(f, x, n=12):
    o = [x]
    for _ in range(n):
        o.append(f(o[-1]))
    return o


def preperiod_cycle(o):
    idx = {}
    for i, v in enumerate(o):
        if v in idx:
            return idx[v], o[idx[v]:i]
        idx[v] = i
    return None, None


def run():
    from collections import Counter

    # --- 18 is C's fixed point ---
    assert C(18) == 18 == Ci(18)
    assert 3 * 18 + 1 == 55 and 55 % P == 18
    assert [x for x in range(P) if C(x) == x] == [18]

    # --- the two orbits ---
    oa, ob = orbit(FA, 18), orbit(FB, 18)
    assert oa == [18, 19, 7, 25, 4, 10, 2, 6, 10, 2, 6, 10, 2]
    assert ob == [18, 21, 22, 2, 13, 31, 7, 19, 31, 7, 19, 31, 7]
    assert [C(x) for x in oa] == ob            # term by term

    pa, ca = preperiod_cycle(oa)
    pb, cb = preperiod_cycle(ob)
    assert (pa, ca) == (5, [10, 2, 6])
    assert (pb, cb) == (5, [31, 7, 19])
    assert [C(x) for x in ca] == cb

    # --- the conjugacy gives it for every n ---
    for n in range(1, 15):
        x = 18
        for _ in range(n):
            x = FA(x)
        y = 18
        for _ in range(n):
            y = FB(y)
        assert y == C(x)
    assert all(FB(x) == C(FA(Ci(x))) for x in range(P))

    # --- identical global shape ---
    ia, ib = census(FA), census(FB)
    la = Counter(v[1] for v in ia.values())
    lb = Counter(v[1] for v in ib.values())
    assert dict(la) == dict(lb) == {3: 31, 1: 6}
    assert {v[2] for v in ia.values()} == {(2, 6, 10), (27,)}
    assert {v[2] for v in ib.values()} == {(7, 19, 31), (8,)}
    assert sorted(Counter(v[2] for v in ia.values()).values(),
                  reverse=True) == [31, 6]
    assert sorted(Counter(v[2] for v in ib.values()).values(),
                  reverse=True) == [31, 6]
    assert max(v[0] for v in ia.values()) == max(v[0] for v in ib.values()) == 5
    # the cycle sets correspond under C
    assert {C(x) for x in (2, 6, 10)} == {7, 19, 31}
    assert C(27) == 8

    print("All assertions passed.\n")
    print("THEOREM 354.  f_b's orbit of 18 is f_a's, pushed through C.\n")
    print(f"   f_a: {' -> '.join(map(str,oa[:8]))} -> ...")
    print(f"   f_b: {' -> '.join(map(str,ob[:8]))} -> ...\n")
    print(f"   f_b: preperiod {pb}, 3-cycle {cb}\n")
    print("   C(18) = 55 == 18, so 18 is C's UNIQUE fixed point, and")
    print("   f_b^n(18) = C(f_a^n(C^-1(18))) = C(f_a^n(18)).")
    print(f"   C applied termwise: {[C(x) for x in oa[:8]]}")
    print(f"   equals the f_b orbit: {ob[:8]}\n")
    print("  IDENTICAL GLOBAL SHAPE, GUARANTEED IN ADVANCE")
    print("   map   lengths          cycles                basins  max pre")
    print(f"   f_a   {dict(la)}   (2,6,10) and (27)     31, 6   5")
    print(f"   f_b   {dict(lb)}   (7,19,31) and (8)     31, 6   5")
    print(f"   C{{2,6,10}} = {{7,19,31}}, C(27) = {C(27)}\n")
    print("   Conjugacy forces every line of that table. The f_b computation")
    print("   carries no information beyond f_a's -- same result, different")
    print("   coordinates. Recorded so it is not later cited as independent")
    print("   corroboration.")


if __name__ == "__main__":
    run()
